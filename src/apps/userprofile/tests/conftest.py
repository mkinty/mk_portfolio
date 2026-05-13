import pytest

from apps.userprofile.models import UserProfile
from apps.users.models import User


@pytest.fixture
def user(db):
    """
    Create and return a test user instance.

    Returns:
        User: A saved user instance.
    """
    return User.objects.create_user(
        email="testuser@example.com",
        password="testpassword123",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def user_profile(user):
    """
    Return the UserProfile associated with the test user.

    Args:
        user (User): The test user fixture.

    Returns:
        UserProfile: The associated user profile instance.
    """
    # Created by the post_save signal
    return UserProfile.objects.get(user=user)
