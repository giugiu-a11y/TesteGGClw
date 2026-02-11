# NEXT (Execucao)

## Prioridade 1 - Teste de Aceite Final
1. Rodar no iPad com `?reset=1` e confirmar: intro -> spawn -> movimento -> progresso de beats sem freeze.
2. Validar links de tileset:
   - default (`external`)
   - `?tileset=punyworld`
   - `?tileset=remote&tilesetPng=...&tilesetJson=...`
3. Confirmar warps principais sem soft-lock (Pallet, Lab, Viridian, Pewter, Indigo).

## Prioridade 2 - Visual FireRed-like
1. Refinar `assets/tilesets/user.tileset.json` para fechamento de bordas/transicoes finas.
2. Ajustar UI de dialogo/batalha para paleta mais proxima FRLG usando os assets em `assets/tilesets/manual_ui` e `assets/tilesets/ui`.
3. Revisar sprites de player/NPC para consistencia de escala e anchor.

## Prioridade 3 - Story Fidelity
1. Manter script atual como baseline (55 beats).
2. Melhorar os 3 capitulos ainda nao cobertos explicitamente no auditor quantitativo.
3. Enriquecer dialogos principais mantendo jogabilidade fluida (sem quebrar storyLock).

## Operacao
- Qualquer alteracao grande deve passar `bash ci-check.sh` antes de commit.
- Atualizar `MANGA_AUDIT_REPORT_2026-02-11.md` sempre que mexer em cobertura narrativa.
