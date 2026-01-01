# Install: pip install qrcode[pil]
import qrcode

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Ganti dengan URL Anda
img = qrcode.make(url)
img.save("qrcode.png")
