#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[metatile-behavior-preflight] FAIL: ${msg}`);
  process.exit(1);
}

const root = path.resolve(__dirname, '..');
const indexPath = path.join(root, 'index.html');
const behaviorPath = path.join(root, 'assets/data/metatile_behaviors.json');
if (!fs.existsSync(indexPath)) fail('index.html missing');
if (!fs.existsSync(behaviorPath)) fail('assets/data/metatile_behaviors.json missing');

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
const payload = JSON.parse(fs.readFileSync(behaviorPath, 'utf8'));
const tiles = payload && typeof payload === 'object' ? payload.tiles : null;
if (!tiles || typeof tiles !== 'object') fail('tiles object missing');

const allowedEncounter = new Set(['none', 'land', 'water']);
let issues = 0;
let warnings = 0;

for (const [name, val] of Object.entries(tiles)) {
  if (!Object.prototype.hasOwnProperty.call(T, name)) {
    console.warn(`[metatile-behavior-preflight] WARN: unknown tile key '${name}'`);
    warnings++;
    continue;
  }
  if (!val || typeof val !== 'object') {
    console.error(`[metatile-behavior-preflight] ISSUE: ${name} must be object`);
    issues++;
    continue;
  }
  if (val.walk !== undefined && typeof val.walk !== 'boolean') {
    console.error(`[metatile-behavior-preflight] ISSUE: ${name}.walk must be boolean`);
    issues++;
  }
  if (val.encounter !== undefined && !allowedEncounter.has(val.encounter)) {
    console.error(`[metatile-behavior-preflight] ISSUE: ${name}.encounter invalid '${val.encounter}'`);
    issues++;
  }
}

for (const name of Object.keys(T)) {
  if (!Object.prototype.hasOwnProperty.call(tiles, name)) {
    console.warn(`[metatile-behavior-preflight] WARN: missing explicit behavior for ${name} (runtime fallback applies)`);
    warnings++;
  }
}

if (issues > 0) fail(`issues=${issues} warnings=${warnings}`);
console.log(`[metatile-behavior-preflight] OK tiles=${Object.keys(tiles).length} warnings=${warnings}`);
