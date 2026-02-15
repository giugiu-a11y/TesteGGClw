#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[map-events-preflight] FAIL: ${msg}`);
  process.exit(1);
}

const root = path.resolve(__dirname, '..');
const htmlPath = path.join(root, 'index.html');
const eventsPath = path.join(root, 'assets/data/map_events.json');
if (!fs.existsSync(htmlPath)) fail('index.html missing');
if (!fs.existsSync(eventsPath)) fail('assets/data/map_events.json missing');

const html = fs.readFileSync(htmlPath, 'utf8');
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

let data;
try { data = JSON.parse(fs.readFileSync(eventsPath, 'utf8')); }
catch (err) { fail(`map_events parse failed: ${err.message}`); }

const maps = data && typeof data === 'object' ? data.maps : null;
if (!maps || typeof maps !== 'object') fail('maps object missing');

const issues = [];
const warnings = [];

for (const [mapId, def] of Object.entries(maps)) {
  const base = MAPS[mapId];
  if (!base) {
    issues.push(`unknown map: ${mapId}`);
    continue;
  }
  if (!def || typeof def !== 'object') {
    issues.push(`${mapId}: invalid definition`);
    continue;
  }
  if (Array.isArray(def.warps)) {
    for (const w of def.warps) {
      if (!w || !Number.isInteger(w.x) || !Number.isInteger(w.y) || !Number.isInteger(w.tx) || !Number.isInteger(w.ty) || typeof w.to !== 'string') {
        issues.push(`${mapId}: invalid warp ${JSON.stringify(w)}`);
        continue;
      }
      if (!MAPS[w.to]) issues.push(`${mapId}: warp target missing ${w.to}`);
      if (w.x < 0 || w.y < 0 || w.x >= base.w || w.y >= base.h) issues.push(`${mapId}: warp source out of bounds (${w.x},${w.y})`);
      const dst = MAPS[w.to];
      if (dst && (w.tx < 0 || w.ty < 0 || w.tx >= dst.w || w.ty >= dst.h)) issues.push(`${mapId}: warp dest out of bounds ${w.to}(${w.tx},${w.ty})`);
      const tile = base.data[w.y * base.w + w.x];
      if (tile !== T.WARP) warnings.push(`${mapId}: warp source not on T.WARP tile (${w.x},${w.y})`);
    }
  }
  if (Array.isArray(def.npcs)) {
    for (const n of def.npcs) {
      if (!n || !Number.isInteger(n.x) || !Number.isInteger(n.y)) {
        issues.push(`${mapId}: invalid NPC ${JSON.stringify(n)}`);
        continue;
      }
      if (n.x < 0 || n.y < 0 || n.x >= base.w || n.y >= base.h) issues.push(`${mapId}: NPC out of bounds (${n.x},${n.y})`);
      if (n.dialog && !Array.isArray(n.dialog)) warnings.push(`${mapId}: NPC dialog is not array (${n.name || 'unnamed'})`);
    }
  }
}

for (const w of warnings) console.warn(`[map-events-preflight] WARN: ${w}`);
for (const e of issues) console.error(`[map-events-preflight] ISSUE: ${e}`);
if (issues.length) {
  console.error(`[map-events-preflight] FAIL issues=${issues.length} warnings=${warnings.length}`);
  process.exit(1);
}
console.log(`[map-events-preflight] OK maps=${Object.keys(maps).length} warnings=${warnings.length}`);
