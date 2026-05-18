from django.urls import path

from apps.blog.web.views import (
    # Posts lists
    PostsIndexView,
    PostsView,
    # Post Detail
    PostDetailIndexView,
    PostDetailView,
    # CRUD for Post Category
    PostCategoryAddView,
    PostCategoryUpdateView,
    PostCategoryDeleteView,
    # CRUD for Post Tag
    PostTagAddView,
    PostTagUpdateView,
    PostTagDeleteView,
    # CRUD for Post
    PostAddView,
    PostUpdateView,
    PostDeleteView,
)

app_name = "blog"

urlpatterns = [
    # posts lists
    path("user/<int:user_id>", PostsIndexView.as_view(), name="index"),
    path("user/<int:user_id>/list", PostsView.as_view(), name="list"),
    # post detail
    path("<int:post_id>", PostDetailIndexView.as_view(), name="detail-index"),
    path("<int:post_id>/detail", PostDetailView.as_view(), name="detail"),
    # CRUD for post category
    path(
        "<int:user_id>/add-category/",
        PostCategoryAddView.as_view(),
        name="add-category",
    ),
    path(
        "<int:category_id>/update-category/",
        PostCategoryUpdateView.as_view(),
        name="update-category",
    ),
    path(
        "<int:category_id>/delete-category/",
        PostCategoryDeleteView.as_view(),
        name="delete-category",
    ),
    # CRUD for post tag
    path("post-tag/", PostTagAddView.as_view(), name="add-tag"),
    path("<int:tag_id>/update-tag/", PostTagUpdateView.as_view(), name="update-tag"),
    path("<int:tag_id>/delete-tag/", PostTagDeleteView.as_view(), name="delete-tag"),
    # CRUD for post
    path("<int:user_id>/add/", PostAddView.as_view(), name="add"),
    path("<int:post_id>/update/", PostUpdateView.as_view(), name="update"),
    path("<int:post_id>/delete/", PostDeleteView.as_view(), name="delete"),
]
