from django.urls import path

from apps.education.web.views import EducationSectionAddView, EducationSectionUpdateView, EducationSectionDeleteView, \
    EducationUpdateView, EducationAddView, EducationDeleteView

app_name = "education"

urlpatterns = [
    # Education Section
    path("<int:user_id>/section/add/", EducationSectionAddView.as_view(), name="add-section"),
    path("<int:education_section_id>/section/update/", EducationSectionUpdateView.as_view(), name="update-section"),
    path("<int:education_section_id>/section/delete/", EducationSectionDeleteView.as_view(), name="delete-section"),
    # Education
    path("<int:education_section_id>/add/", EducationAddView.as_view(), name="add"),
    path("<int:education_id>/update/", EducationUpdateView.as_view(), name="update"),
    path("<int:education_id>/delete/", EducationDeleteView.as_view(), name="delete"),
]
