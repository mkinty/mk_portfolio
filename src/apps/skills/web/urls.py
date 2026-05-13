from django.urls import path

from apps.skills.web.views import SkillAddView, SkillDeleteView, SkillUpdateView

app_name = "skills"

urlpatterns = [
    path("<int:user_id>/add/", SkillAddView.as_view(), name="add"),
    path("<int:skill_id>/update/", SkillUpdateView.as_view(), name="update"),
    path("<int:skill_id>/delete/", SkillDeleteView.as_view(), name="delete"),
]
