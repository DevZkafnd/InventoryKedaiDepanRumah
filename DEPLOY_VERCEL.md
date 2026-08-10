# 🚀 Panduan Deploy ke Vercel + PostgreSQL

## 📋 Checklist Persiapan

✅ File yang sudah disiapkan:
- `vercel.json` - Konfigurasi Vercel
- `build_files.sh` - Script build otomatis
- `requirements.txt` - Updated dengan PostgreSQL support
- `settings.py` - Updated untuk production
- `.vercelignore` - File yang tidak di-upload ke Vercel

---

## 🗄️ LANGKAH 1: Setup Database PostgreSQL (Neon)

### 1.1 Buat Akun Neon
1. Buka: **https://neon.tech**
2. Klik **"Sign Up"** (bisa pakai GitHub/Google)
3. Login dan buat project baru

### 1.2 Buat Database
1. Klik **"Create Project"**
2. Isi detail:
   - **Project Name**: `inventory-kedai`
   - **Region**: Pilih **Singapore** (terdekat ke Indonesia)
   - **PostgreSQL Version**: `16` (latest)
3. Klik **"Create Project"**

### 1.3 Copy Connection String
Setelah database dibuat, akan muncul **Connection String**:

```
postgresql://username:password@ep-xxx-xxx.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
```

**⚠️ SIMPAN connection string ini!** Akan dipakai di Vercel nanti.

---

## 🐙 LANGKAH 2: Push ke GitHub

### 2.1 Cek Git Status
Buka terminal di folder project, jalankan:

```bash
git status
```

### 2.2 Add & Commit Files
```bash
git add .
git commit -m "Prepare for Vercel deployment with PostgreSQL support"
```

### 2.3 Setup Remote (jika belum)
```bash
git remote add origin https://github.com/DevZkafnd/InventoryKedaiDepanRumah.git
```

### 2.4 Push ke GitHub
```bash
git branch -M main
git push -u origin main
```

**✅ Jika berhasil**, buka GitHub dan pastikan semua file sudah terupload.

---

## ☁️ LANGKAH 3: Deploy ke Vercel

### 3.1 Buat Akun Vercel
1. Buka: **https://vercel.com**
2. Klik **"Sign Up"**
3. Pilih **"Continue with GitHub"**
4. Authorize Vercel untuk akses GitHub

### 3.2 Import Project
1. Di dashboard Vercel, klik **"Add New Project"**
2. Pilih repository: **`InventoryKedaiDepanRumah`**
3. Klik **"Import"**

### 3.3 Configure Project
Di halaman konfigurasi:

**Framework Preset**: `Other`

**Build & Development Settings**:
- Build Command: `chmod +x build_files.sh && ./build_files.sh`
- Output Directory: `staticfiles`
- Install Command: `pip install -r requirements.txt`

**Root Directory**: `.` (default)

### 3.4 Setup Environment Variables
Klik **"Environment Variables"**, tambahkan satu per satu:

| Variable Name | Value | Contoh |
|---------------|-------|--------|
| `DJANGO_SECRET_KEY` | Generate baru (lihat cara di bawah) | `django-insecure-abc123...` |
| `DJANGO_DEBUG` | `False` | `False` |
| `DJANGO_ALLOWED_HOSTS` | Domain Vercel kamu | `.vercel.app` |
| `DATABASE_URL` | Connection string dari Neon | `postgresql://user:pass@...` |
| `AXES_FAILURE_LIMIT` | `5` | `5` |
| `AXES_COOLOFF_TIME` | `30` | `30` |
| `ALLOW_PW_CHANGE` | `True` | `True` |
| `AI_PROVIDER` | `gemini` atau `groq` | `gemini` |
| `GEMINI_API_KEY` | API key kamu | `AIzaSy...` |
| `GROQ_API_KEY` | API key kamu (optional) | `gsk_...` |

**💡 Cara Generate Django Secret Key:**
Buka Python di terminal lokal:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
Copy hasilnya.

### 3.5 Deploy!
Klik **"Deploy"** dan tunggu 2-5 menit.

---

## 🎯 LANGKAH 4: Setup Database di Vercel

Setelah deploy selesai, buka terminal dan jalankan:

