from django.urls import path

from apps.certifications.web.views import (
    CertificationsAddView,
    CertificationsDeleteView,
    CertificationsUpdateView,
)

app_name = "certifications"

urlpatterns = [
    path("<int:user_id>/add/", CertificationsAddView.as_view(), name="add"),
    path(
        "<int:certification_id>/update/",
        CertificationsUpdateView.as_view(),
        name="update",
    ),
    path(
        "<int:certification_id>/delete/",
        CertificationsDeleteView.as_view(),
        name="delete",
    ),
]
