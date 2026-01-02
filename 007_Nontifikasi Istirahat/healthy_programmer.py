import time
from plyer import notification

interval_detik = 10 


def jalankan_pengingat():
    print(f"Program 'Healthy Programmer' berjalan...")
    print(f"Notifikasi akan muncul setiap {interval_detik} detik.")
    print("Tekan Ctrl+C di terminal untuk menghentikan program.")

    try:
        while True:
            # Kirim notifikasi
            notification.notify(
                title="Jangan Lupa Minum! 🥤",
                message="Istirahat sejenak, regangkan badan, dan minum air putih. Coding butuh fokus, tapi kesehatan nomor satu!",
                app_name="Healthy Programmer",
                timeout=10  # Notifikasi hilang otomatis setelah 10 detik
            )
            
            # Print log ke terminal (opsional, biar tahu program masih jalan)
            print("Notifikasi terkirim! Menunggu interval berikutnya...")

            # Tunggu sesuai interval
            time.sleep(interval_detik)

    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna (Ctrl+C). Tetap sehat! 👋")

if __name__ == "__main__":
    jalankan_pengingat()
