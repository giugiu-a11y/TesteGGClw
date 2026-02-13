# BEST_PRACTICES.md - Skills & Agents para Projetos Longos

**Fonte:** https://developers.openai.com/blog/skills-shell-tips
**Data de referência:** 2026-02-12
**Acesso:** Todos os projetos

---

## 🎯 Resumo Executivo

Para agentes long-running que fazem trabalho real:
1. **Skills** = Procedimentos reutilizáveis (SKILL.md + workflows)
2. **Shell** = Ambiente de execução real (dependências, scripts, outputs)
3. **Compaction** = Gerenciamento automático de contexto (sem limite de tokens)

---

## 10 Dicas Práticas para Implementação

### 1️⃣ Descrições de Skills = Lógica de Roteamento
**NÃO:** Marketing copy vago
**SIM:** Responder:
- Quando usar? (inputs, contexto)
- Quando NÃO usar? (edge cases)
- O que entrega? (outputs esperados)
- Qual ferramenta executa?

📝 Incluir: "Use quando..." e "Não use quando..." direto na descrição

---

### 2️⃣ Exemplos Negativos = Reduz Misfires
**Problema:** Adicionar skills pode reduzir triggering correto (20% queda inicial em evals)
**Solução:** Adicionar casos explícitos de "don't call when..." + edge cases

💡 Glean: Recuperou 20% loss adicionando exemplos negativos nas descrições

---

### 3️⃣ Templates & Exemplos = Dentro da Skill
**Antes:** Tudo no system prompt → inflaciona tokens para queries não relacionadas
**Depois:** Exemplos dentro da skill → carregam APENAS quando skill trigga

✨ Melhor para:
- Relatórios estruturados
- Summaries de escalação
- Account plans
- Write-ups de análise de dados

---

### 4️⃣ Design para Longas Durações DESDE O INÍCIO
**Container Reuse:**
```
- Reutilizar mesmo container → dependências estáveis, cache, outputs intermediários
- Passar previous_response_id → continuar no mesmo thread
- Usar compaction como default, não como fallback de emergência
```

✅ Resultado: Menos restarts, multi-step jobs coerentes

---

### 5️⃣ Quando Precisa Determinismo = Força Uso Explícito
**Default:** Modelo decide quando usar skill (fuzzy routing)
**Production:** Diga explicitamente ao modelo:

```
"Use the <skill_name> skill."
```

🔒 Transforma roteamento fuzzy em contrato explícito

---

### 6️⃣ ⚠️ Skills + Networking = Alto Risco
**Perigo:** Exfiltração de dados via network access
**Defesa:**
- ✅ Skills: allowed
- ✅ Shell: allowed  
- ⚠️ Network: APENAS com allowlist mínima, per-request, tarefas narrow-scoped

**Regra de Ouro:** Evitar network + procedimentos poderosos em consumer-facing flows

---

### 7️⃣ /mnt/data = Handoff Boundary para Artifacts
**Padrão Mental:** Tools escrevem → Modelos raciocinam → Developers recuperam

Salvar em `/mnt/data/`:
- Relatórios
- Datasets limpos
- Spreadsheets finalizadas
- Outputs para steps posteriores

---

### 8️⃣ Allowlists = Sistema de 2 Camadas
**Org-level allowlist** (admin)
↓
**Request-level network_policy** (subset do org allowlist)

💼 Operacionalmente:
- Manter org allowlist: pequena + estável
- Manter request allowlist: ainda menor (apenas destinos necessários)
- Se request tiver domain fora org allowlist → error

---

### 9️⃣ domain_secrets = Auth sem Vazamento de Credenciais
**Problema:** Modelo nunca vê credenciais brutas
**Solução:** 
```
Modelo vê: $API_KEY (placeholder)
Sidecar injeta: valor real apenas para destinos aprovados
```

🔐 Default quando agent precisa chamar APIs protegidas dentro do container

---

### 🔟 APIs Idênticas = Cloud & Local
**Dev Loop Prático:**
1. **Local** → iteração rápida, debugging fácil, acesso a tooling interno
2. **Hosted Container** → repeatability, isolamento, deployment consistency
3. **Skills ficam iguais** → workflow estável entre modos

---

## 3 Padrões de Build

### Pattern A: Install → Fetch → Write Artifact ⭐
Mais simples. Benefício imediato:
```
1. Agent instala dependências
2. Scrape/API call
3. Escreve report em /mnt/data/report.md
→ Boundary limpo para review/log/diff/steps posteriores
```

### Pattern B: Skills + Shell para Workflows Repetíveis
**Quando:** Confiabilidade degrada com prompt drift
```
1. Encode workflow em skill (steps, guardrails, templates)
2. Mount skill no shell
3. Agent segue skill → artifacts determinísticos
```

**Casos de uso:**
- Spreadsheet analysis/editing
- Dataset cleaning + summary
- Standardized reports (recurring)

### Pattern C (Advanced): Skills como Enterprise Workflow Carriers
**Resultado Glean:** 73% → 85% accuracy eval + 18.1% TTF reduction
```
Skills = Living SOPs (Standard Operating Procedures)
- Account planning
- Escalation triage  
- Brand-aligned content generation
- Evolui com a org, executado consistently
```

---

## Checklist para Novo Projeto

- [ ] Skills têm descrição com "Use quando" + "Não use quando"
- [ ] Incluídos exemplos negativos nos skills
- [ ] Templates/exemplos estão DENTRO do skill, não no system prompt
- [ ] Planned para long-runs (container reuse + compaction)
- [ ] Outputs salvos em `/mnt/data/` ou equivalente
- [ ] Network allowlist configurada (se aplicável)
- [ ] domain_secrets usado para auth (se aplicável)
- [ ] Testado localmente primeiro, depois hosted
- [ ] Documentação de workflow em SKILL.md
- [ ] Versioning em place para skills

---

## Referências

- Skills Docs: https://developers.openai.com/api/docs/guides/tools-skills
- Shell Docs: https://developers.openai.com/api/docs/guides/tools-shell
- Compaction Docs: https://developers.openai.com/api/docs/guides/context-management
- Blog Post: https://developers.openai.com/blog/skills-shell-tips

---

**Aplicável a:** Todos os projetos longos, multi-step, agents real-work
**Última revisão:** 2026-02-12 por Akira Master
