from unittest.mock import patch

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestPostsView:
    """Test cases for posts views."""

    def test_get_posts_view(self, client, user, post):
        """Test that the posts list view returns a 200 status code."""
        url = reverse("blog:list", kwargs={"user_id": user.id})

        response = client.get(url)

        assert response.status_code == 200
        assert "articles" in response.context
        assert "user_obj" in response.context


@pytest.mark.django_db
class TestPostDetailView:
    """Test cases for post detail view."""

    def test_get_post_detail(self, client, post):
        """Test that the post detail view returns a 200 status code."""
        url = reverse("blog:detail", kwargs={"post_id": post.id})

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["article"] == post


@pytest.mark.django_db
class TestPosttCategoryAddView:
    """Test cases for post category add view."""

    def test_get(self, client, user):
        """Test that the post category add view returns a 200 status code."""
        url = reverse("blog:add-category", kwargs={"user_id": user.id})

        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    @patch("apps.blog.web.views.PostCategoryServices.create")
    def test_post_success(self, mock_create, client, user):
        """
        Test that the post category add view
        returns a 200 status code on success.
        """
        mock_create.return_value = (True, None, None)

        url = reverse("blog:add-category", kwargs={"user_id": user.id})

        response = client.post(url, data={"name": "Test"})

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"

    @patch("apps.blog.web.views.PostCategoryServices.create")
    def test_post_invalid(self, mock_create, client, user):
        """
        Test that the post category add view
        returns a 200 status code on invalid form.
        """

        class FakeForm:
            def is_valid(self):
                return False

        mock_create.return_value = (False, FakeForm(), user)

        url = reverse("blog:add-category", kwargs={"user_id": user.id})

        response = client.post(url, data={"name": ""})

        assert response.status_code == 200
        assert "form" in response.context


@pytest.mark.django_db
class TestPostCategoryUpdateView:
    """Test cases for post category update view."""

    def test_get(self, client, post_category):
        """
        Test that the post category update view
        returns a 200 status code.
        """
        url = reverse("blog:update-category", kwargs={"category_id": post_category.id})

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["category"] == post_category

    @patch("apps.blog.web.views.PostCategoryServices.update")
    def test_post_success(self, mock_update, client, post_category):
        """
        Test that the post category update view
        returns a 200 status code on success.
        """
        mock_update.return_value = (True, None, post_category)

        url = reverse("blog:update-category", kwargs={"category_id": post_category.id})

        response = client.post(url, data={"name": "Updated"})

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"


@pytest.mark.django_db
class TestPostCategoryDeleteView:
    """Test cases for post category delete view"""

    def test_get(self, client, post_category):
        """
        Test that the post category delete view
        returns a 200 status code.
        """
        url = reverse("blog:delete-category", kwargs={"category_id": post_category.id})

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["category"] == post_category

    @patch("apps.blog.web.views.PostCategoryServices.delete")
    def test_post_success(self, mock_delete, client, post_category):
        """
        Test that the post category delete view
        returns a 200 status code on success.
        """
        mock_delete.return_value = True

        url = reverse("blog:delete-category", kwargs={"category_id": post_category.id})

        response = client.post(url)

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"

    @patch("apps.blog.web.views.PostCategoryServices.delete")
    def test_post_failure(self, mock_delete, client, post_category):
        """
        Test that the post category delete view
        returns a 400 status code on failure.
        """
        mock_delete.return_value = False

        url = reverse("blog:delete-category", kwargs={"category_id": post_category.id})

        response = client.post(url)

        assert response.status_code == 400


@pytest.mark.django_db
class TestPostTagAddView:
    """Test cases for post tag add view"""

    def test_get(self, client):
        """Test that the post tag add view returns a 200 status code."""
        url = reverse("blog:add-tag")

        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    @patch("apps.blog.web.views.PostTagServices.create")
    def test_post_success(self, mock_create, client):
        """Test that the post tag add view returns a 200 status code on success."""
        mock_create.return_value = (True, None, None)

        url = reverse("blog:add-tag")

        response = client.post(url, data={"name": "Django"})

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"

    @patch("apps.blog.web.views.PostTagServices.create")
    def test_post_invalid(self, mock_create, client):
        """
        Test that the post tag add view returns a 200
        status code on invalid form.
        """

        class FakeForm:
            def is_valid(self):
                return False

        mock_create.return_value = (False, FakeForm(), None)

        url = reverse("blog:add-tag")

        response = client.post(url, data={"name": ""})

        assert response.status_code == 200
        assert "form" in response.context


