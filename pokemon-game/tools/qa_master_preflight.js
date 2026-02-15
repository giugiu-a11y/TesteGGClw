#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[qa-master] FAIL: ${msg}`);
  process.exit(1);
}

const root = path.resolve(__dirname, '..');
const indexPath = path.join(root, 'index.html');
const storyPath = path.join(root, 'story/season1.ptbr.json');
const mapbgManifestPath = path.join(root, 'assets/tilesets/mapbg.manifest.json');
const reportPath = path.join(root, '.runtime/qa-report.json');

if (!fs.existsSync(indexPath)) fail('index.html missing');
if (!fs.existsSync(storyPath)) fail('story/season1.ptbr.json missing');
if (!fs.existsSync(mapbgManifestPath)) fail('assets/tilesets/mapbg.manifest.json missing');

const html = fs.readFileSync(indexPath, 'utf8');
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) fail('main <script> block not found');
const script = scriptMatch[1];

function grabConst(name) {
  const rx = new RegExp(`const\\s+${name}\\s*=\\s*([\\s\\S]*?);\\n\\s*\\n`);
  const mm = script.match(rx);
  if (!mm) fail(`const ${name} not found`);
  return mm[1];
}

function parseMaps() {
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
  return eval(`(${script.slice(script.indexOf('{', start), end + 1)})`);
}

const T = eval(`(${grabConst('T')})`);
const SOLID = eval(grabConst('SOLID'));
const STYLE_LOCK_CORE_MAPS = eval(grabConst('STYLE_LOCK_CORE_MAPS'));
const MAPS = parseMaps();
const story = JSON.parse(fs.readFileSync(storyPath, 'utf8'));
const mapbgManifest = JSON.parse(fs.readFileSync(mapbgManifestPath, 'utf8'));
const MAPBG = mapbgManifest && mapbgManifest.mapbg ? mapbgManifest.mapbg : {};

const issues = [];
const warnings = [];
function issue(msg) {
  issues.push(msg);
  console.error(`[qa-master] ISSUE: ${msg}`);
}
function warn(msg) {
  warnings.push(msg);
  console.warn(`[qa-master] WARN: ${msg}`);
}

const TILE_VALUES = new Set(Object.values(T));

function inBounds(map, x, y) {
  return x >= 0 && y >= 0 && x < map.w && y < map.h;
}

function tileAt(map, x, y) {
  return map.data[y * map.w + x];
}

function buildCollisionGrid(mapId) {
  const map = MAPS[mapId];
  if (!map) return null;
  const total = map.w * map.h;
  const grid = new Uint8Array(total);
  for (let i = 0; i < total; i++) {
    grid[i] = SOLID.includes(map.data[i]) ? 1 : 0;
  }
  const conf = MAPBG[mapId];
  const rects = conf && Array.isArray(conf.solidRects) ? conf.solidRects : [];
  for (const r of rects) {
    const rx = Number(r && r.x);
    const ry = Number(r && r.y);
    const rw = Number(r && r.w);
    const rh = Number(r && r.h);
    if (!Number.isFinite(rx) || !Number.isFinite(ry) || !Number.isFinite(rw) || !Number.isFinite(rh)) {
      issue(`${mapId}: invalid solidRect ${JSON.stringify(r)}`);
      continue;
    }
    for (let y = ry; y < ry + rh; y++) {
      for (let x = rx; x < rx + rw; x++) {
        if (x >= 0 && y >= 0 && x < map.w && y < map.h) {
          grid[y * map.w + x] = 1;
        }
      }
    }
  }
  return grid;
}

function isWalkable(mapId, x, y, options = {}) {
  const map = MAPS[mapId];
  if (!map) return false;
  if (!inBounds(map, x, y)) return false;
  const ignoreNpc = !!options.ignoreNpc;
  const g = collisionGrids[mapId];
  if (g[y * map.w + x]) return false;
  if (!ignoreNpc) {
    for (const npc of map.npcs || []) {
      if (npc.x === x && npc.y === y) return false;
    }
  }
  return true;
}

