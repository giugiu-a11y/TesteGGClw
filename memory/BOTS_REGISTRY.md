# Bots Registry (Master + Auxiliares)

## Princípio
- **Master**: Akira Master (não alterar).
- **Bots auxiliares**: específicos por função (personagens, assistente, atendimento).
- **Nunca** enviar mensagens de bots auxiliares para canais errados.

## Onde ficam as configs (caminhos)

### 1) OpenClaw (core)
- Config principal: `/home/ubuntu/.openclaw/openclaw.json`
- Allowlist Telegram: `/home/ubuntu/.openclaw/credentials/telegram-allowFrom.json`
- Pairing Telegram: `/home/ubuntu/.openclaw/credentials/telegram-pairing.json`

### 2) Assistente Clawd Opus (bot auxiliar)
- Sessão isolada (definição): `/home/ubuntu/clawd/sessions/assistente-opus/config.json`
- Tokens/ID do assistente: `/home/ubuntu/clawd/sessions/assistente-opus/.env.assistente`
  - `TELEGRAM_BOT_TOKEN=...`
  - `ALLOWED_USER_ID=...`

### 3) Personagens IA
- Sessão isolada: `/home/ubuntu/clawd/sessions/personajes/`
- Prompt oficial (Jesus Sincero):
  - `/home/ubuntu/clawd/memory/jesus-sincero-prompt.md`
  - `/home/ubuntu/clawd/sessions/personajes/jesus_prompt.txt`

### 4) M6 Atendimento
- Sessão isolada: `/home/ubuntu/clawd/sessions/m60-atendimento/`

## Observações críticas
- **Não mudar** o Master (Akira) nem o allowlist sem confirmar chat_id correto.
- Tokens **não** devem ser copiados para docs nem expostos em logs.
- Se o bot auxiliar não enviar, verifique:
  1) `ALLOWED_USER_ID` correto
  2) rede/liberação para `api.telegram.org`
  3) gateway/openclaw ativo

## Próximo passo seguro
- Confirmar o `ALLOWED_USER_ID` correto do Assistente.
- Depois, testar envio direto somente para esse chat.

## Auditoria (2026-02-04)
- Job Curator (vagas remotas): falha em `/etc/llm.env` com PermissionError ao postar.
  - Corrigido: `projects/job-curator-bot/post_next.py` agora ignora PermissionError.
- Assistente Opus: múltiplos supervisores rodando; normalizado para 1.
- Bots M60 Atendimento e Personajes: leitura de `/etc/llm.env` agora com fallback seguro.

### Processos em execução (esperado)
- Assistente Opus: `sessions/assistente-opus/run.sh`
- Job Curator Bot: `projects/job-curator-bot/app.py`

## 🔒 Routing lock (2026-02-04)
- `memory/ROUTING_MAP.md` documenta destinos permitidos.
- `projects/job-curator-bot/post_next.py` bloqueia alerta para grupos.
- `scripts/briefings/send_telegram_assistente.py` usa somente token/chat do Assistente.
