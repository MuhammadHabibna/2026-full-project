# Local Search Engine

Mesin pencari lokal sederhana untuk file teks/code Anda.

## Fitur
- **Indexing Cepat**: Membaca file `.txt`, `.md`, `.py`, `.html`, `.css`, `.js`.
- **Inverted Index**: Pencarian sangat cepat `O(1)` setelah indexing.
- **Snippet Preview**: Menampilkan baris kode/teks yang mengandung kata kunci.

## Cara Menggunakan

1.  **Install dependencies**:
    ```bash
    pip install rich
    ```
2.  **Jalankan program**:
    ```bash
    python search_engine.py
    ```
3.  **Scan**: Masukkan path folder yang mau discan (default: folder `365days` induk).
4.  **Search**: Ketik kata kunci, misal "def", "class", atau "day".

## Teknologi
- **Crawler**: `os.walk` untuk menjelajah folder.
- **Data Structure**: Dictionary sebagai Hash Map untuk Inverted Index.
