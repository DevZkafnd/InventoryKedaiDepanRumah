# 📝 Commands Cheat Sheet - Deploy Vercel

## 🔑 Generate Django Secret Key

```python
# Buka Python shell
python

# Jalankan:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

# Copy hasilnya untuk DJANGO_SECRET_KEY
```

---

## 🗄️ Database Commands

### Test Connection ke PostgreSQL Lokal
```bash
# Set DATABASE_URL dari Neon
set DATABASE_URL=postgresql://username:password@ep-xxx.neon.tech/neondb?sslmode=require

# Test connection
python manage.py dbshell
```

### Run Migrations
```bash
# Lokal (SQLite)
python manage.py migrate

# Production (PostgreSQL via DATABASE_URL)
set DATABASE_URL=postgresql://...
python manage.py migrate
```

### Create Superuser
```bash
# Lokal
python manage.py createsuperuser

# Production (dengan DATABASE_URL)
set DATABASE_URL=postgresql://...
python manage.py createsuperuser
```

### Export Data dari SQLite
```bash
# Dump semua data
python manage.py dumpdata > data.json

# Dump specific app
python manage.py dumpdata stock_manager > stock_data.json

# Exclude auth & sessions
python manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude sessions > clean_data.json
```

### Import Data ke PostgreSQL
```bash
# Set DATABASE_URL ke Neon
set DATABASE_URL=postgresql://...

# Load data
python manage.py loaddata data.json

# Atau load specific file
python manage.py loaddata stock_data.json
```

---

## 🚀 Vercel CLI Commands

### Install Vercel CLI
```bash
npm install -g vercel
```

### Login ke Vercel
```bash
vercel login
```

### Deploy Manual
```bash
# Deploy dari folder project
cd d:\projekan\inventory-kedai-depan-rumah
vercel

# Deploy production
vercel --prod
```

### Pull Environment Variables
```bash
vercel env pull .env.production
```

### View Logs
```bash
vercel logs
```

### List Deployments
```bash
vercel ls
```

---

## 🔧 Local Testing dengan PostgreSQL

### 1. Create `.env.production` file
```env
DATABASE_URL=postgresql://username:password@ep-xxx.neon.tech/neondb?sslmode=require
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

### 2. Load environment
```bash
# Load dari .env.production
set $(cat .env.production | xargs)

# Atau manual
set DATABASE_URL=postgresql://...
```

### 3. Run Django dengan Production Database
```bash
python manage.py runserver
```

---

## 📊 Neon Database SQL Commands

### Via Neon Dashboard → SQL Editor

**Check Tables:**
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

**Count Records:**
```sql
SELECT COUNT(*) FROM stock_manager_item;
SELECT COUNT(*) FROM auth_user;
```

**Check Superusers:**
```sql
SELECT username, email, is_superuser, is_staff 
FROM auth_user 
WHERE is_superuser = TRUE;
```

**Delete All Data (HATI-HATI!):**
```sql
TRUNCATE TABLE stock_manager_item CASCADE;
```

**Drop All Tables (HATI-HATI!):**
```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

---

## 🔄 Git Commands

### Push Changes ke GitHub
```bash
git add .
git commit -m "Update description"
git push origin master
```

### Revert Last Commit (Local Only)
```bash
git reset --soft HEAD~1
```

### Check Status
```bash
git status
git log --oneline -5
```

---

## 🧪 Django Testing Commands

### Run Tests
```bash
python manage.py test
```

### Run Specific Test
```bash
python manage.py test stock_manager.tests
```

### Check for Issues
```bash
python manage.py check
python manage.py check --deploy
```

### Collect Static Files
```bash
python manage.py collectstatic --noinput
```

---

## 🐛 Debugging Commands

### Django Shell
```bash
python manage.py shell

# Inside shell:
from django.contrib.auth.models import User
User.objects.all()
```

### Show Migrations
```bash
python manage.py showmigrations
```

### Make Migrations
```bash
python manage.py makemigrations
```

### SQL for Migration
```bash
python manage.py sqlmigrate stock_manager 0001
```

---

## 📦 Package Management

### Install Requirements
```bash
pip install -r requirements.txt
```

### Update Requirements
```bash
pip freeze > requirements.txt
```

### Install Specific Package
```bash
pip install package-name==version
```

---

## 🔐 Security Commands

### Change Password (Django Admin)
```bash
python manage.py changepassword username
```

### Create Auth Token (DRF)
```bash
python manage.py drf_create_token username
```

---

## 💡 Useful One-Liners

### Generate Random String
```python
import secrets
print(secrets.token_urlsafe(50))
```

### Check Django Version
```bash
python -m django --version
```

### Check Python Version
```bash
python --version
```

### Check Installed Packages
```bash
pip list
pip show django
```

---

## 🆘 Emergency Commands

### Reset Database (Local SQLite)
```bash
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Force Recreate Migrations
```bash
# Delete migrations (HATI-HATI!)
del stock_manager\migrations\0*.py

# Recreate
python manage.py makemigrations
python manage.py migrate
```

---

## 📱 Vercel Environment Variables via CLI

### List All Env Vars
```bash
vercel env ls
```

### Add Env Var
```bash
vercel env add VARIABLE_NAME
```

### Remove Env Var
```bash
vercel env rm VARIABLE_NAME
```

---

**Pro Tip**: Simpan file ini untuk referensi cepat! 📌
