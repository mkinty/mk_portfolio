from django.urls import path

from apps.userprofile.web.views import (
    UserProfileView,
    UserProfileUpdateView,
    UserProfileDeleteView,
    UserProfileIndexView,
    AddUserProfileView
)

app_name = "userprofile"

urlpatterns = [
    path("<int:user_id>/", UserProfileIndexView.as_view(), name="index"),
    path("<int:user_id>/detail", UserProfileView.as_view(), name="detail"),
    path("<int:user_id>/add/", AddUserProfileView.as_view(), name="add-profile"),
    path("<int:userprofile_id>/update/", UserProfileUpdateView.as_view(), name="update-profile"),
    path("<int:userprofile_id>/delete/", UserProfileDeleteView.as_view(), name="delete-profile"),
]
