from typing import Tuple

from django.forms import BaseForm

from apps.experiences.forms import ExperienceForm
from apps.experiences.models import Experience
from apps.experiences.selectors.experiences_selectors import get_experience_by_id
from apps.users.models import User
from apps.users.selectors.user_selectors import get_user_by_id


class ExperienceService:
    """
    Service layer for managing Experience business logic.

    This class centralizes all operations related to the Experience model,
    including creation, update, retrieval and deletion.

    Benefits:
        - Keeps views thin
        - Centralizes business logic
        - Improves testability
    """

    @staticmethod
    def get_add_form(user_id: int) -> Tuple[BaseForm, User]:
        """
        Prepare an empty Experience form for a given user.

        Args:
            user_id (int): ID of the user.

        Returns:
            Tuple[BaseForm, User]:
                - Empty ExperienceForm instance
                - User instance

        Raises:
            Http404: If user is not found.
        """
        user = get_user_by_id(user_id)
        form = ExperienceForm()
        return form, user

    @staticmethod
    def create(user: User, data, files) -> Tuple[bool, BaseForm, Experience | None]:
        """
        Create a new Experience instance.

        Args:
            user (User): User owning the experience.
            data (QueryDict): POST data.
            files (MultiValueDict): Uploaded files.

        Returns:
            Tuple[bool, BaseForm, Experience | None]:
                - Success flag
                - Form instance
                - Created Experience or None
        """
        form = ExperienceForm(data, files)

        if not form.is_valid():
            return False, form, None

        experience = form.save(commit=False)
        experience.user = user
        experience.save()

        return True, form, experience

    @staticmethod
    def get_update_form(experience_id: int) -> Tuple[BaseForm, Experience]:
        """
        Retrieve an Experience and return a pre-filled form.

        Args:
            experience_id (int): ID of the experience.

        Returns:
            Tuple[BaseForm, Experience]
        """
        experience = get_experience_by_id(experience_id)
        form = ExperienceForm(instance=experience)
        return form, experience

    @staticmethod
    def update(experience_id: int, data, files) -> Tuple[bool, BaseForm, Experience]:
        """
        Update an existing Experience.

        Args:
            experience_id (int): Experience ID.
            data (QueryDict): POST data.
            files (MultiValueDict): Uploaded files.

        Returns:
            Tuple[bool, BaseForm, Experience]
        """
        experience = get_experience_by_id(experience_id)

        form = ExperienceForm(data, files, instance=experience)

        if not form.is_valid():
            return False, form, experience

        form.save()

        return True, form, experience

    @staticmethod
    def delete(experience_id: Experience) -> None:
        """
        Delete an Experience instance.

        Args:
            experience_id (Experience): instance to delete.
        """
        experience = get_experience_by_id(experience_id)
        if not experience:
            return False
        experience.delete()
        return True
