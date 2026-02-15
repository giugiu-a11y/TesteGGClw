# Regression Memory (Pokemon Game)

Objetivo: evitar repetir regressoes de jogabilidade, colisao e visual quando houver varias IAs mexendo no projeto.

## Erros recorrentes (historico)
- `mapbg.manifest.json` sobrescrevendo `index.html` com `ts/px/py` diferentes.
- Uso de mapa comprimido (`viridian_main_1x.png`) que miniaturizou Viridian e desalinhou colisao visual.
- Ajustes de story sem validar rota walkable (cutscene tentando mover para tile solido).
- Execucao paralela de comandos dependentes (ex.: sincronizar inline story e rodar CI ao mesmo tempo).

## Correcoes aplicadas
- Viridian voltou para sheet original com escala correta:
  - `./assets/tilesets/cities/3874_city_viridian.png`
  - `ts: 32, px: 8, py: 24`
- Route 2 e Viridian Forest calibrados para a mesma base de sheet:
  - `ts: 32, px: 8, py: 24` (route2)
  - `ts: 32, px: 8, py: 200` (viridian_forest)
- `ch1_intro` ajustado para remover movimento inicial inseguro e manter path valido.
- `viridian/route2/viridian_forest` foram ampliados para grid 2x (40x36 / 40x50 / 40x50) para evitar mapa miniaturizado e alinhar melhor colisao com os prebuilt.
- WARP bidirecional adicionado entre `route2 <-> viridian_forest` para fechar interligacao de caminhos.
- Intro sem teleport de `oak_lab -> viridian`: agora o jogador sai do laboratorio pela porta e segue pelos mapas.
- Sincronizacao de story inline padronizada:
  - atualizar `story/season1.ptbr.json`
  - regenerar `story/season1.ptbr.inline.js`
  - depois rodar CI (sequencial, nunca paralelo).
- Colisao por tipo de mapa endurecida com allowlist por classe:
  - `CITY_STRICT_WALKABLE`
  - `ROUTE_STRICT_WALKABLE`
  - `FOREST_STRICT_WALKABLE`
  - `INTERIOR_STRICT_WALKABLE`
  - `CAVE_STRICT_WALKABLE`
- `loadCollisionGrid()` agora considera tambem `solidRects` do `mapbg.manifest.json`.
- `runMovePath()` (movimento de cutscene) passou a chamar `checkWarp()` a cada passo para manter transicao real de mapa.
- `runActions(kind=teleport)` tenta primeiro rota por warp real (BFS) e so usa fallback de teleport quando necessario.
- Conexoes de borda estilo FireRed adicionadas (`MAP_CONNECTIONS`):
  - transicao por `north/south/east/west` para mapas principais de Kanto
  - aplicada em movimento manual e em `runMovePath` de cutscene
  - resolve casos em que jogador chega ao limite da rota/cidade e nao troca de mapa por falta de warp pontual
- `MAP_CONNECTIONS` agora pode ser carregado de `assets/data/map_headers.json` (fallback para default interno).
- Novo preflight `tools/map_headers_preflight.js` no `ci-check.sh`.
- Eventos de mapa externalizados em `assets/data/map_events.json` (warps/NPCs/encounters), com fallback para eventos internos.
- Novo preflight `tools/map_events_preflight.js` no `ci-check.sh`.
- Runner de historia aceita aliases de script estilo FireRed:
  - `message` -> `dialog`
  - `applyMovement` -> `move`
  - `warp` -> `teleport`
  - `setFlag`, `lock`, `release`
- Input mobile endurecido:
  - D-pad e botao B migrados para `pointer*` handlers dedicados (`onDpadDown/onDpadUp/onRunDown/onRunUp`)
  - trava de `pointerId` para evitar duplicidade touch+mouse no Safari/iPad
  - `touch-action: none` nos botoes de controle
- Runtime state machine explicitado:
  - `MODE` com estados `WORLD/DIALOG/MENU/SCRIPT/AUTOPILOT/LOADING`
  - `setMode()/modeIs()/syncModeFromRuntime()`
  - `SceneManager.swapScene()` com transicao controlada e `setMode(MODE.LOADING)`
  - `Runtime.activeLoops` controlado em `startRenderLoop()/stopRenderLoop()`
- Save envelope versionado:
  - `SAVE_SCHEMA_VERSION = 2`
  - `buildSaveEnvelope()` e suporte a carregar save antigo (GS cru) ou envelope novo
- `runtime_hardening_preflight` passou e foi adicionado ao `ci-check.sh`.
- Warps de `cinnabar -> indigo_plateau` corrigidos para destino walkable em `indigo_plateau`.
- MapBG endurecido para evitar desalinhamento render x colisao:
  - `sanitizeMapBgConfig()` aplicado no load do manifesto
  - `ts` forcado para `16` em runtime (paridade com `TILE`)
  - merge seguro `DEFAULT_PREBUILT_MAP_BG_CONFIG + manifest` (evita perder mapas quando manifesto parcial)
- CI ampliado para scripts de mapa:
  - `assets/data/map_scripts.json` validado em `ci-check.sh`
  - `tools/map_scripts_preflight.js` executado no `ci-check.sh`
  - preflight corrigido para parsear `T` antes de avaliar `MAPS`
