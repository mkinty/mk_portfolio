# Architecture du projet Django Portfolio

Ce document décrit l’organisation du projet Django `portfolio`, ses dossiers, apps et fichiers principaux, ainsi que la structure interne des apps.

---

## 1. Structure globale du projet

```text
portfolio/
├── .env                  # Variables d'environnement
├── .gitignore
├── mkdocs.yml            # Documentation
├── project.toml          # Gestion des dépendances
├── uv.lock               # Fichier de lock des dépendances
├── README.md
└── src/
    ├── apps/             # Contient toutes les applications Django
    │   ├── users/
    │   │   ├── models.py
    │   │   ├── services/
    │   │   │   └── user_service.py
    │   │   ├── selectors/
    │   │   │   └── user_selector.py
    │   │   ├── web/
    │   │   │   └── views.py
    │   │   └── tests/
    │   │
    │   ├── authentication/
    │   │   ├── services/
    │   │   │   ├── auth_service.py
    │   │   │   └── password_service.py
    │   │   ├── selectors/
    │   │   │   └── auth_selector.py
    │   │   ├── web/
    │   │   │   └── views.py
    │   │   └── tests/
    │   │
    │   └── notifications/
    │       ├── tasks.py
    │       ├── services/
    │       │   └── email_service.py
    │       └── templates/
    │
    ├── config/           # Configuration globale Django
    │   ├── settings/
    │   │   ├── settings.py
    │   │   ├── dev.py
    │   │   └── prod.py
    │   ├── asgi.py
    │   ├── celery.py
    │   ├── urls.py
    │   └── wsgi.py
    │
    ├── static/           # Fichiers statiques (CSS, JS, images)
    │   ├── css/
    │   ├── js/
    │   └── images/
    │
    └── templates/        # Templates Django
```

## 2. Détails des apps

### 2.1 App `users`

- **models.py** : définition des modèles utilisateurs  
- **services/user_service.py** : logique métier liée aux utilisateurs  
- **selectors/user_selector.py** : récupération et filtrage des données  
- **web/views.py** : endpoints web ou API  
- **tests/** : tests unitaires et d’intégration  

### 2.2 App `authentication`

- **services/auth_service.py** : gestion de l’authentification (login, tokens)  
- **services/password_service.py** : gestion des mots de passe et sécurité  
- **selectors/auth_selector.py** : récupération de données liées à l’authentification  
- **web/views.py** : endpoints web/API pour l’authentification  
- **tests/** : tests unitaires et d’intégration  

### 2.3 App `notifications`

- **tasks.py** : tâches asynchrones Celery  
- **services/email_service.py** : envoi d’emails  
- **templates/** : templates pour emails/notifications  

---

## 3. Variables d’environnement (`.env`)

```env
DEBUG=True
SECRET_KEY=django-insecure-xxxxxxxxxxxxxxxxxxxxxxxx
DJANGO_SETTINGS_MODULE=config.settings.dev

POSTGRES_DB=db_name
POSTGRES_USER=user_name
POSTGRES_PASSWORD=***
POSTGRES_HOST=host_name
POSTGRES_PORT=5432

CELERY_BROKER_URL=url
```

## 4. Notes importantes

- Les apps suivent une architecture hexagonale simplifiée avec dossiers `services`, `selectors`, `web` et `tests`.  
- La configuration est segmentée par environnement (`dev.py`, `prod.py`) pour faciliter le déploiement.  
- Les fichiers statiques et templates sont centralisés sous `src/`.  
- Celery est configuré dans `config/celery.py` et les tâches sont définies dans les apps spécifiques (ici `notifications`).  