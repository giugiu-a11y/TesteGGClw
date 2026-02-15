#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[e2e-audit] FAIL: ${msg}`);
  process.exit(1);
}

const root = path.resolve(__dirname, '..');
const indexPath = path.join(root, 'index.html');
const storyPath = path.join(root, 'story/season1.ptbr.json');
const mapbgPath = path.join(root, 'assets/tilesets/mapbg.manifest.json');
if (!fs.existsSync(indexPath)) fail('index.html missing');
if (!fs.existsSync(storyPath)) fail('story JSON missing');
if (!fs.existsSync(mapbgPath)) fail('mapbg manifest missing');

const html = fs.readFileSync(indexPath, 'utf8');
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) fail('main script not found');
const script = scriptMatch[1];
const story = JSON.parse(fs.readFileSync(storyPath, 'utf8'));
const mapbgManifest = JSON.parse(fs.readFileSync(mapbgPath, 'utf8'));
const mapbg = mapbgManifest && mapbgManifest.mapbg ? mapbgManifest.mapbg : {};

function extractConst(name) {
  const rx = new RegExp(`const\\s+${name}\\s*=\\s*([\\s\\S]*?);\\n\\s*\\n`);
  const m = script.match(rx);
  if (!m) fail(`const ${name} not found`);
  return m[1];
}

function extractMaps() {
  const start = script.indexOf('const MAPS = {');
  if (start < 0) fail('MAPS not found');
  let i = script.indexOf('{', start);
  let depth = 0;
  let end = -1;
  for (; i < script.length; i++) {
    const c = script[i];
    if (c === '{') depth++;
    else if (c === '}') {
      depth--;
      if (depth === 0) {
        end = i;
        break;
      }
    }
  }
  if (end < 0) fail('MAPS parse error');
  return eval(`(${script.slice(script.indexOf('{', start), end + 1)})`);
}

const T = eval(`(${extractConst('T')})`);
const SOLID = eval(extractConst('SOLID'));
const STRICT_CITY_MAPS = eval(extractConst('STRICT_CITY_MAPS'));
const STRICT_ROUTE_MAPS = eval(extractConst('STRICT_ROUTE_MAPS'));
const STRICT_FOREST_MAPS = eval(extractConst('STRICT_FOREST_MAPS'));
const STRICT_INTERIOR_MAPS = eval(extractConst('STRICT_INTERIOR_MAPS'));
const STRICT_CAVE_MAPS = eval(extractConst('STRICT_CAVE_MAPS'));
const CITY_STRICT_WALKABLE = eval(extractConst('CITY_STRICT_WALKABLE'));
const ROUTE_STRICT_WALKABLE = eval(extractConst('ROUTE_STRICT_WALKABLE'));
const FOREST_STRICT_WALKABLE = eval(extractConst('FOREST_STRICT_WALKABLE'));
const INTERIOR_STRICT_WALKABLE = eval(extractConst('INTERIOR_STRICT_WALKABLE'));
const CAVE_STRICT_WALKABLE = eval(extractConst('CAVE_STRICT_WALKABLE'));
const MAPS = extractMaps();

function strictSetForMap(mapId) {
  if (STRICT_CITY_MAPS.has(mapId)) return CITY_STRICT_WALKABLE;
  if (STRICT_ROUTE_MAPS.has(mapId)) return ROUTE_STRICT_WALKABLE;
  if (STRICT_FOREST_MAPS.has(mapId)) return FOREST_STRICT_WALKABLE;
  if (STRICT_INTERIOR_MAPS.has(mapId)) return INTERIOR_STRICT_WALKABLE;
  if (STRICT_CAVE_MAPS.has(mapId)) return CAVE_STRICT_WALKABLE;
  return null;
}

function inBounds(map, x, y) {
  return x >= 0 && y >= 0 && x < map.w && y < map.h;
}

function tileAt(map, x, y) {
  return map.data[y * map.w + x];
}

