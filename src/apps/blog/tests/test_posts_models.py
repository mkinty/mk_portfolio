from datetime import date

import pytest

from apps.blog.models import Post


@pytest.mark.django_db
class TestPostCategoryModel:
    def test_create_post_category(self, post_category, user):
        assert post_category.id is not None
        assert post_category.name == "Web"
        assert post_category.user == user
        assert post_category.created_at is not None

    def test_str_method(self, post_category):
        assert str(post_category) == "Web"

    def test_user_relationship(self, post_category, user):
        assert post_category in user.post_categories.all()


@pytest.mark.django_db
class TestPostModel:
    def test_create_post(self, post, user, post_category):
        assert post.id is not None
        assert post.title == "Portfolio"
        assert post.user == user
        assert post.category == post_category
        assert post.is_active is True


    def test_str_method(self, post):
        assert str(post) == "Portfolio"

    def test_relationship_with_category(self, post, post_category):
        assert post in post_category.articles.all()

    def test_ordering(self, user, post_category):
        p1 = Post.objects.create(
            user=user,
            title="Old Project",
            category=post_category,
            published_at=date(2023, 1, 1),
        )

        p2 = Post.objects.create(
            user=user,
            title="New Project",
            category=post_category,
            published_at=date(2024, 1, 1),
        )

        articles = Post.objects.all()

        assert articles[0] == p2
        assert articles[1] == p1

    def test_cascade_delete_category(self, post, post_category):
        post_category.delete()
        assert Post.objects.count() == 0

    def test_cascade_delete_user(self, post, user):
        user.delete()
        assert Post.objects.count() == 0
