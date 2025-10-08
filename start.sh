#!/bin/bash
set -e  # Agar biror buyruq xato bo‘lsa — skript to‘xtaydi

echo "🚀 Starting Django setup..."

# 1️⃣ Migrate database
echo "Running migrations..."
python manage.py migrate --noinput

# 2️⃣ Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 3️⃣ Create superuser (if not exists)
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
username = 'admin';
password = 'admin123';
email = 'admin@example.com';
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password);
    print('✅ Superuser created: admin / admin123');
else:
    print('ℹ️ Superuser already exists.');
"

# 4️⃣ Run server
echo "Starting Django server..."
gunicorn kassasystem.wsgi:application --bind 0.0.0.0:8000
