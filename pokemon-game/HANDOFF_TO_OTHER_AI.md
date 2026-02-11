# HANDOFF TECNICO COMPLETO (Pokemon Game Web)

Data de referencia: 2026-02-11  
Repositorio: `/home/ubuntu/clawd`  
Projeto: `/home/ubuntu/clawd/pokemon-game`

## 1. Objetivo do Projeto
Construir um jogo web de Pokemon Adventures (manga), com jogabilidade estilo FireRed/FRLG, fluxo manga-first (confirm-only), progressao por cenas/flags e deploy estavel via GitHub Pages.

## 2. Estado Atual (real)
1. O projeto roda no browser e esta publicado em Pages.
2. Ha estrutura de mapas, warps, dialogos e batalhas scriptadas.
3. Story script esta externo em JSON (`story/season1.ptbr.json`) com 17+ blocos narrativos.
4. Engine de auto-progressao por flags/mapa existe (`tryAutoStoryBeat`).
5. Ainda NAO esta 100% final em fidelidade visual FireRed nem 100% manga literal.

## 3. URLs e Deploy
1. URL base: `https://giugiu-a11y.github.io/TesteGGClw/`
2. URL estilo atual recomendado: `https://giugiu-a11y.github.io/TesteGGClw/?tileset=punyworld`
3. Workflow Pages: `/home/ubuntu/clawd/.github/workflows/pages.yml`
4. QA noturno: `/home/ubuntu/clawd/.github/workflows/nightly-qa.yml`
5. Script de check local: `/home/ubuntu/clawd/pokemon-game/ci-check.sh`

## 4. Arquivos-Chave (onde mexer)
1. Engine principal: `/home/ubuntu/clawd/pokemon-game/index.html`
2. Story beats: `/home/ubuntu/clawd/pokemon-game/story/season1.ptbr.json`
3. Tileset atual: `/home/ubuntu/clawd/pokemon-game/assets/tilesets/punyworld.png`
4. Mapeamento de tiles: `/home/ubuntu/clawd/pokemon-game/assets/tilesets/punyworld.tileset.json`
5. Coordenacao: `/home/ubuntu/clawd/pokemon-game/COORDINATION.md`
6. Estado/TODO: `/home/ubuntu/clawd/pokemon-game/STATUS.md` e `/home/ubuntu/clawd/pokemon-game/NEXT.md`

## 5. Pontos de Integracao no `index.html` (funcoes e linhas aproximadas)
1. `runActions(...)` (acoes do story JSON): ~1089
2. `playBeat(id)` (disparador de beat + lock): ~1130
3. `tryLoadExternalTileset()` (carregamento tilesets): ~1297
4. `drawSprite(...)` (render de player/NPC): ~1425
5. `tryAutoStoryBeat()` (encadeamento automatico por flags/mapa): ~1715
6. `onMapEnter(mapId)` (hooks de entrada): ~1786
7. `loadGame()` (restore state): ~2489
8. `startNewGame()` (reset runtime + estado inicial): ~2512

## 6. Estrutura de Mapas (declarados em `MAPS`)
Ordem de definicao atual:
1. `pallet_town`
2. `route1`
3. `viridian`
4. `route2`
5. `pewter`
6. `route3`
7. `mt_moon`
8. `cerulean`
9. `vermilion`
10. `lavender`
11. `saffron`
12. `silph_lobby`
13. `pewter_gym`
14. `viridian_forest`
15. `player_house`
16. `rival_house`
17. `oak_lab`

## 7. Story Beats em `story/season1.ptbr.json` (ids atuais)
1. `ch1_intro`
2. `ch1_oak_mew_explain`
3. `ch1_viridian_arrival`
4. `ch1_viridian_forest_first`
5. `ch1_pewter_arrival`
6. `ch1_brock_intro`
7. `ch2_depart_pewter`
8. `ch2_mtmoon_entry`
9. `ch2_green_first_contact`
10. `ch2_rocket_grunt_cave`
11. `ch2_fossil_rumor`
12. `ch3_cerulean_arrival`
13. `ch3_misty_clash`
14. `ch3_bill_event`
15. `ch4_vermilion_setup`
16. `ch4_ssanne_rocket`
17. `ch5_surge_pressure`
18. `ch6_lavender_shadow`
19. `ch7_silph_infiltration`
20. `ch8_saffron_psychic`
21. `ch9_final_island_setup`
22. `ch10_mewtwo_confront`
23. `s1_outline_next`

