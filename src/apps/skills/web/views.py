from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from apps.skills.selectors.skills_selectors import SkillsSelectors
from apps.skills.services.skills_servives import SkillsService
from apps.users.selectors.user_selectors import get_user_by_id


class SkillAddView(View):
    """
    Create a new skill.
    - GET: show form
    - POST: save skill
    """

    template_name = "skills/form.html"
    title = "Ajouter une categorie de compétences"

    def get(self, request, user_id):
        """Display the creation form."""
        form, user_obj = SkillsService.get_add_form(user_id)

        return render(request, self.template_name, {
            "form": form,
            "user_obj": user_obj,
            "title": self.title,
        })

    def post(self, request, user_id):
        """Handle form submission."""
        user_obj = get_user_by_id(user_id)

        success, form, skill = SkillsService.create(
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

        messages.success(request, "Catégorie de compétences ajoutée.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class SkillUpdateView(View):
    """
    Update a skill.
    - GET: show form
    - POST: update skill
    """

    template_name = "skills/form.html"
    title = "Modifier la catégorie de compétences"

    def get(self, request, skill_id):
        """Show update form."""
        form, skill = SkillsService.get_update_form(skill_id)

        return render(request, self.template_name, {
            "form": form,
            "skill": skill,
            "title": self.title,
        })

    def post(self, request, skill_id):
        """Handle update."""
        success, form, skill = SkillsService.update(
            skill_id,
            request.POST,
            request.FILES
        )

        if not success:
            messages.error(request, "Corrigez les erreurs.")
            return render(request, self.template_name, {
                "form": form,
                "skill": skill,
                "title": self.title,
            })

        messages.success(request, "Expérience mise à jour.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class SkillDeleteView(View):
    """
    Delete a skill.
    - GET: confirmation page
    - POST: delete skill
    """

    template_name = "skills/delete_confirm.html"
    title = "Supprimer la catégorie de compétences"

    def get(self, request, skill_id):
        """Show confirmation page."""
        skill = SkillsSelectors.get_skill_by_id(skill_id)

        return render(request, self.template_name, {
            "skill": skill,
            "title": self.title,
        })

    def post(self, request, skill_id):
        """Delete experience."""

        SkillsService.delete(skill_id)

        messages.success(request, "Catégorie de compétences supprimée.")
        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})
