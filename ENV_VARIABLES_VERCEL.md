# 🔐 Environment Variables untuk Vercel

## ✅ Checklist Environment Variables

Semua variable ini harus ditambahkan di **Vercel Dashboard** → **Project Settings** → **Environment Variables**.

---

## 🔴 WAJIB (Required)

### 1. `DJANGO_SECRET_KEY`
**Value**: Generate baru dengan cara:
```python
# Buka Python shell
python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

**Contoh hasil**:
```
django-insecure-abc123xyz789!@#$%^&*()_+-=
```

**⚠️ Jangan pakai secret key yang sama dengan local development!**

---

### 2. `DJANGO_DEBUG`
**Value**: `False`

**⚠️ HARUS False untuk production!**

---

### 3. `DJANGO_ALLOWED_HOSTS`
**Value**: `.vercel.app`

**Penjelasan**: Ini mengizinkan semua subdomain Vercel. Jika kamu punya custom domain, tambahkan juga:
```
.vercel.app,yourdomain.com,www.yourdomain.com
```

---

### 4. `DATABASE_URL`
**Value**: Connection string dari Neon PostgreSQL

**Format**:
```
postgresql://username:password@ep-xxx-xxx.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
```

**Cara dapat**:
1. Buka Neon Dashboard
2. Pilih project kamu
3. Klik **Connection Details**
4. Copy **Connection string** (Pilih "Pooled connection" untuk better performance)

**⚠️ Pastikan ada `?sslmode=require` di akhir!**

---

### 5. `AXES_FAILURE_LIMIT`
**Value**: `5`

**Penjelasan**: Jumlah login gagal sebelum akun terkunci.

---

### 6. `AXES_COOLOFF_TIME`
**Value**: `30`

**Penjelasan**: Waktu cooldown (dalam menit) setelah akun terkunci.

---

### 7. `ALLOW_PW_CHANGE`
**Value**: `True`

**Penjelasan**: Izinkan user mengganti password sendiri.

---

## 🤖 AI Configuration (Optional tapi Disarankan)

### 8. `AI_PROVIDER`
**Value**: `gemini` atau `groq`

**Pilih salah satu**:
- `gemini` - Google Gemini AI (Gratis, perlu API key)
- `groq` - Groq AI (Gratis, perlu API key)

---

### 9. `GEMINI_API_KEY` (Jika pakai Gemini)
**Value**: API key dari Google AI Studio

**Cara dapat**:
1. Buka: https://aistudio.google.com/app/apikey
2. Login dengan Google
3. Klik **"Get API Key"** atau **"Create API Key"**
4. Copy API key

**Contoh**:
```
AIzaSyABC123XYZ789...
```

**⚠️ Jika tidak pakai AI Assistant, bisa dikosongi atau tidak ditambahkan.**

---

### 10. `GROQ_API_KEY` (Jika pakai Groq)
**Value**: API key dari Groq Console

**Cara dapat**:
1. Buka: https://console.groq.com/keys
2. Sign up / Login
3. Klik **"Create API Key"**
4. Copy API key

**Contoh**:
```
gsk_ABC123XYZ789...
```

---

## 📧 Email Service (Optional)

Jika kamu mau email notifications/reset password:

### 11. `MAIL_SERVICE_BACKEND`
**Value**: `anymail.backends.sparkpost.EmailBackend`

### 12. `MAIL_SERVICE_API_KEY`
**Value**: API key dari SparkPost

### 13. `MAIL_SERVICE_API_URL`
**Value**: `https://api.sparkpost.com/api/v1`

### 14. `MAIL_DEFAULT_FROM`
**Value**: Email pengirim (contoh: `noreply@yourdomain.com`)

### 15. `MAIL_SERVER_EMAIL`
**Value**: Email server (contoh: `server@yourdomain.com`)

**Jika tidak pakai email service, kosongi atau jangan ditambahkan.**

---

## 📊 Logging (Optional)

### 16. `LOG_FILE`
**Value**: Kosongi saja untuk production

**Penjelasan**: Di Vercel, logs otomatis tersimpan di Vercel dashboard, tidak perlu file logging.

---

## 🗂️ Database (Optional - untuk development)

### 17. `DB_NAME`
**Value**: `db.sqlite3`

**Penjelasan**: Ini hanya untuk local development. Di production (Vercel), otomatis pakai `DATABASE_URL`.

**⚠️ Tidak perlu ditambahkan di Vercel karena sudah pakai PostgreSQL.**

---

## 📝 Summary - Minimal Environment Variables

Untuk **minimal working deployment**, kamu cukup setup ini:

```env
DJANGO_SECRET_KEY = (generate baru)
DJANGO_DEBUG = False
DJANGO_ALLOWED_HOSTS = .vercel.app
DATABASE_URL = (dari Neon)
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 30
ALLOW_PW_CHANGE = True
```

Jika mau **AI Assistant jalan**, tambahkan:
```env
AI_PROVIDER = gemini
GEMINI_API_KEY = (dari Google AI Studio)
```

---

## 🎯 Cara Tambahkan di Vercel

### Via Vercel Dashboard (Web):
1. Buka: https://vercel.com/dashboard
2. Pilih project: `InventoryKedaiDepanRumah`
3. Klik tab **"Settings"**
4. Klik **"Environment Variables"** di sidebar
5. Klik **"Add New"**
6. Masukkan **Key** dan **Value**
7. Pilih environment: **Production, Preview, Development** (centang semua)
8. Klik **"Save"**
9. Ulangi untuk semua variables

### Via Vercel CLI:
```bash
vercel env add DJANGO_SECRET_KEY
# Paste value when prompted

vercel env add DJANGO_DEBUG
# Type: False

# ... dst untuk semua variables
```

---

## 🔄 Update Environment Variables

Jika sudah deploy dan mau update env var:
1. Edit di Vercel Dashboard → Settings → Environment Variables
2. Klik **"Redeploy"** di tab **Deployments**

Atau via CLI:
```bash
vercel env rm VARIABLE_NAME
vercel env add VARIABLE_NAME
```

---

## ✅ Verifikasi

Setelah semua environment variables ditambahkan, cek di:
**Vercel Dashboard → Project → Settings → Environment Variables**

Pastikan semua variables yang **WAJIB** sudah ada. ✅

---

## 🆘 Troubleshooting

### Error: "SECRET_KEY not found"
**Solusi**: Pastikan `DJANGO_SECRET_KEY` sudah ditambahkan.

### Error: "DisallowedHost"
**Solusi**: Pastikan `DJANGO_ALLOWED_HOSTS` berisi `.vercel.app` atau domain kamu.

### Error: "Database connection failed"
**Solusi**: 
1. Cek `DATABASE_URL` format benar
2. Pastikan ada `?sslmode=require`
3. Test connection string di local dulu

### Error: "AI service not configured"
**Solusi**: Tambahkan `AI_PROVIDER` dan API key yang sesuai.

---

**Setelah semua environment variables ditambahkan, deploy akan jalan otomatis!** 🚀
