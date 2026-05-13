import pytest

from apps.techstack.models import TechStack, TechStackCategory
from apps.users.models import User


@pytest.fixture
def user(db):
    """
    Create a test user.
    """
    return User.objects.create_user(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="testpass123",
    )


@pytest.fixture
def tech_category(user):
    """
    Create a test tech stack category.
    """
    return TechStackCategory.objects.create(user=user, name="Backend", order=1)


@pytest.fixture
def tech_stack(user, tech_category):
    """
    Create a test tech stack.
    """
    return TechStack.objects.create(user=user, category=tech_category, name="Django")
