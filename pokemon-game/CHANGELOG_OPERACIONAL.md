# CHANGELOG OPERACIONAL

## 2026-02-12
- Formalizado playbook operacional para evitar perda de contexto e regressao.
- Definido protocolo fixo de envio Telegram com fallback obrigatorio (`openclaw` -> `send_link.sh`).
- Definidas regras de publicacao e checklist anti-regressao de intro/mapa/colisao.
- Adicionado `tools/intro_preflight.js` para validar fluxo inicial (Intro -> Oak -> Viridian).
- `ci-check.sh` passou a exigir `intro-preflight` antes de liberar publish.

## Como manter
- Cada ciclo relevante (bugfix, ajuste visual, mudanca de fluxo) deve adicionar uma linha aqui.
- Entradas devem ser factuais: o que mudou, por que mudou, como validar.
