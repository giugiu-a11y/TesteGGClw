#!/usr/bin/env python3
"""
Download all assets from Spriters-Resource Pokemon FireRed/LeafGreen folder.
Passes Cloudflare using Playwright (headless browser).
"""

import asyncio
import os
import sys
from pathlib import Path
from urllib.parse import urljoin

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright not installed. Run: pip install playwright")
    sys.exit(1)

BASE_URL = "https://www.spriters-resource.com/game_boy_advance/pokemonfireredleafgreen/"
OUTPUT_DIR = Path("/home/ubuntu/clawd/pokemon-game/assets/tilesets")

# Asset categories (based on typical structure)
CATEGORIES = {
    "pokemon": "Pokémon sprites (battle front/back)",
    "characters": "NPC & trainer sprites",
    "tilesets": "Environmental tilesets",
    "battles": "Battle backgrounds",
    "houses": "Building/house interiors",
    "routes": "Route/outdoor terrain",
    "cities": "City maps",
    "animated": "Animated tiles"
}

async def download_assets():
    async with async_playwright() as p:
        # Launch headless browser with stealth
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        print(f"🌐 Fetching {BASE_URL}...")
        await page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
        
        # Extract all download links
        print("📥 Extracting download links...")
        links = await page.evaluate("""
            () => {
                const links = [];
                document.querySelectorAll('a[href*="download"], a[href*="/files/"]').forEach(a => {
                    const href = a.getAttribute('href');
                    const text = a.innerText.trim();
                    if (href && text) {
                        links.push({ href, text });
                    }
                });
                return links;
            }
        """)
        
        print(f"✅ Found {len(links)} download links")
        
        # Group by category
        assets_by_category = {cat: [] for cat in CATEGORIES}
        for link in links:
            text = link['text'].lower()
            for cat in CATEGORIES:
                if cat in text:
                    assets_by_category[cat].append(link)
                    break
            else:
                # Unclassified
                if 'assets_by_category.get("other")' not in assets_by_category:
                    assets_by_category["other"] = []
                assets_by_category["other"].append(link)
        
        # Download & organize
        for category, items in assets_by_category.items():
            if not items:
                continue
            
            cat_dir = OUTPUT_DIR / category
            cat_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"\n📦 {category.upper()} ({len(items)} items)")
            print(f"   → {cat_dir}")
            
            for i, item in enumerate(items, 1):
                url = urljoin(BASE_URL, item['href'])
                filename = item['text'].replace(' ', '_')[:50]  # Limit name length
                
                try:
                    response = await page.request.get(url)
                    if response.ok:
                        filepath = cat_dir / filename
                        with open(filepath, 'wb') as f:
                            f.write(await response.body())
                        print(f"   ✅ [{i}/{len(items)}] {filename}")
                    else:
                        print(f"   ❌ [{i}/{len(items)}] {filename} (HTTP {response.status})")
                except Exception as e:
                    print(f"   ⚠️  [{i}/{len(items)}] {filename} ({str(e)[:30]})")
        
        await browser.close()
        
        # Summary
        print("\n" + "="*60)
        print("✅ Download complete!")
        print(f"📂 Assets saved to: {OUTPUT_DIR}")
        total_size = sum(f.stat().st_size for f in OUTPUT_DIR.rglob('*') if f.is_file())
        print(f"💾 Total size: {total_size / 1024 / 1024:.1f} MB")

if __name__ == "__main__":
    try:
        asyncio.run(download_assets())
    except KeyboardInterrupt:
        print("\n⏹️  Cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
