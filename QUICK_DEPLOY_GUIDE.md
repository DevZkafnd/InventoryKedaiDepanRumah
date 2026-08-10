# ⚡ Panduan Cepat Deploy ke Vercel

## ✅ Yang Sudah Selesai:
- ✅ File konfigurasi Vercel sudah dibuat
- ✅ Requirements.txt sudah diupdate dengan PostgreSQL
- ✅ Settings.py sudah dikonfigurasi untuk production
- ✅ Code sudah di-push ke GitHub

**GitHub Repo**: https://github.com/DevZkafnd/InventoryKedaiDepanRumah.git

---

## 🎯 Yang Harus Kamu Lakukan:

### 📝 STEP 1: Setup Database PostgreSQL (5 menit)

1. **Buka**: https://neon.tech
2. **Sign Up** pakai GitHub/Google
3. **Create Project**:
   - Name: `inventory-kedai`
   - Region: **Singapore**
4. **Copy Connection String** (akan muncul seperti ini):
   ```
   postgresql://username:password@ep-xxx.neon.tech/neondb?sslmode=require
   ```
5. **SIMPAN** connection string ini! ⚠️

---

### 🚀 STEP 2: Deploy ke Vercel (5 menit)

1. **Buka**: https://vercel.com
2. **Sign Up** pakai GitHub
3. **Import Project**:
   - Pilih repo: `InventoryKedaiDepanRumah`
   - Klik **Import**

4. **Configure**:
   - Framework: **Other**
   - Build Command: `chmod +x build_files.sh && ./build_files.sh`
   - Output Directory: `staticfiles`

5. **Environment Variables** - Tambahkan ini satu per satu:

```
DJANGO_SECRET_KEY = (generate baru - lihat cara di bawah)
DJANGO_DEBUG = False
DJANGO_ALLOWED_HOSTS = .vercel.app
DATABASE_URL = (paste connection string dari Neon)
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 30
ALLOW_PW_CHANGE = True
AI_PROVIDER = gemini
GEMINI_API_KEY = (api key kamu)
```

**💡 Generate Django Secret Key:**
Buka Python di terminal:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

6. **Klik Deploy** dan tunggu 3-5 menit ☕

---

### 👤 STEP 3: Buat Superuser (2 menit)

Setelah deploy selesai:

**Option A - Via Local Computer:**
```bash
set DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require
python manage.py createsuperuser
```

**Option B - Via Neon SQL Editor:**
1. Buka Neon Dashboard → SQL Editor
2. Paste & run:
```sql
-- Lihat semua users
SELECT * FROM auth_user;
```

Atau buat script Python sederhana untuk create superuser.

---

### ✅ STEP 4: Test Website

1. Buka URL Vercel kamu (contoh: `https://inventory-kedai.vercel.app`)
2. Klik **Login** atau buka `/admin`
3. Login dengan superuser
4. Test CRUD operations

---

## 🐛 Troubleshooting

### ❌ "DisallowedHost at /"
**Solusi**: Tambahkan domain Vercel ke environment variable:
```
DJANGO_ALLOWED_HOSTS = .vercel.app,your-app-name.vercel.app
```
Lalu **Redeploy**.

### ❌ "Database connection error"
**Solusi**: 
1. Pastikan `DATABASE_URL` benar
2. Harus ada `?sslmode=require` di akhir
3. Test connection di lokal dulu

### ❌ "Static files not loading"
**Solusi**: Redeploy project dari Vercel dashboard

### ❌ "No module named psycopg2"
**Solusi**: Sudah fix, tapi kalau masih error:
- Cek `requirements.txt` ada `psycopg2-binary==2.9.10`
- Redeploy

---

## 🔄 Update Code di Future

Setelah aplikasi live, untuk update:

```bash
# Edit code
git add .
git commit -m "Update feature X"
git push origin master

# Vercel otomatis deploy ulang! 🎉
```

---

## 📚 Dokumentasi Lengkap

Baca: **`DEPLOY_VERCEL.md`** untuk panduan detail step-by-step dengan screenshot dan penjelasan lengkap.

---

## 💰 Biaya

- **Neon**: ✅ Gratis selamanya (512 MB database)
- **Vercel**: ✅ Gratis selamanya (100 GB bandwidth/bulan)

Untuk inventory app kecil-menengah, **100% GRATIS!** 🎉

---

## 📞 Butuh Bantuan?

Kalau ada error, screenshot dan kirim:
1. Error message lengkap
2. URL Vercel kamu
3. Kapan error terjadi (saat build/runtime)

Good luck! 🚀