@pytest.mark.django_db
class TestPostTagUpdateView:
    """Test cases for post tag update view"""

    @patch("apps.blog.web.views.PostTagServices.get_update_form")
    def test_get(self, mock_get_form, client):
        """Test that the post tag update view returns a 200 status code."""
        mock_get_form.return_value = ("form", "tag")

        url = reverse("blog:update-tag", kwargs={"tag_id": 1})

        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context
        assert "tag" in response.context

    @patch("apps.blog.web.views.PostTagServices.update")
    def test_post_success(self, mock_update, client):
        """Test that the post tag update view returns a 200 status code on success."""
        mock_update.return_value = (True, None, "tag")

        url = reverse("blog:update-tag", kwargs={"tag_id": 1})

        response = client.post(url, data={"name": "Updated"})

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"

    @patch("apps.blog.web.views.PostTagServices.update")
    def test_post_invalid(self, mock_update, client):
        """
        Test that the post tag update view returns a 200
        status code on invalid form.
        """

        class FakeForm:
            def is_valid(self):
                return False

        mock_update.return_value = (False, FakeForm(), "tag")

        url = reverse("blog:update-tag", kwargs={"tag_id": 1})

        response = client.post(url, data={"name": ""})

        assert response.status_code == 200
        assert "form" in response.context


@pytest.mark.django_db
class TestPostTagDeleteView:
    """Test cases for post tag delete view"""

    @patch("apps.blog.web.views.PostTagSelectors.get_post_tag_by_id")
    def test_get(self, mock_get_tag, client):
        """Test that the post tag delete view returns a 200 status code."""
        mock_get_tag.return_value = "tag"

        url = reverse("blog:delete-tag", kwargs={"tag_id": 1})

        response = client.get(url)

        assert response.status_code == 200
        assert "tag" in response.context

    @patch("apps.blog.web.views.PostTagServices.delete")
    def test_post_success(self, mock_delete, client):
        """
        Test that the post tag delete view returns a 200
        status code on success.
        """
        mock_delete.return_value = True

        url = reverse("blog:delete-tag", kwargs={"tag_id": 1})

        response = client.post(url)

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"

    @patch("apps.blog.web.views.PostTagServices.delete")
    def test_post_failure(self, mock_delete, client):
        """
        Test that the post tag delete view
        returns a 400 status code on failure.
        """
        mock_delete.return_value = False

        url = reverse("blog:delete-tag", kwargs={"tag_id": 1})

        response = client.post(url)

        assert response.status_code == 400


@pytest.mark.django_db
class TestPostAddView:
    """Test cases for post add view"""

    def test_get(self, client, user):
        """Test that the post add view returns a 200 status code."""
        url = reverse("blog:add", kwargs={"user_id": user.id})

        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    @patch("apps.blog.web.views.PostServices.create")
    def test_post_success(self, mock_create, client, user):
        """
        Test that the post add view
        returns a 200 status code on success.
        """
        mock_create.return_value = (True, None, None)

        url = reverse("blog:add", kwargs={"user_id": user.id})

        response = client.post(url, data={"title": "Test"})

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"


@pytest.mark.django_db
class TestPostUpdateView:
    """Test cases for post update view"""

    def test_get(self, client, post):
        """
        Test that the post update view
        returns a 200 status code.
        """
        url = reverse("blog:update", kwargs={"post_id": post.id})

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["article"] == post

    @patch("apps.blog.web.views.PostServices.update")
    def test_post_success(self, mock_update, client, post):
        """
        Test that the post update view
        returns a 200 status code on success.
        """
        mock_update.return_value = (True, None, post)

        url = reverse("blog:update", kwargs={"post_id": post.id})

        response = client.post(url, data={"title": "Updated"})

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"


@pytest.mark.django_db
class TestPostDeleteView:
    """Test cases for post delete view"""

    def test_get(self, client, post):
        """
        Test that the post delete view
        returns a 200 status code.
        """
        url = reverse("blog:delete", kwargs={"post_id": post.id})

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["article"] == post

    @patch("apps.blog.web.views.PostServices.delete")
    def test_post_success(self, mock_delete, client, post):
        """
        Test that the post delete view
        returns a 200 status code on success.
        """
        mock_delete.return_value = True

        url = reverse("blog:delete", kwargs={"post_id": post.id})
        expected_url = reverse("blog:index", kwargs={"user_id": post.user.id})

        response = client.post(url)

        assert response.status_code == 200
        assert response.headers["HX-Redirect"] == expected_url

    @patch("apps.blog.web.views.PostServices.delete")
    def test_post_failure(self, mock_delete, client, post):
        """
        Test that the post delete view
        returns a 400 status code on failure.
        """
        mock_delete.return_value = False

        url = reverse("blog:delete", kwargs={"post_id": post.id})

        response = client.post(url)

        assert response.status_code == 400
