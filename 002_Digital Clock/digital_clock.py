import tkinter as tk
import time

# Update
def update_time():
    current_time = time.strftime('%H:%M:%S')
    clock_label.config(text=current_time)
    clock_label.after(1000, update_time)

# Main Window Setup
root = tk.Tk()
root.title("Modern Digital Clock")
root.geometry("500x200")
root.configure(bg='#1e1e1e')
root.resizable(False, False)

# Clock Label Design
clock_label = tk.Label(
    root,
    font=('Helvetica', 80, 'bold'),
    background='#1e1e1e',
    foreground='#00ffcc',  # Neon Cyan
    pady=20
)
clock_label.pack(expand=True)

# Start Clock
update_time()
root.mainloop()
