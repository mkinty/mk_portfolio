from django.urls import path

from apps.tracking.web.views import (
    ApplicationsTrackingIndexView,
    ApplicationsTrackingView
)

app_name = "tracking"

urlpatterns = [
    path("<int:user_id>/", ApplicationsTrackingIndexView.as_view(), name="applications-index"),
    path("<int:user_id>/applications/", ApplicationsTrackingView.as_view(), name="applications-tracking"),
]
