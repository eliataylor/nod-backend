#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Run database migrations
python manage.py makemigrations && python manage.py migrate && python manage.py migrate --run-syncdb

# Create a superuser if it does not exist
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ] && [ "$DJANGO_SUPERUSER_EMAIL" ]; then
    python manage.py createsuperuser --noinput || true
fi

# Run the gunicorn server
exec gunicorn nod_backend.wsgi:application --bind 0.0.0.0:8000 --workers 1 --threads 8