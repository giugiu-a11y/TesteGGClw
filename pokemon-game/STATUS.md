# STATUS (Pokemon Game)

Data: 2026-02-12

## Estado Atual
- Plataforma: `index.html` standalone + deploy em GitHub Pages.
- Runtime visual: **strict local-only** (sem URLs externas no script principal).
- Story script: `story/season1.ptbr.json` com **55 beats** conectados no runner (`55/55`).
- Fluxo: manga-first (`storyLock=true`), batalhas confirm-only e cutscenes roteirizadas.

## Finalizado Hoje
- Governanca operacional adicionada:
  - `OPERATIONS_PLAYBOOK.md` (padrao de qualidade + anti-regressao + protocolo Telegram).
  - `CHANGELOG_OPERACIONAL.md` (historico tecnico-operacional continuo).
  - `send_release_telegram.sh` (envio com fallback automatico).
- Scene lifecycle hardening:
  - `SceneManager` ativo com `currentScene`, `unloadScene()`, `loadScene()`, `clearRenderLayer()`.
  - loop único de render com `startRenderLoop()` / `stopRenderLoop()`.
  - prevenção de render concorrente entre cenas/mapas.
- Transições e colisão:
  - `collisionGrid` por mapa com recarga a cada `loadScene`.
  - validação de warps/destinos/caminhabilidade em preflight.
  - ajustes de entrada/interiores com refinamento em `assets/tilesets/mapbg.manifest.json`.
- Sobreposição visual (layer-over-layer):
  - correção para evitar empilhar `sceneBackdrop` e `mapbg` idênticos na mesma cena.
- Pacing das cenas iniciais:
  - primeiros 5 beats com pausas e `stepMs` ajustados para fluidez narrativa.
- QA e contrato:
  - `tools/asset_preflight.py` + `tools/gameplay_preflight.js` no `ci-check.sh`.
  - checklist release consolidado em `QA_CHECKLIST_RELEASE.md`.

## Qualidade / Validacoes
- `bash ci-check.sh`: OK.
- JSON (story/tiles/sprites/manifests): OK.
- JS syntax (`index.html` script): OK.
- Preflight de assets: OK.
- Preflight de gameplay: OK (`maps=21`).

## Build Publicada
- Branch: `main`
- Commit atual publicado: `71319e8`

## Link de Teste
- `https://giugiu-a11y.github.io/TesteGGClw/?tileset=external&reset=1&v=71319e8`

## Regra de Coordenacao (2 IAs)
- Mudou fluxo/gameplay/story/tiles -> atualizar `STATUS.md` + `NEXT.md` no mesmo commit.
- Nao reativar modos remotos/externos no runtime principal.
- Nao quebrar `storyLock` e nem remover preflights do CI.
