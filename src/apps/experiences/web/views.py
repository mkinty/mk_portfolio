from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from apps.experiences.selectors.experiences_selectors import get_experience_by_id
from apps.experiences.services.experiences_services import ExperienceService
from apps.users.selectors.user_selectors import get_user_by_id


class ExperienceAddView(View):
    """
    Create a new experience.
    - GET: show form
    - POST: save experience
    """

    template_name = "experiences/form.html"
    title = "Ajouter une expérience"

    def get(self, request, user_id):
        """Display the creation form."""
        form, user_obj = ExperienceService.get_add_form(user_id)

        return render(request, self.template_name, {
            "form": form,
            "user_obj": user_obj,
            "title": self.title,
        })

    def post(self, request, user_id):
        """Handle form submission."""
        user_obj = get_user_by_id(user_id)

        success, form, experience = ExperienceService.create(
            user_obj,
            request.POST,
            request.FILES
        )

        if not success:
            messages.error(request, "Corrigez les erreurs.")
            return render(request, self.template_name, {
                "form": form,
                "user_obj": user_obj,
                "title": self.title,
            })

        messages.success(request, "Expérience ajoutée.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class ExperienceUpdateView(View):
    """
    Update an experience.
    - GET: show form
    - POST: update experience
    """

    template_name = "experiences/form.html"
    title = "Modifier l'expérience"

    def get(self, request, experience_id):
        """Show update form."""
        form, experience = ExperienceService.get_update_form(experience_id)

        return render(request, self.template_name, {
            "form": form,
            "experience": experience,
            "title": self.title,
        })

    def post(self, request, experience_id):
        """Handle update."""
        success, form, experience = ExperienceService.update(
            experience_id,
            request.POST,
            request.FILES
        )

        if not success:
            messages.error(request, "Corrigez les erreurs.")
            return render(request, self.template_name, {
                "form": form,
                "experience": experience,
                "title": self.title,
            })

        messages.success(request, "Expérience mise à jour.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class ExperienceDeleteView(View):
    """
    Delete an experience.
    - GET: confirmation page
    - POST: delete experience
    """

    template_name = "experiences/delete_confirm.html"
    title = "Supprimer l'expérience"

    def get(self, request, experience_id):
        """Show confirmation page."""
        experience = get_experience_by_id(experience_id)

        return render(request, self.template_name, {
            "experience": experience,
            "title": self.title,
        })

    def post(self, request, experience_id):
        """Delete experience."""
        experience = get_experience_by_id(experience_id)

        ExperienceService.delete(experience)

        messages.success(request, "Expérience supprimée.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})
