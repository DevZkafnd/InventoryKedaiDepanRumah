# 🔄 Panduan Pindah dari SQLite ke NeonTech PostgreSQL

## 📋 Masalah yang Terjadi

Saat Anda deploy ke Vercel dengan database NeonTech PostgreSQL, database baru tersebut **masih kosong**. Data dari SQLite lokal (db.sqlite3) **TIDAK otomatis pindah** ke PostgreSQL.

### Yang Hilang di Database NeonTech:
- ❌ User (admin, owner1, kasir1)
- ❌ Grup (managers, owners, cashiers, shop_users)
- ❌ Data barang (Item)
- ❌ Konfigurasi aplikasi (Admin model)

### Kenapa Ini Terjadi?

SQLite dan PostgreSQL adalah **database yang berbeda**. Django tidak otomatis mengopi data antar database. Yang otomatis berjalan di Vercel hanya:

1. ✅ Migrasi struktur tabel (schema) via `python manage.py migrate`
2. ❌ Seed data TIDAK otomatis - harus dijalankan manual!

---

## ✅ Solusi: Setup Database NeonTech dari Lokal

### **LANGKAH 1: Jalankan Setup Database**

```bash
setup_neontech_db.bat
```

Script ini akan:
1. ✅ Migrasi struktur database ke NeonTech
2. ✅ Membuat semua grup: owners, managers, cashiers, shop_users
3. ✅ Membuat user dengan password yang sama seperti SQLite lokal:
   - `admin` (password: admin123) → Grup: managers
   - `owner1` (password: owner123) → Grup: owners
   - `kasir1` (password: kasir123) → Grup: cashiers + shop_users
4. ✅ Mengisi 25 data barang contoh (mie, beras, kopi, dll)
5. ✅ Mengisi stok toko untuk kasir1

### **LANGKAH 2: Verifikasi di Web**

Buka browser dan login:
- **URL:** https://inventory-kedai-depan-rumah-iota.vercel.app/accounts/login/

**Test login semua user:**

| Username | Password  | Seharusnya Redirect Ke | Role           |
|----------|-----------|------------------------|----------------|
| admin    | admin123  | /dashboard/            | Manager/Admin  |
| owner1   | owner123  | /dashboard/            | Owner (read)   |
| kasir1   | kasir123  | /shop/                 | Kasir/Shop     |

### **LANGKAH 3: Verifikasi di Django Admin**

- **URL:** https://inventory-kedai-depan-rumah-iota.vercel.app/admin/
- **Login:** admin / admin123

Cek:
- Users → admin → Groups = "managers" ✅
- Users → owner1 → Groups = "owners" ✅
- Users → kasir1 → Groups = "cashiers", "shop_users" ✅
- Items → Harus ada 25 item ✅

---

## 🔍 Troubleshooting

### ❌ Masih Error 403 setelah setup?

**Penyebab:** Session lama masih cache di browser

**Solusi:**
1. Logout dulu dari aplikasi
2. Clear cookies/cache browser
3. Login lagi

### ❌ Error "relation does not exist" saat seed data?

**Penyebab:** Tabel belum di-migrate

**Solusi:**
```bash
# Set DATABASE_URL di terminal
set DATABASE_URL=postgresql://neondb_owner:npg_j8ThFKgdmpw7@ep-orange-wildflower-aztc4bgj.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

# Migrate dulu
python manage.py migrate

# Baru seed data
python seed_data.py
```

### ❌ User sudah ada, tapi grup masih kosong?

**Solusi:** Jalankan script fix:
```bash
run_fix_admin_neon.bat
```

Script ini hanya menambahkan user ke grup tanpa membuat user baru.

---

## 🎯 Perbedaan SQLite vs PostgreSQL

| Aspek             | SQLite (Lokal)          | PostgreSQL (NeonTech)      |
|-------------------|-------------------------|----------------------------|
| File Database     | `db.sqlite3`            | Remote server di cloud     |
| Lokasi            | Folder project lokal    | NeonTech cloud (Singapore) |
| Akses             | Hanya lokal development | Dari mana saja (internet)  |
| Deploy Vercel     | ❌ Tidak disupport      | ✅ Recommended             |
| Data              | Tetap ada setelah seed  | Tetap ada (persistent)     |
| Performance       | Cepat untuk testing     | Optimized untuk production |

---

## 📊 Struktur Role & Akses

### **Role: managers (admin)**
- ✅ Dashboard (analytics)
- ✅ Warehouse (manage semua item)
- ✅ Shop (lihat stok toko semua kasir)
- ✅ Transfer (approve transfer request)
- ✅ Reports (import/export Excel)
- ✅ Waste (catat barang rusak)

### **Role: owners (owner1)**
- ✅ Dashboard (read-only, lihat analytics)
- ✅ Reports (lihat laporan, tidak bisa import)
- ✅ Waste (lihat waste, tidak bisa create)
- ✅ AI Assistant (analytics dengan AI)
- ❌ Warehouse (tidak bisa akses)
- ❌ Shop (tidak bisa akses)

### **Role: cashiers/shop_users (kasir1)**
- ✅ Shop (manage stok toko sendiri)
- ✅ Transfer (request barang dari warehouse)
- ❌ Dashboard (tidak bisa akses)
- ❌ Warehouse (tidak bisa akses)
- ❌ Reports (tidak bisa akses)

---

## 💡 Tips Penting

### 1. **Untuk Development Lokal: Gunakan SQLite**

Edit `.env`:
```env
# Comment DATABASE_URL untuk pakai SQLite
# DATABASE_URL=postgresql://...

DB_NAME=db.sqlite3
```

### 2. **Untuk Testing Production: Gunakan NeonTech**

Edit `.env`:
```env
# Uncomment untuk connect ke NeonTech
DATABASE_URL=postgresql://neondb_owner:npg_j8ThFKgdmpw7@ep-orange-wildflower-aztc4bgj.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
```

### 3. **Jangan Lupa Seed Data Setelah Setup Database Baru**

Setiap kali Anda:
- 🆕 Buat database baru
- 🗑️ Drop/reset database
- 🔄 Pindah database

Wajib jalankan:
```bash
python manage.py migrate
python seed_data.py
```

### 4. **Backup Data Production**

Untuk backup data NeonTech ke lokal:
```bash
# Export dari NeonTech
python manage.py dumpdata > backup_neontech.json

# Import ke SQLite lokal
python manage.py loaddata backup_neontech.json
```

---

## 📝 File Bantuan

- ✅ `setup_neontech_db.bat` - Setup lengkap database NeonTech
- ✅ `run_fix_admin_neon.bat` - Fix user admin jika grup hilang
- ✅ `seed_data.py` - Script seed data (user + items)
- ✅ `fix_admin_groups.py` - Script perbaiki grup user

---

## 🚀 Checklist Deploy Production

- [ ] Setup database NeonTech via `setup_neontech_db.bat`
- [ ] Verifikasi user admin, owner1, kasir1 bisa login
- [ ] Test semua role redirect ke halaman yang benar
- [ ] Ganti password default (admin123, owner123, kasir123)
- [ ] Test create/edit item di warehouse
- [ ] Test transfer request dari kasir
- [ ] Test approve transfer dari manager
- [ ] Verifikasi data tidak hilang setelah redeploy Vercel

---

**🎉 Database NeonTech Anda siap digunakan!**
