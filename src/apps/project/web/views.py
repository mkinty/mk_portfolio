from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import View

from apps.project.selectors.projects_selectors import (
    ProjectSelectors,
    ProjectCategorySelectors,
    TagSelectors
)
from apps.project.services.projects_services import (
    ProjectCategoryServices,
    ProjectServices,
    TagServices
)
from apps.users.selectors.user_selectors import get_user_by_id


class ProjectIndexView(View):
    template_name = "project/project_index.html"

    def get(self, request, user_id):
        user_obj = get_user_by_id(user_id)
        categories = ProjectCategorySelectors.get_project_categories()
        tags = TagSelectors.get_tags()
        categories.navbar_url = reverse_lazy('project:index', kwargs={'user_id': user_id})
        context = {
            "categories": categories,
            "projects": categories,
            "tags": tags,
            "user_obj": user_obj,
        }
        return render(request, self.template_name, context)


class ProjectsView(View):
    template_name = "project/projects_list.html"

    def get(self, request, user_id):
        user_obj = get_user_by_id(user_id)
        projects = ProjectSelectors.get_projects()
        projects.navbar_url = reverse_lazy('projects:list', kwargs={'user_id': user_id})

        category_id = request.GET.get('category')
        tag_ids = request.GET.getlist('tags')
        query = request.GET.get('qs', '')

        if category_id:
            projects = projects.filter(category_id=category_id)

        if tag_ids:
            projects = projects.filter(tags__id__in=tag_ids).distinct()

        if query:
            queryset = (Q(title__icontains=query) | Q(description__icontains=query))
            projects = projects.filter(queryset).distinct()

        context = {
            "projects": projects,
            "user_obj": user_obj,
        }
        return render(request, self.template_name, context)


class ProjectDetailIndexView(View):
    template_name = "project/project_detail_index.html"

    def get(self, request, project_id):
        project = ProjectSelectors.get_project_by_id(project_id)
        projects = ProjectSelectors.get_projects()
        projects.navbar_url = reverse_lazy('project:detail-index', kwargs={'project_id': project_id})
        context = {
            "projects": projects,
            "project": project,
            "user_obj": project.user,
        }
        return render(request, self.template_name, context)


class ProjectDetailView(View):
    template_name = "project/project_detail.html"

    def get(self, request, project_id):
        project = ProjectSelectors.get_project_by_id(project_id)
        projects = ProjectSelectors.get_projects()
        projects.navbar_url = reverse_lazy('projects:detail', kwargs={'project_id': project_id})
        print("project.category", project.category)
        context = {
            "projects": projects,
            "project": project,
            "current_project": project,
            "current_category": project.category,
            "user_obj": project.user,
        }
        return render(request, self.template_name, context)


