from django.urls import path

from apps.tracking.web.views import ApplicationsTrackingView

app_name = "tracking"

urlpatterns = [
    path("applications/", ApplicationsTrackingView.as_view(), name="applications-tracking"),
]
