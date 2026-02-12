# QA Checklist Release (Pokemon Web - Safari + GitHub Pages)

Data: 2026-02-12
Escopo: qualidade técnica + consistência visual + jogabilidade

## 1) Engine / Loop / Cena
- [x] Apenas um loop de render ativo (`startRenderLoop`/`stopRenderLoop`).
- [x] SceneManager implementado (`currentScene`, `unloadScene`, `loadScene`, `clearRenderLayer`).
- [x] Transição de mapa desmonta cena anterior antes de montar nova.
- [x] Canvas é limpo antes de renderizar a cena atual.
- [x] Estado transitório (dialog/battle/overlay/input) não vaza entre cenas.

## 2) Tilemap / Colisão / Movimento
- [x] `collisionGrid` por mapa implementado.
- [x] `collisionGrid` recarregado a cada troca de cena/mapa.
- [x] Tiles sólidos bloqueiam movimento (árvore/parede/água/etc).
- [x] Warps validados (destino existe, dentro de bounds e caminhável).
- [x] Preflight de gameplay ativo no CI.
- [ ] Ajuste fino manual de 2-3 pontos de colisão visual (playtest humano).

## 3) Assets / Visual / Consistência
- [x] Runtime sem URLs externas no script principal.
- [x] Tileset base em modo estrito local (`user.png` + `user.tileset.json`).
- [x] Sprites carregados localmente (`./assets/...`).
- [x] `mapbg.manifest.json` cobre mapas jogáveis.
- [x] `scene_backdrop.manifest.json` ativo para cutscenes.
- [x] Regras para evitar layer-over-layer em mapbg + scene backdrop.
- [ ] Micro-ajuste visual de offsets por mapa após playtest final.

## 4) Story / Fluxo / Batalha
- [x] Beats da história conectados ao runner (55/55).
- [x] Sequência inicial com pacing refinado (pausas + stepMs).
- [x] Batalha/cutscene com fail-safe para evitar soft-lock.
- [x] Teleportes e hooks de história com fluxo estável.
- [ ] Revisão final humana de ritmo narrativo (10-15 min jogando).

## 5) Save / Recuperação
- [x] Save primário + backup.
- [x] Migração de save (`migrateSave`) para compatibilidade.
- [x] Autosave em movimento/warp/story.
- [x] Flag de reset para limpar estado antigo (`?reset=1`).

## 6) Safari / Mobile / GitHub Pages
- [x] Input touch/pointer/click com fallback iPad/Safari.
- [x] Pixel art com `imageSmoothingEnabled = false`.
- [x] Build estável no GitHub Pages (cache bust por `?v=<commit>`).
- [x] Caminhos relativos compatíveis com AWS local e Pages.
- [ ] Rodada manual específica Safari (iPad): 20 min contínuos.

## 7) CI / Preflight
- [x] `ci-check.sh` valida JSON story/tileset/sprites.
- [x] `ci-check.sh` valida JS do `index.html`.
- [x] `asset_preflight.py` ativo.
- [x] `gameplay_preflight.js` ativo.

## Status geral
- Técnico/arquitetura: **Pronto**
- Estabilidade de runtime: **Pronto**
- Consistência visual base: **Pronto**
- Polimento final humano (visual + sensorial): **Pendente leve**

## Roteiro curto de fechamento (manual)
1. Abrir com `?tileset=external&reset=1&v=<commit>` e jogar 10-15 min.
2. Validar transições: Pallet -> Oak Lab -> Viridian -> Forest -> Pewter Gym.
3. Confirmar: sem sobreposição de cena, sem andar em parede, sem entrada fora da porta.
4. Confirmar 3 batalhas seguidas sem travar UI/cutscene.

