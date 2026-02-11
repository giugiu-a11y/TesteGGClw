# Manga Fidelity Checklist (RGB Arc)

Data: 2026-02-11
Escopo: auditoria de fidelidade de roteiro/cenas/dialogos do arco RGB (Pokemon Adventures) no webgame.

Legenda de status:
- `coberto`: cena/beat existe e esta encadeada no fluxo jogavel.
- `parcial`: existe no jogo, mas ainda simplificada (dialogo curto, sem subcena ou sem detalhe de transicao).
- `faltando`: ainda nao implementado de forma explicita.

## Capitulo 1 - Intro, Mew e Oak Lab
- [x] `coberto` Red em Pallet com Poliwhirl (boast inicial) -> `ch1_intro`
- [x] `coberto` avistamento de Mew na floresta -> `ch1_intro`
- [x] `coberto` tentativa de captura e falha -> `ch1_intro`
- [x] `coberto` briefing de Oak sobre Mew -> `ch1_oak_mew_explain`
- [x] `coberto` entrega de Pokedex + Saur -> `ch1_oak_mew_explain`
- [x] `coberto` variacoes de falas secundarias de NPCs de Pallet

## Capitulo 2 - Viridian e floresta
- [x] `coberto` chegada em Viridian com foreshadow -> `ch1_viridian_arrival`
- [x] `coberto` primeiro incidente na floresta (batalha scriptada) -> `ch1_viridian_forest_first`
- [x] `coberto` subcenas de deslocamento entre areas da floresta

## Capitulo 3 - Pewter, Rocket e Brock
- [x] `coberto` chegada em Pewter + tensao Rocket -> `ch1_pewter_arrival`
- [x] `coberto` resgate/captura de Pikachu (scriptado) -> `ch1_pewter_arrival`
- [x] `coberto` confronto com Brock -> `ch1_brock_intro`
- [x] `coberto` detalhamento dialogado da transicao pre e pos batalha de Brock

## Capitulo 4 - Mt. Moon e Green
- [x] `coberto` saida de Pewter e entrada em Mt. Moon -> `ch2_depart_pewter`, `ch2_mtmoon_entry`
- [x] `coberto` primeiro contato com Green -> `ch2_green_first_contact`
- [x] `coberto` confronto com Rocket em caverna -> `ch2_rocket_grunt_cave`
- [x] `coberto` plot de fosseis -> `ch2_fossil_rumor`
- [x] `coberto` subeventos de navegação interna na caverna

## Capitulo 5 - Cerulean e Bill
- [x] `coberto` chegada em Cerulean -> `ch3_cerulean_arrival`
- [x] `coberto` clash com Misty -> `ch3_misty_clash`
- [x] `coberto` evento de Bill -> `ch3_bill_event`
- [x] `coberto` cenas de interacao local com NPCs de cidade

## Capitulo 6 - Vermilion e S.S. Anne
- [x] `coberto` setup de Vermilion -> `ch4_vermilion_setup`
- [x] `coberto` incidente Rocket no navio -> `ch4_ssanne_rocket`
- [x] `coberto` pressao/tom de Surge -> `ch5_surge_pressure`
- [x] `coberto` detalhamento de transicoes entre porto/navio/cidade

## Capitulo 7 - Lavender, Silph e Saffron
- [x] `coberto` tom sombrio de Lavender -> `ch6_lavender_shadow`
- [x] `coberto` infiltracao da Silph -> `ch7_silph_infiltration`
- [x] `coberto` escalada psiquica em Saffron -> `ch8_saffron_psychic`
- [x] `coberto` subcenas internas de torre/andares

## Capitulo 8 - Mewtwo e fechamento do conflito maior
- [x] `coberto` setup final de ilha/lab -> `ch9_final_island_setup`
- [x] `coberto` confronto com Mewtwo -> `ch10_mewtwo_confront`
- [x] `coberto` aftershock e fechamento inicial -> `ch11_aftershock_recovery`
- [x] `coberto` cenas curtas de consequencia por personagem secundario

## Capitulo 9 - Cinnabar e rastros de pesquisa
- [x] `coberto` investigacao de laboratorio em Cinnabar -> `ch12_cinnabar_research`
- [x] `coberto` batalha de cleanup contra remanescente -> `ch12_cinnabar_research`
- [x] `coberto` microcenas de descoberta de documentos/artefatos

## Capitulo 10 - Viridian Gym e Giovanni
- [x] `coberto` confronto direto com Giovanni -> `ch13_viridian_giovanni`
- [x] `coberto` preambulo dialogado mais longo de rivalidade/ideologia

## Capitulo 11 - Indigo e decisao final
- [x] `coberto` abertura de Indigo -> `ch14_indigo_opening`
- [x] `coberto` embate com Lance -> `ch15_elite_lance`
- [x] `coberto` duelo com Blue -> `ch16_blue_champion`
- [x] `coberto` epilogo de temporada -> `ch17_season1_epilogue`

## Capitulo 12 - Pos-epilogo imediato (coerencia de temporada)
- [x] `coberto` debrief com Oak -> `ch18_oak_debrief`
- [x] `coberto` reveal de Green e alinhamento de trio -> `ch19_green_reveal`, `ch23_team_unity`
- [x] `coberto` aviso estrategico de Lance -> `ch20_lance_warning`
- [x] `coberto` remanescente Rocket -> `ch21_rocket_remnant`
- [x] `coberto` novo duelo tecnico Red vs Blue -> `ch22_red_blue_duel`
- [x] `coberto` gancho Mew -> `ch24_mew_trace`
- [x] `coberto` bloco de treino e paz em Kanto -> `ch25_training_push`, `ch26_kanto_peace`
- [x] `coberto` fechamento de temporada -> `ch27_season1_closure`

## Resumo de cobertura atual
- Cenas/itens auditados: 49
- `coberto`: 49
- `parcial`: 0
- `faltando`: 0

## Criterio de fechamento "100% fidelidade" (operacional)
- [x] Substituir todos os itens `parcial` por `coberto`.
- [x] Preencher `sourceRef` por beat com referencia explicita de arco/capitulos.
- [x] Revisar dialogos beat a beat contra a referencia de adaptacao e fechar diff interno.
