@echo off
chcp 65001 >nul
title Inventory Kedai Depan Rumah - Setup & Jalankan

echo.
echo  ╔══════════════════════════════════════════════════════╗
echo  ║     INVENTORY KEDAI DEPAN RUMAH                     ║
echo  ║     Setup Otomatis dan Jalankan Aplikasi             ║
echo  ╚══════════════════════════════════════════════════════╝
echo.

:: ── Cek Python tersedia ──────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan!
    echo         Silakan install Python 3.10+ dari https://python.org
    echo         Pastikan centang "Add Python to PATH" saat instalasi.
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [OK] Python %PYVER% ditemukan

:: ── Cek pip tersedia ─────────────────────────────────────────
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip tidak ditemukan. Coba jalankan: python -m ensurepip
    pause
    exit /b 1
)
echo [OK] pip ditemukan

:: ── Cek dan install dependencies ─────────────────────────────
echo.
echo [INFO] Memeriksa dan menginstall dependencies...
echo.

python -c "import django" >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Menginstall django...
    pip install django==6.0.5 -q
) else (
    for /f "tokens=2" %%v in ('python -c "import django; print(django.__version__)"') do set DV=%%v
    python -c "import django; print(django.__version__)" >tmp_ver.txt 2>&1
    set /p DV=<tmp_ver.txt
    del tmp_ver.txt >nul 2>&1
    echo [OK] django sudah terinstall ^(%DV%^)
)

python -c "import rest_framework" >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Menginstall djangorestframework...
    pip install djangorestframework==3.17.1 -q
) else (
    echo [OK] djangorestframework sudah terinstall
)

python -c "import dotenv" >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Menginstall python-dotenv...
    pip install python-dotenv==1.2.1 -q
) else (
    echo [OK] python-dotenv sudah terinstall
)

python -c "import axes" >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Menginstall django-axes...
    pip install django-axes==8.3.1 -q
) else (
    echo [OK] django-axes sudah terinstall
)

python -c "import anymail" >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Menginstall django-anymail...
    pip install django-anymail==15.0 -q
) else (
    echo [OK] django-anymail sudah terinstall
)

python -c "import openpyxl" >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Menginstall openpyxl...
    pip install openpyxl==3.1.5 -q
) else (
    echo [OK] openpyxl sudah terinstall
)

python -c "import natsort" >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Menginstall natsort...
    pip install natsort==8.4.0 -q
) else (
    echo [OK] natsort sudah terinstall
)

python -c "import pytz" >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Menginstall pytz...
    pip install pytz==2026.2 -q
) else (
    echo [OK] pytz sudah terinstall
)

python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo [INSTALL] Menginstall requests...
    pip install requests==2.32.3 -q
) else (
    echo [OK] requests sudah terinstall
)

echo.
echo [OK] Semua dependencies siap.

:: ── Cek file .env ────────────────────────────────────────────
echo.
if not exist ".env" (
    echo [INFO] File .env tidak ditemukan, membuat dari template...
    copy ".env_default" ".env" >nul
    echo [OK] File .env dibuat dari .env_default
    echo [PERHATIAN] Silakan edit .env dan isi DJANGO_SECRET_KEY yang aman untuk produksi.
) else (
    echo [OK] File .env sudah ada
)

:: ── Setup database ───────────────────────────────────────────
echo.
echo [INFO] Menjalankan migrasi database...
python manage.py migrate --run-syncdb 2>&1
if errorlevel 1 (
    echo [ERROR] Migrasi database gagal!
    pause
    exit /b 1
)
echo [OK] Database siap

:: ── Seed data contoh ─────────────────────────────────────────
echo.
echo [INFO] Mengisi data contoh ke database...
python seed_data.py
if errorlevel 1 (
    echo [PERINGATAN] Seed data gagal, tapi aplikasi tetap bisa dijalankan.
)

:: ── Jalankan server ──────────────────────────────────────────
echo.
echo  ╔══════════════════════════════════════════════════════╗
echo  ║  Aplikasi siap! Buka browser dan akses:             ║
echo  ║                                                      ║
echo  ║    http://127.0.0.1:8000/                           ║
echo  ║    http://127.0.0.1:8000/admin/                     ║
echo  ║                                                      ║
echo  ║  Tekan CTRL+C untuk menghentikan server             ║
echo  ╚══════════════════════════════════════════════════════╝
echo.

python manage.py runserver 8000
