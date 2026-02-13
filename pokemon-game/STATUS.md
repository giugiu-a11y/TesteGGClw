# STATUS (Pokemon Game)

Data: 2026-02-13

## Estado Atual
- Plataforma: `index.html` standalone + deploy em GitHub Pages.
- Runtime visual: **strict local-only** (sem URLs externas no script principal).
- Story script: `story/season1.ptbr.json` com **55 beats** conectados no runner (`55/55`).
- Fluxo: manga-first (`storyLock=true`), batalhas confirm-only e cutscenes roteirizadas.
- **Branch ativa:** `fix/gameplay-audit-v2`

## Correções de 2026-02-13 (HOJE)

### ✅ Tiles e Colisão
- Adicionados tiles faltantes: `ROOF_RED`, `ROOF_BLUE`, `ROOF_LAB`, `WALL`, `DOOR`, `WINDOW`, `PATH_ALT`, `GRASS_ALT`
- Lista SOLID atualizada para incluir telhados, paredes e janelas
- Personagem não atravessa mais paredes/telhados/janelas

### ✅ Movimento e Race Conditions
- Sistema de movimento refatorado com `moveSessionId` para prevenir callbacks órfãos
- Verificações estritas de `MODE.WORLD` antes de qualquer movimento
- `clearOrphanRuntimeLocks` agora para movimento em cutscenes
- Adicionada verificação de `activeBeatId` para prevenir movimento durante beats

### ✅ Bugs Corrigidos
1. ~~Personagem anda sozinho~~ → Corrigido
2. ~~Fica rotacionando~~ → Corrigido
3. ~~Anda automático em cenas~~ → Corrigido
4. ~~Atravessa paredes/telhados~~ → Corrigido
5. ~~Entra pela chaminé~~ → Corrigido (ROOF agora é sólido)

## Qualidade / Validações
- `bash ci-check.sh`: OK
- JSON (story/tiles/sprites/manifests): OK
- JS syntax (`index.html` script): OK
- Preflight de assets: OK
- Preflight de gameplay: OK (`maps=21`)
- Intro preflight: OK
- Full season preflight: OK (`beats=55`)

## Build Atual
- Branch: `fix/gameplay-audit-v2`
- Commit: `5f73ca6`

## Pendências
- [ ] Validação visual real em Safari/iPad
- [ ] Audit de cenários (padrão FRLG-like)
- [ ] Audit de fidelidade ao mangá (qualitativa)

## Link de Teste (após push)
- `https://giugiu-a11y.github.io/TesteGGClw/?tileset=external&reset=1&v=5f73ca6`

## Regra de Coordenação (2 IAs)
- Mudou fluxo/gameplay/story/tiles -> atualizar `STATUS.md` + `NEXT.md` no mesmo commit.
- Não reativar modos remotos/externos no runtime principal.
- Não quebrar `storyLock` e nem remover preflights do CI.
