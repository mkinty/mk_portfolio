# ruff: noqa: F403,F405

from .settings import *

DEBUG = False

SECRET_KEY = "test-secret"

ALLOWED_HOSTS = ["*"]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

CELERY_TASK_ALWAYS_EAGER = True

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