function firstWalkable(mapId) {
  const map = MAPS[mapId];
  for (let y = 0; y < map.h; y++) {
    for (let x = 0; x < map.w; x++) {
      if (isWalkable(mapId, x, y, {ignoreNpc: true})) return {x, y};
    }
  }
  return null;
}

function bfsReachable(mapId, startX, startY) {
  const map = MAPS[mapId];
  const seen = new Uint8Array(map.w * map.h);
  const qx = [];
  const qy = [];
  if (!isWalkable(mapId, startX, startY, {ignoreNpc: true})) return seen;
  qx.push(startX); qy.push(startY);
  seen[startY * map.w + startX] = 1;
  for (let qi = 0; qi < qx.length; qi++) {
    const x = qx[qi];
    const y = qy[qi];
    const dirs = [[1,0],[-1,0],[0,1],[0,-1]];
    for (const [dx, dy] of dirs) {
      const nx = x + dx;
      const ny = y + dy;
      if (!inBounds(map, nx, ny)) continue;
      const idx = ny * map.w + nx;
      if (seen[idx]) continue;
      if (!isWalkable(mapId, nx, ny, {ignoreNpc: true})) continue;
      seen[idx] = 1;
      qx.push(nx);
      qy.push(ny);
    }
  }
  return seen;
}

const collisionGrids = {};
for (const mapId of Object.keys(MAPS)) {
  collisionGrids[mapId] = buildCollisionGrid(mapId);
}

// 1) Core static validation.
for (const [mapId, map] of Object.entries(MAPS)) {
  if (!Number.isInteger(map.w) || !Number.isInteger(map.h) || map.w <= 0 || map.h <= 0) {
    issue(`${mapId}: invalid dimensions`);
    continue;
  }
  if (!Array.isArray(map.data)) {
    issue(`${mapId}: data missing`);
    continue;
  }
  if (map.data.length !== map.w * map.h) {
    issue(`${mapId}: data length ${map.data.length} != ${map.w * map.h}`);
  }

  for (let i = 0; i < map.data.length; i++) {
    const t = map.data[i];
    if (!TILE_VALUES.has(t)) {
      issue(`${mapId}: unknown tile value ${t} at index ${i}`);
      break;
    }
  }

  const walk = firstWalkable(mapId);
  if (!walk) issue(`${mapId}: no walkable tiles`);

  for (const npc of map.npcs || []) {
    if (!inBounds(map, npc.x, npc.y)) {
      issue(`${mapId}: NPC ${npc.name || '(unnamed)'} out of bounds (${npc.x},${npc.y})`);
      continue;
    }
    if (!isWalkable(mapId, npc.x, npc.y, {ignoreNpc: true})) {
      issue(`${mapId}: NPC ${npc.name || '(unnamed)'} on blocked tile (${npc.x},${npc.y})`);
    }
    if (!npc.sprite || typeof npc.sprite !== 'string') {
      warn(`${mapId}: NPC ${npc.name || '(unnamed)'} missing sprite key`);
    }
  }

  const seenWarpSources = new Set();
  for (const w of map.warps || []) {
    if (!Number.isInteger(w.x) || !Number.isInteger(w.y) || !Number.isInteger(w.tx) || !Number.isInteger(w.ty)) {
      issue(`${mapId}: warp has non-integer coords ${JSON.stringify(w)}`);
      continue;
    }
    if (!inBounds(map, w.x, w.y)) {
      issue(`${mapId}: warp source out of bounds (${w.x},${w.y})`);
      continue;
    }

    const srcKey = `${w.x},${w.y}`;
    if (seenWarpSources.has(srcKey)) {
      warn(`${mapId}: multiple warp entries sharing source (${srcKey})`);
    }
    seenWarpSources.add(srcKey);

    if (tileAt(map, w.x, w.y) !== T.WARP) {
      issue(`${mapId}: warp source not on WARP tile at (${w.x},${w.y})`);
    }
    if (!isWalkable(mapId, w.x, w.y, {ignoreNpc: true})) {
      issue(`${mapId}: warp source blocked by collision at (${w.x},${w.y})`);
    }

    if (!MAPS[w.to]) {
      issue(`${mapId}: warp target map missing (${w.to})`);
      continue;
    }
    const dst = MAPS[w.to];
    if (!inBounds(dst, w.tx, w.ty)) {
      issue(`${mapId}: warp destination out of bounds ${w.to} (${w.tx},${w.ty})`);
    } else if (!isWalkable(w.to, w.tx, w.ty, {ignoreNpc: true})) {
      issue(`${mapId}: warp destination blocked ${w.to} (${w.tx},${w.ty})`);
    }
  }
}

