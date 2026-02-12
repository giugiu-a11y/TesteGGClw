#!/usr/bin/env python3
import json
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
MAPBG_MANIFEST = ROOT / "assets/tilesets/mapbg.manifest.json"
SCENE_MANIFEST = ROOT / "assets/tilesets/scene_backdrop.manifest.json"
SPRITES_JSON = ROOT / "assets/sprites/user.sprites.json"
STORY_JSON = ROOT / "story/season1.ptbr.json"


def fail(msg: str) -> None:
    print(f"[asset-preflight] FAIL: {msg}")
    sys.exit(1)


def load_json(path: pathlib.Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"invalid json {path}: {e}")


def check_file_exists(path: pathlib.Path) -> None:
    if not path.exists():
        fail(f"missing file: {path}")


def extract_maps(index_text: str):
    m = re.search(r"const MAPS = \{([\s\S]*?)\n\s*};\n", index_text)
    if not m:
        fail("MAPS block not found in index.html")
    block = m.group(1)
    ids = re.findall(r"^\s{8}([a-z0-9_]+):\s*\{", block, re.M)
    if not ids:
        fail("no map ids found in MAPS")
    return sorted(set(ids))


def check_mapbg_manifest(map_ids):
    data = load_json(MAPBG_MANIFEST)
    if "mapbg" not in data or not isinstance(data["mapbg"], dict):
        fail("mapbg.manifest.json missing 'mapbg' object")
    entries = data["mapbg"]
    missing = [m for m in map_ids if m != "story" and m not in entries]
    if missing:
        fail(f"mapbg manifest missing maps: {', '.join(missing)}")
    for map_id, conf in entries.items():
        url = conf.get("url")
        if not isinstance(url, str) or not url.startswith("./assets/"):
            fail(f"mapbg[{map_id}] has invalid url")
        target = ROOT / url[2:]
        check_file_exists(target)
        ts = conf.get("ts", 16)
        if not isinstance(ts, int) or ts <= 0:
            fail(f"mapbg[{map_id}] has invalid ts")


def check_sprites_manifest():
    data = load_json(SPRITES_JSON)
    sprites = data.get("sprites", {})
    if not isinstance(sprites, dict) or not sprites:
        fail("user.sprites.json has empty/non-object 'sprites'")
    for key, value in sprites.items():
        if isinstance(value, str) and value.startswith("./assets/"):
            check_file_exists(ROOT / value[2:])


def check_scene_manifest(story_ids):
    data = load_json(SCENE_MANIFEST)
    default = data.get("default")
    rules = data.get("rules")
    if not isinstance(default, str) or not default.startswith("./assets/"):
        fail("scene_backdrop.manifest.json invalid default")
    check_file_exists(ROOT / default[2:])
    if not isinstance(rules, list) or not rules:
        fail("scene_backdrop.manifest.json requires non-empty rules")
    compiled = []
    for i, rule in enumerate(rules):
        if not isinstance(rule, dict):
            fail(f"scene rule #{i} must be object")
        patt = rule.get("match")
        url = rule.get("url")
        if not isinstance(patt, str) or not patt.strip():
            fail(f"scene rule #{i} invalid match")
        if not isinstance(url, str) or not url.startswith("./assets/"):
            fail(f"scene rule #{i} invalid url")
        check_file_exists(ROOT / url[2:])
        try:
            compiled.append((re.compile(patt), url))
        except re.error as e:
            fail(f"scene rule #{i} regex error: {e}")

    # Ensure every beat can resolve to a backdrop (rule or default).
    for beat_id in story_ids:
        lowered = beat_id.lower()
        _resolved = default
        for rx, url in compiled:
            if rx.search(lowered):
                _resolved = url
                break


def main():
    check_file_exists(INDEX)
    check_file_exists(STORY_JSON)
    check_file_exists(MAPBG_MANIFEST)
    check_file_exists(SCENE_MANIFEST)
    check_file_exists(SPRITES_JSON)

    index_text = INDEX.read_text(encoding="utf-8")
    script_match = re.search(r"<script>([\s\S]*?)</script>", index_text)
    if not script_match:
        fail("main script block not found in index.html")
    runtime_script = script_match.group(1)
    if re.search(r"https?://", runtime_script):
        fail("external URL found in runtime script; strict local assets required")
    map_ids = extract_maps(index_text)
    story = load_json(STORY_JSON)
    beats = story.get("beats", [])
    story_ids = [b.get("id", "") for b in beats if isinstance(b, dict)]
    if not story_ids:
        fail("story has no beats")

    check_mapbg_manifest(map_ids)
    check_sprites_manifest()
    check_scene_manifest(story_ids)
    print("[asset-preflight] OK")


if __name__ == "__main__":
    main()
