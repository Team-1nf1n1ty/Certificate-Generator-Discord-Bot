from PIL import Image, ImageDraw, ImageFont
from config import total_teams, name_position, team_position, place_position, max_name_width, max_team_width, max_position_width, font_path

def get_max_font_size(draw, text, font_path, max_width, initial_size=100):
    """Find the maximum font size that fits within the max width."""
    for size in range(initial_size, 0, -1):  # Decrease size
        font = ImageFont.truetype(font_path, size)
        # Get the bounding box of the text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]  # width = right - left
        if text_width <= max_width:
            return size, text_width
    return 1  # Return a minimum size if none fits

def create_certificate(template_path, name, place, team_name = 'THIS IS a TEST TEAM'):
    # Open the certificate template
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)

    team_name = '[ ' + team_name + ' ]'
    place = f"{place}/{total_teams}"

    # Get max font size
    name_font_size, name_width = get_max_font_size(draw, name, font_path, max_name_width, 60)
    team_font_size, team_width = get_max_font_size(draw, team_name, font_path, max_team_width, 50)
    place_font_size, place_width = get_max_font_size(draw, place, font_path, max_position_width, 40)

    # Create fonts with the determined sizes
    name_font = ImageFont.truetype(font_path, name_font_size)
    place_font = ImageFont.truetype(font_path, place_font_size)
    team_font = ImageFont.truetype(font_path, team_font_size)

    # Draw the text on the image
    draw.text((name_position[0] + max_name_width/2 - name_width/2, name_position[1]), name, fill="white", font=name_font)
    draw.text((team_position[0] + max_team_width/2 - team_width/2, team_position[1]), team_name, fill="white", font=team_font)
    draw.text((place_position[0] + max_position_width/2 - place_width/2, place_position[1]), place, fill="white", font=place_font)

    return image


