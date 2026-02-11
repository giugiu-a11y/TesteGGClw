#!/usr/bin/env python3
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "tilesets"
PTR_RE = re.compile(r"/home/ubuntu/.openclaw/media/inbound/file_[^\s]+?\.(?:png|jpg|jpeg|webp)")

resolved = 0
failed = []

for p in ASSETS.rglob("*.png"):
    try:
        raw = p.read_bytes()
    except Exception:
        continue

    # Broken placeholder files are tiny text blobs with an inbound path.
    if not raw or len(raw) >= 4096:
        continue
    if not raw.startswith(b"/home/ubuntu/.openclaw/media/inbound/"):
        continue

    text = raw.decode("utf-8", errors="ignore")
    cands = PTR_RE.findall(text)
    src = None
    for c in cands:
        cp = Path(c)
        if cp.exists() and cp.is_file():
            src = cp
            break

    if not src:
        failed.append(str(p.relative_to(ROOT)))
        continue

    shutil.copyfile(src, p)
    resolved += 1

print(f"resolved={resolved}")
if failed:
    print("failed:")
    for f in failed:
        print(f" - {f}")
