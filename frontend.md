# Frontend Inventory Kedai Depan Rumah

Dokumentasi ini menjelaskan tentang teknologi dan implementasi frontend yang digunakan dalam proyek Inventory Kedai Depan Rumah.

---

## 📦 Teknologi Frontend yang Digunakan

Berikut adalah daftar teknologi frontend utama dalam proyek ini:

### 1. **Django Templates**
- Digunakan sebagai template engine untuk merender halaman HTML secara server-side.
- File template utama: `templates/index.html`
- Fitur:
  - Menggunakan tag `{% load static %}` untuk memuat file statis.
  - Mendukung variabel dan tag Django.

### 2. **Bootstrap 5.3.8**
- Framework CSS untuk styling responsif dan komponen UI.
- Diimpor dari CDN: `https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css`
- Komponen Bootstrap yang digunakan:
  - Container
  - Buttons
  - Forms
  - Tables
  - Pagination
  - Badges

### 3. **Bootstrap Icons 1.11.3**
- Library ikon open-source dari Bootstrap.
- Diimpor dari CDN: `https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css`
- Ikon yang sering dipakai:
  - `bi-building` (untuk Stok Gudang)
  - `bi-shop` (untuk Stok Toko)
  - `bi-search` (untuk pencarian)
  - `bi-plus` (untuk tambah barang)
  - `bi-trash3` (untuk hapus barang)
  - `bi-exclamation-triangle` (untuk notifikasi kadaluarsa)

### 4. **jQuery 3.7.1**
- Library JavaScript untuk manipulasi DOM dan AJAX.
- Diimpor dari CDN: `https://code.jquery.com/jquery-3.7.1.min.js`
- Kegunaan utama:
  - Melakukan request AJAX ke API backend.
  - Memanipulasi elemen HTML secara dinamis.
  - Menangani event klik dan perubahan.

### 5. **Google Fonts (Inter)**
- Font family utama yang digunakan.
- Diimpor dari CDN: `https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap`
- Berat font yang dipakai: 300 (Light), 400 (Regular), 500 (Medium), 600 (SemiBold), 700 (Bold).

---

## 🎨 Desain UI/UX

Proyek ini menggunakan desain modern dengan warna-warna yang nyaman:

### Warna Utama
- **Primary**: `#1a6b3c` (hijau tua)
- **Primary Dark**: `#0f4526`
- **Accent**: `#f5a623` (kuning oranye)
- **Danger**: `#dc3545` (merah)

### Komponen Utama UI

#### 1. **Topbar**
- Navbar tetap di atas dengan warna hijau primary.
- Menampilkan logo, judul aplikasi, dan informasi user.

#### 2. **Section Card**
- Kotak konten dengan shadow dan border-radius.
- Digunakan untuk menampilkan setiap bagian (Stok Gudang, Stok Toko).

#### 3. **Search Bar**
- Input pencarian dengan ikon search.
- Digunakan untuk mencari barang di setiap tabel.

#### 4. **Table**
- Tabel untuk menampilkan daftar barang.
- Fitur:
  - Sorting (urutkan kolom).
  - Pagination (halaman).
  - Editable field (untuk manager).

#### 5. **Expiry Notification**
- Notifikasi untuk barang yang mendekati kadaluarsa (≤ 48 jam) atau sudah kadaluarsa (≤ 24 jam).
- Warna background: `#fee2e2` (merah muda).
- Border: `#dc3545` (merah).

---

## 📝 Fitur Frontend Utama

Berikut adalah fitur-fitur frontend yang ada di proyek ini:

### 1. **Manajemen Stok Gudang**
- Tampilkan daftar barang di gudang.
- Tambah barang baru (dengan tanggal kadaluarsa).
- Edit barang (harga beli, stok, deskripsi, tanggal kadaluarsa).
- Hapus barang.
- Cari barang.
- Urutkan barang berdasarkan kolom.
- Lihat notifikasi barang mendekati kadaluarsa.
- Ekspor data stok ke Excel.
- Impor data stok dari Excel.

### 2. **Manajemen Stok Toko**
- Tampilkan daftar barang di toko.
- Cari barang.
- Urutkan barang berdasarkan kolom.

### 3. **Interaksi dengan Backend**
Semua interaksi dengan backend dilakukan melalui **API REST** menggunakan jQuery AJAX:
- `GET /api/items/` → Ambil daftar barang gudang.
- `POST /api/items/` → Tambah barang baru.
- `PUT /api/items/{sku}/` → Edit barang.
- `DELETE /api/items/{sku}/` → Hapus barang.
- `GET /api/shop_items/` → Ambil daftar barang toko.
- `GET /api/export_data/` → Ekspor data ke Excel.
- `POST /api/import_data/` → Impor data dari Excel.

---

## 📂 Struktur File Frontend

```
inventory-kedai-depan-rumah/
├── templates/
│   ├── index.html          # Halaman utama aplikasi
│   └── registration/       # Halaman login & ganti password
│       ├── login.html
│       └── password_change_form.html
└── static/
    ├── admin/              # File statis untuk Django Admin
    ├── rest_framework/     # File statis untuk Django REST Framework
    └── img/
        └── logo.webp       # Logo aplikasi
```

---

## 🚀 Cara Menjalankan Frontend

Frontend dijalankan bersama dengan backend Django. Berikut langkahnya:

1. Pastikan Anda berada di direktori proyek.
2. Jalankan server Django:
   ```bash
   python manage.py runserver
   ```
3. Buka browser dan akses `http://127.0.0.1:8000/`.

---

## 📌 Catatan Penting

- Semua file CSS dan JavaScript diimpor dari **CDN** untuk kecepatan akses dan kemudahan maintenance.
- Frontend dirancang **responsif**, bisa diakses dari desktop atau mobile.
- Warna dan styling diatur menggunakan **CSS custom properties (variables)** untuk kemudahan perubahan tema.

Selamat menggunakan proyek Inventory Kedai Depan Rumah! 🎉
