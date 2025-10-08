#!/bin/bash
set -e

echo "🚀 Starting Django setup..."

# Django environment variable
export DJANGO_SETTINGS_MODULE=kassasystem.settings

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser (if not exists)..."
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get("ADMIN_USERNAME", "admin")
email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
password = os.environ.get("ADMIN_PASSWORD", "admin123")
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✅ Superuser created.")
else:
    print("ℹ️ Superuser already exists.")
EOF

echo "Starting Django server..."
exec gunicorn kassasystem.wsgi:application --bind 0.0.0.0:$PORT
