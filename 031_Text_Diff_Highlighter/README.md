# Text Diff Highlighter

Alat sederhan untuk membandingkan dua teks dan melihat perbedaannya.

## Cara Menggunakan

1.  Pastikan Python sudah terinstall.
2.  Install library:
    ```bash
    pip install rich
    ```
3.  Jalankan program:
    ```bash
    python diff_highlighter.py
    ```
4.  Paste teks **Original** (Asli/Lama).
5.  Ketik `END` di baris baru lalu Enter.
6.  Paste teks **New** (Baru/Revisi).
7.  Ketik `END` di baris baru lalu Enter.

Output akan muncul:
- <span style="color:red">- Merah</span>: Menandakan baris yang dihapus.
- <span style="color:green">+ Hijau</span>: Menandakan baris yang ditambahkan.

Cocok untuk cek revisi artikel, kode, atau dokumen.
