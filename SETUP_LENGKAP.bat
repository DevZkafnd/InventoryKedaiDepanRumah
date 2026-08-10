@echo off
title Setup Lengkap Database NeonTech
color 0A

echo.
echo ================================================================
echo           SETUP LENGKAP DATABASE NEONTECH
echo         Inventory Kedai Depan Rumah v1.0
echo ================================================================
echo.
echo Script ini akan melakukan:
echo.
echo [1] Install semua dependencies yang diperlukan
echo [2] Migrasi database ke NeonTech PostgreSQL
echo [3] Membuat user: admin, owner1, kasir1 dengan role yang benar
echo [4] Seed data barang contoh (25 items)
echo.
echo PENTING:
echo - Pastikan koneksi internet aktif
echo - Proses akan memakan waktu 2-5 menit
echo.
echo ================================================================
echo.
pause

echo.
echo [INFO] Mengaktifkan virtual environment...
call .venv314\Scripts\activate.bat

echo.
echo ================================================================
echo [STEP 1/4] INSTALL DEPENDENCIES
echo ================================================================
echo.
echo [INFO] Menginstall packages untuk Python 3.14...
echo.

REM Upgrade pip dulu
python -m pip install --upgrade pip -q

REM Install dependencies satu per satu untuk menghindari error psycopg2-binary
pip install -q django==6.0.5 djangorestframework==3.17.1 python-dotenv==1.2.1 django-axes==8.3.1 django-anymail==15.0 openpyxl==3.1.5 natsort==8.4.0 pytz==2026.2 asgiref==3.11.1 sqlparse==0.5.5 requests==2.32.3 dj-database-url==2.2.0 whitenoise==6.8.2 gunicorn==23.0.0

REM Install psycopg3 terpisah
pip install -q "psycopg[binary]==3.2.3"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Gagal install dependencies!
    echo [INFO] Coba jalankan: .\install_deps_python314.bat
    pause
    exit /b 1
)

echo.
echo [OK] Dependencies berhasil diinstall!

REM Set DATABASE_URL untuk connect ke NeonTech (Pooled Connection)
set DATABASE_URL=postgresql://neondb_owner:npg_j8ThFKgdmpw7@ep-orange-wildflower-aztc4bgj-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

echo.
echo ================================================================
echo [STEP 2/4] MIGRASI DATABASE KE NEONTECH
echo ================================================================
echo.
echo [INFO] Connecting to NeonTech PostgreSQL...
echo [INFO] Membuat struktur tabel...
echo.
python manage.py migrate

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Gagal migrasi database!
    echo [INFO] Periksa koneksi internet dan DATABASE_URL
    pause
    exit /b 1
)

echo.
echo [OK] Migrasi database berhasil!

echo.
echo ================================================================
echo [STEP 3/4] SEED DATA (USERS + GROUPS)
echo ================================================================
echo.
echo [INFO] Membuat user admin, owner1, kasir1...
echo [INFO] Mengisi data barang contoh...
echo.
python seed_data.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Gagal seed data!
    pause
    exit /b 1
)

echo.
echo [OK] Seed data berhasil!

echo.
echo ================================================================
echo [STEP 4/4] VERIFIKASI
echo ================================================================
echo.
echo [INFO] Checking database connection...
python -c "import os; os.environ['DATABASE_URL']='postgresql://neondb_owner:npg_j8ThFKgdmpw7@ep-orange-wildflower-aztc4bgj.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'; import django; django.setup(); from django.contrib.auth.models import User; print(f'[OK] Total users: {User.objects.count()}'); print(f\"[OK] User admin exists: {'admin' in [u.username for u in User.objects.all()]}\")"

echo.
echo ================================================================
echo            SETUP SELESAI! DATABASE SIAP DIGUNAKAN
echo ================================================================
echo.
echo [INFO] User yang tersedia:
echo.
echo   ^| Username ^| Password  ^| Role              ^|
echo   ^|----------^|-----------^|-------------------^|
echo   ^| admin    ^| admin123  ^| Manager/Admin     ^|
echo   ^| owner1   ^| owner123  ^| Owner (read-only) ^|
echo   ^| kasir1   ^| kasir123  ^| Kasir/Shop User   ^|
echo.
echo [INFO] Silakan test login di:
echo   https://inventory-kedai-depan-rumah-iota.vercel.app/accounts/login/
echo.
echo [INFO] Seharusnya:
echo   - admin redirect ke /dashboard/
echo   - owner1 redirect ke /dashboard/
echo   - kasir1 redirect ke /shop/
echo.
echo ================================================================
echo.
pause
