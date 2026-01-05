import pandas as pd
import matplotlib.pyplot as plt

# Test script untuk melihat laporan dan chart
CSV_FILE = 'keuangan.csv'

df = pd.read_csv(CSV_FILE)

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

print("\n[INFO] Menampilkan Pie Chart...")
plt.tight_layout()
plt.savefig('chart_preview.png', dpi=100, bbox_inches='tight')
print("[INFO] Chart disimpan sebagai 'chart_preview.png'\n")
