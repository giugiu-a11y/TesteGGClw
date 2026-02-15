#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[story-fidelity-audit] FAIL: ${msg}`);
  process.exit(1);
}

const root = path.resolve(__dirname, '..');
const storyPath = path.join(root, 'story/season1.ptbr.json');
if (!fs.existsSync(storyPath)) fail('story/season1.ptbr.json missing');
const story = JSON.parse(fs.readFileSync(storyPath, 'utf8'));
const beats = Array.isArray(story.beats) ? story.beats : [];
if (!beats.length) fail('no beats');

const issues = [];
const warnings = [];
const text = JSON.stringify(story).toLowerCase();

// Coverage anchors for RGB arc fidelity (adapted form, not literal manga transcript).
const requiredMentions = [
  'brock','misty','surge','erika','koga','blaine','giovanni','sabrina',
  'mewtwo','articuno','zapdos','moltres','bulbasaur','pikachu','psyduck','arbok'
];
for (const k of requiredMentions) {
  if (!text.includes(k)) issues.push(`missing narrative anchor: ${k}`);
}

// Ensure key beats exist.
const requiredBeats = [
  'ch1_intro','ch1_oak_mew_explain','ch3_misty_clash','ch5_surge_pressure',
  'ch10_mewtwo_confront','ch13_viridian_giovanni','ch16_blue_champion',
  'ch43_erika_alliance','ch44_koga_counterattack','ch45_blaine_cinnabar_test',
  'ch46_powerplant_zapdos','ch47_seafoam_articuno','ch48_victoryroad_moltres',
  'ch49_psyduck_rescue','ch50_rgb_true_epilogue'
];
const beatSet = new Set(beats.map(b => b && b.id).filter(Boolean));
for (const b of requiredBeats) {
  if (!beatSet.has(b)) issues.push(`missing beat: ${b}`);
}

// Dialog density sanity.
let dialogs = 0;
let battles = 0;
let evolves = 0;
for (const b of beats) {
  for (const a of (b.actions || [])) {
    if (a.kind === 'dialog') dialogs++;
    if (a.kind === 'battle') battles++;
    if (a.kind === 'evolve') evolves++;
  }
}
if (dialogs < 250) warnings.push(`low dialog density: ${dialogs}`);
if (battles < 20) warnings.push(`low battle density: ${battles}`);
if (evolves < 2) warnings.push(`low evolution density: ${evolves}`);

// Evolution consistency for SAUR chain.
const saurEvos = [];
for (const b of beats) {
  for (const a of (b.actions || [])) {
    if (a.kind === 'evolve' && a.slot === 'saur' && typeof a.to === 'string') saurEvos.push({beat:b.id,to:a.to});
  }
}
const seen = new Set();
for (const e of saurEvos) {
  if (seen.has(e.to)) issues.push(`duplicate SAUR evolution target: ${e.to} (beat ${e.beat})`);
  seen.add(e.to);
}

for (const w of warnings) console.warn(`[story-fidelity-audit] WARN: ${w}`);
for (const i of issues) console.error(`[story-fidelity-audit] ISSUE: ${i}`);
if (issues.length) fail(`issues=${issues.length} warnings=${warnings.length}`);
console.log(`[story-fidelity-audit] OK beats=${beats.length} dialogs=${dialogs} battles=${battles} evolves=${evolves} warnings=${warnings.length}`);
