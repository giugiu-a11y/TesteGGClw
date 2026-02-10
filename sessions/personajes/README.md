# Jesus Sincero - Twitter Automation Bot

**Uma persona reflexiva, existencial e provocadora postando automaticamente no Twitter.**

---

## 🚨 AVISO CRÍTICO PARA OUTROS LLMs

### O Bug do `source .env`

Se você está tendo erro **401 Unauthorized**, provavelmente é porque `source .env` **NÃO EXPORTA** variáveis para subprocessos Python!

```bash
# ❌ ERRADO - Python não vê as variáveis
source .env
python3 scripts/post_jesus.py "texto"

# ✅ CORRETO - Python consegue ver as variáveis
set -a          # Ativa auto-export
source .env     # Carrega E exporta
set +a          # Desativa auto-export
python3 scripts/post_jesus.py "texto"
```

**Leia o TROUBLESHOOTING.md para mais detalhes!**

---

## 🎯 Visão Geral

- **Conta:** @jesussemfiltro
- **Frequência:** 5 posts/dia (09:00, 12:00, 15:00, 18:00, 21:00 BRT)
- **Geração:** Batch semanal (1 call Claude = 35 posts)
- **Posting:** Automático via cron (bash + requests_oauthlib, zero IA)
- **Economia:** 88% menos tokens vs posting individual

---

## 📂 Estrutura

```
personajes/
├── README.md              # Este arquivo
├── ARCHITECTURE.md        # Detalhes técnicos
├── TROUBLESHOOTING.md     # Solução de problemas (LEIA!)
├── SETUP.md               # Guia de setup
├── .env                   # Credentials (chmod 600, NÃO COMMITAR)
├── .gitignore             # Ignorar .env, logs, cache
│
├── config/
│   ├── persona.txt        # Prompt da persona
│   ├── settings.json      # Configuração
│   └── examples.txt       # Exemplos de tweets
│
├── scripts/
│   ├── batch-generator.sh # Gera 35 posts (1x/semana)
│   ├── post-daily.sh      # Posta (5x/dia) - USA `set -a`!
│   ├── post_jesus.py      # Wrapper OAuth 1.0a
│   └── test-single-post.sh# Teste manual - USA `set -a`!
│
├── data/
│   ├── posts_current.json # Posts semana atual
│   └── archive/           # Histórico
│
├── logs/
│   ├── posting.log        # Logs de posts
│   ├── batch-generation.log
│   └── error.log          # Erros
│
└── venv/                  # Python virtual environment
```

---

## 🚀 Quick Start

### 1. Ativar ambiente

```bash
cd /home/ubuntu/clawd/sessions/personajes
source venv/bin/activate
```

### 2. Testar post manual

```bash
# IMPORTANTE: Use set -a para exportar variáveis!
set -a && source .env && set +a
python3 scripts/post_jesus.py "Seu tweet aqui..."
```

### 3. Verificar cron jobs

```bash
crontab -l | grep personajes
```

---

## 🔐 Credenciais

### OAuth 1.0a (USAR ESTE!)
```
TWITTER_CONSUMER_KEY=...
TWITTER_CONSUMER_SECRET=...
TWITTER_ACCESS_TOKEN=...
TWITTER_ACCESS_TOKEN_SECRET=...
```

### OAuth 2.0 (NÃO USAR PARA POSTING!)
OAuth 2.0 Bearer tokens são "App-Only" e retornam 403 Forbidden para posting.

---

## ⏰ Cron Jobs

```bash
# Posting 5x/dia (BRT = UTC-3)
0 12 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 09:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1
0 15 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 12:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1
0 18 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 15:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1
0 21 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 18:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1
0 0 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 21:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1

# Healthcheck diário (DNS + reachability; sem LLM)
5 6 * * * /home/ubuntu/clawd/sessions/personajes/scripts/healthcheck.sh >> /home/ubuntu/clawd/sessions/personajes/logs/healthcheck.log 2>&1

# Batch generation (2ª 23:00 BRT = 02:00 UTC Terça)
0 2 * * 2 cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/batch-generator.sh" >> /home/ubuntu/clawd/sessions/personajes/logs/batch-generation.log 2>&1
```

---

## 🐛 Problemas Comuns

| Erro | Causa | Solução |
|------|-------|---------|
| 401 Unauthorized | Variáveis não exportadas | Use `set -a && source .env && set +a` |
| 403 Forbidden | Usando OAuth 2.0 Bearer | Use OAuth 1.0a credentials |
| No module found | venv não ativado | `source venv/bin/activate` |
| No post for date | JSON desatualizado | `bash scripts/batch-generator.sh` |
| DNS falhando | Resolver instável | `resolvectl query api.twitter.com` + healthcheck |

**Para mais detalhes, veja TROUBLESHOOTING.md!**

---

## 📊 Economia de Tokens

| Cenário | Tokens/Semana | Economia |
|---------|---------------|----------|
| ❌ Sem batch (35 calls/dia) | 157.500 | - |
| ✅ Com batch (1 call/semana) | 4.000 | **97% menos** |

---

## 📝 Persona: Jesus Sincero

**Tom:** Reflexivo, existencial, provocador
**Linguagem:** Simples, direta, acessível
**Perspectiva:** Terceira pessoa (NUNCA "eu")
**Temas:** Mudança pessoal, autenticidade, relacionamentos, paradoxos
**Comprimento:** 280 chars max

**Exemplo:**
> "Metade das orações são pra mudar os outros. Outra metade, pra Deus não mudar nada dentro de si. Jesus sorri dessa contradição humana."

---

## 📞 Contato

**Responsável:** Matheus (@matheustomoto)
**Bot:** @jesussemfiltro
**Pasta:** `/home/ubuntu/clawd/sessions/personajes/`

---

**Última atualização:** 2026-02-05
**Status:** 🟢 Operacional
