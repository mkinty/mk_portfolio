from django.urls import path

from apps.techstack.web.views import (
    TechStackAddView,
    TechStackUpdateView,
    TechStackDeleteView,
)

app_name = "techstack"

urlpatterns = [
    path("<int:user_id>/add/", TechStackAddView.as_view(), name="add"),
    path("<int:techstack_id>/update/", TechStackUpdateView.as_view(), name="update"),
    path("<int:techstack_id>/delete/", TechStackDeleteView.as_view(), name="delete"),
]
