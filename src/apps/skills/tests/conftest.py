import pytest

from apps.skills.models import Skills
from apps.users.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="testpass123",
    )


@pytest.fixture
def skill(user):
    return Skills.objects.create(
        user=user, name="Test Skill", description="Test Description"
    )
