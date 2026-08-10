# 🔐 Permission Matrix - Role & Access Control

## 📊 Tabel Akses Per Role

| Menu/Fitur | managers (admin) | owners (owner1) | cashiers (kasir1) |
|------------|------------------|-----------------|-------------------|
| **Dashboard** | ✅ Full Access | ✅ Read-only | ❌ No Access |
| **Warehouse** | ✅ Full Access | ❌ No Access | ❌ No Access |
| **Shop** | ✅ Full Access | ❌ No Access | ✅ Own Shop Only |
| **Transfer** | ✅ Approve/Manage | ❌ No Access | ✅ Request Only |
| **Reports** | ✅ Full Access | ✅ Read-only | ❌ No Access |
| **Waste** | ✅ Create/View | ✅ Read-only | ❌ No Access |
| **AI Assistant** | ❌ No Access | ✅ Full Access | ❌ No Access |

---

## 👥 Detail Permission Per Role

### **1. managers (Admin - admin)**

**Philosophy:** Operational manager yang mengelola inventory harian

**Full Access:**
- ✅ Dashboard - Analytics lengkap
- ✅ Warehouse - Manage semua item gudang (CRUD)
- ✅ Shop - Lihat stok semua toko
- ✅ Transfer - Approve transfer request dari kasir
- ✅ Reports - Import/Export Excel
- ✅ Waste - Catat barang rusak/expired

**Cannot Access:**
- ❌ AI Assistant - Hanya untuk owner/strategic analysis

**Use Cases:**
- Update stok gudang setiap hari
- Approve transfer request dari kasir
- Input data barang baru
- Generate laporan untuk owner
- Catat waste/barang rusak

---

### **2. owners (Owner - owner1)**

**Philosophy:** Business owner yang fokus pada strategic oversight

**Read-Only Access:**
- ✅ Dashboard - Lihat analytics & trends (tidak bisa edit)
- ✅ Reports - Download laporan untuk analisis (tidak bisa import)
- ✅ Waste - Monitor waste untuk kontrol biaya (tidak bisa create)

**Full Access:**
- ✅ AI Assistant - Natural language analytics dengan AI

**Cannot Access:**
- ❌ Warehouse - Tidak manage inventory langsung
- ❌ Shop - Tidak manage toko kasir
- ❌ Transfer - Tidak handle operational transfer

**Use Cases:**
- Monitor performa bisnis via dashboard
- Analisa trends dengan AI Assistant
- Download laporan untuk strategic planning
- Monitor waste & losses
- High-level oversight tanpa operational details

---

### **3. cashiers/shop_users (Kasir - kasir1)**

**Philosophy:** Front-line staff yang manage stok toko sendiri

**Full Access:**
- ✅ Shop - Manage stok toko sendiri (lihat & update quantity)
- ✅ Transfer - Request barang dari warehouse

**Cannot Access:**
- ❌ Dashboard - Tidak perlu lihat analytics
- ❌ Warehouse - Tidak akses gudang
- ❌ Reports - Tidak generate laporan
- ❌ Waste - Tidak catat waste (manajer yang handle)
- ❌ AI Assistant - Tidak perlu strategic analysis

**Use Cases:**
- Cek stok toko sendiri
- Update quantity setelah jual barang
- Request transfer dari warehouse jika stok habis
- Lihat pending transfer requests

---

## 🔒 Perubahan yang Sudah Diterapkan

### **Sebelum (SALAH):**
```javascript
// Shop & Transfer tampil untuk semua role
setVisible('#menuShop', isCashier || isManager || isOwner);  // ❌ Owner ga boleh!
setVisible('#menuTransfer', isCashier || isManager || isOwner);  // ❌ Owner ga boleh!
setVisible('#menuAI', isManager || isOwner);  // ❌ Manager ga boleh!
```

**Masalah:**
- Owner bisa klik menu Shop/Transfer → Error 403
- Manager bisa klik AI Assistant → Error 403
- UX buruk: menu tampil tapi tidak bisa diakses

