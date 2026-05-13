#!/bin/bash

# Ce script lance les services redis et celery en arriere plan

## Activer l'environnement virtuel
# shellcheck disable=SC1090
source ~/virtualenv/mkinty/mk_portfolio/src/3.11/bin/activate

# Supprimer les anciens processus celery
pkill -f "celery -A config worker" || true

# Supprimer les anciens processus redis
pkill -f "redis-server" || true

# Lancer le serveur redis en arriere plan
redis-server --daemonize yes

# Se place sur le dossier src, ici le fichier celery.py se trouve dans le dossier src
# shellcheck disable=SC2164
cd ~/mkinty/mk_portfolio/src

# Lancer le worker celery
nohup python -m celery -A config worker \
-l info \
--concurrency=2 \
> celery.log 2>&1 &

## Pour lancer ce script, execute ce bash
# chmod +x start_services.sh
# Puis lance le script
# ./start_services.sh

## Puis lancer le serveur ou l'application
# python -m uvicorn app:app --host 0.0.0.0 --port 8000

## Pour arreter les services
# pkill -f redis-server
# pkill -f celery
# pkill -f uvicorn

## Pour verifier les services
# ps aux | grep redis-server
# ps aux | grep celery
# ps aux | grep uvicorn

## Pour verifier les logs
# tail -f celery.log
# tail -f uvicorn.log

