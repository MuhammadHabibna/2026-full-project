from gtts import gTTS
import os
import platform

def text_to_speech():
    print("=== Text-to-Speech Converter (Bahasa Indonesia) ===")
    
    # 1. Input: Minta user memasukkan kalimat
    text = input("Masukkan kalimat: ")
    
    if not text:
        print("Teks tidak boleh kosong!")
        return

    try:
        # 2. Proses: Ubah teks menjadi suara (bahasa Indonesia)
        print("Sedang memproses suara...")
        tts = gTTS(text=text, lang='id')
        
        # 3. Output: Simpan hasilnya
        filename = "hasil_suara.mp3"
        tts.save(filename)
        print(f"Berhasil disimpan sebagai: {filename}")
        
        # 4. Auto-Play: Putar audio secara otomatis
        print("Memutar audio...")
        
        # Cek sistem operasi untuk command play yang sesuai
        if platform.system() == "Windows":
            os.startfile(filename)
        elif platform.system() == "Darwin": # macOS
            os.system(f"afplay {filename}")
        else: # Linux
            os.system(f"xdg-open {filename}")
            
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    text_to_speech()
