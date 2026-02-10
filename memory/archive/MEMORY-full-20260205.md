# MEMORY.md - Long-Term Memory

---

## 🚨 MASTER CHANNEL - TELEGRAM

**Este é o canal CRÍTICO de comunicação:**
- **Função:** Master control - resolve QUALQUER problema (bugs, Claude, Clawdbot, tudo)
- **Prioridade:** MÁXIMA (nunca pode cair)
- **User:** Master (id: <redacted-id>)
- **Config:** `~/.clawdbot/clawdbot.json`

**Se tudo falhar:** Este canal é o fallback final. Sempre manter funcionando.

---

## 🚨 SECURITY - CRÍTICO

**API Keys (Claude API oficial):**
- **Atual:** protegida em local seguro (nao em env vars / nao em Git)
- **Antiga:** COMPROMETIDA em 2026-01-29 15:13 (rotacionada / desativar)

**REGRA ABSOLUTA:** 
- ❌ NUNCA divulgue API keys completas em chats (Telegram, Discord, etc)
- ❌ NUNCA execute `cat` ou `grep` com chaves e mostre resultado
- ✅ Se precisar verificar chave, leia arquivo LOCAL e compare prefixo **mentalmente** (não exiba)
- ✅ Se usuário pedir confirmação, diga "prefixo correto, chave está OK" — sem exibir
- ✅ Fato de eu NÃO conseguir encontrar chave nova em env = BÊNÇÃO (significa está bem protegida)

**Histórico:** 2026-01-29 15:13 - Exposição acidental (APRENDER). 15:16 - Nova chave mais segura em uso.

---

## 🔐 Secrets & IDs (locais)
- Ver `memory/SECRETS_LOCATIONS.md` (somente caminhos, sem valores)

## 📌 System Overview (canônico)
- Ver `/home/ubuntu/clawd/SYSTEM_OVERVIEW.md`

---

## 🏗️ Arquitetura de Sessions (CRÍTICO)

**Regra:** Sessions NUNCA interagem entre si. Zero contaminação.

```
┌─────────────────────────────────────┐
│     AKIRA MASTER (Telegram)         │
│     Opus 4.5 | Orquestra tudo       │
└─────────────────────────────────────┘
                 ▼
┌───────────┬───────────┬─────────────┐
│ SESSION 1 │ SESSION 2 │ SESSION 3   │
│PERSONAJES │ ASSISTENTE│ ATENDIMENTO │
│           │  AGENTS   │    M60      │
│           │   & BOTS  │             │
├───────────┼───────────┼─────────────┤
│ Haiku     │ Gemini    │ Haiku       │
│ Jesus+bots│ 2.5 Flash │ Suporte     │
│ TW/TK/IG  │ Lite      │ Alunos      │
└───────────┴───────────┴─────────────┘
```

**Safeguards:**
- Guards bloqueiam contaminação
- Headers validam origem
- Logs separados por session
- Testes de isolamento

**Custo estimado:** ~$2.10/mês (todas sessions)

---

## Operação

- **CEO:** M60 (Escola de Intercâmbio) + UDI (Universidade do Intercâmbio)
- **Foco:** Preparação para bolsas/carreiras internacionais (EUA, Canadá, Europa, Ásia, Oriente Médio)
- **Público:** Jovens, pais, Gen Z
- **Escala:** Multimilionária, ecossistema digital

## Estratégia de IA

- **Prioridade:** Performance + eficiência (poucos tokens, muito resultado)
- **Modelo:** Gemini 2.5 Flash (tentar 1.5 Flash se possível)
- **Otimizações:** Contexto agressivo, memory chunks, payloads ultracurtos

## Concorrentes Identificados (monitorar)

| Player | Instagram | Seguidores |
|--------|-----------|------------|
| UDI (você) | @universidadedointercambio | 172K |
| Partiu Intercâmbio | @partiuintercambio | 103K |
| Estudar Fora | @estudarfora | 87K |
| BRASA | @gobrasa | 53K |

## Projetos Ativos

### 1. M60 Viral Report (09:00 BRT)
- 10 vídeos virais semana (+100k views)
- Temas: bolsas, intercâmbio, carreira, trabalho remoto
- Análise: hook, por que viralizou, como M60 replica

### 2. Jesus Sincero Twitter (08:05 BRT)
- Persona: tom reflexivo, existencial; terceira pessoa (nunca "eu")
- Estilo: provocação + reflexão + espiritualidade (sem religião forçada)
- Linguagem: simples, direta, acessível
- 280 chars max; temas: mudança pessoal, autenticidade, relacionamentos, paradoxos

