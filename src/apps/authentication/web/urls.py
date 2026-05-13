from django.urls import path

from .views import (
    ActivateAccountView,
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RegistrationView,
)

app_name = "auth"
urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path(
        "activate/<str:uidb64>/<str:token>/",
        ActivateAccountView.as_view(),
        name="activate",
    ),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path(
        "password-reset/<str:uidb64>/<str:token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
