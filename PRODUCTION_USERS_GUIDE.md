# 🔐 Production Users & Security Guide

## ✅ **CORRECT Permission Structure**

Permission structure telah di-fix sesuai requirement!

---

## 👥 User Roles & Access Matrix

| Feature | 👑 Owner | 🧑‍💼 Manager | 🧾 Kasir |
|---------|:--------:|:---------:|:--------:|
| **Dashboard (Analytics)** | ✅ View | ✅ View | ❌ |
| **AI Assistant (Analytics)** | ✅ Only | ❌ | ❌ |
| **Reports (Export)** | ✅ View/Export | ✅ View/Export | ❌ |
| **Warehouse** | ❌ | ✅ Full | ❌ |
| **Maintenance Mode** | ❌ | ✅ Only | ❌ |
| **Waste Input** | ❌ View Only | ✅ Create | ❌ |
| **Barang Masuk (Import)** | ❌ | ✅ Only | ❌ |
| **Shop Operations** | ❌ | ✅ Full | ✅ View |
| **Request Stok (Transfer)** | ❌ | ✅ Full | ✅ Only |

---

## 🎯 Role Descriptions

### 👑 **Owner (Pemilik) - Read-Only Analytics**

**Fungsi**: Pengawas/monitoring dari atas, tidak ikut campur operasional.

**Access**:
- ✅ **Dashboard** - View analytics & performance metrics
- ✅ **AI Assistant** - Business insights & analitik AI (EXCLUSIVE untuk owner)
- ✅ **Reports** - View & export reports untuk analisis
- ✅ **Waste View** - Lihat data barang rusak/terbuang (read-only)
- ❌ **Warehouse** - Tidak bisa akses sama sekali
- ❌ **Shop** - Tidak bisa akses sama sekali
- ❌ **Input/Edit Data** - Tidak bisa mengubah apa pun

**Security**: Owner tidak bisa mengubah data secara sepihak, hanya bisa memantau.

---

### 🧑‍💼 **Manager (Manajer) - Full Operations**

**Fungsi**: Operator penuh atas operasional & data toko/gudang.

**Access**:
- ✅ **Dashboard** - View analytics + manage maintenance mode
- ✅ **Warehouse** - Full CRUD (Create, Read, Update, Delete)
- ✅ **Maintenance Mode** - Aktivasi/deaktivasi maintenance
- ✅ **Waste Input** - Input barang rusak/terbuang
- ✅ **Barang Masuk** - Import Excel, input stok masuk
- ✅ **Shop Operations** - Manage shop stock
- ✅ **Request Stok** - Request & approve transfers
- ✅ **Reports** - View, export, import
- ❌ **AI Assistant** - Tidak bisa akses (exclusive untuk owner)

**Security**: Manager punya kontrol penuh operasional harian, tapi tidak bisa akses AI analytics owner.

---

### 🧾 **Kasir (Cashier) - Limited Operations**

**Fungsi**: Operasional dasar sehari-hari di kasir/toko.

**Access**:
- ✅ **Shop** - View shop stock (read-only)
- ✅ **Request Stok** - Request transfer dari warehouse ke shop
- ❌ **Dashboard** - Tidak bisa akses
- ❌ **Warehouse** - Tidak bisa akses
- ❌ **AI Assistant** - Tidak bisa akses
- ❌ **Reports** - Tidak bisa akses
- ❌ **Maintenance Mode** - Tidak bisa akses
- ❌ **Waste Input** - Tidak bisa akses
- ❌ **Barang Masuk** - Tidak bisa akses

**Security**: Kasir hanya bisa request stok saat kehabisan barang, tidak berwenang input/edit data lain.

---

## 🎯 Recommended Production Users

### **1. Owner** (untuk kamu - full access)
- Username: `owner1`
- Password: `owner123` ⚠️ **GANTI setelah login!**
- Access: Full (semua fitur)

### **2. Manager** (untuk admin/staff warehouse)
- Username: `manager1`
- Password: `manager123` ⚠️ **GANTI setelah login!**
- Access: Warehouse management, Import Excel, Reports

### **3. Kasir** (untuk kasir toko)
- Username: `kasir1`
- Password: `kasir123` ⚠️ **GANTI setelah login!**
- Access: Shop operations, Transfer items dari warehouse

---

## 📋 SQL Queries untuk Create Users

