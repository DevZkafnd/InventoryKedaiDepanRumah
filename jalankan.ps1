# ============================================================
#  Inventory Kedai Depan Rumah - Setup & Jalankan
#  Jalankan dengan: powershell -ExecutionPolicy Bypass -File jalankan.ps1
# ============================================================

$Host.UI.RawUI.WindowTitle = "Inventory Kedai Depan Rumah"
$ErrorActionPreference = "Stop"

function Write-Header {
    Write-Host ""
    Write-Host " ========================================================" -ForegroundColor Cyan
    Write-Host "      INVENTORY KEDAI DEPAN RUMAH                       " -ForegroundColor Cyan
    Write-Host "      Setup Otomatis dan Jalankan Aplikasi              " -ForegroundColor Cyan
    Write-Host " ========================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-OK   { param($msg) Write-Host " [OK]      $msg" -ForegroundColor Green }
function Write-Info { param($msg) Write-Host " [INFO]    $msg" -ForegroundColor Yellow }
function Write-Inst { param($msg) Write-Host " [INSTALL] $msg" -ForegroundColor Magenta }
function Write-Err  { param($msg) Write-Host " [ERROR]   $msg" -ForegroundColor Red }
function Write-Warn { param($msg) Write-Host " [WARN]    $msg" -ForegroundColor DarkYellow }

# Ubah ke direktori script
Set-Location $PSScriptRoot
$requirementsFile = Join-Path $PSScriptRoot "requirements.txt"

function Invoke-UvPython {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    & uv run --with-requirements $requirementsFile python @Arguments
}

Write-Header

# Cek requirements file
if (-not (Test-Path $requirementsFile)) {
    Write-Err "File requirements.txt tidak ditemukan!"
    Read-Host "Tekan Enter untuk keluar"
    exit 1
}

# Cek uv
Write-Info "Memeriksa uv..."
try {
    $uvver = uv --version 2>&1
    Write-OK "$uvver ditemukan"
} catch {
    Write-Err "uv tidak ditemukan! Install uv terlebih dahulu agar script bisa menjalankan Python 3.14 yang stabil."
    Read-Host "Tekan Enter untuk keluar"
    exit 1
}

# Cek Python dari uv
Write-Info "Menyiapkan Python environment via uv..."
try {
    $pyver = Invoke-UvPython --version 2>&1
    Write-OK "$pyver siap dipakai"
} catch {
    Write-Err "Gagal menyiapkan Python via uv."
    exit 1
}

# Cek dependencies via uv
Write-Host ""
Write-Info "Memeriksa dependencies..."
Write-Host ""

Write-Inst "Sinkronisasi environment dari requirements.txt..."
Invoke-UvPython -c "import django, rest_framework, dotenv, axes, anymail, openpyxl, natsort, pytz, requests"
if ($LASTEXITCODE -ne 0) {
    Write-Err "Gagal menyiapkan dependencies dari requirements.txt"
    Read-Host "Tekan Enter untuk keluar"
    exit 1
}

Write-Host ""
Write-OK "Semua dependencies siap via uv."

# Cek file .env
Write-Host ""
if (-not (Test-Path ".env")) {
    Write-Info "File .env tidak ditemukan, membuat dari template..."
    Copy-Item ".env_default" ".env"
    Write-OK "File .env dibuat"
    Write-Warn "Edit .env dan ganti DJANGO_SECRET_KEY untuk keamanan produksi!"
} else {
    Write-OK "File .env sudah ada"
}

# Migrasi database
Write-Host ""
Write-Info "Menjalankan migrasi database..."
Invoke-UvPython manage.py migrate --run-syncdb
if ($LASTEXITCODE -ne 0) {
    Write-Err "Migrasi database gagal!"
    Read-Host "Tekan Enter untuk keluar"
    exit 1
}
Write-OK "Database siap"

# Seed data
Write-Host ""
Write-Info "Mengisi data contoh ke database..."
Invoke-UvPython seed_data.py
if ($LASTEXITCODE -ne 0) {
    Write-Warn "Seed data gagal, tapi aplikasi tetap bisa dijalankan."
}

# Jalankan server
Write-Host ""
Write-Host " ========================================================" -ForegroundColor Green
Write-Host "   Aplikasi siap! Buka browser dan akses:              " -ForegroundColor Green
Write-Host "                                                        " -ForegroundColor Green
Write-Host "     http://127.0.0.1:8000/                            " -ForegroundColor Green
Write-Host "     http://127.0.0.1:8000/admin/                      " -ForegroundColor Green
Write-Host "                                                        " -ForegroundColor Green
Write-Host "   Tekan CTRL+C untuk menghentikan server              " -ForegroundColor Green
Write-Host " ========================================================" -ForegroundColor Green
Write-Host ""

Invoke-UvPython manage.py runserver 8000
