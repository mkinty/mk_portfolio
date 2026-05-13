from datetime import date

import pytest

from apps.project.models import Project, ProjectCategory, Tag
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
def category(user):
    return ProjectCategory.objects.create(user=user, name="Web")


@pytest.fixture
def tag(db):
    return Tag.objects.create(name="Django")


@pytest.fixture
def project(user, category):
    return Project.objects.create(
        user=user,
        title="Portfolio",
        category=category,
        start_date=date(2024, 1, 1),
    )


@pytest.fixture
def project_with_tag(user, category, tag):
    project = Project.objects.create(
        user=user,
        title="Tagged Project",
        category=category,
        start_date=date(2024, 1, 1),
    )
    project.tags.add(tag)
    return project


@pytest.fixture
def other_tag(db):
    return Tag.objects.create(name="Python")


@pytest.fixture
def multi_tag_project(user, category, tag, other_tag):
    project = Project.objects.create(
        user=user,
        title="Multi Tag Project",
        category=category,
        start_date=date(2024, 1, 1),
    )
    project.tags.add(tag, other_tag)
    return project
