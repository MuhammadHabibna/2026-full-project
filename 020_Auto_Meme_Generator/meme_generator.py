from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import sys

def generate_meme(image_path, top_text, bottom_text, output_path="meme_result.jpg"):
    """
    Generates a meme by adding top and bottom text to an image.
    Uses 'Impact' font if available, otherwise defaults to arial.
    Adds a black stroke/outline to the white text for readability.
    """
    print(f"[INFO] Processing '{image_path}'...")

    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"[ERROR] Could not open image: {e}")
        return

    draw = ImageDraw.Draw(img)
    image_width, image_height = img.size

    # Load Font
    # Impact is the standard meme font. Windows usually has it.
    font_path = "impact.ttf"
    try:
        # Initial font size estimate based on image height
        font_size = int(image_height / 8)
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        print("[WARN] Impact font not found. Using default.")
        font_path = "arial.ttf" # Fallback
        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
             font = ImageFont.load_default()

    def draw_text_with_outline(draw, text, position, font):
        """Draws text with a black outline."""
        x, y = position
        
        # Split text into lines if it's too long
        # A simple approximation: max chars based on width
        # For a "masterpiece", we might want smarter wrapping, but this suffices for memes
        # Let's just convert case to Upper as is tradition
        text = text.upper()
        
        # Calculate text size using getbbox (left, top, right, bottom)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center X
        x = (image_width - text_width) / 2
        
        # Outline (Stroke) parameters
        stroke_width = int(font_size / 15)
        stroke_fill = "black"
        text_fill = "white"

        draw.text((x, y), text, font=font, fill=text_fill, stroke_width=stroke_width, stroke_fill=stroke_fill)
        return text_height

    # Draw Top Text
    if top_text:
        draw_text_with_outline(draw, top_text, (0, 10), font)

    # Draw Bottom Text
    if bottom_text:
        # We need height to position correctly at bottom
        # Recalculate size to find Y position
        bbox = draw.textbbox((0, 0), bottom_text.upper(), font=font)
        text_h = bbox[3] - bbox[1]
        y_pos = image_height - text_h - 20 # 20px padding from bottom
        draw_text_with_outline(draw, bottom_text, (0, y_pos), font)

    # Save
    try:
        img.save(output_path)
        print(f"[SUCCESS] Meme saved to '{output_path}'!")
        # Automatically open the result
        if os.name == 'nt':
            os.startfile(output_path)
    except Exception as e:
        print(f"[ERROR] Could not save image: {e}")

def main():
    print("="*40)
    print("      ULTIMATE MEME GENERATOR 3000      ")
    print("="*40)
    
    # Check for sample image if no args
    default_img = "sample_image.jpg"
    
    img_path = input(f"Image Path [Enter for '{default_img}']: ").strip().strip('"')
    if not img_path:
        img_path = default_img
    
    if not os.path.exists(img_path):
        print(f"[ERROR] Image '{img_path}' not found!")
        return

    top = input("Top Text    : ")
    bottom = input("Bottom Text : ")

    generate_meme(img_path, top, bottom)

if __name__ == "__main__":
    main()
