from django.urls import path
from .views import user_list_view

app_name = "users"

urlpatterns = [
    path("", user_list_view, name="user-list"),
]
