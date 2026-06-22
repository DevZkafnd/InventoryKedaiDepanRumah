# 🎨 Logo Implementation Guide

## ✅ Logo yang Telah Diterapkan

Logo "Kedai Depan Rumah" sudah diterapkan di seluruh aplikasi dengan konsistensi warna yang sesuai dengan UI.

### 📁 Lokasi File Logo

```
static/img/
├── logo-black.png   # Logo hitam untuk background terang
├── logo-white.png   # Logo putih untuk background gelap
└── logo.svg         # Logo lama (backup)
```

## 🎯 Penerapan Logo Per Halaman

### 1. **Landing Page** (`landing.html`)
- **Logo**: `logo-black.png` (hitam)
- **Lokasi**: Header hero section
- **Ukuran**: 80px × 80px
- **Animasi**: Pulse effect
- **Alasan**: Background putih, butuh kontras dengan logo hitam

```html
<img src="{% static 'img/logo-black.png' %}" alt="Logo Kedai Depan Rumah" class="logo-icon">
<div class="logo-text">Kedai Depan Rumah</div>
```

### 2. **Dashboard** (`dashboard.html`)
- **Logo**: `logo-white.png` (putih)
- **Lokasi**: Sidebar header
- **Ukuran**: 45px height (auto width)
- **Background**: Gradient ungu (#667eea - #764ba2)
- **Alasan**: Sidebar gelap, butuh logo putih untuk visibility

```html
<img src="{% static 'img/logo-white.png' %}" alt="Logo Kedai Depan Rumah">
<span>Kedai Depan Rumah</span>
```

### 3. **Base Dashboard** (`base_dashboard.html`)
- **Logo**: `logo-white.png` (putih)
- **Lokasi**: Sidebar header (shared template)
- **Ukuran**: 45px height
- **Digunakan di**:
  - Warehouse page
  - Shop page
  - Transfer page
  - Reports page
  - Settings page

### 4. **Index/Old Dashboard** (`index.html`)
- **Logo**: `logo-white.png` (putih)
- **Lokasi**: Top navbar
- **Ukuran**: 40px height
- **Background**: Gradient navbar
- **Filter**: Brightness + invert untuk ensure visibility

```html
<img src="{% static 'img/logo-white.png' %}" alt="Logo Kedai Depan Rumah">
```

## 🎨 Design Guidelines

### Ukuran Logo
| Lokasi | Height | Width | Rasio |
|--------|--------|-------|-------|
| Landing Page | 80px | auto | Original |
| Sidebar | 45px | auto | Original |
| Navbar | 40px | auto | Original |

### Spacing
- Gap antara logo & text: 12-15px
- Margin bottom: 30px (landing page)
- Padding sidebar: 25px 20px

### Warna Background yang Cocok

#### Logo Hitam (`logo-black.png`)
✅ Cocok untuk:
- White background
- Light gray background (#f5f7fa, #f8f9fa)
- Pastels (light colors)

❌ Tidak cocok untuk:
- Dark backgrounds
- Gradients (purple, blue, etc.)

#### Logo Putih (`logo-white.png`)
✅ Cocok untuk:
- Dark backgrounds
- Gradients (purple, blue, green)
- Colored backgrounds

❌ Tidak cocok untuk:
- White/light backgrounds
- Pastels

## 🔧 CSS Styling

### Landing Page Logo
```css
.logo-icon {
    width: 80px;
    height: 80px;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
```

### Sidebar Logo
```css
.sidebar-brand img {
    height: 45px;
    width: auto;
}
```

### Navbar Logo (with filter)
```css
.navbar-brand img {
    height: 40px;
    width: auto;
    filter: brightness(0) invert(1); /* Make logo white if needed */
}
```

## 🚀 Implementasi

### Langkah-langkah yang Sudah Dilakukan

1. ✅ Copy logo files ke `static/img/`
2. ✅ Update `landing.html` - logo hitam di hero
3. ✅ Update `dashboard.html` - logo putih di sidebar
4. ✅ Update `base_dashboard.html` - logo putih di sidebar
5. ✅ Update `index.html` - logo putih di navbar
6. ✅ Run `collectstatic` untuk deploy static files
7. ✅ Test visibility di semua halaman

### Testing Checklist

- [x] Landing page - logo terlihat jelas
- [x] Dashboard - logo kontras dengan sidebar ungu
- [x] Warehouse - logo dari base template
- [x] Shop - logo dari base template  
- [x] Index - logo di navbar
- [x] Logo tidak pixelated
- [x] Logo proporsional (tidak stretched)
- [x] Animasi smooth (landing page)

## 🎯 Responsive Behavior

### Desktop (> 768px)
- Logo full size
- Text "Kedai Depan Rumah" visible
- Sidebar logo 45px
- Landing logo 80px

### Mobile (≤ 768px)
- Logo size tetap sama
- Text mungkin wrap atau hide (depending on space)
- Sidebar collapse, logo hanya visible saat expanded

## 💡 Tips Customization

### Mengubah Ukuran Logo

**Landing Page:**
```css
.logo-icon {
    width: 100px;  /* Ubah dari 80px */
    height: 100px;
}
```

**Sidebar:**
```css
.sidebar-brand img {
    height: 50px;  /* Ubah dari 45px */
}
```

### Menambah Glow Effect

```css
.sidebar-brand img {
    filter: drop-shadow(0 0 10px rgba(255,255,255,0.5));
}
```

### Hover Animation

```css
.sidebar-brand img {
    transition: transform 0.3s ease;
}

.sidebar-brand:hover img {
    transform: scale(1.1);
}
```

## 📝 Notes

1. **Format PNG**: Logo dalam format PNG untuk transparency
2. **No SVG**: SVG bisa digunakan tapi PNG lebih universal
3. **Resolution**: Pastikan logo high-res untuk retina displays
4. **Caching**: Browser mungkin cache logo lama, force refresh: Ctrl+Shift+R

## 🐛 Troubleshooting

### Logo tidak muncul?

1. **Check file exists:**
   ```bash
   ls static/img/logo-*.png
   ```

2. **Run collectstatic:**
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Check template tag:**
   ```django
   {% load static %}
   {% static 'img/logo-white.png' %}
   ```

4. **Check browser console:**
   - F12 > Network tab
   - Look for 404 errors on logo files

### Logo terlalu besar/kecil?

Edit CSS `height` property di masing-masing template.

### Logo tidak kontras?

Pilih variant yang benar:
- Dark background → `logo-white.png`
- Light background → `logo-black.png`

---

**Logo Version**: v1.0  
**Last Updated**: 2026-06-23  
**Status**: ✅ Implemented & Tested
