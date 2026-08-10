# 🚀 START HERE - Deploy ke Vercel + Neon

## ✅ Yang Sudah Selesai

**Semua konfigurasi code sudah siap dan di-push ke GitHub!**

Repository: https://github.com/DevZkafnd/InventoryKedaiDepanRumah.git

---

## 🎯 Yang Harus Kamu Lakukan (3 Langkah Utama)

### 📍 STEP 1: Buat Database PostgreSQL (5 menit)

1. **Buka**: https://neon.tech
2. **Sign Up** dengan GitHub
3. **Create New Project**:
   - Name: `inventory-kedai`
   - Region: **Singapore** (paling dekat Indonesia)
   - PostgreSQL: 16 (latest)
4. **Copy Connection String** yang muncul:
   ```
   postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require
   ```
5. **Simpan** connection string ini! ⚠️

**✅ Done? Lanjut Step 2**

---

### 📍 STEP 2: Deploy ke Vercel (10 menit)

#### A. Import Project
1. **Buka**: https://vercel.com
2. **Sign Up** dengan GitHub
3. Klik **"Add New Project"**
4. Pilih repo: **`InventoryKedaiDepanRumah`**
5. Klik **"Import"**

#### B. Configure Build Settings
- **Framework Preset**: Other
- **Build Command**: `chmod +x build_files.sh && ./build_files.sh`
- **Output Directory**: `staticfiles`
- **Install Command**: `pip install -r requirements.txt`

#### C. Setup Environment Variables
Klik **"Environment Variables"**, lalu tambahkan:

| Variable | Value | Cara Dapat |
|----------|-------|------------|
| `DJANGO_SECRET_KEY` | (generate baru) | Lihat cara di bawah ⬇️ |
| `DJANGO_DEBUG` | `False` | Ketik: False |
| `DJANGO_ALLOWED_HOSTS` | `.vercel.app` | Ketik: .vercel.app |
| `DATABASE_URL` | (dari Neon) | Paste connection string dari Step 1 |
| `AXES_FAILURE_LIMIT` | `5` | Ketik: 5 |
| `AXES_COOLOFF_TIME` | `30` | Ketik: 30 |
| `ALLOW_PW_CHANGE` | `True` | Ketik: True |

**Optional - Jika mau AI Assistant:**
| Variable | Value | Cara Dapat |
|----------|-------|------------|
| `AI_PROVIDER` | `gemini` | Ketik: gemini |
| `GEMINI_API_KEY` | (API key) | https://aistudio.google.com/app/apikey |

**💡 Cara Generate DJANGO_SECRET_KEY:**
Buka Python di terminal lokal:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
Copy hasilnya.

#### D. Deploy!
Klik **"Deploy"** dan tunggu 3-5 menit. ☕

**✅ Done? Lanjut Step 3**

---

### 📍 STEP 3: Setup Admin User (2 menit)

Setelah deploy selesai, buat superuser:

#### Option A: Via Local Terminal
```bash
# Set DATABASE_URL (paste dari Neon)
set DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require

# Create superuser
python manage.py createsuperuser

# Isi username, email, password
```

#### Option B: Via Vercel CLI
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Create superuser
vercel env pull .env.production
python manage.py createsuperuser
```

**✅ Done? Test website!**

---

## 🎉 Testing

1. **Buka URL Vercel kamu** (contoh: `https://inventory-kedai.vercel.app`)
2. **Test landing page** - Pastikan halaman utama muncul
3. **Login** ke `/admin` atau `/login` dengan superuser
4. **Test Dashboard** - Cek semua menu jalan
5. **Test CRUD** - Coba tambah/edit/hapus item

---

## 🔄 Auto Deploy (Update di Future)

**Setelah aplikasi live**, untuk update code:

```bash
# 1. Edit code sesuai kebutuhan
# 2. Commit & push
git add .
git commit -m "Update feature X"
git push origin master

# 3. Vercel otomatis deploy! 🎉
```

**Tidak perlu konfigurasi ulang!** Cukup push ke GitHub, Vercel akan auto-deploy.

---

## 📚 Dokumentasi Lengkap

Baca dokumentasi detail di:

| File | Isi |
|------|-----|
| **QUICK_DEPLOY_GUIDE.md** | Panduan ringkas step-by-step |
| **DEPLOY_VERCEL.md** | Panduan lengkap dengan troubleshooting |
| **ENV_VARIABLES_VERCEL.md** | Penjelasan detail semua environment variables |
| **CHECKLIST_DEPLOY.md** | Checklist apa saja yang sudah/belum dikerjakan |
| **COMMANDS_CHEATSHEET.md** | Kumpulan command untuk database, git, dll |

---

## 🆘 Troubleshooting Cepat

### ❌ Error: "DisallowedHost"
**Solusi**: Tambahkan domain Vercel ke `DJANGO_ALLOWED_HOSTS`:
```
DJANGO_ALLOWED_HOSTS = .vercel.app,your-app.vercel.app
```
Lalu **Redeploy** di Vercel dashboard.

### ❌ Error: "Database connection failed"
**Solusi**: 
1. Cek `DATABASE_URL` di Vercel environment variables
2. Pastikan ada `?sslmode=require` di akhir
3. Test connection di local dulu

### ❌ Error: "Static files not found"
**Solusi**: Redeploy dari Vercel dashboard → Deployments → Redeploy

### ❌ Error saat Build
**Solusi**: Cek **Function Logs** di Vercel dashboard → Deployments → View Function Logs

---

## 💰 Biaya

- **Neon PostgreSQL**: ✅ Gratis selamanya (512 MB storage)
- **Vercel Hosting**: ✅ Gratis selamanya (100 GB bandwidth/bulan)
- **Google Gemini AI**: ✅ Gratis (60 requests/menit)

**100% GRATIS untuk inventory app kecil-menengah!** 🎉

---

## 🎓 Struktur Code yang Sudah Disiapkan

```
✅ vercel.json - Config Vercel deployment
✅ build_files.sh - Build script (collect static, migrate)
✅ requirements.txt - Dependencies dengan PostgreSQL support
✅ ssm/settings.py - Auto switch SQLite (local) ↔️ PostgreSQL (production)
✅ ssm/wsgi_vercel.py - WSGI handler untuk Vercel
✅ .vercelignore - File yang diabaikan saat deploy
✅ .gitignore - File yang tidak di-commit
```

**Semua sudah di-push ke GitHub!** Tinggal deploy saja. 🚀

---

## 📞 Butuh Bantuan?

Jika ada error:
1. Screenshot error message lengkap
2. Cek di **Vercel Dashboard → Deployments → Function Logs**
3. Baca troubleshooting di **DEPLOY_VERCEL.md**

**Happy Deploying!** 🎉

---

**Quick Links**:
- GitHub Repo: https://github.com/DevZkafnd/InventoryKedaiDepanRumah.git
- Neon (Database): https://neon.tech
- Vercel (Hosting): https://vercel.com
- Google AI Studio (Gemini API): https://aistudio.google.com/app/apikey
