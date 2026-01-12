import hashlib
import colorsys
import numpy as np
from PIL import Image, ImageDraw

def generate_identicon_from_id(user_id: str) -> tuple:
    """
    Generate the identicon image and related data from a user ID.
    
    Args:
        user_id: The GitHub user ID (string or int)
        
    Returns:
        tuple: (PIL Image, dict of generation metadata)
    """
    metadata = {}
    
    # Generate hash from user ID
    hash_obj = hashlib.md5(str(user_id).encode('utf-8'))
    hex_hash = hash_obj.hexdigest()
    metadata['md5_hash'] = hex_hash
    
    # Extract color values from hash
    hue_hex = hex_hash[-7:-4]
    hue = int(hue_hex, 16) / 4095.0
    metadata['hue_segment'] = hue_hex
    
    sat_hex = hex_hash[-4:-2]
    saturation = 0.65 - (int(sat_hex, 16) / 255.0) * 0.20
    metadata['sat_segment'] = sat_hex
    
    lig_hex = hex_hash[-2:]
    lightness = 0.75 - (int(lig_hex, 16) / 255.0) * 0.20
    metadata['lig_segment'] = lig_hex
    
    r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
    color = (int(r * 255), int(g * 255), int(b * 255))
    metadata['color_rgb'] = color
    metadata['color_hex'] = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
    
    # Store pattern segment
    metadata['pattern_segment'] = hex_hash[:15]
    
    background = (240, 240, 240)
    
    # Generate 5x5 grid pattern
    nibbles = [int(char, 16) for char in hex_hash[:15]]
    grid = np.zeros((5, 5), dtype=int)
    
    # Center column
    for i in range(5):
        if nibbles[i] % 2 == 0:
            grid[i, 2] = 1
    
    # Second columns (symmetric)
    for i in range(5):
        if nibbles[i + 5] % 2 == 0:
            grid[i, 1] = 1
            grid[i, 3] = 1
    
    # Outer columns (symmetric)
    for i in range(5):
        if nibbles[i + 10] % 2 == 0:
            grid[i, 0] = 1
            grid[i, 4] = 1
    
    # Create image
    size = 420
    padding = 35
    img = Image.new('RGB', (size, size), background)
    draw = ImageDraw.Draw(img)
    cell_size = (size - (2 * padding)) // 5
    
    for row in range(5):
        for col in range(5):
            if grid[row, col] == 1:
                x0 = padding + (col * cell_size)
                y0 = padding + (row * cell_size)
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                draw.rectangle([x0, y0, x1, y1], fill=color)
                
    return img, metadata
