#!/usr/bin/env bash
set -e
echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser from env if provided
if [ -n "$ADMIN_USERNAME" ] && [ -n "$ADMIN_EMAIL" ] && [ -n "$ADMIN_PASSWORD" ]; then
  echo "Creating superuser..."
  python manage.py shell - <<PY
from django.contrib.auth import get_user_model
User = get_user_model()
username = "$ADMIN_USERNAME"
email = "$ADMIN_EMAIL"
password = "$ADMIN_PASSWORD"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created:", username)
else:
    print("Superuser already exists:", username)
PY
fi

echo "Starting Gunicorn..."
exec gunicorn kassasystem.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --log-file -
