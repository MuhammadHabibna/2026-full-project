import json
import os
from datetime import datetime

# ========================================
# LINK COLLECTOR (BOOKMARK MANAGER) - DAY 16
# Simpan & Cari Link Favoritmu
# ========================================

DB_FILE = 'bookmarks.json'

def load_data():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_link():
    print("\n🔗 TAMBAH LINK BARU")
    url = input("URL Link   : ").strip()
    if not url: return
    
    judul = input("Judul/Ket  : ").strip()
    tags = input("Tags (koma): ").strip().lower() # misal: coding, python, tutorial
    
    tag_list = [t.strip() for t in tags.split(',') if t.strip()]
    
    entry = {
        "url": url,
        "title": judul,
        "tags": tag_list,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    data = load_data()
    data.append(entry)
    save_data(data)
    print(f"✅ Link berhasil disimpan! (Total: {len(data)})")

def search_by_tag():
    print("\n🔍 CARI BERDASARKAN TAG")
    keyword = input("Masukkan Tag: ").strip().lower()
    
    data = load_data()
    results = [d for d in data if keyword in d['tags']]
    
    if not results:
        print(f"❌ Tidak ditemukan link dengan tag '{keyword}'")
        return

    print(f"\n✨ Ditemukan {len(results)} link untuk tag '{keyword}':")
    print("-" * 50)
    
    for i, item in enumerate(results, 1):
        print(f"{i}. {item['title']}")
        print(f"   🌍 {item['url']}")
        print(f"   🏷️  [{', '.join(item['tags'])}] | 📅 {item['date']}")
        print("-" * 50)

def main():
    while True:
        print("\n" + "=" * 40)
        print("🔖 CLI LINK COLLECTOR")
        print("=" * 40)
        print("[1] Tambah Link")
        print("[2] Cari Link by Tag")
        print("[3] Tampilkan Semua")
        print("[0] Keluar")
        
        pilihan = input("\nPilih Menu: ").strip()
        
        if pilihan == '1':
            add_link()
        elif pilihan == '2':
            search_by_tag()
        elif pilihan == '3':
            data = load_data()
            print(f"\n📂 TOTAL KOLEKSI: {len(data)} Links")
            for item in data:
                print(f"- {item['title']} ({item['url']})")
        elif pilihan == '0':
            print("Bye! 👋")
            break
        else:
            print("Pilihan salah!")

if __name__ == "__main__":
    main()
