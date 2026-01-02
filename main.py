"""
GitHub Identicon Generator

This module generates GitHub-style identicons based on user IDs.
It replicates GitHub's algorithm for creating unique visual identifiers.
"""

import hashlib
import colorsys
import numpy as np
import requests
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt


def get_real_github_identicon(username, forced_id=None):
    """
    Generate a GitHub-style identicon for a given username.
    
    This function fetches the user's GitHub ID, generates an MD5 hash,
    and creates a 5x5 symmetric identicon with colors derived from the hash.
    
    Args:
        username (str): GitHub username to generate identicon for
        forced_id (int, optional): Override user ID for testing purposes
        
    Returns:
        PIL.Image: Generated identicon image (420x420 pixels)
        
    Algorithm:
        1. Fetch user ID from GitHub API or use forced_id
        2. Generate MD5 hash of user ID
        3. Extract color values from hash (hue, saturation, lightness)
        4. Generate 5x5 grid pattern from hash nibbles
        5. Render symmetric pattern with calculated colors
    """
    
    # Retrieve GitHub user ID
    if forced_id:
        user_id = str(forced_id)
    else:
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)
        
        if response.status_code == 200:
            user_id = str(response.json()['id'])
            print(f"User found: {username} (ID: {user_id})")
        else:
            print(f"User '{username}' not found. Using fallback ID.")
            user_id = "170270"  # Default fallback ID

    # Generate MD5 hash from user ID
    hash_obj = hashlib.md5(user_id.encode('utf-8'))
    hex_hash = hash_obj.hexdigest()

    # Extract color components from hash
    # Uses last 7 characters (28 bits): [Hue: 3 chars][Saturation: 2 chars][Lightness: 2 chars]
    
    # Hue: 0-360 degrees color wheel position
    hue_hex = hex_hash[-7:-4]
    hue = int(hue_hex, 16) / 4095.0
    
    # Saturation: Base 65% with 0-20% reduction for earthy tones
    sat_hex = hex_hash[-4:-2]
    saturation = 0.65 - (int(sat_hex, 16) / 255.0) * 0.20
    
    # Lightness: Base 75% with 0-20% reduction for retro aesthetic
    lig_hex = hex_hash[-2:]
    lightness = 0.75 - (int(lig_hex, 16) / 255.0) * 0.20

    # Convert HLS to RGB (Python's colorsys uses HLS order)
    r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
    color = (int(r * 255), int(g * 255), int(b * 255))
    
    # Define background color
    background = (240, 240, 240)

    # Generate 5x5 grid pattern from hash
    # Uses first 15 nibbles (hexadecimal digits) to determine filled cells
    nibbles = [int(char, 16) for char in hex_hash[:15]]
    grid = np.zeros((5, 5), dtype=int)
    
    # Fill center column (nibbles 0-4)
    for i in range(5):
        if nibbles[i] % 2 == 0:
            grid[i, 2] = 1

    # Fill middle columns with symmetry (nibbles 5-9)
    for i in range(5):
        if nibbles[i + 5] % 2 == 0:
            grid[i, 1] = 1
            grid[i, 3] = 1

    # Fill outer columns with symmetry (nibbles 10-14)
    for i in range(5):
        if nibbles[i + 10] % 2 == 0:
            grid[i, 0] = 1
            grid[i, 4] = 1

    # Render identicon image
    size = 420
    padding = 35
    img = Image.new('RGB', (size, size), background)
    draw = ImageDraw.Draw(img)
    cell_size = (size - (2 * padding)) // 5
    
    # Draw filled cells
    for row in range(5):
        for col in range(5):
            if grid[row, col] == 1:
                x0 = padding + (col * cell_size)
                y0 = padding + (row * cell_size)
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                draw.rectangle([x0, y0, x1, y1], fill=color)

    return img


if __name__ == "__main__":
    # Generate and display identicon for test user
    target_user = "siddharth-narigra"
    img = get_real_github_identicon(target_user)
    
    plt.figure(figsize=(5, 5))
    plt.imshow(img)
    plt.axis('off')
    plt.title(f"GitHub Identicon: {target_user}")
    plt.show()