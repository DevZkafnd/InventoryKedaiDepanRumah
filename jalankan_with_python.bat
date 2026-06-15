@echo off
REM Jalankan aplikasi dengan Python embedded
echo ========================================
echo Inventory Kedai - Starting Server
echo ========================================
echo.

cd /d %~dp0

REM Check konfigurasi port
set PORT=8000
if exist config_port.txt (
    for /f "delims=" %%a in (config_port.txt) do set PORT=%%a
)

echo Server akan berjalan di: http://127.0.0.1:%PORT%
echo.
echo Tekan Ctrl+C untuk menghentikan server
echo ========================================
echo.

REM Jalankan Django development server
python-embed\python.exe manage.py runserver %PORT%

pause
