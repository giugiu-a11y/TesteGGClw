# Pokemon Adventures (Manga-First) - Checklist Final

Baseado no que voce pediu no Telegram:
- Capturas, batalhas, evolucoes e progresso seguem o mangá (nao RNG).
- O jogador sente que esta jogando, mas a sequencia e controlada pela historia.
- Look and feel tipo Pokemon (Yellow/FRLG), adaptado e colorido.

## 0) Fonte Unica de Verdade
- [ ] Criar `pokemon-game/NEXT.md` com: Done/Doing/Next + como testar + definicao de "final".
- [ ] Regra: toda IA que mexer aqui atualiza `NEXT.md` antes de encerrar.

## 1) Estabilidade de Acesso (iPad)
- [ ] Deploy estavel (preferencial): GitHub Pages.
- [ ] Fallback (temporario): tunnel (localtunnel e instavel, usar so para teste rapido).

## 2) Motor de Historia (sem RNG)
- [ ] `storyLock=true` por default.
- [ ] Encontros selvagens so acontecem quando a historia manda (ex: Mew, Bulbasaur, Pikachu).
- [ ] Captura so acontece nos momentos do mangá (sem farm de pokeball).
- [ ] Evolucoes so acontecem nos marcos do mangá.
- [ ] "Level" pode existir como cosmetico/ficticio (para feedback), mas nao deve mudar a historia.

## 3) Batalha (minimalista, manga-driven)
- [ ] Batalhas scripted: o jogador so confirma (A/OK). Ataques/itens sao automaticos conforme o mangá.
- [ ] Sem BAG manual: itens (ex: Potion, Pokeball) aparecem/acontecem apenas quando a historia mandar.
- [ ] Sem grind: sem random encounters, sem farm de captura, sem XP/level-up automatico em `storyLock`.
- [ ] Resultado altera flags de historia e segue para proxima cena.
- [ ] Remover/ocultar aleatoriedade (escape chance, encounter rate) quando `storyLock=true`.

## 4) Mapas e Tiles (FRLG-style)
- [ ] Trocar render "tiles canvas" por tileset real (FRLG).
- [ ] Pipeline: baixar tiles PNG (nao commitar no git se for copyright) + gerar tilemap.
- [ ] Pallet / Route 1 / Viridian / Pewter com tiles e colisao.

## 5) Conteudo (Capitulos do Volume 1)
- [ ] Intro completa (Mew + Oak lab) com texto >= 75% fiel.
- [ ] Capitulo Bulbasaur (scripted encounter + captura).
- [ ] Capitulo Rocket/Forest (evento, batalha, dialogos).
- [ ] Capitulo Pikachu (scripted).
- [ ] Blue battle quando acontecer no mangá (nao antes).

## 6) Persistencia e QA
- [ ] Save/Load robusto (versionamento do save).
- [ ] Botao "Reset Save" (debug).
- [ ] Suite minima de testes manuais (roteiro 10 minutos).

## 7) Higiene do Repo
- [ ] `.gitignore` para nao versionar caches, `__pycache__`, downloads de assets.
- [ ] Evitar commits que misturam `sessions/` e `pokemon-game/`.
