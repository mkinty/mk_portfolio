from unittest.mock import patch

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestProjectsView:
    """Test cases for projects views."""

    def test_get_projects_view(self, client, user, project):
        """Test that the projects list view returns a 200 status code."""
        url = reverse("project:list", kwargs={"user_id": user.id})

        response = client.get(url)

        assert response.status_code == 200
        assert "projects" in response.context
        assert "user_obj" in response.context


@pytest.mark.django_db
class TestProjectDetailView:
    """Test cases for project detail view."""

    def test_get_project_detail(self, client, project):
        """Test that the project detail view returns a 200 status code."""
        url = reverse("project:detail", kwargs={"project_id": project.id})

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["project"] == project


@pytest.mark.django_db
class TestProjectCategoryAddView:
    """Test cases for project category add view."""

    def test_get(self, client, user):
        """Test that the project category add view returns a 200 status code."""
        url = reverse("project:add-category", kwargs={"user_id": user.id})

        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    @patch("apps.project.web.views.ProjectCategoryServices.create")
    def test_post_success(self, mock_create, client, user):
        """Test that the project category add view returns a 200 status code on success."""
        mock_create.return_value = (True, None, None)

        url = reverse("project:add-category", kwargs={"user_id": user.id})

        response = client.post(url, data={"name": "Test"})

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"

    @patch("apps.project.web.views.ProjectCategoryServices.create")
    def test_post_invalid(self, mock_create, client, user):
        """Test that the project category add view returns a 200 status code on invalid form."""

        class FakeForm:
            def is_valid(self): return False

        mock_create.return_value = (False, FakeForm(), user)

        url = reverse("project:add-category", kwargs={"user_id": user.id})

        response = client.post(url, data={"name": ""})

        assert response.status_code == 200
        assert "form" in response.context


@pytest.mark.django_db
class TestProjectCategoryUpdateView:
    """Test cases for project category update view."""

    def test_get(self, client, category):
        """Test that the project category update view returns a 200 status code."""
        url = reverse("project:update-category", kwargs={"category_id": category.id})

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["category"] == category

    @patch("apps.project.web.views.ProjectCategoryServices.update")
    def test_post_success(self, mock_update, client, category):
        """Test that the project category update view returns a 200 status code on success."""
        mock_update.return_value = (True, None, category)

        url = reverse("project:update-category", kwargs={"category_id": category.id})

        response = client.post(url, data={"name": "Updated"})

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"


@pytest.mark.django_db
class TestProjectCategoryDeleteView:
    """Test cases for project category delete view"""

    def test_get(self, client, category):
        """Test that the project category delete view returns a 200 status code."""
        url = reverse("project:delete-category", kwargs={"category_id": category.id})

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["category"] == category

    @patch("apps.project.web.views.ProjectCategoryServices.delete")
    def test_post_success(self, mock_delete, client, category):
        """Test that the project category delete view returns a 200 status code on success."""
        mock_delete.return_value = True

        url = reverse("project:delete-category", kwargs={"category_id": category.id})

        response = client.post(url)

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"

    @patch("apps.project.web.views.ProjectCategoryServices.delete")
    def test_post_failure(self, mock_delete, client, category):
        """Test that the project category delete view returns a 400 status code on failure."""
        mock_delete.return_value = False

        url = reverse("project:delete-category", kwargs={"category_id": category.id})

        response = client.post(url)

        assert response.status_code == 400


@pytest.mark.django_db
class TestTagAddView:
    """Test cases for tag add view"""

    def test_get(self, client):
        """Test that the tag add view returns a 200 status code."""
        url = reverse("project:add-tag")

        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    @patch("apps.project.web.views.TagServices.create")
    def test_post_success(self, mock_create, client):
        """Test that the tag add view returns a 200 status code on success."""
        mock_create.return_value = (True, None, None)

        url = reverse("project:add-tag")

        response = client.post(url, data={"name": "Django"})

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"

    @patch("apps.project.web.views.TagServices.create")
    def test_post_invalid(self, mock_create, client):
        """Test that the tag add view returns a 200 status code on invalid form."""

        class FakeForm:
            def is_valid(self): return False

        mock_create.return_value = (False, FakeForm(), None)

        url = reverse("project:add-tag")

        response = client.post(url, data={"name": ""})

        assert response.status_code == 200
        assert "form" in response.context


