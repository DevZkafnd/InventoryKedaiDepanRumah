"""
Run Django migrations on Neon database
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Set environment variables
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_j8ThFKgdmpw7@ep-orange-wildflower-aztc4bgj-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
os.environ['DJANGO_SECRET_KEY'] = 'bbr+#nr)bxx^rgno4ki@=ecu*6bl^i-3^cu*v+=rqa6o0^1#h+'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'localhost'
os.environ['AXES_FAILURE_LIMIT'] = '5'
os.environ['AXES_COOLOFF_TIME'] = '30'
os.environ['ALLOW_PW_CHANGE'] = 'True'

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ssm.settings')
django.setup()

print("="*60)
print("RUNNING DJANGO MIGRATIONS ON NEON DATABASE")
print("="*60)

# Run migrations
print("\n📊 Running migrations...")
try:
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    print("\n✅ Migrations completed successfully!")
except Exception as e:
    print(f"\n❌ Error running migrations: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("DONE! Database tables created.")
print("="*60)
print("\nNext steps:")
print("1. Run: python generate_password_hash.py")
print("2. Copy SQL query")
print("3. Run di Neon SQL Editor")
print("4. Login ke website")
print("="*60)
