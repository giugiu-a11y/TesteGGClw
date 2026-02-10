
🎯 LÓGICA FINAL - JOB CURATOR BOT v2.1

📅 CICLO DE 24H: Início (00:00 UTC = 21:00 BRT anterior)
1. Pesquisa vagas globalmente (Google Jobs, LinkedIn, Indeed, Agregadores)
2. Filtra por países + idioma + setor
3. Resolve links para site oficial
4. Analisa com Claude (batch 1 call) - **ATENÇÃO:** Trocar para Gemini 2.5 Flash Lite
5. Valida diversidade
6. Salva resultado em cache (TTL 24h)

Posting (3x distribuído)
• 09:00 UTC → 1 vaga
• 15:00 UTC → 1 vaga
• 21:00 UTC → 1 vaga

🔍 FASE 1: PESQUISA (1 CALL)
Busca 50 vagas brutas com keywords variados:
- "Software Engineer remote"
- "Designer remote"
- "Nurse remote"
- "Project Manager remote"
- "Accountant remote"
- ... (rotação por setor)
Fontes:
• Google Jobs API
• LinkedIn (scraping básico)
• Indeed
• WWR, RemoteOK (só pra achar vagas, não postar)

✅ FASE 2: FILTROS (ZERO LLM)
Rejeita automaticamente:
❌ Brasil / LATAM
❌ Índia, Filipinas, etc
✅ Europa (DE, FR, NL, PT, UK, IT, ES, etc)
✅ Austrália
✅ EUA
✅ Canadá
Output: ~15-20 vagas passam

🔗 FASE 3: RESOLUÇÃO DE LINKS (VERIFICAR USO DE LLM)
Para cada vaga agregadora:
1. Extrai empresa + cargo
2. Busca site oficial (google.com/careers, netflix.jobs, etc)
3. Encontra a vaga lá
4. Valida URL direto (não agregador)
5. Se falhar → descarta
Output: ~10-15 vagas com links diretos

🤖 FASE 4: ANÁLISE GEMINI (1 BATCH CALL) - **PRIORIDADE Gemini 2.5 Flash Lite**
Prompt: "Analise estas 15 vagas e retorne JSON estruturado"
Extrai para CADA vaga:
JSON {
  "titulo": "...",
  "empresa": "...",
  "pais": "...",
  "setor": "saude|exatas|humanas|artes|tech|business",
  "salario_usd_mes": 5000,
  "salario_estimado": true/false,
  "requisitos": {
    "ingles": "fluente|intermediario|basico|nao_precisa",
    "faculdade": "sim|nao|nao_importa",
    "experiencia_anos": 0|2|5|10,
    "descricao": "1 linha"
  },
  "aprovada": true/false,
  "motivo_rejeicao": "..."
}
Output: ~8-12 vagas analisadas

📊 FASE 5: VALIDAÇÃO DE DIVERSIDADE (ZERO LLM)
Antes de postar, valida:
✅ Países mesclados? (min 2 países diferentes)
✅ Com faculdade? (min 1)
✅ Sem faculdade? (min 1)
✅ Setores variados? (min 3 diferentes)
✅ Sem inglês fluente? (min 1)
✅ Sem experiência? (min 1)
✅ Com experiência? (min 1)
✅ Internacional? (ninguém de cidadania específica)
Se falhar validação → descarta lote, tenta novamente amanhã
Output: 3 vagas aprovadas por ciclo (garantem diversidade)

📤 FASE 6: POSTING (3x distribuído)
09:00 UTC → Vaga 1 (Tech, Alemanha, com experiência)
15:00 UTC → Vaga 2 (Saúde, Canadá, sem experiência, português OK)
21:00 UTC → Vaga 3 (Design, USA, sem faculdade necessária)

Formato:
🎯 [TÍTULO] [EMPRESA]
📍 [PAÍS]
💰 [MOEDA] $[SALÁRIO]/mês
✓ [Descrição 1 linha]
Requisitos:
• Inglês: [Fluente/Intermediário/Básico/Não precisa]
• Faculdade: [Sim/Não/Não importa]
• Experiência: [Sim, X+ anos / Não / Qualquer um]
APLICAR: [LINK DIRETO]

💰 EFICIÊNCIA (OTIMIZADO):
| Fase | LLM Calls | Tipo | Resultado |
| -------------- | --------- | ------------ | ---------------- |
| Pesquisa | 0 | Scraping | 50 vagas |
| Filtros | 0 | Regex | 15 vagas |
| Resolver Links | VERIFICAR USO DE LLM | HTTP/Parsing | 12 vagas |
| Análise | 1 | Gemini Batch | 8 vagas |
| Validação | 0 | Lógica | 3 vagas |
| TOTAL/DIA | ~1-2 CALLS (dependendo Fase 3) | | 3 vagas postadas |

📁 ARQUIVOS A CRIAR/ATUALIZAR:
1. sessions/assistente-agents-bots/remote-work-bot/job_sources.py — Google Jobs + LinkedIn + Indeed
2. sessions/assistente-agents-bots/remote-work-bot/job_filters.py → NOVO: Filtros país/setor/idioma (zero LLM)
3. sessions/assistente-agents-bots/remote-work-bot/link_resolver.py — Atualizado: Resolve links diretos (VERIFICAR USO DE LLM)
4. sessions/assistente-agents-bots/remote-work-bot/job_analyzer.py — Atualizado: Análise batch (1 call Gemini 2.5 Flash Lite)
5. sessions/assistente-agents-bots/remote-work-bot/diversity_validator.py → NOVO: Valida requisitos
6. sessions/assistente-agents-bots/remote-work-bot/telegram_poster.py — Atualizado: Novo formato, usa API direta, chat_id=-1003378765936
7. sessions/assistente-agents-bots/remote-work-bot/main.py — Pipeline novo com ciclo 24h + posting 3x
8. sessions/assistente-agents-bots/remote-work-bot/cron_config → Cron: 00:00 UTC pesquisa, 09/15/21:00 UTC posting
