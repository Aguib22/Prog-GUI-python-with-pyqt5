#!/usr/bin/env python3
"""
Génère un petit jeu d'images .jpg dans le sous-dossier `images/` pour tester TP4_base.py.
Usage (PowerShell):
    pip install pillow
    python .\make_sample_images.py

Le script crée 3 images 900x900 composées d'une grille 3x3 et sauvegarde dans images/.
"""
from PIL import Image, ImageDraw, ImageFont
import os

images_dir = os.path.join(os.path.dirname(__file__), 'images')
os.makedirs(images_dir, exist_ok=True)

colors = [(220,20,60), (30,144,255), (34,139,34), (255,165,0), (148,0,211), (255,192,203), (210,180,140), (0,206,209), (255,255,0)]

for idx in range(1,4):
    img = Image.new('RGB', (900, 900), (0,0,0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    # draw 3x3 patches of 300x300
    patch = 0
    for y in range(0, 900, 300):
        for x in range(0, 900, 300):
            color = colors[patch % len(colors)]
            draw.rectangle([x, y, x+300-1, y+300-1], fill=color)
            # label
            text = f"Img{idx}-P{patch+1}"
            tw, th = draw.textsize(text, font=font)
            draw.text((x+10, y+10), text, fill=(255,255,255), font=font)
            patch += 1
    filename = os.path.join(images_dir, f'image_{idx}.jpg')
    img.save(filename, 'JPEG', quality=85)
    print('Wrote', filename)

print('Created sample images in', images_dir)
