"""
Script untuk test koneksi ke Neon PostgreSQL
"""
import os
import sys
import django

# Set DATABASE_URL
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_j8ThFKgdmpw7@ep-orange-wildflower-aztc4bgj.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
os.environ['DJANGO_SECRET_KEY'] = 'test-secret-key-for-testing-only'
os.environ['DJANGO_DEBUG'] = 'True'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'localhost'
os.environ['AXES_FAILURE_LIMIT'] = '5'
os.environ['AXES_COOLOFF_TIME'] = '30'
os.environ['ALLOW_PW_CHANGE'] = 'True'

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ssm.settings')
django.setup()

# Test connection
from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print("✅ Koneksi ke Neon PostgreSQL BERHASIL!")
        print(f"📊 PostgreSQL Version: {version[0]}")
        
        # Check tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"\n📋 Tables yang ada ({len(tables)}):")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("\n📋 Belum ada tables (database masih kosong)")
            print("   Jalankan: python manage.py migrate")
        
except Exception as e:
    print("❌ Koneksi ke Neon PostgreSQL GAGAL!")
    print(f"Error: {e}")
    sys.exit(1)
