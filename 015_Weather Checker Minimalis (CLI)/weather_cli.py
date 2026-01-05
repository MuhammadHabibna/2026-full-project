import requests
import sys

# ========================================
# REAL-TIME WEATHER CLI - DAY 15
# Menggunakan Open-Meteo API (Gratis)
# ========================================

# Setup agar support emoji di terminal Windows
sys.stdout.reconfigure(encoding='utf-8')

def get_weather_emoji(wmo_code):
    """
    Mapping WMO Weather Code ke Emoji & Deskripsi
    Sumber: https://open-meteo.com/en/docs
    """
    if wmo_code == 0:
        return "☀️", "Cerah (Clear Sky)"
    elif wmo_code in [1, 2, 3]:
        return "⛅", "Berawan (Partly Cloudy)"
    elif wmo_code in [45, 48]:
        return "🌫️", "Berkabut (Foggy)"
    elif wmo_code in [51, 53, 55, 56, 57]:
        return "🌦️", "Gerimis (Drizzle)"
    elif wmo_code in [61, 63, 65, 66, 67, 80, 81, 82]:
        return "🌧️", "Hujan (Rain)"
    elif wmo_code in [71, 73, 75, 77, 85, 86]:
        return "❄️", "Salju (Snow)"
    elif wmo_code in [95, 96, 99]:
        return "⛈️", "Badai Petir (Thunderstorm)"
    else:
        return "🌈", "Lainnya"

def cek_cuaca():
    print("=" * 60)
    print("🌤️  PYTHON WEATHER CHECKER (CLI)")
    print("=" * 60)
    
    kota = input("Masukkan Nama Kota (misal: Jakarta, Surabaya): ").strip()
    
    if not kota:
        print("[ERROR] Nama kota tidak boleh kosong!")
        return

    print(f"\n🔍 Mencari koordinat kota '{kota}'...")
    
    try:
        # STEP 1: Geocoding API
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={kota}&count=1&language=id&format=json"
        geo_response = requests.get(geo_url).json()
        
        if not geo_response.get('results'):
            print(f"❌ Kota '{kota}' tidak ditemukan! Coba nama lain.")
            return

        lokasi = geo_response['results'][0]
        lat = lokasi['latitude']
        lon = lokasi['longitude']
        nama_lokasi = f"{lokasi['name']}, {lokasi.get('country', '')}"
        
        print(f"✅ Koordinat ditemukan: {nama_lokasi} ({lat}, {lon})")
        print("\n⏳ Mengambil data cuaca...")

        # STEP 2: Weather API
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_url).json()
        
        current = weather_response['current_weather']
        suhu = current['temperature']
        angin = current['windspeed']
        kode_cuaca = current['weathercode']
        
        # Mapping kondisi
        emoji, kondisi = get_weather_emoji(kode_cuaca)

        # OUTPUT VISUAL (KARTU)
        print("\n" + "=" * 40)
        print(f"📍  Cuaca di: {nama_lokasi}")
        print("-" * 40)
        print(f"🌡️  Suhu     : {suhu}°C")
        print(f"💨  Angin    : {angin} km/h")
        print(f"☁️  Kondisi  : {emoji} {kondisi}")
        print("=" * 40 + "\n")

    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] Gagal menghubungi API: {e}")
    except Exception as e:
        print(f"\n[ERROR] Terjadi kesalahan: {e}")

if __name__ == "__main__":
    cek_cuaca()
    
    # Perintah Instalasi Library
    # pip install requests
