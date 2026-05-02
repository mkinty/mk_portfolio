from datetime import date

import pytest

from apps.project.models import Project


@pytest.mark.django_db
class TestProjectCategoryModel:

    def test_create_project_category(self, category, user):
        assert category.id is not None
        assert category.name == "Web"
        assert category.user == user
        assert category.created_at is not None

    def test_str_method(self, category):
        assert str(category) == "Web"

    def test_user_relationship(self, category, user):
        assert category in user.project_categories.all()


@pytest.mark.django_db
class TestProjectModel:

    def test_create_project(self, project, user, category):
        assert project.id is not None
        assert project.title == "Portfolio"
        assert project.user == user
        assert project.category == category
        assert project.is_active is True

    def test_optional_fields(self, user, category, project):
        assert project.end_date is None
        assert project.source_code_url is None

    def test_str_method(self, project):
        assert str(project) == "Portfolio"

    def test_relationship_with_category(self, project, category):
        assert project in category.projects.all()

    def test_ordering(self, user, category):
        p1 = Project.objects.create(
            user=user,
            title="Old Project",
            category=category,
            start_date=date(2023, 1, 1),
        )

        p2 = Project.objects.create(
            user=user,
            title="New Project",
            category=category,
            start_date=date(2024, 1, 1),
        )

        projects = Project.objects.all()

        assert projects[0] == p2
        assert projects[1] == p1

    def test_cascade_delete_category(self, project, category):
        category.delete()
        assert Project.objects.count() == 0

    def test_cascade_delete_user(self, project, user):
        user.delete()
        assert Project.objects.count() == 0
