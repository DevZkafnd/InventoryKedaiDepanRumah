@echo off
REM First Run Setup Script
echo ========================================
echo Inventory Kedai - First Run Setup
echo ========================================
echo.

cd /d %~dp0

REM Check if .env exists, if not copy from .env_default
if not exist .env (
    echo Membuat file konfigurasi .env...
    copy .env_default .env
    echo File .env telah dibuat.
)

REM Generate Django secret key jika belum ada
if exist config_secretkey.txt (
    echo Menggunakan secret key kustom...
    for /f "delims=" %%a in (config_secretkey.txt) do set SECRET_KEY=%%a
    powershell -Command "(gc .env) -replace 'YOUR_SECRET_KEY', '%SECRET_KEY%' | Out-File -encoding ASCII .env"
    del config_secretkey.txt
) else (
    echo Generating Django secret key...
    python-embed\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > temp_key.txt
    for /f "delims=" %%a in (temp_key.txt) do set SECRET_KEY=%%a
    powershell -Command "(gc .env) -replace 'YOUR_SECRET_KEY', '%SECRET_KEY%' | Out-File -encoding ASCII .env"
    del temp_key.txt
)

REM Install dependencies
echo.
echo Installing Python dependencies...
python-embed\python.exe -m pip install --upgrade pip --quiet
python-embed\python.exe -m pip install -r requirements.txt --quiet

REM Run migrations
echo.
echo Setting up database...
python-embed\python.exe manage.py makemigrations --no-input
python-embed\python.exe manage.py migrate --no-input

REM Collect static files
echo.
echo Collecting static files...
python-embed\python.exe manage.py collectstatic --no-input --clear

REM Create superuser dengan prompt
echo.
echo ========================================
echo PENTING: Buat akun administrator
echo ========================================
python-embed\python.exe manage.py createsuperuser

echo.
echo ========================================
echo Setup selesai!
echo ========================================
echo Aplikasi siap digunakan.
echo.
pause
