# 📘 Dokumentasi Singkat - Inventory Kedai Depan Rumah

## 🎯 Overview Sistem

Ini adalah sistem inventory management berbasis web menggunakan Django + JavaScript dengan fitur:
- Manajemen stok gudang & toko
- Transfer barang antar gudang-toko  
- AI Assistant (Groq/Llama)
- Laporan & Export Excel
- Role-based access (Owner, Manajer, Kasir)

---

## 📊 DATABASE

### Tabel Utama:

**1. Item (Barang Gudang)**
```python
- sku (PK, VARCHAR 100) - Kode barang unik
- description (VARCHAR 250) - Nama barang
- purchase_price (DECIMAL 10,2) - Harga beli
- quantity (INT) - Stok gudang
- expiry_date (DATE, nullable) - Tanggal kadaluarsa
- is_active (BOOL) - Soft delete flag
- last_updated (DATETIME) - Auto update
```

**2. ShopItem (Barang Toko)**
```python
- id (PK, INT) - Auto increment
- shop_user_id (FK → User) - Kasir pemilik
- item_id (FK → Item.sku) - Barang
- quantity (INT) - Stok di toko kasir ini
- last_updated (DATETIME)

UNIQUE (shop_user_id, item_id) - 1 kasir + 1 barang = max 1 record
```

**3. TransferItem (Permintaan Transfer)**
```python
- id (PK, INT)
- shop_user_id (FK → User) - Kasir yang request
- item_id (FK → Item.sku) - Barang
- quantity (INT) - Jumlah diminta
- ordered (BOOL) - False=draft, True=submit
- created_at (DATETIME)
- last_updated (DATETIME)
```

**4. WasteItem (Barang Rusak)**
```python
- id (PK, INT)
- item_id (FK → Item.sku, PROTECT)
- shop_user_id (FK → User, nullable)
- source (VARCHAR 20) - 'warehouse' atau 'shop'
- quantity (INT) - Jumlah rusak
- reason (VARCHAR 255) - Alasan
- recorded_at (DATE)
```

**5. Admin (Konfigurasi App)**
```python
- id (PK, INT) - Always 1 (singleton)
- edit_lock (BOOL) - Maintenance mode
- allow_uploads (BOOL) - Izinkan upload Excel
- allow_upload_deletions (BOOL) - Hapus data saat upload
- allow_email_notifications (BOOL)
- records_per_page (INT) - Pagination

Akses: Admin.get_solo()
```

---

## 🔧 BACKEND (Django)

### Struktur File Penting:

```
stock_manager/
├── models.py       # Database models
├── views.py        # Business logic + API
├── serializers.py  # JSON transformation
├── urls.py         # URL routing
├── utils.py        # Helper functions
└── pagination.py   # Custom pagination

ai_service/
├── views.py        # AI API endpoints
├── groq_client.py  # Groq API client
└── middleware.py   # Security

ssm/
├── settings.py     # Django config
└── urls.py         # Main routing
```

### Models.py - Contoh Item Model

```python
class Item(models.Model):
    sku = models.CharField(primary_key=True, max_length=100)
    description = models.CharField(max_length=250)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    expiry_date = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        # Validasi purchase_price ke 2 desimal
        dec = Decimal(self.purchase_price)
        dec = dec.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.purchase_price = dec
        super().save(*args, **kwargs)
```

### Views.py - Contoh ItemViewSet

```python
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.filter(is_active=True)
    serializer_class = ItemSerializer
    lookup_field = "sku"  # Gunakan SKU bukan ID
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        # Cek permission: hanya manager & owner
        user = self.request.user
        if not (user.groups.filter(name="managers").exists() or
                user.groups.filter(name="owners").exists()):
            raise PermissionDenied("Permission denied.")
        
        queryset = Item.objects.filter(is_active=True)
        
        # Search filter
        search_query = self.request.query_params.get("search", None)
        if search_query:
            queryset = queryset.filter(
                Q(description__icontains=search_query) | 
                Q(sku__icontains=search_query)
            )
        
        # Ordering
        ordering = self.request.query_params.get("ordering", None)
        if ordering:
            if ordering == "sku":
                items = list(queryset)
                items = natsorted(items, key=lambda x: x.sku)
                return items
            queryset = queryset.order_by(Lower(ordering))
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        # Cek permission: hanya manager
        if not request.user.groups.filter(name="managers").exists():
            return Response({"detail": "Permission denied."}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # Cek jika SKU sudah ada tapi inactive → reactivate
        sku = request.data.get("sku")
        if sku:
            try:
                item = Item.objects.get(sku=sku)
                if not item.is_active:
                    serializer = ItemSerializer(item, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save(is_active=True)
                        return Response(serializer.data, status=200)
            except Item.DoesNotExist:
                pass
        
        return super().create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        # Soft delete - set is_active = False
        sku = kwargs.get("sku")
        try:
            item = Item.objects.get(sku=sku)
            item.is_active = False
            item.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            return Response({"error": "Item not found."}, status=404)
```

