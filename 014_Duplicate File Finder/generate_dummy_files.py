import os
import shutil
import random

# Script Generator Dummy File untuk Testing Day 14
TARGET_DIR = "target_scan_files"

def create_dummy_content(size_kb=1):
    """Membuat konten random dengan ukuran tertentu KB"""
    return os.urandom(size_kb * 1024)

def setup_dummy_files():
    if os.path.exists(TARGET_DIR):
        shutil.rmtree(TARGET_DIR)
    os.makedirs(TARGET_DIR)
    
    print(f"[FOLDER] Membuat folder dummy di: {os.path.abspath(TARGET_DIR)}\n")

    # 1. Foto Liburan (Ada duplikat)
    dir_foto = os.path.join(TARGET_DIR, "Foto Liburan")
    os.makedirs(dir_foto)
    
    content_foto_A = create_dummy_content(size_kb=500) # 500KB
    content_foto_B = create_dummy_content(size_kb=700) # 700KB
    
    # Simpan file asli
    with open(os.path.join(dir_foto, "IMG_2024_001.jpg"), "wb") as f: f.write(content_foto_A)
    with open(os.path.join(dir_foto, "IMG_2024_002.jpg"), "wb") as f: f.write(content_foto_B)
    
    # Buat duplikat dengan nama beda
    with open(os.path.join(dir_foto, "IMG_2024_001 - Copy.jpg"), "wb") as f: f.write(content_foto_A)
    print("[OK] Grup Foto Liburan: 2 file asli, 1 duplikat.")

    # 2. Dokumen Kerja (Nested folder & duplikat banyak)
    dir_kerja = os.path.join(TARGET_DIR, "Dokumen Kerja")
    os.makedirs(dir_kerja)
    
    content_laporan = b"Laporan Keuangan Q1 2024 - DRAFT FINAL REVISI" * 1000
    
    # Asli di root folder kerja
    with open(os.path.join(dir_kerja, "Laporan_Q1.docx"), "wb") as f: f.write(content_laporan)
    
    # Duplikat di subfolder "Old"
    dir_kerja_old = os.path.join(dir_kerja, "Old Backup")
    os.makedirs(dir_kerja_old)
    with open(os.path.join(dir_kerja_old, "Laporan_Q1_Backup.docx"), "wb") as f: f.write(content_laporan)
    with open(os.path.join(dir_kerja_old, "Copy of Laporan.docx"), "wb") as f: f.write(content_laporan)
    
    print("[OK] Grup Dokumen Kerja: 1 file asli, 2 duplikat (di subfolder).")

    # 3. File Random Unik (Tidak ada duplikat)
    dir_lain = os.path.join(TARGET_DIR, "Lain-lain")
    os.makedirs(dir_lain)
    with open(os.path.join(dir_lain, "notes.txt"), "w") as f: f.write("Belanja sayur hari ini")
    with open(os.path.join(dir_lain, "todolist.txt"), "w") as f: f.write("Coding Day 14")
    print("[OK] Grup Lain-lain: 2 file unik.")
    
    print("\n[DONE] Selesai! Folder siap discan.")
    print(f"--> Path untuk dicopy: {os.path.abspath(TARGET_DIR)}")

if __name__ == "__main__":
    setup_dummy_files()
