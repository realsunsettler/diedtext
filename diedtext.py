import sys
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_echo_text(draw, text, font, position, color, iterations=3, offset=3):
    for i in range(iterations, 0, -1):
        alpha = int(50 / iterations * i)  # Reduced alpha for more fading
        echo_color = color + (alpha,)
        echo_pos = (position[0] - offset * i, position[1])  # Only horizontal offset
        draw.text(echo_pos, text, font=font, fill=echo_color)

def create_faded_background(img, text_height, y_position):
    background = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(background)
    
    mina, innera, edgeh = 0, 150, 20
    total_height = text_height + edgeh*2  # Text height + 20px above and below
    y_start = int(y_position - edgeh)
    y_end = int(y_start + total_height)

    for y in range(y_start, y_end):
        if y < y_start + edgeh:
            alpha = int(0 + (y - y_start) * (innera/edgeh))  # Fade from 50 to 150
        elif y > y_end - edgeh:
            alpha = int(innera - (y - (y_end - edgeh)) * (innera/edgeh))  # Fade from 150 to 50
        else:
            alpha = innera
        draw.line([(0, y), (img.width, y)], fill=(0, 0, 0, alpha))
    
    return background

def overlay_text(image_path, text):
    with Image.open(image_path).convert('RGBA') as img:
        # Create a new RGBA image with the same size
        txt = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)
        
        # Load the font
        font_size = int(img.width / 10)
        font = ImageFont.truetype("OptimusPrinceps.ttf", font_size)
        
        # Get text size
        text_width, text_height = draw.textsize(text, font=font)
        
        # Calculate position (centered)
        position = ((img.width - text_width) / 2, (img.height - text_height) / 2)
        
        # Create faded background
        background = create_faded_background(img, text_height, position[1])
        
        # Create echo effect
        create_echo_text(draw, text, font, position, (255, 215, 0), iterations=5, offset=3)
        
        # Draw main text
        draw.text(position, text, font=font, fill=(255, 215, 0, 255))  # Golden color
        
        # Combine the original image, background, and text with echo
        result = Image.alpha_composite(img, background)
        result = Image.alpha_composite(result, txt)
        
        # Save the result as PNG
        output_path = os.path.splitext(image_path)[0] + "_output.png"
        result.save(output_path, format='PNG')
        print(f"Image saved as {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py 'Your Text' /path/to/image.jpg")
        sys.exit(1)
    
    text = sys.argv[1]
    image_path = sys.argv[2]
    overlay_text(image_path, text)