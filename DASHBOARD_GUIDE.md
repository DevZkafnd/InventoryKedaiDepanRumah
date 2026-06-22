# 📊 Dashboard Guide - Inventory System

## ✨ Fitur Baru Dashboard

Dashboard baru sudah dilengkapi dengan:

### 🎨 UI/UX Features
- ✅ **Sidebar Navigation** - Menu samping dengan icon yang jelas
- ✅ **Multi-Page Layout** - Halaman terpisah untuk setiap fitur
- ✅ **Responsive Design** - Sidebar collapse di mobile
- ✅ **Modern Design** - Gradient colors, shadows, smooth animations

### 📈 Analytics & Charts
- ✅ **Pie Chart** - Distribusi stok (Tersedia/Menipis/Habis)
- ✅ **Bar Chart** - Top 5 barang dengan stok terbanyak
- ✅ **Stats Cards** - Total barang, stok tersedia, menipis, habis
- ✅ **Recent Items** - List barang terbaru

### 📱 Pages
1. **Dashboard** (`/dashboard/`) - Analytics & overview
2. **Stok Gudang** (`/warehouse/`) - Manage warehouse inventory
3. **Stok Toko** (`/shop/`) - Shop inventory
4. **Transfer** - Transfer items (coming soon)
5. **Laporan** - Reports (coming soon)
6. **AI Assistant** - AI-powered insights (integrated)

## 🚀 Cara Menjalankan

### 1. Pastikan Server Berjalan
```bash
python manage.py runserver
```

### 2. Buka Browser
Kunjungi: **http://127.0.0.1:8000**

### 3. Flow Aplikasi
1. **Landing Page** - Halaman pertama dengan design menarik
2. Klik **"Masuk ke Dashboard"**
3. **Login** dengan username/password
4. **Dashboard** - Langsung melihat analytics

## 📊 Menggunakan Dashboard

### Stats Cards
Menampilkan 4 metrik penting:
- **Total Barang** - Jumlah total item
- **Stok Tersedia** - Barang dengan stok > 10
- **Stok Menipis** - Barang dengan stok 1-10
- **Stok Habis** - Barang dengan stok 0

### Charts

#### Pie Chart (Doughnut)
- Visualisasi distribusi stok dalam bentuk lingkaran
- Warna:
  - 🟢 Hijau = Stok Tersedia
  - 🟡 Kuning = Stok Menipis
  - 🔴 Merah = Stok Habis

#### Bar Chart
- Menampilkan 5 barang teratas
- Sorted by quantity
- Interactive hover effect

### Recent Items
- List 5 barang terbaru
- Icon status:
  - ✅ = Stok Tersedia (> 10)
  - ⚠️ = Stok Menipis (1-10)
  - ❌ = Stok Habis (0)

## 🎨 Teknologi Charts

Menggunakan **Chart.js v4.4.0** - Library charting yang:
- ✅ Lightweight & fast
- ✅ Responsive & mobile-friendly
- ✅ Beautiful default styling
- ✅ Interactive & animated
- ✅ Open source & free

## 🔧 Kustomisasi

### Mengubah Warna Chart

Edit di `dashboard.html` bagian `createPieChart()`:

```javascript
backgroundColor: ['#10b981', '#f59e0b', '#ef4444']
```

### Mengubah Jumlah Item di Bar Chart

Edit di `loadDashboardData()`:

```javascript
createBarChart(items.slice(0, 5)); // Ubah 5 menjadi angka lain
```

### Mengubah Threshold Stok

Edit di `loadDashboardData()`:

```javascript
const inStock = items.filter(i => i.quantity > 10).length; // Ubah 10
const lowStock = items.filter(i => i.quantity > 0 && i.quantity <= 10).length; // Ubah 10
```

## 📱 Responsive Behavior

### Desktop (> 768px)
- Sidebar visible (260px width)
- Main content margin-left: 260px
- Full charts displayed

### Mobile (≤ 768px)
- Sidebar hidden by default
- Toggle button appears
- Charts stack vertically
- Stats cards in single column

## 🎯 Next Steps

Dashboard sudah siap digunakan! Berikutnya bisa:
1. ✅ Tambah data dummy untuk testing charts
2. ✅ Customize colors & branding
3. ✅ Add more chart types (line chart, area chart)
4. ✅ Implement real-time updates
5. ✅ Add export chart as image feature

## 💡 Tips

1. **Data Dummy untuk Testing**
   ```bash
   python manage.py shell
   from stock_manager.models import Item
   Item.objects.create(sku='TEST-001', description='Test Item', quantity=15, purchase_price=10000)
   ```

2. **Clear Cache Browser**
   - Ctrl + Shift + R (Chrome/Firefox)
   - Untuk reload CSS & JS terbaru

3. **Inspect Charts**
   - Right click chart > Inspect
   - Check console for Chart.js errors

## 🐛 Troubleshooting

### Chart tidak muncul?
1. Cek console browser (F12)
2. Pastikan Chart.js loaded: `typeof Chart !== 'undefined'`
3. Cek data API: `/api/items/` harus return data

### Sidebar tidak responsive?
1. Cek window width: `window.innerWidth`
2. Force reload: Ctrl + Shift + R

### Stats tidak update?
1. Clear browser cache
2. Refresh data: Click refresh button
3. Check API endpoint

---

**Made with ❤️ using Django + Chart.js**
