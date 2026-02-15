#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[story-motion-preflight] FAIL: ${msg}`);
  process.exit(1);
}

const root = path.resolve(__dirname, '..');
const indexPath = path.join(root, 'index.html');
const storyPath = path.join(root, 'story/season1.ptbr.json');
const headersPath = path.join(root, 'assets/data/map_headers.json');

if (!fs.existsSync(indexPath)) fail('index.html missing');
if (!fs.existsSync(storyPath)) fail('story/season1.ptbr.json missing');

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

const mapsStart = script.indexOf('const MAPS = {');
if (mapsStart < 0) fail('MAPS not found');
let i = script.indexOf('{', mapsStart);
let depth = 0;
let mapsEnd = -1;
for (; i < script.length; i++) {
  const ch = script[i];
  if (ch === '{') depth++;
  else if (ch === '}') {
    depth--;
    if (depth === 0) {
      mapsEnd = i;
      break;
    }
  }
}
if (mapsEnd < 0) fail('MAPS parse failed');
const MAPS = eval(`(${script.slice(script.indexOf('{', mapsStart), mapsEnd + 1)})`);

function sanitizeMapConnections(raw) {
  if (!raw || typeof raw !== 'object') return {};
  const out = {};
  for (const [mapId, edges] of Object.entries(raw)) {
    if (!MAPS[mapId] || !edges || typeof edges !== 'object') continue;
    const entry = {};
    for (const dir of ['north', 'south', 'east', 'west']) {
      const c = edges[dir];
      if (!c || typeof c !== 'object') continue;
      if (!c.to || !MAPS[c.to]) continue;
      const clean = { to: c.to };
      if (Number.isInteger(c.min)) clean.min = c.min;
      if (Number.isInteger(c.max)) clean.max = c.max;
      entry[dir] = clean;
    }
    if (Object.keys(entry).length) out[mapId] = entry;
  }
  return out;
}

let MAP_CONNECTIONS = {};
if (fs.existsSync(headersPath)) {
  try {
    const parsed = JSON.parse(fs.readFileSync(headersPath, 'utf8'));
    const incoming = parsed && typeof parsed === 'object' ? parsed.connections : null;
    if (incoming && typeof incoming === 'object') {
      MAP_CONNECTIONS = sanitizeMapConnections(incoming);
    }
  } catch {
    // keep defaults
  }
}

const story = JSON.parse(fs.readFileSync(storyPath, 'utf8'));
const beats = Array.isArray(story.beats) ? story.beats : [];

function isWalkable(mapId, x, y) {
  const map = MAPS[mapId];
  if (!map) return false;
  if (x < 0 || y < 0 || x >= map.w || y >= map.h) return false;
  const t = map.data[y * map.w + x];
  return !SOLID.includes(t);
}

function findWarpAt(mapId, x, y) {
  const map = MAPS[mapId];
  if (!map || !Array.isArray(map.warps)) return null;
  for (const w of map.warps) {
    if (w && w.x === x && w.y === y && MAPS[w.to]) return w;
  }
  return null;
}

function connectionStep(state, dir, nx, ny) {
  const conn = MAP_CONNECTIONS[state.map] && MAP_CONNECTIONS[state.map][dir];
  if (!conn || !MAPS[conn.to]) return null;
  const boundaryPos = (dir === 'left' || dir === 'right') ? state.py : state.px;
  if (Number.isInteger(conn.min) && boundaryPos < conn.min) return null;
  if (Number.isInteger(conn.max) && boundaryPos > conn.max) return null;

  const dst = MAPS[conn.to];
  if (dir === 'left') return { map: conn.to, px: dst.w - 1, py: Math.max(0, Math.min(dst.h - 1, ny)) };
  if (dir === 'right') return { map: conn.to, px: 0, py: Math.max(0, Math.min(dst.h - 1, ny)) };
  if (dir === 'up') return { map: conn.to, px: Math.max(0, Math.min(dst.w - 1, nx)), py: dst.h - 1 };
  return { map: conn.to, px: Math.max(0, Math.min(dst.w - 1, nx)), py: 0 };
}

