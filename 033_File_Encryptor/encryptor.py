import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a URL-safe base64-encoded key from the password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_file(filepath: str, password: str):
    """Encrypt a file and save it with .enc extension."""
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return

    # Generate a random 16-byte salt
    salt = os.urandom(16)
    key = derive_key(password, salt)
    f = Fernet(key)

    with open(filepath, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    # Save salt + encrypted data
    output_path = filepath + ".enc"
    with open(output_path, "wb") as file:
        file.write(salt + encrypted_data)

    print(f"File encrypted successfully: {output_path}")

def decrypt_file(filepath: str, password: str):
    """Decrypt a .enc file and restore it."""
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return
    
    if not filepath.endswith(".enc"):
        print("Warning: File does not have .enc extension. Proceeding anyway.")

    with open(filepath, "rb") as file:
        data = file.read()

    # Extract salt (first 16 bytes)
    salt = data[:16]
    encrypted_data = data[16:]

    key = derive_key(password, salt)
    f = Fernet(key)
    
    try:
        decrypted_data = f.decrypt(encrypted_data)
        
        # Determine output filename (remove .enc)
        if filepath.endswith(".enc"):
            output_path = filepath[:-4]
        else:
            output_path = filepath + ".decrypted"
            
        with open(output_path, "wb") as file:
            file.write(decrypted_data)
            
        print(f"File decrypted successfully: {output_path}")
        
    except Exception as e:
        print("Error: Decryption failed. Wrong password or corrupted file.")
        # print(f"Debug Info: {e}")

def main():
    print("=== Simple File Encryptor (AES) ===")
    print("1. Encrypt File")
    print("2. Decrypt File")
    
    choice = input("Choose option (1/2): ")
    
    if choice == '1':
        filepath = input("Enter file path to encrypt: ").strip('"') # Strip quotes for ease
        password = input("Enter password: ")
        encrypt_file(filepath, password)
    elif choice == '2':
        filepath = input("Enter file path to decrypt: ").strip('"')
        password = input("Enter password: ")
        decrypt_file(filepath, password)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
