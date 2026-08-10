# 🚀 Setup Database NeonTech - Panduan Lengkap

## ❌ Error yang Anda Alami

```
ModuleNotFoundError: No module named 'dj_database_url'
```

**Penyebab:** Dependencies belum diinstall lengkap di virtual environment lokal.

---

## ✅ SOLUSI TERCEPAT (Pilih Salah Satu)

### **🎯 OPSI 1: Script All-in-One (RECOMMENDED)**

Jalankan 1 command ini saja:

```bash
.\SETUP_LENGKAP.bat
```

Script ini akan otomatis:
- ✅ Install semua dependencies yang diperlukan
- ✅ Migrasi database ke NeonTech
- ✅ Membuat user admin, owner1, kasir1
- ✅ Seed data barang contoh
- ✅ Verifikasi hasil

**Waktu: ~5 menit**

---

### **🎯 OPSI 2: Step by Step Manual**

#### **STEP 1: Install Dependencies**

```bash
.\install_dependencies.bat
```

Atau manual:
```bash
.\.venv314\Scripts\activate.bat
pip install -r requirements.txt
```

#### **STEP 2: Setup Database**

```bash
.\setup_neontech_db.bat
```

---

## 🧪 Test Hasil Setup

### **1. Login di Web**

Buka: https://inventory-kedai-depan-rumah-iota.vercel.app/accounts/login/

Test 3 user ini:

| Username | Password  | Seharusnya Redirect Ke | Role            |
|----------|-----------|------------------------|-----------------|
| admin    | admin123  | ✅ /dashboard/         | Manager/Admin   |
| owner1   | owner123  | ✅ /dashboard/         | Owner (read)    |
| kasir1   | kasir123  | ✅ /shop/              | Kasir/Shop User |

### **2. Cek di Django Admin**

- URL: https://inventory-kedai-depan-rumah-iota.vercel.app/admin/
- Login: `admin` / `admin123`

Verifikasi:
- ✅ Users → admin → Groups ada "managers"
- ✅ Users → owner1 → Groups ada "owners"
- ✅ Users → kasir1 → Groups ada "cashiers" dan "shop_users"
- ✅ Items → Ada 25 items (MIE-001, BRS-001, dll)

### **3. Test Error 403 Sudah Hilang**

- ✅ Login dengan admin → Tidak ada error 403 lagi
- ✅ Redirect otomatis ke /dashboard/
- ✅ Bisa akses semua menu (Dashboard, Warehouse, Shop, dll)

---

## 🔧 Troubleshooting

### ❌ Error: "pip: command not found"

**Solusi:** Virtual environment belum aktif

```bash
.\.venv314\Scripts\activate.bat
```

Setelah aktif, prompt akan berubah jadi: `(.venv314) D:\projekan\...`

---

### ❌ Error: "could not connect to server"

**Penyebab:** Koneksi internet bermasalah atau DATABASE_URL salah

**Solusi:**
1. Cek koneksi internet
2. Verifikasi DATABASE_URL di `.env` atau script
3. Test ping ke NeonTech:
   ```bash
   ping ep-orange-wildflower-aztc4bgj.ap-southeast-1.aws.neon.tech
   ```

---

### ❌ Error: "relation already exists"

**Penyebab:** Tabel sudah dibuat sebelumnya

**Solusi:** Skip error ini, lanjut ke seed data:
```bash
python seed_data.py
```

---

### ❌ Error: "UNIQUE constraint failed"

**Penyebab:** User sudah ada di database

**Solusi:** Ini normal! Script akan update user yang sudah ada. Output akan menunjukkan:
```
[--] Superuser 'admin' sudah ada
[--] User 'owner1' sudah ada
```

---

### ❌ Masih 403 setelah setup?

**Solusi:**
1. **Logout dulu** dari aplikasi
2. **Clear cookies** browser (Ctrl+Shift+Del → Cookies)
3. **Login lagi** dengan username dan password yang benar

---

## 📦 Dependencies yang Diinstall

File `requirements.txt` berisi:

```
django==6.0.5                 # Framework utama
djangorestframework==3.17.1   # REST API
python-dotenv==1.2.1          # Load .env file
django-axes==8.3.1            # Login protection
django-anymail==15.0          # Email service
openpyxl==3.1.5               # Excel import/export
natsort==8.4.0                # Natural sorting
pytz==2026.2                  # Timezone
psycopg2-binary==2.9.10       # PostgreSQL driver ← PENTING!
dj-database-url==2.2.0        # Parse DATABASE_URL ← PENTING!
whitenoise==6.8.2             # Static files
gunicorn==23.0.0              # Production server
```

---

## 💾 Data yang Dibuat oleh Script

### **User & Grup**

| User   | Password  | Grup                      | Email             |
|--------|-----------|---------------------------|-------------------|
| admin  | admin123  | managers                  | admin@kedai.com   |
| owner1 | owner123  | owners                    | owner1@kedai.com  |
| kasir1 | kasir123  | cashiers, shop_users      | kasir1@kedai.com  |

### **Data Barang (25 items)**

- Mie Instan (3 jenis)
- Beras (2 jenis)
- Gula, Garam, Minyak Goreng
- Kopi & Teh
- Sabun & Sampo
- Rokok
- Air Mineral
- Snack & Biskuit
- Susu
- Kecap & Sambal
- dll

### **Stok Toko Kasir1 (10 items)**

Kasir1 sudah punya stok awal di toko:
- Mie Instan Goreng (20)
- Kopi Sachet (55)
- Air Mineral (20)
- Snack (22)
- dll

---

## 🎯 Checklist Setelah Setup

- [ ] Dependencies sudah terinstall (`pip list | findstr dj-database-url`)
- [ ] Migrasi database berhasil (tidak ada error)
- [ ] Seed data berhasil (user & items dibuat)
- [ ] Login admin berhasil → redirect ke /dashboard/
- [ ] Login owner1 berhasil → redirect ke /dashboard/
- [ ] Login kasir1 berhasil → redirect ke /shop/
- [ ] Tidak ada error 403 lagi
- [ ] Bisa akses menu sesuai role

---

## 📞 Butuh Bantuan?

Jika masih ada masalah, cek file dokumentasi lainnya:
- `PINDAH_KE_NEONTECH.md` - Penjelasan detail masalah
- `SOLUSI_SINGKAT.md` - Ringkasan solusi
- `FIX_LOGIN_ERROR_403.md` - Troubleshooting error 403

---

**🎉 Selamat! Database NeonTech Anda siap digunakan!**
