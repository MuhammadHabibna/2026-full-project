import time
import random
from plyer import notification
import os

# ========================================
# DESKTOP QUOTE NOTIFIER - DAY 17
# Munculin motivasi di layar tiap X menit
# ========================================

FILE_QUOTES = 'quotes.txt'


def load_quotes():
    """Load quotes dari file txt"""
    default_quotes = [
        "Keep going!",
        "Jangan menyerah, error itu biasa!",
        "Istirahat dulu kalau pusing",
        "Satu baris code lagi!",
        "You are doing great!"
    ]
    
    if not os.path.exists(FILE_QUOTES):
        return default_quotes
        
    try:
        with open(FILE_QUOTES, 'r', encoding='utf-8') as f:
            # Ambil baris yang tidak kosong
            quotes = [line.strip() for line in f.readlines() if line.strip()]
            return quotes if quotes else default_quotes
    except Exception as e:
        print(f"[ERROR] Gagal baca file: {e}")
        return default_quotes

def show_notification(quote):
    """Menampilkan popup notifikasi"""
    try:
        # Pisahkan Quote dan Author jika ada pemisah " - "
        parts = quote.split(" - ")
        if len(parts) > 1:
            pesan = parts[0]
            judul = f"[QUOTE] {parts[1]}"
        else:
            pesan = quote
            judul = "[QUOTE] Daily Motivation"

        notification.notify(
            title=judul,
            message=pesan,
            app_name='Python Motivator',
            timeout=10,  # Notifikasi hilang setlah 10 detik
            # app_icon='icon.ico' # Opsional: Jika punya file icon.ico
        )
        print(f"[SENT] {judul}: {pesan}")
        
    except Exception as e:
        print(f"[ERROR] Gagal menampilkan notifikasi: {e}")

def main():
    print("=" * 50)
    print("RANDOM QUOTE NOTIFIER (OFFLINE)")
    print("=" * 50)
    
    try:
        input_menit = input("Set Interval Notifikasi (menit) [Default: 30]: ").strip()
        if not input_menit:
            menit = 30
        else:
            menit = float(input_menit)
    except ValueError:
        print("[!] Input tidak valid, menggunakan default 30 menit.")
        menit = 30
    
    interval_detik = menit * 60

    print(f"[*] Script berjalan di background...")
    print(f"[*] Interval: Setiap {menit} menit")
    print("[*] Tekan Ctrl+C untuk berhenti.")
    print("-" * 50)
    
    # Test notifikasi pertama saat start
    first_quote = "Selamat Coding! Semangat 365 Days Challenge!"
    show_notification(first_quote)
    
    try:
        while True:
            # Countdown
            for remaining in range(int(interval_detik), 0, -1):
                mins, secs = divmod(remaining, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                print(f"[*] Next quote in: {timer} ", end="\r")
                time.sleep(1)
            print(" " * 40, end="\r") # Clear line after countdown
            
            # Load ulang file tiap kali loop (biar bisa update quotes realtime)
            quotes = load_quotes()
            quote_pilihan = random.choice(quotes)
            
            show_notification(quote_pilihan)
            
    except KeyboardInterrupt:
        print("\n\n👋 Bye! Sampai jumpa lagi.")
        print("Script dihentikan.")

if __name__ == "__main__":
    # Perintah Install Library:
    # pip install plyer
    main()
