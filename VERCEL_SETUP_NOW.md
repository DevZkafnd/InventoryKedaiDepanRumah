# 🚀 Setup Vercel - Copy Paste Ready!

## ✅ Database Neon Sudah Siap!

**Connection String**:
```
postgresql://neondb_owner:npg_j8ThFKgdmpw7@ep-orange-wildflower-aztc4bgj.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
```

---

## 📝 **Environment Variables untuk Vercel**

Copy paste values di bawah ini ke Vercel Dashboard → Environment Variables

### ✅ **WAJIB (Copy Paste)**

| Key | Value |
|-----|-------|
| `DJANGO_SECRET_KEY` | `bbr+#nr)bxx^rgno4ki@=ecu*6bl^i-3^cu*v+=rqa6o0^1#h+` |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `.vercel.app` |
| `DATABASE_URL` | `postgresql://neondb_owner:npg_j8ThFKgdmpw7@ep-orange-wildflower-aztc4bgj.ap-southeast-1.aws.neon.tech/neondb?sslmode=require` |
| `AXES_FAILURE_LIMIT` | `5` |
| `AXES_COOLOFF_TIME` | `30` |
| `ALLOW_PW_CHANGE` | `True` |

### 🤖 **Optional - AI Assistant**

Jika mau AI Assistant aktif, tambahkan ini juga:

| Key | Value |
|-----|-------|
| `AI_PROVIDER` | `gemini` |
| `GEMINI_API_KEY` | *(Ambil dari https://aistudio.google.com/app/apikey)* |

**Cara dapat Gemini API Key**:
1. Buka: https://aistudio.google.com/app/apikey
2. Login dengan Google
3. Klik **"Create API Key"**
4. Copy API key yang muncul
5. Paste ke Vercel

---

## 🎯 **Step-by-Step Deploy Vercel**

### **1. Buka Vercel**
https://vercel.com

### **2. Sign Up / Login**
- Klik **"Sign Up"** atau **"Login"**
- Pilih **"Continue with GitHub"**
- Authorize Vercel

### **3. Import Project**
- Klik **"Add New Project"**
- Pilih repository: **`InventoryKedaiDepanRumah`**
- Klik **"Import"**

### **4. Configure Project**

**Framework Preset**: 
```
Other
```

**Root Directory**: 
```
. 
```
(biarkan default / kosong)

**Build Command**: 
```
chmod +x build_files.sh && ./build_files.sh
```

**Output Directory**: 
```
staticfiles
```

**Install Command**: 
```
pip install -r requirements.txt
```

### **5. Add Environment Variables**

Klik **"Environment Variables"**, lalu tambahkan satu per satu dari tabel di atas.

**Cara tambahkan**:
1. Ketik **Key** (contoh: `DJANGO_SECRET_KEY`)
2. Paste **Value** (contoh: `bbr+#nr)bxx^rgno4ki@=ecu*6bl^i-3^cu*v+=rqa6o0^1#h+`)
3. Pilih environment: **Production, Preview, Development** (centang semua)
4. Klik **"Add"**
5. Ulangi untuk semua variables

**⚠️ PENTING**: 
- Untuk `DATABASE_URL`, copy PERSIS dari atas (termasuk `?sslmode=require`)
- Jangan ada spasi di awal/akhir value!

### **6. Deploy!**

Klik **"Deploy"** dan tunggu 3-5 menit. ☕

Vercel akan:
- ✅ Install dependencies
- ✅ Run migrations
- ✅ Collect static files
- ✅ Deploy aplikasi

---

## 📊 **Monitor Deployment**

Saat deploy, kamu bisa lihat progress di:
1. **Building** - Install dependencies
2. **Deploying** - Upload ke server
3. **Ready** - Aplikasi live! 🎉

Jika ada error, klik **"View Function Logs"** untuk lihat detail error.

---

## ✅ **Setelah Deploy Selesai**

### **A. Cek URL**
Vercel akan kasih URL seperti:
```
https://inventory-kedai-depan-rumah.vercel.app
```

Buka URL tersebut, pastikan landing page muncul.

### **B. Create Superuser**

**Option 1 - Via Local Terminal (Recommended)**:
```bash
# Set environment variables
set DATABASE_URL=postgresql://neondb_owner:npg_j8ThFKgdmpw7@ep-orange-wildflower-aztc4bgj.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
set DJANGO_SECRET_KEY=bbr+#nr)bxx^rgno4ki@=ecu*6bl^i-3^cu*v+=rqa6o0^1#h+
set DJANGO_DEBUG=False
set DJANGO_ALLOWED_HOSTS=localhost
set AXES_FAILURE_LIMIT=5
set AXES_COOLOFF_TIME=30
set ALLOW_PW_CHANGE=True

# Create superuser
python manage.py createsuperuser

# Isi:
# Username: admin
# Email: admin@example.com
# Password: (password kuat kamu)
```

**Option 2 - Via Neon SQL Editor**:
1. Buka Neon Dashboard
2. Klik project kamu
3. Klik **"SQL Editor"**
4. Paste & run script create user (akan saya buatkan nanti jika opsi 1 gagal)

### **C. Test Login**
1. Buka: `https://your-app.vercel.app/admin`
2. Login dengan superuser yang baru dibuat
3. Test CRUD operations

---

## 🔄 **Update Code di Future**

Setelah aplikasi live, untuk update:

```bash
# Edit code
git add .
git commit -m "Update feature X"
git push origin master

# Vercel otomatis deploy ulang! 🎉
```

---

## 🆘 **Troubleshooting**

### ❌ **Build Failed**
1. Klik **"View Function Logs"**
2. Cari error message
3. Biasanya masalah:
   - Environment variables salah
   - Missing dependencies
   - Syntax error di code

### ❌ **"DisallowedHost at /"**
**Solusi**: Edit environment variable `DJANGO_ALLOWED_HOSTS`:
```
.vercel.app,your-app-name.vercel.app
```
Lalu **Redeploy** (Deployments → Redeploy)

### ❌ **"Database connection failed"**
**Solusi**: 
1. Cek `DATABASE_URL` di Vercel
2. Pastikan PERSIS sama dengan yang di atas
3. Harus ada `?sslmode=require`

### ❌ **Static files not loading**
**Solusi**: Redeploy dari dashboard

---

## 📞 **Butuh Bantuan?**

Jika ada error:
1. Screenshot error message lengkap
2. Screenshot **Function Logs** di Vercel
3. Tanya di chat

---

## 🎉 **Summary**

1. ✅ Database Neon: Ready
2. ⏳ Deploy Vercel: Lakukan sekarang
3. ⏳ Create Superuser: Setelah deploy
4. ⏳ Test Website: Setelah superuser

**Buka Vercel sekarang**: https://vercel.com 🚀

Good luck! 🎉
