import os
import hashlib
import sys

# ========================================
# DUPLICATE FILE FINDER & CLEANER - DAY 14
# Detect & Remove Duplicates by Content
# ========================================

def get_file_hash(filepath, block_size=65536):
    """
    Menghitung MD5 hash dari file.
    Membaca file dalam blok-blok kecil agar hemat RAM untuk file besar.
    """
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read(block_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(block_size)
        return hasher.hexdigest()
    except (OSError, IOError) as e:
        print(f"[ERROR] Tidak bisa membaca file {filepath}: {e}")
        return None

def scan_directory(folder_path):
    """
    Scan folder dan sub-folder untuk mencari duplikat.
    """
    print(f"\n[SCAN] Sedang memindai: {folder_path} ...")
    
    # Dictionary untuk menyimpan {hash: [list_file_path]}
    hashes = {}
    total_files = 0
    
    # Walk through directory
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            
            # Skip file sistem/hidden jika perlu, tapi fokus ke semua file
            
            file_hash = get_file_hash(filepath)
            if file_hash:
                if file_hash not in hashes:
                    hashes[file_hash] = []
                hashes[file_hash].append(filepath)
                total_files += 1
                
                # Visual feedback sederhana (print dot)
                if total_files % 10 == 0:
                    print(".", end="", flush=True)

    print("\n[OK] Scan selesai!")
    return hashes

def process_duplicates(hashes):
    """
    Memproses hasil scan dan menampilkan laporan.
    Mengembalikan list file yang aman untuk dihapus.
    """
    duplicates = []
    total_waste_size = 0
    
    print("\n" + "=" * 60)
    print("LAPORAN FILE DUPLIKAT")
    print("=" * 60)
    
    found_any = False
    
    for file_hash, file_list in hashes.items():
        if len(file_list) > 1:
            found_any = True
            
            # Sort file agar yang "asli" (biasanya nama terpendek) ada di awal
            # Contoh: "foto.jpg" (asli) vs "foto - Copy.jpg" (copy)
            file_list.sort(key=len)
            
            original = file_list[0]
            copies = file_list[1:]
            
            file_size = os.path.getsize(original)
            waste_size = file_size * len(copies)
            total_waste_size += waste_size
            
            print(f"\n[FILE] File: {os.path.basename(original)}")
            print(f"   Ukuran: {file_size / 1024:.2f} KB | Hash: {file_hash[:8]}...")
            print(f"   [KEEP] Asli (Dipertahankan): {original}")
            for copy in copies:
                print(f"   [DEL]  Duplikat (Akan dihapus): {copy}")
                duplicates.append(copy)
    
    if not found_any:
        print("\n[INFO] Tidak ditemukan file duplikat sama sekali!")
        return [], 0
        
    print("\n" + "-" * 60)
    print(f"RINGKASAN:")
    print(f"   Total File Duplikat : {len(duplicates)} file")
    print(f"   Potensi Hemat Ruang : {total_waste_size / (1024 * 1024):.2f} MB")
    print("-" * 60)
    
    return duplicates, total_waste_size

def main():
    print("=" * 60)
    print("PYTHON DUPLICATE FILE FINDER & CLEANER")
    print("=" * 60)
    
    folder_path = input("Masukkan Path Folder untuk discan: ").strip()
    
    # Hapus tanda kutip jika user melakukan copy path as pathh ("C:\...")
    folder_path = folder_path.replace('"', '')
    
    if not os.path.exists(folder_path):
        print("\n[ERROR] Folder tidak ditemukan!")
        return

    hashes = scan_directory(folder_path)
    files_to_delete, saved_space = process_duplicates(hashes)
    
    if not files_to_delete:
        return

    print("\n[PILIHAN TINDAKAN]")
    print("[1] Hapus Semua File Duplikat (Hanya simpan yang Asli)")
    print("[2] Biarkan Saja & Keluar")
    
    pilihan = input("\nPilihan Anda (1/2): ").strip()
    
    if pilihan == '1':
        confirm = input(f"[WARNING] Yakin ingin menghapus {len(files_to_delete)} file? (y/n): ").strip().lower()
        if confirm == 'y':
            print("\nMemulai penghapusan...")
            deleted_count = 0
            for filepath in files_to_delete:
                try:
                    os.remove(filepath)
                    print(f"[DELETED] Dihapus: {filepath}")
                    deleted_count += 1
                except OSError as e:
                    print(f"[ERROR] Gagal menghapus {filepath}: {e}")
            
            print("\n" + "=" * 60)
            print(f"SUKSES! Bersih-bersih selesai.")
            print(f"   {deleted_count} file dihapus.")
            print(f"   Ruang penyimpanan hemat: {saved_space / (1024 * 1024):.2f} MB")
            print("=" * 60)
        else:
            print("\n[INFO] Penghapusan dibatalkan.")
    else:
        print("\n[INFO] Tidak ada file yang dihapus. Program selesai.")

if __name__ == "__main__":
    # Library hashlib dan os adalah bawaan Python, tidak perlu install
    main()
