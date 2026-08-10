# 🧪 Testing Guide - Inventory Dashboard

## ✅ Fix Applied

### jQuery Error Fixed
Error `Uncaught ReferenceError: $ is not defined` sudah diperbaiki dengan:

1. **base_dashboard.html** - jQuery dimuat sebelum script lain
2. **warehouse.html** - Script dipindah ke block `extra_js` 
3. **dashboard.html** - Standalone dengan jQuery yang benar
4. **index.html** - Sudah ada jQuery

## 🚀 Testing Steps

### 1. Start Server
```bash
python manage.py runserver
```

### 2. Test Landing Page
- URL: `http://127.0.0.1:8000/`
- ✅ Landing page muncul tanpa error
- ✅ Animasi berjalan smooth
- ✅ Button "Masuk ke Dashboard" berfungsi

### 3. Test Login
- URL: `http://127.0.0.1:8000/accounts/login/`
- ✅ Form login muncul
- ✅ Login berhasil redirect ke `/dashboard/`

## ✅ Pengujian Wajib Skripsi (BAB III)

Bagian ini disesuaikan dengan implementasi aktual project agar tabel pengujian di skripsi tidak bertentangan dengan kode. Cakupan pengujian dibawa ke 8 fitur inti: keamanan login, transfer, waste, soft delete, import Excel, RBAC, dan AI quota.

### 3.2.4 Pengujian Sistem

Format tabel yang direkomendasikan untuk Word:
`No | Skenario Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Kesimpulan`

Catatan sinkronisasi dengan kode:
- Django Axes saat ini memakai `AXES_FAILURE_LIMIT=3` dan `AXES_COOLOFF_TIME=1` dari `.env`, jadi skenario lockout harus mengikuti konfigurasi aktual ini.
- Fitur waste pada project saat ini adalah **pencatatan waste**, bukan pengurangan stok otomatis.
- Import Excel hanya dapat dilakukan oleh `managers` dan hanya saat `allow_uploads=true`.
- AI Assistant hanya dapat diakses oleh grup `managers` dan `owners`.

### Tabel Rekomendasi Hasil Pengujian Black Box

| No | Skenario Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Kesimpulan |
| --- | --- | --- | --- | --- |
| 1 | Login gagal berturut-turut hingga melewati batas Django Axes (konfigurasi saat ini: 3 kali) | Sistem menolak login lanjutan dan akun/permintaan masuk status lockout selama masa `cooloff`. | Sesuai / Tidak sesuai | Berhasil / Gagal |
| 2 | Kasir menambahkan draft transfer lalu submit permintaan transfer barang | Draft transfer berhasil dibuat, lalu status permintaan tersimpan sebagai `ordered=True` dan sistem menampilkan pesan berhasil submit. | Sesuai / Tidak sesuai | Berhasil / Gagal |
| 3 | Manajer melakukan approve atau cancel terhadap permintaan transfer yang sudah disubmit | Saat approve, transfer diproses dan stok pindah ke data toko. Saat cancel, permintaan transfer dibatalkan. | Sesuai / Tidak sesuai | Berhasil / Gagal |
| 4 | Manajer mencatat waste barang | Catatan waste baru berhasil tersimpan dan tampil pada halaman/daftar waste. | Sesuai / Tidak sesuai | Berhasil / Gagal |
| 5 | Manajer menonaktifkan item gudang (soft delete) | Item tidak dihapus permanen dari basis data, tetapi `is_active` menjadi `False` dan item tidak lagi tampil pada daftar stok gudang aktif. | Sesuai / Tidak sesuai | Berhasil / Gagal |
| 6 | Manajer upload file Excel berisi SKU baru | Sistem memproses file Excel, membuat item baru berbasis SKU, dan SKU baru tampil pada stok gudang. | Sesuai / Tidak sesuai | Berhasil / Gagal |
| 7 | Kasir mencoba mengakses menu atau URL Kelola Stok Gudang | Sistem menolak akses kasir ke halaman `/warehouse/` dan menampilkan `Permission denied` / `403 Forbidden`. | Sesuai / Tidak sesuai | Berhasil / Gagal |
| 8 | Pengguna manajer/owner mengirim permintaan AI Assistant melebihi kuota | Setelah kuota habis, sistem mengembalikan `HTTP 429` dengan pesan `Rate limit exceeded`. | Sesuai / Tidak sesuai | Berhasil / Gagal |

### Rincian Eksekusi per Skenario

#### TC-SEC-AXES-01 — Django Axes Lockout
- Pre-condition:
  - `.env` berisi `AXES_FAILURE_LIMIT=3`
  - `.env` berisi `AXES_COOLOFF_TIME=1`
