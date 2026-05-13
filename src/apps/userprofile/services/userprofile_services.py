from typing import Tuple

from django.forms import BaseForm

from apps.userprofile.forms import UserProfileForm
from apps.userprofile.models import UserProfile
from apps.userprofile.selectors.userprofile_selectors import get_userprofile_by_id
from apps.users.models import User
from apps.users.selectors.user_selectors import get_user_by_id


class UserProfileService:
    """
    Service layer for managing UserProfile business logic.

    This class centralizes all operations related to user profiles,
    including creation, update, retrieval and deletion.

    Benefits:
        - Keeps views thin
        - Centralizes business logic
        - Improves testability
        - Consistent architecture across the project
    """

    @staticmethod
    def get_add_form(user_id: int) -> Tuple[BaseForm, User]:
        """
        Prepare an empty UserProfile form for a given user.

        Args:
            user_id (int): ID of the user.

        Returns:
            Tuple[BaseForm, User]:
                - Empty UserProfileForm instance
                - User instance

        Raises:
            Http404: If user is not found.
        """
        user = get_user_by_id(user_id)
        form = UserProfileForm()
        return form, user

    @staticmethod
    def create(user: User, data, files) -> Tuple[bool, BaseForm, UserProfile | None]:
        """
        Create a new UserProfile instance.

        Args:
            user (User): User owning the profile.
            data (QueryDict): POST data.
            files (MultiValueDict): Uploaded files.

        Returns:
            Tuple[bool, BaseForm, UserProfile | None]:
                - Success flag
                - Form instance
                - Created UserProfile or None
        """
        form = UserProfileForm(data, files)

        if not form.is_valid():
            return False, form, None

        profile = form.save(commit=False)
        profile.user = user
        profile.save()

        return True, form, profile

    @staticmethod
    def get_update_form(userprofile_id: int) -> Tuple[BaseForm, UserProfile]:
        """
        Retrieve a UserProfile and return a pre-filled form.

        Args:
            userprofile_id (int): ID of the profile.

        Returns:
            Tuple[BaseForm, UserProfile]
        """
        profile = get_userprofile_by_id(userprofile_id)
        form = UserProfileForm(instance=profile)
        return form, profile

    @staticmethod
    def update(userprofile_id: int, data, files) -> Tuple[bool, BaseForm, UserProfile]:
        """
        Update an existing UserProfile.

        Args:
            userprofile_id (int): Profile ID.
            data (QueryDict): POST data.
            files (MultiValueDict): Uploaded files.

        Returns:
            Tuple[bool, BaseForm, UserProfile]
        """
        profile = get_userprofile_by_id(userprofile_id)

        form = UserProfileForm(data, files, instance=profile)

        if not form.is_valid():
            return False, form, profile

        form.save()

        return True, form, profile

    @staticmethod
    def delete(profile: UserProfile) -> None:
        """
        Delete a UserProfile instance.

        Args:
            profile (UserProfile): instance to delete.
        """
        profile.delete()
