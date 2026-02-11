#!/usr/bin/env python3
"""
Download FireRed/LeafGreen assets from Spriters-Resource using cloudscraper.
"""

import cloudscraper
import os
import re
import time
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.spriters-resource.com"
GAME_URL = f"{BASE_URL}/game_boy_advance/pokemonfireredleafgreen/"
OUTPUT_DIR = Path("/home/ubuntu/clawd/pokemon-game/assets/tilesets")

# Create scraper that bypasses Cloudflare
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'linux',
        'desktop': True
    }
)

def get_page(url, retries=3):
    """Fetch page with retries"""
    for i in range(retries):
        try:
            response = scraper.get(url, timeout=30)
            if response.status_code == 200:
                return response
            print(f"  ⚠️ HTTP {response.status_code}, retry {i+1}/{retries}")
        except Exception as e:
            print(f"  ⚠️ Error: {e}, retry {i+1}/{retries}")
        time.sleep(2)
    return None

def download_file(url, filepath):
    """Download file from URL"""
    try:
        response = scraper.get(url, timeout=60)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"    ❌ Download failed: {e}")
    return False

def main():
    print("🎮 Pokemon FireRed/LeafGreen Asset Downloader")
    print("=" * 60)
    
    # Fetch main page
    print(f"\n📥 Fetching {GAME_URL}...")
    response = get_page(GAME_URL)
    
    if not response:
        print("❌ Failed to fetch main page")
        return
    
    print("✅ Page loaded successfully!")
    
    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all sheet links (they have /sheet/ in href)
    sheet_links = soup.find_all('a', href=re.compile(r'/sheet/\d+'))
    
    print(f"\n📦 Found {len(sheet_links)} sprite sheets")
    
    # Categories based on name patterns
    categories = {
        'pokemon': ['pokemon', 'front', 'back', 'icon', 'party'],
        'characters': ['trainer', 'player', 'npc', 'overworld', 'sprite'],
        'battles': ['battle', 'background', 'arena'],
        'tilesets': ['tileset', 'tile', 'terrain', 'outdoor', 'indoor'],
        'cities': ['city', 'town', 'pallet', 'viridian', 'pewter', 'cerulean'],
        'routes': ['route', 'road', 'forest', 'cave', 'mountain'],
        'houses': ['house', 'building', 'interior', 'room', 'mart', 'center'],
        'animated': ['anim', 'water', 'flower', 'flame']
    }
    
    downloaded = 0
    
    for link in sheet_links:
        href = link.get('href')
        name = link.get_text(strip=True)
        
        if not href or not name:
            continue
        
        # Determine category
        name_lower = name.lower()
        category = 'misc'
        for cat, keywords in categories.items():
            if any(kw in name_lower for kw in keywords):
                category = cat
                break
        
        # Create category directory
        cat_dir = OUTPUT_DIR / category
        cat_dir.mkdir(parents=True, exist_ok=True)
        
        # Get sheet page to find download link
        sheet_url = urljoin(BASE_URL, href)
        print(f"\n📄 [{category}] {name}")
        print(f"   → {sheet_url}")
        
        sheet_response = get_page(sheet_url)
        if not sheet_response:
            print("   ❌ Failed to load sheet page")
            continue
        
        sheet_soup = BeautifulSoup(sheet_response.text, 'html.parser')
        
        # Find download link
        download_link = sheet_soup.find('a', href=re.compile(r'/download/\d+'))
        if not download_link:
            print("   ⚠️ No download link found")
            continue
        
        download_url = urljoin(BASE_URL, download_link.get('href'))
        
        # Extract sheet ID for filename
        sheet_id = re.search(r'/(\d+)', href)
        sheet_id = sheet_id.group(1) if sheet_id else 'unknown'
        
        # Clean filename
        safe_name = re.sub(r'[^\w\-]', '_', name)[:50]
        filename = f"{sheet_id}_{safe_name}.png"
        filepath = cat_dir / filename
        
        # Download
        print(f"   ⬇️ Downloading to {filename}...")
        if download_file(download_url, filepath):
            size_kb = filepath.stat().st_size / 1024
            print(f"   ✅ Downloaded ({size_kb:.1f} KB)")
            downloaded += 1
        else:
            print("   ❌ Download failed")
        
        # Rate limiting
        time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print(f"✅ Downloaded {downloaded}/{len(sheet_links)} assets")
    
    # Summary
    total_size = sum(f.stat().st_size for f in OUTPUT_DIR.rglob('*.png') if f.is_file())
    print(f"💾 Total size: {total_size / 1024 / 1024:.1f} MB")
    print(f"📂 Location: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
