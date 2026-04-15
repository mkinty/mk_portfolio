# Makefile professionnel pour projet Django "portfolio" avec uv, Celery et Redis
# Compatible macOS

# Variables
PYTHON=uv run python
MANAGE=$(PYTHON) src/manage.py
CELERY=PYTHONPATH=src uv run celery -A config worker -l info
REDIS_SERVER=redis-server
LOG_DIR=logs

.PHONY: help install migrate runserver createsuperuser celery redis dev clean

help:
	@echo "Commandes disponibles :"
	@echo "  make install             -> Installer les dépendances via uv"
	@echo "  make migrate             -> Appliquer les migrations Django"
	@echo "  make runserver           -> Lancer le serveur Django"
	@echo "  make createsuperuser     -> Créer un super utilisateur Django"
	@echo "  make celery              -> Lancer le worker Celery"
	@echo "  make redis               -> Lancer Redis"
	@echo "  make dev                 -> Lancer Redis + Celery + Django (logs séparés)"
	@echo "  make clean               -> Supprimer fichiers compilés Python et __pycache__"

# Installer les dépendances via uv
install:
	uv sync

# Effectuer de nouvelles migrations
makemigrations:
	$(MANAGE) makemigrations

# Appliquer les migrations
migrate:
	$(MANAGE) migrate

# Lancer le serveur Django
runserver:
	$(MANAGE) runserver

# Créer un super utilisateur
createsuperuser:
	$(MANAGE) createsuperuser

# Lancer Celery worker
celery:
	$(CELERY)

# Lancer Redis en local (macOS/Homebrew)
redis:
	@echo "Démarrage de Redis..."
	@command -v redis-server >/dev/null 2>&1 || { echo "Redis n'est pas installé. Faites 'brew install redis'"; exit 1; }
	mkdir -p $(LOG_DIR)
	$(REDIS_SERVER) > $(LOG_DIR)/redis.log 2>&1 &

# Lancer tout en dev (Redis + Celery + Django) avec logs séparés
dev:
	@echo "Vérification de Redis..."
	@command -v redis-server >/dev/null 2>&1 || { echo "Redis n'est pas installé. Faites 'brew install redis'"; exit 1; }
	mkdir -p $(LOG_DIR)
	@echo "Démarrage de Redis..."
	$(REDIS_SERVER) > $(LOG_DIR)/redis.log 2>&1 &
	@echo "Démarrage de Celery..."
	$(CELERY) > $(LOG_DIR)/celery.log 2>&1 &
	@echo "Démarrage du serveur Django..."
	$(MANAGE) runserver


# Lancer les tests pour l'application users
test-users:
	$(MANAGE) test apps.users

# Tests Django pour toutes les apps
tests:
	PYTHONPATH=src DJANGO_SETTINGS_MODULE=config.settings.dev $(MANAGE) test apps.users

# Tests pytest pour toutes les apps
pytest:
	PYTHONPATH=src DJANGO_SETTINGS_MODULE=config.settings.dev uv run pytest src/apps

# Tests pytest pour une app spécifique
pytest-app:
	PYTHONPATH=src DJANGO_SETTINGS_MODULE=config.settings.dev uv run pytest src/apps/$(APP)

# Coverage pour toutes les apps
coverage:
	PYTHONPATH=src DJANGO_SETTINGS_MODULE=config.settings.dev uv run coverage run --source=src/apps -m pytest src/apps
	PYTHONPATH=src DJANGO_SETTINGS_MODULE=config.settings.dev uv run coverage report -m
	PYTHONPATH=src DJANGO_SETTINGS_MODULE=config.settings.dev uv run coverage html

# Nettoyer fichiers compilés Python
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete