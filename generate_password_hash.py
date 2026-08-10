"""
Generate Django password hash untuk create superuser manual
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ssm.settings')
os.environ['DJANGO_SECRET_KEY'] = 'temp-key-for-hash-generation'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'localhost'
os.environ['AXES_FAILURE_LIMIT'] = '5'
os.environ['AXES_COOLOFF_TIME'] = '30'
os.environ['ALLOW_PW_CHANGE'] = 'True'

django.setup()

from django.contrib.auth.hashers import make_password

# Ganti password di bawah dengan password yang kamu mau
password = "admin123"  # GANTI INI!
username = "admin"      # Username untuk superuser

# Generate hash
password_hash = make_password(password)

print("="*60)
print("DJANGO PASSWORD HASH GENERATOR")
print("="*60)
print(f"\nUsername: {username}")
print(f"Password: {password}")
print(f"\nPassword Hash (copy ini):")
print(password_hash)
print("\n" + "="*60)
print("\nSQL Query untuk create superuser:")
print("="*60)
print(f"""
INSERT INTO auth_user (
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined
) VALUES (
    '{password_hash}',
    NULL,
    true,
    '{username}',
    '',
    '',
    '{username}@example.com',
    true,
    true,
    NOW()
);
""")
print("="*60)
print("\nCara pakai:")
print("1. Copy SQL query di atas")
print("2. Buka Neon Dashboard -> SQL Editor")
print("3. Paste & Run query")
print("4. Login dengan username & password di atas")
print("="*60)
