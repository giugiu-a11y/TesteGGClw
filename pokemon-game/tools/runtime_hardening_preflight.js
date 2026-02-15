#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[runtime-hardening] FAIL: ${msg}`);
  process.exit(1);
}

const root = path.resolve(__dirname, '..');
const indexPath = path.join(root, 'index.html');
if (!fs.existsSync(indexPath)) fail('index.html missing');
const html = fs.readFileSync(indexPath, 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) fail('main <script> block not found');
const script = m[1];

function mustContain(re, msg) {
  if (!re.test(script)) fail(msg);
}

mustContain(/const\s+MODE\s*=\s*Object\.freeze\s*\(\s*\{[\s\S]*WORLD[\s\S]*DIALOG[\s\S]*MENU[\s\S]*SCRIPT[\s\S]*AUTOPILOT[\s\S]*LOADING[\s\S]*\}\s*\)/m,
  'MODE enum missing required states');
mustContain(/let\s+currentMode\s*=\s*MODE\.LOADING/, 'currentMode missing');
mustContain(/function\s+setMode\s*\(/, 'setMode missing');
mustContain(/function\s+modeIs\s*\(/, 'modeIs missing');

mustContain(/const\s+SceneManager\s*=\s*\{[\s\S]*getCurrentScene\s*\([\s\S]*clearRenderLayer\s*\([\s\S]*unloadScene\s*\([\s\S]*loadScene\s*\([\s\S]*swapScene\s*\(/m,
  'SceneManager lifecycle methods missing');

mustContain(/function\s+buildMapRuntimeLayers\s*\([\s\S]*ground[\s\S]*obstacle[\s\S]*overlay[\s\S]*collision[\s\S]*triggers/m,
  'buildMapRuntimeLayers must define GROUND/OBSTACLE/OVERLAY/COLLISION/TRIGGERS');
mustContain(/function\s+loadCollisionGrid\s*\([\s\S]*currentCollisionHash/m,
  'loadCollisionGrid must update collision hash');

mustContain(/Runtime\.activeLoops\s*=\s*1/, 'active loop increment missing');
mustContain(/Runtime\.activeLoops\s*=\s*0/, 'active loop decrement missing');

mustContain(/const\s+SAVE_SCHEMA_VERSION\s*=\s*2/, 'SAVE_SCHEMA_VERSION missing');
mustContain(/function\s+buildSaveEnvelope\s*\(/, 'buildSaveEnvelope missing');
mustContain(/schemaVersion\s*:\s*SAVE_SCHEMA_VERSION/, 'save envelope schema missing');

mustContain(/function\s+runAutopilotEncounter\s*\(/, 'autopilot encounter flow missing');
mustContain(/checkEncounter\s*\([\s\S]*runAutopilotEncounter\(/m, 'checkEncounter must use autopilot flow');
mustContain(/const\s+AUTO_CUTSCENE_MOVE\s*=\s*qs\('autocutmove',\s*'1'\)\s*===\s*'1'/, 'AUTO_CUTSCENE_MOVE query flag missing');
mustContain(/function\s+onDpadDown\s*\(/, 'pointer-safe D-pad handler missing');
mustContain(/function\s+onDpadUp\s*\(/, 'pointer-safe D-pad release missing');
mustContain(/function\s+onRunDown\s*\(/, 'pointer-safe run handler missing');
mustContain(/function\s+onRunUp\s*\(/, 'pointer-safe run release missing');

console.log('[runtime-hardening] OK');