// 2) Reachability inside each map.
for (const mapId of Object.keys(MAPS)) {
  const map = MAPS[mapId];
  const seed = firstWalkable(mapId);
  if (!seed) continue;
  const reach = bfsReachable(mapId, seed.x, seed.y);

  for (const w of map.warps || []) {
    if (!inBounds(map, w.x, w.y)) continue;
    if (!reach[w.y * map.w + w.x]) {
      issue(`${mapId}: warp source unreachable from map walkable space (${w.x},${w.y})`);
    }
  }

  for (const npc of map.npcs || []) {
    if (!inBounds(map, npc.x, npc.y)) continue;
    if (!reach[npc.y * map.w + npc.x]) {
      warn(`${mapId}: NPC ${npc.name || '(unnamed)'} is isolated/unreachable (${npc.x},${npc.y})`);
    }
  }
}

// 3) Global map connectivity through warps.
const graph = new Map();
for (const mapId of Object.keys(MAPS)) graph.set(mapId, new Set());
for (const [mapId, map] of Object.entries(MAPS)) {
  for (const w of map.warps || []) {
    if (MAPS[w.to]) graph.get(mapId).add(w.to);
  }
}
const visited = new Set(['pallet_town']);
const q = ['pallet_town'];
for (let i = 0; i < q.length; i++) {
  const cur = q[i];
  for (const nxt of graph.get(cur) || []) {
    if (visited.has(nxt)) continue;
    visited.add(nxt);
    q.push(nxt);
  }
}
for (const mapId of Object.keys(MAPS)) {
  if (!visited.has(mapId)) warn(`map disconnected from pallet_town via warps: ${mapId}`);
}

// 4) Story validation (kinds + runtime walkability simulation with collision grid).
const beats = Array.isArray(story.beats) ? story.beats : [];
if (!beats.length) issue('story has no beats');
const knownKinds = new Set(['dialog', 'set', 'face', 'pause', 'move', 'teleport', 'ensureTeam', 'evolve', 'battle']);

