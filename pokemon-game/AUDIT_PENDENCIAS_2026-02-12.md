# AUDIT PENDENCIAS - 2026-02-12

Pedido do usuario revisado ponto a ponto.

## 1) Jogabilidade (movimento do player)
- Status: EM CORRECAO CONTINUA
- Ja feito:
  - limpeza de locks orfaos (`dialog`, `cutsceneLock`, `activeBeatId`, `tapOverlay`)
  - caminho unico de input para evitar eventos duplicados
  - failsafe de auto-avanco em cutscene (2.6s) para evitar travar no meio do dialogo
- Pendente:
  - validacao final no Safari/iPad apos commit atual

## 2) Harmonia visual (pixels/frames/tiles)
- Status: BASE OK
- Ja feito:
  - mapas core com cobertura completa de prebuilt (`21/21`)
  - curadoria de backdrops nao-prebuilt para FRLG-like em `scene_backdrop.manifest.json`
- Pendente:
  - ajuste fino artistico por cena apos playtest (se algum frame destoar)

## 3) Dialogos funcionando sem quebrar
- Status: EM CORRECAO CONTINUA
- Ja feito:
  - removidos handlers inline duplicados
  - guardas de reentrada no `tapAdvance`
  - protecao de `nextDialog()` para estado nulo
  - auto-avanco de cutscene (failsafe)
- Pendente:
  - confirmar no dispositivo do usuario que nao congela na intro

## 4) Colisao/caminhabilidade (nao andar em telhado/parede)
- Status: BASE OK
- Evidencia automatica:
  - `gameplay-preflight` OK (`maps=21`)
  - `story_motion_audit` `issues 0`
- Pendente:
  - validacao visual real em maps com fundo prebuilt (alinhamento perceptivo)

## 5) Uso das referencias prebuilt em /assets
- Status: OK COM RESSALVA
- Ja feito:
  - priorizacao de prebuilt nos mapas core
  - fallback curado para cenas sem prebuilt direto
- Ressalva:
  - nem toda cena do manga tem prebuilt 1:1; nesses casos e usada composicao curada

## 6) Fidelidade ao manga (cenas/dialogos/acontecimentos/evolucoes)
- Status: PARCIALMENTE VALIDADO
- Ja feito:
  - beats roteirizados em `story/season1.ptbr.json` (55 beats)
  - cadeia automatica por progresso de mapa/flags
- Pendente forte:
  - auditoria manual comparando checklist de capitulos x beats (qualitativa)

## 7) Simulacoes de batalha (ataque/level/dano)
- Status: FUNCIONAL, AINDA AJUSTAVEL
- Ja feito:
  - batalhas scriptadas manga-first e confirm-only
- Pendente:
  - balance pass de dano/ritmo para realismo adicional

## Resumo de risco atual
- Maior risco remanescente: comportamento touch/eventos no Safari/iPad na intro.
- Mitigacao aplicada: locks cleanup + input unico + fallback auto-avanco de cutscene.
