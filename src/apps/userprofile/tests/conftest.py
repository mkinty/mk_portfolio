import pytest
from apps.users.models import User


@pytest.fixture
def user(db):
    """
    Create and return a test user instance.

    This fixture creates a User with basic required fields.
    The Django database is enabled via the `db` fixture.

    Returns:
        User: A saved user instance.
    """
    return User.objects.create(
        email="testuser@example.com",
        password="testpassword123",
        first_name="Test",
        last_name="User"
    )


@pytest.fixture
def user_profile(user):
    """
    Return the UserProfile associated with the test user.

    The UserProfile is automatically created by the post_save
    signal when the User is created, so this fixture simply
    retrieves the related profile.

    Args:
        user (User): The test user fixture.

    Returns:
        UserProfile: The associated user profile instance.
    """
    # Created by the post_save signal
    return user.profile
