from django.contrib import messages
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views import View

from apps.users.selectors.user_selectors import get_user_by_id
from apps.userprofile.selectors.userprofile_selectors import (
    get_userprofile_by_id,
    get_userprofile_by_user
)
from apps.userprofile.services.userprofile_services import (
    delete_user_profile,
    get_userprofile_update_form,
    update_userprofile,
    create_userprofile, get_userprofile_add_form
)


class UserProfileIndexView(View):
    """
    Display the user profile index page.

    This view handles:
    - Retrieving a user by ID
    - Rendering the user profile index template

    The template is expected to display information related to
    the given user, such as profile details, actions, or related data.

    Attributes:
        template_name (str): Path to the user profile index template.
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

    This view retrieves a user profile by its ID and renders it
    using the specified template.

    Attributes:
        template_name (str): Path to the template used to render the profile page.
    """

    template_name = "userprofile/userprofile.html"

    def get(self, request: HttpRequest, user_id: int) -> HttpResponse:
        """
        Handle GET request to display a user profile.

        Args:
            request (HttpRequest): The incoming HTTP request.
            user_id (int): The ID of the user to retrieve.

        Returns:
            HttpResponse: Rendered HTML page displaying the user profile.
        """
        user_obj = get_user_by_id(user_id)
        userprofile = get_userprofile_by_user(user_obj)
        if not userprofile:
            messages.info(request, "Profil utilisateur non trouvé ou non configuré.")
            return render(request, "userprofile/userprofile_not_found.html", {"user_obj": user_obj})

        context = {
            "user_obj": user_obj,
            "userprofile": userprofile
        }

        return render(request, self.template_name, context)


class AddUserProfileView(View):
    """
    Handle the creation of a new user profile.

    This view:
    - GET: Display profile creation form
    - POST: Create a new user profile
    """

    template_name = "userprofile/form.html"
    title = "Créer le profil"

    def get(self, request: HttpRequest, user_id: int) -> HttpResponse:
        """
        Display the user profile creation form.

        Args:
            request (HttpRequest): The incoming HTTP request.
            user_id (int): ID of the user to create a profile for.

        Returns:
            HttpResponse: Rendered form page.
        """
        form, user_obj = get_userprofile_add_form(user_id)
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

        success, form, userprofile = create_userprofile(user_obj, request.POST, request.FILES)

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

    The form is powered by `UserProfileForm`, which includes:
    - Standard Django validation
    - File upload support for avatar
    - Rich text editing for bio using CKEditor5

    Attributes:
        template_name (str): Path to the form template.
        title (str): Page title displayed in the template.
    """

    template_name = "userprofile/form.html"
    title = "Modifier le profil"

    def get(self, request: HttpRequest, userprofile_id: int) -> HttpResponse:
        """
        Display the user profile update form.

        Args:
            request (HttpRequest): The incoming HTTP request.
            userprofile_id (int): ID of the user profile to edit.

        Returns:
            HttpResponse: Rendered form with pre-filled profile data.

        Notes:
            - Uses `UserProfileForm` with instance binding.
            - CKEditor5 widget is automatically applied to the bio field.
        """
        form, userprofile = get_userprofile_update_form(userprofile_id)

        context = {
            "form": form,
            "userprofile": userprofile,
            "title": self.title,
        }

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, userprofile_id: int) -> HttpResponse:
        """
        Handle profile update submission.

        This method:
        1. Retrieves the user profile
        2. Binds POST and FILES data to the form
        3. Validates form data
        4. Saves changes if valid
        5. Returns HTMX response on success

        Args:
            request (HttpRequest): The incoming HTTP request containing form data.
            userprofile_id (int): ID of the user profile to update.

        Returns:
            HttpResponse:
                - 200 response with HTMX trigger on success
                - Rendered form with validation errors on failure

        Notes:
            - `request.FILES` is required for avatar upload support
            - Uses Django messages framework for feedback
            - HTMX event "formSubmittedEvent" is triggered on success
        """
        success, form, userprofile = update_userprofile(userprofile_id, request.POST, request.FILES)

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
    - POST: Deletes a user profile after confirmation

    Attributes:
        template_name (str): Path to the confirmation template.
    """

    template_name = "userprofile/delete_confirm.html"
    title = "Supprimer le profil"

    def get(self, request: HttpRequest, userprofile_id: int) -> HttpResponse:
        """
        Display a confirmation page before deleting a user profile.

        Args:
            request (HttpRequest): The incoming HTTP request.
            userprofile_id (int): ID of the user profile to delete.

        Returns:
            HttpResponse: Rendered confirmation page.
        """
        userprofile = get_userprofile_by_id(userprofile_id)

        context = {
            "title": self.title,
            "userprofile": userprofile
        }

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, userprofile_id: int) -> HttpResponse:
        """
        Handle profile deletion request.

        Args:
            request (HttpRequest): The incoming HTTP request.
            userprofile_id (int): ID of the profile to delete.

        Returns:
            HttpResponse:
                - 200 No Content on success (for HTMX or AJAX)
                - Render confirmation page on error
        """
        userprofile = get_userprofile_by_id(userprofile_id)

        try:
            delete_user_profile(userprofile)

        except ValueError as e:
            messages.error(request, str(e))
            return render(request, self.template_name, {"userprofile": userprofile})

        messages.success(request, "Profile deleted successfully.")

        return HttpResponse(status=200, headers={"HX-Trigger": "formSubmittedEvent"})
