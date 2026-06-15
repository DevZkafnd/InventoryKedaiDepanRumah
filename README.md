# 🏪 Inventory Kedai Depan Rumah

Aplikasi web manajemen inventori untuk kedai/toko kecil. Dibangun dengan **Django** + **Django REST Framework**, tampilan berbasis Bootstrap 5.

---

## ✨ Fitur Utama

| Fitur | Keterangan |
|---|---|
| **Stok Gudang** | Kelola semua barang di gudang (tambah, edit, hapus) |
| **Stok Toko** | Pantau stok yang sudah ada di toko |
| **Transfer Barang** | Kasir bisa minta transfer barang dari gudang ke toko |
| **Persetujuan Transfer** | Manajer menyetujui dan mengirim barang ke toko |
| **Import/Export Excel** | Upload & download data stok dalam format `.xlsx` |
| **Mode Pemeliharaan** | Kunci gudang saat sedang diperbarui |
| **Multi Pengguna** | Role manajer dan kasir dengan hak akses berbeda |

---

## 🖥️ Persyaratan Sistem

- **Python** 3.10 atau lebih baru → [Download Python](https://python.org/downloads)
- **pip** (biasanya sudah termasuk bersama Python)
- Koneksi internet (untuk download dependencies pertama kali)
- Windows 10/11, Linux, atau macOS

---

## 🚀 Cara Menjalankan (Satu Perintah)

> 💡 **Tip:** Rename folder proyek dari `simple-stock-management-main` menjadi `inventory-kedai-depan-rumah` melalui File Explorer atau perintah berikut (tutup VS Code/editor dulu):
> ```
> rename "d:\projekan\simple-stock-management-main" "inventory-kedai-depan-rumah"
> ```

### Windows — Double-click atau jalankan di CMD:

```bat
jalankan.bat
```

### Windows — PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File jalankan.ps1
```

Script ini secara otomatis akan:
1. ✅ Cek Python & pip
2. ✅ Cek setiap library — install jika belum ada
3. ✅ Buat file `.env` jika belum ada
4. ✅ Jalankan migrasi database
5. ✅ Isi data contoh (jika database masih kosong)
6. ✅ Jalankan server di `http://127.0.0.1:8000/`

---

## 🔧 Setup Manual (Langkah per Langkah)

Jika ingin setup secara manual tanpa script otomatis:

### 1. Clone / Download Proyek

```bash
# Jika menggunakan git
git clone <url-repo>
cd inventory-kedai-depan-rumah

# Atau ekstrak ZIP ke folder pilihan Anda
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Buat File Konfigurasi `.env`

Salin dari template:

```bash
# Windows CMD
copy .env_default .env

# Windows PowerShell / Linux / macOS
cp .env_default .env
```

Lalu buka `.env` dan sesuaikan:

```env
DJANGO_SECRET_KEY='ganti-dengan-kunci-rahasia-yang-panjang-dan-acak'
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS='127.0.0.1,localhost'
DB_NAME='db.sqlite3'
AXES_FAILURE_LIMIT=5
AXES_COOLOFF_TIME=1
ALLOW_PW_CHANGE=True
```

> ⚠️ **Penting:** Ganti `DJANGO_SECRET_KEY` dengan string acak yang panjang sebelum digunakan di produksi.

### 4. Setup Database

```bash
python manage.py migrate
```

### 5. Isi Data Contoh

```bash
python seed_data.py
```

### 6. Jalankan Server

```bash
python manage.py runserver 8000
```

Buka browser dan akses: **http://127.0.0.1:8000/**

---

## 👤 Akun Default

Setelah menjalankan `seed_data.py`:

| Username | Password | Role | Akses |
|---|---|---|---|
| `admin` | `admin123` | Manajer | Kelola gudang, setujui transfer, import/export |
| `kasir1` | `kasir123` | Kasir/Toko | Lihat stok, minta transfer barang |

> 🔐 **Ganti password** setelah login pertama melalui menu **Ganti Kata Sandi**.

---

## 🌐 Halaman Aplikasi

| URL | Keterangan |
|---|---|
| `http://127.0.0.1:8000/` | Halaman utama dashboard inventori |
| `http://127.0.0.1:8000/accounts/login/` | Halaman login |
| `http://127.0.0.1:8000/admin/` | Panel administrasi Django |
| `http://127.0.0.1:8000/accounts/password_change/` | Ganti kata sandi |

---

## 📁 Struktur Proyek

```
inventory-kedai-depan-rumah/
├── 📄 jalankan.bat          ← Script setup & jalankan (Windows CMD)
├── 📄 jalankan.ps1          ← Script setup & jalankan (PowerShell)
├── 📄 seed_data.py          ← Script isi data contoh
├── 📄 requirements.txt      ← Daftar library Python
├── 📄 manage.py             ← Django management tool
├── 📄 .env                  ← Konfigurasi (dibuat dari .env_default)
├── 📄 .env_default          ← Template konfigurasi
│
├── 📁 ssm/                  ← Konfigurasi utama Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── 📁 stock_manager/        ← Aplikasi utama inventori
│   ├── models.py            ← Model: Item, ShopItem, TransferItem, Admin
│   ├── views.py             ← API views
│   ├── urls.py              ← URL routing
│   ├── serializers.py       ← DRF serializers
│   ├── admin.py             ← Konfigurasi admin panel
│   └── utils.py             ← Tools import/export Excel
│
├── 📁 email_service/        ← Layanan notifikasi email
│
├── 📁 templates/            ← Template HTML
│   ├── index.html           ← Halaman utama dashboard
│   └── registration/        ← Login, ganti password
│
└── 📁 static/               ← File statis (CSS, JS, gambar)
    └── img/logo.svg         ← Logo kedai
```

---

## 🔑 Panduan Penggunaan

### Sebagai Manajer (admin)

1. Login dengan akun `admin`
2. **Stok Gudang** — tambah barang baru, edit harga/stok, hapus barang
3. **Toggle pemeliharaan** — aktifkan saat sedang update massal (mencegah transfer)
4. **Transfer Menunggu** — klik **Kirim** untuk setujui permintaan transfer dari kasir
5. **Unduh/Unggah Data Stok** — export ke Excel atau import dari file `.xlsx`

### Sebagai Kasir (kasir1)

1. Login dengan akun `kasir1`
2. **Stok Gudang** — lihat barang tersedia, isi kolom **Jml Transfer** lalu tekan Enter
3. **Kirim Permintaan Transfer** — klik tombol untuk mengirim semua permintaan ke manajer
4. **Transfer Menunggu** — pantau status permintaan (abu-abu = sudah dikirim ke manajer)
5. **Stok Toko** — lihat barang yang sudah ada di toko Anda

---

## ⚙️ Konfigurasi Lanjutan

### Menambah Pengguna Baru

Melalui panel admin (`/admin/`):
1. Buka **Authentication → Users → Add User**
2. Isi username dan password
3. Di bagian **Groups**, tambahkan ke grup:
   - `managers` — untuk manajer gudang
   - `shop_users` — untuk kasir/pengguna toko
   - `receive_mail` — untuk menerima notifikasi email transfer

### Konfigurasi Aplikasi

Melalui panel admin → **App Configuration**:

| Opsi | Keterangan |
|---|---|
| Allow uploads | Izinkan import data dari Excel |
| Allow upload deletions | Hapus data yang tidak ada di file Excel saat import |
| Allow email notifications | Kirim email notifikasi saat ada transfer |
| Records per page | Jumlah baris per halaman tabel |

---

## 🛠️ Troubleshooting

**Port 8000 sudah dipakai:**
```bash
python manage.py runserver 8080
# Akses di http://127.0.0.1:8080/
```

**Error "No module named X":**
```bash
pip install -r requirements.txt
```

**Database error / tabel tidak ada:**
```bash
python manage.py migrate
```

**Lupa password admin:**
```bash
python manage.py changepassword admin
```

**Reset database (hapus semua data):**
```bash
# Hapus file database
del db.sqlite3          # Windows CMD
Remove-Item db.sqlite3  # PowerShell

# Buat ulang
python manage.py migrate
python seed_data.py
```

---

## 📦 Dependencies

| Library | Versi | Fungsi |
|---|---|---|
| Django | 6.0.5 | Framework web utama |
| djangorestframework | 3.17.1 | REST API |
| python-dotenv | 1.2.1 | Baca file .env |
| django-axes | 8.3.1 | Proteksi brute-force login |
| django-anymail | 15.0 | Layanan email transaksional |
| openpyxl | 3.1.5 | Baca/tulis file Excel |
| natsort | 8.4.0 | Pengurutan natural (SKU) |
| pytz | 2026.2 | Zona waktu |

---

*Inventory Kedai Depan Rumah v1.0 — Lisensi GPLv3*
