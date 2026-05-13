from django.urls import path

from apps.home.web.views import ContactPageView, HomePageView

app_name = "home"
urlpatterns = [
    path("", HomePageView.as_view(), name="home-page"),
    path("contact/", ContactPageView.as_view(), name="contact-page"),
]
