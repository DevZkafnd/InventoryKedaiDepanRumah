@echo off
echo ========================================
echo  Install Dependencies (Python 3.14)
echo ========================================
echo.
echo Script ini akan install dependencies
echo dengan psycopg3 yang support Python 3.14
echo.
pause

REM Aktifkan virtual environment
call .venv314\Scripts\activate.bat

echo.
echo [INFO] Upgrade pip dulu...
python -m pip install --upgrade pip

echo.
echo [INFO] Install dependencies (skip psycopg2-binary yang error)...
echo.

REM Install semua kecuali psycopg2-binary
pip install -q django==6.0.5
pip install -q djangorestframework==3.17.1
pip install -q python-dotenv==1.2.1
pip install -q django-axes==8.3.1
pip install -q django-anymail==15.0
pip install -q openpyxl==3.1.5
pip install -q natsort==8.4.0
pip install -q pytz==2026.2
pip install -q asgiref==3.11.1
pip install -q sqlparse==0.5.5
pip install -q requests==2.32.3
pip install -q dj-database-url==2.2.0
pip install -q whitenoise==6.8.2
pip install -q gunicorn==23.0.0

echo.
echo [INFO] Install psycopg3 (support Python 3.14)...
pip install "psycopg[binary]==3.2.3"

echo.
echo ========================================
echo  Install Selesai!
echo ========================================
echo.
echo Packages terinstall:
pip list | findstr "django psycopg dj-database"
echo.
pause