### Serializers.py

```python
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["sku", "description", "purchase_price", 
                  "quantity", "expiry_date"]
    
    def validate_quantity(self, value):
        # Validasi quantity harus integer
        if not re.match(r"^\d+$", str(value)):
            raise serializers.ValidationError("Quantity must be integer.")
        return int(value)
    
    def validate_purchase_price(self, value):
        # Validasi price format (max 2 desimal)
        if not re.match(r"^\d+(\.\d{1,2})?$", str(value)):
            raise serializers.ValidationError("Invalid price format.")
        return float(value)
```

---

## 🎨 FRONTEND (HTML/JS)

### Struktur Template:

```
templates/
├── landing.html              # Public landing page
├── base_dashboard.html       # Base template (sidebar+topbar)
├── dashboard.html            # Dashboard (stats + charts)
├── warehouse.html            # Gudang (tabel items)
├── shop.html                 # Toko kasir
├── transfer.html             # Transfer management
├── reports.html              # Laporan & export
├── waste.html                # Waste management
└── ai_assistant.html         # AI chatbot
```

### Landing Page (landing.html)

```html
<!-- Hero Section dengan Grid 2 kolom -->
<div class="hero-section">
    <!-- Left: Text + CTA -->
    <div class="hero-content">
        <div class="logo-container">
            <img src="{% static 'img/logo-black.png' %}">
            <div class="logo-text">Kedai Depan Rumah</div>
        </div>
        <h1>Kelola Inventory dengan Mudah & Cerdas</h1>
        <p class="subtitle">Sistem manajemen inventory modern...</p>
        
        <!-- Feature Icons -->
        <div class="features">
            <div class="feature-item">
                <div class="feature-icon">📊</div>
                <div class="feature-text">Tracking Real-time</div>
            </div>
            <!-- 3 items lainnya... -->
        </div>
        
        <a href="/accounts/login/" class="cta-button">Login →</a>
    </div>
    
    <!-- Right: Illustration -->
    <div class="hero-image">
        <div class="card-illustration">
            <div class="ai-badge">✨ AI Powered</div>
            <div class="card-stack">
                <!-- 3 floating cards dengan animasi -->
            </div>
        </div>
    </div>
</div>
```

### Dashboard (dashboard.html)

**Stats Cards:**
```html
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-icon blue">
            <i class="bi bi-box-seam"></i>
        </div>
        <div class="stat-details">
            <h3 id="totalItems">0</h3>
            <p>Total Barang</p>
        </div>
    </div>
    <!-- 3 cards lainnya: Stok Tersedia, Menipis, Habis -->
</div>
```

**Charts (Chart.js):**
```javascript
// Pie Chart - Distribusi Stok
function createPieChart(inStock, lowStock, outOfStock) {
    const ctx = document.getElementById('stockPieChart');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Stok Tersedia', 'Stok Menipis', 'Stok Habis'],
            datasets: [{
                data: [inStock, lowStock, outOfStock],
                backgroundColor: ['#10b981', '#555555', '#000000']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// Bar Chart - Top 5 Barang
function createBarChart(items) {
    const ctx = document.getElementById('topItemsChart');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: items.map(item => item.sku),
            datasets: [{
                label: 'Jumlah Stok',
                data: items.map(item => item.quantity),
                backgroundColor: 'rgba(16, 185, 129, 0.8)'
            }]
        }
    });
}
```

### JavaScript - AJAX Pattern

**1. Get CSRF Token:**
```javascript
function getCSRFToken() {
    const cookie = document.cookie.split('; ')
        .find(r => r.startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
}
```

**2. Load Items:**
```javascript
function loadItems() {
    $.ajax({
        url: '/api/items/',
        method: 'GET',
        data: {
            page: 1,
            page_size: 25,
            search: searchQuery,
            ordering: '-quantity'  // descending by quantity
        },
        success: function(data) {
            renderItems(data.results);
            renderPagination(data);
        },
        error: function(xhr) {
            alert('Error: ' + xhr.responseJSON.detail);
        }
    });
}
```

**3. Create Item:**
```javascript
function createItem(itemData) {
    $.ajax({
        url: '/api/items/',
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken() },
        contentType: 'application/json',
        data: JSON.stringify(itemData),
        success: function(data) {
            alert('Item berhasil ditambahkan!');
            loadItems();
        },
        error: function(xhr) {
            alert('Error: ' + xhr.responseJSON.detail);
        }
    });
}
```

