import pytest

from apps.projects.selectors.projects_selectors import (
    ProjectCategorySelectors,
    ProjectSelectors
)


@pytest.mark.django_db
class TestProjectCategorySelectors:

    def test_get_project_category_by_id(self, category):
        result = ProjectCategorySelectors.get_project_category_by_id(category.id)

        assert result == category

    def test_get_project_category_by_id_not_found(self):
        result = ProjectCategorySelectors.get_project_category_by_id(999)

        assert result is None

    def test_get_project_categories(self, category):
        categories = ProjectCategorySelectors.get_project_categories()

        assert categories.count() == 1
        assert category in categories


@pytest.mark.django_db
class TestProjectSelectors:

    def test_get_project_by_id(self, project):
        result = ProjectSelectors.get_project_by_id(project.id)

        assert result == project

    def test_get_project_by_id_not_found(self):
        result = ProjectSelectors.get_project_by_id(999)

        assert result is None

    def test_get_projects(self, project):
        projects = ProjectSelectors.get_projects()

        assert projects.count() == 1
        assert project in projects

    def test_get_projects_by_category(self, project, category):
        projects = ProjectSelectors.get_projects_by_category(category)

        assert project in projects
        assert projects.count() == 1

    def test_get_projects_by_user(self, project, user):
        projects = ProjectSelectors.get_projects_by_user(user)

        assert project in projects

    def test_get_projects_by_user_filters(self, user, category):
        from datetime import date
        from apps.projects.models import Project
        from apps.users.models import User

        other_user = User.objects.create_user(
            email="other@example.com",
            password="testpass123"
        )

        p1 = Project.objects.create(
            user=user,
            title="User Project",
            category=category,
            start_date=date(2024, 1, 1),
        )

        Project.objects.create(
            user=other_user,
            title="Other Project",
            category=category,
            start_date=date(2024, 1, 1),
        )

        projects = ProjectSelectors.get_projects_by_user(user)

        assert p1 in projects
        assert projects.count() == 1