# Audio Metronome + Tap BPM

Metronome digital dengan fitur **Tap Tempo** untuk membantu musisi menemukan BPM lagu.

## Fitur
1.  **Tap Tempo**: Tekan SPASI berulang kali mengikuti irama lagu, BPM akan otomatis terdeteksi.
2.  **Audio Tick**: Suara "beep" akurat, dihasilkan secara real-time (tanpa file mp3 eksternal).
3.  **Visual Flash**: Layar berkedip saat beat berbunyi.

## Cara Menggunakan

1.  **Install dependencies**:
    ```bash
    pip install pygame numpy
    ```
2.  **Jalankan program**:
    ```bash
    python metronome.py
    ```
3.  **Kontrol**:
    - **SPACE**: Tap tempo (ketuk minimal 2-3 kali).
    - **ENTER**: Mulai / Stop metronome.
    - **PANAH ATAS/BAWAH**: Tambah/Kurang 1 BPM.
    - **PANAH KANAN/KIRI**: Tambah/Kurang 5 BPM.
