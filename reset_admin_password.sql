-- Skrip SQL untuk mereset password admin ke 'admin123' dengan hash yang sesuai
UPDATE pengguna
SET password = '$pbkdf2-sha256$1000000$UICYVxTXddajDHsv$3689261fbc01836f93b59e83c6fc8a7f41a815b7b4f62203fdb294d3d0fbc'
WHERE username = 'admin';
