#!/bin/bash
export DJANGO_SETTINGS_MODULE=portfolio.settings
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn portfolio.wsgi:application --bind 0.0.0.0:$PORT