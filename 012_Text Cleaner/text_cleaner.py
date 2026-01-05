import re

# Python Text Cleaner - Membersihkan teks berantakan dengan Regex


def bersihkan_teks(teks):
    """Membersihkan teks berantakan menggunakan Regular Expression"""
    
    teks = teks.strip()
    teks = re.sub(r'  +', ' ', teks)
    teks = re.sub(r'(?<![.!?\n:])\n(?![\n*-])', ' ', teks)
    teks = re.sub(r'\n{3,}', '\n\n', teks)
    teks = re.sub(r'\n\s*[*-]\s+', '\n• ', teks)
    teks = re.sub(r'\s+([.,!?;:])', r'\1', teks)
    teks = re.sub(r'([.,!?;:])(?=[^\s\n])', r'\1 ', teks)
    
    return teks


# Main Program
print("=" * 60)
print("*** PYTHON TEXT CLEANER - REGEX POWER ***")
print("=" * 60)

print("\nPaste teks berantakan Anda (tekan Enter 2x untuk selesai):")
print("-" * 60)

lines = []
while True:
    try:
        line = input()
        if line == "" and len(lines) > 0 and lines[-1] == "":
            break
        lines.append(line)
    except EOFError:
        break

teks_kotor = '\n'.join(lines)

print("\n--- TEKS ASLI (BERANTAKAN) ---\n")
print(teks_kotor)

teks_bersih = bersihkan_teks(teks_kotor)

print("\n" + "=" * 60)
print("--- HASIL BERSIH (RAPI) ---\n")
print(teks_bersih)

print("\n" + "=" * 60)
print("[SUCCESS] Teks berhasil dibersihkan dalam hitungan detik!")
print("=" * 60)