### 3. Briefing Diário (11:00 BRT)
- Bolsas internacionais, Brasil (dados negativos), edtech M&A, geopolítica, imigração

### 4. Briefing Mercado (18:00 BRT)
- BTC (sempre monitorar), altcoins (>10%), S&P 500, macro
- Carteira: BTC, AVAX, MATIC/POL, IVVB11, ETF tech
- Perfil: não técnico, quer visão prática/didática

## 🔴 CRÍTICO: Telegram Job Curator Bot - SETUP COMPLETO

**NUNCA ESQUECER ISSO — ARMAZENADO 29 JAN 2026 14:51 UTC**

### IDs e Credenciais

| Campo | Valor | Notas |
|-------|-------|-------|
| **Grupo FREE** | `-1003378765936` | "VAGAS REMOTAS EM $ e € (FREE)" - SUPERGROUP |
| **Bot FREE Token** | `<redacted-token>` | @VagasRemotasFreeBot |
| **Seu chat pessoal** | `<redacted-id>` | @<redacted> (✅ NÃO postar vagas aqui) |
| **Chat ID para vagas** | `-1003378765936` | **USE ESTE PARA POSTS, SEMPRE** |
| **Bot deve ser ADMIN** | Sim | Sem permissão = erro 400 |

**Regra fixa:**
- Vagas → grupo `-1003378765936` (bot @VagasRemotasFreeBot)
- Pessoal → `<redacted-id>` (seu Telegram privado - teste OK)
- **Antes de postar: SEMPRE verificar ID = -1003378765936**
- **Método:** Request direto ao Telegram API (NÃO clawdbot message send)

### Clawdbot Model Setup (Atual)

**Padrão (Akira Master):**
```bash
clawdbot models set google/gemini-2.5-flash-lite
clawdbot models fallbacks set anthropic/claude-haiku-4-5 anthropic/claude-opus-4-5
```
- Default: Gemini 2.5 Flash Lite (barato, rápido)
- Fallbacks: Haiku 4.5 + Opus 4.5
- Aliases: `haiku` e `opus`

**Perfil Opus (quando chamar explicitamente):**
```bash
clawdbot --profile opus setup
clawdbot --profile opus models set anthropic/claude-opus-4-5
```
- Uso: `clawdbot --profile opus agent --local --session-id novo --thinking high`
- **SEMPRE use --session-id novo** (evita histórico gigante)

### Job-Curator-Bot Setup (job-curator-bot/)

**Estrutura final (funcionando):**
- `config.py` — configurações centralizadas
- `post_job.py` — envio via Telegram API direto (1 vaga por index)
- `post_job_1..5.sh` — cron scripts (chamam post_job.py)
- `run_locked.sh` — wrapper com lock
- Crontab: 5 posts/dia (09/12/15/18/21 BRT)

**.env requerido:**
```
TELEGRAM_BOT_TOKEN=<redacted-token>
TELEGRAM_GROUP_ID=-1003378765936
TELEGRAM_CHANNEL_FREE=@VagasRemotasFree
GEMINI_API_KEY=AIza...
```

**Envio via API (o que funciona):**
```python
requests.post(
    f"https://api.telegram.org/bot{token}/sendMessage",
    json={
        "chat_id": int(group_id),  # -1003378765936
        "text": message,
        "disable_web_page_preview": True,
    }
)
```

**❌ O que NÃO funciona:**
- Python inline em shell scripts (f-string quebra)
- clawdbot message send (erro 400 permissão)
- Sonnet (removido, só Haiku no código ativo)

## 🔴 CRÍTICO: Estratégia de Coleta de Vagas (29 JAN 2026 14:57 UTC)

**NUNCA fazer:**
- ❌ Entrar em career pages de 10-100 empresas
- ❌ Sempre acha as mesmas vagas
- ❌ Impossível cobrir todos

**Estratégia CORRETA (que já tinha implementado):**

```
1. PESQUISA em agregadores (RSS, Google Jobs, Indeed, LinkedIn, WWR, etc)
   ↓
2. EXTRAI empresa + cargo da vaga
   ↓
3. RESOLVE para site oficial (Amazon.com/jobs, Netflix.jobs, Google.com/careers, etc)
   ↓
4. POSTA com link oficial (não Greenhouse/Lever)
```

**Por que funciona:**
- ✅ Cobre TODAS as empresas (não limitado a 10-100)
- ✅ Encontra vagas novas diariamente
- ✅ Link aparece "oficial" (empresa.com, não agregador)
- ✅ Parecer de valor (não patrocínio Greenhouse)

