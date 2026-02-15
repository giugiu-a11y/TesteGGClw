#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[map-scripts-preflight] FAIL: ${msg}`);
  process.exit(1);
}

const root = path.resolve(__dirname, '..');
const indexPath = path.join(root, 'index.html');
const scriptsPath = path.join(root, 'assets/data/map_scripts.json');
const storyPath = path.join(root, 'story/season1.ptbr.json');
if (!fs.existsSync(indexPath)) fail('index.html missing');
if (!fs.existsSync(scriptsPath)) fail('assets/data/map_scripts.json missing');
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

// MAPS initializer references T.* constants.
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
const story = JSON.parse(fs.readFileSync(storyPath, 'utf8'));
const beatIds = new Set((story.beats || []).map(b => b && b.id).filter(Boolean));

let data;
try { data = JSON.parse(fs.readFileSync(scriptsPath, 'utf8')); }
catch (err) { fail(`map_scripts parse failed: ${err.message}`); }

const maps = data && typeof data === 'object' ? data.maps : null;
if (!maps || typeof maps !== 'object') fail('maps object missing');

const issues = [];
const warnings = [];

for (const [mapId, triggers] of Object.entries(maps)) {
  const map = MAPS[mapId];
  if (!map) {
    issues.push(`unknown map: ${mapId}`);
    continue;
  }
  if (!Array.isArray(triggers)) {
    issues.push(`${mapId}: trigger list must be array`);
    continue;
  }
  const ids = new Set();
  for (const t of triggers) {
    if (!t || !Number.isInteger(t.x) || !Number.isInteger(t.y)) {
      issues.push(`${mapId}: invalid trigger ${JSON.stringify(t)}`);
      continue;
    }
    if (t.x < 0 || t.y < 0 || t.x >= map.w || t.y >= map.h) {
      issues.push(`${mapId}: trigger out of bounds (${t.x},${t.y})`);
    }
    const id = (typeof t.id === 'string' && t.id.trim()) ? t.id.trim() : `${mapId}_${t.x}_${t.y}`;
    if (ids.has(id)) warnings.push(`${mapId}: duplicate trigger id ${id}`);
    ids.add(id);

    if (t.beat && !beatIds.has(t.beat)) issues.push(`${mapId}:${id}: unknown beat '${t.beat}'`);
    if (!t.beat && !Array.isArray(t.actions)) warnings.push(`${mapId}:${id}: trigger without beat/actions`);
    if (t.actions && !Array.isArray(t.actions)) issues.push(`${mapId}:${id}: actions must be array`);
    if (t.once !== undefined && typeof t.once !== 'boolean') issues.push(`${mapId}:${id}: once must be boolean`);
    if (t.requireFlag !== undefined && typeof t.requireFlag !== 'string') issues.push(`${mapId}:${id}: requireFlag must be string`);
    if (t.setFlag !== undefined && typeof t.setFlag !== 'string') issues.push(`${mapId}:${id}: setFlag must be string`);
  }
}

for (const w of warnings) console.warn(`[map-scripts-preflight] WARN: ${w}`);
for (const e of issues) console.error(`[map-scripts-preflight] ISSUE: ${e}`);
if (issues.length) {
  console.error(`[map-scripts-preflight] FAIL issues=${issues.length} warnings=${warnings.length}`);
  process.exit(1);
}
console.log(`[map-scripts-preflight] OK maps=${Object.keys(maps).length} warnings=${warnings.length}`);