---

### **Sesudah (BENAR):**
```javascript
// Menu hanya tampil jika user punya akses
setVisible('#menuDashboard', isManager || isOwner);
setVisible('#menuWarehouse', isManager); // Only managers
setVisible('#menuShop', isCashier || isManager); // Only cashiers & managers
setVisible('#menuTransfer', isCashier || isManager); // Only cashiers & managers
setVisible('#menuReports', isManager || isOwner); // Managers & owners
setVisible('#menuWaste', isManager || isOwner); // Managers & owners
setVisible('#menuAI', isOwner); // Only owners
```

**Benefit:**
- ✅ Menu yang tidak boleh diakses **tidak tampil** di sidebar
- ✅ Tidak ada error 403 lagi
- ✅ UX lebih bersih dan jelas
- ✅ User hanya lihat fitur yang relevan untuk role mereka

---

## 📝 Backend Permission Check (views.py)

Backend sudah implement permission check di setiap view:

### **Dashboard** (managers + owners):
```python
@login_required
def dashboard(request):
    if request.user.groups.filter(name="cashiers").exists() or request.user.groups.filter(name="shop_users").exists():
        return redirect("shop")
    
    if not (request.user.groups.filter(name="managers").exists() or request.user.groups.filter(name="owners").exists()):
        return HttpResponseForbidden("Permission denied.")
```

### **Warehouse** (managers only):
```python
@login_required
def warehouse(request):
    if not request.user.groups.filter(name="managers").exists():
        return HttpResponseForbidden("Permission denied. Warehouse is for managers only.")
```

### **Shop** (cashiers + managers):
```python
@login_required
def shop(request):
    if not (request.user.groups.filter(name="cashiers").exists() or request.user.groups.filter(name="shop_users").exists() or request.user.groups.filter(name="managers").exists()):
        return HttpResponseForbidden("Permission denied. Shop is for cashiers and managers only.")
```

### **AI Assistant** (owners only):
```python
@login_required
def ai_assistant(request):
    if not request.user.groups.filter(name="owners").exists():
        return HttpResponseForbidden("Permission denied. AI Assistant is for owners only.")
```

---

## 🧪 Testing Permission

Setelah perubahan ini, test dengan 3 user:

### **Test dengan admin (managers):**
```
Login: admin / admin123
Sidebar Menu yang tampil:
✅ Dashboard
✅ Warehouse
✅ Shop
✅ Transfer
✅ Reports
✅ Waste
❌ AI Assistant (hidden)
```

### **Test dengan owner1 (owners):**
```
Login: owner1 / owner123
Sidebar Menu yang tampil:
✅ Dashboard
✅ Reports
✅ Waste
✅ AI Assistant
❌ Warehouse (hidden)
❌ Shop (hidden)
❌ Transfer (hidden)
```

### **Test dengan kasir1 (cashiers):**
```
Login: kasir1 / kasir123
Sidebar Menu yang tampil:
✅ Shop
✅ Transfer
❌ Dashboard (hidden)
❌ Warehouse (hidden)
❌ Reports (hidden)
❌ Waste (hidden)
❌ AI Assistant (hidden)
```

---

## 🎯 Summary

**Prinsip:**
- ✅ Frontend (sidebar) = Backend (views.py) permission
- ✅ Kalau tidak boleh akses, **jangan tampilkan menu**
- ✅ Tidak ada lagi error 403 karena klik menu yang tidak boleh

**Files yang diupdate:**
- ✅ `templates/dashboard.html` - applyMenuVisibility()
- ✅ `templates/base_dashboard.html` - applyMenuVisibility()

**Result:**
- ✅ UX lebih bersih
- ✅ User tidak bingung
- ✅ Tidak ada error 403 lagi
- ✅ Setiap role hanya lihat fitur yang relevan

---

**🎉 Permission matrix sudah benar dan konsisten antara frontend & backend!**
