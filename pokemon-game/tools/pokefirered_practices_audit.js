#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error(`[pokefirered-practices] FAIL: ${msg}`);
  process.exit(1);
}

const root = path.resolve(__dirname, '..');
const indexPath = path.join(root, 'index.html');
if (!fs.existsSync(indexPath)) fail('index.html missing');

const html = fs.readFileSync(indexPath, 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) fail('main <script> block not found');
const script = m[1];

const checks = [
  {
    id: 'map_headers_manifest',
    desc: 'Map headers/connections loaded from external manifest',
    must: ["tryLoadMapHeadersManifest", "assets/data/map_headers.json", "MAP_CONNECTIONS"]
  },
  {
    id: 'map_events_manifest',
    desc: 'Map events/warps/npcs loaded from external manifest',
    must: ["tryLoadMapEventsManifest", "assets/data/map_events.json", "applyMapEventsOverrides"]
  },
  {
    id: 'map_scripts_manifest',
    desc: 'Map scripts/coord triggers loaded from external manifest',
    must: ["tryLoadMapScriptsManifest", "assets/data/map_scripts.json", "checkMapScriptTrigger"]
  },
  {
    id: 'metatile_behavior_manifest',
    desc: 'Metatile behavior table loaded from external manifest',
    must: ["tryLoadMetatileBehaviorManifest", "assets/data/metatile_behaviors.json", "isTileWalkableForMap"]
  },
  {
    id: 'scene_lifecycle_manager',
    desc: 'Scene manager with explicit swap/unload lifecycle',
    must: ["const SceneManager", "swapScene(nextSceneId", "unloadScene(opts = {})", "clearRenderLayer()"]
  },
  {
    id: 'single_loop_guard',
    desc: 'Single active game loop guard in runtime',
    must: ["Runtime.activeLoops", "startRenderLoop()", "stopRenderLoop()"]
  },
  {
    id: 'mode_state_machine',
    desc: 'Global mode state machine gates input/runtime',
    must: ["const MODE", "setMode(mode)", "syncModeFromRuntime()"]
  },
  {
    id: 'warp_and_connection_traversal',
    desc: 'Warp route and border connection traversal for map transitions',
    must: ["findWarpRouteToMap", "findMapRouteByWarps", "tryMapConnectionStep"]
  },
  {
    id: 'save_schema_versioning',
    desc: 'Versioned save envelope and migration',
    must: ["SAVE_SCHEMA_VERSION", "buildSaveEnvelope", "migrateSave(gs)"]
  },
  {
    id: 'encounter_pipeline',
    desc: 'Encounter pipeline with autopilot and map encounter tables',
    must: ["checkEncounter()", "runAutopilotEncounter", "GAME_MODE"]
  }
];

let failed = 0;
for (const c of checks) {
  const miss = c.must.filter(tok => !script.includes(tok));
  if (miss.length) {
    failed++;
    console.error(`[pokefirered-practices] ISSUE: ${c.id} missing: ${miss.join(', ')}`);
  }
}

if (failed) fail(`missing_checks=${failed}/${checks.length}`);
console.log(`[pokefirered-practices] OK checks=${checks.length}`);
