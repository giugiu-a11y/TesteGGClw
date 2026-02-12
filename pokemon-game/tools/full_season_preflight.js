#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[full-season-preflight] FAIL: ${msg}`);
  process.exit(1);
}

const root = path.resolve(__dirname, '..');
const indexPath = path.join(root, 'index.html');
if (!fs.existsSync(indexPath)) fail('index.html missing');
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

const storyPath = path.join(root, 'story/season1.ptbr.json');
if (!fs.existsSync(storyPath)) fail('story/season1.ptbr.json missing');
const story = JSON.parse(fs.readFileSync(storyPath, 'utf8'));
const beats = Array.isArray(story.beats) ? story.beats : [];
if (!beats.length) fail('story beats missing');

function isWalkable(mapId, x, y) {
  const map = MAPS[mapId];
  if (!map) return false;
  if (x < 0 || y < 0 || x >= map.w || y >= map.h) return false;
  const t = map.data[y * map.w + x];
  return !SOLID.includes(t);
}

function nearestWalkable(mapId, x, y) {
  const map = MAPS[mapId];
  if (!map) return null;
  for (let r = 0; r <= Math.max(map.w, map.h); r++) {
    for (let dy = -r; dy <= r; dy++) {
      for (let dx = -r; dx <= r; dx++) {
        if (Math.abs(dx) + Math.abs(dy) > r) continue;
        const tx = x + dx;
        const ty = y + dy;
        if (isWalkable(mapId, tx, ty)) return {x: tx, y: ty};
      }
    }
  }
  return null;
}

const issues = [];
const pushIssue = (msg) => issues.push(msg);

const state = {
  map: 'pallet_town',
  x: 9,
  y: 13,
  dir: 'down'
};

for (const beat of beats) {
  const beatId = beat && beat.id ? beat.id : '(no-id)';
  const actions = Array.isArray(beat.actions) ? beat.actions : [];
  for (let ai = 0; ai < actions.length; ai++) {
    const a = actions[ai] || {};
    const kind = a.kind;
    if (kind === 'teleport') {
      if (typeof a.map === 'string' && MAPS[a.map]) state.map = a.map;
      if (typeof a.x === 'number') state.x = a.x;
      if (typeof a.y === 'number') state.y = a.y;
      if (typeof a.dir === 'string') state.dir = a.dir;
      if (!isWalkable(state.map, state.x, state.y)) {
        const alt = nearestWalkable(state.map, state.x, state.y);
        pushIssue(`${beatId}[${ai}] teleport blocked at ${state.map} (${state.x},${state.y})${alt ? ` nearest=(${alt.x},${alt.y})` : ''}`);
      }
      continue;
    }

    if (kind === 'move') {
      const pathDirs = Array.isArray(a.path) ? a.path : [];
      for (let pi = 0; pi < pathDirs.length; pi++) {
        const d = String(pathDirs[pi]);
        let nx = state.x;
        let ny = state.y;
        if (d === 'up') ny--;
        else if (d === 'down') ny++;
        else if (d === 'left') nx--;
        else if (d === 'right') nx++;
        else {
          pushIssue(`${beatId}[${ai}] invalid move dir: ${d}`);
          continue;
        }
        if (!isWalkable(state.map, nx, ny)) {
          pushIssue(`${beatId}[${ai}] move[${pi}] blocked at ${state.map} (${nx},${ny}) from (${state.x},${state.y})`);
          break;
        }
        state.x = nx;
        state.y = ny;
        state.dir = d;
      }
      continue;
    }
  }
}

if (issues.length) {
  for (const msg of issues.slice(0, 80)) {
    console.error(`[full-season-preflight] ISSUE: ${msg}`);
  }
  fail(`${issues.length} issue(s) found`);
}

console.log(`[full-season-preflight] OK beats=${beats.length}`);
