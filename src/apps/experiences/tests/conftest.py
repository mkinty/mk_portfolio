import pytest
from datetime import date

from apps.experiences.models import Experience
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
        last_name="User"
    )


@pytest.fixture
def experience(user):
    """
    Create and return a test experience instance.

    Returns:
        Experience: A saved experience instance.
    """
    return Experience.objects.create(
        user=user,
        title="Test Experience",
        company="Test Company",
        start_date=date(2023, 1, 1),
        description="Test Description",
    )
