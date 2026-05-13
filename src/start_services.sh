#!/bin/bash

set -e

echo "=== STOP OLD SERVICES ==="
pkill -f "celery -A config worker" || true
pkill -f "redis-server" || true

echo "=== START REDIS ==="
redis-server --daemonize yes

sleep 3

echo "=== START CELERY ==="
nohup python -m celery \
  -A config worker \
  -l info \
  --concurrency=2 \
  > celery.log 2>&1 &

sleep 5

echo "=== SERVICES STARTED ==="

