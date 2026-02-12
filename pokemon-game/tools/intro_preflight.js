#!/usr/bin/env node
const fs = require('fs');

function fail(msg) {
  console.error(`[intro-preflight] FAIL: ${msg}`);
  process.exit(1);
}

const html = fs.readFileSync('index.html', 'utf8');
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

const story = JSON.parse(fs.readFileSync('story/season1.ptbr.json', 'utf8'));
const byId = new Map(story.beats.map(b => [b.id, b]));

function isWalkable(mapId, x, y) {
  const map = MAPS[mapId];
  if (!map) return false;
  if (x < 0 || y < 0 || x >= map.w || y >= map.h) return false;
  const t = map.data[y * map.w + x];
  return !SOLID.includes(t);
}

function walkPath(state, path, beatId) {
  for (const d of path) {
    let nx = state.x;
    let ny = state.y;
    if (d === 'up') ny--;
    else if (d === 'down') ny++;
    else if (d === 'left') nx--;
    else if (d === 'right') nx++;
    if (!isWalkable(state.map, nx, ny)) {
      fail(`${beatId}: move '${d}' blocked at ${state.map} (${nx},${ny}) from (${state.x},${state.y})`);
    }
    state.x = nx;
    state.y = ny;
  }
}

function checkBeat(id, initial) {
  const beat = byId.get(id);
  if (!beat) fail(`beat ${id} missing`);
  const state = {...initial};
  for (const a of beat.actions || []) {
    if (a.kind === 'teleport') {
      if (typeof a.map === 'string') state.map = a.map;
      if (typeof a.x === 'number') state.x = a.x;
      if (typeof a.y === 'number') state.y = a.y;
      if (!isWalkable(state.map, state.x, state.y)) {
        fail(`${id}: teleport lands on blocked tile ${state.map} (${state.x},${state.y})`);
      }
    }
    if (a.kind === 'move') {
      walkPath(state, Array.isArray(a.path) ? a.path : [], id);
    }
  }
  return state;
}

// Intro chain must be safe and coherent.
const s0 = checkBeat('ch1_intro', {map: 'pallet_town', x: 9, y: 13});
if (s0.map !== 'oak_lab') fail(`ch1_intro should end in oak_lab, got ${s0.map}`);

const s1 = checkBeat('ch1_oak_mew_explain', {map: 'oak_lab', x: 5, y: 9});
if (s1.map !== 'viridian') fail(`ch1_oak_mew_explain should end in viridian, got ${s1.map}`);

checkBeat('ch1_viridian_arrival', {map: 'viridian', x: 9, y: 16});

console.log('[intro-preflight] OK');
