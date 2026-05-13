from datetime import date

import pytest

from apps.education.models import Education, EducationSection
from apps.users.models import User


@pytest.fixture
def user(db):
    """
    Create and return a test user instance.
    """
    return User.objects.create_user(
        email="testuser@example.com",
        password="testpassword123",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def education_section(user):
    """
    Create and return a test education section instance.
    """
    return EducationSection.objects.create(user=user, name="Education")


@pytest.fixture
def education_entry(education_section):
    """
    Create and return a test education entry instance.
    """
    return Education.objects.create(
        education_section=education_section,
        school="Test University",
        degree="Bachelor of Science",
        field_of_study="Computer Science",
        start_date=date(2020, 9, 1),
        end_date=date(2024, 6, 30),
        description="Completed my undergraduate degree with honors.",
    )
