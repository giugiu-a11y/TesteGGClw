# Job Curator Bot

Bot que coleta vagas remotas, analisa com Claude AI, e posta no Telegram.

## 🎯 Regra de Ouro

**NUNCA posta link de agregador.** Só links diretos (Greenhouse, Lever, careers page).

## Arquitetura

```
job_sources.py     → Coleta vagas (RemoteOK, WWR, Himalayas)
link_resolver.py   → Resolve agregador → link direto
job_analyzer.py    → Analisa com Claude (requisitos, salário, etc)
telegram_poster.py → Formata e posta no Telegram
main.py            → Pipeline orquestrador
```

## Formato das Vagas

```
🎯 [TÍTULO]

[EMPRESA]
📍 [PAÍS/REMOTO]
💰 USD $[SALÁRIO]/mês

✓ [Descrição em 1 linha]

Requisitos:
• Inglês: [Sim/Não/Fluente]
• Faculdade: [Sim/Não/Não importa]
• Experiência: [Sim/Não/Qualquer um]

APLICAR: [LINK DIRETO]
```

## Uso

```bash
# Dry run (simula sem postar)
python main.py --dry-run --limit 5 --max-posts 3

# Com Telegram
export TELEGRAM_BOT_TOKEN="seu_token"
export TELEGRAM_CHAT_ID="@seu_canal"
python main.py --max-posts 5
```

## Linguagem Simples

- Sem jargões: "Junior/Pleno/Senior" ❌
- Use: "Com experiência", "Sem experiência", "2+ anos" ✅

## Agregadores Bloqueados

- weworkremotely.com
- remoteok.com
- indeed.com
- linkedin.com
- glassdoor.com
- etc.

Se a fonte é agregador, o bot tenta extrair o link direto (apply URL).
Se não conseguir = vaga descartada.
