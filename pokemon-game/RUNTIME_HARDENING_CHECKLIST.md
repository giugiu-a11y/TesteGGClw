# Runtime Hardening Checklist

Objetivo: garantir jogabilidade estável + consistência visual no fluxo inteiro.

## 1) Integridade de Movimento e Input

- [x] Travar input durante cutscene (`cutsceneLock`) para evitar estados inválidos.
- [x] Destravar input no fim de beat e em reset de sessão.
- [x] Garantir avanço de diálogo por tap/click/pointer com debounce.

## 2) Integridade de Fluxo de História

- [x] Suportar ações de cena (`move`, `teleport`, `pause`, `face`) no runner.
- [x] Evitar deadlock em batalhas `only_if_win` (fallback de continuação).
- [x] Introdução com encenação real (movimento + batalha visível de Mew).

## 3) Integridade de Save

- [x] Save principal + backup + metadado de recuperação.
- [x] Autosave em movimento, warp, ações de história e início de jogo.
- [x] `?reset=1` limpa estado completo (principal/backup/meta).

## 4) Consistência Visual

- [x] Padronizar UI de batalha com assets locais.
- [x] Padronizar portraits de treinador por contexto.
- [x] Desabilitar overlays prebuilt no gameplay para evitar desalinhamento com colisão/warps.
- [x] Manter backdrops de cena para beats manga sem referência 1:1.

## 5) Validações

- [x] `node --check` do script extraído de `index.html`.
- [x] JSON de história válido.
- [x] JSON de sprites/tileset válido.
