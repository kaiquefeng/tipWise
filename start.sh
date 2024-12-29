#!/bin/bash

# Número de workers baseado no número de cores CPU
WORKERS=$((2 * $(nproc) + 1))

# Iniciar o Gunicorn
exec gunicorn --bind 0.0.0.0:${PORT:-8080} \
    --workers ${WORKERS} \
    --worker-class gthread \
    --threads 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    app:app 