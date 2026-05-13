import pytest

from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.users.models import User
from apps.project.models import (
    Project,
    ProjectCategory,
    Tag,
)


@pytest.fixture
def user_fixture(db):
    user = User.objects.create_user(
        email="test@test.com",
        password="password123",
        first_name="Moustapha",
        last_name="KINTY"
    )

    avatar = SimpleUploadedFile(
        "avatar.jpg",
        b"fake-image-content",
        content_type="image/jpeg"
    )

    # récupérer le profil créé automatiquement
    profile = user.profile

    profile.title = "Data Analyst"
    profile.position = "Consultant BI"

    profile.avatar.save(
        "avatar.jpg",
        avatar,
        save=True
    )

    profile.save()

    return user


@pytest.fixture
def category_fixture(db, user_fixture):
    return ProjectCategory.objects.create(
        user=user_fixture,
        name="Data"
    )


@pytest.fixture
def data_tag_fixture(db):
    return Tag.objects.create(
        name="Data"
    )


@pytest.fixture
def dev_tag_fixture(db):
    return Tag.objects.create(
        name="Development"
    )


@pytest.fixture
def data_project_fixture(
        db,
        user_fixture,
        category_fixture,
        data_tag_fixture
):
    project = Project.objects.create(
        user=user_fixture,
        category=category_fixture,
        title="Projet Data",
        start_date=date(2024, 1, 1),
    )

    project.tags.add(data_tag_fixture)

    return project


@pytest.fixture
def dev_project_fixture(
        db,
        user_fixture,
        category_fixture,
        dev_tag_fixture
):
    project = Project.objects.create(
        user=user_fixture,
        category=category_fixture,
        title="Projet Dev",
        start_date=date(2024, 1, 1),
    )

    project.tags.add(dev_tag_fixture)

    return project
