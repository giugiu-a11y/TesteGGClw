# NEXT (Execucao)

## Prioridade 1 - Fechar Base Jogavel
1. Validar no iPad que o intro completo avanca sem travar (ch1_intro inteiro).
2. Validar entrada/saida de casas + Oak Lab com novo layout de Pallet.
3. Ajustar colisao/warps se algum tile de porta ficar desalinhado.

## Prioridade 2 - Visual FireRed-like (sem retrabalho)
1. Refinar `assets/tilesets/punyworld.tileset.json` com coordenadas finais.
2. Revisar tiles de interior (`FLOOR_IN`, `WALL_IN`, `TABLE`, `SHELF`) para nao parecer placeholder.
3. Padronizar paleta de UI (dialog/battle) para combinar melhor com overworld.

## Prioridade 3 - Story Season 1
1. Expandir beats em `story/season1.ptbr.json`:
   - Viridian chegada
   - Floresta / encontro chave
   - Rocket setup
   - Pewter arco inicial
2. Ligar cada beat a trigger claro (`onMapEnter`, fala NPC, batalha scriptada).
3. Manter `sourceRef` por beat para rastreabilidade de fidelidade.

## Regras Operacionais
- Nao voltar a logica de cutscene dentro de `checkWarp()`.
- Nao quebrar `storyLock` (sem grind manual).
- Mudanca grande = atualizar `STATUS.md` + este arquivo no mesmo commit.
