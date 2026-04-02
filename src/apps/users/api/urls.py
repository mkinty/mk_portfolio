from django.urls import path

from apps.users.api.views import MeView, UserListView

urlpatterns = [
    # users
    path("me/", MeView.as_view()),
    path("", UserListView.as_view()),
]
