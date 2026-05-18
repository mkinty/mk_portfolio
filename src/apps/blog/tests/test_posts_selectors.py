from datetime import date

import pytest

from apps.blog.models import Post
from apps.blog.selectors.posts_selectors import (
    PostCategorySelectors,
    PostTagSelectors,
    PostSelectors,
)
from apps.users.models import User


@pytest.mark.django_db
class TestPostCategorySelectors:
    """
    Test post category selectors
    """

    def test_get_post_category_by_id(self, post_category):
        """
        Test getting post category by ID
        """
        result = PostCategorySelectors.get_post_category_by_id(post_category.id)

        assert result == post_category

    def test_get_post_category_by_id_not_found(self):
        """
        Test getting post category by ID when not found
        """
        result = PostCategorySelectors.get_post_category_by_id(999)

        assert result is None

    def test_get_post_categories(self, post_category):
        """
        Test getting all post categories
        """
        categories = PostCategorySelectors.get_post_categories()

        assert categories.count() == 1
        assert post_category in categories


@pytest.mark.django_db
class TestPostTagSelectors:
    """
    Test post tag selectors
    """

    def test_get_tag_by_id(self, post_tag):
        """
        Test getting tag by ID
        """
        result = PostTagSelectors.get_post_tag_by_id(post_tag.id)

        assert result == post_tag

    def test_get_tag_by_id_not_found(self):
        """
        Test getting tag by ID when not found
        """
        result = PostTagSelectors.get_post_tag_by_id(999)

        assert result is None

    def test_get_tags(self, post_tag):
        """
        Test getting all tags
        """
        tags = PostTagSelectors.get_post_tags()

        assert tags.count() == 1
        assert post_tag in tags


@pytest.mark.django_db
class TestPostSelectors:
    """
    Test post selectors
    """

    def test_get_post_by_id(self, post):
        """
        Test getting post by ID
        """
        result = PostSelectors.get_post_by_id(post.id)

        assert result == post

    def test_get_post_by_id_not_found(self):
        """
        Test getting post by ID when not found
        """
        result = PostSelectors.get_post_by_id(999)

        assert result is None

    def test_get_projects(self, post):
        """
        Test getting all posts
        """
        posts = PostSelectors.get_posts()

        assert posts.count() == 1
        assert post in posts

    def test_get_posts_by_category(self, post, post_category):
        """
        Test getting posts by post category
        """
        posts = PostSelectors.get_posts_by_category(post_category)

        assert post in posts
        assert posts.count() == 1

    def test_get_projects_by_user(self, post, user):
        """
        Test getting posts by user
        """
        posts = PostSelectors.get_posts_by_user(user)

        assert post in posts

    def test_get_posts_by_user_filters(self, user, post_category):
        """
        Test getting post by user filters
        """

        other_user = User.objects.create_user(
            email="other@example.com", password="testpass123"
        )

        p1 = Post.objects.create(
            user=user,
            title="User Project",
            category=post_category,
            published_at=date(2024, 1, 1),
        )

        Post.objects.create(
            user=other_user,
            title="Other Project",
            category=post_category,
            published_at=date(2024, 1, 1),
        )

        posts = PostSelectors.get_posts_by_user(user)

        assert p1 in posts
        assert posts.count() == 1

    def test_get_posts_by_tag(self, post_with_tag, post_tag):
        posts = PostSelectors.get_posts_by_tag("Django")

        assert post_with_tag in posts
        assert posts.count() == 1
