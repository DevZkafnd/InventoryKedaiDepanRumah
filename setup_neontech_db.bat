@echo off
echo ================================================================
echo  SETUP DATABASE NEONTECH - Inventory Kedai Depan Rumah
echo ================================================================
echo.
echo Script ini akan:
echo 0. Install dependencies yang diperlukan
echo 1. Migrasi struktur database ke NeonTech PostgreSQL
echo 2. Membuat semua grup user yang diperlukan
echo 3. Membuat user: admin, owner1, kasir1
echo 4. Mengisi data barang contoh
echo.
echo PENTING: Pastikan koneksi internet aktif!
echo.
pause

REM Aktifkan virtual environment
call .venv314\Scripts\activate.bat

REM Set DATABASE_URL untuk connect ke NeonTech
set DATABASE_URL=postgresql://neondb_owner:npg_j8ThFKgdmpw7@ep-orange-wildflower-aztc4bgj.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

echo.
echo ========================================
echo  STEP 0: Install Dependencies
echo ========================================
pip install -q dj-database-url psycopg2-binary

echo.
echo ========================================
echo  STEP 1: Migrasi Database
echo ========================================
python manage.py migrate

echo.
echo ========================================
echo  STEP 2: Seed Data (Users + Items)
echo ========================================
python seed_data.py

echo.
echo ================================================================
echo  SETUP SELESAI!
echo ================================================================
echo.
echo User yang tersedia:
echo.
echo   Username: admin      Password: admin123    Role: Manager/Admin
echo   Username: owner1     Password: owner123    Role: Owner (Read-only)
echo   Username: kasir1     Password: kasir123    Role: Kasir/Shop User
echo.
echo Silakan login di:
echo https://inventory-kedai-depan-rumah-iota.vercel.app/accounts/login/
echo.
pause
