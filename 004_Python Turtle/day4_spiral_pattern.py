import turtle
import colorsys

# Setup screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Day 4: Pola Spiral Geometris")

# Setup turtle
t = turtle.Turtle()
t.speed(0)  # Kecepatan maksimum
t.hideturtle()  # Sembunyikan kursor
t.width(2)

# Variabel untuk mengontrol pola
n = 36  # Jumlah iterasi
hue = 0  # Nilai awal untuk warna (HSV)

# Gambar spiral dengan warna pelangi
for i in range(360):
    # Konversi HSV ke RGB untuk efek pelangi
    color = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    t.pencolor(color)
    
    # Gambar gerakan spiral
    t.forward(i * 2)
    t.left(59)  # Sudut yang menciptakan pola menarik
    
    # Update warna untuk siklus pelangi
    hue += 0.005
    if hue >= 1.0:
        hue = 0

# Selesai - klik untuk menutup
screen.exitonclick()
