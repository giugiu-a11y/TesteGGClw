#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[gameplay-preflight] FAIL: ${msg}`);
  process.exit(1);
}

const root = path.resolve(__dirname, '..');
const indexPath = path.join(root, 'index.html');
if (!fs.existsSync(indexPath)) fail('index.html missing');
const html = fs.readFileSync(indexPath, 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) fail('main <script> block not found');
const script = m[1];

function grabConst(name) {
  const rx = new RegExp(`const\\s+${name}\\s*=\\s*([\\s\\S]*?);\\n\\s*\\n`);
  const mm = script.match(rx);
  if (!mm) fail(`const ${name} not found`);
  return mm[1];
}

const T = eval(`(${grabConst('T')})`);
const SOLID = eval(grabConst('SOLID'));

const start = script.indexOf('const MAPS = {');
if (start < 0) fail('MAPS not found');
let i = script.indexOf('{', start);
let depth = 0;
let end = -1;
for (; i < script.length; i++) {
  const ch = script[i];
  if (ch === '{') depth++;
  else if (ch === '}') {
    depth--;
    if (depth === 0) {
      end = i;
      break;
    }
  }
}
if (end < 0) fail('MAPS parse failed');
const MAPS = eval(`(${script.slice(script.indexOf('{', start), end + 1)})`);
const mapIds = Object.keys(MAPS);

function tileAt(map, x, y) {
  return map.data[y * map.w + x];
}

function isWalkable(map, x, y) {
  if (x < 0 || y < 0 || x >= map.w || y >= map.h) return false;
  const t = tileAt(map, x, y);
  return !SOLID.includes(t);
}

let issueCount = 0;
function issue(msg) {
  issueCount++;
  console.error(`[gameplay-preflight] ISSUE: ${msg}`);
}

for (const [id, map] of Object.entries(MAPS)) {
  if (!map || !Number.isInteger(map.w) || !Number.isInteger(map.h) || !Array.isArray(map.data)) {
    issue(`map ${id} malformed`);
    continue;
  }
  if (map.data.length !== map.w * map.h) {
    issue(`map ${id} data len ${map.data.length} != ${map.w * map.h}`);
  }

  for (const npc of map.npcs || []) {
    if (!isWalkable(map, npc.x, npc.y)) {
      issue(`npc on non-walkable tile in ${id} at (${npc.x},${npc.y})`);
    }
  }

  for (const w of map.warps || []) {
    if (!MAPS[w.to]) {
      issue(`${id} warp target map missing: ${w.to}`);
      continue;
    }
    if (w.x < 0 || w.y < 0 || w.x >= map.w || w.y >= map.h) {
      issue(`${id} warp source out of bounds (${w.x},${w.y})`);
    } else {
      const src = tileAt(map, w.x, w.y);
      if (src !== T.WARP) {
        issue(`${id} warp source not on WARP tile at (${w.x},${w.y}) type=${src}`);
      }
    }

    const dst = MAPS[w.to];
    if (w.tx < 0 || w.ty < 0 || w.tx >= dst.w || w.ty >= dst.h) {
      issue(`${id} warp -> ${w.to} destination out of bounds (${w.tx},${w.ty})`);
    } else if (!isWalkable(dst, w.tx, w.ty)) {
      issue(`${id} warp -> ${w.to} destination blocked (${w.tx},${w.ty})`);
    }
  }
}

// Door-entry checks for key interiors: source warp should be directly under a building facade tile.
const DOOR_EXPECTED = new Set(['player_house', 'rival_house', 'oak_lab', 'pewter_gym']);
const BUILDING_TOP_TILES = new Set([T.HOUSE_RED, T.HOUSE_BLUE, T.LAB, T.WALL_IN]);
for (const [id, map] of Object.entries(MAPS)) {
  for (const w of map.warps || []) {
    if (!DOOR_EXPECTED.has(w.to)) continue;
    const ay = w.y - 1;
    const above = ay >= 0 ? tileAt(map, w.x, ay) : null;
    if (!BUILDING_TOP_TILES.has(above)) {
      issue(`${id} -> ${w.to} warp at (${w.x},${w.y}) is not aligned to a building door`);
    }
  }
}

// Runtime should be strict local-only assets (no remote sprite/tileset URLs).
if (/https?:\/\//i.test(script)) {
  issue('external URL found in runtime script');
}

if (issueCount > 0) {
  fail(`${issueCount} issue(s) found`);
}

console.log(`[gameplay-preflight] OK maps=${mapIds.length}`);
