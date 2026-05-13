from django.urls import path

from apps.userprofile.web.views import (
    UserProfileAddView,
    UserProfileDeleteView,
    UserProfileIndexView,
    UserProfileUpdateView,
    UserProfileView,
)

app_name = "userprofile"

urlpatterns = [
    path("<int:user_id>/", UserProfileIndexView.as_view(), name="index"),
    path("<int:user_id>/detail", UserProfileView.as_view(), name="detail"),
    path("<int:user_id>/add/", UserProfileAddView.as_view(), name="add"),
    path(
        "<int:userprofile_id>/update/", UserProfileUpdateView.as_view(), name="update"
    ),
    path(
        "<int:userprofile_id>/delete/", UserProfileDeleteView.as_view(), name="delete"
    ),
]