function isWalkable(mapId, x, y, ignoreNpc = false) {
    const map = MAPS[mapId];
    if (!map || !inBounds(map, x, y)) return false;
    const tile = tileAt(map, x, y);
    if (SOLID.includes(tile)) return false;
  const strict = strictSetForMap(mapId);
  if (strict && !strict.has(tile)) return false;
  if (!ignoreNpc) {
    for (const n of map.npcs || []) {
      if (n.x === x && n.y === y) return false;
    }
  }
  const conf = mapbg[mapId];
  const rects = conf && Array.isArray(conf.solidRects) ? conf.solidRects : [];
  for (const r of rects) {
    const rx = Number(r && r.x);
    const ry = Number(r && r.y);
    const rw = Number(r && r.w);
    const rh = Number(r && r.h);
    if (!Number.isFinite(rx) || !Number.isFinite(ry) || !Number.isFinite(rw) || !Number.isFinite(rh)) continue;
    if (x >= rx && x < rx + rw && y >= ry && y < ry + rh) return false;
  }
  return true;
}

function firstWalkable(mapId) {
  const map = MAPS[mapId];
  for (let y = 0; y < map.h; y++) {
    for (let x = 0; x < map.w; x++) {
      if (isWalkable(mapId, x, y, true)) return {x, y};
    }
  }
  return null;
}

function bfsReachable(mapId, sx, sy) {
  const map = MAPS[mapId];
  const seen = new Uint8Array(map.w * map.h);
  if (!isWalkable(mapId, sx, sy, true)) return seen;
  const q = [[sx, sy]];
  seen[sy * map.w + sx] = 1;
  for (let i = 0; i < q.length; i++) {
    const [x, y] = q[i];
    for (const [dx, dy] of [[1,0],[-1,0],[0,1],[0,-1]]) {
      const nx = x + dx;
      const ny = y + dy;
      if (!inBounds(map, nx, ny)) continue;
      const idx = ny * map.w + nx;
      if (seen[idx]) continue;
      if (!isWalkable(mapId, nx, ny, true)) continue;
      seen[idx] = 1;
      q.push([nx, ny]);
    }
  }
  return seen;
}

const issues = [];
const warnings = [];
function issue(msg) {
  issues.push(msg);
  console.error(`[e2e-audit] ISSUE: ${msg}`);
}
function warn(msg) {
  warnings.push(msg);
  console.warn(`[e2e-audit] WARN: ${msg}`);
}

// 1) Global map topology validation
for (const [mapId, map] of Object.entries(MAPS)) {
  if (!Array.isArray(map.data) || map.data.length !== map.w * map.h) {
    issue(`${mapId}: invalid data length`);
    continue;
  }
  const seed = firstWalkable(mapId);
  if (!seed) {
    issue(`${mapId}: no walkable tile`);
    continue;
  }
  const reach = bfsReachable(mapId, seed.x, seed.y);

  for (const w of map.warps || []) {
    if (!inBounds(map, w.x, w.y)) {
      issue(`${mapId}: warp source out-of-bounds (${w.x},${w.y})`);
      continue;
    }
    if (!MAPS[w.to]) {
      issue(`${mapId}: warp target map missing (${w.to})`);
      continue;
    }
    const dst = MAPS[w.to];
    if (!inBounds(dst, w.tx, w.ty)) {
      issue(`${mapId}: warp destination out-of-bounds ${w.to}(${w.tx},${w.ty})`);
      continue;
    }
    if (!isWalkable(mapId, w.x, w.y, true)) {
      issue(`${mapId}: warp source blocked (${w.x},${w.y})`);
    }
    if (!isWalkable(w.to, w.tx, w.ty, true)) {
      issue(`${mapId}: warp destination blocked ${w.to}(${w.tx},${w.ty})`);
    }
    if (!reach[w.y * map.w + w.x]) {
      issue(`${mapId}: warp unreachable from map walkable region (${w.x},${w.y})`);
    }
  }

  for (const n of map.npcs || []) {
    if (!inBounds(map, n.x, n.y)) {
      issue(`${mapId}: NPC out-of-bounds ${n.name || '(unnamed)'}(${n.x},${n.y})`);
      continue;
    }
    if (!isWalkable(mapId, n.x, n.y, true)) {
      issue(`${mapId}: NPC on blocked tile ${n.name || '(unnamed)'}(${n.x},${n.y})`);
    }
    if (!reach[n.y * map.w + n.x]) {
      warn(`${mapId}: NPC unreachable ${n.name || '(unnamed)'}(${n.x},${n.y})`);
    }
  }
}

