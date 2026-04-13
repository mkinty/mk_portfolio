from apps.userprofile.forms import UserProfileForm
from apps.userprofile.models import UserProfile
from apps.userprofile.selectors.userprofile_selectors import get_userprofile_by_id

from django.forms import BaseForm
from typing import Tuple

from apps.users.models import User
from apps.users.selectors.user_selectors import get_user_by_id


def get_userprofile_add_form(user_id: int) -> Tuple[BaseForm, User]:
    """
    Retrieve a user and return a form for creating a user profile.

    This service function:
    - Fetches the user by ID
    - Instantiates an empty form for creating a new profile
    - Associates the form context with the retrieved user

    Args:
        user_id (int): ID of the user for whom the profile will be created.

    Returns:
        Tuple[BaseForm, User]:
            - BaseForm: Empty form instance ready for profile creation.
            - User: Retrieved user instance.

    Raises:
        Http404: If the user does not exist.
    """
    user = get_user_by_id(user_id)
    form = UserProfileForm()
    return form, user


def create_userprofile(user, data, files) -> Tuple[bool, BaseForm, UserProfile | None]:
    """
    Create a new user profile.

    This service function handles:
    - Binding POST and FILES data to the form
    - Validating submitted data
    - Creating a new UserProfile instance if validation succeeds

    Args:
        user (User): The user instance.
        data (QueryDict): POST data from the request.
        files (MultiValueDict): Uploaded files (e.g., avatar image).

    Returns:
        Tuple[bool, BaseForm, UserProfile | None]:
            - bool: Indicates whether creation was successful.
            - BaseForm: Bound form instance (with errors if validation failed).
            - UserProfile | None: Created user profile instance if successful, otherwise None.
    """
    form = UserProfileForm(data, files)

    if not form.is_valid():
        return False, form, None

    userprofile = form.save(commit=False)
    userprofile.user = user
    userprofile.save()

    return True, form, userprofile


def get_userprofile_update_form(userprofile_id: int) -> Tuple[BaseForm, UserProfile]:
    """
    Retrieve a user profile and return a bound update form.

    This service function:
    - Fetches the user profile by ID
    - Instantiates a form pre-filled with existing profile data

    Args:
        userprofile_id (int): ID of the user profile to edit.

    Returns:
        Tuple[BaseForm, UserProfile]:
            - BaseForm: Form instance bound to the existing user profile.
            - UserProfile: Retrieved user profile instance.

    Raises:
        Http404: If the user profile does not exist.
    """
    userprofile = get_userprofile_by_id(userprofile_id)
    form = UserProfileForm(instance=userprofile)
    return form, userprofile


def update_userprofile(userprofile_id: int, data, files) -> Tuple[bool, BaseForm, UserProfile]:
    """
    Update an existing user profile.

    This service function handles:
    - Retrieving the user profile instance
    - Binding POST and FILES data to the form
    - Validating submitted data
    - Saving the profile if validation succeeds

    Args:
        userprofile_id (int): ID of the user profile to update.
        data (QueryDict): POST data from the request.
        files (MultiValueDict): Uploaded files (e.g., avatar image).

    Returns:
        Tuple[bool, BaseForm, UserProfile]:
            - bool: Indicates whether the update was successful.
            - BaseForm: Bound form instance (with errors if validation failed).
            - UserProfile: The retrieved user profile instance.
    """
    userprofile = get_userprofile_by_id(userprofile_id)

    form = UserProfileForm(data, files, instance=userprofile)

    if not form.is_valid():
        return False, form, userprofile

    form.save()

    return True, form, userprofile


def delete_user_profile(profile: UserProfile) -> None:
    """
    Delete a user profile from the database.

    Args:
        profile (UserProfile): The profile instance to delete.

    Returns:
        None

    Notes:
        - Uses Django ORM delete() method.
        - This operation is irreversible.
    """
    profile.delete()
    if profile.pk:
        raise ValueError("User profile deletion failed")
