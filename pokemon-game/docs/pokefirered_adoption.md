# Pokefirered Best-Practice Adoption Matrix

Source benchmark: `../pokefirered` (pret/pokefirered architecture patterns).

## Adopted
- Map headers/connections externalized (`assets/data/map_headers.json` + runtime loader).
- Map events externalized (`assets/data/map_events.json` for warps/NPC/encounters).
- Map scripts externalized (`assets/data/map_scripts.json` for coord triggers).
- Metatile behavior table externalized (`assets/data/metatile_behaviors.json`).
- Scene lifecycle manager with controlled swap/unload/load.
- Single game-loop guard (`Runtime.activeLoops`).
- Global runtime mode gate (`MODE`: WORLD/DIALOG/MENU/SCRIPT/AUTOPILOT/LOADING).
- Warp-pair consistency checks and route traversal fallback for cutscene teleports.
- Versioned saves + migration path.
- Encounter pipeline with deterministic scripted/autopilot support.
- Encounter cooldown steps (anti immediate retrigger), inspired by encounter cooldown handling.

## Partially Adopted
- Event object model is simplified compared to ROM object templates.
- Script engine supports core aliases (`lock/release/setFlag/message/applyMovement/warp`) but is not full command parity.
- Encounter system is story-first; full FR encounter table complexity (time/day/ability hooks) is intentionally reduced.

## Not Adopted (by design)
- Full C-engine level movement/collision internals (`MapGridGetMetatileBehaviorAt` level behavior matrix with every edge case).
- Full disassembly-scale command set and macro pipeline.
- Full ROM build graph, assembler macros, and low-level task scheduler behaviors.

## Guard Rails
- CI includes explicit audit: `tools/pokefirered_practices_audit.js`.
- CI/preflights include map, story-motion, journey, warp, runtime, and behavior validation.