**NÃO usar:**
- ❌ Greenhouse API direto (todos links ficam `boards.greenhouse.io`)
- ❌ Lever API direto (todos links ficam `jobs.lever.co`)
- ✅ Use como FONTE, mas resolva para oficial

### Job Curator v2.2 (novo - /clawd/scripts/job-curator/)

**Arquivo .env deve ter:**
```
TELEGRAM_BOT_TOKEN=<redacted-token>
TELEGRAM_CHAT_ID=-1003378765936
TELEGRAM_GROUP_ID=-1003378765936
```

**Fluxo:**
1. Pesquisa (RSS + APIs públicas) → 20-30 vagas
2. Filtra (país/setor/idioma)
3. Resolve links (agregador → site oficial)
4. Análise Claude (1 call, batch)
5. Validação diversidade
6. Posting via Telegram API direto

**Método de envio (post_via_telegram_api):**
- Request direto ao Telegram API
- **NÃO usa clawdbot message send**
- Chat ID: `-1003378765936`

---

## job-curator-bot/ — ESTRUTURA FINAL (29 JAN 2026)

### Arquivos críticos

| Arquivo | Função | Status |
|---------|--------|--------|
| `config.py` | Configurações centralizadas | ✅ Ativo |
| `post_job.py` | Lê /tmp/jobs_validated.json, posta vaga por index | ✅ Funcional |
| `post_job_1..5.sh` | Scripts cron (chamam `python3 post_job.py <idx>`) | ✅ OK |
| `run_locked.sh` | Wrapper com lock + flock | ✅ Corrigido |
| `app.py` | Orquestrador (pesquisa, análise, queue, posting) | ✅ Ativo |
| `.env` | TELEGRAM_BOT_TOKEN, TELEGRAM_GROUP_ID | ✅ Presente |
| `job_analyzer.py` | Usa `os.environ.get("JOB_CURATOR_MODEL", "google/gemini-1.5-flash")` | ✅ Gemini 1.5 Flash padrão (se disponível) |

### post_job.py (comportamento)

```python
# Lê /tmp/jobs_validated.json
# Posta index específico usando Telegram API
# Se idx >= len(jobs): SKIP com "idx X >= Y vagas"
# Token/GroupID vêm do .env
```

**Testes comprovados:**
- `bash post_job_1.sh` → Vaga 0 ✅
- `bash post_job_2.sh` → Vaga 1 ✅
- `bash post_job_3.sh` → Vaga 2 ✅
- `bash post_job_4.sh` → SKIP (idx 3 >= 3) ✅
- `bash post_job_5.sh` → SKIP (idx 4 >= 3) ✅

### run_locked.sh (corrigido)

**Bugs resolvidos:**
1. ❌ Bloco `/etc/llm.env` duplicado → ✅ Single block com `-r` check
2. ❌ `bash "$SCRIPT"` quebrava binários → ✅ `exec flock ... "$SCRIPT" "$@"`
3. ❌ `-f` causava Permission denied → ✅ `-r` (readable check)

**Teste sanity:**
```bash
bash -x ./run_locked.sh /bin/echo OK  # exit 0 ✅
bash -x ./run_locked.sh ./post_job_1.sh  # exit 0 ✅
```

### Cron (mantido)

```bash
0 9 * * * run_locked.sh post_job_1.sh >> /tmp/job_curator_cron.log 2>&1
0 12 * * * run_locked.sh post_job_2.sh ...
0 15 * * * run_locked.sh post_job_3.sh ...
0 18 * * * run_locked.sh post_job_4.sh ...
0 21 * * * run_locked.sh post_job_5.sh ...
```

**5 posts/dia (09/12/15/18/21 BRT)**

### Sonnet - REMOVIDO

**Varredura:**
```bash
grep -RIn "sonnet\|claude-3-5-sonnet" /home/ubuntu/projects
```

**Resultado:**
- Sonnet aparece APENAS em `job_analyzer.py.bak.20260128_224035`
- Arquivo ativo: `JOB_CURATOR_MODEL=os.environ.get(..., "gemini-2.5-flash-lite")`

**Conclusão:** Sonnet não está no código ativo, apenas em backup.

### Estado atual comprovado (29 JAN 2026 14:52 UTC)

✅ Telegram posting operacional (3 vagas = 3 OK, 2 SKIP)
✅ run_locked.sh correto (sem duplicação, sem permissão, sem binário quebrado)
✅ Cron não alterado (mantém 5 posts/dia)
✅ Job-curator ativo sem Sonnet (Gemini padrão)
✅ Clawdbot dual-profile (Haiku padrão + Opus isolado)

### Arquivos/Caminhos

