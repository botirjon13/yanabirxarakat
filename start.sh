#!/usr/bin/env bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if env vars present and not exists
if [ -n "$ADMIN_USERNAME" ] && [ -n "$ADMIN_EMAIL" ] && [ -n "$ADMIN_PASSWORD" ]; then
  python - <<PY
from django.contrib.auth import get_user_model
User = get_user_model()
u = "$ADMIN_USERNAME"
e = "$ADMIN_EMAIL"
p = "$ADMIN_PASSWORD"
if not User.objects.filter(username=u).exists():
    User.objects.create_superuser(username=u, email=e, password=p)
    print("Superuser created:", u)
else:
    print("Superuser already exists:", u)
PY
fi

echo "Starting Gunicorn..."
exec gunicorn kassasystem.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3 --timeout 120 --log-file -
