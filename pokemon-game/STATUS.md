# STATUS (Pokemon Game)

Data: 2026-02-11

## Estado Atual
- Plataforma: `index.html` standalone + deploy via GitHub Pages.
- Modo de jogo: `storyLock=true` (manga-first, sem grind RNG).
- Fluxo de batalha: confirm-only (OK/A), com passos roteirizados.
- Story script externo: `story/season1.ptbr.json` (beats iniciais ativos).

## Corrigido Hoje
- Travamento de dialogo (iPad/Pallet) resolvido:
  - em `nextDialog()`, limpeza de estado agora ocorre antes do callback.
- Fluxo duplicado de cutscene removido:
  - `checkWarp()` nao dispara mais roteiro legado de Oak Lab.
  - Gatilhos de historia centralizados em `onMapEnter()` e nos beats JSON.
- Layout revisado:
  - `pallet_town` redesenhado (estrada central, casas, lab, entradas).
  - `oak_lab` com corredor central e props laterais.
- Visual tileset:
  - `punyworld.tileset.json` com mapeamento de telhado/parede/porta atualizado.

## Riscos Abertos
- Mapeamento do Puny World ainda e aproximado (precisa refinamento fino por tile).
- Temporada 1 ainda parcial no JSON (falta lista grande de beats/cenas).
- Rede do servidor esta instavel para `git push` (DNS intermitente).

## Como Testar
- Pages:
  - `https://giugiu-a11y.github.io/TesteGGClw/`
  - `https://giugiu-a11y.github.io/TesteGGClw/?tileset=punyworld`
  - `https://giugiu-a11y.github.io/TesteGGClw/?tileset=punyworld&debug=1`

## Regra de Ouro (para 2 IAs)
- Qualquer alteracao de fluxo/historia/input deve atualizar este arquivo e `NEXT.md` no mesmo commit.
