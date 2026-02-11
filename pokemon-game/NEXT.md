# NEXT (Execucao)

## Prioridade 1 - Fechar Base Jogavel
1. Testar no iPad o fluxo completo ate `ch17_season1_epilogue` (sem freeze e sem replay indevido).
2. Validar cadeia de mapas nova: `saffron -> fuchsia -> cinnabar -> indigo_plateau`.
3. Revisar warps de retorno (`indigo_plateau <-> viridian_gym <-> saffron`) para evitar soft-lock.

## Prioridade 2 - Visual FireRed-like (sem retrabalho)
1. Refinar `assets/tilesets/punyworld.tileset.json` com coordenadas finais.
2. Revisar blocos de predio (telhado/parede/porta/janela) para reduzir efeito "placeholder".
3. Padronizar paleta de UI (dialog/battle) para combinar melhor com overworld.

## Prioridade 3 - Story Season 1
1. Story fidelity do arco RGB: CONCLUIDO (checklist 49/49 coberto).
2. Trocar placeholders de sprites faltantes por assets corretos.
2. Ligar cada beat a trigger claro (`onMapEnter`, fala NPC, batalha scriptada).
3. Manter `sourceRef` por beat para rastreabilidade de fidelidade.
4. Manter `MANGA_FIDELITY_CHECKLIST.md` como gate de regressao (nao reabrir `parcial` sem motivo).

## Regras Operacionais
- Nao voltar a logica de cutscene dentro de `checkWarp()`.
- Nao quebrar `storyLock` (sem grind manual).
- Mudanca grande = atualizar `STATUS.md` + este arquivo no mesmo commit.
