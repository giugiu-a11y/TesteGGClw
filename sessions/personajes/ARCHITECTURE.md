# Arquitetura: Jesus Sincero Bot

---

## 🏗️ Fluxo de Execução

```
┌─────────────────────────────────────────────────────────────┐
│ SEMANA N                                                    │
└─────────────────────────────────────────────────────────────┘

📅 SEGUNDA-FEIRA 23:00 BRT (02:00 UTC TERÇA)
│
├─ BATCH GENERATOR (1 call Claude)
│  ├─ Lê: config/persona.txt
│  ├─ Prompt: Gera 35 posts (5/dia × 7 dias)
│  ├─ Output: JSON {"posts": [{"date": "2026-02-06", "time": "09:00", "text": "..."}]}
│  └─ Salva: data/posts_current.json
│
├─ ARQUIVO: data/archive/posts_2026-02-06.json (backup)
│
└─ ✅ Pronto para semana

┌─────────────────────────────────────────────────────────────┐
│ TERÇA a DOMINGO (5 posts/dia)                              │
└─────────────────────────────────────────────────────────────┘

⏰ 09:00 BRT (12:00 UTC) — POST #1
│
├─ CRON executa: scripts/post-daily.sh 09:00
│  ├─ Lê: data/posts_current.json
│  ├─ Extrai: post com time="09:00" e date=hoje
│  ├─ Posta: Chama post_jesus.py (tweepy)
│  └─ Log: logs/posting.log
│
└─ 🐦 Tweet enviado

⏰ 12:00 BRT — POST #2
│
├─ CRON executa: scripts/post-daily.sh 12:00
│  └─ (mesmo fluxo)
│
└─ 🐦 Tweet enviado

... (15:00, 18:00, 21:00)
```

---

## 📊 Economia de Tokens

### Sem Batch (❌ Antigo)
```
35 chamadas Claude/dia
× 150 tokens por chamada
= 5.250 tokens/dia
× 30 dias
= 157.500 tokens/mês
```

### Com Batch (✅ Novo)
```
1 chamada Claude/semana
× 4.000 tokens
= 4.000 tokens/semana

Posting (bash): 0 tokens
× 35 posts
= 0 tokens/semana (zero IA)

Total: 4.000 tokens/semana ÷ 7 dias = 571 tokens/dia
× 30 dias = 2.280 tokens/mês

ECONOMIA: 157.500 - 2.280 = 155.220 tokens/mês (98% MENOS)
```

---

## 🔐 Segurança & Credenciais

### .env (OAuth 1.1 Twitter)
```
TWITTER_CONSUMER_KEY=AJT7vOOsiJur52qWFKS20N2hn
TWITTER_CONSUMER_SECRET=v8hr2MVDCq2cU24btG7vpo1vuBQX6Zi1ysc5pa3ZWEZSyr9MSK
TWITTER_ACCESS_TOKEN=1993067298794655744-RBpTkBSz1JC9UkokSyulbiU9kQ1zDV
TWITTER_ACCESS_TOKEN_SECRET=Xaj7rUGne4k26pbEZ55eWlQncDWe7JO7XnNi6ymMYUKcu
```

### Permissions
```bash
chmod 600 .env
# Só ubuntu lê/escreve
```

### Redação em Logs
```python
# post_jesus.py faz redação automática
_TOKEN_RE = re.compile(r"\b\d{9,}:[A-Za-z0-9_-]{20,}\b")
# Substitui: <redacted-token>
```

---

## 📝 Persona: Regras Rígidas

**TONE:**
- ✅ Reflexivo, existencial, provocador
- ✅ Simples, direto, acessível
- ✅ Terceira pessoa ("Jesus vê...", "Jesus pergunta...")
- ❌ NUNCA "Eu..." ou "Nós..."
- ❌ NUNCA linguagem técnica ou complexa

**TEMAS:**
- ✅ Mudança pessoal, autenticidade, relacionamentos
- ✅ Paradoxos da vida, espiritualidade (sem religião forçada)
- ✅ Reflexões sobre medo, vulnerabilidade, transformação
- ❌ NUNCA bolsas, intercâmbio, educação formal
- ❌ NUNCA reclame, negatividade pura, politização

**COMPRIMENTO:**
- 280 chars max (1 tweet)
- Provocação + reflexão + ação implícita

**EXEMPLO BOM:**
"Metade das orações são pra mudar os outros. Outra metade, pra Deus não mudar nada dentro de si. Jesus sorri dessa contradição humana."
→ Comprimento: 118 chars
→ Provocação: "oração não funciona assim"
→ Reflexão: contradição humana
→ Ação: implícita (reflita e mude)

**EXEMPLO RUIM:**
"Quer bolsa internacional? Vem com a gente!"
→ Errado: Tema proibido (bolsas)
→ Errado: Marketing, não reflexão
→ Errado: Tom direto demais, não Jesus Sincero

---

## 🔄 Fluxo de Dados

### posts_current.json (Semana Ativa)
```json
{
  "week": "2026-02-05 to 2026-02-11",
  "generated_at": "2026-02-04T23:00:00Z",
  "posts": [
    {
      "date": "2026-02-05",
      "time": "09:00",
      "text": "Metade das orações são pra mudar os outros..."
    },
    {
      "date": "2026-02-05",
      "time": "12:00",
      "text": "..."
    },
    ...
  ]
}
```

### Archive (Histórico)
```
data/archive/
├── posts_2026-01-30.json (semana anterior)
├── posts_2026-02-06.json (semana atual)
└── posts_2026-02-13.json (próxima semana)
```

---

## 🚨 Error Handling

### Se tweets falharem (API limit, credenciais, etc)
```bash
logs/error.log ← Todos os erros

Estratégia:
1. Log com timestamp
2. Não falha cron (exit 0)
3. Tenta novamente próximo horário
4. Alert se >3 erros/dia
```

### Se batch generator falhar
```bash
logs/batch-generation.log

Se falhar:
1. Mantém posts_current.json anterior (fallback)
2. Log de erro detalhado
3. Sem interrupção de posts
```

---

## 📋 Checklist de Produção

- [x] Pasta estruturada
- [x] Credenciais seguras (.env, chmod 600)
- [x] Persona documentada
- [x] Scripts profissionais
- [x] Logs organizados
- [x] Cron agendado
- [x] Post manual testado
- [x] Confirmação no Twitter
- [x] Healthcheck DNS diário (sem LLM)

---

## 🔄 Atualização Semanal

**Toda 2ª-feira 23:00 BRT:**
```bash
# Cron automático:
0 2 * * 2 cd /home/ubuntu/clawd/sessions/personajes && bash -lc "source venv/bin/activate && bash scripts/batch-generator.sh" >> /home/ubuntu/clawd/sessions/personajes/logs/batch-generation.log 2>&1
```

**Processo:**
1. Claude gera 35 tweets
2. Salva em data/posts_current.json
3. Backup anterior em data/archive/
4. Pronto para semana!

---

**Última atualização:** 05 FEV 2026
**Status:** 🟢 Operacional e monitorado