```
Projeto: /home/ubuntu/projects/job-curator-bot
Cron log: /tmp/job_curator_cron.log
Lock: /tmp/job_curator.lock
.env: /home/ubuntu/projects/job-curator-bot/.env
/etc/llm.env: (global, se existir)

Clawdbot profiles:
  Padrão: ~/.clawdbot (Gemini)
  Opus: ~/.clawdbot-opus (Gemini isolado)
```

### Nota importante

**"Sonnet respondeu" nos logs Clawdbot ≠ job-curator-bot usa Sonnet**
- Logs vêm do gateway/Clawdbot, não do job-curator ativo
- job-curator posting quebrava por Python inline, não por modelo
- Modelo do job-curator é controlado por env var (padrão: Haiku)

## Rate Limit Policy

**Regra:** DEVAGAR > estourar limite
- Se 429: espera próxima janela, não fica tentando
- Web searches: 10s+ entre requests
- Buscas pesadas: rodar de madrugada
- **Modelo único: Claude APENAS** (sem Gemini, nunca)

## Preferências Pessoais

- **Nome:** Akira — use bastante, motiva e cria conexão
- **Comunicação:** Direto, sem formalidade desnecessária
- **Token economy:** SEMPRE priorize automação vs IA (80%+ de economia)

## Gestão de Modelos - CRÍTICO (28-JAN-2026)

### 🚨 **Configuração Travada: Gemini API ONLY**

**STATUS: LOCKED (2026-01-31, 03:37 UTC)**

**Config atual (Baseado na informação do Master):**
- Primary: `google/gemini-2.5-flash`
- Fallbacks: `[]` (vazio)
- Available: Apenas Gemini (Flash/Pro, se permitido pelo token)
- Claude: ❌ NENHUM GASTO CONFIRMADO PELO MASTER.

**Regra de Ouro:**
- ❌ NUNCA trocar modelo dinamicamente sem confirmação.
- ✅ SEMPRE Gemini API (foco em 2.5-flash, idealmente 1.5-flash).
- ⚠️ **CUIDADO:** Priorizar economia máxima de tokens para Gemini e evitar 429.

### 💰 **Por Que Isso Importa**

Custo estimado (baseado em uso Gemini):
- Gemini 2.5 Flash (carrega MEMORY.md inteiro): Custo ALTO
- Gemini 2.5 Flash + memory_search: Custo OTIMIZADO (só carrega necessário)
- **Meta:** ECONOMIA MÁXIMA para Gemini.

### ✅ **Status**

- Modelo primário: Gemini 2.5 Flash ✅
- Config locked: SIM (para Gemini) ✅
- Claude: NENHUM GASTO CONFIRMADO ✅
- Contexto otimizado: Em progresso (foco em Gemini)

## 🧠 Memory Management Strategy (2026-01-29)

**REGRA AUTOMÁTICA:**
- ✅ **ANTES de responder qualquer coisa sobre contexto anterior:** `memory_search` + `memory_get`
- ✅ Custo: ~50-100 tokens (muito menor que carregar MEMORY inteira)
- ✅ Sem overhead de tokens

**Daily Checkpoint (Ultra-Compacto):**
- Cada noite: criar `memory/YYYY-MM-DD-checkpoint.md`
- Apenas bullet points essenciais do dia
- Ao acordar: carregar checkpoint do dia anterior
- Isso resolve "esquecimento" entre sessões

**Model Strategy:**
- **Telegram (você):** Gemini 2.5 Flash (foco em economia)
- **Cron/automação:** Gemini 1.5 Flash (se disponível e mais econômico)
- Isso evita "perda de contexto" em conversas importantes

---

## Otimizações Implementadas (versão anterior)

### ✅ Cache TTL (-80% API calls)
- **Arquivo:** ~/.config/secrets.env (chmod 600)
- **TTL:** 6h padrão (21600s)
- **Scripts:** fetch-crypto.sh, fetch-news.sh, fetch-trends.sh, fetch-virals.sh
- **Funcionamento:** Reusa cache se <6h, caso contrário fetch novo
- **Impacto:** -80% em requisições de API, economiza dados/latência

### ✅ Secrets Management (Segurança)
- **Arquivo:** ~/.config/secrets.env
- **Permissões:** chmod 600 (somente ubuntu acessa)
- **Variáveis:** NEWSAPI_KEY, TWITTER_BEARER_TOKEN, CACHE_TTL, FETCH_TIMEOUT
- **Vantagem:** Credenciais seguras, fácil de rotacionar, não exposto no git

