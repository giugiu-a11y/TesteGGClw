#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[warp-pair-preflight] FAIL: ${msg}`);
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

const warns = [];
const issues = [];

const ALLOW_ONE_WAY = new Set([
  'cinnabar->indigo_plateau'
]);

for (const [mapId, map] of Object.entries(MAPS)) {
  const warps = Array.isArray(map.warps) ? map.warps : [];
  for (const w of warps) {
    if (!w || !w.to || !MAPS[w.to]) continue;
    if (ALLOW_ONE_WAY.has(`${mapId}->${w.to}`)) continue;
    const dstMap = MAPS[w.to];
    const dstWarps = Array.isArray(dstMap.warps) ? dstMap.warps : [];
    const hasReverse = dstWarps.some(dw => dw && dw.to === mapId);
    if (!hasReverse) {
      warns.push(`${mapId}(${w.x},${w.y})->${w.to}(${w.tx},${w.ty}) without reverse warp`);
    }
  }
}

// Hard fail only if a map has zero warps but is not a pure interior cutscene room.
for (const [mapId, map] of Object.entries(MAPS)) {
  const warps = Array.isArray(map.warps) ? map.warps : [];
  if (!warps.length && !String(mapId).includes('lab') && !String(mapId).includes('house')) {
    issues.push(`${mapId}: has no warps`);
  }
}

for (const w of warns) console.warn(`[warp-pair-preflight] WARN: ${w}`);
for (const e of issues) console.error(`[warp-pair-preflight] ISSUE: ${e}`);

if (issues.length) {
  console.error(`[warp-pair-preflight] FAIL issues=${issues.length} warnings=${warns.length}`);
  process.exit(1);
}
console.log(`[warp-pair-preflight] OK maps=${Object.keys(MAPS).length} warnings=${warns.length}`);
