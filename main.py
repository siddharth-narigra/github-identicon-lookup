import hashlib
import colorsys
import numpy as np
import requests
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt


def get_real_github_identicon(username, forced_id=None):
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
            user_id = "170270"

    hash_obj = hashlib.md5(user_id.encode('utf-8'))
    hex_hash = hash_obj.hexdigest()

    hue_hex = hex_hash[-7:-4]
    hue = int(hue_hex, 16) / 4095.0
    
    sat_hex = hex_hash[-4:-2]
    saturation = 0.65 - (int(sat_hex, 16) / 255.0) * 0.20
    
    lig_hex = hex_hash[-2:]
    lightness = 0.75 - (int(lig_hex, 16) / 255.0) * 0.20

    r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
    color = (int(r * 255), int(g * 255), int(b * 255))
    
    background = (240, 240, 240)

    nibbles = [int(char, 16) for char in hex_hash[:15]]
    grid = np.zeros((5, 5), dtype=int)
    
    for i in range(5):
        if nibbles[i] % 2 == 0:
            grid[i, 2] = 1

    for i in range(5):
        if nibbles[i + 5] % 2 == 0:
            grid[i, 1] = 1
            grid[i, 3] = 1

    for i in range(5):
        if nibbles[i + 10] % 2 == 0:
            grid[i, 0] = 1
            grid[i, 4] = 1

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

    return img


if __name__ == "__main__":
    target_user = "siddharth-narigra"
    img = get_real_github_identicon(target_user)
    
    plt.figure(figsize=(5, 5))
    plt.imshow(img)
    plt.axis('off')
    plt.title(f"GitHub Identicon: {target_user}")
    plt.show()