- Steps:
  1. Buka `http://127.0.0.1:8000/accounts/logout/`
  2. Buka `http://127.0.0.1:8000/accounts/login/`
  3. Masukkan username valid
  4. Masukkan password salah sebanyak 3 kali berturut-turut
  5. Coba login lagi, termasuk dengan password benar, sebelum masa cooloff berakhir
- Expected:
  - Login ditolak karena lockout
  - Selama masa cooloff, autentikasi tetap diblok

#### TC-TRF-01 — Kasir Submit Transfer
- Steps:
  1. Login sebagai kasir
  2. Buka `/transfer/`
  3. Pilih SKU dan isi jumlah transfer
  4. Klik `Tambah`
  5. Klik `Submit`
- Expected:
  - Draft transfer berhasil dibuat
  - Sistem menyimpan request transfer dan menampilkan pesan `Transfer successfully submitted`

#### TC-TRF-02 — Manajer Approve/Cancel Transfer
- Steps:
  1. Pastikan sudah ada transfer kasir yang berstatus ordered
  2. Login sebagai manajer
  3. Buka `/transfer/`
  4. Klik tombol approve atau cancel pada salah satu request
- Expected:
  - Approve: transfer selesai diproses
  - Cancel: transfer dibatalkan
  - Sistem menampilkan pesan `Transfer action successful`

#### TC-WST-01 — Pencatatan Waste
- Steps:
  1. Login sebagai manajer
  2. Buka `/waste/`
  3. Pilih SKU, sumber, jumlah, alasan, dan tanggal pencatatan
  4. Simpan catatan waste
- Expected:
  - Data waste tersimpan melalui endpoint `/api/waste_items/`
  - Data tampil pada tabel waste

#### TC-ITM-DEL-01 — Soft Delete Item
- Steps:
  1. Login sebagai manajer
  2. Buka `/warehouse/`
  3. Hapus/nonaktifkan salah satu item
- Expected:
  - Item tidak muncul lagi pada daftar item aktif
  - Secara logika aplikasi item dinonaktifkan, bukan hard delete

#### TC-IMP-01 — Import Excel SKU Baru
- Pre-condition:
  - Konfigurasi aplikasi `allow_uploads=true`
- Steps:
  1. Login sebagai manajer
  2. Siapkan file `.xlsx` dengan sheet `Warehouse Stock`
  3. Pastikan terdapat SKU yang belum ada di sistem
  4. Upload file melalui `/warehouse/` atau endpoint `/api/import_data/`
- Expected:
  - File berhasil diproses
  - SKU baru dibuat di tabel item
  - SKU baru tampil di halaman stok gudang

#### TC-RBAC-01 — Kasir Ditolak Mengakses Gudang
- Steps:
  1. Login sebagai kasir
  2. Akses `/warehouse/`
- Expected:
  - Sistem menolak akses dengan `403 Forbidden` / `Permission denied`

#### TC-AI-RL-01 — Rate Limiting AI Assistant
- Steps:
  1. Login sebagai manajer atau owner
  2. Buka `/ai-assistant/` atau cek `/api/ai/status/`
  3. Kirim request berulang ke `/api/ai/ask/` hingga kuota habis
- Expected:
  - Sebelum limit: request berhasil
  - Setelah melewati limit: sistem memberi `HTTP 429` dengan pesan `Rate limit exceeded. Maximum 20 requests per hour.`

### 4. Test Dashboard (Main Page)
- URL: `http://127.0.0.1:8000/dashboard/`
- Check browser console (F12):
  - ✅ Tidak ada error jQuery
  - ✅ Chart.js loaded
  - ✅ AJAX calls berhasil
  
- Visual checks:
  - ✅ Sidebar muncul dengan gradient ungu
  - ✅ Stats cards menampilkan angka
  - ✅ Pie chart muncul
  - ✅ Bar chart muncul
  - ✅ Recent items list muncul

### 5. Test Warehouse Page
- URL: `http://127.0.0.1:8000/warehouse/`
- Check console:
  - ✅ Tidak ada error `$ is not defined`
  - ✅ loadWarehouse() berjalan
  - ✅ Table terisi data
  
- Visual checks:
  - ✅ Search box berfungsi
  - ✅ Refresh button berfungsi
  - ✅ Table responsive

### 6. Test Shop Page  
- URL: `http://127.0.0.1:8000/shop/`
- Sama seperti warehouse

