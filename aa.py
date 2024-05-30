from PIL import Image, ImageDraw, ImageFont
import os

def generate_banner(description, layout, background_image_path, logo_image_path, output_path):
    # Check if the background image exists
    if not os.path.exists(background_image_path):
        print(f"Error: The file {background_image_path} does not exist.")
        return
    
    # Check if the logo image exists
    if not os.path.exists(logo_image_path):
        print(f"Error: The file {logo_image_path} does not exist.")
        return

    # Open the background image
    try:
        background = Image.open(background_image_path).convert("RGBA")
    except Exception as e:
        print(f"Error opening background image: {e}")
        return

    # Open the logo image
    try:
        logo = Image.open(logo_image_path).convert("RGBA")
    except Exception as e:
        print(f"Error opening logo image: {e}")
        return

    draw = ImageDraw.Draw(background)

    # Set font and size (ensure you have a font file, e.g., Arial.ttf)
    font_path = "arial.ttf"  # Update this path to the font file you have
    max_font_size = 100  # Start with a large font size to find the best fit
    min_font_size = 10
    width, height = background.size

    # Adjust font size to fit text within the image width
    def get_font_size(text, max_width, max_font_size, min_font_size):
        font_size = max_font_size
        while font_size >= min_font_size:
            font = ImageFont.truetype(font_path, font_size)
            text_width, _ = draw.textbbox((0, 0), text, font=font)[2:4]
            if text_width <= max_width:
                return font
            font_size -= 1
        return ImageFont.truetype(font_path, min_font_size)

    font = get_font_size(description, width - 20, max_font_size, min_font_size)

    text_bbox = draw.textbbox((0, 0), description, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    # Position for the text
    if layout == "center":
        text_position = ((width - text_width) // 2, (height - text_height) // 2)
    elif layout == "top":
        text_position = ((width - text_width) // 2, logo.size[1] + 20)
    elif layout == "bottom":
        text_position = ((width - text_width) // 2, height - text_height - 20)
    else:
        text_position = (10, height - text_height - 20)

    # Position for the logo at the right corner
    logo_position = (width - logo.size[0] - 10, height - logo.size[1] - 10)

    # Draw the text on the background image
    draw.text(text_position, description, (255, 255, 255), font=font)

    # Paste the logo on the background image
    background.paste(logo, logo_position, logo)

    # Convert background image to RGB before saving as JPEG
    rgb_background = background.convert("RGB")
    rgb_background.save(output_path, format='JPEG')
    print(f"Banner saved to {output_path}")

if __name__ == "__main__":
    description = "The error you're encountering, OSError: cannot write mode RGBA as JPEG, is due to the fact that JPEG format does not support transparency (the alpha channel), which is part of the RGBA mode. Since you're working with images that might have transparency and want to save the final image as JPEG, you need to convert the image mode from RGBA to RGB before saving it."
    layout = "center"  # Options: center, top, bottom
    background_image_path = "imgs/123333.jpg"  # Update this path
    logo_image_path = "imgs/2222.png"  # Update this path to your logo image
    output_path = "banner.jpg"

    generate_banner(description, layout, background_image_path, logo_image_path, output_path)
