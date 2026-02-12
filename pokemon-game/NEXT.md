# NEXT (Execucao)

## Prioridade 1 - Fechamento Manual (Release Candidate)
1. Rodar 20-30 min no iPad/Safari com:
   - `?tileset=external&reset=1&v=71319e8`
2. Validar trilha critica:
   - Pallet -> Oak Lab -> Viridian -> Forest -> Pewter -> Pewter Gym
3. Confirmar:
   - sem layer-over-layer no inicio
   - sem andar em parede/arvore/agua
   - entrada/saida por porta correta
   - sem freeze em battle/dialog/cutscene

## Prioridade 2 - Micro-polish Visual
1. Ajuste fino de `px/py` em `assets/tilesets/mapbg.manifest.json` (somente se teste visual pedir).
2. Ajustar detalhes de UI (contraste/legibilidade) mantendo estilo FR-like.
3. Não alterar pipeline local-only nem SceneManager.

## Prioridade 3 - Narrativa
1. Manter os 55 beats como baseline fechado.
2. Apenas ajustes de ritmo/pausa se algum ponto parecer abrupto no playtest.
3. Não reduzir cobertura de cenas já implementadas.

## Operacao
- Qualquer alteração deve passar:
  - `bash ci-check.sh`
- Validar checklist final:
  - `QA_CHECKLIST_RELEASE.md`
- Seguir governanca:
  - `OPERATIONS_PLAYBOOK.md`
  - atualizar `CHANGELOG_OPERACIONAL.md` a cada ciclo relevante
