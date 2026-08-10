# ⚡ SOLUSI CEPAT - Error 403 & Role Berantakan

## 🎯 Masalah Anda

1. ❌ **Error 403** saat login dengan username `admin` di Vercel
2. ❌ **Role berantakan** - user admin, owner1, kasir1 tidak ada di NeonTech
3. ❌ **ModuleNotFoundError: No module named 'dj_database_url'**

## 💡 Penyebab

1. **Data SQLite lokal TIDAK otomatis pindah ke PostgreSQL NeonTech!**
2. **Dependencies belum diinstall lengkap** di virtual environment lokal

---

## ✅ SOLUSI (5 MENIT)

### **STEP 1: Install Dependencies Dulu**

```bash
.\install_dependencies.bat
```

Ini akan install semua package yang diperlukan termasuk:
- `dj-database-url` - Untuk parsing DATABASE_URL
- `psycopg2-binary` - Driver PostgreSQL
- Dan semua dependencies lainnya

### **STEP 2: Setup Database NeonTech**

```bash
.\setup_neontech_db.bat
```

**Apa yang dilakukan:**
1. Install dependencies tambahan (jika ada yang kurang)
2. Migrasi struktur database ke NeonTech
3. Membuat semua grup (owners, managers, cashiers, shop_users)
4. Membuat user:
   - `admin` (password: admin123) → Role: Manager
   - `owner1` (password: owner123) → Role: Owner
   - `kasir1` (password: kasir123) → Role: Kasir
5. Mengisi 25 data barang contoh

### **STEP 3: Test Login!**

Login di: https://inventory-kedai-depan-rumah-iota.vercel.app/accounts/login/

| Username | Password  | Akan Redirect Ke |
|----------|-----------|------------------|
| admin    | admin123  | /dashboard/      |
| owner1   | owner123  | /dashboard/      |
| kasir1   | kasir123  | /shop/           |

---

## 🎉 Bonus: Lisensi GPLv3 Sudah Dihapus!

✅ File `LICENSE` diganti ke MIT License
✅ Footer login tidak ada teks "Lisensi GPLv3" lagi
✅ File `email_service/email.py` sudah dihapus referensi GPL

---

## 🔧 Jika Ada Error "ModuleNotFoundError"

Jika muncul error:
```
ModuleNotFoundError: No module named 'dj_database_url'
```

**Solusi:** Install dependencies dulu
```bash
.\install_dependencies.bat
```

Atau pakai script all-in-one:
```bash
.\SETUP_LENGKAP.bat
```

Script ini akan otomatis install dependencies sebelum setup database.

---

## 📚 Dokumentasi Lengkap

- `README_SETUP.md` - **BACA INI DULU!** Panduan lengkap + troubleshooting
- `PINDAH_KE_NEONTECH.md` - Penjelasan lengkap masalah & solusi
- `FIX_LOGIN_ERROR_403.md` - Troubleshooting error 403

---

**Selesai! Database NeonTech Anda siap digunakan! 🚀**