### 4.1 Install Vercel CLI (jika belum)
```bash
npm install -g vercel
```

### 4.2 Login ke Vercel
```bash
vercel login
```

### 4.3 Jalankan Migrations
```bash
vercel env pull .env.production
```

Kemudian jalankan migration manual via Vercel dashboard atau buat script sederhana.

**ATAU** cara mudah:

1. Buka Vercel Dashboard → Project kamu
2. Klik tab **"Settings"** → **"Functions"**
3. Scroll ke bawah, klik **"Redeploy"**
4. Build script otomatis akan menjalankan migration

### 4.4 Buat Superuser

**Option A: Via Python Anywhere / Local dengan DATABASE_URL**

Di komputer lokal, export DATABASE_URL:
```bash
set DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require
python manage.py createsuperuser --settings=ssm.settings
```

**Option B: Via Django Shell di Vercel** (Advanced)
Buat file `create_superuser.py`:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'password123')
    print("Superuser created!")
```

Upload via:
```bash
vercel env pull
python manage.py shell < create_superuser.py
```

---

## ✅ LANGKAH 5: Testing

### 5.1 Buka Website
Setelah deploy selesai, Vercel akan memberikan URL:
```
https://inventory-kedai-depan-rumah.vercel.app
```

### 5.2 Test Login
1. Buka `/admin` atau `/login`
2. Login dengan superuser yang dibuat
3. Test CRUD operations

### 5.3 Cek Database
1. Buka Neon Dashboard
2. Klik project kamu
3. Klik **"Tables"** di sidebar
4. Pastikan table Django sudah ada

---

## 🔧 Troubleshooting

### ❌ Error: "DisallowedHost"
**Solusi**: Tambahkan domain Vercel ke `DJANGO_ALLOWED_HOSTS`:
```
DJANGO_ALLOWED_HOSTS=.vercel.app,your-domain.vercel.app
```

### ❌ Error: "Static files not found"
**Solusi**: 
1. Pastikan `build_files.sh` executable: `chmod +x build_files.sh`
2. Redeploy project

### ❌ Error: "Database connection failed"
**Solusi**:
1. Cek `DATABASE_URL` di Vercel environment variables
2. Pastikan ada `?sslmode=require` di akhir connection string
3. Test connection string di lokal dulu

### ❌ Error: "No module named 'psycopg2'"
**Solusi**: Pastikan `requirements.txt` sudah include `psycopg2-binary==2.9.10`

---

## 🔄 Update Aplikasi (Push Changes)

Setelah aplikasi live, untuk update:

```bash
# 1. Edit code
# 2. Commit
git add .
git commit -m "Update feature X"

# 3. Push ke GitHub
git push origin main

# Vercel akan otomatis deploy ulang!
```

---

## 📊 Monitoring

### Cek Logs di Vercel
1. Buka Vercel Dashboard
2. Klik project kamu
3. Klik tab **"Deployments"**
4. Klik deployment terakhir
5. Klik **"View Function Logs"**

### Cek Database Usage di Neon
1. Buka Neon Dashboard
2. Klik project kamu
3. Lihat **"Usage"** di sidebar

---

## 💰 Gratis Selamanya?

### Neon Free Tier:
- ✅ 512 MB database storage
- ✅ 3 GB data transfer/bulan
- ✅ 1 project gratis selamanya
- ⚠️ Hibernate setelah 5 menit inactive (auto-wake saat ada request)

### Vercel Free Tier:
- ✅ 100 GB bandwidth/bulan
- ✅ 100 deployments/hari
- ✅ Unlimited projects
- ⚠️ 10 detik max function duration

**Untuk inventory app kecil-menengah, free tier cukup!** 🎉

---

## 🎓 Custom Domain (Optional)

Jika punya domain sendiri:

1. Buka Vercel Dashboard → Project → **Settings** → **Domains**
2. Tambahkan domain kamu
3. Update DNS di provider domain:
   - Add CNAME record: `www` → `cname.vercel-dns.com`
   - Add A record: `@` → `76.76.21.21`

---

## 📞 Need Help?

Jika ada error, kirim screenshot error log beserta:
1. URL Vercel kamu
2. Error message lengkap
3. Kapan error terjadi (saat build/runtime)

Good luck! 🚀
