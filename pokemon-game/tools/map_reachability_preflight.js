#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[map-reachability-preflight] FAIL: ${msg}`);
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

const issues = [];
const warnings = [];

function isWalkable(map, x, y) {
  if (!map || x < 0 || y < 0 || x >= map.w || y >= map.h) return false;
  const t = map.data[y * map.w + x];
  return !SOLID.includes(t);
}

function bfsFrom(map, sx, sy) {
  const total = map.w * map.h;
  const seen = new Uint8Array(total);
  const q = [];
  const start = sy * map.w + sx;
  if (!isWalkable(map, sx, sy)) return seen;
  seen[start] = 1;
  q.push([sx, sy]);
  const D = [[1,0],[-1,0],[0,1],[0,-1]];
  while (q.length) {
    const [x, y] = q.shift();
    for (const [dx, dy] of D) {
      const nx = x + dx;
      const ny = y + dy;
      if (!isWalkable(map, nx, ny)) continue;
      const idx = ny * map.w + nx;
      if (seen[idx]) continue;
      seen[idx] = 1;
      q.push([nx, ny]);
    }
  }
  return seen;
}

for (const [mapId, map] of Object.entries(MAPS)) {
  if (!map || !map.w || !map.h || !Array.isArray(map.data)) {
    issues.push(`${mapId}: malformed map`);
    continue;
  }

  const points = [];
  for (const w of map.warps || []) {
    if (!Number.isInteger(w.x) || !Number.isInteger(w.y)) continue;
    points.push({kind: 'warp', x: w.x, y: w.y, label: `${w.x},${w.y}->${w.to}`});
  }
  for (const n of map.npcs || []) {
    if (!Number.isInteger(n.x) || !Number.isInteger(n.y)) continue;
    points.push({kind: 'npc', x: n.x, y: n.y, label: `${n.name || 'NPC'}@${n.x},${n.y}`});
  }

  if (!points.length) continue;

  const walkablePoints = points.filter(p => isWalkable(map, p.x, p.y));
  for (const p of points) {
    if (!isWalkable(map, p.x, p.y)) issues.push(`${mapId}: ${p.kind} on blocked tile (${p.label})`);
  }
  if (!walkablePoints.length) continue;

  const seed = walkablePoints[0];
  const seen = bfsFrom(map, seed.x, seed.y);

  for (const p of walkablePoints) {
    const idx = p.y * map.w + p.x;
    if (!seen[idx]) {
      issues.push(`${mapId}: disconnected ${p.kind} (${p.label}) from ${seed.label}`);
    }
  }

  // Check if each warp has at least one walkable neighbor for reliable entry/exit.
  for (const w of (map.warps || [])) {
    if (!isWalkable(map, w.x, w.y)) continue;
    let adj = 0;
    for (const [dx, dy] of [[1,0],[-1,0],[0,1],[0,-1]]) {
      if (isWalkable(map, w.x + dx, w.y + dy)) adj++;
    }
    if (adj === 0) issues.push(`${mapId}: isolated warp at (${w.x},${w.y})`);
    else if (adj === 1) warnings.push(`${mapId}: narrow warp at (${w.x},${w.y})`);
  }
}

for (const w of warnings.slice(0, 100)) console.warn(`[map-reachability-preflight] WARN: ${w}`);
for (const e of issues.slice(0, 200)) console.error(`[map-reachability-preflight] ISSUE: ${e}`);
if (issues.length) fail(`issues=${issues.length} warnings=${warnings.length}`);
console.log(`[map-reachability-preflight] OK maps=${Object.keys(MAPS).length} warnings=${warnings.length}`);
