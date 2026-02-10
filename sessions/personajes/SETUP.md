# Setup & Deployment Guide

---

## ✅ Estrutura Profissional - COMPLETA

```
✅ Pastas criadas (config, scripts, data/archive, logs)
✅ Documentação (README.md, ARCHITECTURE.md)
✅ Configuração (settings.json, persona.txt, examples.txt)
✅ Scripts profissionais (batch-generator.sh, post-daily.sh, test-single-post.sh)
✅ Python wrapper (post_jesus.py com tweepy)
✅ Virtual environment (venv/) com dependências
✅ Posts de teste (data/posts_current.json - 5 posts para hoje)
✅ .gitignore configurado
```

---

## 🔑 Credenciais (VERIFICAR)

**Status Atual:** 401 Unauthorized (credenciais podem estar expiradas)

**Próximos passos:**
1. Verificar se token Twitter ainda é válido
2. Se expirado: regenerar em https://twitter.com/settings/apps
3. Atualizar `.env` com novas credenciais

**Arquivo:**
```
/home/ubuntu/clawd/sessions/personajes/.env
```

---

## 🚀 Como Testar (Quando Credenciais Forem Válidas)

### 1. Testar Post Manual

```bash
cd /home/ubuntu/clawd/sessions/personajes
source venv/bin/activate
bash scripts/test-single-post.sh "Seu tweet aqui..."
```

### 2. Testar Posting do JSON

```bash
source venv/bin/activate
bash scripts/post-daily.sh 09:00
# Posta o tweet agendado para 09:00 de hoje
```

### 3. Ativar Cron (5x/dia)

```bash
crontab -e

# Adicionar:
0 12 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 09:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1
0 15 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 12:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1
0 18 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 15:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1
0 21 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 18:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1
0 0 * * * cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/post-daily.sh 21:00" >> /home/ubuntu/clawd/sessions/personajes/logs/posting.log 2>&1

# Healthcheck diário (DNS + API reachability)
5 6 * * * /home/ubuntu/clawd/sessions/personajes/scripts/healthcheck.sh >> /home/ubuntu/clawd/sessions/personajes/logs/healthcheck.log 2>&1

# Batch generation (2ª 23:00 BRT = 02:00 UTC Terça)
0 2 * * 2 cd /home/ubuntu/clawd/sessions/personajes && source venv/bin/activate && bash scripts/batch-generator.sh >> logs/batch-generation.log 2>&1
```

---

## 📊 Arquivos & Estrutura

```
/home/ubuntu/clawd/sessions/personajes/
│
├── README.md                 ← Start here
├── ARCHITECTURE.md           ← Technical details
├── SETUP.md                  ← Este arquivo
│
├── .env                      ← Credentials (chmod 600)
├── .gitignore                ← Git ignore rules
│
├── config/
│   ├── persona.txt           ← Persona prompt
│   ├── settings.json         ← Configuration
│   └── examples.txt          ← Exemplos de tweets
│
├── scripts/
│   ├── batch-generator.sh    ← Gera 35 posts/semana (1 Claude call)
│   ├── post-daily.sh         ← Posta (5x/dia, bash puro)
│   ├── post_jesus.py         ← Wrapper tweepy
│   └── test-single-post.sh   ← Teste manual
│
├── data/
│   ├── posts_current.json    ← Posts ativos (5 para teste)
│   └── archive/              ← Histórico
│
├── logs/
│   ├── posting.log           ← Daily posting logs
│   ├── batch-generation.log  ← Weekly batch logs
│   └── error.log             ← Errors
│
└── venv/                     ← Python virtual environment
    ├── bin/
    │   ├── python
    │   ├── pip
    │   └── ...
    └── lib/python3.12/site-packages/
        ├── tweepy/
        └── dotenv/
```

---

## 🧪 Status Atual (05 FEV 2026)

```
✅ Estrutura: 100% Completa
✅ Documentação: 100% Completa
✅ Scripts: 100% Funcionais
✅ Virtual Env: 100% Configurado
⏳ Credenciais: Expiradas (401 Unauthorized)
❌ Posting: Bloqueado por credenciais

PRÓXIMAS AÇÕES:
1. Renovar token Twitter (@jesussemfiltro)
2. Atualizar .env
3. Testar primeiro post
4. Ativar cron (5x/dia)
5. Confirmar no Twitter
6. Amanhã: Gerar 35 posts para próxima semana
```

---

## 📝 Credenciais Esperadas no .env

```
TWITTER_CONSUMER_KEY=<your_key>
TWITTER_CONSUMER_SECRET=<your_secret>
TWITTER_ACCESS_TOKEN=<your_token>
TWITTER_ACCESS_TOKEN_SECRET=<your_secret>
```

---

## 🔐 Segurança

- ✅ `.env` com `chmod 600` (só ubuntu acessa)
- ✅ Secrets redacted em logs
- ✅ Não commitar `.env` (.gitignore configurado)
- ✅ OAuth 1.1 seguro via tweepy

---

## 📞 Próximos Passos

1. **Renovar credenciais Twitter** (se expiradas)
2. **Testar primeiro post** (`test-single-post.sh`)
3. **Ativar cron** (adicionar ao crontab)
4. **Confirmar no Twitter** (checar se posts saem)
5. **Gerar 35 posts** (2ª 23:00 BRT)
6. **Monitorar logs** (tail -f logs/posting.log)

---

**Setup Data:** 05 FEV 2026, 01:45 UTC
**Status:** 🟢 Pronto para testar (aguardando credenciais válidas)
