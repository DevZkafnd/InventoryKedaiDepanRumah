# 🔑 Cara Update DATABASE_URL NeonTech

## ❌ Masalah Saat Ini

```
psycopg.OperationalError: password authentication failed for user 'neondb_owner'
```

**Penyebab:** PASSWORD DATABASE sudah kedaluwarsa atau berubah!

---

## ✅ SOLUSI: Dapatkan DATABASE_URL Baru dari NeonTech

### **STEP 1: Login ke NeonTech**

1. Buka: https://neon.tech/
2. Login dengan akun Anda
3. Pilih project: **inventory-kedai-depan-rumah** (atau nama database Anda)

### **STEP 2: Copy DATABASE_URL yang Baru**

1. Klik tab **"Dashboard"** atau **"Connection Details"**
2. Cari bagian **"Connection string"**
3. Pilih **"Pooled connection"** atau **"Direct connection"**
4. Copy connection string yang muncul

Format connection string:
```
postgresql://[username]:[password]@[host]/[database]?sslmode=require
```

Contoh:
```
postgresql://neondb_owner:NEW_PASSWORD_HERE@ep-orange-wildflower-aztc4bgj.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
```

---

### **STEP 3: Update di Vercel**

1. Buka Vercel Dashboard: https://vercel.com/dashboard
2. Pilih project: **inventory-kedai-depan-rumah**
3. Klik **Settings** → **Environment Variables**
4. Cari variable **DATABASE_URL**
5. Klik **Edit** (ikon pensil)
6. **Paste** connection string baru yang sudah dicopy
7. Klik **Save**

### **STEP 4: Redeploy Vercel**

1. Masih di Vercel Dashboard
2. Klik tab **"Deployments"**
3. Klik tombol **"Redeploy"** (pojok kanan atas)
4. Pilih deployment terbaru
5. Klik **"Redeploy"**

---

### **STEP 5: Update di Lokal (untuk seed data)**

Update file `.env` atau script dengan DATABASE_URL yang baru:

**Opsi A: Update file `.env`**

Edit file `.env` dan uncomment baris DATABASE_URL:

```env
# Uncomment dan ganti dengan DATABASE_URL baru
DATABASE_URL=postgresql://neondb_owner:NEW_PASSWORD@ep-orange-wildflower-aztc4bgj.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
```

**Opsi B: Atau jalankan di terminal**

```powershell
$env:DATABASE_URL="postgresql://neondb_owner:NEW_PASSWORD@ep-orange-wildflower-aztc4bgj.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
python manage.py migrate
python seed_data.py
```

**Ganti `NEW_PASSWORD` dengan password yang sebenarnya dari NeonTech!**

---

## 🧪 Test Koneksi Database

Setelah update DATABASE_URL, test koneksi:

```powershell
# Aktifkan venv
.\.venv314\Scripts\activate.bat

# Set DATABASE_URL (ganti dengan yang baru!)
$env:DATABASE_URL="postgresql://YOUR_NEW_DATABASE_URL_HERE"

# Test koneksi
python manage.py dbshell --version
```

Jika berhasil, tidak ada error authentication.

---

## 📝 Checklist

- [ ] Login ke NeonTech Dashboard
- [ ] Copy DATABASE_URL baru (dengan password yang benar)
- [ ] Update di Vercel Environment Variables
- [ ] Redeploy Vercel
- [ ] Update di lokal (file `.env` atau terminal)
- [ ] Test koneksi database
- [ ] Jalankan migrate: `python manage.py migrate`
- [ ] Jalankan seed data: `python seed_data.py`
- [ ] Test login di web

---

## 💡 Tips

### **Jika Password NeonTech Tidak Terlihat:**

1. NeonTech hanya menampilkan password **1 kali** saat database dibuat
2. Jika lupa password, Anda bisa:
   - **Reset password** di NeonTech Dashboard
   - Atau **buat database baru** (database NeonTech gratis)

### **Cara Reset Password NeonTech:**

1. Login ke https://neon.tech/
2. Pilih project database Anda
3. Klik **Settings** → **Reset Password**
4. Copy password baru yang muncul
5. Update di Vercel dan lokal

### **Atau Buat Database Baru:**

Jika lebih mudah, buat database baru:

1. Login ke https://neon.tech/
2. Klik **"New Project"**
3. Beri nama: `inventory-kedai`
4. Region: **Singapore** (ap-southeast-1)
5. Copy DATABASE_URL yang muncul
6. Update di Vercel dan lokal

---

## 🚨 PENTING!

**JANGAN COMMIT DATABASE_URL KE GITHUB!**

File yang boleh berisi DATABASE_URL:
- ✅ `.env` (sudah di .gitignore)
- ✅ `.env.vercel` (sudah di .gitignore)
- ❌ JANGAN di `settings.py`
- ❌ JANGAN di file lain yang di-commit

---

## 🎯 Setelah Database URL Update

Jalankan script setup database:

```bash
.\SETUP_LENGKAP.bat
```

Atau manual:

```bash
# Aktifkan venv
.\.venv314\Scripts\activate.bat

# Set DATABASE_URL baru (dari NeonTech)
$env:DATABASE_URL="postgresql://YOUR_NEW_URL_HERE"

# Migrate
python manage.py migrate

# Seed data
python seed_data.py
```

---

**Setelah DATABASE_URL diupdate, error 403 akan hilang!** 🎉
