# STATUS (Pokemon Game)

Data: 2026-02-11

## Estado Atual
- Plataforma: `index.html` standalone + deploy em GitHub Pages.
- Modo: `storyLock=true` (manga-first, sem grind manual).
- Fluxo: batalha confirm-only com dano/eventos roteirizados.
- Story script: `story/season1.ptbr.json` com **55 beats** (`ch1..ch42` + fechamento).
- Encadeamento: runner em `index.html` cobre todos os beats (incluindo `s1_outline_next`).

## Finalizado Nesta Rodada
- Corrigido beat sem trigger no final:
  - `s1_outline_next` agora dispara em `indigo_plateau` apos `block_49_done`.
  - beat final marca `story.block_50_done` para evitar replay infinito.
- Tileset default alterado para `external`:
  - jogo passa a usar `assets/tilesets/user.png` + `assets/tilesets/user.tileset.json` por padrao.
  - `?tileset=punyworld` e `?tileset=remote` continuam disponiveis.
- Integracao de assets externos mantida:
  - sprites/NPC/Pokemon via `assets/sprites/user.sprites.json`.
  - mapeamentos de tiles e sprites validados com `json.tool`.

## Qualidade / Validacoes
- `bash ci-check.sh`: OK.
- JSON story/tiles/sprites: OK.
- JS syntax (`index.html` script): OK.
- Auditoria de fidelidade: `MANGA_AUDIT_REPORT_2026-02-11.md` (>=75% atingido no criterio definido).

## Links de Teste
- Pages (pack local por padrao):
  - `https://giugiu-a11y.github.io/TesteGGClw/?reset=1`
- Forcar punyworld:
  - `https://giugiu-a11y.github.io/TesteGGClw/?tileset=punyworld&reset=1`
- Debug:
  - `https://giugiu-a11y.github.io/TesteGGClw/?debug=1&reset=1`

## Regra de Coordenacao (2 IAs)
- Mudou fluxo/gameplay/story/tiles -> atualizar `STATUS.md` + `NEXT.md` no mesmo commit.
- Nao recolocar cutscene legada em `checkWarp()`.
- Nao quebrar `storyLock`.
