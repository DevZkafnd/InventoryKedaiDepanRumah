# 📦 Inventory Management System - Kedai Depan Rumah

Sistem manajemen inventory modern dengan **AI Assistant** menggunakan Groq API untuk membantu bisnis Anda lebih efisien.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Django](https://img.shields.io/badge/django-6.0+-orange.svg)
![AI](https://img.shields.io/badge/AI-Groq%20Llama%203-purple.svg)

## ✨ Fitur Utama

### 📊 **Core Features**
- ✅ **Real-time Inventory Tracking** - Monitor stok barang secara real-time
- ✅ **Transfer Management** - Sistem pemindahan barang antar lokasi
- ✅ **Multi-user Support** - Mendukung banyak pengguna dengan role berbeda
- ✅ **Excel Import/Export** - Import dan export data dalam format Excel
- ✅ **Responsive Design** - Tampilan optimal di desktop & mobile

### 🤖 **AI Assistant (NEW!)**
- ✅ **Smart Insights** - Dapatkan insights dari data inventory Anda
- ✅ **Q&A System** - Tanya jawab tentang inventory management
- ✅ **Token Efficient** - Menggunakan model Llama 3 yang hemat token
- ✅ **Simple Queue System** - Rate limiting otomatis untuk efisiensi
- ✅ **Free Tier** - Menggunakan Groq API gratis

### 🔒 **Security Features**
- ✅ **Anti SQL Injection** - Proteksi dari serangan SQL injection
- ✅ **XSS Prevention** - Mencegah serangan cross-site scripting
- ✅ **Rate Limiting** - Membatasi jumlah request per IP/user
- ✅ **Login Protection** - Sistem lockout setelah beberapa kali gagal login
- ✅ **CSRF Protection** - Django CSRF protection built-in

## 🎨 Preview

### Landing Page
Landing page modern dengan animasi smooth dan desain gradient yang menarik

### Dashboard
Dashboard inventory dengan fitur lengkap dan AI Assistant

## 🚀 Instalasi

### Prasyarat
- Python 3.8 atau lebih tinggi
- pip (Python package manager)
- Git (opsional)

### Langkah Instalasi

#### 1️⃣ Clone atau Download Repository
```bash
git clone https://github.com/yourusername/inventory-kedai-depan-rumah.git
cd inventory-kedai-depan-rumah
```

#### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3️⃣ Setup Environment Variables
Copy file `.env_default` menjadi `.env`:
```bash
copy .env_default .env
```

Edit file `.env` dan sesuaikan konfigurasi:
```env
DJANGO_SECRET_KEY='generate-your-secret-key-here'
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS='127.0.0.1,localhost'
GROQ_API_KEY='your-groq-api-key-here'
```

**Generate Django Secret Key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 4️⃣ Database Migration
```bash
python manage.py migrate
```

#### 5️⃣ Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

#### 6️⃣ Collect Static Files
```bash
python manage.py collectstatic --noinput
```

#### 7️⃣ Run Development Server
```bash
python manage.py runserver
```

Aplikasi akan berjalan di: **http://127.0.0.1:8000**

## 🎯 Cara Menggunakan

### Akses Aplikasi
1. Buka browser dan kunjungi `http://127.0.0.1:8000`
2. Anda akan melihat **Landing Page** yang menarik
3. Klik tombol **"Masuk ke Dashboard"**
4. Login dengan username dan password yang telah dibuat

### Fitur AI Assistant

#### 1. Simple Ask (Tanya Jawab)
```bash
POST /api/ai/ask/
Content-Type: application/json

{
  "question": "Bagaimana cara mengelola stok yang efisien?",
  "model": "fast"
}
```

#### 2. Inventory Insights
```bash
POST /api/ai/inventory-insights/
Content-Type: application/json

{
  "inventory_data": {...},
  "question": "Apa insight dari data inventory ini?"
}
```

#### 3. Check Status & Quota
```bash
GET /api/ai/status/
```

### Rate Limits
- **Ask Endpoint**: 20 requests per hour per user
- **Insights Endpoint**: 10 requests per hour per user
- **Global**: 100 requests per minute per IP

## 🛠️ Teknologi yang Digunakan

### Backend
- **Django 6.0.5** - Web framework
- **Django REST Framework** - API framework
- **SQLite** - Database (bisa diganti MySQL/PostgreSQL)
- **Python-dotenv** - Environment variable management

### AI & Machine Learning
- **Groq API** - AI inference platform
- **Llama 3.1 Models** - Language models (8B, 70B, 90B)

### Security
- **Django Axes** - Brute force protection
- **Custom Middleware** - SQL injection & XSS prevention
- **Rate Limiting** - Request throttling

### Frontend
- **HTML5, CSS3, JavaScript** - Modern web standards
- **Responsive Design** - Mobile-friendly
- **Animations** - Smooth CSS animations

## 📁 Struktur Project

```
inventory-kedai-depan-rumah/
├── ai_service/              # AI Service Module
│   ├── groq_client.py       # Groq API client
│   ├── middleware.py        # Security middleware
│   ├── views.py             # AI endpoints
│   └── urls.py              # AI routes
├── stock_manager/           # Main app
│   ├── models.py            # Database models
│   ├── views.py             # Views & business logic
│   ├── urls.py              # URL routing
│   └── serializers.py       # DRF serializers
├── templates/
│   ├── landing.html         # Landing page
│   ├── index.html           # Dashboard
│   └── registration/        # Auth templates
├── static/                  # Static files
├── ssm/                     # Project settings
│   ├── settings.py
│   └── urls.py
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
├── manage.py               # Django management script
└── README.md               # This file
```

## � Keamanan

### Built-in Security Features

1. **Anti SQL Injection**
   - Pattern detection untuk query berbahaya
   - Parameterized queries di Django ORM

2. **XSS Prevention**
   - Input sanitization
   - HTML escaping otomatis di templates

3. **Rate Limiting**
   - Per IP: 100 requests/minute
   - Per User (AI): 20 requests/hour

4. **Brute Force Protection**
   - Max 3 login attempts
   - Cooldown 1 hour after lockout

5. **CSRF Protection**
   - Django CSRF middleware
   - Token validation untuk forms

## 🎓 AI Models yang Tersedia

### Model Options
| Model | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| `fast` | ⚡⚡⚡ | ⭐⭐ | Quick answers, simple queries |
| `balanced` | ⚡⚡ | ⭐⭐⭐ | General purpose, good balance |
| `quality` | ⚡ | ⭐⭐⭐⭐ | Complex analysis, detailed insights |

### Token Efficiency Tips
- Batasi max_tokens (default: 300)
- Gunakan model `fast` untuk query sederhana
- Potong data besar sebelum kirim ke AI
- Gunakan caching untuk query berulang

## 📝 Development

### Run Tests
```bash
python manage.py test
```

### Create Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Shell Access
```bash
python manage.py shell
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## � Acknowledgments

- **Django** - The web framework for perfectionists
- **Groq** - Fast AI inference platform
- **Meta** - Llama language models
- **Community** - All open source contributors

## 📞 Support

Jika Anda menemukan bug atau memiliki pertanyaan:
- Open an issue di GitHub
- Email: support@example.com

## 🎉 Updates

### Version 1.0.0 (Current)
- ✅ Landing page dengan modern UI
- ✅ AI Assistant integration dengan Groq
- ✅ Security middleware (anti-hacker)
- ✅ Token efficient AI system
- ✅ Simple queue system untuk rate limiting
- ✅ Responsive design untuk mobile

---

**Made with ❤️ for Indonesian SMEs**
