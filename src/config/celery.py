import os

from celery import Celery

# Définit le module de settings Django à utiliser
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

# Crée l'application Celery
app = Celery("portfolio")

# Charge la configuration depuis les settings Django,
# avec le préfixe CELERY_ pour ne prendre que les variables CELERY_*
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-détecte les tasks dans toutes les apps installées
app.autodiscover_tasks()

# Optionnel : affichage de logs plus clairs pour dev
app.conf.update(
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)
