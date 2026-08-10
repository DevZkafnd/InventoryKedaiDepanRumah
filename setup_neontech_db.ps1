# ================================================================
# SETUP DATABASE NEONTECH - Inventory Kedai Depan Rumah
# ================================================================

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host " SETUP DATABASE NEONTECH - Inventory Kedai Depan Rumah" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Script ini akan:" -ForegroundColor Yellow
Write-Host "1. Migrasi struktur database ke NeonTech PostgreSQL"
Write-Host "2. Membuat semua grup user yang diperlukan"
Write-Host "3. Membuat user: admin, owner1, kasir1"
Write-Host "4. Mengisi data barang contoh"
Write-Host ""
Write-Host "PENTING: Pastikan koneksi internet aktif!" -ForegroundColor Red
Write-Host ""
Write-Host "Tekan Enter untuk melanjutkan atau Ctrl+C untuk batal..." -ForegroundColor Yellow
Read-Host

# Set DATABASE_URL untuk connect ke NeonTech
$env:DATABASE_URL = "postgresql://neondb_owner:npg_j8ThFKgdmpw7@ep-orange-wildflower-aztc4bgj.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " STEP 1: Migrasi Database" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Aktifkan virtual environment dan migrate
& .\.venv314\Scripts\Activate.ps1
python manage.py migrate

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " STEP 2: Seed Data (Users + Items)" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

python seed_data.py

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host " SETUP SELESAI!" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "User yang tersedia:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Username: admin      Password: admin123    Role: Manager/Admin" -ForegroundColor Green
Write-Host "  Username: owner1     Password: owner123    Role: Owner (Read-only)" -ForegroundColor Green
Write-Host "  Username: kasir1     Password: kasir123    Role: Kasir/Shop User" -ForegroundColor Green
Write-Host ""
Write-Host "Silakan login di:" -ForegroundColor Yellow
Write-Host "https://inventory-kedai-depan-rumah-iota.vercel.app/accounts/login/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tekan Enter untuk keluar..." -ForegroundColor Gray
Read-Host
