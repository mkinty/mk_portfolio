import pytest
from datetime import date
from apps.project.models import Project
from apps.users.models import User

from apps.project.selectors.projects_selectors import (
    ProjectCategorySelectors,
    ProjectSelectors, TagSelectors
)


@pytest.mark.django_db
class TestProjectCategorySelectors:
    """
    Test project category selectors
    """

    def test_get_project_category_by_id(self, category):
        """
        Test getting project category by ID
        """
        result = ProjectCategorySelectors.get_project_category_by_id(category.id)

        assert result == category

    def test_get_project_category_by_id_not_found(self):
        """
        Test getting project category by ID when not found
        """
        result = ProjectCategorySelectors.get_project_category_by_id(999)

        assert result is None

    def test_get_project_categories(self, category):
        """
        Test getting all project categories
        """
        categories = ProjectCategorySelectors.get_project_categories()

        assert categories.count() == 1
        assert category in categories


@pytest.mark.django_db
class TestTagSelectors:
    """
    Test tag selectors
    """

    def test_get_tag_by_id(self, tag):
        """
        Test getting tag by ID
        """
        result = TagSelectors.get_tag_by_id(tag.id)

        assert result == tag

    def test_get_tag_by_id_not_found(self):
        """
        Test getting tag by ID when not found
        """
        result = TagSelectors.get_tag_by_id(999)

        assert result is None

    def test_get_tags(self, tag):
        """
        Test getting all tags
        """
        tags = TagSelectors.get_tags()

        assert tags.count() == 1
        assert tag in tags


@pytest.mark.django_db
class TestProjectSelectors:
    """
    Test project selectors
    """

    def test_get_project_by_id(self, project):
        """
        Test getting project by ID
        """
        result = ProjectSelectors.get_project_by_id(project.id)

        assert result == project

    def test_get_project_by_id_not_found(self):
        """
        Test getting project by ID when not found
        """
        result = ProjectSelectors.get_project_by_id(999)

        assert result is None

    def test_get_projects(self, project):
        """
        Test getting all projects
        """
        projects = ProjectSelectors.get_projects()

        assert projects.count() == 1
        assert project in projects

    def test_get_projects_by_category(self, project, category):
        """
        Test getting projects by category
        """
        projects = ProjectSelectors.get_projects_by_category(category)

        assert project in projects
        assert projects.count() == 1

    def test_get_projects_by_user(self, project, user):
        """
        Test getting projects by user
        """
        projects = ProjectSelectors.get_projects_by_user(user)

        assert project in projects

    def test_get_projects_by_user_filters(self, user, category):
        """
        Test getting projects by user filters
        """

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

    def test_get_projects_by_tag(self, project_with_tag, tag):
        projects = ProjectSelectors.get_projects_by_tag("Django")

        assert project_with_tag in projects
        assert projects.count() == 1
