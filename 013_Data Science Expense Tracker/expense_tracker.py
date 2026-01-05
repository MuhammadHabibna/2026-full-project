import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Data Science Expense Tracker - Day 13

CSV_FILE = 'keuangan.csv'

def init_csv():
    """Inisialisasi file CSV jika belum ada"""
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['Tanggal', 'Item', 'Kategori', 'Harga'])
        df.to_csv(CSV_FILE, index=False)
        print(f"File {CSV_FILE} berhasil dibuat!\n")

def tambah_data():
    """Menu [1] - Tambah data pengeluaran"""
    print("\n--- TAMBAH PENGELUARAN ---")
    
    item = input("Nama Item: ").strip()
    kategori = input("Kategori (Makan/Transport/Hobi/dll): ").strip()
    
    while True:
        try:
            harga = float(input("Harga (Rp): "))
            break
        except ValueError:
            print("Harga harus berupa angka! Coba lagi.")
    
    tanggal = datetime.now().strftime('%Y-%m-%d')
    
    data_baru = {
        'Tanggal': tanggal,
        'Item': item,
        'Kategori': kategori,
        'Harga': harga
    }
    
    df = pd.read_csv(CSV_FILE)
    df = pd.concat([df, pd.DataFrame([data_baru])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    
    print(f"\n[SUCCESS] Berhasil simpan: {item} (Rp {harga:,.0f})\n")

def laporan_visualisasi():
    """Menu [2] - Laporan & Visualisasi Data"""
    df = pd.read_csv(CSV_FILE)
    
    if df.empty:
        print("\n[INFO] Belum ada data pengeluaran. Tambahkan data terlebih dahulu!\n")
        return
    
    print("\n" + "=" * 60)
    print("LAPORAN PENGELUARAN PER KATEGORI")
    print("=" * 60)
    
    ringkasan = df.groupby('Kategori')['Harga'].sum().sort_values(ascending=False)
    
    for kategori, total in ringkasan.items():
        print(f"{kategori:.<30} Rp {total:>15,.0f}")
    
    total_semua = ringkasan.sum()
    print("-" * 60)
    print(f"{'TOTAL':.<30} Rp {total_semua:>15,.0f}")
    print("=" * 60)
    
    plt.figure(figsize=(10, 7))
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0']
    
    plt.pie(ringkasan.values, 
            labels=ringkasan.index, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors[:len(ringkasan)],
            textprops={'fontsize': 11})
    
    plt.title('Distribusi Pengeluaran Saya', fontsize=16, fontweight='bold', pad=20)
    plt.axis('equal')
    
    print("\n[INFO] Menampilkan Pie Chart...\n")
    plt.tight_layout()
    plt.show()

def main():
    """Main program"""
    init_csv()
    
    while True:
        print("=" * 60)
        print("*** DATA SCIENCE EXPENSE TRACKER ***")
        print("=" * 60)
        print("[1] Tambah Pengeluaran")
        print("[2] Laporan & Visualisasi")
        print("[0] Keluar")
        print("=" * 60)
        
        pilihan = input("Pilih menu: ").strip()
        
        if pilihan == '1':
            tambah_data()
        elif pilihan == '2':
            laporan_visualisasi()
        elif pilihan == '0':
            print("\n[INFO] Terima kasih! Program selesai.\n")
            break
        else:
            print("\n[ERROR] Pilihan tidak valid! Pilih 1, 2, atau 0.\n")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("INSTALASI LIBRARY:")
    print("pip install pandas matplotlib")
    print("=" * 60 + "\n")
    
    main()
