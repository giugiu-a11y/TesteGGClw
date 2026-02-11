# NEXT (Pokemon Adventures)

## Definicao de "Final"
1. Manga-first: eventos, capturas e evolucoes acontecem quando o mangá dita.
2. Feel de Pokemon classico (Yellow/FRLG), mas sem grind infinito.
3. Link estavel para iPad (preferir GitHub Pages; tunnel so para testes).
4. Jogador so confirma (A/OK). Ataques/itens acontecem automaticamente conforme o mangá.

## Done
- Sprint 1: cenas + warps + save/load (ver `STATUS.md`).
- Batalha basica + UI e sprites (atual em `index.html`).
- Batalha scripted/confirm-only (A/OK) em `storyLock` (sem BAG manual).

## Doing (agora)
- Deploy GitHub Pages (tirar dependencia de tunnel).
- StoryScript (temporada 1): estrutura + flags + cenas com dialogos fieis.

## Next
- Map rendering com tileset FRLG (Pallet/Route1/Viridian/Pewter).
- Scripted encounters/battles/captures (temporada 1) sem RNG.
- Revisar/reescrever dialogos para >= 75% fidelidade do mangá.
- Quebrar conteudo por beats em `clawd/pokemon-game/SEASON1_CHECKLIST.md`.

## Como testar
- Dev: `cd /home/ubuntu/clawd/pokemon-game && ./start-dev.sh`
- iPad: abrir o link do GitHub Pages (quando publicado).

## Coordenação (multi-IA)
- Ler `clawd/pokemon-game/COORDINATION.md` antes de mudar coisas grandes.
- Atualizar este arquivo (`NEXT.md`) na mesma mudanca.
