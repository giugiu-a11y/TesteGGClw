#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[story-inline-sync] FAIL: ${msg}`);
  process.exit(1);
}

const root = path.resolve(__dirname, '..');
const jsonPath = path.join(root, 'story/season1.ptbr.json');
const inlinePath = path.join(root, 'story/season1.ptbr.inline.js');
if (!fs.existsSync(jsonPath)) fail('story/season1.ptbr.json missing');
if (!fs.existsSync(inlinePath)) fail('story/season1.ptbr.inline.js missing');

const srcJson = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
const inlineRaw = fs.readFileSync(inlinePath, 'utf8');
const m = inlineRaw.match(/window\.__POKEMON_STORY__\s*=\s*([\s\S]*?);\s*$/);
if (!m) fail('window.__POKEMON_STORY__ assignment missing');

let inlineJson;
try {
  inlineJson = JSON.parse(m[1]);
} catch (err) {
  fail(`inline JSON parse failed: ${err.message}`);
}

const a = JSON.stringify(srcJson);
const b = JSON.stringify(inlineJson);
if (a !== b) {
  fail('inline story is out of sync with season1.ptbr.json');
}

console.log('[story-inline-sync] OK');
