from datetime import date

import pytest

from apps.blog.models import PostCategory, PostTag, Post
from apps.blog.services.posts_services import (
    PostCategoryServices,
    PostTagServices,
    PostServices,
)


@pytest.mark.django_db
class TestPostCategoryServices:
    """Test post category services"""

    def test_get_add_form(self, user):
        """Test getting the add form"""
        form, returned_user = PostCategoryServices.get_add_form(user.id)

        assert form is not None
        assert returned_user == user

    def test_create_success(self, user):
        """Test creating a post category successfully"""
        data = {"name": "Backend"}

        success, form, category = PostCategoryServices.create(user, data, {})

        assert success is True
        assert form.is_valid()
        assert category is not None
        assert category.name == "Backend"
        assert category.user == user
        assert PostCategory.objects.count() == 1

    def test_create_invalid(self, user):
        """Test creating a post category with invalid data"""
        data = {"name": ""}  # invalide

        success, form, category = PostCategoryServices.create(user, data, {})

        assert success is False
        assert not form.is_valid()
        assert category is None

    def test_get_update_form(self, post_category):
        """Test getting the update form"""
        form, returned_category = PostCategoryServices.get_update_form(post_category.id)

        assert form.instance == post_category
        assert returned_category == post_category

    def test_update_success(self, post_category):
        """Test updating a post category successfully"""
        data = {"name": "Updated"}

        success, form, updated_category = PostCategoryServices.update(
            post_category.id, data, {}
        )

        assert success is True
        assert updated_category.name == "Updated"

    def test_update_invalid(self, post_category):
        """Test updating a post category with invalid data"""
        data = {"name": ""}

        success, form, updated_category = PostCategoryServices.update(
            post_category.id, data, {}
        )

        assert success is False
        assert not form.is_valid()

    def test_delete(self, post_category):
        """Test deleting a post category"""
        result = PostCategoryServices.delete(post_category.id)

        assert result is True
        assert PostCategory.objects.count() == 0


@pytest.mark.django_db
class TestPostTagServices:
    """
    Test post tag services
    """

    def test_get_add_form(self):
        """
        Test getting the add form
        """
        form = PostTagServices.get_add_form()

        assert form is not None

    def test_create_success(self):
        """
        Test creating a post tag successfully
        """
        data = {"name": "Django"}

        success, form, tag = PostTagServices.create(data, {})

        assert success is True
        assert form.is_valid()
        assert tag is not None
        assert tag.name == "Django"
        assert PostTag.objects.count() == 1

    def test_create_invalid(self):
        """
        Test creating a post tag with invalid data
        """
        data = {"name": ""}  # invalide

        success, form, tag = PostTagServices.create(data, {})

        assert success is False
        assert not form.is_valid()
        assert tag is None

    def test_get_update_form(self, post_tag):
        """
        Test getting the update form
        """
        form, returned_tag = PostTagServices.get_update_form(post_tag.id)

        assert form.instance == post_tag
        assert returned_tag == post_tag

    def test_update_success(self, post_tag):
        """
        Test updating a post tag successfully
        """
        data = {"name": "Updated Tag"}

        success, form, updated_tag = PostTagServices.update(post_tag.id, data, {})

        assert success is True
        assert updated_tag.name == "Updated Tag"

    def test_update_invalid(self, post_tag):
        """
        Test updating a post tag with invalid data
        """
        data = {"name": ""}

        success, form, updated_tag = PostTagServices.update(post_tag.id, data, {})

        assert success is False
        assert not form.is_valid()
        assert updated_tag == post_tag

    def test_delete(self, post_tag):
        """Test deleting a post tag"""
        result = PostTagServices.delete(post_tag.id)

        assert result is True
        assert PostTag.objects.count() == 0

    def test_delete_non_existing_safe(self):
        """Test deleting a non existing post tag"""
        result = PostTagServices.delete(999)

        assert result is False


@pytest.mark.django_db
class TestPostServices:
    """Test post services"""

    def test_create_success(self, user, post_category):
        """Test creating a post successfully"""
        data = {
            "title": "New Project",
            "category": post_category.id,
            "start_date": date(2024, 1, 1),
        }

        success, form, article = PostServices.create(user, data, {})

        assert success is True
        assert form.is_valid()
        assert article is not None
        assert article.title == "New Project"
        assert article.user == user
        assert Post.objects.count() == 1

    def test_create_invalid(self, user, post_category):
        """Test creating a post with invalid data"""
        data = {
            "title": "",  # invalide
            "category": post_category.id,
        }

        success, form, article = PostServices.create(user, data, {})

        assert success is False
        assert not form.is_valid()
        assert article is None

    def test_get_update_form(self, post):
        """Test getting the update form"""
        form, returned_project = PostServices.get_update_form(post.id)

        assert form.instance == post
        assert returned_project == post

    def test_update_success(self, post, post_category):
        """Test updating a post successfully"""
        data = {
            "title": "Updated Project",
            "category": post_category.id,
            "published_at": post.published_at,
        }

        success, form, updated_project = PostServices.update(post.id, data, {})

        assert success is True
        assert updated_project.title == "Updated Project"

    def test_update_invalid(self, post, post_category):
        """Test updating a post with invalid data"""
        data = {
            "title": "",
            "category": post_category.id,
        }

        success, form, updated_project = PostServices.update(post.id, data, {})

        assert success is False
        assert not form.is_valid()

    def test_delete(self, post):
        """Test deleting a post"""
        result = PostServices.delete(post.id)

        assert result is True
        assert Post.objects.count() == 0
