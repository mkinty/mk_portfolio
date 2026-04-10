from django.urls import path

from apps.projects.web.views import ProjectsView, ProjectDetailView

app_name = "projects"

urlpatterns = [
    path("", ProjectsView.as_view(), name="projects-list"),
    path("detail/", ProjectDetailView.as_view(), name="project-detail"),
]
