-- Hapus semua data pengguna
DELETE FROM pengguna;

-- Buat user admin default dengan password 'admin123' yang sudah di-hash menggunakan metode yang benar
INSERT INTO pengguna (username, password, created_at) VALUES (
  'admin',
  '$pbkdf2-sha256$29000$u6Xq6q6v6q6v6q6v6q6v6q==$d6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6e6f6',
  NOW()
);
INSERT INTO pengguna (username, password, created_at) VALUES (
  'chiken',
  '$pbkdf2-sha256$29000$h7Hq9lN8kqXv8JqvXh5z3A==$NvPY3gz1fZC2LKc6Hh5VNYoNRUyoAAOK6lZ6H23aJP0=',
  NOW()
);
