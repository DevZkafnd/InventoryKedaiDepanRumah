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

# Daftar package yang dibutuhkan: (import_name, pip_package, versi)
$packages = @(
    @{ import = "django";        pip = "django==6.0.5" },
    @{ import = "rest_framework"; pip = "djangorestframework==3.17.1" },
    @{ import = "dotenv";        pip = "python-dotenv==1.2.1" },
    @{ import = "axes";          pip = "django-axes==8.3.1" },
    @{ import = "anymail";       pip = "django-anymail==15.0" },
    @{ import = "openpyxl";      pip = "openpyxl==3.1.5" },
    @{ import = "natsort";       pip = "natsort==8.4.0" },
    @{ import = "pytz";          pip = "pytz==2026.2" }
)

# Ubah ke direktori script
Set-Location $PSScriptRoot

Write-Header

# Cek Python
Write-Info "Memeriksa Python..."
try {
    $pyver = python --version 2>&1
    Write-OK "$pyver ditemukan"
} catch {
    Write-Err "Python tidak ditemukan! Install dari https://python.org"
    Read-Host "Tekan Enter untuk keluar"
    exit 1
}

# Cek pip
try {
    pip --version | Out-Null
    Write-OK "pip ditemukan"
} catch {
    Write-Err "pip tidak ditemukan!"
    exit 1
}

# Cek & install dependencies
Write-Host ""
Write-Info "Memeriksa dependencies..."
Write-Host ""

foreach ($pkg in $packages) {
    $check = python -c "import $($pkg.import)" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Inst "Menginstall $($pkg.pip)..."
        pip install $($pkg.pip) -q
        if ($LASTEXITCODE -ne 0) {
            Write-Err "Gagal menginstall $($pkg.pip)"
            Read-Host "Tekan Enter untuk keluar"
            exit 1
        }
        Write-OK "$($pkg.pip) berhasil diinstall"
    } else {
        Write-OK "$($pkg.import) sudah terinstall"
    }
}

Write-Host ""
Write-OK "Semua dependencies siap."

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
python manage.py migrate --run-syncdb
if ($LASTEXITCODE -ne 0) {
    Write-Err "Migrasi database gagal!"
    Read-Host "Tekan Enter untuk keluar"
    exit 1
}
Write-OK "Database siap"

# Seed data
Write-Host ""
Write-Info "Mengisi data contoh ke database..."
python seed_data.py
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

python manage.py runserver 8000
