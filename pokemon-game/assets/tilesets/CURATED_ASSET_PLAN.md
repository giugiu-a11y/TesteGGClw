# Curadoria Técnica de Assets (2026-02-12)

## Objetivo
Padronizar o visual FRLG-like sem quebrar jogabilidade, priorizando os arquivos já enviados pelo usuário.

## Inventário validado
- `assets/tilesets`: **1741 arquivos**
- Integridade de referências no jogo:
  - `assets/sprites/user.sprites.json`: **OK (0 paths quebrados)**
  - `index.html` prebuilt map backgrounds: **OK (0 paths quebrados)**

## Base recomendada (usar como padrão)
1. `assets/tilesets/cities/`
- Mapas completos de cidade (externo + vários interiores no mesmo sheet).
- Melhor consistência de estilo FRLG.

2. `assets/tilesets/manual_environmental/`
- Cenários especiais de arco (Mt Moon, Saffron, Indigo, Rocket, etc).
- Usar preferencialmente como *prebuilt scene backgrounds*.

3. `assets/tilesets/characters/`
- Overworlds/NPCs completos.
- Mantém estilo do jogo original para movimentação e cenas.

4. `assets/tilesets/pokemon_sprites/`
- Batalha (front/back/icon) com cobertura ampla.

5. `assets/tilesets/trainers/`
- Retratos de treinador para batalhas/cutscenes.

6. `assets/tilesets/battle_terrain/`
- Fundos de batalha por terreno (grama, caverna, água, etc).

## Uso recomendado com cautela (não como tileset base de chão)
1. `assets/tilesets/missing_tiles/`
- Ótimo para completar lacunas de mapas e UI.
- Mistura sheet e mapas já compostos; usar por arquivo (não em massa).

2. `assets/tilesets/manual_ui/` e `assets/tilesets/interface/`
- Úteis para HUD/UI, mas precisam de escala e recorte consistentes.

3. `assets/tilesets/manual_items/`
- Catálogo rico, porém vários sheets não alinhados a grid 16x16.

## Não usar como base de render de tile 16x16 sem normalização
- Arquivos com dimensão fora de múltiplos de 16: **73 PNGs**.
- Esses arquivos funcionam melhor como:
  - background fixo de cena
  - sprite retrato
  - UI recortada
- Evitar usar diretamente no autotile/chão para não gerar "Frankenstein" visual.

## Critério de qualidade aprovado
- Estilo principal deve vir de `cities + manual_environmental + characters + pokemon_sprites`.
- Proibido fallback procedural visível em cenas principais.
- Cada mapa/cena deve ter origem artística explícita e consistente.

## Próximo passo técnico
- Criar uma `manifest` única por cena/mapa (fonte visual + offset + modo fixed).
- Travar renderer para recusar atlas inválido como tileset base.
- Completar mapeamento dos interiores faltantes por cidade usando os próprios sheets de `cities/`.