**4. Update Item:**
```javascript
function updateItem(sku, updatedData) {
    $.ajax({
        url: `/api/items/${sku}/`,
        method: 'PATCH',
        headers: { 'X-CSRFToken': getCSRFToken() },
        contentType: 'application/json',
        data: JSON.stringify(updatedData),
        success: function(data) {
            alert('Item berhasil diupdate!');
            loadItems();
        }
    });
}
```

**5. Delete Item (Soft Delete):**
```javascript
function deleteItem(sku) {
    if (!confirm('Yakin ingin menghapus?')) return;
    
    $.ajax({
        url: `/api/items/${sku}/`,
        method: 'DELETE',
        headers: { 'X-CSRFToken': getCSRFToken() },
        success: function() {
            alert('Item berhasil dihapus!');
            loadItems();
        }
    });
}
```

**6. Render Table:**
```javascript
function renderItems(items) {
    const tbody = $('#itemTableBody');
    tbody.empty();
    
    if (items.length === 0) {
        tbody.html('<tr><td colspan="6" class="text-center">Tidak ada data</td></tr>');
        return;
    }
    
    items.forEach(item => {
        const row = `
            <tr>
                <td>${escapeHtml(item.sku)}</td>
                <td>${escapeHtml(item.description)}</td>
                <td>Rp ${formatNumber(item.purchase_price)}</td>
                <td>${item.quantity}</td>
                <td>${formatDate(item.expiry_date)}</td>
                <td>
                    <button class="btn btn-sm btn-primary btn-edit" 
                            data-sku="${item.sku}">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-danger btn-delete" 
                            data-sku="${item.sku}">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        `;
        tbody.append(row);
    });
}

// Helper functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatNumber(num) {
    return Number(num).toLocaleString('id-ID');
}

function formatDate(dateStr) {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleDateString('id-ID');
}
```

---

## 🔐 AUTHENTICATION & AUTHORIZATION

### User Groups (Roles):

1. **owners** - Lihat semua, tidak bisa edit
2. **managers** - Full access (CRUD semua)
3. **cashiers / shop_users** - Lihat stok toko sendiri + request transfer

### Permission Check di Views:

```python
# Cek apakah user adalah manager
if not request.user.groups.filter(name="managers").exists():
    return Response({"detail": "Permission denied."}, status=403)

# Cek apakah user adalah manager atau owner
if not (request.user.groups.filter(name="managers").exists() or
        request.user.groups.filter(name="owners").exists()):
    return HttpResponseForbidden("Permission denied.")

# Cek apakah user adalah kasir
if not request.user.groups.filter(name="cashiers").exists():
    return Response({"detail": "Permission denied."}, status=403)
```

### Menu Visibility (Frontend):

```javascript
function applyMenuVisibility(groups) {
    const isManager = groups.includes('managers');
    const isOwner = groups.includes('owners');
    const isCashier = groups.includes('cashiers') || groups.includes('shop_users');
    
    // Manager only
    $('#menuWarehouse').toggle(isManager);
    
    // Manager + Owner
    $('#menuWaste').toggle(isManager || isOwner);
    $('#menuReports').toggle(isManager || isOwner);
    $('#menuAI').toggle(isManager || isOwner);
    $('#menuDashboard').toggle(isManager || isOwner);
    
    // All authenticated
    $('#menuShop').toggle(true);
    $('#menuTransfer').toggle(true);
}

// Load user info
$.ajax({
    url: '/auth/user/',
    success: function(data) {
        $('#userName').text(data.username);
        applyMenuVisibility(data.groups);
    }
});
```

---

## 📡 API ENDPOINTS

### Items (Barang Gudang)

```
GET    /api/items/                    # List items (paginated)
POST   /api/items/                    # Create item (manager only)
GET    /api/items/<sku>/              # Get item detail
PATCH  /api/items/<sku>/              # Update item (manager only)
DELETE /api/items/<sku>/              # Soft delete (manager only)

Query params:
- page=1
- page_size=25
- search=indomie
- ordering=sku / -quantity (- = descending)
```

### Shop Items (Barang Toko)

```
GET  /api/shop_items/                 # List shop items
    - Manager/Owner: semua shop items
    - Kasir: shop items sendiri saja
```

### Transfer

```
GET  /api/transfer_items/             # List transfer requests
POST /api/transfer/                   # Add item to draft transfer (kasir)
POST /api/submit-transfer-request/    # Submit request (kasir)
POST /api/complete-transfer/          # Approve/cancel (manager)
```

