from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from apps.techstack.selectors.techstack_selectors import (
    TechStackCategorySelectors,
    TechStackSelectors,
)
from apps.techstack.services.techstack_servives import (
    TechStackCategoryServices,
    TechStackServices,
)
from apps.users.selectors.user_selectors import get_user_by_id


class TechStackCategoryAddView(View):
    """
    Create a new tech stack category.
    - GET: show form
    - POST: save tech stack category
    """

    template_name = "techstack/category_form.html"
    title = "Ajouter une categorie de stack technique"

    def get(self, request, user_id):
        """Display the creation form."""
        form, user_obj = TechStackCategoryServices.get_add_form(user_id)

        return render(
            request,
            self.template_name,
            {"form": form, "user_obj": user_obj, "title": self.title},
        )

    def post(self, request, user_id):
        """Handle form submission."""
        user_obj = get_user_by_id(user_id)

        success, form, skill = TechStackCategoryServices.create(
            user_obj, request.POST, request.FILES
        )

        if not success:
            messages.error(request, "Corrigez les erreurs.")
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "user_obj": user_obj,
                    "title": self.title,
                },
            )

        messages.success(request, "Catégorie de stack technique ajoutée.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class TechStackCategoryUpdateView(View):
    """
    Update a tech stack category.
    - GET: show form
    - POST: update tech stack category
    """

    template_name = "techstack/category_form.html"
    title = "Modifier la catégorie de stack technique"

    def get(self, request, tech_category_id):
        """Show update form."""
        form, tech_category = TechStackCategoryServices.get_update_form(
            tech_category_id
        )

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "tech_category": tech_category,
                "user_obj": tech_category.user,
                "title": self.title,
            },
        )

    def post(self, request, tech_category_id):
        """Handle update."""
        success, form, tech_category = TechStackCategoryServices.update(
            tech_category_id, request.POST, request.FILES
        )

        if not success:
            messages.error(request, "Corrigez les erreurs.")
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "tech_category": tech_category,
                    "user_obj": tech_category.user,
                    "title": self.title,
                },
            )

        messages.success(request, "Catégorie de stack technique mise à jour.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class TechStackCategoryDeleteView(View):
    """
    Delete a techstack.
    - GET: confirmation page
    - POST: delete techstack
    """

    template_name = "techstack/category_delete_confirm.html"
    title = "Supprimer la catégorie"

    def get(self, request, tech_category_id):
        """Show confirmation page."""
        tech_category = TechStackCategorySelectors.get_techstack_category_by_id(
            tech_category_id
        )

        return render(
            request,
            self.template_name,
            {
                "tech_category": tech_category,
                "user_obj": tech_category.user,
                "title": self.title,
            },
        )

    def post(self, request, tech_category_id):
        """Delete experience."""

        TechStackCategoryServices.delete(tech_category_id)

        messages.success(request, "Catégorie de stack technique supprimée.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class TechStackAddView(View):
    """
    Create a new tech stack.
    - GET: show form
    - POST: save tech stack
    """

    template_name = "techstack/form.html"
    title = "Ajouter une stack technique"

    def get(self, request, user_id):
        """Display the creation form."""
        form, user_obj = TechStackServices.get_add_form(user_id)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "user_obj": user_obj,
                "title": self.title,
            },
        )

    def post(self, request, user_id):
        """Handle form submission."""
        user_obj = get_user_by_id(user_id)

        success, form, skill = TechStackServices.create(
            user_obj, request.POST, request.FILES
        )

        if not success:
            messages.error(request, "Corrigez les erreurs.")

            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "user_obj": user_obj,
                    "title": self.title,
                },
            )

        messages.success(request, "Stack technique ajoutée.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class TechStackUpdateView(View):
    """
    Update a tech stack.
    - GET: show form
    - POST: update tech stack
    """

    template_name = "techstack/form.html"
    title = "Modifier la stack technique"

    def get(self, request, tech_stack_id):
        """Show update form."""
        form, tech_stack = TechStackServices.get_update_form(tech_stack_id)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "tech_stack": tech_stack,
                "user_obj": tech_stack.user,
                "title": self.title,
            },
        )

    def post(self, request, tech_stack_id):
        """Handle update."""
        success, form, tech_stack = TechStackServices.update(
            tech_stack_id, request.POST, request.FILES
        )

        if not success:
            messages.error(request, "Corrigez les erreurs.")
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "tech_stack": tech_stack,
                    "user_obj": tech_stack.user,
                    "title": self.title,
                },
            )

        messages.success(request, "Stack technique mise à jour.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class TechStackDeleteView(View):
    """
    Delete a techstack.
    - GET: confirmation page
    - POST: delete techstack
    """

    template_name = "techstack/delete_confirm.html"
    title = "Supprimer la stack technique"

    def get(self, request, tech_stack_id):
        """Show confirmation page."""
        tech_stack = TechStackSelectors.get_tech_stack_by_id(tech_stack_id)

        return render(
            request,
            self.template_name,
            {
                "tech_stack": tech_stack,
                "title": self.title,
            },
        )

    def post(self, request, tech_stack_id):
        """Delete experience."""

        TechStackServices.delete(tech_stack_id)

        messages.success(request, "Stack technique supprimée.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})
