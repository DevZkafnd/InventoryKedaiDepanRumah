-- Create Superuser via Neon SQL Editor
-- Jalankan di Neon Dashboard -> SQL Editor

-- 1. Check apakah sudah ada user
SELECT id, username, email, is_superuser, is_staff 
FROM auth_user;

-- 2. Create superuser (jika belum ada)
-- GANTI 'yourpassword' dengan password yang aman!
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
    'pbkdf2_sha256$870000$yourSaltHere$hashHere',  -- Ini akan kita generate
    NULL,
    true,
    'admin',
    '',
    '',
    'admin@example.com',
    true,
    true,
    NOW()
);

-- Atau cara lebih mudah: Generate password hash dulu di Python
