"""
Fix Django migrations conflicts on Neon database
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
print("FIXING DJANGO MIGRATIONS")
print("="*60)

# Fake the problematic migration
print("\n⚠️ Faking problematic migration...")
try:
    execute_from_command_line(['manage.py', 'migrate', 'stock_manager', '0002', '--fake'])
    print("✅ Migration faked successfully!")
except Exception as e:
    print(f"❌ Error: {e}")

# Run remaining migrations
print("\n📊 Running remaining migrations...")
try:
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    print("✅ All migrations completed!")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("✅ DONE! Database ready.")
print("="*60)
