#!/usr/bin/env python3
"""
Download FireRed/LeafGreen assets from public GitHub repositories.
"""

import urllib.request
import os
import json
from pathlib import Path

OUTPUT_DIR = Path("/home/ubuntu/clawd/pokemon-game/assets/tilesets")

# Known sources for FRLG assets (public repos with extracted sprites)
SOURCES = {
    # PokeAPI sprites (official-ish)
    "pokemon_front": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/firered-leafgreen/",
    "pokemon_back": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-iii/firered-leafgreen/back/",
    
    # Decomp project (has tilesets)
    "decomp_tilesets": "https://raw.githubusercontent.com/pret/pokefirered/master/graphics/tilesets/",
    
    # Veekun (comprehensive sprite database)
    "veekun": "https://veekun.com/static/pokedex/downloads/",
}

# Pokemon IDs for Gen 1 (1-151) + some extras
POKEMON_IDS = list(range(1, 152))

def download_file(url, filepath):
    """Download file from URL"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        return False

def main():
    print("🎮 Pokemon FireRed/LeafGreen Asset Downloader (GitHub Sources)")
    print("=" * 60)
    
    # Create directories
    pokemon_dir = OUTPUT_DIR / "pokemon"
    pokemon_dir.mkdir(parents=True, exist_ok=True)
    
    # Download Pokemon front sprites
    print(f"\n📥 Downloading Pokemon front sprites (Gen 1)...")
    downloaded = 0
    for pid in POKEMON_IDS:
        url = f"{SOURCES['pokemon_front']}{pid}.png"
        filepath = pokemon_dir / f"{pid:03d}_front.png"
        if download_file(url, filepath):
            downloaded += 1
            if downloaded % 20 == 0:
                print(f"   ✅ {downloaded}/{len(POKEMON_IDS)} sprites downloaded...")
    print(f"   ✅ Downloaded {downloaded} front sprites")
    
    # Download Pokemon back sprites  
    print(f"\n📥 Downloading Pokemon back sprites...")
    downloaded_back = 0
    for pid in POKEMON_IDS:
        url = f"{SOURCES['pokemon_back']}{pid}.png"
        filepath = pokemon_dir / f"{pid:03d}_back.png"
        if download_file(url, filepath):
            downloaded_back += 1
    print(f"   ✅ Downloaded {downloaded_back} back sprites")
    
    # Download decomp tilesets
    print(f"\n📥 Downloading tilesets from pokefirered decomp...")
    tilesets_to_download = [
        ("primary/general/tiles.png", "general_tiles.png"),
        ("primary/building/tiles.png", "building_tiles.png"),
        ("secondary/pallet_town/tiles.png", "pallet_town.png"),
        ("secondary/viridian/tiles.png", "viridian.png"),
        ("secondary/pewter/tiles.png", "pewter.png"),
        ("secondary/route1/tiles.png", "route1.png"),
        ("secondary/oaks_lab/tiles.png", "oaks_lab.png"),
        ("secondary/house/tiles.png", "house_interior.png"),
        ("secondary/mart/tiles.png", "mart.png"),
        ("secondary/pokemon_center/tiles.png", "pokemon_center.png"),
    ]
    
    tilesets_dir = OUTPUT_DIR
    downloaded_tiles = 0
    for remote, local in tilesets_to_download:
        url = f"{SOURCES['decomp_tilesets']}{remote}"
        filepath = tilesets_dir / local
        if download_file(url, filepath):
            print(f"   ✅ {local}")
            downloaded_tiles += 1
        else:
            print(f"   ⚠️ {local} (not found)")
    
    print(f"\n✅ Downloaded {downloaded_tiles} tilesets")
    
    # Summary
    total_files = len(list(OUTPUT_DIR.rglob('*.png')))
    total_size = sum(f.stat().st_size for f in OUTPUT_DIR.rglob('*.png') if f.is_file())
    print(f"\n" + "=" * 60)
    print(f"📊 Summary:")
    print(f"   📁 Total files: {total_files}")
    print(f"   💾 Total size: {total_size / 1024 / 1024:.2f} MB")
    print(f"   📂 Location: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
