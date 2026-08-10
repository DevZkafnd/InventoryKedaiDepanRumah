@echo off
echo ========================================
echo  Memperbaiki User Admin di NeonTech DB
echo ========================================
echo.
echo Script ini akan:
echo 1. Connect ke database NeonTech PostgreSQL
echo 2. Membuat grup 'managers' jika belum ada
echo 3. Menambahkan user 'admin' ke grup 'managers'
echo 4. Set admin sebagai superuser
echo.
echo PENTING: Pastikan koneksi internet aktif!
echo.
pause

REM Aktifkan virtual environment
call .venv314\Scripts\activate.bat

REM Set DATABASE_URL untuk connect ke NeonTech (Pooled Connection)
set DATABASE_URL=postgresql://neondb_owner:npg_j8ThFKgdmpw7@ep-orange-wildflower-aztc4bgj-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

echo.
echo [INFO] Connecting to NeonTech PostgreSQL...
echo.

REM Jalankan script perbaikan
python fix_admin_groups.py

echo.
echo ========================================
echo  Selesai!
echo ========================================
echo.
echo Silakan coba login lagi di Vercel dengan:
echo URL: https://inventory-kedai-depan-rumah-iota.vercel.app
echo Username: admin
echo Password: admin123
echo.
echo Seharusnya sekarang bisa redirect ke /dashboard/
echo.
pause
