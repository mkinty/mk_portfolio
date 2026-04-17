from django.urls import path

from apps.techstack.web.views import (
    TechStackCategoryAddView,
    TechStackCategoryUpdateView,
    TechStackCategoryDeleteView,
    TechStackAddView,
    TechStackUpdateView,
    TechStackDeleteView,
)

app_name = "techstack"

urlpatterns = [
    # tech stack category
    path("<int:user_id>/add-category/", TechStackCategoryAddView.as_view(), name="add-category"),
    path("<int:tech_category_id>/update-category/", TechStackCategoryUpdateView.as_view(), name="update-category"),
    path("<int:tech_category_id>/delete-category/", TechStackCategoryDeleteView.as_view(), name="delete-category"),
    # tech stack
    path("<int:user_id>/add/", TechStackAddView.as_view(), name="add"),
    path("<int:tech_stack_id>/update/", TechStackUpdateView.as_view(), name="update"),
    path("<int:tech_stack_id>/delete/", TechStackDeleteView.as_view(), name="delete"),
]
