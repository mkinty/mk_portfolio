from django.urls import path

from apps.experiences.web.views import (
    ExperienceAddView,
    ExperienceDeleteView,
    ExperienceUpdateView,
)

app_name = "experiences"

urlpatterns = [
    path("<int:user_id>/add/", ExperienceAddView.as_view(), name="add"),
    path("<int:experience_id>/update/", ExperienceUpdateView.as_view(), name="update"),
    path("<int:experience_id>/delete/", ExperienceDeleteView.as_view(), name="delete"),
]
