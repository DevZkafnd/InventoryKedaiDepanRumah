"""
Script untuk memperbaiki grup user admin di database production
Menambahkan user 'admin' ke grup 'managers' jika belum ada
"""
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ssm.settings")
django.setup()

from django.contrib.auth.models import User, Group


def fix_admin_groups():
    print("=" * 60)
    print("  Memperbaiki Grup User Admin")
    print("=" * 60)

    # 1. Pastikan semua grup ada
    owners_group, created = Group.objects.get_or_create(name="owners")
    if created:
        print("[✓] Grup 'owners' dibuat")
    
    managers_group, created = Group.objects.get_or_create(name="managers")
    if created:
        print("[✓] Grup 'managers' dibuat")
    
    cashiers_group, created = Group.objects.get_or_create(name="cashiers")
    if created:
        print("[✓] Grup 'cashiers' dibuat")
    
    shop_users_group, created = Group.objects.get_or_create(name="shop_users")
    if created:
        print("[✓] Grup 'shop_users' dibuat")
    
    receive_mail_group, created = Group.objects.get_or_create(name="receive_mail")
    if created:
        print("[✓] Grup 'receive_mail' dibuat")

    # 2. Cek dan perbaiki user admin
    try:
        admin_user = User.objects.get(username="admin")
        print(f"\n[INFO] User 'admin' ditemukan (ID: {admin_user.id})")
        
        # Periksa grup saat ini
        current_groups = list(admin_user.groups.values_list('name', flat=True))
        print(f"[INFO] Grup saat ini: {current_groups if current_groups else 'TIDAK ADA'}")
        
        # Pastikan admin adalah superuser dan staff
        updated = False
        if not admin_user.is_superuser:
            admin_user.is_superuser = True
            updated = True
            print("[✓] Status superuser diaktifkan")
        
        if not admin_user.is_staff:
            admin_user.is_staff = True
            updated = True
            print("[✓] Status staff diaktifkan")
        
        if updated:
            admin_user.save()
        
        # Tambahkan ke grup managers jika belum ada
        if not admin_user.groups.filter(name="managers").exists():
            admin_user.groups.add(managers_group)
            print("[✓] User 'admin' ditambahkan ke grup 'managers'")
        else:
            print("[OK] User 'admin' sudah ada di grup 'managers'")
        
        # Verifikasi ulang
        final_groups = list(admin_user.groups.values_list('name', flat=True))
        print(f"\n[INFO] Grup setelah perbaikan: {final_groups}")
        print(f"[INFO] is_superuser: {admin_user.is_superuser}")
        print(f"[INFO] is_staff: {admin_user.is_staff}")
        
    except User.DoesNotExist:
        print("\n[ERROR] User 'admin' tidak ditemukan di database!")
        print("[INFO] Membuat user 'admin' baru dengan password 'admin123'...")
        
        admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@kedai.com",
            password="admin123",
        )
        admin_user.groups.add(managers_group)
        print("[✓] User 'admin' berhasil dibuat dan ditambahkan ke grup 'managers'")

    print("\n" + "=" * 60)
    print("  Selesai! User admin siap digunakan.")
    print("=" * 60)
    print("\n  Login dengan:")
    print("  Username: admin")
    print("  Password: admin123")
    print()


if __name__ == "__main__":
    fix_admin_groups()
