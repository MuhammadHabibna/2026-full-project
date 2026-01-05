import time
import winsound
from plyer import notification

# Konfigurasi Default (Bisa diubah)
DEFAULT_MINUTES = 25

def pomodoro_timer(minutes):
    """
    Menjalankan timer hitung mundur dan memberikan notifikasi saat selesai.
    """
    total_seconds = int(minutes * 60)
    
    print(f"\n🚀 Fokus dimulai selama {minutes} menit! Semangat! 🚀\n")
    
    try:
        while total_seconds > 0:
            mins, secs = divmod(total_seconds, 60)
            timer_format = f"{mins:02d}:{secs:02d}"
            
            # Print dengan end='\r' untuk menimpa baris yang sama (efek jam digital)
            print(f"⏳ Waktu Tersisa: {timer_format}", end='\r')
            
            time.sleep(1)
            total_seconds -= 1
            
        # Waktu habis!
        print(f"⏳ Waktu Tersisa: 00:00", end='\r') # Pastikan angka akhir terlihat
        print("\n\n✅ Selesai! Waktu Istirahat!")
        
        # 1. Bunyikan Suara Beep
        # Frekuensi 1000Hz, Durasi 1000ms (1 detik)
        winsound.Beep(1000, 1000)
        
        # 2. Tampilkan Notifikasi Desktop
        notification.notify(
            title="Pomodoro Timer Selesai!",
            message="Waktu Habis! Istirahat dulu bro ☕",
            app_name="Pomodoro Python",
            timeout=10
        )
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Timer dihentikan oleh pengguna.")

def main():
    print("="*40)
    print("🍅  SIMPLE POMODORO TIMER  🍅")
    print("="*40)
    
    try:
        user_input = input(f"Masukkan waktu fokus (menit) [Default: {DEFAULT_MINUTES}]: ")
        
        if user_input.strip() == "":
            minutes = DEFAULT_MINUTES
        else:
            minutes = float(user_input)
            
        if minutes <= 0:
            print("❌ Harap masukkan angka lebih dari 0.")
            return

        pomodoro_timer(minutes)
        
    except ValueError:
        print("❌ Error: Input harus berupa angka.")

if __name__ == "__main__":
    main()
