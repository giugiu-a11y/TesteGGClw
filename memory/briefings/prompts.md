# Briefings - Prompts (PT)

## 1) Virais/Trends (separado de notícias)
**Input:** JSON de `/tmp/briefing-virais.json`

**Instruções:**
- PT sempre, direto, sem enrolação.
- 5 itens máx.
- Cada item: tema + por que viralizou + 1 ideia prática.
- **Sem links**.
- Sem texto extra.

**Formato sugerido (Telegram):**
- 🔥 Tema — por que viralizou | ideia M60

---

## 2) Briefing Notícias (separado de virais)
**Input:** JSON de `/tmp/briefing-noticias.json`

**Instruções:**
- PT sempre.
- Top 3 notícias (bolsas, edtech M&A, imigração, geopolítica, Brasil economia).
- Para cada: impacto prático **sem links**.
- Fechar com 1 ação recomendada.

**Formato sugerido (Telegram):**
- 🧭 Notícia — impacto
- ✅ Ação: ...

---

## 3) Briefing Mercado (curtinho)
**Input:** JSON de `/tmp/briefing-mercado.json`

**Instruções:**
- PT sempre.
- 5–6 bullets no máximo.
- BTC/AVAX/MATIC, S&P 500, USD/BRL e Selic.
- Uma linha de risco/oportunidade.

**Formato sugerido (Telegram):**
- ₿ BTC: $... (24h ...) — leitura rápida
- 🔺 AVAX: $... | 🔷 MATIC/POL: $...
- 📈 S&P 500: ...
- 💵 USD/BRL: ... | 🏦 Selic: ...
- ⚠️ Risco/Oportunidade: ...
