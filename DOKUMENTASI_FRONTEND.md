# 🎨 Dokumentasi Frontend - Inventory Kedai Depan Rumah

## Daftar Isi
- [Arsitektur Frontend](#arsitektur-frontend)
- [Tech Stack](#tech-stack)
- [Struktur Template](#struktur-template)
- [Landing Page](#landing-page)
- [Dashboard](#dashboard)
- [Design System](#design-system)
- [JavaScript Architecture](#javascript-architecture)
- [AJAX & API Communication](#ajax--api-communication)
- [Responsive Design](#responsive-design)

---

## Arsitektur Frontend

Frontend menggunakan pendekatan **Server-Side Rendering (SSR)** dengan Django Templates + **AJAX** untuk dynamic content.

### Pola Arsitektur

```
┌────────────────────────────────────────────┐
│         Browser (Client)                    │
│                                             │
│  ┌────────────────────────────────────┐   │
│  │   HTML (Django Template)           │   │
│  │   - landing.html                   │   │
│  │   - base_dashboard.html            │   │
│  │   - dashboard.html, warehouse.html │   │
│  └──────────┬─────────────────────────┘   │
│             │                               │
│  ┌──────────▼─────────────────────────┐   │
│  │   CSS (Inline + Bootstrap)         │   │
│  │   - Custom styling                  │   │
│  │   - Bootstrap 5.3                   │   │
│  │   - Bootstrap Icons 1.11           │   │
│  └──────────┬─────────────────────────┘   │
│             │                               │
│  ┌──────────▼─────────────────────────┐   │
│  │   JavaScript (jQuery + Vanilla)    │   │
│  │   - AJAX untuk API calls           │   │
│  │   - Event handling                  │   │
│  │   - Chart.js untuk grafik          │   │
│  └────────────────────────────────────┘   │
└──────────────┬─────────────────────────────┘
               │
               │ AJAX (JSON)
               │
┌──────────────▼─────────────────────────────┐
│     Django Backend API                      │
│     /api/items/, /api/transfer/, etc.      │
└─────────────────────────────────────────────┘
```

---

## Tech Stack

### Libraries & Frameworks

| Library | Version | Purpose |
|---------|---------|---------|
| Bootstrap | 5.3.0 | CSS framework untuk layout & components |
| Bootstrap Icons | 1.11.0 | Icon library |
| jQuery | 3.7.1 | DOM manipulation & AJAX |
| Chart.js | 4.4.0 | Grafik & visualisasi data |
| Vanilla JS | ES6+ | Custom logic tanpa library |

### Why These Choices?

1. **Bootstrap 5.3**:
   - Responsive grid system
   - Pre-built components (buttons, forms, modals)
   - Consistent design language

2. **jQuery 3.7.1**:
   - Simplify AJAX calls
   - Cross-browser compatibility
   - Event handling

3. **Chart.js 4.4.0**:
   - Lightweight charting library
   - Support pie chart, bar chart, line chart
   - Responsive & animated

---

## Struktur Template

### Template Hierarchy

```
templates/
│
├── landing.html              # 🏠 Landing page (public)
│
├── base_dashboard.html       # 📐 Base template (sidebar + topbar)
│   │
│   ├── dashboard.html        # 📊 Extends base
│   ├── warehouse.html        # 🏢 Extends base
│   ├── shop.html             # 🛍️ Extends base
│   ├── transfer.html         # ↔️ Extends base
│   ├── reports.html          # 📈 Extends base
│   ├── waste.html            # 🗑️ Extends base
│   └── ai_assistant.html     # 🤖 Extends base
│
└── registration/
    └── login.html            # 🔐 Login page
```

### Template Inheritance

Django menggunakan **template inheritance** dengan `{% extends %}` dan `{% block %}`.

**Contoh:**

```django
{# base_dashboard.html #}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Dashboard{% endblock %}</title>
</head>
<body>
    <aside class="sidebar">...</aside>
    <main>
        {% block content %}
        {# Content akan diisi oleh child template #}
        {% endblock %}
    </main>
</body>
</html>

{# dashboard.html #}
{% extends "base_dashboard.html" %}

{% block title %}Dashboard - Inventory System{% endblock %}

{% block content %}
<div class="stats-grid">
    {# Dashboard content di sini #}
</div>
{% endblock %}
```

---

## Landing Page

File: `templates/landing.html`

### Struktur HTML

```html
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inventory Management System</title>
    <style>
        /* Inline CSS untuk performance */
    </style>
</head>
<body>
    <div class="container">
        <!-- Hero Section -->
        <div class="hero-section">
            <!-- Left: Text + CTA -->
            <div class="hero-content">
                <div class="logo-container">
                    <img src="{% static 'img/logo-black.png' %}" alt="Logo">
                    <div class="logo-text">Kedai Depan Rumah</div>
                </div>
                
                <h1>Kelola Inventory dengan Mudah & Cerdas</h1>
                
                <p class="subtitle">
                    Sistem manajemen inventory modern dengan AI Assistant
                </p>

                <!-- Feature Icons -->
                <div class="features">
                    <div class="feature-item">
                        <div class="feature-icon">📊</div>
                        <div class="feature-text">Tracking Real-time</div>
                    </div>
                    <!-- ... 3 items lainnya -->
                </div>

                <!-- CTA Button -->
                <a href="/accounts/login/" class="cta-button">
                    <span>Login</span>
                    <span>→</span>
                </a>
            </div>

            <!-- Right: Illustration -->
            <div class="hero-image">
                <div class="card-illustration">
                    <div class="ai-badge">✨ AI Powered</div>
                    <div class="card-stack">
                        <!-- Mini cards dengan animasi float -->
                        <div class="mini-card">...</div>
                        <div class="mini-card">...</div>
                        <div class="mini-card">...</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Stats Section -->
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">⚡</div>
                <div class="stat-label">Fast & Efficient</div>
            </div>
            <!-- ... 2 stats lainnya -->
        </div>
    </div>
</body>
</html>
```

### CSS Highlights

**1. Responsive Grid dengan CSS Grid:**

```css
.hero-section {
    display: grid;
    grid-template-columns: 1fr 1fr;  /* 2 kolom sama besar */
    gap: 60px;
    padding: 80px 60px;
    align-items: center;
}

@media (max-width: 968px) {
    .hero-section {
        grid-template-columns: 1fr;  /* 1 kolom di mobile */
    }
}
```

**2. Smooth Animations:**

```css
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(50px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.container {
    animation: fadeInUp 0.8s ease-out;
}
```

**3. Interactive Hover Effects:**

```css
.feature-item {
    transition: all 0.3s ease;
}

.feature-item:hover {
    background: #e0e0e0;
    transform: translateX(10px);  /* Geser ke kanan */
}
```

**4. Floating Animation untuk Cards:**

```css
@keyframes float {
    0%, 100% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-10px);  /* Naik 10px */
    }
}

.mini-card {
    animation: float 3s ease-in-out infinite;
}

.mini-card:nth-child(1) { animation-delay: 0s; }
.mini-card:nth-child(2) { animation-delay: 0.5s; }
.mini-card:nth-child(3) { animation-delay: 1s; }
```

---

## Dashboard

File: `templates/dashboard.html`

### Struktur Komponen

```
Dashboard
├── Sidebar (fixed, left side)
│   ├── Logo + Brand
│   ├── Navigation Menu
│   └── User Info + Logout
│
├── Main Content (right side)
│   ├── Top Bar
│   │   ├── Toggle Sidebar Button (mobile)
│   │   ├── Page Title
│   │   └── Current Date
│   │
│   └── Content Area
│       ├── Stats Cards (4 cards)
│       ├── Maintenance Mode Card (jika user = manager)
│       ├── Charts (2 grafik)
│       └── Recent Items List
```

### Stats Cards

```html
<div class="stats-grid">
    <!-- Card 1: Total Barang -->
    <div class="stat-card">
        <div class="stat-icon blue">
            <i class="bi bi-box-seam"></i>
        </div>
        <div class="stat-details">
            <h3 id="totalItems">0</h3>
            <p>Total Barang</p>
        </div>
    </div>
    
    <!-- Card 2: Stok Tersedia -->
    <div class="stat-card">
        <div class="stat-icon green">
            <i class="bi bi-check-circle"></i>
        </div>
        <div class="stat-details">
            <h3 id="inStock">0</h3>
            <p>Stok Tersedia</p>
        </div>
    </div>
    
    <!-- Card 3: Stok Menipis -->
    <!-- Card 4: Stok Habis -->
    <!-- ... -->
</div>
```

**CSS Grid untuk Responsive Layout:**

```css
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

/* auto-fit: otomatis adjust jumlah kolom berdasarkan ukuran layar */
/* minmax(240px, 1fr): minimal 240px, maksimal 1 fraction */
```

**Hover Effect:**

```css
.stat-card {
    transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
    transform: translateY(-5px);  /* Naik 5px */
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}
```

### Charts dengan Chart.js

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
                backgroundColor: ['#10b981', '#555555', '#000000'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: { size: 12 }
                    }
                }
            }
        }
    });
}

// Bar Chart - Top 5 Barang
function createBarChart(items) {
    const ctx = document.getElementById('topItemsChart');
    const labels = items.map(item => item.sku);
    const quantities = items.map(item => item.quantity);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Jumlah Stok',
                data: quantities,
                backgroundColor: 'rgba(16, 185, 129, 0.8)',
                borderColor: 'rgba(16, 185, 129, 1)',
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(0, 0, 0, 0.05)' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}
```

**Penjelasan Chart.js:**

- **type**: Jenis chart (`doughnut`, `bar`, `line`, dll)
- **data.labels**: Label untuk setiap data point
- **data.datasets**: Array of datasets (bisa multiple untuk line chart)
- **backgroundColor**: Warna background (bisa array atau single color)
- **responsive**: Auto-resize saat window resize
- **maintainAspectRatio**: false = gunakan height container

---

## Design System

### Color Palette

```css
:root {
    /* Primary */
    --color-primary: #10b981;       /* Green */
    --color-primary-dark: #065f46;
    --color-primary-light: #d1fae5;
    
    /* Neutrals */
    --color-black: #000000;
    --color-white: #ffffff;
    --color-gray-dark: #555555;
    --color-gray-light: #f5f5f5;
    --color-gray-border: #e0e0e0;
    
    /* Status Colors */
    --color-success: #10b981;
    --color-warning: #555555;
    --color-danger: #000000;
    
    /* Backgrounds */
    --bg-main: #f5f5f5;
    --bg-card: #ffffff;
    --bg-sidebar: #000000;
}
```

### Typography

```css
/* Font Stack */
body {
    font-family: -apple-system, BlinkMacSystemFont, 
                 'Segoe UI', Roboto, sans-serif;
}

/* Font Sizes */
--font-xs: 0.75rem;    /* 12px */
--font-sm: 0.875rem;   /* 14px */
--font-base: 1rem;     /* 16px */
--font-lg: 1.125rem;   /* 18px */
--font-xl: 1.25rem;    /* 20px */
--font-2xl: 1.5rem;    /* 24px */
--font-3xl: 1.875rem;  /* 30px */
--font-4xl: 2.25rem;   /* 36px */

/* Font Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### Spacing System

```css
/* Consistent spacing scale */
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-5: 1.25rem;  /* 20px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
--space-10: 2.5rem;  /* 40px */
--space-12: 3rem;    /* 48px */
--space-16: 4rem;    /* 64px */
```

### Border Radius

```css
--radius-sm: 8px;
--radius-md: 12px;
--radius-lg: 16px;
--radius-xl: 20px;
--radius-full: 9999px;  /* Fully rounded */
```

### Shadows

```css
--shadow-sm: 0 2px 8px rgba(0,0,0,0.05);
--shadow-md: 0 4px 12px rgba(0,0,0,0.1);
--shadow-lg: 0 8px 20px rgba(0,0,0,0.15);
--shadow-xl: 0 20px 60px rgba(0,0,0,0.3);
```

### Component Styling Patterns

**1. Cards:**

```css
.card {
    background: var(--bg-card);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
    padding: var(--space-6);
    transition: all 0.3s ease;
}

.card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}
```

**2. Buttons:**

```css
.btn-primary {
    background: var(--color-primary);
    color: white;
    padding: var(--space-3) var(--space-6);
    border-radius: var(--radius-full);
    border: none;
    font-weight: var(--font-semibold);
    transition: all 0.3s ease;
    cursor: pointer;
}

.btn-primary:hover {
    background: var(--color-primary-dark);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}
```

**3. Input Fields:**

```css
.form-control {
    padding: var(--space-3) var(--space-4);
    border: 1px solid var(--color-gray-border);
    border-radius: var(--radius-sm);
    font-size: var(--font-base);
    transition: border-color 0.3s ease;
}

.form-control:focus {
    outline: none;
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}
```

---

## JavaScript Architecture

### AJAX Pattern dengan jQuery

Semua komunikasi dengan backend menggunakan AJAX (Asynchronous JavaScript and XML).

**Standard AJAX Pattern:**

```javascript
// 1. Get CSRF Token (untuk POST requests)
function getCSRFToken() {
    const cookie = document.cookie.split('; ')
        .find(r => r.startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
}

// 2. GET Request
function loadItems() {
    $.ajax({
        url: '/api/items/',
        method: 'GET',
        success: function(data) {
            // Handle sukses
            console.log('Data:', data);
            renderItems(data.results);
        },
        error: function(xhr) {
            // Handle error
            console.error('Error:', xhr.responseJSON);
            alert('Gagal memuat data: ' + xhr.responseJSON.detail);
        }
    });
}

// 3. POST Request
function createItem(itemData) {
    $.ajax({
        url: '/api/items/',
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken()  // CSRF token wajib!
        },
        contentType: 'application/json',
        data: JSON.stringify(itemData),
        success: function(data) {
            alert('Item berhasil ditambahkan!');
            loadItems();  // Reload list
        },
        error: function(xhr) {
            alert('Error: ' + xhr.responseJSON.detail);
        }
    });
}

// 4. PUT/PATCH Request (Update)
function updateItem(sku, updatedData) {
    $.ajax({
        url: `/api/items/${sku}/`,
        method: 'PATCH',  // atau 'PUT'
        headers: {
            'X-CSRFToken': getCSRFToken()
        },
        contentType: 'application/json',
        data: JSON.stringify(updatedData),
        success: function(data) {
            alert('Item berhasil diupdate!');
            loadItems();
        },
        error: function(xhr) {
            alert('Error: ' + xhr.responseJSON.detail);
        }
    });
}

// 5. DELETE Request
function deleteItem(sku) {
    if (!confirm('Yakin ingin menghapus item ini?')) return;
    
    $.ajax({
        url: `/api/items/${sku}/`,
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken()
        },
        success: function() {
            alert('Item berhasil dihapus!');
            loadItems();
        },
        error: function(xhr) {
            alert('Error: ' + xhr.responseJSON.detail);
        }
    });
}
```

**Penjelasan CSRF Token:**

Django memerlukan CSRF token untuk semua POST/PUT/PATCH/DELETE requests sebagai proteksi keamanan.

```javascript
// Django menyimpan CSRF token di cookie bernama 'csrftoken'
// Kita ambil dari cookie dan kirim di header 'X-CSRFToken'

function getCSRFToken() {
    // document.cookie = "csrftoken=abc123; sessionid=xyz789"
    const cookie = document.cookie
        .split('; ')                    // ["csrftoken=abc123", "sessionid=xyz789"]
        .find(r => r.startsWith('csrftoken='));  // "csrftoken=abc123"
    return cookie ? cookie.split('=')[1] : '';  // "abc123"
}
```

---

### Event Handling

**1. Document Ready:**

```javascript
$(document).ready(function() {
    // Kode di sini akan execute setelah DOM ready
    console.log('DOM is ready!');
    
    loadUser();
    loadItems();
    initEventListeners();
});
```

**2. Button Click Events:**

```javascript
// Event delegation (untuk dynamic elements)
$(document).on('click', '.btn-edit', function() {
    const sku = $(this).data('sku');  // data-sku attribute
    editItem(sku);
});

$(document).on('click', '.btn-delete', function() {
    const sku = $(this).data('sku');
    deleteItem(sku);
});

// Direct binding (untuk static elements)
$('#btnAddItem').on('click', function() {
    showAddItemModal();
});
```

**3. Form Submit:**

```javascript
$('#formAddItem').on('submit', function(e) {
    e.preventDefault();  // Prevent default form submit
    
    // Get form data
    const formData = {
        sku: $('#inputSKU').val(),
        description: $('#inputDescription').val(),
        purchase_price: $('#inputPrice').val(),
        quantity: $('#inputQuantity').val(),
        expiry_date: $('#inputExpiryDate').val() || null
    };
    
    // Submit via AJAX
    createItem(formData);
});
```

**4. Input Change Events:**

```javascript
// Real-time search
$('#searchInput').on('input', function() {
    const searchQuery = $(this).val();
    searchItems(searchQuery);
});

// Debounced search (untuk performance)
let searchTimeout;
$('#searchInput').on('input', function() {
    const searchQuery = $(this).val();
    
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(function() {
        searchItems(searchQuery);
    }, 300);  // Wait 300ms after user stops typing
});
```

---

### Data Rendering Patterns

**1. Render Table:**

```javascript
function renderItems(items) {
    const tbody = $('#itemTableBody');
    tbody.empty();  // Clear existing rows
    
    if (items.length === 0) {
        tbody.html(`
            <tr>
                <td colspan="6" class="text-center">
                    Tidak ada data
                </td>
            </tr>
        `);
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
                        <i class="bi bi-pencil"></i> Edit
                    </button>
                    <button class="btn btn-sm btn-danger btn-delete" 
                            data-sku="${item.sku}">
                        <i class="bi bi-trash"></i> Hapus
                    </button>
                </td>
            </tr>
        `;
        tbody.append(row);
    });
}

// Escape HTML untuk prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Format number dengan separator
function formatNumber(num) {
    return Number(num).toLocaleString('id-ID');
}

// Format date
function formatDate(dateStr) {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toLocaleDateString('id-ID');
}
```

**2. Render Cards:**

```javascript
function renderStatsCards(stats) {
    $('#totalItems').text(stats.total);
    $('#inStock').text(stats.in_stock);
    $('#lowStock').text(stats.low_stock);
    $('#outOfStock').text(stats.out_of_stock);
    
    // Add animation
    $('.stat-details h3').each(function() {
        $(this).addClass('animate-count');
    });
}
```

---

## AJAX & API Communication

### API Endpoints yang Digunakan

| Endpoint | Method | Deskripsi |
|----------|--------|-----------|
| `/api/items/` | GET | List semua barang gudang |
| `/api/items/` | POST | Tambah barang baru |
| `/api/items/<sku>/` | GET | Detail barang by SKU |
| `/api/items/<sku>/` | PATCH | Update barang |
| `/api/items/<sku>/` | DELETE | Hapus barang (soft delete) |
| `/api/shop_items/` | GET | List barang toko |
| `/api/transfer_items/` | GET | List transfer requests |
| `/api/transfer/` | POST | Tambah item ke draft transfer |
| `/api/submit-transfer-request/` | POST | Submit transfer request |
| `/api/complete-transfer/` | POST | Approve/cancel transfer |
| `/api/export_data/` | GET | Export Excel |
| `/api/import_data/` | POST | Import Excel |
| `/auth/user/` | GET | Get current user info |

### Request/Response Examples

**1. Get Items (dengan pagination & search):**

```javascript
// Request
$.ajax({
    url: '/api/items/',
    method: 'GET',
    data: {
        page: 1,
        page_size: 25,
        search: 'indomie',
        ordering: '-quantity'  // descending
    },
    success: function(data) {
        console.log(data);
    }
});

// Response
{
    "results": [
        {
            "sku": "INDOMIE-001",
            "description": "Indomie Goreng Original",
            "purchase_price": "2500.00",
            "quantity": 150,
            "expiry_date": "2027-12-31"
        },
        // ... more items
    ],
    "current_page": 1,
    "total_pages": 5,
    "previous": null,
    "next": "http://localhost:8000/api/items/?page=2",
    "previous_page_number": null,
    "next_page_number": 2
}
```

**2. Create Item:**

```javascript
// Request
$.ajax({
    url: '/api/items/',
    method: 'POST',
    headers: { 'X-CSRFToken': getCSRFToken() },
    contentType: 'application/json',
    data: JSON.stringify({
        sku: 'INDOMIE-002',
        description: 'Indomie Soto',
        purchase_price: '2500.00',
        quantity: 100,
        expiry_date: '2027-12-31'
    }),
    success: function(data) {
        console.log('Created:', data);
    }
});

// Response (201 Created)
{
    "sku": "INDOMIE-002",
    "description": "Indomie Soto",
    "purchase_price": "2500.00",
    "quantity": 100,
    "expiry_date": "2027-12-31"
}
```

**3. Error Response:**

```javascript
// Response (400 Bad Request)
{
    "detail": "Item with this SKU already exists."
}

// Response (403 Forbidden)
{
    "detail": "Permission denied."
}

// Response (404 Not Found)
{
    "error": "Item not found."
}
```

---

## Responsive Design

### Mobile-First Approach

```css
/* Base styles (mobile) */
.sidebar {
    width: 260px;
    transform: translateX(-260px);  /* Hidden by default */
}

.main-content {
    margin-left: 0;  /* No margin for mobile */
}

/* Desktop styles */
@media (min-width: 769px) {
    .sidebar {
        transform: translateX(0);  /* Visible */
    }
    
    .main-content {
        margin-left: 260px;  /* Adjust for sidebar */
    }
}
```

### Breakpoints

```css
/* Extra Small (phones) */
@media (max-width: 575px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }
}

/* Small (tablets portrait) */
@media (min-width: 576px) and (max-width: 767px) {
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Medium (tablets landscape) */
@media (min-width: 768px) and (max-width: 991px) {
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Large (desktops) */
@media (min-width: 992px) {
    .stats-grid {
        grid-template-columns: repeat(4, 1fr);
    }
}
```

### Mobile Sidebar Toggle

```javascript
// Toggle sidebar on mobile
$('#sidebarToggle').on('click', function() {
    $('body').toggleClass('sidebar-open');
});

// Close sidebar when click overlay
$('#sidebarOverlay').on('click', function() {
    $('body').removeClass('sidebar-open');
});

// Auto-close sidebar on window resize
$(window).on('resize', function() {
    if (window.innerWidth > 768) {
        $('body').removeClass('sidebar-open');
    }
});
```

```css
/* Mobile sidebar styles */
@media (max-width: 768px) {
    .sidebar {
        transform: translateX(-260px);
        transition: transform 0.3s ease;
    }
    
    body.sidebar-open .sidebar {
        transform: translateX(0);
    }
    
    body.sidebar-open .sidebar-overlay {
        display: block;  /* Show overlay */
    }
}
```

---

## Performance Optimization

### 1. Debouncing Search Input

```javascript
// Prevent excessive API calls saat user typing
let searchTimeout;
$('#searchInput').on('input', function() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(function() {
        performSearch();
    }, 300);  // Wait 300ms
});
```

### 2. Lazy Loading Images

```html
<img src="placeholder.jpg" 
     data-src="actual-image.jpg" 
     loading="lazy" 
     alt="Image">
```

### 3. Minimize DOM Manipulation

```javascript
// ❌ BAD - Multiple DOM operations
items.forEach(item => {
    $('#list').append(`<li>${item.name}</li>`);
});

// ✅ GOOD - Single DOM operation
let html = '';
items.forEach(item => {
    html += `<li>${item.name}</li>`;
});
$('#list').html(html);
```

### 4. Event Delegation

```javascript
// ❌ BAD - Bind event to each button
$('.btn-delete').on('click', function() {
    deleteItem($(this).data('sku'));
});

// ✅ GOOD - Event delegation
$(document).on('click', '.btn-delete', function() {
    deleteItem($(this).data('sku'));
});
```

---

**📝 Catatan Akhir:**

Frontend ini dirancang dengan prinsip:
- ✅ Responsive & mobile-friendly
- ✅ Performance optimization
- ✅ Clean & maintainable code
- ✅ Accessibility (ARIA labels, semantic HTML)
- ✅ Progressive enhancement

---

**Terakhir Diupdate:** 24 Juli 2026
