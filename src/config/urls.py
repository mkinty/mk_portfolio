"""
URL configuration for portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # CKEditor 5
    path('ckeditor5/', include('django_ckeditor_5.urls')),

    # API
    path("api/users/", include("apps.users.api.urls")),
    # path("api/auth/", include("apps.authentication.api.urls")),

    # API documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # Web (templates Django)
    path("", include("apps.home.web.urls", namespace="home")),
    path("users/", include("apps.users.web.urls", namespace="users")),
    path("auth/", include("apps.authentication.web.urls", namespace="auth")),
    path("userprofile/", include("apps.userprofile.web.urls", namespace="userprofile")),
    path("projects/", include("apps.projects.web.urls", namespace="projects")),
    path("tracking/", include("apps.tracking.web.urls", namespace="tracking")),
    path("experiences/", include("apps.experiences.web.urls", namespace="experiences")),
    path("skills/", include("apps.skills.web.urls", namespace="skills")),
    path("education/", include("apps.education.web.urls", namespace="education")),
]

# Servir les fichiers media et statiques seulement en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
