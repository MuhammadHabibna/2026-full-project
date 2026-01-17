# Smart Study Planner

Simple generator jadwal belajar otomatis berbasis deadline.

## Cara Menggunakan

1.  Pastikan Python sudah terinstall.
2.  Install library yang dibutuhkan:
    ```bash
    pip install rich
    ```
3.  Jalankan program:
    ```bash
    python study_planner.py
    ```
4.  Konfigurasi:
    - Masukkan jam belajar harian kamu.
    - Masukkan nama mata pelajaran/tugas.
    - Masukkan deadline (YYYY-MM-DD).
    - Masukkan estimasi butuh berapa jam.
    - Ketik `done` untuk selesai input.

## Contoh

Input:
- **Math**: Deadline 2026-01-20, Butuh 5 jam.
- **Physics**: Deadline 2026-01-25, Butuh 10 jam.
- **Daily Capacity**: 3 jam.

Output akan memprioritaskan Math di hari-hari awal, lalu menyicil Physics.

## Fitur
- **Prioritas Otomatis**: Tugas dengan deadline terdekat dikerjakan duluan.
- **Visual Table**: Jadwal ditampilkan rapi 7 hari ke depan.
- **Warning**: Memberi peringatan jika jadwal terlalu padat dan tidak mungkin selesai tepat waktu.
