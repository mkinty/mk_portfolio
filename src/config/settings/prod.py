from .settings import *

# Debug
DEBUG = False

# Allowed hosts
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "mkinty.kmyprod.com").split(",")

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT", 5432),
    }
}

# Media files
MEDIA_URL = os.getenv("MEDIA_URL", "/media/")
MEDIA_ROOT = os.getenv("MEDIA_ROOT", "/var/www/mkportfolio/media")

# Static files
STATIC_URL = os.getenv("STATIC_URL", "/static/")
STATIC_ROOT = os.getenv("STATIC_ROOT", "/var/www/mkportfolio/staticfiles")


# Celery
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# Rediriger toutes les requêtes HTTP vers HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Email config
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # backend SMTP par défaut
EMAIL_HOST = "smtp.gmail.com"  # serveur SMTP
EMAIL_PORT = 587  # port SMTP
EMAIL_USE_TLS = True  # protocole TLS
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")  # l’adresse email expéditeur
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # mot de passe ou token