import os
from PIL import Image
import sys
import time

def batch_resize_compress():
    print("="*50)
    print("    BATCH IMAGE RESIZER & COMPRESSOR (Day 19)")
    print("="*50)

    # 1. Get Input Folder
    input_folder = input("Drag & drop INPUT folder here (or type path): ").strip().strip('"').strip("'")
    if not os.path.exists(input_folder):
        print(f"[ERROR] Folder not found: {input_folder}")
        return

    # 2. Get Output Folder or Default
    default_output = os.path.join(input_folder, "Optimized")
    output_folder = input(f"Output folder [Enter for '{default_output}']: ").strip().strip('"').strip("'")
    if not output_folder:
        output_folder = default_output

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 3. Settings
    try:
        target_width_str = input("Target Width (px) [Enter for 1920]: ")
        target_width = int(target_width_str) if target_width_str else 1920
        
        quality_str = input("Compression Quality (1-100) [Enter for 80]: ")
        quality = int(quality_str) if quality_str else 80
    except ValueError:
        print("[ERROR] Invalid number. Using defaults (1920px, 80).")
        target_width = 1920
        quality = 80

    # 4. Process Images
    supported_exts = ('.jpg', '.jpeg', '.png', '.webp', '.bmp')
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(supported_exts)]
    
    if not files:
        print("[INFO] No matching images found in folder.")
        return

    print(f"\n[INFO] Found {len(files)} images. Starting process...\n")
    
    total_saved_bytes = 0
    start_time = time.time()

    for idx, filename in enumerate(files, 1):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        try:
            # Open Image
            with Image.open(input_path) as img:
                # Convert to RGB (in case of PNG with transparency if saving as JPG, 
                # but we'll try to keep extension or force specific handling if needed)
                # For this simple tool, we keep format unless it's strictly RGBA->JPG related issue.
                # To be safe for web optimization, let's keep original format but handle RGBA for JPEG.
                
                original_format = img.format
                
                # Resize Logic (Maintain Aspect Ratio)
                w_percent = (target_width / float(img.size[0]))
                
                # Only resize if image is larger than target
                if w_percent < 1:
                    h_size = int((float(img.size[1]) * float(w_percent)))
                    img = img.resize((target_width, h_size), Image.Resampling.LANCZOS)
                
                # Handling PNG with transparency -> if user wants jpg, we need background. 
                # But here we just save as original extension.
                
                # Save
                img.save(output_path, optimize=True, quality=quality)

            # Stats
            original_size = os.path.getsize(input_path)
            new_size = os.path.getsize(output_path)
            saved = original_size - new_size
            total_saved_bytes += saved
            
            percent = (saved / original_size) * 100 if original_size > 0 else 0
            
            print(f"[{idx}/{len(files)}] {filename}")
            print(f"      Before: {original_size/1024:.1f} KB -> After: {new_size/1024:.1f} KB")
            print(f"      Saved: {percent:.1f}%")

        except Exception as e:
            print(f"[ERROR] Failed to process {filename}: {e}")

    # Summary
    elapsed = time.time() - start_time
    print("\n" + "="*50)
    print("    COMPLETION SUMMARY")
    print("="*50)
    print(f"Files Processed: {len(files)}")
    print(f"Total Space Saved: {total_saved_bytes / (1024*1024):.2f} MB")
    print(f"Time Elapsed: {elapsed:.2f} seconds")
    print(f"Output Folder: {output_folder}")
    print("="*50)
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    batch_resize_compress()
