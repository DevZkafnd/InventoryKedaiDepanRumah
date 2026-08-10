# 🔧 Fix Vercel Build Error

## ❌ Error Yang Terjadi:
```
Error: Command "./build_files.sh" exited with 1
```

## ✅ Solusi:

### **Option 1: Simplify Build (Recommended)**

Di Vercel Dashboard → Project Settings → General:

#### **1. Build Command**:
**GANTI dari**:
```bash
chmod +x build_files.sh && ./build_files.sh
```

**MENJADI**:
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

#### **2. Output Directory**:
**KOSONGKAN** (hapus `staticfiles`)

#### **3. Install Command**:
**BIARKAN KOSONG** atau isi:
```bash
pip install -r requirements.txt
```

---

### **Option 2: Hapus Build Command Sama Sekali**

Di Vercel Dashboard → Project Settings:

1. **Build Command**: Kosongkan (hapus semua)
2. **Output Directory**: Kosongkan
3. **Install Command**: Kosongkan

Vercel akan otomatis detect Django dan build sendiri.

---

### **Option 3: Override Build Settings di vercel.json**

File `vercel.json` sudah di-update dengan konfigurasi minimal:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "ssm/wsgi.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "ssm/wsgi.py"
    }
  ]
}
```

**Redeploy** project dari Vercel dashboard.

---

## 🔍 Cek Environment Variables

Pastikan semua environment variables sudah diisi dengan benar:

### **WAJIB**:
```
✅ DJANGO_SECRET_KEY
✅ DJANGO_DEBUG = False
✅ DJANGO_ALLOWED_HOSTS = .vercel.app
✅ DATABASE_URL = postgresql://...
✅ AXES_FAILURE_LIMIT = 5
✅ AXES_COOLOFF_TIME = 30
✅ ALLOW_PW_CHANGE = True
```

**Cek di**: Vercel Dashboard → Project → Settings → Environment Variables

---

## 🚀 Redeploy

Setelah ubah settings:

1. Buka Vercel Dashboard
2. Klik tab **"Deployments"**
3. Klik **"..."** di deployment terakhir
4. Pilih **"Redeploy"**
5. Tunggu 2-3 menit

---

## 📊 Cek Logs

Jika masih error, cek detail logs:

1. Buka deployment yang failed
2. Klik **"View Function Logs"** atau **"Build Logs"**
3. Screenshot error message lengkap
4. Share ke saya untuk troubleshooting

---

## 🆘 Common Errors

### ❌ "No module named 'psycopg2'"
**Solusi**: Pastikan `requirements.txt` berisi `psycopg2-binary==2.9.10`

### ❌ "SECRET_KEY not found"
**Solusi**: Cek environment variable `DJANGO_SECRET_KEY` sudah diisi

### ❌ "Database connection failed"
**Solusi**: 
1. Cek `DATABASE_URL` format benar
2. Pastikan ada `?sslmode=require` di akhir

### ❌ "DisallowedHost"
**Solusi**: Pastikan `DJANGO_ALLOWED_HOSTS` berisi `.vercel.app`

---

## 💡 Tips

- Gunakan **Option 1** (simplify build command) untuk hasil terbaik
- Static files akan di-serve oleh WhiteNoise middleware (sudah dikonfigurasi di settings.py)
- Migrations akan dijalankan saat pertama kali ada request ke database

---

**Setelah fix, redeploy dan test website!** 🎉
