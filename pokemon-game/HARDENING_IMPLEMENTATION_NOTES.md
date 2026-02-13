# Runtime Hardening Implementation Notes

## Authoritative collision data
- Source of truth: `MAPS[mapId].data` + optional `PREBUILT_MAP_BG_CONFIG[mapId].solidRects`.
- Rebuild path: `SceneManager.loadScene()` -> `loadCollisionGrid(mapId)` -> `buildMapRuntimeLayers(mapId)`.
- Runtime hash: `currentCollisionHash` / `Runtime.collisionGridHash` (FNV-like hash from `Uint8Array`).
- Runtime layer schema produced on load: `GROUND`, `OBSTACLE`, `OVERLAY`, `COLLISION`, `TRIGGERS`.

## Single active update/render loop guarantee
- Guard in `startRenderLoop()`: early return when `renderLoopActive` is already true.
- Token invalidation in `stopRenderLoop()` and `startRenderLoop()` (`renderLoopToken`) prevents old RAF chains.
- Runtime counter: `Runtime.activeLoops` must stay `0` or `1`.

## Player hitbox definition
- Foot-anchor hitbox helper: `playerFootHitbox()`.
- Definition: `{ x: GS.px*16 + 2, y: GS.py*16 + 8, w: 12, h: 8 }` in world pixels.
- Rendering scale conversion: multiplied by `SCALE_FACTOR` for debug overlay.

## Exact scene swap sequence
- Entry: `SceneManager.swapScene(nextSceneId, spawnPoint, transitionType, opts)`.
- Sequence:
  1. `setMode(LOADING)`
  2. stop movement/timers tied to movement (`stopMove`, `cancelStoryMove`)
  3. stop scene audio hook (`__audioStopBgm`, optional)
  4. `unloadScene(current)` (clear scene listeners, clear render, optionally reset flow state)
  5. clear renderer (`clearRenderLayer`)
  6. `loadScene(nextSceneId, spawnPoint)`
  7. rebuild collision (`loadCollisionGrid`)
  8. normalize spawn (`ensureWalkablePlayerPosition`)
  9. start audio hook (`__audioPlayBgm`, optional)
  10. `setMode(nextMode)`

## Style validators and build rejection rules
- CI preflight script: `tools/runtime_hardening_preflight.js`.
- Fails build when missing:
  - required `MODE` states and gating helpers
  - `SceneManager` lifecycle API (`getCurrentScene`, `unloadScene`, `loadScene`, `swapScene`, `clearRenderLayer`)
  - collision rebuild/hash pipeline
  - save schema envelope (`SAVE_SCHEMA_VERSION`, `buildSaveEnvelope`)
  - autopilot encounter path usage
  - listener policy (raw `addEventListener` calls outside helper)

## Autopilot encounter state machine and re-entrancy control
- Lock: `autopilotEncounterLock` (single encounter flow at a time).
- Entry guard in `checkEncounter()`:
  - only in `MODE.WORLD`
  - no lock active
  - cooldown (`GS.encounterCooldown`) must be zero
- Flow:
  1. `setMode(AUTOPILOT)`
  2. freeze movement
  3. show encounter dialog micro-scene
  4. deterministic policy (`shouldAutopilotCapture`)
  5. capture simulation and party/storage assignment
  6. apply cooldown and save
  7. unlock + return to `MODE.WORLD`
