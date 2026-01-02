from rembg import remove
from PIL import Image
import matplotlib.pyplot as plt
import os
import sys


def remove_background(input_path, output_path=None):
    try:
        # Validasi file inputt
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"File tidak ditemukan: {input_path}")
        
        # Validasi ekstensi file
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
        file_ext = os.path.splitext(input_path)[1].lower()
        if file_ext not in valid_extensions:
            raise ValueError(f"Format file tidak didukung. Gunakan: {', '.join(valid_extensions)}")
        
        print(f"Memproses gambar: {input_path}")
        
        # Baca gambar input
        input_image = Image.open(input_path)
        
        # Proses penghapusan background
        print("Menghapus background...")
        output_image = remove(input_image)
        
        # Generate nama file output jika tidak diberikan
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = f"{base_name}_no_bg.png"
        
        # Pastikan output adalah PNG untuk transparansi
        if not output_path.lower().endswith('.png'):
            output_path = os.path.splitext(output_path)[0] + '.png'
        
        # Simpan hasil sebagai PNG
        output_image.save(output_path, format='PNG')
        print(f"Berhasil disimpan: {output_path}")
        
        return input_image, output_image
    
    except FileNotFoundError as e:
        print(f"\n{e}")
        print("Pastikan path file benar dan file ada di lokasi tersebut.")
        sys.exit(1)
    
    except ValueError as e:
        print(f"\n{e}")
        sys.exit(1)
    
    except Exception as e:
        print(f"\nTerjadi kesalahan: {str(e)}")
        sys.exit(1)


def visualize_before_after(input_image, output_image):
    print("Menampilkan visualisasi Before vs After...")
    
    # Buat figure dengan 2 subplot side-by-side
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    
    # Before (Original)
    axes[0].imshow(input_image)
    axes[0].set_title('BEFORE (Original)', fontsize=14, fontweight='bold', pad=10)
    axes[0].axis('off')
    
    # After (Background Removed)
    axes[1].imshow(output_image)
    axes[1].set_title('AFTER (Background Removed)', fontsize=14, fontweight='bold', pad=10)
    axes[1].axis('off')
    
    # Styling
    plt.suptitle('Day 3: Hapus Background Foto Otomatis', 
                 fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    
    # Tampilkan
    plt.show()


def main():
    print("=" * 60)
    print("Day 3: Hapus Background Foto Otomatis")
    print("=" * 60)
    
    # Input dari user
    if len(sys.argv) > 1:
        # Jika path diberikan sebagai argument
        input_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        # Input interaktif
        input_path = input("Masukkan path gambar input: ").strip()
        output_path = input("Masukkan path output (tekan Enter untuk auto): ").strip()
        output_path = output_path if output_path else None
    
    # Proses penghapusan background
    input_image, output_image = remove_background(input_path, output_path)
    
    # Visualisasi hasil
    visualize_before_after(input_image, output_image)
    
    print("\n" + "=" * 60)
    print("Proses selesai!")
    print("=" * 60)


if __name__ == "__main__":
    main()
