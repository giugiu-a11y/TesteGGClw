#!/bin/bash
# compile-news.sh - Compila briefing em 3 partes (3 prompts IA separados)
# Input: /tmp/news.json | Output: /tmp/briefing-news-part{1,2,3}.txt

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$DIR/../venv"

# Carrega secrets
if [ -f ~/.config/secrets.env ]; then
  export $(cat ~/.config/secrets.env | grep -E "^[A-Z]|^export" | sed 's/export //' | xargs)
fi

# Ativa venv
if [ -f "$VENV/bin/activate" ]; then
  source "$VENV/bin/activate"
fi

if [ ! -f /tmp/news.json ]; then
  echo "Erro: /tmp/news.json não encontrado" >&2
  exit 1
fi

# ═══════════════════════════════════════════════════════════
# 3 PROMPTS SEPARADOS (melhor foco da IA)
# ═══════════════════════════════════════════════════════════

python3 << 'PYTHON_SCRIPT'
import json
import os
import sys
from datetime import datetime

# API setup
try:
    from google import genai
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
    USE_NEW_API = True
except ImportError:
    import google.generativeai as genai
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
    USE_NEW_API = False

# Carrega notícias
with open("/tmp/news.json", "r") as f:
    news = json.load(f)

# Data
meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
hoje = datetime.now()
data_pt = f"{hoje.day} de {meses[hoje.month-1]} de {hoje.year}"

def call_gemini(prompt):
    if USE_NEW_API:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        text = response.text.strip()
        try:
            usage = getattr(response, "usage_metadata", None)
        except Exception:
            usage = None
        return text, usage
    else:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        text = response.text.strip()
        usage = None
        # Older SDK may expose usage via response.candidates or response.usage_metadata
        try:
            usage = getattr(response, "usage_metadata", None)
        except Exception:
            usage = None
        return text, usage

def log_usage(tag, usage):
    try:
        with open("/tmp/briefings_llm_usage.jsonl", "a") as f:
            f.write(json.dumps({
                "ts": datetime.utcnow().isoformat() + "Z",
                "kind": "news",
                "part": tag,
                "model": "gemini-2.0-flash",
                "usage": usage if usage is not None else {}
            }) + "\n")
    except Exception:
        pass

def format_articles(categories):
    text = ""
    for cat_key, cat_name in categories:
        articles = news.get(cat_key, [])
        if articles:
            text += f"\n## {cat_name}:\n"
            for art in articles[:5]:
                if isinstance(art, dict):
                    title = art.get('title', '')
                    source = art.get('source', '')
                    if title and title != 'null':
                        text += f"- {title} ({source})\n"
    return text

base_rules = """
REGRAS RÍGIDAS:
❌ IGNORAR COMPLETAMENTE: esportes, futebol, apostas, Super Bowl, celebridades, entretenimento, curiosidades científicas, música, jogadores, times.
❌ Se a notícia não tiver relação DIRETA com educação/carreira/brasileiros no exterior → IGNORAR.
✅ APENAS notícias relevantes para brasileiros que querem estudar/trabalhar no exterior.
✅ Traduza títulos em inglês para português.
✅ Para cada notícia: título + (fonte) → impacto prático para alunos brasileiros.
✅ Se não houver notícias relevantes em uma categoria, escreva "Sem notícias relevantes hoje."
"""

def add_blank_lines(text):
    lines = text.splitlines()
    out = []
    for i, line in enumerate(lines):
        out.append(line)
        if line.strip().startswith(tuple(f"{n}." for n in range(1, 10))):
            if i + 1 < len(lines) and lines[i + 1].strip() != "":
                out.append("")
    return "\n".join(out).rstrip() + "\n"

# ═══════════════════════════════════════════════════════════
# PARTE 1: EDUCAÇÃO (Bolsas + Intercâmbio + Setor Educação)
# ═══════════════════════════════════════════════════════════

print("Gerando Parte 1: Educação...")
news_edu = format_articles([
    ('bolsas_exterior', 'BOLSAS INTERNACIONAIS'),
    ('intercambio', 'INTERCÂMBIO'),
    ('setor_educacao', 'SETOR EDUCAÇÃO')
])

prompt1 = f"""Você é curador de notícias para um briefing diário da UDI (escola brasileira de intercâmbio).

NOTÍCIAS COLETADAS:
{news_edu}

{base_rules}

REGRAS ESPECÍFICAS:
- BOLSAS: APENAS bolsas internacionais abertas para brasileiros (Fulbright, Chevening, DAAD, etc). ❌ Prouni, Fies, bolsas só para cidadãos locais.
- INTERCÂMBIO: Programas de estudo no exterior, universidades internacionais.
- SETOR EDUCAÇÃO: Tendências globais relevantes para quem quer estudar fora.

FORMATO (máx 1200 chars):
📰 BRIEFING DIÁRIO — {data_pt}
Parte 1/3: Educação & Oportunidades

🎓 BOLSAS INTERNACIONAIS
1. [título] (fonte) → [impacto prático]

2. [título] (fonte) → [impacto prático]

3. [título] (fonte) → [impacto prático]

🌍 INTERCÂMBIO
1. [título] (fonte) → [impacto prático]

2. [título] (fonte) → [impacto prático]

3. [título] (fonte) → [impacto prático]

📚 SETOR EDUCAÇÃO
1. [título] (fonte) → [impacto prático]

2. [título] (fonte) → [impacto prático]

3. [título] (fonte) → [impacto prático]

Gere agora:"""