let issues = 0;
const warn = (msg) => console.warn(`[story-motion-preflight] WARN: ${msg}`);
const issue = (msg) => {
  issues++;
  console.error(`[story-motion-preflight] ISSUE: ${msg}`);
};

const state = {
  map: 'pallet_town',
  px: 9,
  py: 13,
  dir: 'down'
};

function stepMove(dir, beatId, ai) {
  let nx = state.px;
  let ny = state.py;
  if (dir === 'up') ny--;
  else if (dir === 'down') ny++;
  else if (dir === 'left') nx--;
  else if (dir === 'right') nx++;
  else {
    issue(`${beatId}#${ai}: invalid move dir '${dir}'`);
    return;
  }

  const outOfBounds = !MAPS[state.map] || nx < 0 || ny < 0 || nx >= MAPS[state.map].w || ny >= MAPS[state.map].h;
  if (outOfBounds) {
    const c = connectionStep(state, dir, nx, ny);
    if (!c) {
      issue(`${beatId}#${ai}: out-of-bounds move ${dir} from ${state.map} (${state.px},${state.py})`);
      return;
    }
    state.map = c.map;
    state.px = c.px;
    state.py = c.py;
  } else {
    if (!isWalkable(state.map, nx, ny)) {
      issue(`${beatId}#${ai}: blocked move ${dir} into ${state.map} (${nx},${ny})`);
      return;
    }
    state.px = nx;
    state.py = ny;
  }

  const w = findWarpAt(state.map, state.px, state.py);
  if (w) {
    if (!isWalkable(w.to, w.tx, w.ty)) {
      issue(`${beatId}#${ai}: warp destination blocked ${w.to} (${w.tx},${w.ty})`);
      return;
    }
    state.map = w.to;
    state.px = w.tx;
    state.py = w.ty;
  }
}

for (const beat of beats) {
  if (!beat || typeof beat !== 'object') continue;
  const beatId = beat.id || '<no-id>';
  const actions = Array.isArray(beat.actions) ? beat.actions : [];
  for (let ai = 0; ai < actions.length; ai++) {
    const a = actions[ai] || {};
    if (a.kind === 'teleport' || a.kind === 'warp') {
      const toMap = (typeof a.map === 'string' && MAPS[a.map]) ? a.map : state.map;
      const toX = Number.isInteger(a.x) ? a.x : state.px;
      const toY = Number.isInteger(a.y) ? a.y : state.py;
      if (!MAPS[toMap]) {
        issue(`${beatId}#${ai}: teleport to unknown map '${toMap}'`);
        continue;
      }
      if (toX < 0 || toY < 0 || toX >= MAPS[toMap].w || toY >= MAPS[toMap].h) {
        issue(`${beatId}#${ai}: teleport out of bounds ${toMap} (${toX},${toY})`);
        continue;
      }
      if (!isWalkable(toMap, toX, toY)) {
        issue(`${beatId}#${ai}: teleport lands on blocked tile ${toMap} (${toX},${toY})`);
        continue;
      }
      state.map = toMap;
      state.px = toX;
      state.py = toY;
      if (typeof a.dir === 'string') state.dir = a.dir;
      continue;
    }

    if (a.kind === 'move' || a.kind === 'applyMovement') {
      const path = Array.isArray(a.path) ? a.path : [];
      if (!path.length) {
        warn(`${beatId}#${ai}: move with empty path`);
        continue;
      }
      for (const dir of path) stepMove(dir, beatId, ai);
    }
  }
}

if (issues > 0) fail(`${issues} issue(s) found`);
console.log(`[story-motion-preflight] OK beats=${beats.length} final=${state.map}(${state.px},${state.py})`);