## 8. Contrato de Acoes no Story JSON
Suportado hoje:
1. `kind: "dialog"` com `speaker` + `lines[]`
2. `kind: "set"` com `path` + `value`
3. `kind: "ensureTeam"` com `value: ["poli","saur","pika"]`
4. `kind: "battle"` com:
   - `enemy: {name,spr,lv,hp,maxHp}`
   - `options.scripted` (bool)
   - `options.scriptSteps[]` (log/playerMove/enemyMove/usePotion/capture/end)
   - `options.onEnd = "only_if_win"` para encadeamento seguro

## 9. Flags de Story importantes (GS.story)
Ja usadas:
1. `sawMew`
2. `gotPokedex`
3. `gotSaur`
4. `caughtPika`
5. `brockBattleDone`
6. `visitedViridian`
7. `visitedPewter`
8. `forestBeat1`
9. `block_02_done ... block_17_done`

Recomendacao para IA:
1. Padronizar nomes em prefixo de capitulo (`c1_`, `c2_`) ou manter `block_XX_done`.
2. Evitar criar flag sem adicionar migracao em `migrateSave`.

## 10. Sistema de Tileset (modo aberto para links)
Implementado em `tryLoadExternalTileset()`.

Modos:
1. `?tileset=punyworld` usa assets locais do projeto.
2. `?tileset=external` usa `assets/tilesets/user.png` + `user.tileset.json`.
3. `?tileset=remote&tilesetPng=...&tilesetJson=...` usa links remotos (salva em localStorage).

Helper global:
1. `setRemoteTileset('https://...png','https://...json')`

## 11. Formato obrigatorio do JSON de tiles
Estrutura minima:
1. `tileSize` (16)
2. `atlasCols` (numero de colunas do atlas)
3. `map` com chaves:
   - `GRASS`
   - `GRASS_ALT`
   - `PATH`
   - `PATH_ALT`
   - `WATER`
   - `TALL_GRASS`
   - `TREE`
   - `FENCE`
   - `SIGN`
   - `FLOWER`
   - `WARP`
   - `ROOF_RED`
   - `ROOF_BLUE`
   - `ROOF_LAB`
   - `WALL`
   - `DOOR`
   - `WINDOW`
   - `FLOOR_IN`
   - `WALL_IN`
   - `TABLE`
   - `SHELF`
4. Cada chave com `{ "ax": <int>, "ay": <int> }`

## 12. Erros reportados pelo usuario e correcoes recentes
1. Travar apos intro/dialogo:
   - corrigido com reset runtime em `startNewGame()` e `loadGame()`
   - lock de beat ativo para evitar reentrancia (`activeBeatId`)
2. Personagem nao aparecer:
   - corrigido com `drawSprite()` robusto + fallback visual
3. Estilo abrir no tileset errado:
   - default de tileset alterado para `punyworld`

## 13. O que falta para 100% (roteiro tecnico para outra IA)
1. Visual 90% FireRed:
   - substituir `punyworld` por tileset final escolhido (remote/local).
   - refinar mapeamento em `punyworld.tileset.json` ou novo `.tileset.json`.
   - melhorar UI battle/dialog para FRLG pixel-authentic.
2. Manga 100%:
   - revisar beat por beat com referencias.
   - adicionar cenas faltantes e transicoes exatas.
   - garantir coerencia de times/evolucoes/capturas.
3. Jogabilidade:
   - revisar colisao/warps em todos os mapas novos.
   - validar no iPad toque + dpad + A/B em sessao longa.
4. QA:
   - roteiro E2E manual:
     - NEW GAME
     - intro completa
     - movimentacao
     - progressao de todos os blocos sem soft-lock
   - manter `ci-check.sh` passando.

## 14. Ordem de Execucao recomendada para concluir
1. Fixar tiles final (remote/local) e validar render de todos os tiles-chave.
2. Congelar layer visual por commit.
3. Congelar story beats por capitulo, sem mexer no renderer.
4. Integrar trigger por mapa/flag com testes de regressao.
5. Rodar QA iPad e ajustar soft-locks.
6. Congelar versao candidata final.

## 15. Comandos uteis (local)
1. Validar JSON:
`python3 -m json.tool story/season1.ptbr.json >/dev/null`
2. Validar JS extraido:
`awk 'BEGIN{p=0} /<script>/{p=1;next} /<\/script>/{p=0} p{print}' index.html > /tmp/pokemon_game_script.js && node --check /tmp/pokemon_game_script.js`
3. Check completo:
`bash ci-check.sh`
4. Commit + push:
`git add ... && git commit -m \"...\" && git push origin main`

## 16. Nota de verdade tecnica
No estado atual, o projeto esta funcional e avancado, mas nao final 100% em:
1. fidelidade visual FireRed
2. fidelidade completa do manga (literal)
3. polimento final de jogabilidade em todos os capitulos

Este documento existe para outra IA continuar sem perda de contexto e sem retrabalho.
