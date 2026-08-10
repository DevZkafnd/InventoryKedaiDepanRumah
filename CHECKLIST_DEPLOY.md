# ✅ Checklist Deploy ke Vercel

## 📦 Yang Sudah Dikerjakan:

✅ **1. File Konfigurasi Dibuat**
- `vercel.json` - Config Vercel
- `build_files.sh` - Build script
- `.vercelignore` - File yang diabaikan
- `requirements.txt` - Updated dengan PostgreSQL support
- `ssm/settings.py` - Updated untuk production
- `ssm/wsgi_vercel.py` - WSGI handler untuk Vercel

✅ **2. Dependencies Ditambahkan**
- `psycopg2-binary==2.9.10` - PostgreSQL adapter
- `dj-database-url==2.2.0` - Database URL parser
- `whitenoise==6.8.2` - Static files handler
- `gunicorn==23.0.0` - Production server

✅ **3. Settings.py Dikonfigurasi**
- Support PostgreSQL via `DATABASE_URL`
- WhiteNoise untuk static files
- Production-ready middleware

✅ **4. Code Pushed ke GitHub**
- Repository: https://github.com/DevZkafnd/InventoryKedaiDepanRumah.git
- Branch: `master`
- Commit: "Prepare for Vercel deployment with PostgreSQL support"

---

## 🎯 Yang Harus Kamu Lakukan Sekarang:

### 🗄️ STEP 1: Setup Database (Neon PostgreSQL)

**Link**: https://neon.tech

**Action Items**:
- [ ] Sign up pakai GitHub/Google
- [ ] Create new project: `inventory-kedai`
- [ ] Pilih region: **Singapore**
- [ ] Copy connection string
- [ ] Simpan connection string dengan aman

**Connection string format**:
```
postgresql://username:password@ep-xxx-xxx.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
```

---

### ☁️ STEP 2: Deploy ke Vercel

**Link**: https://vercel.com

**Action Items**:
- [ ] Sign up pakai GitHub
- [ ] Import project: `InventoryKedaiDepanRumah`
- [ ] Set framework: **Other**
- [ ] Set build command: `chmod +x build_files.sh && ./build_files.sh`
- [ ] Set output directory: `staticfiles`

**Environment Variables yang Harus Ditambahkan**:
- [ ] `DJANGO_SECRET_KEY` (generate baru)
- [ ] `DJANGO_DEBUG` = `False`
- [ ] `DJANGO_ALLOWED_HOSTS` = `.vercel.app`
- [ ] `DATABASE_URL` (dari Neon)
- [ ] `AXES_FAILURE_LIMIT` = `5`
- [ ] `AXES_COOLOFF_TIME` = `30`
- [ ] `ALLOW_PW_CHANGE` = `True`
- [ ] `AI_PROVIDER` = `gemini` atau `groq`
- [ ] `GEMINI_API_KEY` (jika pakai Gemini)
- [ ] `GROQ_API_KEY` (jika pakai Groq)

- [ ] Klik Deploy dan tunggu selesai

---

### 👤 STEP 3: Setup Superuser

**Action Items**:
- [ ] Copy `DATABASE_URL` dari Vercel environment variables
- [ ] Di terminal lokal, set environment variable:
  ```bash
  set DATABASE_URL=postgresql://...
  ```
- [ ] Run createsuperuser:
  ```bash
  python manage.py createsuperuser
  ```
- [ ] Masukkan username, email, password

---

### ✅ STEP 4: Testing

**Action Items**:
- [ ] Buka URL Vercel kamu
- [ ] Test halaman landing (`/`)
- [ ] Test login (`/login` atau `/admin`)
- [ ] Test dashboard
- [ ] Test CRUD operations
- [ ] Test AI Assistant (jika ada)

---

## 📚 Dokumentasi

Baca dokumentasi lengkap di:
- **QUICK_DEPLOY_GUIDE.md** - Panduan ringkas dengan command
- **DEPLOY_VERCEL.md** - Panduan lengkap step-by-step

---

## 🆘 Jika Ada Error

### Error saat Build di Vercel
1. Cek **Function Logs** di Vercel
2. Screenshot error message
3. Pastikan semua environment variables sudah diset

### Error Database Connection
1. Cek `DATABASE_URL` format benar
2. Harus ada `?sslmode=require`
3. Test connection di lokal dulu

### Error Static Files
1. Redeploy dari Vercel dashboard
2. Pastikan `build_files.sh` executable

---

## 🎉 Setelah Success

Update aplikasi di future:
```bash
git add .
git commit -m "Update feature X"
git push origin master
```

Vercel akan otomatis deploy ulang! 🚀

---

**Status**: ✅ Ready to Deploy
**GitHub**: ✅ Pushed
**Next**: Setup Neon → Deploy Vercel → Create Superuser → Test
