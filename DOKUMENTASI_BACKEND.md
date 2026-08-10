# 🔧 Dokumentasi Backend - Inventory Kedai Depan Rumah

## Daftar Isi
- [Arsitektur Backend](#arsitektur-backend)
- [Struktur Django Project](#struktur-django-project)
- [Models (Database Layer)](#models-database-layer)
- [Views (Business Logic)](#views-business-logic)
- [Serializers (Data Transformation)](#serializers-data-transformation)
- [URL Routing](#url-routing)
- [API Endpoints](#api-endpoints)
- [Authentication & Authorization](#authentication--authorization)
- [Security Features](#security-features)
- [AI Service](#ai-service)
- [Email Service](#email-service)
- [Utilities](#utilities)

---

## Arsitektur Backend

Sistem ini menggunakan **Django 6.0.5** dengan **Django REST Framework 3.17.1** untuk API.

### Stack Teknologi

```
┌─────────────────────────────────────────────┐
│           Frontend (HTML/JS)                 │
│   Landing, Dashboard, Warehouse, dll        │
└──────────────────┬──────────────────────────┘
                   │ HTTP Request/Response
                   │ (AJAX/Fetch API)
┌──────────────────┴──────────────────────────┐
│        Django REST Framework (DRF)           │
│     API Endpoints + Serializers              │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────┴──────────────────────────┐
│           Django Views Layer                 │
│  Business Logic + Authorization Checks       │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────┴──────────────────────────┐
│         Django ORM (Models)                  │
│    Database Abstraction Layer                │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────┴──────────────────────────┐
│            SQLite Database                   │
│         (db.sqlite3)                         │
└──────────────────────────────────────────────┘
```

### Pola Arsitektur: MVC/MTV

Django menggunakan **MTV** (Model-Template-View) pattern:

- **Model**: Definisi struktur database (`models.py`)
- **Template**: HTML templates (`templates/`)
- **View**: Business logic (`views.py`)

---

## Struktur Django Project

### Project Structure

```
inventory-kedai-depan-rumah/
│
├── ssm/                    # Django project settings
│   ├── __init__.py
│   ├── settings.py        # ⚙️ Konfigurasi utama
│   ├── urls.py            # 🔗 URL routing utama
│   └── wsgi.py            # 🚀 WSGI untuk deployment
│
├── stock_manager/         # 📦 Main app (inventory logic)
│   ├── models.py          # 📊 Database models
│   ├── views.py           # 🎯 Business logic
│   ├── serializers.py     # 🔄 Data serialization
│   ├── urls.py            # 🔗 App URL routing
│   ├── pagination.py      # 📄 Custom pagination
│   ├── utils.py           # 🛠️ Helper functions
│   └── admin.py           # 👑 Django admin config
│
├── ai_service/            # 🤖 AI Assistant
│   ├── views.py           # AI API endpoints
│   ├── groq_client.py     # Groq API client
│   ├── middleware.py      # Security middleware
│   └── urls.py            # AI URL routing
│
├── email_service/         # 📧 Email notifications
│   └── email.py           # Email sending logic
│
├── templates/             # 📄 HTML templates
│   ├── landing.html
│   ├── dashboard.html
│   ├── warehouse.html
│   └── ...
│
└── manage.py              # Django management script
```

---

## Models (Database Layer)

File: `stock_manager/models.py`

### Overview

Models adalah representasi Python dari tabel database. Django ORM otomatis convert ke SQL.

### Model: Item (Barang Gudang)

```python
class Item(models.Model):
    # Primary Key - SKU (Stock Keeping Unit)
    sku = models.CharField(
        primary_key=True,      # Ini adalah PK, bukan auto-increment
        unique=True,           # Harus unik
        editable=True,         # Bisa diedit
        max_length=100         # Maksimal 100 karakter
    )
    
    # Deskripsi barang
    description = models.CharField(max_length=250)
    
    # Harga beli - Decimal untuk akurasi uang
    purchase_price = models.DecimalField(
        max_digits=10,         # Total 10 digit
        decimal_places=2       # 2 digit di belakang koma (contoh: 12345678.99)
    )
    
    # Jumlah stok
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)]  # Minimum 0, tidak boleh negatif
    )
    
    # Tanggal kadaluarsa (opsional)
    expiry_date = models.DateField(
        null=True,             # Boleh NULL
        blank=True             # Boleh kosong di form
    )
    
    # Timestamp otomatis saat update
    last_updated = models.DateTimeField(auto_now=True)
    
    # Soft delete flag
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        """String representation di Django Admin"""
        return f"{self.sku} ({'Active' if self.is_active else 'Inactive'})"
    
    def save(self, *args, **kwargs):
        """
        Custom save method - validasi purchase_price
        
        Proses:
        1. Convert purchase_price ke Decimal
        2. Bulatkan ke 2 desimal (ROUND_HALF_UP)
        3. Validasi format dengan regex
        4. Jika valid, simpan
        5. Jika tidak, raise ValueError
        """
        try:
            dec = Decimal(self.purchase_price)
        except (InvalidOperation, TypeError, ValueError):
            raise ValueError("Purchase price must be a valid number.")
        
        # Bulatkan ke 2 desimal
        dec = dec.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
        # Validasi format (harus digit dan maks 2 desimal)
        dec_str = format(dec, 'f')  # Fixed-point notation (hindari scientific notation)
        if not re.match(r"^\d+(\.\d{1,2})?$", dec_str):
            raise ValueError(
                "Purchase price must be a valid number with up to 2 decimal places."
            )
        
        self.purchase_price = dec
        super().save(*args, **kwargs)
```

**Penjelasan Per Baris:**

- **Line 2-7**: Field `sku` sebagai Primary Key (bukan ID auto-increment seperti biasa)
- **Line 10**: Deskripsi barang, maksimal 250 karakter
- **Line 13-17**: `DecimalField` untuk harga (lebih akurat daripada FloatField untuk uang)
- **Line 20-22**: Quantity dengan validator minimal 0
- **Line 25-28**: Tanggal kadaluarsa opsional
- **Line 31**: Auto-update timestamp saat save()
- **Line 34**: Soft delete flag (tidak hapus fisik dari database)
- **Line 36-38**: Method `__str__` untuk representasi objek
- **Line 40-67**: Method `save()` custom untuk validasi harga

---

### Model: ShopItem (Barang Toko)

```python
class ShopItem(models.Model):
    # Foreign Key ke User (kasir)
    shop_user = models.ForeignKey(
        User,                  # Django built-in User model
        on_delete=models.CASCADE  # Jika user dihapus, ShopItem ikut dihapus
    )
    
    # Foreign Key ke Item
    item = models.ForeignKey(
        Item,
        on_delete=models.SET_NULL,  # Jika item dihapus, set NULL (data shop tetap ada)
        null=True,
        blank=True
    )
    
    # Quantity di toko kasir ini
    quantity = models.IntegerField(default=0)
    
    # Timestamp otomatis
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        # Constraint: satu kasir + satu item = maksimal 1 record
        unique_together = ("shop_user", "item")
    
    def __str__(self):
        return f"{self.shop_user.username} - {self.item.sku if self.item else 'Item Deleted'}"
```

**Penjelasan:**

- **Foreign Key `on_delete` Options:**
  - `CASCADE`: Jika parent dihapus, child ikut dihapus
  - `SET_NULL`: Jika parent dihapus, foreign key jadi NULL
  - `PROTECT`: Tidak bisa hapus parent jika ada child
- **Meta.unique_together**: Constraint database untuk mencegah duplikat

---

### Model: TransferItem (Transfer Request)

```python
class TransferItem(models.Model):
    # FK ke User (kasir yang request)
    shop_user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # FK ke Item
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    
    # Jumlah yang direquest
    quantity = models.IntegerField(default=0)
    
    # Status: False = draft, True = sudah submit
