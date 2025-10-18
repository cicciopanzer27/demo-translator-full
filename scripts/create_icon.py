#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Crea un'icona semplice per il Traduttore LAC
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_translator_icon():
    """Crea icona 256x256 per il traduttore"""
    
    # Dimensione icona
    size = 256
    
    # Crea immagine con sfondo nero
    img = Image.new('RGB', (size, size), color='#000000')
    draw = ImageDraw.Draw(img)
    
    # Disegna cerchio bianco (bordo)
    padding = 20
    draw.ellipse(
        [padding, padding, size-padding, size-padding],
        outline='#FFFFFF',
        width=8
    )
    
    # Testo IT
    try:
        # Prova a usare font Arial bold
        font_large = ImageFont.truetype("arial.ttf", 80)
        font_small = ImageFont.truetype("arial.ttf", 40)
    except:
        # Fallback a font default
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Disegna "IT" al centro (grande)
    text_it = "IT"
    bbox = draw.textbbox((0, 0), text_it, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) / 2
    y = (size - text_height) / 2 - 20
    draw.text((x, y), text_it, fill='#FFFFFF', font=font_large)
    
    # Disegna frecce (↔)
    text_arrows = "↔"
    bbox_arrows = draw.textbbox((0, 0), text_arrows, font=font_small)
    arrows_width = bbox_arrows[2] - bbox_arrows[0]
    x_arrows = (size - arrows_width) / 2
    y_arrows = y + text_height + 10
    draw.text((x_arrows, y_arrows), text_arrows, fill='#FFFFFF', font=font_small)
    
    # Salva come PNG
    png_path = Path(__file__).parent / "translator_icon.png"
    img.save(png_path, 'PNG')
    print(f"Icona PNG creata: {png_path}")
    
    # Converti a ICO (multiple sizes per Windows)
    try:
        icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        images = []
        
        for icon_size in icon_sizes:
            img_resized = img.resize(icon_size, Image.Resampling.LANCZOS)
            images.append(img_resized)
        
        ico_path = Path(__file__).parent / "translator_icon.ico"
        images[0].save(ico_path, format='ICO', sizes=icon_sizes)
        print(f"Icona ICO creata: {ico_path}")
        
        return str(ico_path)
    
    except Exception as e:
        print(f"Errore creazione ICO: {e}")
        print("Usa solo PNG")
        return str(png_path)

if __name__ == "__main__":
    try:
        icon_path = create_translator_icon()
        print(f"\nIcona pronta: {icon_path}")
        print("\nPer applicare l'icona al collegamento, esegui:")
        print("  .\\scripts\\update_shortcut_icon.ps1")
    except ImportError:
        print("Installa Pillow per creare icone:")
        print("  .\\venv\\Scripts\\pip install Pillow")

