from django.urls import path

from apps.home.web.views import HomePageView

app_name = "home"
urlpatterns = [
    path("", HomePageView.as_view(), name="home-page"),
]
