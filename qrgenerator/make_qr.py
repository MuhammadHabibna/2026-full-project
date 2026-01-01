import qrcode

url = input("Masukkan URL link: ")
img = qrcode.make(url)
img.save("qrcode.png")
