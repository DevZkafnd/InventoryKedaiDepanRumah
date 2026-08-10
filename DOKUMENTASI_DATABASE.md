# 📊 Dokumentasi Database - Inventory Kedai Depan Rumah

## Daftar Isi
- [Overview Database](#overview-database)
- [Struktur Tabel](#struktur-tabel)
- [Relasi Antar Tabel](#relasi-antar-tabel)
- [Penjelasan Detail Setiap Tabel](#penjelasan-detail-setiap-tabel)

---

## Overview Database

Sistem ini menggunakan **SQLite** sebagai database default (bisa diganti ke MySQL/PostgreSQL). Database menyimpan semua data inventory, user, transfer, dan konfigurasi aplikasi.

**Lokasi Database:** `db.sqlite3` (di root folder project)

**Total Tabel Utama:** 5 tabel
- `stock_manager_item` - Barang di gudang
- `stock_manager_shopitem` - Barang di toko (per kasir)
- `stock_manager_transferitem` - Permintaan transfer barang
- `stock_manager_wasteitem` - Pencatatan barang rusak/terbuang
- `stock_manager_admin` - Konfigurasi aplikasi

---

## Struktur Tabel

### 1. Tabel: `stock_manager_item` (Barang Gudang)

**Deskripsi:** Menyimpan semua barang yang ada di gudang

| Kolom | Tipe Data | Nullable | Default | Deskripsi |
|-------|-----------|----------|---------|-----------|
| `sku` | VARCHAR(100) | NO | - | **Primary Key** - Kode unik barang (Stock Keeping Unit) |
| `description` | VARCHAR(250) | NO | - | Nama/deskripsi barang |
| `purchase_price` | DECIMAL(10,2) | NO | - | Harga beli barang (2 desimal) |
| `quantity` | INTEGER | NO | 0 | Jumlah stok di gudang (min: 0) |
| `expiry_date` | DATE | YES | NULL | Tanggal kadaluarsa (opsional) |
| `last_updated` | DATETIME | NO | Auto | Waktu terakhir data diubah |
| `is_active` | BOOLEAN | NO | TRUE | Status aktif (soft delete flag) |

**Contoh Data:**
```
SKU: "INDOMIE-001"
Description: "Indomie Goreng Original"
Purchase Price: 2500.00
Quantity: 150
Expiry Date: 2027-12-31
Last Updated: 2026-07-24 10:30:00
Is Active: TRUE
```

**Index:**
- PRIMARY KEY pada `sku`

---

### 2. Tabel: `stock_manager_shopitem` (Barang Toko/Kasir)

**Deskripsi:** Menyimpan barang yang sudah ditransfer ke toko (per kasir/shop_user)

| Kolom | Tipe Data | Nullable | Default | Deskripsi |
|-------|-----------|----------|---------|-----------|
| `id` | INTEGER | NO | Auto | **Primary Key** - ID unik |
| `shop_user_id` | INTEGER | NO | - | **Foreign Key** ke `auth_user.id` |
| `item_id` | VARCHAR(100) | YES | NULL | **Foreign Key** ke `stock_manager_item.sku` |
| `quantity` | INTEGER | NO | 0 | Jumlah barang di toko kasir ini |
| `last_updated` | DATETIME | NO | Auto | Waktu terakhir data diubah |

**Constraints:**
- UNIQUE (`shop_user_id`, `item_id`) - Satu kasir hanya punya 1 record per barang
- ON DELETE CASCADE untuk `shop_user_id`
- ON DELETE SET NULL untuk `item_id` (jika barang dihapus)

**Contoh Data:**
```
ID: 1
Shop User ID: 5 (username: kasir1)
Item ID: "INDOMIE-001"
Quantity: 30
Last Updated: 2026-07-24 11:00:00
```

---

### 3. Tabel: `stock_manager_transferitem` (Transfer Barang)

**Deskripsi:** Menyimpan permintaan transfer barang dari gudang ke toko

| Kolom | Tipe Data | Nullable | Default | Deskripsi |
|-------|-----------|----------|---------|-----------|
| `id` | INTEGER | NO | Auto | **Primary Key** - ID unik |
| `shop_user_id` | INTEGER | NO | - | **Foreign Key** ke `auth_user.id` (kasir yang request) |
| `item_id` | VARCHAR(100) | NO | - | **Foreign Key** ke `stock_manager_item.sku` |
| `quantity` | INTEGER | NO | 0 | Jumlah barang yang diminta |
| `ordered` | BOOLEAN | NO | FALSE | Status: FALSE = draft, TRUE = sudah disubmit |
| `last_updated` | DATETIME | NO | Auto | Waktu terakhir data diubah |
| `created_at` | DATETIME | NO | Auto | Waktu request dibuat |

**Constraints:**
- ON DELETE CASCADE untuk kedua foreign key

**Contoh Data:**
```
ID: 10
Shop User ID: 5 (kasir1)
Item ID: "INDOMIE-001"
Quantity: 50
Ordered: TRUE (sudah disubmit, menunggu approve manajer)
Created At: 2026-07-24 09:00:00
Last Updated: 2026-07-24 09:15:00
```

**Alur Status `ordered`:**
1. Kasir tambah item ke draft transfer → `ordered = FALSE`
2. Kasir submit request → `ordered = TRUE` (email ke manajer jika aktif)
3. Manajer approve → Data dipindah ke `ShopItem`, record `TransferItem` dihapus
4. Manajer cancel → Record `TransferItem` dihapus

---

### 4. Tabel: `stock_manager_wasteitem` (Barang Rusak/Waste)

**Deskripsi:** Mencatat barang yang rusak, kadaluarsa, atau terbuang (di luar penjualan)

| Kolom | Tipe Data | Nullable | Default | Deskripsi |
|-------|-----------|----------|---------|-----------|
| `id` | INTEGER | NO | Auto | **Primary Key** - ID unik |
| `item_id` | VARCHAR(100) | NO | - | **Foreign Key** ke `stock_manager_item.sku` |
| `shop_user_id` | INTEGER | YES | NULL | **Foreign Key** ke `auth_user.id` (jika dari toko) |
| `source` | VARCHAR(20) | NO | 'warehouse' | Sumber: 'warehouse' atau 'shop' |
| `quantity` | INTEGER | NO | - | Jumlah barang yang rusak (min: 1) |
| `reason` | VARCHAR(255) | NO | - | Alasan: rusak, kadaluarsa, dll |
| `recorded_at` | DATE | NO | Today | Tanggal kejadian waste |
| `created_at` | DATETIME | NO | Auto | Waktu record dibuat |

**Constraints:**
- ON DELETE PROTECT untuk `item_id` (tidak bisa hapus item jika ada waste record)
- ON DELETE SET NULL untuk `shop_user_id`

**Contoh Data:**
```
ID: 1
Item ID: "INDOMIE-001"
Shop User ID: NULL (dari warehouse)
Source: "warehouse"
Quantity: 5
Reason: "Kemasan rusak saat bongkar"
Recorded At: 2026-07-23
Created At: 2026-07-24 08:00:00
```

---

### 5. Tabel: `stock_manager_admin` (Konfigurasi Aplikasi)

**Deskripsi:** Menyimpan konfigurasi global aplikasi (singleton - hanya 1 record dengan id=1)

| Kolom | Tipe Data | Nullable | Default | Deskripsi |
|-------|-----------|----------|---------|-----------|
| `id` | INTEGER | NO | 1 | **Primary Key** - Selalu 1 (singleton) |
| `edit_lock` | BOOLEAN | NO | FALSE | Maintenance mode (blok transfer kasir) |
| `allow_uploads` | BOOLEAN | NO | FALSE | Izinkan upload Excel |
| `allow_upload_deletions` | BOOLEAN | NO | FALSE | Hapus data tidak ada di Excel saat upload |
| `allow_email_notifications` | BOOLEAN | NO | FALSE | Aktifkan notifikasi email |
| `records_per_page` | INTEGER | NO | 25 | Jumlah data per halaman (pagination) |

**Contoh Data:**
```
ID: 1
Edit Lock: FALSE
Allow Uploads: TRUE
Allow Upload Deletions: FALSE
Allow Email Notifications: FALSE
Records Per Page: 25
```

**Cara Akses:**
```python
config = Admin.get_solo()  # Selalu return record dengan id=1
```

---

## Relasi Antar Tabel

### Diagram Relasi (ER Diagram)

```
┌─────────────────┐
│   auth_user     │  (Django built-in)
│                 │
│ - id (PK)       │
│ - username      │
│ - email         │
└────────┬────────┘
         │
         │ 1
         │
         │ Many
    ┌────┴─────────────────────────┐
    │                              │
    │                              │
    ▼                              ▼
┌───────────────────┐    ┌──────────────────────┐
│  ShopItem         │    │  TransferItem        │
│                   │    │                      │
│ - id (PK)         │    │ - id (PK)            │
│ - shop_user_id FK │    │ - shop_user_id FK    │
│ - item_id FK      │    │ - item_id FK         │
│ - quantity        │    │ - quantity           │
│ - last_updated    │    │ - ordered            │
└─────────┬─────────┘    └────────┬─────────────┘
          │                       │
          │                       │
          │                       │
          │ Many            Many  │
          │                       │
          └───────────┬───────────┘
                      │
                      │ 1
                      ▼
         ┌────────────────────────┐
         │  Item                  │
         │                        │
         │ - sku (PK)             │
         │ - description          │
         │ - purchase_price       │
         │ - quantity             │
         │ - expiry_date          │
         │ - is_active            │
         │ - last_updated         │
         └────────────┬───────────┘
                      │
                      │ 1
                      │
                      │ Many
                      ▼
         ┌────────────────────────┐
         │  WasteItem             │
         │                        │
         │ - id (PK)              │
         │ - item_id FK (PROTECT) │
         │ - shop_user_id FK      │
         │ - source               │
         │ - quantity             │
         │ - reason               │
         │ - recorded_at          │
         └────────────────────────┘


         ┌────────────────────────┐
         │  Admin (Singleton)     │
         │                        │
         │ - id (PK) = 1          │
         │ - edit_lock            │
         │ - allow_uploads        │
         │ - records_per_page     │
         └────────────────────────┘
```

### Penjelasan Relasi:

1. **User → ShopItem (One-to-Many)**
   - Satu kasir bisa punya banyak `ShopItem`
   - Jika user dihapus → semua `ShopItem` ikut terhapus (CASCADE)

2. **User → TransferItem (One-to-Many)**
   - Satu kasir bisa request banyak transfer
   - Jika user dihapus → semua `TransferItem` ikut terhapus (CASCADE)

3. **Item → ShopItem (One-to-Many)**
   - Satu item bisa ada di banyak toko (kasir berbeda)
   - Jika item dihapus → `item_id` di `ShopItem` jadi NULL (SET_NULL)

4. **Item → TransferItem (One-to-Many)**
   - Satu item bisa di-request oleh banyak kasir
   - Jika item dihapus → transfer terkait juga dihapus (CASCADE)

5. **Item → WasteItem (One-to-Many)**
   - Satu item bisa punya banyak waste record
   - Jika item akan dihapus → **DITOLAK** jika ada waste (PROTECT)

---

## Penjelasan Detail Setiap Tabel

### Tabel: Item

**Fungsi:** Menyimpan master data barang di gudang

**Field Penting:**
- `sku`: Harus unik, tidak boleh kosong. Ini adalah identitas barang
- `is_active`: Soft delete flag. Jika FALSE, barang "dihapus" tapi data masih ada
- `quantity`: Stok di gudang. Dikurangi saat transfer ke toko
- `purchase_price`: Harga beli (untuk laporan profit)
- `expiry_date`: Opsional, untuk track barang yang bisa kadaluarsa

**Query Contoh:**
```sql
-- Ambil semua barang aktif
SELECT * FROM stock_manager_item WHERE is_active = 1;

-- Barang dengan stok menipis (≤ 10)
SELECT sku, description, quantity 
FROM stock_manager_item 
WHERE is_active = 1 AND quantity <= 10 
ORDER BY quantity ASC;

-- Barang yang akan kadaluarsa dalam 30 hari
SELECT sku, description, expiry_date 
FROM stock_manager_item 
WHERE is_active = 1 
  AND expiry_date IS NOT NULL 
  AND expiry_date <= DATE('now', '+30 days')
ORDER BY expiry_date ASC;
```

---

### Tabel: ShopItem

**Fungsi:** Track stok barang per kasir/toko

**Logika Bisnis:**
1. Kasir request transfer (masuk ke `TransferItem`)
2. Manajer approve
3. Barang dipindah: `Item.quantity` berkurang, `ShopItem.quantity` bertambah
4. Satu kasir + satu barang = maksimal 1 record (karena UNIQUE constraint)

**Query Contoh:**
```sql
-- Stok barang kasir tertentu
SELECT 
    si.id,
    u.username AS kasir,
    i.sku,
    i.description,
    si.quantity
FROM stock_manager_shopitem si
JOIN auth_user u ON si.shop_user_id = u.id
JOIN stock_manager_item i ON si.item_id = i.sku
WHERE u.username = 'kasir1';

-- Total stok per barang (di semua toko)
SELECT 
    i.sku,
    i.description,
    SUM(si.quantity) AS total_di_toko
FROM stock_manager_item i
LEFT JOIN stock_manager_shopitem si ON i.sku = si.item_id
WHERE i.is_active = 1
GROUP BY i.sku, i.description;
```

---

### Tabel: TransferItem

**Fungsi:** Sistem antrian transfer barang

**Status Lifecycle:**
1. **Draft** (`ordered = FALSE`):
   - Kasir menambah item ke draft
   - Bisa diedit/hapus kapan saja
   - Belum mengirim email ke manajer

2. **Submitted** (`ordered = TRUE`):
   - Kasir submit request
   - Email notifikasi ke manajer (jika diaktifkan)
   - Tidak bisa edit lagi

3. **Approved** (record dihapus):
   - Manajer approve
   - Barang pindah ke `ShopItem`
   - Record `TransferItem` dihapus

4. **Cancelled** (record dihapus):
   - Manajer cancel
   - Record langsung dihapus

**Query Contoh:**
```sql
-- Transfer yang menunggu approval
SELECT 
    ti.id,
    u.username AS kasir,
    i.sku,
    i.description,
    ti.quantity,
    ti.created_at
FROM stock_manager_transferitem ti
JOIN auth_user u ON ti.shop_user_id = u.id
JOIN stock_manager_item i ON ti.item_id = i.sku
WHERE ti.ordered = 1
ORDER BY ti.created_at ASC;

-- Draft transfer kasir tertentu
SELECT 
    ti.id,
    i.sku,
    i.description,
    ti.quantity,
    i.quantity AS stok_gudang
FROM stock_manager_transferitem ti
JOIN stock_manager_item i ON ti.item_id = i.sku
JOIN auth_user u ON ti.shop_user_id = u.id
WHERE u.username = 'kasir1' AND ti.ordered = 0;
```

---

### Tabel: WasteItem

**Fungsi:** Melacak kerugian karena barang rusak/terbuang (bukan penjualan)

**Field `source`:**
- `'warehouse'`: Rusak di gudang (sebelum distribusi)
- `'shop'`: Rusak di toko

**Contoh Use Case:**
- Barang jatuh saat handling → rusak
- Kadaluarsa sebelum terjual
- Kemasan rusak
- Recall produk

**Bedakan dengan Penjualan:**
- **Penjualan**: Barang laku, stok berkurang → UNTUNG
- **Waste**: Barang rusak, stok berkurang → RUGI

**Query Contoh:**
```sql
-- Total waste per item (30 hari terakhir)
SELECT 
    i.sku,
    i.description,
    SUM(w.quantity) AS total_waste,
    COUNT(w.id) AS kejadian,
    GROUP_CONCAT(w.reason) AS alasan
FROM stock_manager_wasteitem w
JOIN stock_manager_item i ON w.item_id = i.sku
WHERE w.recorded_at >= DATE('now', '-30 days')
GROUP BY i.sku, i.description
ORDER BY total_waste DESC;

-- Waste dengan nilai kerugian
SELECT 
    i.sku,
    i.description,
    w.quantity,
    i.purchase_price,
    (w.quantity * i.purchase_price) AS kerugian,
    w.reason,
    w.recorded_at
FROM stock_manager_wasteitem w
JOIN stock_manager_item i ON w.item_id = i.sku
ORDER BY kerugian DESC;
```

---

### Tabel: Admin

**Fungsi:** Konfigurasi global aplikasi (singleton pattern)

**Cara Kerja Singleton:**
- Hanya boleh ada 1 record dengan `id = 1`
- Diakses via `Admin.get_solo()` di kode Python
- Jika belum ada, otomatis dibuat saat pertama kali diakses

**Field Penting:**
1. **edit_lock** (Maintenance Mode):
   - `TRUE` → Kasir tidak bisa transfer (maintenance)
   - `FALSE` → Normal, kasir bisa transfer

2. **allow_uploads**:
   - `TRUE` → Manajer bisa upload Excel
   - `FALSE` → Upload diblok

3. **allow_upload_deletions**:
   - `TRUE` → Saat upload Excel, data tidak ada di file akan dihapus
   - `FALSE` → Upload hanya update/tambah, tidak hapus

4. **allow_email_notifications**:
   - `TRUE` → Kirim email saat ada transfer request
   - `FALSE` → Tidak kirim email

5. **records_per_page**:
   - Jumlah data per halaman (pagination)
   - Default: 25
   - Min: 1

**Query Contoh:**
```sql
-- Cek status maintenance
SELECT edit_lock FROM stock_manager_admin WHERE id = 1;

-- Update konfigurasi
UPDATE stock_manager_admin 
SET allow_uploads = 1, records_per_page = 50 
WHERE id = 1;
```

---

## Query Berguna Lainnya

### 1. Dashboard Statistics

```sql
-- Total barang aktif
SELECT COUNT(*) AS total_items 
FROM stock_manager_item 
WHERE is_active = 1;

-- Stok tersedia (quantity > 10)
SELECT COUNT(*) AS in_stock 
FROM stock_manager_item 
WHERE is_active = 1 AND quantity > 10;

-- Stok menipis (1-10)
SELECT COUNT(*) AS low_stock 
FROM stock_manager_item 
WHERE is_active = 1 AND quantity > 0 AND quantity <= 10;

-- Stok habis (quantity = 0)
SELECT COUNT(*) AS out_of_stock 
FROM stock_manager_item 
WHERE is_active = 1 AND quantity = 0;
```

### 2. Laporan Stok Lengkap

```sql
-- Stok di gudang + toko + transfer pending
SELECT 
    i.sku,
    i.description,
    i.quantity AS stok_gudang,
    COALESCE(SUM(si.quantity), 0) AS stok_toko,
    COALESCE(SUM(CASE WHEN ti.ordered = 1 THEN ti.quantity ELSE 0 END), 0) AS transfer_pending,
    (i.quantity + COALESCE(SUM(si.quantity), 0)) AS total_stok
FROM stock_manager_item i
LEFT JOIN stock_manager_shopitem si ON i.sku = si.item_id
LEFT JOIN stock_manager_transferitem ti ON i.sku = ti.item_id
WHERE i.is_active = 1
GROUP BY i.sku, i.description, i.quantity
ORDER BY i.sku;
```

### 3. Audit Trail (Perubahan Data)

```sql
-- Barang yang baru diupdate (24 jam terakhir)
SELECT 
    sku, 
    description, 
    quantity, 
    last_updated 
FROM stock_manager_item 
WHERE last_updated >= DATETIME('now', '-1 day')
ORDER BY last_updated DESC;
```

### 4. Analisis Waste (Kerugian)

```sql
-- Total kerugian per bulan
SELECT 
    strftime('%Y-%m', w.recorded_at) AS bulan,
    SUM(w.quantity * i.purchase_price) AS total_kerugian
FROM stock_manager_wasteitem w
JOIN stock_manager_item i ON w.item_id = i.sku
GROUP BY bulan
ORDER BY bulan DESC;
```

---

## Backup dan Restore Database

### Backup Database (SQLite)

```bash
# Cara 1: Copy file langsung
copy db.sqlite3 backup_db_2026-07-24.sqlite3

# Cara 2: Export ke SQL
sqlite3 db.sqlite3 .dump > backup_db_2026-07-24.sql
```

### Restore Database

```bash
# Cara 1: Copy file backup
copy backup_db_2026-07-24.sqlite3 db.sqlite3

# Cara 2: Import dari SQL
sqlite3 db.sqlite3 < backup_db_2026-07-24.sql
```

---

## Migrasi Database

Django menggunakan sistem **migrations** untuk manage schema database.

### Membuat Migration Baru

```bash
# Setelah edit models.py
python manage.py makemigrations
```

### Apply Migration

```bash
python manage.py migrate
```

### Lihat Status Migration

```bash
python manage.py showmigrations
```

### Rollback Migration

```bash
# Rollback ke migration tertentu
python manage.py migrate stock_manager 0003_previous_migration
```

---

## Tips dan Best Practices

### 1. Soft Delete (is_active)

**Jangan** gunakan `DELETE` langsung untuk barang:
```sql
-- ❌ SALAH - data hilang permanen
DELETE FROM stock_manager_item WHERE sku = 'ABC-123';

-- ✅ BENAR - soft delete
UPDATE stock_manager_item SET is_active = 0 WHERE sku = 'ABC-123';
```

**Keuntungan Soft Delete:**
- Data history tetap ada
- Bisa restore jika salah hapus
- Relasi ke tabel lain tidak rusak

### 2. Transaction untuk Transfer

**Proses transfer harus atomic** (semua berhasil atau semua gagal):

```python
# Django ORM Transaction
from django.db import transaction

with transaction.atomic():
    # 1. Kurangi stok gudang
    item.quantity -= transfer_quantity
    item.save()
    
    # 2. Tambah stok toko
    shop_item.quantity += transfer_quantity
    shop_item.save()
    
    # 3. Hapus transfer request
    transfer_item.delete()
```

### 3. Index untuk Performa

**Field yang sering di-query harus punya index:**
- `sku` (sudah ada - PRIMARY KEY)
- `is_active` (untuk filter barang aktif)
- `shop_user_id`, `item_id` di ShopItem (sudah ada - FOREIGN KEY)

### 4. Validasi Data

**Validasi di Level Model (models.py):**
- `quantity >= 0` → MinValueValidator
- `purchase_price` → Decimal dengan 2 desimal
- `sku` → Unique, required

**Validasi di Level Serializer (serializers.py):**
- Regex untuk format data
- Custom validation logic

---

**📝 Catatan Akhir:**

Database ini dirancang untuk:
- ✅ Sederhana dan mudah dipahami
- ✅ Mendukung multi-user dengan role berbeda
- ✅ Audit trail lengkap (timestamp)
- ✅ Data integrity dengan foreign key constraints
- ✅ Soft delete untuk data safety

---

**👨‍💻 Butuh Bantuan?**

Jika ada pertanyaan tentang database, silakan buka issue di GitHub atau hubungi tim developer.

**Terakhir Diupdate:** 24 Juli 2026