@pytest.mark.django_db
class TestTagUpdateView:
    """Test cases for tag update view"""

    @patch("apps.project.web.views.TagServices.get_update_form")
    def test_get(self, mock_get_form, client):
        """Test that the tag update view returns a 200 status code."""
        mock_get_form.return_value = ("form", "tag")

        url = reverse("project:update-tag", kwargs={"tag_id": 1})

        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context
        assert "tag" in response.context

    @patch("apps.project.web.views.TagServices.update")
    def test_post_success(self, mock_update, client):
        """Test that the tag update view returns a 200 status code on success."""
        mock_update.return_value = (True, None, "tag")

        url = reverse("project:update-tag", kwargs={"tag_id": 1})

        response = client.post(url, data={"name": "Updated"})

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"

    @patch("apps.project.web.views.TagServices.update")
    def test_post_invalid(self, mock_update, client):
        """Test that the tag update view returns a 200 status code on invalid form."""

        class FakeForm:
            def is_valid(self): return False

        mock_update.return_value = (False, FakeForm(), "tag")

        url = reverse("project:update-tag", kwargs={"tag_id": 1})

        response = client.post(url, data={"name": ""})

        assert response.status_code == 200
        assert "form" in response.context


@pytest.mark.django_db
class TestTagDeleteView:
    """Test cases for tag delete view"""

    @patch("apps.project.web.views.TagSelectors.get_tag_by_id")
    def test_get(self, mock_get_tag, client):
        """Test that the tag delete view returns a 200 status code."""
        mock_get_tag.return_value = "tag"

        url = reverse("project:delete-tag", kwargs={"tag_id": 1})

        response = client.get(url)

        assert response.status_code == 200
        assert "tag" in response.context

    @patch("apps.project.web.views.TagServices.delete")
    def test_post_success(self, mock_delete, client):
        """Test that the tag delete view returns a 200 status code on success."""
        mock_delete.return_value = True

        url = reverse("project:delete-tag", kwargs={"tag_id": 1})

        response = client.post(url)

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"

    @patch("apps.project.web.views.TagServices.delete")
    def test_post_failure(self, mock_delete, client):
        """Test that the tag delete view returns a 400 status code on failure."""
        mock_delete.return_value = False

        url = reverse("project:delete-tag", kwargs={"tag_id": 1})

        response = client.post(url)

        assert response.status_code == 400


@pytest.mark.django_db
class TestProjectAddView:
    """Test cases for project add view"""

    def test_get(self, client, user):
        """Test that the project add view returns a 200 status code."""
        url = reverse("project:add", kwargs={"user_id": user.id})

        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    @patch("apps.project.web.views.ProjectServices.create")
    def test_post_success(self, mock_create, client, user):
        """Test that the project add view returns a 200 status code on success."""
        mock_create.return_value = (True, None, None)

        url = reverse("project:add", kwargs={"user_id": user.id})

        response = client.post(url, data={"title": "Test"})

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"


@pytest.mark.django_db
class TestProjectUpdateView:
    """Test cases for project update view"""

    def test_get(self, client, project):
        """Test that the project update view returns a 200 status code."""
        url = reverse("project:update", kwargs={"project_id": project.id})

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["project"] == project

    @patch("apps.project.web.views.ProjectServices.update")
    def test_post_success(self, mock_update, client, project):
        """Test that the project update view returns a 200 status code on success."""
        mock_update.return_value = (True, None, project)

        url = reverse("project:update", kwargs={"project_id": project.id})

        response = client.post(url, data={"title": "Updated"})

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"


@pytest.mark.django_db
class TestProjectDeleteView:
    """Test cases for project delete view"""

    def test_get(self, client, project):
        """Test that the project delete view returns a 200 status code."""
        url = reverse("project:delete", kwargs={"project_id": project.id})

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["project"] == project

    @patch("apps.project.web.views.ProjectServices.delete")
    def test_post_success(self, mock_delete, client, project):
        """Test that the project delete view returns a 200 status code on success."""
        mock_delete.return_value = True

        url = reverse("project:delete", kwargs={"project_id": project.id})

        response = client.post(url)

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"

    @patch("apps.project.web.views.ProjectServices.delete")
    def test_post_failure(self, mock_delete, client, project):
        """Test that the project delete view returns a 400 status code on failure."""
        mock_delete.return_value = False

        url = reverse("project:delete", kwargs={"project_id": project.id})

        response = client.post(url)

        assert response.status_code == 400
