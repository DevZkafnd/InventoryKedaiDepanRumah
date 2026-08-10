# 🔧 Cara Memperbaiki Error 403 Permission Denied

## 📋 Masalah

Setelah deploy ke Vercel dan login dengan username `admin`, muncul error:
```
Permission denied.
Failed to load resource: the server responded with a status of 403
GET /post-login/ HTTP/1.1" 403
```

## 🎯 Penyebab

User `admin` di database NeonTech belum ditambahkan ke grup `managers`, sehingga tidak punya akses ke halaman dashboard.

## ✅ Solusi

### **Opsi 1: Jalankan Script Otomatis (RECOMMENDED)**

1. **Pastikan file `.env` sudah memiliki `DATABASE_URL` yang mengarah ke NeonTech:**

   ```env
   DATABASE_URL=postgresql://neondb_owner:npg_j8ThFKgdmpw7@ep-orange-wildflower-aztc4bgj.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
   ```

2. **Jalankan script perbaikan:**

   ```bash
   run_fix_admin.bat
   ```

   Script ini akan:
   - ✓ Membuat semua grup yang diperlukan (owners, managers, cashiers, shop_users)
   - ✓ Menambahkan user `admin` ke grup `managers`
   - ✓ Memastikan `admin` adalah superuser dan staff
   - ✓ Jika user tidak ada, akan membuat user baru

3. **Refresh browser dan login lagi**

   ```
   Username: admin
   Password: admin123
   ```

---

### **Opsi 2: Manual via Django Shell**

Jika Anda ingin melakukannya secara manual:

```bash
# Aktifkan virtual environment
.venv314\Scripts\activate.bat

# Buka Django shell
python manage.py shell
```

Kemudian jalankan perintah berikut di shell:

```python
from django.contrib.auth.models import User, Group

# Buat grup managers jika belum ada
managers_group, created = Group.objects.get_or_create(name="managers")

# Ambil user admin
admin_user = User.objects.get(username="admin")

# Tambahkan ke grup managers
admin_user.groups.add(managers_group)

# Pastikan adalah superuser
admin_user.is_superuser = True
admin_user.is_staff = True
admin_user.save()

print("User admin berhasil diperbaiki!")
exit()
```

---

### **Opsi 3: Jalankan Seed Data Lengkap**

Jika Anda ingin mengisi database dengan data contoh sekaligus:

```bash
# Aktifkan virtual environment
.venv314\Scripts\activate.bat

# Jalankan seed data
python seed_data.py
```

Ini akan:
- ✓ Membuat semua grup
- ✓ Membuat user admin, owner1, kasir1
- ✓ Mengisi data barang contoh
- ✓ Mengisi stok toko kasir1

---

## 🧪 Verifikasi

Setelah menjalankan script, verifikasi dengan cara:

1. **Login ke aplikasi:**
   - URL: https://inventory-kedai-depan-rumah-iota.vercel.app/accounts/login/
   - Username: `admin`
   - Password: `admin123`

2. **Seharusnya redirect ke:** `/dashboard/` (bukan error 403 lagi)

3. **Cek user di Django admin:**
   - URL: https://inventory-kedai-depan-rumah-iota.vercel.app/admin/
   - Login dengan `admin` / `admin123`
   - Buka **Users** → **admin** → Cek bagian **Groups** apakah ada `managers`

---

## 📊 Struktur Grup & Akses

| Grup       | Akses                                                      |
|------------|-----------------------------------------------------------|
| `owners`   | Dashboard (read-only), Reports, Waste (read-only), AI     |
| `managers` | Dashboard, Warehouse, Shop, Transfer, Reports, Waste      |
| `cashiers` | Shop, Transfer (tidak bisa ke Dashboard/Warehouse)        |
| `shop_users` | Shop, Transfer (alias untuk cashiers, legacy support)   |

---

## 🔍 Troubleshooting

### Masih Error 403 Setelah Perbaikan?

1. **Cek apakah script berhasil:**
   ```bash
   python fix_admin_groups.py
   ```
   
   Output seharusnya:
   ```
   [✓] Grup 'managers' dibuat (atau sudah ada)
   [INFO] User 'admin' ditemukan
   [✓] User 'admin' ditambahkan ke grup 'managers'
   ```

2. **Cek di Django shell:**
   ```python
   from django.contrib.auth.models import User
   admin = User.objects.get(username="admin")
   print(admin.groups.values_list('name', flat=True))
   # Output: ['managers']
   ```

3. **Logout dan login lagi** (penting! session lama mungkin masih cache)

### User 'admin' Tidak Ditemukan?

Script akan otomatis membuat user baru dengan:
- Username: `admin`
- Password: `admin123`
- Grup: `managers`
- Status: superuser & staff

---

## 💡 Tips

- Untuk production, sebaiknya ganti password default `admin123` setelah login
- Jika ingin testing, gunakan user `owner1` (password: `owner123`) atau `kasir1` (password: `kasir123`)
- Pastikan `.env` atau environment variables di Vercel sudah set `DATABASE_URL` dengan benar

---

## 📝 File Terkait

- `fix_admin_groups.py` - Script perbaikan otomatis
- `run_fix_admin.bat` - Batch script untuk Windows
- `seed_data.py` - Script lengkap untuk seed database
- `stock_manager/views.py` - File yang mengandung logika `post_login_redirect`
