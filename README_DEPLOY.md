
Railway deployment instructions:

1. Push this repository to GitHub.
2. Create a new project in Railway and connect your GitHub repo.
3. Railway will auto-detect Python. Set environment variables:
   - DJANGO_SECRET_KEY
   - DATABASE_URL (Railway can provide a managed PostgreSQL)
   - ADMIN_USERNAME
   - ADMIN_EMAIL
   - ADMIN_PASSWORD
4. Railway will run './start.sh' (Procfile specifies it). The script runs migrations, collects static and creates superuser (if env vars present).
5. Open the deployed URL and visit /admin to login.