### Configuration

```
GET  /api/app_config/                 # Get app config
POST /api/set_edit_lock_status/       # Set maintenance mode
GET  /api/get_edit_lock_status/       # Check maintenance status
```

### Reports

```
GET  /api/export_data/                # Export Excel
POST /api/import_data/                # Import Excel (manager + config)
```

### AI

```
POST /api/ai/ask/                     # Ask AI
POST /api/ai/inventory-insights/      # Get insights
GET  /api/ai/status/                  # Check AI quota
```

---

## 🛡️ SECURITY FEATURES

### 1. CSRF Protection

```python
# Django middleware (di settings.py)
MIDDLEWARE = [
    ...
    'django.middleware.csrf.CsrfViewMiddleware',
    ...
]

# Di JavaScript
headers: { 'X-CSRFToken': getCSRFToken() }
```

### 2. SQL Injection Prevention

```python
# Django ORM automatically escapes
Item.objects.filter(sku__icontains=search_query)  # Safe

# Middleware pattern detection
if re.search(r'(union|select|insert|update|delete|drop)', 
             request_body, re.IGNORECASE):
    return JsonResponse({"error": "Potential SQL injection"}, status=400)
```

### 3. XSS Prevention

```python
# Django templates auto-escape HTML
{{ item.description }}  # Auto-escaped

# JavaScript
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;  # Safe
    return div.innerHTML;
}
```

### 4. Rate Limiting

```python
# DRF throttling (settings.py)
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '100/second'
    }
}

# AI Service rate limiting (per user)
cache_key = f'ai_rate_limit_user_{user_id}'
request_count = cache.get(cache_key, 0)
if request_count >= 20:
    return Response({'error': 'Rate limit exceeded'}, status=429)
cache.set(cache_key, request_count + 1, 3600)  # 1 hour
```

### 5. Login Protection

```python
# Django Axes (settings.py)
AXES_FAILURE_LIMIT = 5       # Max 5 failed attempts
AXES_COOLOFF_TIME = 30       # 30 minutes lockout
```

---

## 🤖 AI SERVICE

### Groq Client:

```python
from ai_service.groq_client import GroqClient

client = GroqClient()

# Simple Q&A
answer = client.simple_ask(
    question="Berapa total stok indomie?",
    context="Data inventory: ...",
    model_preference='fast'  # fast | balanced | quality
)

# Model options:
# - fast: llama-3.1-8b-instant (cepat & hemat token)
# - balanced: llama-3.1-70b-versatile
# - quality: llama-3.2-90b-text-preview
```

### Rate Limiting:

```python
# Per user quota:
# - Ask: 20 requests/hour
# - Insights: 10 requests/hour

# Simple queue untuk rate limiting API provider
# Max 10 requests/minute ke Groq
```

---

## 📧 EMAIL SERVICE

```python
from email_service.email import SendEmail

# Send transfer notification
SendEmail().compose(
    records=transfer_items,
    user=kasir_user,
    notification_type=SendEmail.EmailType.STOCK_TRANSFER
)
```

---

## 🎨 DESIGN SYSTEM

### Colors:

```css
Primary: #10b981 (Green)
Black: #000000
White: #ffffff
Gray Dark: #555555
Gray Light: #f5f5f5
Gray Border: #e0e0e0
```

### Animations:

```css
/* Fade In Up */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(50px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Float */
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

/* Pulse */
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
```

### Responsive Breakpoints:

```css
/* Mobile */
@media (max-width: 768px) {
    .sidebar { transform: translateX(-260px); }
    .stats-grid { grid-template-columns: 1fr; }
}

/* Desktop */
@media (min-width: 769px) {
    .sidebar { transform: translateX(0); }
    .stats-grid { grid-template-columns: repeat(4, 1fr); }
}
```

---

## 🚀 DEPLOYMENT CHECKLIST

### Production Settings:

```python
# .env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_SECRET_KEY=<generate-new-secret-key>

# Database (switch to PostgreSQL/MySQL)
ENGINE=django.db.backends.postgresql
DB_NAME=inventory_db
DB_USER=db_user
DB_PASSWORD=<strong-password>
DB_HOST=localhost
DB_PORT=5432
```

### Static Files:

```bash
python manage.py collectstatic --noinput
```

### Migrations:

```bash
python manage.py migrate
```

### Create Superuser:

```bash
python manage.py createsuperuser
```

---

**Terakhir Diupdate:** 24 Juli 2026  
**Versi:** 1.2.0

---

**🎉 Selamat! Dokumentasi lengkap telah selesai dibuat!**
