import speedtest
import sys
import time
import threading

def loading_animation(message, stop_event):
    chars = "/-\|"
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{message} {chars[i % len(chars)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r{message} \n")

def print_separator():
    print("-" * 50)

def main():
    print("\n")
    print_separator()
    print("      🚀 INTERNET SPEED TEST BY PYTHON 🚀      ")
    print_separator()
    print("Mohon tunggu sebentar, sedang inisialisasi...")

    stop_event = threading.Event()
    t = None

    try:
        # 1. Setup & Ping
        print("\n[1/3] Sedang mencari server terbaik...")
        stop_event.clear()
        t = threading.Thread(target=loading_animation, args=("Menghubungkan ke server...", stop_event))
        t.daemon = True # Panting: Agar thread mati jika program error/selesai
        t.start()
        
        st = speedtest.Speedtest()
        best = st.get_best_server()
        ping = best['latency']
        
        stop_event.set()
        t.join()
        print(f"      ✅ Ping: {ping:.2f} ms")

        # 2. Download
        stop_event.clear()
        print("\n[2/3] Sedang menguji kecepatan Download...")
        t = threading.Thread(target=loading_animation, args=("Testing Download...", stop_event))
        t.daemon = True
        t.start()
        
        download_raw = st.download()
        download_mbps = download_raw / 1_000_000
        
        stop_event.set()
        t.join()
        print(f"      ✅ Download: {download_mbps:.2f} Mbps")

        # 3. Upload
        stop_event.clear()
        print("\n[3/3] Sedang menguji kecepatan Upload...")
        t = threading.Thread(target=loading_animation, args=("Testing Upload...", stop_event))
        t.daemon = True
        t.start()
        
        upload_raw = st.upload()
        upload_mbps = upload_raw / 1_000_000
        
        stop_event.set()
        t.join()
        print(f"      ✅ Upload: {upload_mbps:.2f} Mbps")

        # Hasil Akhir
        print("\n")
        print_separator()
        print("                HASIL TES                    ")
        print_separator()
        print(f"🌐 Server   : {best['host']} ({best['country']})")
        print(f"📶 Ping     : {ping:.2f} ms")
        print(f"⬇️  Download : {download_mbps:.2f} Mbps")
        print(f"⬆️  Upload   : {upload_mbps:.2f} Mbps")
        print_separator()
        print("\n")

    except KeyboardInterrupt:
        stop_event.set()
        print("\n\n[!] Program dihentikan pengguna.")
    except Exception as e:
        stop_event.set()
        print(f"\n\n[!] Terjadi kesalahan: {e}")
        print("Saran: Coba jalankan 'pip uninstall speedtest speedtest-cli -y' lalu 'pip install speedtest-cli'")

if __name__ == "__main__":
    main()
