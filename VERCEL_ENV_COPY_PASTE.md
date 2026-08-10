# 📋 Copy Paste Environment Variables ke Vercel

## ✅ **7 VARIABLES WAJIB (HARUS DIISI!)**

Copy paste satu per satu ke Vercel Dashboard → Environment Variables.

---

### **1️⃣ DJANGO_SECRET_KEY**
```
bbr+#nr)bxx^rgno4ki@=ecu*6bl^i-3^cu*v+=rqa6o0^1#h+
```

---

### **2️⃣ DJANGO_DEBUG**
```
False
```

---

### **3️⃣ DJANGO_ALLOWED_HOSTS**
```
.vercel.app
```

---

### **4️⃣ DATABASE_URL**
```
postgresql://neondb_owner:npg_j8ThFKgdmpw7@ep-orange-wildflower-aztc4bgj.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
```

---

### **5️⃣ AXES_FAILURE_LIMIT**
```
5
```

---

### **6️⃣ AXES_COOLOFF_TIME**
```
30
```

---

### **7️⃣ ALLOW_PW_CHANGE**
```
True
```

---

## 🤖 **AI Assistant (3 Variables) - PILIH SALAH SATU!**

Kamu punya 2 pilihan AI provider:

### **OPTION A: Pakai Groq (Lebih Cepat)** ✅ Recommended

### **8️⃣ AI_PROVIDER**
```
groq
```

### **9️⃣ GROQ_API_KEY**
```
(Copy dari file .env lokal kamu - format: gsk_...)
```

---

### **OPTION B: Pakai Gemini (Google)** 

### **8️⃣ AI_PROVIDER**
```
gemini
```

### **9️⃣ GEMINI_API_KEY**
```
(Copy dari file .env lokal kamu - format: AQ....)
```

---

### **OPTION C: Pakai Keduanya (Backup)** ⭐ Best

Tambahkan semua 3 variables ini:

### **8️⃣ AI_PROVIDER**
```
groq
```
*(Ganti ke `gemini` jika Groq bermasalah)*

### **9️⃣ GROQ_API_KEY**
```
(Copy dari file .env lokal kamu - format: gsk_...)
```

### **🔟 GEMINI_API_KEY**
```
(Copy dari file .env lokal kamu - format: AQ....)
```

**⚠️ Jika tidak mau AI Assistant, SKIP semua langkah AI!**

---

## 📊 **Tabel Ringkasan**

### **Minimal (7 Variables)**: Tanpa AI
| No | Key | Value | Wajib? |
|----|-----|-------|--------|
| 1 | `DJANGO_SECRET_KEY` | `bbr+#nr)bxx^rgno4ki@=ecu*6bl^i-3^cu*v+=rqa6o0^1#h+` | ✅ Ya |
| 2 | `DJANGO_DEBUG` | `False` | ✅ Ya |
| 3 | `DJANGO_ALLOWED_HOSTS` | `.vercel.app` | ✅ Ya |
| 4 | `DATABASE_URL` | `postgresql://neondb_owner:npg...` | ✅ Ya |
| 5 | `AXES_FAILURE_LIMIT` | `5` | ✅ Ya |
| 6 | `AXES_COOLOFF_TIME` | `30` | ✅ Ya |
| 7 | `ALLOW_PW_CHANGE` | `True` | ✅ Ya |

### **Dengan AI - Option A (9 Variables)**: Groq Only
| No | Key | Value | Wajib? |
|----|-----|-------|--------|
| ... | *(7 variables di atas)* | ... | ✅ Ya |
| 8 | `AI_PROVIDER` | `groq` | ⚪ Optional |
| 9 | `GROQ_API_KEY` | `gsk_Lxjne...` | ⚪ Optional |

### **Dengan AI - Option B (9 Variables)**: Gemini Only
| No | Key | Value | Wajib? |
|----|-----|-------|--------|
| ... | *(7 variables di atas)* | ... | ✅ Ya |
| 8 | `AI_PROVIDER` | `gemini` | ⚪ Optional |
| 9 | `GEMINI_API_KEY` | `AQ.Ab8R...` | ⚪ Optional |

### **Dengan AI - Option C (10 Variables)**: Keduanya ⭐ Recommended
| No | Key | Value | Wajib? |
|----|-----|-------|--------|
| ... | *(7 variables di atas)* | ... | ✅ Ya |
| 8 | `AI_PROVIDER` | `groq` atau `gemini` | ⚪ Optional |
| 9 | `GROQ_API_KEY` | `gsk_Lxjne...` | ⚪ Optional |
| 10 | `GEMINI_API_KEY` | `AQ.Ab8R...` | ⚪ Optional |

---

## 🎯 **Cara Input ke Vercel**

### **Step 1: Buka Environment Variables**
Di Vercel project configuration, scroll ke **"Environment Variables"**

### **Step 2: Hapus EXAMPLE_NAME**
Klik icon **minus (-)** untuk hapus contoh yang ada

### **Step 3: Tambah Variable Pertama**
1. Di field **"Key"**, ketik: `DJANGO_SECRET_KEY`
2. Di field **"Value"**, paste: `bbr+#nr)bxx^rgno4ki@=ecu*6bl^i-3^cu*v+=rqa6o0^1#h+`
3. **Environments**: Pilih **"Production and Preview"**
4. Klik **icon save** atau tekan Enter

### **Step 4: Klik "+ Add More"**
Untuk tambah variable berikutnya

### **Step 5: Ulangi untuk Variable 2-7**
Copy paste dari tabel di atas

### **Step 6 (Optional): Tambah AI Variables**
Jika mau AI Assistant, tambahkan variable 8 & 9

---

## ✅ **Verifikasi**

Setelah selesai, pastikan kamu punya **MINIMAL 7 variables** di list:

```
✅ DJANGO_SECRET_KEY
✅ DJANGO_DEBUG
✅ DJANGO_ALLOWED_HOSTS
✅ DATABASE_URL
✅ AXES_FAILURE_LIMIT
✅ AXES_COOLOFF_TIME
✅ ALLOW_PW_CHANGE

(Optional)
⚪ AI_PROVIDER
⚪ GEMINI_API_KEY
```

---

## 🚀 **Setelah Input Semua Variables**

1. **Scroll ke bawah**
2. **Klik tombol "Deploy"**
3. **Tunggu 3-5 menit** ☕
4. **Done!** 🎉

---

## 🆘 **Troubleshooting**

### ❌ "Lupa sudah tambah variable apa saja"
**Solusi**: Di Vercel, kamu bisa lihat list variables yang sudah ditambahkan di section Environment Variables. Cocokkan dengan checklist di atas.

### ❌ "Value terlalu panjang tidak terlihat penuh"
**Solusi**: Tidak masalah! Vercel menyimpan value lengkap meskipun tampilan terpotong.

### ❌ "Error: SECRET_KEY not found"
**Solusi**: Pastikan key-nya adalah `DJANGO_SECRET_KEY` (huruf besar semua, ada underscore)

### ❌ "Error: DisallowedHost"
**Solusi**: Pastikan `DJANGO_ALLOWED_HOSTS` valuenya adalah `.vercel.app` (ada titik di depan)

---

## 💡 **Tips**

- Copy paste langsung dari file ini, jangan ketik manual!
- Pastikan tidak ada spasi di awal/akhir value
- Untuk `DATABASE_URL`, pastikan ada `?sslmode=require` di akhir
- Jika tidak yakin, screenshot list environment variables kamu dan tunjukkan ke saya

---

**File lengkap**: Lihat `.env.vercel` untuk referensi lengkap dengan komentar
