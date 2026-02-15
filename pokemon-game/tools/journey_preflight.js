#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[journey-preflight] FAIL: ${msg}`);
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
    if (depth === 0) { mapsEnd = i; break; }
  }
}
if (mapsEnd < 0) fail('MAPS parse failed');
const MAPS = eval(`(${script.slice(script.indexOf('{', mapsStart), mapsEnd + 1)})`);

function isWalkable(mapId, x, y) {
  const map = MAPS[mapId];
  if (!map || x < 0 || y < 0 || x >= map.w || y >= map.h) return false;
  const t = map.data[y * map.w + x];
  return !SOLID.includes(t);
}

function findPath(mapId, sx, sy, tx, ty, max = 2000) {
  const map = MAPS[mapId];
  if (!map) return null;
  if (!isWalkable(mapId, sx, sy) || !isWalkable(mapId, tx, ty)) return null;
  if (sx === tx && sy === ty) return [];
  const total = map.w * map.h;
  const seen = new Uint8Array(total);
  const prev = new Int32Array(total);
  const pdir = new Array(total).fill('');
  prev.fill(-1);
  const start = sy * map.w + sx;
  const goal = ty * map.w + tx;
  const q = [start];
  seen[start] = 1;
  const dirs = [
    {d: 'up', dx: 0, dy: -1},
    {d: 'down', dx: 0, dy: 1},
    {d: 'left', dx: -1, dy: 0},
    {d: 'right', dx: 1, dy: 0}
  ];
  for (let qi = 0; qi < q.length; qi++) {
    const cur = q[qi];
    if (cur === goal) break;
    const cx = cur % map.w;
    const cy = Math.floor(cur / map.w);
    for (const ent of dirs) {
      const nx = cx + ent.dx;
      const ny = cy + ent.dy;
      if (!isWalkable(mapId, nx, ny)) continue;
      const idx = ny * map.w + nx;
      if (seen[idx]) continue;
      seen[idx] = 1;
      prev[idx] = cur;
      pdir[idx] = ent.d;
      q.push(idx);
      if (q.length > max) return null;
    }
  }
  if (!seen[goal]) return null;
  const out = [];
  let cur = goal;
  while (cur !== start) {
    out.push(pdir[cur]);
    cur = prev[cur];
    if (cur < 0) return null;
    if (out.length > max) return null;
  }
  out.reverse();
  return out;
}

function findWarpTo(mapId, targetMapId) {
  const map = MAPS[mapId];
  if (!map || !Array.isArray(map.warps)) return null;
  for (const w of map.warps) {
    if (w && w.to === targetMapId) return w;
  }
  return null;
}

const state = { map: 'pallet_town', x: 9, y: 13 };

function walkTo(tx, ty) {
  const p = findPath(state.map, state.x, state.y, tx, ty, 6000);
  if (!p) fail(`no path in ${state.map} from (${state.x},${state.y}) to (${tx},${ty})`);
  state.x = tx;
  state.y = ty;
}

function warpTo(nextMap) {
  const w = findWarpTo(state.map, nextMap);
  if (!w) fail(`warp ${state.map} -> ${nextMap} not found`);
  walkTo(w.x, w.y);
  if (!isWalkable(w.to, w.tx, w.ty)) fail(`warp lands blocked: ${w.to} (${w.tx},${w.ty})`);
  state.map = w.to;
  state.x = w.tx;
  state.y = w.ty;
}

// Core smoke journey across early game.
warpTo('route1');
warpTo('viridian');
warpTo('viridian_pokecenter');
warpTo('viridian');
warpTo('route2');
warpTo('viridian_forest');
warpTo('route2');
warpTo('pewter');
warpTo('pewter_gym');
warpTo('pewter');
warpTo('route3');
warpTo('mt_moon');
warpTo('cerulean');

console.log(`[journey-preflight] OK final=${state.map}(${state.x},${state.y})`);
