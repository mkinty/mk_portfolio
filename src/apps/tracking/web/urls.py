from django.urls import path

from apps.tracking.web.views import (
    ApplicationsTrackingIndexView,
    ApplicationsTrackingView,
    JobApplicationAddView,
    JobApplicationUpdateView,
    ApplicationStatusUpdateView,
    JobApplicationDeleteView,
    ApplicationFollowUpAddView,
    ApplicationFollowUpUpdateView,
    ApplicationFollowUpDeleteView,
)

app_name = "tracking"

urlpatterns = [
    path("<int:user_id>/", ApplicationsTrackingIndexView.as_view(), name="applications-index"),
    path("applications/<int:user_id>/", ApplicationsTrackingView.as_view(), name="applications-tracking"),
    # job applications
    path("applications/<int:user_id>/add/", JobApplicationAddView.as_view(), name="add-application"),
    path("applications/<int:application_id>/update/", JobApplicationUpdateView.as_view(), name="update-application"),
    path("applications/<int:application_id>/update/status", ApplicationStatusUpdateView.as_view(),
         name="update-application-status"),
    path("applications/<int:application_id>/delete/", JobApplicationDeleteView.as_view(), name="delete-application"),
    # follow-up
    path("applications/<int:application_id>/followup/add/", ApplicationFollowUpAddView.as_view(), name="add-followup"),
    path("applications/<int:followup_id>/followup/update/", ApplicationFollowUpUpdateView.as_view(),
         name="update-followup"),
    path("applications/<int:followup_id>/followup/delete/", ApplicationFollowUpDeleteView.as_view(),
         name="delete-followup"),
]
