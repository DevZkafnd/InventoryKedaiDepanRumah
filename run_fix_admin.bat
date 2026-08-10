@echo off
echo ========================================
echo  Memperbaiki User Admin di Production
echo ========================================
echo.
echo PENTING: Script ini akan menggunakan DATABASE_URL
echo dari file .env (pastikan sudah diset ke NeonTech)
echo.
pause

REM Aktifkan virtual environment
call .venv314\Scripts\activate.bat

REM Jalankan script perbaikan
python fix_admin_groups.py

echo.
echo ========================================
echo  Selesai!
echo ========================================
echo.
echo Silakan coba login lagi dengan:
echo Username: admin
echo Password: admin123
echo.
pause
