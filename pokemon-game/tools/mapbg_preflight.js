#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[mapbg-preflight] FAIL: ${msg}`);
  process.exit(1);
}

const root = path.resolve(__dirname, '..');
const htmlPath = path.join(root, 'index.html');
const manifestPath = path.join(root, 'assets/tilesets/mapbg.manifest.json');
if (!fs.existsSync(htmlPath)) fail('index.html missing');
if (!fs.existsSync(manifestPath)) fail('mapbg.manifest.json missing');

const html = fs.readFileSync(htmlPath, 'utf8');
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) fail('main <script> block not found');
const script = scriptMatch[1];

function grabConst(name) {
  const rx = new RegExp(`const\\s+${name}\\s*=\\s*([\\s\\S]*?);\\n\\s*\\n`);
  const mm = script.match(rx);
  if (!mm) fail(`const ${name} not found`);
  return mm[1];
}

const styleLockMaps = eval(grabConst('STYLE_LOCK_CORE_MAPS'));
// Needed because MAPS initializer references T.* constants.
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

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const mapbg = manifest && manifest.mapbg ? manifest.mapbg : null;
if (!mapbg || typeof mapbg !== 'object') fail('manifest.mapbg missing');

const issues = [];
const pushIssue = (msg) => issues.push(msg);

for (const mapId of styleLockMaps) {
  if (!mapbg[mapId]) pushIssue(`style-lock map missing in manifest: ${mapId}`);
}

for (const [mapId, conf] of Object.entries(mapbg)) {
  const map = MAPS[mapId];
  if (!map) {
    pushIssue(`manifest map not present in MAPS: ${mapId}`);
    continue;
  }
  const url = conf.url;
  if (typeof url !== 'string' || !url.trim()) {
    pushIssue(`${mapId}: invalid url`);
    continue;
  }
  const imgPath = path.join(root, url.replace(/^\.\//, ''));
  if (!fs.existsSync(imgPath)) {
    pushIssue(`${mapId}: missing image ${url}`);
    continue;
  }

  const ts = Number.isFinite(conf.ts) ? conf.ts : 16;
  if (ts !== 16) {
    pushIssue(`${mapId}: ts must be 16 for collision/render parity (got ${conf.ts})`);
    continue;
  }

  const srcW = map.w * ts;
  const srcH = map.h * ts;

  // Parse PNG dimensions from header (IHDR) without dependencies.
  const fd = fs.openSync(imgPath, 'r');
  try {
    const sig = Buffer.alloc(24);
    fs.readSync(fd, sig, 0, 24, 0);
    // PNG width/height are bytes 16..23 in the file.
    const imgW = sig.readUInt32BE(16);
    const imgH = sig.readUInt32BE(20);

    const originX = Number.isFinite(conf.px) ? Math.floor(conf.px) : Math.floor((conf.ox || 0) * ts);
    const originY = Number.isFinite(conf.py) ? Math.floor(conf.py) : Math.floor((conf.oy || 0) * ts);

    if (srcW > imgW || srcH > imgH) {
      pushIssue(`${mapId}: viewport ${srcW}x${srcH} larger than image ${imgW}x${imgH}`);
      continue;
    }
    if (originX < 0 || originY < 0 || originX >= imgW || originY >= imgH) {
      pushIssue(`${mapId}: invalid origin (${originX},${originY}) for image ${imgW}x${imgH}`);
      continue;
    }
    if (conf.fixed) {
      if (originX + srcW > imgW || originY + srcH > imgH) {
        pushIssue(`${mapId}: fixed crop out of bounds origin=(${originX},${originY}) size=${srcW}x${srcH} image=${imgW}x${imgH}`);
      }
    }
  } finally {
    fs.closeSync(fd);
  }
}

if (issues.length) {
  for (const msg of issues.slice(0, 80)) {
    console.error(`[mapbg-preflight] ISSUE: ${msg}`);
  }
  fail(`${issues.length} issue(s) found`);
}

console.log(`[mapbg-preflight] OK maps=${Object.keys(mapbg).length}`);