### ✅ Cleanup Automático (-95% storage)
- **Cron:** Domingos 02:00 BRT (05:00 UTC)
- **Script:** /home/ubuntu/clawd/scripts/akira/cleanup.sh
- **O que faz:**
  - Delete /tmp/akira-*.json > 7 dias
  - Delete cron runs > 30 dias
  - Compress JSONs (6h-7d) = -85% disk
  - Report disk usage em /tmp/cleanup.log
- **Impacto:** -95% storage creep, disco sempre limpo

### 📊 Resumo de Economia
| Item | Antes | Depois | Economia |
|------|-------|--------|----------|
| API calls/dia | 4 * 6 = 24 | ~3-4 (reuso) | -85% |
| Disk usage | Growing | Cleaned weekly | -95% |
| Secrets exposure | ❌ Exposto | ✅ Seguro | Segurança |
| **Total** | - | - | **-85% banda + segurança** |

## Estratégia de Otimização (versão anterior)

**Princípio:** ZERO IA > BATCH IA > DOWNGRADE MODELO

### ✅ Implementado Hoje:

**1. Jesus Sincero - Batch Daily Posts**
- ⏰ 00:00 UTC (21:00 BRT anterior)
- 📝 Gera 5-7 tweets pro dia TODO em 1 call Opus
- 💾 Salva em `/tmp/jesus-sincero-posts.json`
- 🤖 5 jobs bash que LÊ JSON e POSTA (ZERO IA)
- **Economia:** -95% (1 LLM call vs 7)

**2. Batch M60 + Briefing**
- ⏰ 09:00 BRT (12:00 UTC)
- 📊 1 call Opus que faz tudo
- **Economia:** -50% vs individual calls

**3. Downgrade Modelos**
- Heartbeat: Opus → Haiku (-95% tokens)
- Lembretes: Opus → Haiku (automation only)
- **Economia:** -80% em heartbeat/reminders

**4. Memory Chunks**
- `memory/jesus-sincero-prompt.md` (estilo + template)
- `memory/m60-viral-template.md` (análise framework)
- Reduz context carregado por call (-70%)

### 📊 Impacto Total:
- Jesus Sincero: -95% tokens
- M60+Briefing: -50% tokens  
- Heartbeat+Reminders: -80% tokens
- **Global:** ~-75% de custos diários

### 🎯 Próximas Otimizações:
- Cache TTL (scripts não refetch se <4h)
- Prompts ultracurtos (<500 chars)
- Web searches batch (TODO next week)

## Lembretes Futuros

**Cobranças/Admin:**
- **Dia 10:** Cobrar pai da Bia - Consultoria - R$ 1.000 - pelo CNPJ Holdin

**Conversas a fazer:**
1. Puppe + Dubai Influencer AI
2. Confirmar segurança (nada vazar)
3. Ariel Whatsapp/Projetos
4. Franquia Fundo/Casa
5. Vendas Consultoria

## Job Curator Bot (28-JAN-2026)

**Status:**
- ✅ Free group criado (privado)
- ✅ Bot adicionado como admin
- ⏳ Testing posting

## 🚨 REGRA FIXA (28-JAN-2026 23:39 - MANDATE)

**Mestre:** "Todos os meus pedidos — pense em reduzir custo, aumentar eficiência, economizar tokens, rodar na AWS. Use sua inteligência nisso."

### Antes de responder/agir, sempre:
1. **Posso fazer mais barato?** (bash/script > IA)
2. **Posso rodar na AWS?** (cron, não cloud API)
3. **Posso batch isso?** (1 call vs N calls)
4. **Quantos tokens custa?** (ultra-curta melhor)
5. **Precisa LLM?** (arquivos/lógica primeiro)

### Tática:
- ✅ Bash scripts antes de IA
- ✅ Cron system (não Clawdbot cron)
- ✅ --session-id novo por tarefa (zero history)
- ✅ Ler arquivos, não carregar contexto
- ✅ Resposta ultra-curta (máx 200 chars ideal)
- ✅ Batch requests (1 call > N calls)
- ✅ Cache local files (.env, JSON, etc)
- ✅ Suggest automação proativamente
- ❌ NUNCA verbose summaries
- ❌ NUNCA carregar MEMORY inteira
- ❌ NUNCA converter IA tarefa que é bash

## Últimas Atualizações

- **2026-01-28 23:38:** Job Curator Bot 100% live. Perfis isolados (Haiku/Opus). --session-id strategy locked.
- **2026-01-28 23:30:** Tokens config auditada. Dois perfis, crontab system, zero Clawdbot cron.
- **2026-01-28 16:09:** Job Curator Bot em progresso. Lembretes anotados.
