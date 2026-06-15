"""
Script untuk mengisi database dengan data contoh
Inventory Kedai Depan Rumah
"""
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ssm.settings")
django.setup()

from django.contrib.auth.models import User, Group
from stock_manager.models import Item, ShopItem, TransferItem, Admin


def seed():
    print("=" * 55)
    print("  Mengisi database dengan data contoh...")
    print("=" * 55)

    # ── 1. Grup pengguna ──────────────────────────────────────
    managers_group, _ = Group.objects.get_or_create(name="managers")
    shop_users_group, _ = Group.objects.get_or_create(name="shop_users")
    receive_mail_group, _ = Group.objects.get_or_create(name="receive_mail")
    print("[OK] Grup: managers, shop_users, receive_mail")

    # ── 2. Superuser / manajer ────────────────────────────────
    if not User.objects.filter(username="admin").exists():
        admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@kedai.com",
            password="admin123",
        )
        admin_user.groups.add(managers_group)
        print("[OK] Superuser 'admin' dibuat  (password: admin123)")
    else:
        admin_user = User.objects.get(username="admin")
        admin_user.groups.add(managers_group)
        print("[--] Superuser 'admin' sudah ada")

    # ── 3. Pengguna toko (kasir) ──────────────────────────────
    if not User.objects.filter(username="kasir1").exists():
        kasir = User.objects.create_user(
            username="kasir1",
            email="kasir1@kedai.com",
            password="kasir123",
        )
        kasir.groups.add(shop_users_group)
        print("[OK] Pengguna toko 'kasir1' dibuat  (password: kasir123)")
    else:
        kasir = User.objects.get(username="kasir1")
        kasir.groups.add(shop_users_group)
        print("[--] Pengguna toko 'kasir1' sudah ada")

    # ── 4. Konfigurasi Admin ──────────────────────────────────
    if not Admin.objects.exists():
        Admin.objects.create(
            edit_lock=False,
            allow_uploads=True,
            allow_upload_deletions=False,
            allow_email_notifications=False,
            records_per_page=25,
        )
        print("[OK] Konfigurasi aplikasi dibuat")
    else:
        print("[--] Konfigurasi aplikasi sudah ada")

    # ── 5. Data barang gudang ─────────────────────────────────
    barang_gudang = [
        # (sku, deskripsi, harga_jual, stok_gudang)
        ("MIE-001",  "Mie Instan Goreng",          3500.00,  120),
        ("MIE-002",  "Mie Instan Kuah Ayam",        3500.00,  100),
        ("MIE-003",  "Mie Instan Kuah Soto",        3500.00,   80),
        ("BRS-001",  "Beras 5 Kg",                 65000.00,   30),
        ("BRS-002",  "Beras 10 Kg",               125000.00,   15),
        ("GLA-001",  "Gula Pasir 1 Kg",            16000.00,   50),
        ("GRM-001",  "Garam Halus 250 gr",          3000.00,   60),
        ("MNY-001",  "Minyak Goreng 1 Liter",      18000.00,   40),
        ("MNY-002",  "Minyak Goreng 2 Liter",      34000.00,   25),
        ("KPI-001",  "Kopi Sachet Hitam",           2000.00,  200),
        ("KPI-002",  "Kopi Sachet Susu",            2500.00,  180),
        ("TEH-001",  "Teh Celup 25 Pcs",            8000.00,   70),
        ("SBN-001",  "Sabun Mandi Batang",          4500.00,   90),
        ("SBN-002",  "Sabun Cuci Piring 500 ml",   12000.00,   45),
        ("SMP-001",  "Sampo Sachet",                2000.00,  150),
        ("RTK-001",  "Rokok Kretek 12 Batang",     22000.00,   60),
        ("AIR-001",  "Air Mineral 600 ml",          4000.00,  100),
        ("AIR-002",  "Air Mineral 1500 ml",         7000.00,   80),
        ("SNK-001",  "Keripik Singkong 200 gr",     8000.00,   55),
        ("SNK-002",  "Biskuit Coklat 100 gr",       6500.00,   65),
        ("SUS-001",  "Susu Kental Manis 385 gr",   14000.00,   35),
        ("SUS-002",  "Susu UHT 200 ml",             5000.00,   90),
        ("KCP-001",  "Kecap Manis 135 ml",          7500.00,   40),
        ("SMB-001",  "Sambal Sachet",               1500.00,  120),
        ("PLT-001",  "Pelembab Wajah Sachet",       2500.00,   80),
    ]

    dibuat = 0
    for sku, desc, harga, stok in barang_gudang:
        obj, created = Item.objects.get_or_create(
            sku=sku,
            defaults={
                "description": desc,
                "retail_price": harga,
                "quantity": stok,
                "is_active": True,
            },
        )
        if created:
            dibuat += 1

    if dibuat:
        print(f"[OK] {dibuat} barang gudang baru ditambahkan")
    else:
        print(f"[--] Data barang gudang sudah ada ({Item.objects.count()} item)")

    # ── 6. Stok toko kasir1 (sebagian barang) ─────────────────
    stok_toko = [
        ("MIE-001", 20),
        ("MIE-002", 15),
        ("KPI-001", 30),
        ("KPI-002", 25),
        ("AIR-001", 20),
        ("SNK-001", 10),
        ("SNK-002", 12),
        ("SBN-001", 15),
        ("GLA-001",  8),
        ("TEH-001", 10),
    ]

    toko_dibuat = 0
    for sku, qty in stok_toko:
        try:
            item = Item.objects.get(sku=sku)
            obj, created = ShopItem.objects.get_or_create(
                shop_user=kasir,
                item=item,
                defaults={"quantity": qty},
            )
            if created:
                toko_dibuat += 1
        except Item.DoesNotExist:
            pass

    if toko_dibuat:
        print(f"[OK] {toko_dibuat} stok toko kasir1 ditambahkan")
    else:
        print(f"[--] Stok toko kasir1 sudah ada")

    print("=" * 55)
    print("  Selesai! Data contoh berhasil diisi.")
    print("=" * 55)
    print()
    print("  Akun tersedia:")
    print("  ┌─────────────┬──────────┬──────────────────┐")
    print("  │ Username    │ Password │ Role             │")
    print("  ├─────────────┼──────────┼──────────────────┤")
    print("  │ admin       │ admin123 │ Manajer/Admin    │")
    print("  │ kasir1      │ kasir123 │ Pengguna Toko    │")
    print("  └─────────────┴──────────┴──────────────────┘")
    print()


if __name__ == "__main__":
    seed()
