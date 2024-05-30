from PIL import Image, ImageDraw, ImageFont
import os

def generate_banner(title, description, layout, background_image_path, logo_image_path, output_path):
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

    # Resize logo to make it larger
    logo_size_factor = 1.5
    logo = logo.resize((int(logo.width * logo_size_factor), int(logo.height * logo_size_factor)), Image.Resampling.LANCZOS)

    draw = ImageDraw.Draw(background)

    # Set font and size (ensure you have a font file, e.g., Arial.ttf)
    font_path = "arial.ttf"  # Update this path to the font file you have
    h1_size = 150  # Equivalent to H1 size
    h3_size = 90  # Equivalent to H3 size
    width, height = background.size

    # Get fonts for title and description
    title_font = ImageFont.truetype(font_path, h1_size)
    desc_font = ImageFont.truetype(font_path, h3_size)

    # Calculate text bounding boxes
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width, title_height = title_bbox[2] - title_bbox[0], title_bbox[3] - title_bbox[1]

    # Wrap the description text
    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        while words:
            line = ''
            while words and draw.textbbox((0, 0), line + words[0], font=font)[2] <= max_width:
                line += (words.pop(0) + ' ')
            lines.append(line.strip())
        return lines

    wrapped_text = wrap_text(description, desc_font, width - 40)  # Adjusted for more padding
    line_height = draw.textbbox((0, 0), 'A', font=desc_font)[3] - draw.textbbox((0, 0), 'A', font=desc_font)[1]
    text_height = line_height * len(wrapped_text)

    # Position for the title with margin
    title_margin = 50  # Adjust this value to change the margin
    title_position = ((width - title_width) // 2, title_margin)

    # Position for the description text
    if layout == "center":
        text_position = (50, (height - text_height) // 2)
    elif layout == "top":
        text_position = ((width - text_height) // 2, title_height + 60)
    elif layout == "bottom":
        text_position = ((width - text_height) // 2, height - text_height - 40)
    else:
        text_position = (50, (height - text_height) // 2)

    # Position for the logo with margin
    logo_margin = 50  # Adjust this value to change the margin
    logo_position = (logo_margin, logo_margin)

    # Draw the title on the background image
    draw.text(title_position, title, (255, 255, 255), font=title_font)

    # Draw the wrapped description text
    current_height = text_position[1]
    for line in wrapped_text:
        draw.text((text_position[0], current_height), line, (255, 255, 255), font=desc_font)
        current_height += line_height

    # Paste the logo on the background image
    background.paste(logo, logo_position, logo)

    # Convert background image to RGB before saving as JPEG
    rgb_background = background.convert("RGB")
    rgb_background.save(output_path, format='JPEG')
    print(f"Banner saved to {output_path}")


if __name__ == "__main__":
    title = "New Life Of the Ocean"
    description = "The error you're encountering, OSError: cannot write mode RGBA as JPEG, is due to the fact that JPEG format does not support transparency (the alpha channel), which is part of the RGBA mode. Since you're working with images that might have transparency and want to save the final image as JPEG, you need to convert the image mode from RGBA to RGB before saving it."
    layout = "center"  # Options: center, top, bottom
    background_image_path = "imgs/123333.jpg"  # Update this path
    logo_image_path = "imgs/2222.png"  # Update this path to your logo image
    output_path = "banner.jpg"

    generate_banner(title, description, layout, background_image_path, logo_image_path, output_path)
