"""
Create users with specific roles (Owner, Manager, Cashier, Shop User)
Via SQL queries untuk Neon
"""
from django.contrib.auth.hashers import make_password
import os
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

# Define users to create
users = [
    {
        "username": "owner1",
        "password": "owner123",
        "email": "owner@example.com",
        "role": "owners",
        "description": "Owner - Full access"
    },
    {
        "username": "manager1",
        "password": "manager123",
        "email": "manager@example.com",
        "role": "managers",
        "description": "Manager/Admin - Warehouse management"
    },
    {
        "username": "kasir1",
        "password": "kasir123",
        "email": "kasir@example.com",
        "role": "cashiers",
        "description": "Kasir - Limited shop access"
    },
]

print("="*70)
print("SQL QUERIES TO CREATE USERS WITH ROLES")
print("="*70)
print("\nRun these queries in Neon SQL Editor one by one:\n")

# First, create groups if not exist
print("-- Step 1: Create Groups (if not exist)")
print("-"*70)
groups = ['owners', 'managers', 'cashiers', 'shop_users']
for group in groups:
    print(f"""
INSERT INTO auth_group (name)
SELECT '{group}'
WHERE NOT EXISTS (SELECT 1 FROM auth_group WHERE name = '{group}');
""")

print("\n-- Step 2: Get Group IDs")
print("-"*70)
print("""
SELECT id, name FROM auth_group 
WHERE name IN ('owners', 'managers', 'cashiers', 'shop_users');
""")
print("\n⚠️ CATAT id untuk setiap group! Akan dipakai di step 3.")

print("\n" + "="*70)
print("-- Step 3: Create Users")
print("="*70)

for i, user in enumerate(users, 1):
    password_hash = make_password(user['password'])
    
    print(f"\n-- {i}. {user['description']}")
    print(f"-- Username: {user['username']}")
    print(f"-- Password: {user['password']}")
    print("-"*70)
    
    # Insert user
    print(f"""
-- Insert user
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
    false,
    '{user['username']}',
    '',
    '',
    '{user['email']}',
    {'true' if user['role'] == 'managers' else 'false'},
    true,
    NOW()
) RETURNING id;
""")
    
    print(f"""
-- Assign to group '{user['role']}'
-- ⚠️ GANTI <user_id> dengan id user yang baru dibuat
-- ⚠️ GANTI <group_id> dengan id group '{user['role']}' dari step 2
INSERT INTO auth_user_groups (user_id, group_id)
VALUES (<user_id>, <group_id>);
""")

print("\n" + "="*70)
print("SUMMARY - User Credentials")
print("="*70)
for user in users:
    print(f"\n{user['description']}:")
    print(f"  Username: {user['username']}")
    print(f"  Password: {user['password']}")
    print(f"  Role:     {user['role']}")

print("\n" + "="*70)
print("SECURITY RECOMMENDATIONS")
print("="*70)
print("""
1. ✅ GANTI password default setelah first login!
2. ✅ Hapus user 'admin' superuser setelah setup:
   DELETE FROM auth_user WHERE username = 'admin';
   
3. ✅ User 'owner1' cukup untuk production (akses penuh tapi bukan superuser)
4. ✅ Berikan akses sesuai kebutuhan:
   - owners:    Full access (warehouse + shop + reports)
   - managers:  Warehouse management
   - cashiers:  Shop operations only
   - shop_users: Limited shop access

5. ⚠️ Jangan expose Django Admin panel (/admin) ke public!
   Hanya owner/manager yang boleh akses.
""")

print("="*70)
print("\n💡 Cara mudah: Copy semua query, run satu per satu di Neon SQL Editor")
print("="*70)
