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
python3 -m json.tool assets/data/map_headers.json >/dev/null
python3 -m json.tool assets/data/map_events.json >/dev/null
python3 -m json.tool assets/data/map_scripts.json >/dev/null
python3 -m json.tool assets/data/metatile_behaviors.json >/dev/null

echo "[ci-check] JSON sprites..."
python3 -m json.tool assets/sprites/user.sprites.json >/dev/null

echo "[ci-check] JS syntax from index.html <script>..."
awk 'BEGIN{p=0} /<script>/{p=1;next} /<\/script>/{p=0} p{print}' index.html > /tmp/pokemon_game_script_ci.js
node --check /tmp/pokemon_game_script_ci.js

echo "[ci-check] Asset preflight..."
python3 tools/asset_preflight.py

echo "[ci-check] Gameplay preflight..."
node tools/gameplay_preflight.js

echo "[ci-check] Map reachability preflight..."
node tools/map_reachability_preflight.js

echo "[ci-check] MapBG preflight..."
node tools/mapbg_preflight.js

echo "[ci-check] Map headers preflight..."
node tools/map_headers_preflight.js

echo "[ci-check] Map events preflight..."
node tools/map_events_preflight.js

echo "[ci-check] Map scripts preflight..."
node tools/map_scripts_preflight.js

echo "[ci-check] Metatile behavior preflight..."
node tools/metatile_behavior_preflight.js

echo "[ci-check] Intro preflight..."
node tools/intro_preflight.js

echo "[ci-check] Story motion preflight..."
node tools/story_motion_preflight.js

echo "[ci-check] Journey preflight..."
node tools/journey_preflight.js

echo "[ci-check] Full season preflight..."
node tools/full_season_preflight.js

echo "[ci-check] Story inline sync..."
node tools/story_inline_sync_preflight.js

echo "[ci-check] Story fidelity audit..."
node tools/story_fidelity_audit.js

echo "[ci-check] QA master preflight..."
node tools/qa_master_preflight.js

echo "[ci-check] Warp pair preflight..."
node tools/warp_pair_preflight.js

echo "[ci-check] Runtime hardening preflight..."
node tools/runtime_hardening_preflight.js

echo "[ci-check] Pokefirered practices audit..."
node tools/pokefirered_practices_audit.js

echo "[ci-check] E2E audit..."
node tools/e2e_audit.js

echo "[ci-check] OK"
