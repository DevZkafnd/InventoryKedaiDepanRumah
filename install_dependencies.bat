@echo off
echo ========================================
echo  Install Dependencies
echo ========================================
echo.
echo Script ini akan install semua packages
echo yang diperlukan dari requirements.txt
echo.
pause

REM Aktifkan virtual environment
call .venv314\Scripts\activate.bat

echo.
echo Installing packages...
echo.
pip install -r requirements.txt

echo.
echo ========================================
echo  Install Selesai!
echo ========================================
echo.
pause
