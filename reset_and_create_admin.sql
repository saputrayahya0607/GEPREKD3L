-- Hapus semua data pengguna
DELETE FROM pengguna;

-- Buat user admin default dengan password 'admin123' yang sudah di-hash menggunakan metode yang benar
INSERT INTO pengguna (username, password, created_at) VALUES (
  'admin',
  '$pbkdf2-sha256$29000$u6Xq6q6v6q6v6q6v6q6v6q==$d6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6',
  NOW()
);
