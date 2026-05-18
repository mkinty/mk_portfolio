from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from apps.blog.selectors.posts_selectors import (
    PostCategorySelectors,
    PostSelectors,
    PostTagSelectors,
)
from apps.blog.services.posts_services import (
    PostCategoryServices,
    PostServices,
    PostTagServices,
)
from apps.users.selectors.user_selectors import get_user_by_id
from apps.utils.services.http_responses import HTTPResponseHXRedirect


class PostsIndexView(View):
    template_name = "blog/posts_index.html"

    def get(self, request, user_id):
        user_obj = get_user_by_id(user_id)
        categories = PostCategorySelectors.get_post_categories()
        tags = PostTagSelectors.get_post_tags()
        categories.navbar_url = reverse_lazy("blog:index", kwargs={"user_id": user_id})
        articles = PostSelectors.get_posts()
        articles.navbar_url = reverse_lazy("blog:index", kwargs={"user_id": user_id})

        context = {
            "categories": categories,
            "articles": articles,
            "tags": tags,
            "user_obj": user_obj,
        }
        return render(request, self.template_name, context)


class PostsView(View):
    template_name = "blog/posts_list.html"

    def get(self, request, user_id):
        user_obj = get_user_by_id(user_id)
        articles = PostSelectors.get_posts()

        category_id = request.GET.get("category")
        tag_ids = request.GET.getlist("tags")
        query = request.GET.get("qs", "")

        if category_id:
            articles = articles.filter(category__id=category_id)

        if tag_ids:
            articles = articles.filter(tags__id__in=tag_ids).distinct()

        if query:
            articles = articles.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).distinct()

        # Nombre d'articles
        nb_articles = (
            f"{len(articles)} Articles"
            if len(articles) > 1
            else f"{len(articles)} Article"
        )

        context = {
            "articles": articles,
            "nb_articles": nb_articles,
            "user_obj": user_obj,
        }
        return render(request, self.template_name, context)


class PostDetailIndexView(View):
    template_name = "blog/post_detail_index.html"

    def get(self, request, post_id):
        article = PostSelectors.get_post_by_id(post_id)
        articles = PostSelectors.get_posts()
        articles.navbar_url = reverse_lazy(
            "blog:detail-index", kwargs={"post_id": post_id}
        )
        context = {
            "article": article,
            "articles": articles,
            "user_obj": article.user,
        }
        return render(request, self.template_name, context)


class PostDetailView(View):
    template_name = "blog/post_detail.html"

    def get(self, request, post_id):
        article = PostSelectors.get_post_by_id(post_id)
        categories = PostCategorySelectors.get_post_categories().prefetch_related(
            "articles"
        )
        articles = PostSelectors.get_posts()

        context = {
            "article": article,
            "categories": categories,
            "articles": articles,
            "current_article": article,
            "current_category": article.category,
            "user_obj": article.user,
        }
        return render(request, self.template_name, context)