const sim = {map: 'pallet_town', x: 9, y: 13, dir: 'down'};
for (const beat of beats) {
  const beatId = beat && beat.id ? beat.id : '(no-id)';
  const actions = Array.isArray(beat && beat.actions) ? beat.actions : null;
  if (!actions) {
    issue(`${beatId}: actions missing`);
    continue;
  }

  for (let ai = 0; ai < actions.length; ai++) {
    const a = actions[ai] || {};
    const kind = a.kind;
    if (!knownKinds.has(kind)) {
      issue(`${beatId}[${ai}]: unknown action kind '${kind}'`);
      continue;
    }

    if (kind === 'dialog') {
      if (!Array.isArray(a.lines) || !a.lines.length) {
        issue(`${beatId}[${ai}]: dialog must have non-empty lines[]`);
      }
      continue;
    }

    if (kind === 'set') {
      if (typeof a.path !== 'string' || !a.path.trim()) {
        issue(`${beatId}[${ai}]: set action missing path`);
      }
      continue;
    }

    if (kind === 'move') {
      const pathDirs = Array.isArray(a.path) ? a.path : [];
      if (!pathDirs.length) warn(`${beatId}[${ai}]: move with empty path`);
      for (let pi = 0; pi < pathDirs.length; pi++) {
        const d = String(pathDirs[pi]);
        let nx = sim.x;
        let ny = sim.y;
        if (d === 'up') ny--;
        else if (d === 'down') ny++;
        else if (d === 'left') nx--;
        else if (d === 'right') nx++;
        else {
          issue(`${beatId}[${ai}]: invalid move dir '${d}' at step ${pi}`);
          continue;
        }
        if (!isWalkable(sim.map, nx, ny, {ignoreNpc: true})) {
          issue(`${beatId}[${ai}]: move blocked at ${sim.map} (${nx},${ny}) from (${sim.x},${sim.y})`);
          break;
        }
        sim.x = nx;
        sim.y = ny;
        sim.dir = d;
      }
      continue;
    }

    if (kind === 'teleport') {
      if (typeof a.map === 'string') {
        if (!MAPS[a.map]) {
          issue(`${beatId}[${ai}]: teleport to unknown map '${a.map}'`);
        } else {
          sim.map = a.map;
        }
      }
      if (Number.isFinite(a.x)) sim.x = Number(a.x);
      if (Number.isFinite(a.y)) sim.y = Number(a.y);
      if (typeof a.dir === 'string') sim.dir = a.dir;

      if (!MAPS[sim.map]) continue;
      if (!isWalkable(sim.map, sim.x, sim.y, {ignoreNpc: true})) {
        issue(`${beatId}[${ai}]: teleport lands on blocked tile ${sim.map} (${sim.x},${sim.y})`);
      }
      continue;
    }

    if (kind === 'battle') {
      if (!a.enemy || typeof a.enemy !== 'object') {
        issue(`${beatId}[${ai}]: battle missing enemy object`);
      }
      continue;
    }
  }
}

// 5) Style lock / manifest consistency.
for (const mapId of STYLE_LOCK_CORE_MAPS) {
  if (!MAPBG[mapId]) {
    issue(`style-lock map missing in mapbg manifest: ${mapId}`);
  }
}

// 6) Runtime default checks.
if (!/const\s+AUTO_CUTSCENE_MOVE\s*=\s*qs\('autocutmove',\s*'[01]'\)\s*===\s*'1'/.test(script)) {
  issue('AUTO_CUTSCENE_MOVE flag missing or malformed');
}
if (/\binDialog\b/.test(script)) {
  issue('stale inDialog identifier found (expected dialog)');
}

const dialogLines = beats.reduce((acc, beat) => {
  const actions = Array.isArray(beat.actions) ? beat.actions : [];
  for (const a of actions) {
    if (a.kind === 'dialog' && Array.isArray(a.lines)) acc += a.lines.length;
  }
  return acc;
}, 0);
const totalWarps = Object.values(MAPS).reduce((acc, m) => acc + ((m.warps || []).length), 0);
const totalNpcs = Object.values(MAPS).reduce((acc, m) => acc + ((m.npcs || []).length), 0);

const report = {
  generatedAt: new Date().toISOString(),
  summary: {
    maps: Object.keys(MAPS).length,
    beats: beats.length,
    dialogLines,
    warps: totalWarps,
    npcs: totalNpcs,
    issues: issues.length,
    warnings: warnings.length
  },
  issues,
  warnings
};

fs.mkdirSync(path.dirname(reportPath), {recursive: true});
fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));

if (issues.length) {
  fail(`${issues.length} issue(s) found. Report: ${path.relative(root, reportPath)}`);
}

console.log(`[qa-master] OK maps=${report.summary.maps} beats=${report.summary.beats} warnings=${warnings.length}`);
console.log(`[qa-master] Report: ${path.relative(root, reportPath)}`);
