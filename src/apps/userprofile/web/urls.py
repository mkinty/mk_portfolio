from django.urls import path

from apps.userprofile.web.views import UserProfileView

app_name = "userprofile"

urlpatterns = [
    path("<int:userprofile_id>/", UserProfileView.as_view(), name="profile"),
]
