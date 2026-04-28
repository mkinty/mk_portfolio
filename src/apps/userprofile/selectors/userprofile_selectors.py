from typing import Optional

from apps.userprofile.models import UserProfile
from apps.users.models import User


def get_userprofile_by_id(userprofile_id: int) -> Optional[UserProfile]:
    """
    Retrieve an userprofile by its unique identifier.

    Args:
        userprofile_id (int): ID of the userprofile.

    Returns:
        UserProfile: The userprofile instance if found, otherwise None.
    """
    try:
        return UserProfile.objects.get(pk=userprofile_id)
    except UserProfile.DoesNotExist:
        return None


def get_userprofile_by_user(user: Optional[User]) -> Optional[UserProfile]:
    """
    Retrieve an userprofile by its user instance.

    Args:
        user (Optional[User]): The user instance.

    Returns:
        UserProfile: The userprofile instance if found, otherwise None.
    """
    return UserProfile.objects.filter(user=user).first()
