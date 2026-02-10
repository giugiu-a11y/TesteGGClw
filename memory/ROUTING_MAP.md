# Routing Map (no values)

## Regras inegociáveis
- Cada projeto/bot usa **seu próprio token** e **seu próprio chat_id**.
- Nunca reutilizar token de um bot para enviar mensagens de outro projeto.
- Nunca enviar alertas para grupos/canais (-100...).

## Destinos permitidos
- Akira Master (alerts): `TELEGRAM_ALERT_CHAT_ID`
- Assistente Opus (briefings): `.env.assistente -> ALLOWED_USER_ID`
- Vagas Remotas: `.env -> TELEGRAM_GROUP_ID`

## Enforcements
- `post_next.py` bloqueia alertas para grupos.
- `send_telegram_assistente.py` lê token/chat do Assistente (não aceita override).
