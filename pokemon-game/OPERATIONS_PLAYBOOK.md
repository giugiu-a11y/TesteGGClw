# OPERATIONS PLAYBOOK

Objetivo: evitar regressao de qualidade (visual/gameplay) e falhas operacionais repetidas.

## 1) Regras Fixas de Qualidade
- Nunca trocar estilo visual para algo inferior ao padrao FRLG-like.
- `prebuilt` e a referencia primaria de aparencia.
- Solucao tecnica que degrade visual NAO entra em `main`.
- Nao publicar sem passar `bash ci-check.sh`.

## 2) Regras Fixas de Gameplay
- Player/NPC nunca podem caminhar em tile solido (parede, arvore, agua, mobiliario).
- Entrada de interiores deve ocorrer por porta (nao telhado/lateral).
- Apenas 1 cena ativa por vez (sem sobreposicao de render loop/camadas).
- Transicao de mapa deve recarregar colisao e limpar estado transiente.

## 3) Protocolo de Publicacao
1. Rodar checks:
   - `bash ci-check.sh`
2. Commit com mensagem objetiva.
3. Push:
   - `git push origin main`
4. Link com cache-buster:
   - `?v=<commit>`
5. Atualizar `STATUS.md` e `NEXT.md` no mesmo ciclo.

## 4) Protocolo de Envio no Telegram (ordem obrigatoria)
1. Tentar `openclaw message send`.
2. Se falhar por rede, usar fallback padrao:
   - `./send_link.sh`
3. So considerar enviado quando retorno for:
   - `SENT`

## 5) Checklist Anti-Regressao (antes de dizer "pronto")
- Intro: sem sprite em telhado/parede.
- Oak aparece no fluxo inicial.
- Player move nas 4 direcoes apos dialogo.
- Sem layer-over-layer na abertura.
- Warps de Pallet/Viridian/Pewter funcionando.

## 6) Politica de Mudancas Sensiveis
- Qualquer alteracao em `index.html` que mexa em render/cutscene/collision exige:
  - `ci-check.sh` + `gameplay_preflight.js` + validacao de intro.
- Se houver conflito entre "estavel" e "bonito", resolver ambos antes do release.
