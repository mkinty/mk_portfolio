from django.contrib import messages
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views import View

from apps.education.selectors.education_selectors import EducationSectionSelectors, EducationSelectors
from apps.experiences.selectors.experiences_selectors import get_all_experiences
from apps.skills.selectors.skills_selectors import SkillsSelectors
from apps.userprofile.services.userprofile_services import UserProfileService
from apps.users.selectors.user_selectors import get_user_by_id
from apps.userprofile.selectors.userprofile_selectors import (
    get_userprofile_by_id,
    get_userprofile_by_user
)


class UserProfileIndexView(View):
    """
    User profile dashboard page.
    Displays user and profile overview.
    """

    template_name = "userprofile/userprofile_index.html"

    def get(self, request: HttpRequest, user_id: int) -> HttpResponse:
        """
        Handle GET request for the user profile index page.

        Args:
            request (HttpRequest): Incoming HTTP request.
            user_id (int): ID of the user to retrieve.

        Returns:
            HttpResponse: Rendered user profile index page.

        Notes:
            - Uses `get_user_by_id` selector/service to retrieve the user.
            - No business logic is handled in this view.
            - The template receives `user_obj` in context.
        """
        user_obj = get_user_by_id(user_id)
        userprofile = get_userprofile_by_user(user_obj)
        userprofile.navbar_url = reverse_lazy('userprofile:index', kwargs={'user_id': user_id})
        context = {
            "user_obj": user_obj,
            "userprofile": userprofile
        }
        return render(request, self.template_name, context)


class UserProfileView(View):
    """
    Display a user profile page.

    Shows profile details or fallback page if not found.
    """

    template_name = "userprofile/userprofile.html"

    def get(self, request: HttpRequest, user_id: int) -> HttpResponse:
        """Handle GET request to display a user profile."""
        user_obj = get_user_by_id(user_id)
        userprofile = get_userprofile_by_user(user_obj)
        experiences = get_all_experiences(user_obj)
        skills = SkillsSelectors.get_all_skills(user_obj)
        education_sections = EducationSectionSelectors.get_all_education_sections(user_obj)

        if not userprofile:
            messages.info(request, "Profil utilisateur non trouvé ou non configuré.")
            return render(request, "userprofile/userprofile_not_found.html", {"user_obj": user_obj})

        context = {
            "user_obj": user_obj,
            "userprofile": userprofile,
            "experiences": experiences,
            "skills": skills,
            "education_sections": education_sections
        }

        return render(request, self.template_name, context)


class UserProfileAddView(View):
    """
    Handle the creation of a new user profile.

    This view:
    - GET: Display profile creation form
    - POST: Create a new user profile
    """

    template_name = "userprofile/form.html"
    title = "Créer le profil"

    def get(self, request: HttpRequest, user_id: int) -> HttpResponse:
        """Display the user profile creation form."""
        form, user_obj = UserProfileService.get_add_form(user_id)
        context = {
            "user_obj": user_obj,
            "form": form,
            "title": self.title,
        }

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, user_id: int) -> HttpResponse:
        """
        Handle profile creation submission.

        Args:
            request (HttpRequest): The incoming HTTP request.
            user_id (int): ID of the user to create a profile for.

        Returns:
            HttpResponse:
                - 200 on success (HTMX)
                - Render form with errors on failure
        """
        user_obj = get_user_by_id(user_id)

        success, form, userprofile = UserProfileService.create(user_obj, request.POST, request.FILES)

        if not success:
            messages.error(request, "Please correct the errors below.")
            context = {
                "form": form,
                "user_obj": user_obj,
                "title": self.title,
            }
            return render(request, self.template_name, context)

        messages.success(request, "Profile created successfully.")

        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class UserProfileUpdateView(View):
    """
    Handle the update of an existing user profile.

    This view allows:
    - GET: Display the profile update form pre-filled with current data
    - POST: Validate submitted data and update the profile
    """

    template_name = "userprofile/form.html"
    title = "Modifier le profil"

    def get(self, request: HttpRequest, userprofile_id: int) -> HttpResponse:
        """Display the user profile update form."""
        form, userprofile = UserProfileService.get_update_form(userprofile_id)

        context = {
            "form": form,
            "userprofile": userprofile,
            "title": self.title,
        }

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, userprofile_id: int) -> HttpResponse:
        """Handle profile update submission."""
        success, form, userprofile = UserProfileService.update(userprofile_id, request.POST, request.FILES)

        if not success:
            messages.error(request, "Please correct the errors below.")

            context = {
                "form": form,
                "userprofile": userprofile,
                "title": self.title,
            }

            return render(request, self.template_name, context)

        messages.success(request, "Profile updated successfully.")

        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})


class UserProfileDeleteView(View):
    """
    Handle deletion of a user profile.

    This view:
    - GET : show confirmation page
    - POST: Deletes a user profile after confirmation
    """

    template_name = "userprofile/delete_confirm.html"
    title = "Supprimer le profil"

    def get(self, request: HttpRequest, userprofile_id: int) -> HttpResponse:
        """
        Display a confirmation page before deleting a user profile.
        """
        userprofile = get_userprofile_by_id(userprofile_id)

        context = {
            "title": self.title,
            "userprofile": userprofile
        }

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, userprofile_id: int) -> HttpResponse:
        """Handle profile deletion request."""
        userprofile = get_userprofile_by_id(userprofile_id)

        UserProfileService.delete(userprofile)

        messages.success(request, "Profile deleted successfully.")

        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})
