
# 📦 Inventory Management System - Kedai Depan Rumah

Sistem manajemen inventory modern dengan **AI Assistant** berbasis **Groq (Llama)** untuk membantu bisnis Anda lebih efisien!

![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Django](https://img.shields.io/badge/django-6.0.5-orange.svg)
![AI](https://img.shields.io/badge/AI-Groq%20(Llama)-purple.svg)

## ✨ Fitur Utama

### 📊 Core Features
- ✅ Real-time Inventory Tracking - Monitor stok gudang &amp; stok toko
- ✅ Multi-user &amp; Role-based Access - Strict RBAC untuk Owner, Manajer, dan Kasir
- ✅ Transfer Management - Request transfer, submit request, approve/cancel oleh manajer
- ✅ Waste Management Module - Pencatatan penyusutan barang (rusak/basi) di luar penjualan untuk menekan kerugian finansial
- ✅ Maintenance Mode (Edit Lock) - Transfer diblok saat gudang sedang maintenance
- ✅ Excel Export/Import - Export laporan Excel, import via upload (bisa diaktif/nonaktifkan)
- ✅ Soft Delete Barang - Delete barang via flag `is_active` (data tetap aman)
- ✅ Pagination Configurable - `records_per_page` &amp; override `page_size` via query param
- ✅ Expiry Date Tracking - Catat &amp; monitor tanggal kadaluarsa barang
- ✅ Responsive UI - Tampilan optimal di desktop &amp; mobile

### 🤖 AI Assistant (Groq - Llama)
- ✅ Q&amp;A System - Tanya jawab inventory management
- ✅ Inventory Insights - Generate insight berbasis data inventory
- ✅ Model Modes - `fast | balanced | quality`
- ✅ Token Efficient - Default max tokens (hemat biaya)
- ✅ Rate Limit Per User - Ask: 20/jam, Insights: 10/jam
- ✅ Simple Queue System - Rate limiting internal untuk API provider

### 🔒 Security Features
- ✅ Anti SQL Injection &amp; XSS Prevention - Pattern detection pada middleware
- ✅ Rate Limiting (Middleware) - Max 100 request/menit per IP
- ✅ DRF Throttling - `anon: 100/day`, `user: 100/second`
- ✅ Login Protection (Django Axes) - `AXES_FAILURE_LIMIT` &amp; `AXES_COOLOFF_TIME` via `.env`
- ✅ CSRF Protection - Django CSRF protection built-in

### 🎨 Design System
- ✅ Minimalist Black/White/Green Theme - Warna bersih dan profesional
- ✅ Custom Logo Integration - Logo Kedai Depan Rumah di semua halaman
- ✅ Smooth Animations - Animasi halus untuk pengalaman pengguna yang baik

## 🚀 Instalasi - Mudah &amp; Cepat!

### Pilih Cara Instalasi:

#### Opsi 1: Jalankan Script Otomatis (Windows)

**Untuk Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy Bypass -File jalankan.ps1
```

**Untuk Windows (Command Prompt):**
```cmd
jalankan.bat
```

Script ini akan otomatis:
1. Memeriksa Python &amp; pip
2. Menginstall semua dependencies
3. Membuat file .env dari template
4. Menjalankan database migration
5. Mengisi seed data (jika ada)
6. Menjalankan development server!

#### Opsi 2: Instalasi Manual

##### 1️⃣ Clone atau Download Repository
```bash
git clone https://github.com/DevZkafnd/InventoryKedaiDepanRumah.git
cd InventoryKedaiDepanRumah
```

##### 2️⃣ Install Dependencies
```bash
pip install django==6.0.5 djangorestframework==3.17.1 python-dotenv==1.2.1 django-axes==8.3.1 django-anymail==15.0 openpyxl==3.1.5 natsort==8.4.0 pytz==2026.2 requests==2.32.3
```

##### 3️⃣ Setup Environment Variables
Copy file `.env_default` menjadi `.env`:
```bash
copy .env_default .env
```

Edit file `.env` dan sesuaikan konfigurasi:
```env
# Django
DJANGO_SECRET_KEY='generate-your-secret-key-here'
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS='127.0.0.1,localhost'

# AI Provider (pilih salah satu: gemini atau groq)
AI_PROVIDER='groq'

# AI API Keys
GROQ_API_KEY='your-groq-api-key-here'
GEMINI_API_KEY='your-gemini-api-key-here'  # opsional (client tersedia, endpoint saat ini memakai Groq)
```

**Generate Django Secret Key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

##### 4️⃣ Database Migration
```bash
python manage.py migrate
```

##### 5️⃣ (Opsional) Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

##### 6️⃣ (Opsional) Collect Static Files
```bash
python manage.py collectstatic --noinput
```

##### 7️⃣ Run Development Server
```bash
python manage.py runserver
```

Aplikasi akan berjalan di: **http://127.0.0.1:8000**

## 📋 Panduan Penggunaan

### Akses Aplikasi
1. Buka browser dan kunjungi `http://127.0.0.1:8000`
2. Anda akan melihat **Landing Page** yang modern
3. Klik tombol **"Masuk ke Dashboard"**
4. Login dengan username dan password yang telah dibuat

### Navigasi Sidebar
1. 🏠 **Dashboard** - Overview stok, grafik, dan statistik
2. 🏢 **Stok Gudang** - Kelola barang di gudang
3. 🛍️ **Stok Toko** - Lihat stok toko (per user toko)
4. ↔️ **Transfer Barang** - Request dan approve transfer barang
5. 📊 **Laporan** - Analisis, export Excel, dan print laporan
6. 🤖 **AI Assistant** - Tanya jawab dan insights dengan AI

### Fitur AI Assistant
AI Assistant saat ini menggunakan **Groq API** (model Llama) untuk Q&amp;A dan insights.

## 📂 Struktur Project - Detail!

Berikut penjelasan setiap file dan folder di project:

### 📁 Root Files
| File | Deskripsi |
|------|-----------|
| `manage.py` | Script manajemen Django (run server, migrate, dll) |
| `.env_default` | Template environment variables |
| `.gitignore` | File yang diabaikan oleh Git |
| `LICENSE` | Lisensi proyek (MIT) |
| `README.md` | Dokumentasi proyek (file ini) |
| `COMPLETE_FEATURES.md` | Daftar fitur lengkap dan testing guide |
| `DASHBOARD_GUIDE.md` | Panduan penggunaan dashboard |
| `TESTING_GUIDE.md` | Panduan testing aplikasi |
| `LOGO_IMPLEMENTATION.md` | Panduan implementasi logo |
| `frontend.md` | Dokumentasi frontend |
| `seed_data.py` | Script untuk mengisi data awal ke database |

### 📁 Startup Scripts (Windows)
| File | Deskripsi |
|------|-----------|
| `jalankan.bat` | Script otomatis untuk Command Prompt |
| `jalankan.ps1` | Script otomatis untuk PowerShell |
| `jalankan_with_python.bat` | Script untuk Python embedded (installer) |
| `setup_first_run.bat` | Setup pertama kali installer |

### 📁 `ai_service/` - AI Service Module
Folder ini menangani semua fitur AI Assistant!
| File | Deskripsi |
|------|-----------|
| `__init__.py` | Init file Python package |
| `apps.py` | Konfigurasi app Django untuk ai_service |
| `ai_factory.py` | Factory pattern untuk multi provider (tersedia, belum dipakai oleh endpoint default) |
| `gemini_client.py` | Client untuk Google Gemini API (opsional) |
| `groq_client.py` | Client untuk Groq API (Llama models) |
| `middleware.py` | Security middleware (rate limiting, anti-SQL, anti-XSS) |
| `urls.py` | Routing URL untuk AI endpoints |
| `views.py` | Views untuk AI API endpoints |

### 📁 `email_service/` - Email Service Module
| File | Deskripsi |
|------|-----------|
| `apps.py` | Konfigurasi app Django untuk email_service |
| `email.py` | Fungsi untuk mengirim email (notifikasi transfer, dll) |

### 📁 `ssm/` - Project Settings (Django)
Ini adalah folder konfigurasi inti Django project!
| File | Deskripsi |
|------|-----------|
| `__init__.py` | Init file Python package |
| `settings.py` | **KONFIGURASI UTAMA DJANGO** (database, apps, middleware, static files, dll) |
| `urls.py` | **ROUTING URL UTAMA** (semua URL aplikasi) |
| `wsgi.py` | Konfigurasi WSGI untuk deployment production |

### 📁 `stock_manager/` - Main Inventory App
Ini adalah aplikasi utama yang menangani semua fitur inventory!
| File/Folder | Deskripsi |
|------|-----------|
| `__init__.py` | Init file Python package |
| `admin.py` | Konfigurasi Django Admin interface |
| `apps.py` | Konfigurasi app Django untuk stock_manager |
| `models.py` | **MODEL DATABASE** (Item, ShopItem, TransferItem, WasteItem, Admin, dll) |
| `views.py` | **VIEWS &amp; BUSINESS LOGIC** (semua halaman dan API views) |
| `urls.py` | **ROUTING URL** untuk stock_manager app |
| `serializers.py` | **DRF SERIALIZERS** (convert model ke JSON/XML untuk API) |
| `pagination.py` | Custom pagination untuk API |
| `utils.py` | Helper functions (misalnya: SpreadsheetTools untuk import/export Excel) |
| `tests.py` | Unit tests untuk stock_manager app |
| `static/img/` | Static files untuk stock_manager (logo-black.png, logo-white.png, logo.webp) |
| `custom_funcs/` | Custom functions (folder kosong untuk fitur tambahan) |

### 📁 `templates/` - HTML Templates
Semua halaman web ada di sini!
| File/Folder | Deskripsi |
|------|-----------|
| `landing.html` | **LANDING PAGE** (halaman utama sebelum login) |
| `base_dashboard.html` | **BASE TEMPLATE** untuk semua halaman dashboard (sidebar, topbar, dll) |
| `dashboard.html` | **DASHBOARD UTAMA** (charts, stats cards, recent items) |
| `warehouse.html` | **HALAMAN STOK GUDANG** (tabel barang, search, tambah/edit) |
| `(reuse) warehouse.html` | **HALAMAN STOK TOKO** (`/shop/` - reuse template, data dari `ShopItem`) |
| `transfer.html` | **HALAMAN TRANSFER BARANG** (request dan approve transfer) |
| `reports.html` | **HALAMAN LAPORAN** (charts, export Excel, print) |
| `ai_assistant.html` | **HALAMAN AI ASSISTANT** (chat interface, insights) |
| `index.html` | **OLD DASHBOARD** (backward compatibility) |
| `registration/login.html` | **HALAMAN LOGIN** |
| `registration/password_change_form.html` | Form ganti password |

### 📁 `static/` - Static Files (CSS, JS, Images)
Semua file static (tidak berubah) ada di sini!
| Folder | Deskripsi |
|------|-----------|
| `img/` | Gambar (logo-black.png, logo-white.png, logo.svg) |
| `admin/` | Static files untuk Django Admin (CSS, JS, images) |
| `rest_framework/` | Static files untuk Django REST Framework |

### � `installer/` - Installer Files
| File | Deskripsi |
|------|-----------|
| `setup.iss` | Script untuk Inno Setup (membuat installer Windows) |

## 🛠️ Tech Stack

### Backend
- **Django 6.0.5** - Web framework Python
- **Django REST Framework 3.17.1** - API framework
- **SQLite** - Database (default, bisa diganti MySQL/PostgreSQL)
- **Python-dotenv 1.2.1** - Environment variable management
- **Requests 2.32.3** - HTTP client untuk API calls
- **Openpyxl 3.1.5** - Baca/tulis file Excel
- **Natsort 8.4.0** - Natural sorting untuk list
- **Pytz 2026.2** - Timezone support

### AI &amp; Machine Learning
- **Groq API** - Model: Llama (mode `fast|balanced|quality`)
- **Gemini Client (opsional)** - Client ada di codebase, namun endpoint AI default saat ini memakai Groq

### Security
- **Django Axes 8.3.1** - Brute force protection
- **Custom Middleware** - SQL injection &amp; XSS prevention
- **Rate Limiting** - Request throttling

### Frontend
- **HTML5, CSS3, JavaScript (ES6+)** - Modern web standards
- **Bootstrap 5.3** - CSS framework responsive
- **jQuery 3.7.1** - Library JavaScript
- **Chart.js 4.4.0** - Library untuk grafik/charts
- **Bootstrap Icons 1.11** - Ikon Bootstrap

## 🎨 Design System

### Color Scheme
```css
Primary Color: #10b981 (Green)
Success: #10b981 (Green)
Warning: #555555 (Gray)
Danger: #000000 (Black)
Background: #f5f5f5 (Light Gray)
Dark Background: #000000 (Black)
Text: #000000 (Black)
Muted Text: #555555 (Gray)
```

### Typography
- Font Family: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- Headers: 700 weight
- Body: 400 weight
- Small: 0.85rem

## 🔧 Development Guide

### Run Development Server
```bash
python manage.py runserver
```

### Create Migrations
Setelah merubah `models.py`:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### Access Admin Interface
Buka: `http://127.0.0.1:8000/admin/`

### Run Tests
```bash
python manage.py test
```

### Django Shell
```bash
python manage.py shell
```

Contoh: Tambah data barang dari shell
```python
from stock_manager.models import Item
Item.objects.create(
    sku='TEST-001',
    description='Produk Test',
    quantity=50,
    purchase_price=15000,
    expiry_date='2026-12-31'
)
```

## 📊 API Endpoints

Berikut daftar endpoint API utama:

### Auth
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/auth/user/` | Dapatkan informasi user yang login |
| POST | `/auth/token/` | Token auth (opsional) |

### Inventory
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/items/` | Dapatkan semua barang di gudang |
| POST | `/api/items/` | Tambah barang baru |
| GET | `/api/items/&lt;sku&gt;/` | Dapatkan detail barang by SKU |
| PUT/PATCH | `/api/items/&lt;sku&gt;/` | Update barang |
| DELETE | `/api/items/&lt;sku&gt;/` | Hapus barang (soft delete) |
| GET | `/api/shop_items/` | Dapatkan barang di toko |
| GET | `/api/transfer_items/` | Dapatkan transfer barang |

### Transfer Actions
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/api/transfer/` | Tambah/update item pending transfer (shop user) |
| POST | `/api/submit-transfer-request/` | Submit semua pending transfer (set `ordered=true` + email opsional) |
| POST | `/api/complete-transfer/` | Approve/cancel transfer (manajer) |
| POST | `/api/set_edit_lock_status/` | Aktif/nonaktif maintenance mode (manajer) |
| GET | `/api/get_edit_lock_status/` | Cek maintenance mode |

### AI
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/api/ai/ask/` | Tanya jawab dengan AI |
| POST | `/api/ai/inventory-insights/` | Dapatkan insights dari data inventory |
| GET | `/api/ai/status/` | Cek status dan quota AI |

### Reports
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/export_data/` | Export laporan ke Excel |
| POST | `/api/import_data/` | Import data via upload Excel (manajer + tergantung konfigurasi) |
| GET | `/api/app_config/` | Ambil konfigurasi aplikasi (records per page, dll) |

## 🔒 Security Features

### Built-in Security Features
1. **Anti SQL Injection**
   - Pattern detection untuk query berbahaya
   - Parameterized queries di Django ORM

2. **XSS Prevention**
   - Input sanitization
   - HTML escaping otomatis di templates

3. **Rate Limiting**
   - Per IP (middleware): 100 requests/menit
   - DRF throttling: `anon: 100/day`, `user: 100/second`
   - Per user (AI): Ask 20/jam, Insights 10/jam

4. **Brute Force Protection**
   - Django Axes: limit &amp; cooldown diatur via `.env` (`AXES_FAILURE_LIMIT`, `AXES_COOLOFF_TIME`)

5. **CSRF Protection**
   - Django CSRF middleware
   - Token validation untuk forms

## 🤖 AI Models yang Tersedia

### Model Options
| Model | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| `fast` | ⚡⚡⚡ | ⭐⭐ | Quick answers, simple queries |
| `balanced` | ⚡⚡ | ⭐⭐⭐ | General purpose, good balance |
| `quality` | ⚡ | ⭐⭐⭐⭐ | Complex analysis, detailed insights |

### Token Efficiency Tips
- Batasi max_tokens (default: 300)
- Gunakan model `fast` untuk query sederhana
- Potong data besar sebelum kirim ke AI
- Gunakan caching untuk query berulang

## 🤝 Contributing

Contributions are welcome! Silakan submit Pull Request.

## 📄 License

Proyek ini menggunakan lisensi **MIT License** - lihat file [LICENSE](LICENSE) untuk detail.

## 🙏 Acknowledgments

- **Django** - Web framework untuk perfectionists
- **Google** - Gemini AI
- **Groq** - Fast AI inference platform
- **Meta** - Llama language models
- **Bootstrap** - CSS framework
- **All Open Source Contributors** - Terima kasih!

## 📞 Support

Jika Anda menemukan bug atau memiliki pertanyaan:
- Open an issue di GitHub: https://github.com/DevZkafnd/InventoryKedaiDepanRumah/issues

## 🎉 Updates

### Version 1.2.0 (Current)
- ✅ Konfigurasi aplikasi (Admin model): pagination (`records_per_page`), toggle upload &amp; email, maintenance mode
- ✅ Endpoint konfigurasi aplikasi: `/api/app_config/`
- ✅ Endpoint kontrol maintenance mode: `/api/set_edit_lock_status/` &amp; `/api/get_edit_lock_status/`
- ✅ Dokumentasi endpoint transfer (submit request + complete transfer)
- ✅ Update README agar sesuai implementasi terbaru (AI, security, pages)

### Version 1.1.0
- ✅ Update UI ke minimal Black/White/Green theme
- ✅ Custom logout view (redirect ke landing page)
- ✅ Add requests dependency ke startup scripts
- ✅ AI Assistant integration (Groq) + quota tracking
- ✅ Expiry date tracking
- ✅ Logo integration di semua halaman
- ✅ Responsive design untuk mobile
- ✅ Fix semua bug reported

### Version 1.0.0
- ✅ Landing page dengan modern UI
- ✅ AI Assistant integration dengan Groq
- ✅ Security middleware (anti-hacker)
- ✅ Token efficient AI system
- ✅ Simple queue system untuk rate limiting

---

**Made with ❤️ for Indonesian SMEs**