try:
    part1, usage1 = call_gemini(prompt1)
    part1 = add_blank_lines(part1)
    with open("/tmp/briefing-news-part1.txt", "w") as f:
        f.write(part1)
    log_usage("part1", usage1)
    print("✅ Parte 1 OK")
except Exception as e:
    print(f"❌ Erro Parte 1: {e}", file=sys.stderr)
    part1 = ""

# ═══════════════════════════════════════════════════════════
# PARTE 2: MOBILIDADE (Vistos + Carreira + Geopolítica)
# ═══════════════════════════════════════════════════════════

print("Gerando Parte 2: Mobilidade...")
news_mob = format_articles([
    ('vistos_imigracao', 'VISTOS & IMIGRAÇÃO'),
    ('carreira_internacional', 'CARREIRA INTERNACIONAL'),
    ('geopolitica', 'GEOPOLÍTICA')
])

prompt2 = f"""Você é curador de notícias para um briefing diário da UDI (escola brasileira de intercâmbio).

NOTÍCIAS COLETADAS:
{news_mob}

{base_rules}

REGRAS ESPECÍFICAS:
- VISTOS: Vistos de estudante, trabalho, nômade digital, H1B, políticas migratórias que afetam brasileiros.
- CARREIRA: Trabalho remoto internacional, vagas globais, salários em dólar/euro.
- GEOPOLÍTICA: Políticas de EUA/Europa/Ásia que afetam brasileiros no exterior.

FORMATO (máx 1200 chars):
📰 BRIEFING DIÁRIO — {data_pt}
Parte 2/3: Mobilidade & Carreira

✈️ VISTOS & IMIGRAÇÃO
1. [título] (fonte) → [impacto prático]

2. [título] (fonte) → [impacto prático]

3. [título] (fonte) → [impacto prático]

💼 CARREIRA INTERNACIONAL
1. [título] (fonte) → [impacto prático]

2. [título] (fonte) → [impacto prático]

3. [título] (fonte) → [impacto prático]

🌐 GEOPOLÍTICA
1. [título] (fonte) → [impacto prático]

2. [título] (fonte) → [impacto prático]

3. [título] (fonte) → [impacto prático]

Gere agora:"""

try:
    part2, usage2 = call_gemini(prompt2)
    part2 = add_blank_lines(part2)
    with open("/tmp/briefing-news-part2.txt", "w") as f:
        f.write(part2)
    log_usage("part2", usage2)
    print("✅ Parte 2 OK")
except Exception as e:
    print(f"❌ Erro Parte 2: {e}", file=sys.stderr)
    part2 = ""

# ═══════════════════════════════════════════════════════════
# PARTE 3: MERCADO (Economia BR + EdTech & M&A)
# ═══════════════════════════════════════════════════════════

print("Gerando Parte 3: Mercado...")
news_mkt = format_articles([
    ('economia_brasil', 'ECONOMIA BRASIL'),
    ('edtech_ma', 'EDTECH & M&A')
])

prompt3 = f"""Você é curador de notícias para um briefing diário da UDI (escola brasileira de intercâmbio).

NOTÍCIAS COLETADAS:
{news_mkt}

{base_rules}

REGRAS ESPECÍFICAS:
- ECONOMIA BR: Dólar, câmbio, Selic - impacto para brasileiros que vão pro exterior.
- EDTECH & M&A: Aquisições, fusões, investimentos em educação/edtech.

FORMATO (máx 1000 chars):
📰 BRIEFING DIÁRIO — {data_pt}
Parte 3/3: Mercado & Tecnologia

📊 ECONOMIA BRASIL
1. [título] (fonte) → [impacto prático]

2. [título] (fonte) → [impacto prático]

3. [título] (fonte) → [impacto prático]

🚀 EDTECH & M&A
1. [título] (fonte) → [impacto prático]

2. [título] (fonte) → [impacto prático]

3. [título] (fonte) → [impacto prático]

✅ Ação do dia: [1 recomendação prática baseada nas notícias de hoje]

Gere agora:"""

try:
    part3, usage3 = call_gemini(prompt3)
    part3 = add_blank_lines(part3)
    with open("/tmp/briefing-news-part3.txt", "w") as f:
        f.write(part3)
    log_usage("part3", usage3)
    print("✅ Parte 3 OK")
except Exception as e:
    print(f"❌ Erro Parte 3: {e}", file=sys.stderr)
    part3 = ""

# Salva lista de partes
parts = []
for i in [1, 2, 3]:
    if os.path.exists(f"/tmp/briefing-news-part{i}.txt"):
        parts.append(f"/tmp/briefing-news-part{i}.txt")

with open("/tmp/briefing-news-parts.txt", "w") as f:
    f.write("\n".join(parts))

print(f"\n✅ {len(parts)} partes geradas com sucesso")

# Mostra preview
for i, p in enumerate(parts, 1):
    print(f"\n--- PARTE {i} ---")
    with open(p) as f:
        print(f.read()[:500] + "...")

PYTHON_SCRIPT
