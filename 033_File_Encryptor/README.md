# Simple File Encryptor

Alat sederhana untuk mengamankan file menggunakan enkripsi AES berbasis password.

## Keamanan
- Menggunakan standar **AES (Fernet)**.
- Password diperkuat dengan **PBKDF2HMAC** (SHA256) dan **Salt** acak.
- Salt disimpan di dalam file terenkripsi (16 byte pertama), sehingga setiap enkripsi unik meskipun password sama.

## Cara Menggunakan

1.  **Install dependencies**:
    ```bash
    pip install cryptography
    ```
2.  **Jalankan program**:
    ```bash
    python encryptor.py
    ```
3.  **Enkripsi**:
    - Pilih opsi 1.
    - Masukkan path file (contoh: `rahasia.txt`).
    - Masukkan password.
    - Hasil: `rahasia.txt.enc`.
4.  **Dekripsi**:
    - Pilih opsi 2.
    - Masukkan path file enc (contoh: `rahasia.txt.enc`).
    - Masukkan password yang SAMA.
    - Hasil: `rahasia.txt` (kembali normal).

## Catatan
- Jangan LUPA password! File tidak bisa dibuka tanpa password yang benar.
- Salt di-generate otomatis, jadi aman.
