#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[map-headers-preflight] FAIL: ${msg}`);
  process.exit(1);
}

const root = path.resolve(__dirname, '..');
const htmlPath = path.join(root, 'index.html');
const headersPath = path.join(root, 'assets/data/map_headers.json');
if (!fs.existsSync(htmlPath)) fail('index.html missing');
if (!fs.existsSync(headersPath)) fail('assets/data/map_headers.json missing');

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
    if (depth === 0) { end = i; break; }
  }
}
if (end < 0) fail('MAPS parse failed');
const MAPS = eval(`(${script.slice(script.indexOf('{', start), end + 1)})`);

let headers;
try { headers = JSON.parse(fs.readFileSync(headersPath, 'utf8')); }
catch (err) { fail(`map_headers parse failed: ${err.message}`); }

const issues = [];
const warnings = [];
const conns = headers && typeof headers === 'object' ? headers.connections : null;
if (!conns || typeof conns !== 'object') fail('connections object missing');

for (const [mapId, edges] of Object.entries(conns)) {
  if (!MAPS[mapId]) {
    issues.push(`unknown source map: ${mapId}`);
    continue;
  }
  if (!edges || typeof edges !== 'object') {
    issues.push(`invalid edges for ${mapId}`);
    continue;
  }
  for (const dir of ['north', 'south', 'east', 'west']) {
    const c = edges[dir];
    if (!c) continue;
    if (!c.to || !MAPS[c.to]) {
      issues.push(`${mapId}.${dir}: invalid target map ${c && c.to}`);
      continue;
    }
    if (c.min !== undefined && !Number.isInteger(c.min)) issues.push(`${mapId}.${dir}: min must be integer`);
    if (c.max !== undefined && !Number.isInteger(c.max)) issues.push(`${mapId}.${dir}: max must be integer`);
    if (Number.isInteger(c.min) && Number.isInteger(c.max) && c.min > c.max) issues.push(`${mapId}.${dir}: min > max`);

    const targetEdges = conns[c.to] && typeof conns[c.to] === 'object' ? conns[c.to] : null;
    const hasBack = !!(targetEdges && ['north', 'south', 'east', 'west'].some(k => targetEdges[k] && targetEdges[k].to === mapId));
    if (!hasBack) {
      warnings.push(`${mapId}.${dir} -> ${c.to} lacks reverse connection`);
    }
  }
}

for (const w of warnings) console.warn(`[map-headers-preflight] WARN: ${w}`);
for (const e of issues) console.error(`[map-headers-preflight] ISSUE: ${e}`);
if (issues.length) {
  console.error(`[map-headers-preflight] FAIL issues=${issues.length} warnings=${warnings.length}`);
  process.exit(1);
}
console.log(`[map-headers-preflight] OK maps=${Object.keys(conns).length} warnings=${warnings.length}`);