class ProjectCategoryAddView(View):
    """View for adding a new project category."""

    template_name = "project/category_form.html"
    title = "Ajouter une catégorie de projet"

    def get(self, request, user_id):
        """Display the creation form"""

        form, user_obj = ProjectCategoryServices.get_add_form(user_id)

        return render(request, self.template_name, {"form": form, "user_obj": user_obj, "title": self.title})

    def post(self, request, user_id):
        """Handle form submission"""
        user_obj = get_user_by_id(user_id)
        success, form, user_obj = ProjectCategoryServices.create(
            user_obj,
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs dans le formulaire")
            return render(request, self.template_name, {
                "form": form,
                "user_obj": user_obj,
                "title": self.title
            })

        messages.success(request, "Catégorie de projet créée avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class ProjectCategoryUpdateView(View):
    """View for updating a project category."""

    template_name = "project/category_form.html"
    title = "Modifier une catégorie de projet"

    def get(self, request, category_id):
        """Display the update form"""

        form, category = ProjectCategoryServices.get_update_form(category_id)

        return render(request, self.template_name, {
            "form": form,
            "category": category,
            "user_obj": category.user,
            "title": self.title
        })

    def post(self, request, category_id):
        """Handle form submission"""
        success, form, category = ProjectCategoryServices.update(
            category_id,
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs dans le formulaire")
            return render(request, self.template_name, {
                "form": form,
                "category": category,
                "user_obj": category.user,
                "title": self.title
            })

        messages.success(request, "Catégorie de projet modifiée avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class ProjectCategoryDeleteView(View):
    """View for deleting a project category."""

    template_name = "project/category_delete_confirm.html"
    title = "Supprimer une catégorie de projet"

    def get(self, request, category_id):
        """Display the confirmation page"""
        category = ProjectCategorySelectors.get_project_category_by_id(category_id)
        return render(request, self.template_name, {"category": category, "title": self.title})

    def post(self, request, category_id):
        """Handle deletion"""
        success = ProjectCategoryServices.delete(category_id)

        if not success:
            messages.error(request, "Erreur lors de la suppression")
            return HttpResponse(status=400)

        messages.success(request, "Catégorie de projet supprimée avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class TagAddView(View):
    """View for adding a new tag."""

    template_name = "project/tag_form.html"
    title = "Ajouter un tag"

    def get(self, request):
        """Display the add tag form"""
        form = TagServices.get_add_form()
        return render(request, self.template_name, {
            "form": form,
            "title": self.title
        })

    def post(self, request):
        """Handle form submission"""
        success, form, tag = TagServices.create(
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs dans le formulaire")
            return render(request, self.template_name, {
                "form": form,
                "title": self.title
            })

        messages.success(request, "Tag ajouté avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class TagUpdateView(View):
    """View for updating a tag."""

    template_name = "project/tag_form.html"
    title = "Modifier un tag"

    def get(self, request, tag_id):
        """Display the update tag form"""
        form, tag = TagServices.get_update_form(tag_id)
        return render(request, self.template_name, {
            "form": form,
            "tag": tag,
            "title": self.title
        })

    def post(self, request, tag_id):
        """Handle form submission"""
        success, form, tag = TagServices.update(
            tag_id,
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs dans le formulaire")
            return render(request, self.template_name, {
                "form": form,
                "tag": tag,
                "title": self.title
            })

        messages.success(request, "Tag modifié avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class TagDeleteView(View):
    """View for deleting a tag."""

    template_name = "project/tag_delete_confirm.html"
    title = "Supprimer un tag"

    def get(self, request, tag_id):
        """Display the delete tag confirmation"""
        tag = TagSelectors.get_tag_by_id(tag_id)
        return render(request, self.template_name, {
            "tag": tag,
            "title": self.title
        })

    def post(self, request, tag_id):
        """Handle form submission"""
        success = TagServices.delete(tag_id)

        if not success:
            messages.error(request, "Erreur lors de la suppression")
            return HttpResponse(status=400)

        messages.success(request, "Tag supprimé avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class ProjectAddView(View):
    """View for adding a new project."""

    template_name = "project/form.html"
    title = "Ajouter un projet"

    def get(self, request, user_id):
        """Display the add project form"""
        form, user_obj = ProjectServices.get_add_form(user_id)
        return render(request, self.template_name, {
            "form": form,
            "user_obj": user_obj,
            "title": self.title
        })

    def post(self, request, user_id):
        """Handle form submission"""
        user_obj = get_user_by_id(user_id)
        success, form, project = ProjectServices.create(
            user_obj,
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs dans le formulaire")
            return render(request, self.template_name, {
                "form": form,
                "user_obj": user_obj,
                "title": self.title
            })

        messages.success(request, "Projet créé avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class ProjectUpdateView(View):
    """View for updating a project."""

    template_name = "project/form.html"
    title = "Modifier un projet"

    def get(self, request, project_id):
        """Display the update project form"""
        form, project = ProjectServices.get_update_form(project_id)
        return render(request, self.template_name, {
            "form": form,
            "project": project,
            "user_obj": project.user,
            "title": self.title
        })

    def post(self, request, project_id):
        """Handle form submission"""
        success, form, project = ProjectServices.update(
            project_id,
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs dans le formulaire")
            return render(request, self.template_name, {
                "form": form,
                "project": project,
                "user_obj": project.user,
                "title": self.title
            })

        messages.success(request, "Projet modifié avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class ProjectDeleteView(View):
    """View for deleting a project."""
    template_name = "project/delete_confirm.html"
    title = "Supprimer un projet"

    def get(self, request, project_id):
        """Display the delete confirmation form"""
        project = ProjectSelectors.get_project_by_id(project_id)
        return render(request, self.template_name, {
            "project": project,
            "title": self.title
        })

    def post(self, request, project_id):
        """Handle delete request"""
        success = ProjectServices.delete(project_id)

        if not success:
            messages.error(request, "Erreur lors de la suppression du projet")
            return HttpResponse(status=400)

        messages.success(request, "Projet supprimé avec succès")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})