- Preflight de movimento de historia adicionado:
  - `tools/story_motion_preflight.js`
  - simula `move`/`teleport` em todos os beats com checagem de bloqueio, out-of-bounds, warp e conexao de borda
  - incluido no `ci-check.sh`
- Acoes `teleport` da historia agora tentam travessia real por cadeia de warps antes de fallback:
  - `findMapRouteByWarps()`
  - `runWarpTraversalToMap()`
  - reduz saltos bruscos entre mapas nas cutscenes
- Preflight de conectividade de mapa adicionado:
  - `tools/map_reachability_preflight.js`
  - valida desconexao entre warps/NPCs e pontos isolados de entrada
  - incluido no `ci-check.sh`
- `pewter_gym` ajustado para porta dupla (2 tiles) ida/volta, removendo gargalo de entrada.
- Reset de input endurecido para evitar auto-movimento/rotacao fantasma:
  - `resetInputRuntimeState()`
  - chamado em `playBeat()`, `showDialog()`, `nextDialog()` (fechamento) e `onMapEnter()`
  - limpa pointers, run hold, fila de direcoes e timer de movimento.
- Preflight de jornada ponta-a-ponta adicionado:
  - `tools/journey_preflight.js`
  - simula progressao manual por warps (Pallet -> Route1 -> Viridian -> Center -> Route2 -> Forest -> Pewter -> Gym -> Route3 -> MtMoon -> Cerulean)
  - incluido no `ci-check.sh`
- Camada de comportamento de metatile (inspirada em `pret/pokefirered`) adicionada:
  - manifesto `assets/data/metatile_behaviors.json`
  - loader/sanitizacao em runtime (`tryLoadMetatileBehaviorManifest`)
  - `isTileWalkableForMap()` agora prioriza behavior table por tile
  - encounters usam behavior (`encounter: land`) em vez de hardcode fixo
  - preflight: `tools/metatile_behavior_preflight.js` + CI
- Cobertura narrativa RGB expandida:
  - beats principais aumentados para 73 (`story/season1.ptbr.json` + `story/season1.ptbr.inline.js` sincronizados)
  - adicoes: Erika, Koga, Blaine, Zapdos, Articuno, Moltres, Psyduck rescue e epilogo true closure
  - gatilhos `tryAutoStoryBeat` extendidos para `block_50_done .. block_58_done`
  - sprites/trainer portraits adicionados para novos encontros (Erika/Koga/Blaine e especies faltantes)
- Boas praticas do `pokefirered` formalizadas e auditadas:
  - `tools/pokefirered_practices_audit.js` no CI
  - matriz de adocao em `docs/pokefirered_adoption.md`
- Encounter cooldown por passos adicionado (anti spam de encontros):
  - `GAME_MODE.encounterCooldownSteps`
  - contador `encounterCooldown` decrementado por movimento valido
- Auditoria de fidelidade narrativa adicionada no CI:
  - `tools/story_fidelity_audit.js`
  - valida presenca de anchors RGB (leaders/legendarios/eventos chave), beats obrigatorios e consistencia de evolucoes
- Inconsistencia corrigida:
  - removida evolucao duplicada `SAUR -> IVYSAUR` em `ch25_training_push`

## Regras obrigatorias antes de release
1. Nao alterar `PREBUILT_MAP_BG_CONFIG` em `index.html` sem espelhar o mesmo ajuste em `assets/tilesets/mapbg.manifest.json`.
2. Nao usar mapas reduzidos/comprimidos em producao sem recalibrar `map.w/map.h` e colisao.
3. Toda acao `move` em beats deve passar no preflight de intro/season.
4. Toda mudanca visual de mapa deve preservar:
   - entrada por porta (sem entrada por telhado),
   - NPC em tile walkable,
   - warp em tile `T.WARP`,
   - destino de warp walkable.
5. Nao aprovar release se `tools/e2e_audit.js` ou `tools/warp_pair_preflight.js` falharem.
6. Em controles mobile, nao misturar `ontouch*` + `onmouse*` no mesmo botao de movimento.
7. Nao usar `ts` diferente de `16` em `mapbg.manifest.json` (quebra alinhamento visual/logico).

## Checklist de validacao (sempre executar)
1. `./ci-check.sh`
2. `node tools/qa_master_preflight.js`
3. `node tools/e2e_audit.js`
4. `node tools/warp_pair_preflight.js`
5. `node tools/runtime_hardening_preflight.js`
6. Validacao manual rapida no browser:
   - Intro completa sem freeze.
   - Controle livre apos `releaseControl`.
   - Viridian: nao andar em casa/arvore/montanha/agua.
   - Entrar/sair do Pokemon Center pela porta.
   - Transicao Viridian <-> Route 2 <-> Viridian Forest funcionando.
7. `node tools/story_motion_preflight.js`

## Padrao para futuras IAs
- Se ajustar colisao, registrar neste arquivo:
  - mapa afetado,
  - coordenadas alteradas (warp/NPC/spawn),
  - comando de validacao executado,
  - resultado.