// 2) Story beat action simulation
const beats = Array.isArray(story.beats) ? story.beats : [];
if (!beats.length) issue('story has no beats');
const byId = new Map(beats.map(b => [b.id, b]));

const state = {
  map: 'pallet_town',
  x: 9,
  y: 13,
  beatId: null
};

function applyWarpIfStanding() {
  const map = MAPS[state.map];
  for (const w of map.warps || []) {
    if (w.x === state.x && w.y === state.y) {
      state.map = w.to;
      state.x = w.tx;
      state.y = w.ty;
      return true;
    }
  }
  return false;
}

function moveDir(dir) {
  let nx = state.x;
  let ny = state.y;
  if (dir === 'up') ny--;
  else if (dir === 'down') ny++;
  else if (dir === 'left') nx--;
  else if (dir === 'right') nx++;
  if (!isWalkable(state.map, nx, ny, false)) return false;
  state.x = nx;
  state.y = ny;
  applyWarpIfStanding();
  return true;
}

function runBeat(beat) {
  for (const a of beat.actions || []) {
    if (!a || typeof a !== 'object') continue;
    if (a.kind === 'dialog') {
      const lines = Array.isArray(a.lines) ? a.lines : [];
      if (lines.length === 0) warn(`${beat.id}: empty dialog block`);
    }
    if (a.kind === 'teleport') {
      if (typeof a.map === 'string' && MAPS[a.map]) state.map = a.map;
      if (Number.isInteger(a.x)) state.x = a.x;
      if (Number.isInteger(a.y)) state.y = a.y;
      if (!isWalkable(state.map, state.x, state.y, true)) {
        issue(`${beat.id}: teleport lands blocked at ${state.map}(${state.x},${state.y})`);
      }
    }
    if (a.kind === 'move') {
      for (const d of (Array.isArray(a.path) ? a.path : [])) {
        if (!moveDir(String(d))) {
          issue(`${beat.id}: blocked move '${d}' from ${state.map}(${state.x},${state.y})`);
          break;
        }
      }
    }
  }
}

// Main chain simulation via next pointers from ch1_intro.
const seenBeats = new Set();
let cur = byId.get('ch1_intro');
while (cur && !seenBeats.has(cur.id)) {
  seenBeats.add(cur.id);
  state.beatId = cur.id;
  runBeat(cur);
  cur = cur.next ? byId.get(cur.next) : null;
}

if (cur && seenBeats.has(cur.id)) warn(`story next-loop detected at ${cur.id}`);

// Full beat sweep in declared order to catch broken beats outside the main next-chain.
for (const beat of beats) {
  if (!beat || typeof beat !== 'object' || !beat.id) continue;
  state.map = 'pallet_town';
  state.x = 9;
  state.y = 13;
  state.beatId = beat.id;
  runBeat(beat);
}

// 3) Coverage report
const covered = seenBeats.size;
const total = beats.length;
const report = {
  generatedAt: new Date().toISOString(),
  summary: {
    maps: Object.keys(MAPS).length,
    beatsTotal: total,
    beatsMainChainCovered: covered,
    issues: issues.length,
    warnings: warnings.length
  },
  issues,
  warnings
};

const out = path.join(root, '.runtime/e2e-audit-report.json');
fs.writeFileSync(out, JSON.stringify(report, null, 2));

if (issues.length) {
  console.error(`[e2e-audit] FAIL issues=${issues.length} warnings=${warnings.length} report=${out}`);
  process.exit(1);
}
console.log(`[e2e-audit] OK maps=${report.summary.maps} beatsMainChain=${covered}/${total} warnings=${warnings.length}`);
console.log(`[e2e-audit] Report: ${out}`);
