from datetime import date

import pytest

from apps.blog.models import PostCategory, PostTag, Post
from apps.users.models import User


@pytest.fixture
def user(db):
    """
    Create a test user.
    """
    return User.objects.create_user(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="testpass123",
    )


@pytest.fixture
def post_category(user):
    return PostCategory.objects.create(user=user, name="Web")


@pytest.fixture
def post_tag(db):
    return PostTag.objects.create(name="Django")


@pytest.fixture
def post(user, post_category):
    return Post.objects.create(
        user=user,
        title="Portfolio",
        category=post_category,
        published_at=date(2024, 1, 1),
    )


@pytest.fixture
def post_with_tag(user, post_category, post_tag):
    article = Post.objects.create(
        user=user,
        title="Tagged Project",
        category=post_category,
        published_at=date(2024, 1, 1),
    )
    article.tags.add(post_tag)
    return article


@pytest.fixture
def other_post_tag(db):
    return PostTag.objects.create(name="Python")


@pytest.fixture
def multi_tag_post(user, post_category, post_tag, other_post_tag):
    article = Post.objects.create(
        user=user,
        title="Multi Tag Project",
        category=post_category,
        published_at=date(2024, 1, 1),
    )
    article.tags.add(post_tag, other_post_tag)
    return article
