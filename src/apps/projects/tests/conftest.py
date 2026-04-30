from datetime import date

import pytest

from apps.projects.models import ProjectCategory, Project
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
        password="testpass123"
    )


@pytest.fixture
def category(user):
    return ProjectCategory.objects.create(
        user=user,
        name="Web"
    )


@pytest.fixture
def project(user, category):
    return Project.objects.create(
        user=user,
        title="Portfolio",
        category=category,
        start_date=date(2024, 1, 1),
    )


@pytest.fixture
def project_with_url(user, category):
    return Project.objects.create(
        user=user,
        title="With URL",
        category=category,
        start_date=date(2024, 1, 1),
        source_code_url="https://github.com/test/repo"
    )
