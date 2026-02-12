#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "[ci-check] JSON story..."
python3 -m json.tool story/season1.ptbr.json >/dev/null

echo "[ci-check] JSON tileset..."
python3 -m json.tool assets/tilesets/punyworld.tileset.json >/dev/null
python3 -m json.tool assets/tilesets/user.tileset.json >/dev/null
python3 -m json.tool assets/tilesets/mapbg.manifest.json >/dev/null
python3 -m json.tool assets/tilesets/scene_backdrop.manifest.json >/dev/null

echo "[ci-check] JSON sprites..."
python3 -m json.tool assets/sprites/user.sprites.json >/dev/null

echo "[ci-check] JS syntax from index.html <script>..."
awk 'BEGIN{p=0} /<script>/{p=1;next} /<\/script>/{p=0} p{print}' index.html > /tmp/pokemon_game_script_ci.js
node --check /tmp/pokemon_game_script_ci.js

echo "[ci-check] Asset preflight..."
python3 tools/asset_preflight.py

echo "[ci-check] Gameplay preflight..."
node tools/gameplay_preflight.js

echo "[ci-check] Intro preflight..."
node tools/intro_preflight.js

echo "[ci-check] OK"