class PostCategoryAddView(View):
    """View for adding a new post category."""

    template_name = "blog/category_form.html"
    title = "Ajouter une catégorie d'articles"

    def get(self, request, user_id):
        """Display the creation form"""

        form, user_obj = PostCategoryServices.get_add_form(user_id)

        return render(
            request,
            self.template_name,
            {"form": form, "user_obj": user_obj, "title": self.title},
        )

    def post(self, request, user_id):
        """Handle form submission"""
        user_obj = get_user_by_id(user_id)
        success, form, user_obj = PostCategoryServices.create(
            user_obj,
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs dans le formulaire")
            return render(
                request,
                self.template_name,
                {"form": form, "user_obj": user_obj, "title": self.title},
            )

        messages.success(request, "Catégorie d'articles' créée avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class PostCategoryUpdateView(View):
    """View for updating a post category."""

    template_name = "blog/category_form.html"
    title = "Modifier une catégorie d'articles"

    def get(self, request, category_id):
        """Display the update form"""

        form, category = PostCategoryServices.get_update_form(category_id)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "category": category,
                "user_obj": category.user,
                "title": self.title,
            },
        )

    def post(self, request, category_id):
        """Handle form submission"""
        success, form, category = PostCategoryServices.update(
            category_id,
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs dans le formulaire")
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "category": category,
                    "user_obj": category.user,
                    "title": self.title,
                },
            )

        messages.success(request, "Catégorie d'articles' modifiée avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class PostCategoryDeleteView(View):
    """View for deleting a post category."""

    template_name = "blog/category_delete_confirm.html"
    title = "Supprimer une catégorie d'articles"

    def get(self, request, category_id):
        """Display the confirmation page"""
        category = PostCategorySelectors.get_post_category_by_id(category_id)
        return render(
            request, self.template_name, {"category": category, "title": self.title}
        )

    def post(self, request, category_id):
        """Handle deletion"""
        success = PostCategoryServices.delete(category_id)

        if not success:
            messages.error(request, "Erreur lors de la suppression")
            return HttpResponse(status=400)

        messages.success(request, "Catégorie d'articles supprimée avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class PostTagAddView(View):
    """View for adding a new post tag."""

    template_name = "blog/tag_form.html"
    title = "Ajouter un tag"

    def get(self, request):
        """Display the add post tag form"""
        form = PostTagServices.get_add_form()
        return render(request, self.template_name, {"form": form, "title": self.title})

    def post(self, request):
        """Handle form submission"""
        success, form, tag = PostTagServices.create(
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs dans le formulaire")
            return render(
                request, self.template_name, {"form": form, "title": self.title}
            )

        messages.success(request, "Tag ajouté avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class PostTagUpdateView(View):
    """View for updating a post tag."""

    template_name = "blog/tag_form.html"
    title = "Modifier un tag"

    def get(self, request, tag_id):
        """Display the update post tag form"""
        form, tag = PostTagServices.get_update_form(tag_id)
        return render(
            request, self.template_name, {"form": form, "tag": tag, "title": self.title}
        )

    def post(self, request, tag_id):
        """Handle form submission"""
        success, form, tag = PostTagServices.update(
            tag_id,
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs dans le formulaire")
            return render(
                request,
                self.template_name,
                {"form": form, "tag": tag, "title": self.title},
            )

        messages.success(request, "Tag modifié avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class PostTagDeleteView(View):
    """View for deleting a post tag."""

    template_name = "blog/tag_delete_confirm.html"
    title = "Supprimer un tag"

    def get(self, request, tag_id):
        """Display the delete post tag confirmation"""
        tag = PostTagSelectors.get_post_tag_by_id(tag_id)
        return render(request, self.template_name, {"tag": tag, "title": self.title})

    def post(self, request, tag_id):
        """Handle form submission"""
        success = PostTagServices.delete(tag_id)

        if not success:
            messages.error(request, "Erreur lors de la suppression")
            return HttpResponse(status=400)

        messages.success(request, "Tag supprimé avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class PostAddView(View):
    """View for adding a new post."""

    template_name = "blog/form.html"
    title = "Ajouter un article"

    def get(self, request, user_id):
        """Display the add project form"""
        form, user_obj = PostServices.get_add_form(user_id)
        return render(
            request,
            self.template_name,
            {"form": form, "user_obj": user_obj, "title": self.title},
        )

    def post(self, request, user_id):
        """Handle form submission"""
        user_obj = get_user_by_id(user_id)
        success, form, project = PostServices.create(
            user_obj,
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs dans le formulaire")
            return render(
                request,
                self.template_name,
                {"form": form, "user_obj": user_obj, "title": self.title},
            )

        messages.success(request, "Article créé avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class PostUpdateView(View):
    """View for updating a project."""

    template_name = "blog/form.html"
    title = "Modifier un article"

    def get(self, request, post_id):
        """Display the update project form"""
        form, article = PostServices.get_update_form(post_id)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "article": article,
                "user_obj": article.user,
                "title": self.title,
            },
        )

    def post(self, request, post_id):
        """Handle form submission"""
        success, form, article = PostServices.update(
            post_id,
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs dans le formulaire")
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "article": article,
                    "user_obj": article.user,
                    "title": self.title,
                },
            )

        messages.success(request, "Article modifié avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class PostDeleteView(View):
    """View for deleting a project."""

    template_name = "blog/delete_confirm.html"
    title = "Supprimer un article"

    def get(self, request, post_id):
        """Display the delete confirmation form"""
        article = PostSelectors.get_post_by_id(post_id)
        return render(
            request, self.template_name, {"article": article, "title": self.title}
        )

    def post(self, request, post_id):
        """Handle delete request"""
        article = PostSelectors.get_post_by_id(post_id)
        user_id = article.user.id
        success = PostServices.delete(post_id)

        if not success:
            messages.error(request, "Erreur lors de la suppression de l'article")
            return HttpResponse(status=400)

        messages.success(request, "Article supprimé avec succès")
        return HTTPResponseHXRedirect(
            reverse_lazy("blog:index", kwargs={"user_id": user_id})
        )
