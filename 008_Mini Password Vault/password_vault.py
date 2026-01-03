import os
import json
from cryptography.fernet import Fernet
from tabulate import tabulate

# Nama file
KEY_FILE = "secret.key"
DATA_FILE = "data_passwords.json"

def load_or_generate_key():
    """Memuat key jika ada, atau membuat baru jika belum ada."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        print(f"[INFO] Key baru dibuat dan disimpan di {KEY_FILE}")
    return key

def load_data():
    """Memuat data password dari file JSON."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []

def save_data(data):
    """Menyimpan data password ke file JSON."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def encrypt_password(cipher_suite, password):
    """Mengenkripsi password."""
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(cipher_suite, encrypted_password):
    """Mendekripsi password."""
    try:
        return cipher_suite.decrypt(encrypted_password.encode()).decode()
    except Exception:
        return "[ERROR: Decryption Failed]"

def add_account(cipher_suite):
    """Menambahkan akun baru."""
    print("\n--- Tambah Akun Baru ---")
    service = input("Nama Layanan (misal: Gmail): ")
    username = input("Username: ")
    password = input("Password: ")

    encrypted_password = encrypt_password(cipher_suite, password)

    data = load_data()
    data.append({
        "service": service,
        "username": username,
        "password": encrypted_password
    })
    save_data(data)
    print("\n[SUKSES] Akun berhasil disimpan!")

def view_accounts(cipher_suite):
    """Melihat daftar akun dengan password terdekripsi."""
    data = load_data()
    if not data:
        print("\n[INFO] Belum ada data tersimpan.")
        return

    table_data = []
    for item in data:
        decrypted_pass = decrypt_password(cipher_suite, item["password"])
        table_data.append([item["service"], item["username"], decrypted_pass])

    print("\n--- Daftar Password Anda ---")
    print(tabulate(table_data, headers=["Layanan", "Username", "Password"], tablefmt="grid"))

def main():
    key = load_or_generate_key()
    cipher_suite = Fernet(key)

    while True:
        print("\n=== MINI PASSWORD VAULT ===")
        print("1. Tambah Akun")
        print("2. Lihat Daftar Password")
        print("3. Keluar")
        
        choice = input("Pilih menu (1-3): ")

        if choice == '1':
            add_account(cipher_suite)
        elif choice == '2':
            view_accounts(cipher_suite)
        elif choice == '3':
            print("Sampai jumpa! Stay safe.")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
