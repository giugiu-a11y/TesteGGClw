# Coordination Rules (Pokemon Game)

Objetivo: evitar retrabalho/regressoes quando 2 IAs (ou mais) mexem no mesmo projeto.

## Fonte Unica de Verdade
- `clawd/pokemon-game/NEXT.md` e o estado do projeto.
- Qualquer mudanca relevante exige atualizar `NEXT.md` no mesmo PR/commit.

## Nao Quebrar o Funil
- O "funil" e: abrir um link estavel no iPad e jogar.
- Prioridade: GitHub Pages.
- Tunnel (localtunnel) so para debug rapido e pode quebrar; nao otimizar o projeto em torno dele.

## Regras de Mudanca
- Nao reescrever `index.html` inteiro: mudar em blocos pequenos e testaveis.
- Nao reintroduzir RNG/grind quando `GAME_MODE.storyLock=true`.
- Nao adicionar passos manuais para o usuario (iPad). Se for inevitavel, deixar 1 passo maximo e mandar por Telegram.

## Definition of Done (por feature)
- Visual: ainda parece FRLG (UI/cores) e nao "demo".
- Narrativa: cenas/dialogos >= 75% fieis ao mangá (sem perder sentido).
- Jogabilidade: jogador so confirma (A/OK) quando a historia mandar.
- Persistencia: save/load nao quebra a progressao do story.

## Higiene
- Nao misturar commits de `sessions/**` com `pokemon-game/**`.
- Se um agente mexer em scripts de deploy/tunnel, registrar em `NEXT.md` o motivo e o comando de teste.