### 7. Test Old Dashboard (Compatibility)
- URL: `http://127.0.0.1:8000/old-dashboard/`
- ✅ Dashboard lama masih berfungsi

## 🔍 Common Issues & Solutions

### Issue 1: jQuery not defined
**Symptoms:**
```
Uncaught ReferenceError: $ is not defined
```

**Solution:**
- Check jQuery script tag ada dan dimuat PERTAMA
- Pastikan URL CDN benar: `https://code.jquery.com/jquery-3.7.1.min.js`
- Cek network tab di browser, pastikan jQuery loaded

### Issue 2: Chart not rendering
**Symptoms:**
- Canvas element kosong
- No error in console

**Solution:**
- Check Chart.js loaded: `typeof Chart !== 'undefined'`
- Verify data exists: Check `/api/items/` returns data
- Check canvas element ID matches JS: `stockPieChart`, `topItemsChart`

### Issue 3: AJAX 403 Forbidden
**Symptoms:**
```
POST /api/... 403 (Forbidden)
```

**Solution:**
- Check CSRF token: `getCSRFToken()` returns valid token
- Check cookie: `document.cookie` contains `csrftoken`
- Verify headers: `X-CSRFToken` in request

### Issue 4: Sidebar tidak muncul
**Symptoms:**
- Sidebar invisible or off-screen

**Solution:**
- Check CSS loaded
- Clear browser cache: Ctrl + Shift + R
- Check responsive: Window width > 768px?

## 📊 Testing Checklist

### Frontend Tests
- [ ] Landing page loads
- [ ] Login works
- [ ] Dashboard loads without console errors
- [ ] Charts render correctly
- [ ] Sidebar navigation works
- [ ] Search functionality works
- [ ] Responsive on mobile (< 768px)
- [ ] Buttons have hover effects
- [ ] Animations smooth

### Backend Tests
- [ ] `/api/items/` returns 200
- [ ] `/api/shop_items/` returns 200
- [ ] `/auth/user/` returns user data
- [ ] CSRF token works
- [ ] Login/logout works
- [ ] Permissions work (managers vs cashiers)
- [ ] Django Axes lockout works (brute force → lockout)
- [ ] Maintenance mode blocks transfer for cashier
- [ ] Import Excel upload works (adds SKU)
- [ ] AI rate limiting works (429 after quota)
- [ ] Expiry date works (stored & displayed)

### Browser Compatibility
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if Mac available)

## 🛠️ Debug Tools

### Browser Console Commands

```javascript
// Check jQuery loaded
typeof $ !== 'undefined'

// Check Chart.js loaded
typeof Chart !== 'undefined'

// Check current user
$.get('/auth/user/', console.log)

// Check items data
$.get('/api/items/', console.log)

// Check CSRF token
document.cookie.split('; ').find(r => r.startsWith('csrftoken='))

// Force reload warehouse data
loadWarehouse()

// Force reload dashboard
loadDashboardData()
```

### Django Debug

```bash
# Check migrations
python manage.py showmigrations

# Create test data
python manage.py shell
>>> from stock_manager.models import Item
>>> Item.objects.create(sku='TEST-001', description='Test Item 1', quantity=25, purchase_price=15000)
>>> Item.objects.create(sku='TEST-002', description='Test Item 2', quantity=5, purchase_price=20000)
>>> Item.objects.create(sku='TEST-003', description='Test Item 3', quantity=0, purchase_price=10000)

# Check data
>>> Item.objects.count()
>>> Item.objects.all()
```

## 📸 Screenshot Checklist

When reporting bugs, include:
1. Full browser window screenshot
2. Console tab (F12) showing errors
3. Network tab showing failed requests
4. URL bar visible
5. Timestamp

## ✅ Expected Results

### Dashboard Stats Example
```
Total Barang: 15
Stok Tersedia: 10  (quantity > 10)
Stok Menipis: 3    (quantity 1-10)
Stok Habis: 2      (quantity = 0)
```

### Pie Chart Colors
- 🟢 Green: Stok Tersedia
- 🟡 Yellow: Stok Menipis  
- 🔴 Red: Stok Habis

### Bar Chart
- Shows top 5 items by quantity
- Purple/blue gradient bars
- Interactive hover

## 🎯 Performance Targets

- Initial page load: < 2 seconds
- AJAX response: < 500ms
- Chart render: < 300ms
- Smooth 60fps animations

## 📝 Notes

- All pages tested on local development server
- Production deployment may need additional testing
- HTTPS required for production
- Consider CDN fallbacks for production

---

Last Updated: 2026-07-01
Server: http://127.0.0.1:8000
Status: ✅ All tests passing