Jalankan di **Neon SQL Editor** (https://console.neon.tech):

### **Step 1: Create Groups**

```sql
-- Create groups if not exist
INSERT INTO auth_group (name)
SELECT 'owners'
WHERE NOT EXISTS (SELECT 1 FROM auth_group WHERE name = 'owners');

INSERT INTO auth_group (name)
SELECT 'managers'
WHERE NOT EXISTS (SELECT 1 FROM auth_group WHERE name = 'managers');

INSERT INTO auth_group (name)
SELECT 'cashiers'
WHERE NOT EXISTS (SELECT 1 FROM auth_group WHERE name = 'cashiers');

INSERT INTO auth_group (name)
SELECT 'shop_users'
WHERE NOT EXISTS (SELECT 1 FROM auth_group WHERE name = 'shop_users');
```

### **Step 2: Get Group IDs**

```sql
SELECT id, name FROM auth_group 
WHERE name IN ('owners', 'managers', 'cashiers', 'shop_users');
```

**⚠️ CATAT id dari setiap group!** Contoh result:
```
id | name
---+------------
1  | owners
2  | managers
3  | cashiers
4  | shop_users
```

### **Step 3: Create Owner User**

```sql
-- Insert owner user
INSERT INTO auth_user (
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined
) VALUES (
    'pbkdf2_sha256$1200000$BISnKmebCo671GZ0zr77Jn$iRejwQ38dqIvO1od/KLo8Kb64cc2d3AB2SbF+XL85K8=',
    NULL,
    false,
    'owner1',
    '',
    '',
    'owner@example.com',
    false,
    true,
    NOW()
) RETURNING id;
```

**Copy id yang muncul** (misal: 5), lalu run:

```sql
-- Assign owner1 to owners group
-- GANTI 5 dengan user_id yang muncul di atas
-- GANTI 1 dengan group_id untuk 'owners' dari step 2
INSERT INTO auth_user_groups (user_id, group_id)
VALUES (5, 1);
```

### **Step 4: Create Manager User**

```sql
-- Insert manager user
INSERT INTO auth_user (
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined
) VALUES (
    'pbkdf2_sha256$1200000$8BInBZilXhdJEcBNt5zJZy$DOJVrnG6BD1cQC22aoPWRMdKmM5n/V7zyKs2RhxrNNY=',
    NULL,
    false,
    'manager1',
    '',
    '',
    'manager@example.com',
    true,
    true,
    NOW()
) RETURNING id;
```

Copy id (misal: 6), lalu:

```sql
-- Assign manager1 to managers group
INSERT INTO auth_user_groups (user_id, group_id)
VALUES (6, 2);
```

### **Step 5: Create Kasir User**

```sql
-- Insert kasir user
INSERT INTO auth_user (
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined
) VALUES (
    'pbkdf2_sha256$1200000$c2xtUH8cTXePL1BIXuRy4G$fzH4pcpxm8+naR58Oc7OIz7b4qc89LfbPMqXj7o1a2c=',
    NULL,
    false,
    'kasir1',
    '',
    '',
    'kasir@example.com',
    false,
    true,
    NOW()
) RETURNING id;
```

Copy id (misal: 7), lalu:

```sql
-- Assign kasir1 to cashiers group
INSERT INTO auth_user_groups (user_id, group_id)
VALUES (7, 3);
```

---

## ✅ Verify Users Created

```sql
SELECT 
    u.id,
    u.username,
    u.email,
    u.is_superuser,
    u.is_staff,
    g.name as group_name
FROM auth_user u
LEFT JOIN auth_user_groups ug ON u.id = ug.user_id
LEFT JOIN auth_group g ON ug.group_id = g.id
ORDER BY u.id;
```

---

## 🔒 Security Best Practices

### **1. Ganti Password Default**

Setelah login pertama kali dengan user baru:
1. Buka Profile/Settings
2. Change Password
3. Gunakan password yang kuat!

### **2. Hapus Admin Superuser**

Setelah create owner1, hapus user admin superuser:

```sql
DELETE FROM auth_user WHERE username = 'admin';
```

### **3. Restrict Django Admin Access**

Di production, **jangan expose** `/admin` ke public!

Tambahkan di `settings.py` atau nginx config:
```python
# Only allow admin panel for specific IPs
ALLOWED_ADMIN_IPS = ['your-ip-address']
```

### **4. Use Strong Passwords**

Password yang baik:
- ✅ Minimal 12 karakter
- ✅ Mix huruf besar, kecil, angka, simbol
- ✅ Tidak mudah ditebak
- ❌ Jangan: `admin123`, `password`, `12345678`

### **5. Monitor Login Attempts**

Aplikasi sudah pakai `django-axes` untuk:
- ✅ Block brute force attacks
- ✅ Lock account setelah 5 kali login gagal
- ✅ Cooldown 30 menit

### **6. HTTPS Only**

Vercel sudah provide HTTPS otomatis, pastikan:
- ✅ Selalu akses via `https://`
- ❌ Jangan akses via `http://`

---

## 📊 User Access Matrix

| Feature | Owner | Manager | Kasir | Shop User |
|---------|:-----:|:-------:|:-----:|:---------:|
| Warehouse View | ✅ | ✅ | ❌ | ❌ |
| Warehouse Edit | ✅ | ✅ | ❌ | ❌ |
| Shop View | ✅ | ✅ | ✅ | ✅ |
| Shop Edit | ✅ | ✅ | ❌ | ❌ |
| Transfer Items | ✅ | ✅ | ✅ | ✅ |
| Reports | ✅ | ✅ | ❌ | ❌ |
| Excel Import | ✅ | ✅ | ❌ | ❌ |
| Settings | ✅ | ✅ | ❌ | ❌ |
| Django Admin | ✅ | ✅ | ❌ | ❌ |

---

## 🆘 Troubleshooting

### ❌ "Permission Denied" saat login
**Solusi**: User belum masuk group yang benar. Verify dengan query:
```sql
SELECT u.username, g.name 
FROM auth_user u
JOIN auth_user_groups ug ON u.id = ug.user_id
JOIN auth_group g ON ug.group_id = g.id
WHERE u.username = 'owner1';
```

### ❌ Lupa password
**Reset via SQL**:
```python
# Generate password hash baru
python generate_password_hash.py
```

Lalu update di database:
```sql
UPDATE auth_user 
SET password = 'pbkdf2_sha256$...' 
WHERE username = 'owner1';
```

---

## 📞 Summary

**Untuk production yang aman**:
1. ✅ Create user `owner1` dengan role `owners`
2. ✅ Login dengan owner1
3. ✅ Test semua fitur
4. ✅ Ganti password default
5. ✅ Hapus user `admin` superuser
6. ✅ Create user lain sesuai kebutuhan (manager, kasir)

**Default Credentials** (⚠️ GANTI setelah login!):
- Owner: `owner1` / `owner123`
- Manager: `manager1` / `manager123`
- Kasir: `kasir1` / `kasir123`

---

**File ini hanya untuk referensi lokal. Jangan commit ke GitHub!** 🔐
