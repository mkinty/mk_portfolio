from django.urls import path

from apps.project.web.views import (
    ProjectAddView,
    ProjectCategoryAddView,
    ProjectCategoryDeleteView,
    ProjectCategoryUpdateView,
    ProjectDeleteView,
    ProjectDetailIndexView,
    ProjectDetailView,
    ProjectIndexView,
    ProjectsView,
    ProjectUpdateView,
    TagAddView,
    TagDeleteView,
    TagUpdateView,
)

app_name = "project"

urlpatterns = [
    # projects
    path("user/<int:user_id>", ProjectIndexView.as_view(), name="index"),
    path("user/<int:user_id>/list", ProjectsView.as_view(), name="list"),
    # project detail
    path("<int:project_id>", ProjectDetailIndexView.as_view(), name="detail-index"),
    path("<int:project_id>/detail", ProjectDetailView.as_view(), name="detail"),
    # project category
    path(
        "<int:user_id>/add-category/",
        ProjectCategoryAddView.as_view(),
        name="add-category",
    ),
    path(
        "<int:category_id>/update-category/",
        ProjectCategoryUpdateView.as_view(),
        name="update-category",
    ),
    path(
        "<int:category_id>/delete-category/",
        ProjectCategoryDeleteView.as_view(),
        name="delete-category",
    ),
    # project tag
    path("tag/", TagAddView.as_view(), name="add-tag"),
    path("<int:tag_id>/update-tag/", TagUpdateView.as_view(), name="update-tag"),
    path("<int:tag_id>/delete-tag/", TagDeleteView.as_view(), name="delete-tag"),
    # project
    path("<int:user_id>/add/", ProjectAddView.as_view(), name="add"),
    path("<int:project_id>/update/", ProjectUpdateView.as_view(), name="update"),
    path("<int:project_id>/delete/", ProjectDeleteView.as_view(), name="delete"),
]
