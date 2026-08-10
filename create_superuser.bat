@echo off
echo ========================================
echo Create Superuser untuk Production (Neon)
echo ========================================
echo.

REM Set environment variables
set DATABASE_URL=postgresql://neondb_owner:npg_j8ThFKgdmpw7@ep-orange-wildflower-aztc4bgj.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
set DJANGO_SECRET_KEY=bbr+#nr)bxx^rgno4ki@=ecu*6bl^i-3^cu*v+=rqa6o0^1#h+
set DJANGO_DEBUG=False
set DJANGO_ALLOWED_HOSTS=localhost
set AXES_FAILURE_LIMIT=5
set AXES_COOLOFF_TIME=30
set ALLOW_PW_CHANGE=True

echo Environment variables set!
echo Connecting to Neon PostgreSQL...
echo.

REM Create superuser
python manage.py createsuperuser

echo.
echo ========================================
echo Done!
echo ========================================
pause
