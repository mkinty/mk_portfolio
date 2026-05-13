from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from apps.education.selectors.education_selectors import (
    EducationSectionSelectors,
    EducationSelectors,
)
from apps.education.services.education_services import (
    EducationSectionServices,
    EducationServices,
)
from apps.users.selectors.user_selectors import get_user_by_id


class EducationSectionAddView(View):
    template_name = "education/section_form.html"
    title = "Ajouter une section d'éducation"

    def get(self, request, user_id):
        form, user_obj = EducationSectionServices.get_add_form(user_id)
        context = {
            "form": form,
            "user_obj": user_obj,
            "title": self.title,
        }
        return render(request, self.template_name, context)

    def post(self, request, user_id):
        user_obj = get_user_by_id(user_id)

        success, form, education_section = EducationSectionServices.create(
            user_obj,
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs.")
            context = {
                "form": form,
                "user_obj": user_obj,
                "title": self.title,
            }
            return render(request, self.template_name, context)

        messages.success(request, "Section d'éducation ajoutée.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class EducationSectionUpdateView(View):
    """
    Update an education_section.
    - GET: show form
    - POST: update skill
    """

    template_name = "education/section_form.html"
    title = "Modifier une section d'éducation"

    def get(self, request, education_section_id):
        """Show update form."""
        form, education_section = EducationSectionServices.get_update_form(
            education_section_id
        )

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "education_section": education_section,
                "title": self.title,
            },
        )

    def post(self, request, education_section_id):
        """Handle update."""
        success, form, education_section = EducationSectionServices.update(
            education_section_id, request.POST, request.FILES
        )

        if not success:
            messages.error(request, "Corrigez les erreurs.")
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "education_section": education_section,
                    "title": self.title,
                },
            )

        messages.success(request, "Section d'éducation mise à jour.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class EducationSectionDeleteView(View):
    """
    Delete a skill.
    - GET: confirmation page
    - POST: delete skill
    """

    template_name = "education/section_delete_confirm.html"
    title = "Supprimer une section d'éducation"

    def get(self, request, education_section_id):
        """Show confirmation page."""
        education_section = EducationSectionSelectors.get_education_section_by_id(
            education_section_id
        )

        return render(
            request,
            self.template_name,
            {
                "education_section": education_section,
                "title": self.title,
            },
        )

    def post(self, request, education_section_id):
        """Delete experience."""

        EducationSectionServices.delete(education_section_id)

        messages.success(request, "Section d'éducation supprimée.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class EducationAddView(View):
    template_name = "education/form.html"
    title = "Ajouter un parcours d'éducation"

    def get(self, request, education_section_id):
        form, education_section = EducationServices.get_add_form(education_section_id)
        context = {
            "form": form,
            "education_section": education_section,
            "title": self.title,
        }
        return render(request, self.template_name, context)

    def post(self, request, education_section_id):
        education_section = EducationSectionSelectors.get_education_section_by_id(
            education_section_id
        )

        success, form, education = EducationServices.create(
            education_section,
            request.POST,
            request.FILES,
        )

        if not success:
            messages.error(request, "Corrigez les erreurs.")
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "education_section": education_section,
                    "title": self.title,
                },
            )

        messages.success(request, "Parcours d'éducation ajouté.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class EducationUpdateView(View):
    """
    Update an education.
    - GET: show form
    - POST: update skill
    """

    template_name = "education/form.html"
    title = "Modifier un parcours d'éducation"

    def get(self, request, education_id):
        """Show update form."""
        form, education = EducationServices.get_update_form(education_id)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "education": education,
                "title": self.title,
            },
        )

    def post(self, request, education_id):
        """Handle update."""
        success, form, education = EducationServices.update(
            education_id, request.POST, request.FILES
        )

        if not success:
            messages.error(request, "Corrigez les erreurs.")
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "education": education,
                    "title": self.title,
                },
            )

        messages.success(request, "Parcours d'éducation mis à jour.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class EducationDeleteView(View):
    """
    Delete an education.
    - GET: confirmation page
    - POST: delete education
    """

    template_name = "education/delete_confirm.html"
    title = "Suppprimer le parcours d'éducation"

    def get(self, request, education_id):
        """Show confirmation page."""
        education = EducationSelectors.get_education_by_id(education_id)

        return render(
            request,
            self.template_name,
            {
                "education": education,
                "title": self.title,
            },
        )

    def post(self, request, education_id):
        """Delete experience."""

        EducationServices.delete(education_id)

        messages.success(request, "Parcours d'éducation supprimé.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})
