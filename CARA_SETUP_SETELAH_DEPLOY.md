# 🚀 Cara Setup Database Setelah Deploy ke Vercel

## ✅ Push ke GitHub Sudah Selesai!

Code sudah dipush dan Vercel akan otomatis redeploy dalam ~2-3 menit.

---

## 📋 Yang Berubah di Deployment Ini:

1. ✅ **psycopg2-binary** → **psycopg[binary]** (support Python 3.14)
2. ✅ Lisensi GPLv3 dihapus → MIT License
3. ✅ Footer login tidak ada "Lisensi GPLv3" lagi
4. ✅ Script setup database lengkap

---

## 🎯 Langkah Setelah Vercel Deploy Selesai

### **STEP 1: Tunggu Deploy Selesai**

1. Buka Vercel Dashboard: https://vercel.com/dashboard
2. Pilih project: `inventory-kedai-depan-rumah`
3. Tunggu sampai status **"Ready"** (biasanya 2-3 menit)
4. Cek logs untuk memastikan tidak ada error

### **STEP 2: Setup Database dari Lokal**

Setelah deployment selesai, jalankan script ini untuk seed data ke NeonTech:

```bash
.\SETUP_LENGKAP.bat
```

**PENTING:** Pastikan requirements.txt sudah update di Vercel. Jika masih ada error, coba option kedua:

```bash
# Install dependencies dulu (skip psycopg2-binary yang error)
pip install django djangorestframework python-dotenv django-axes django-anymail openpyxl natsort pytz requests dj-database-url whitenoise gunicorn

# Install psycopg3 (versi baru yang support Python 3.14)
pip install "psycopg[binary]"

# Baru setup database
.\setup_neontech_db.bat
```

### **STEP 3: Verifikasi di Web**

Buka browser dan test login:

**URL:** https://inventory-kedai-depan-rumah-iota.vercel.app/accounts/login/

| Username | Password  | Seharusnya Redirect |
|----------|-----------|---------------------|
| admin    | admin123  | ✅ /dashboard/      |
| owner1   | owner123  | ✅ /dashboard/      |
| kasir1   | kasir123  | ✅ /shop/           |

**Jika masih error 403:**
- Clear cookies browser
- Logout dan login lagi

---

## 🔍 Cek Vercel Logs

Jika masih ada masalah, cek logs di Vercel:

1. Buka: https://vercel.com/devzkafnds-projects/inventory-kedai-depan-rumah
2. Klik tab **"Deployments"**
3. Klik deployment terbaru
4. Klik tab **"Logs"** atau **"Build Logs"**

**Yang harus dicek:**
- ✅ Build berhasil (no error)
- ✅ `requirements.txt` install semua packages
- ✅ `python manage.py migrate` berhasil
- ✅ Tidak ada error `ModuleNotFoundError`

---

## 🛠️ Troubleshooting

### ❌ Build Error: "psycopg2-binary failed to build"

**Solusi:** requirements.txt sudah diupdate ke `psycopg[binary]==3.2.3`. 

Jika Vercel masih pakai cache lama:
1. Buka Vercel Dashboard → Project Settings
2. Klik **"Redeploy"**
3. Centang **"Clear Build Cache"**
4. Klik **"Redeploy"**

### ❌ Runtime Error: "ModuleNotFoundError: No module named 'psycopg2'"

**Penyebab:** Django masih cari `psycopg2` tapi kita pakai `psycopg`

**Solusi:** Tidak perlu ubah apa-apa! Django 4.2+ otomatis support `psycopg` (psycopg3). Cek `settings.py`:

```python
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}
```

`dj_database_url` akan otomatis detect `psycopg` jika tersedia.

### ❌ Error 403 setelah login

**Solusi:** Database masih kosong! Jalankan seed data:

```bash
.\SETUP_LENGKAP.bat
```

---

## 📦 Perubahan di requirements.txt

**Sebelum:**
```
psycopg2-binary==2.9.10  # ❌ Tidak support Python 3.14
```

**Sesudah:**
```
psycopg[binary]==3.2.3  # ✅ Support Python 3.14+
```

**Keunggulan psycopg3:**
- ✅ Support Python 3.14
- ✅ Lebih cepat dan modern
- ✅ Full compatible dengan Django 4.2+
- ✅ Binary package tersedia (tidak perlu compile)

---

## ✅ Checklist Deploy

- [x] Push code ke GitHub
- [x] Vercel otomatis trigger redeploy
- [ ] Deployment selesai (status: Ready)
- [ ] Build logs tidak ada error
- [ ] Jalankan `.\SETUP_LENGKAP.bat` untuk seed data
- [ ] Test login 3 user (admin, owner1, kasir1)
- [ ] Tidak ada error 403 lagi

---

## 🎉 Selesai!

Setelah deployment dan seed data selesai, aplikasi Anda siap digunakan!

**URL Production:** https://inventory-kedai-depan-rumah-iota.vercel.app/
