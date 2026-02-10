#!/usr/bin/env python3
"""
Job Analyzer v2.1 - Análise em BATCH com Claude
Sem termos RH (Junior/Pleno/Senior).
1 CALL para N vagas = máxima eficiência.
"""

import json
import os
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)


@dataclass
class JobAnalysis:
    """Resultado estruturado da análise"""
    titulo: str
    empresa: str
    pais_ou_remoto: str
    salario_usd_mes: int  # SEMPRE preenchido
    moeda: str
    descricao_curta: str  # 1 linha
    
    # Requisitos (linguagem SIMPLES)
    nivel_ingles: str  # "Fluente", "Intermediário", "Básico", "Não precisa"
    texto_faculdade: str  # "Sim", "Não", "Não importa"
    texto_experiencia: str  # "Qualquer um", "Sim", "X+ anos"
    
    # URLs
    url_origem: str  # Onde encontrou (fonte - informativo)
    direct_url: str  # SITE OFICIAL (o que será postado)
    
    aprovada: bool
    motivo_rejeicao: Optional[str] = None


# Estimativas de salário por cargo (USD/mês)
SALARY_ESTIMATES = {
    # Tech
    "engineer": 6000, "senior engineer": 9000, "staff engineer": 12000,
    "software developer": 5500, "devops": 7000, "data scientist": 8000,
    "frontend": 5500, "backend": 6500, "fullstack": 6500,
    "machine learning": 9000, "ai engineer": 9000, "cloud": 7500,
    # Design
    "designer": 5500, "ux designer": 5500, "product designer": 6000,
    # Management
    "manager": 7000, "project manager": 5500, "product manager": 8000,
    # Other
    "analyst": 5000, "accountant": 5500, "nurse": 4500,
}


def call_gemini_api(prompt: str, timeout: int = 30) -> Optional[str]:
    """Chama Gemini via Google Generative AI API"""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.error("Gemini: GEMINI_API_KEY/GOOGLE_API_KEY não configurado")
        return None
    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
        )
        response_text = getattr(response, "text", None)
        if response_text:
            logger.debug("✓ Gemini respondeu")
            return response_text
        logger.error("Gemini: sem resposta")
        return None
    except Exception as e:
        logger.error(f"Gemini API erro: {e}")
        return None

# Anthropic mantido para futuro, mas desativado no fluxo atual
# def call_claude_api(prompt: str, timeout: int = 30) -> Optional[str]:
#     """Chama Claude via Anthropic API direto (desativado por enquanto)"""
#     try:
#         import anthropic
#         
#         client = anthropic.Anthropic()
#         
#         message = client.messages.create(
#             model="claude-haiku-4-5",
#             max_tokens=4096,
#             messages=[
#                 {"role": "user", "content": prompt}
#             ],
#             timeout=timeout
#         )
#         
#         response_text = message.content[0].text if message.content else None
#         
#         if response_text:
#             logger.debug(f"✓ Claude respondeu ({message.usage.output_tokens} tokens)")
#             return response_text
#         else:
#             logger.error("Claude: sem resposta")
#             return None
#             
#     except Exception as e:
#         logger.error(f"Claude API erro: {e}")
#         return None


def infer_salary(title: str, country: str) -> int:
    """
    Infere salário baseado em cargo e país.
    Retorna USD/mês.
    """
    title_lower = title.lower()
    
    # Busca no mapeamento
    for key, salary in SALARY_ESTIMATES.items():
        if key in title_lower:
            # Ajusta para país (LATAM é ~50% de US, mas aqui só temos US/EU/AU/CA)
            # Europa geralmente é 80% de US
            if any(x in country.lower() for x in ["germany", "france", "netherlands", "europe"]):
                return int(salary * 0.8)
            
            # Canadá = 85% de US
            if "canada" in country.lower():
                return int(salary * 0.85)
            
            # Default = US rate
            return salary
    
    # Default genérico
    return 5500

def _strip_html(text: str) -> str:
    if not text:
        return ""
    cleaned = re.sub(r"<[^>]+>", " ", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def batch_analyze_jobs(jobs: List[Dict[str, Any]], timeout: int = 60) -> List[JobAnalysis]:
    """
    Analisa múltiplas vagas em UM BATCH call.
    Máxima eficiência = 1 call para N vagas.
    """
    
    if not jobs:
        logger.warning("Nenhuma vaga para analisar")
        return []
    
    # Prepara jobs para prompt
    jobs_text = ""
    for i, job in enumerate(jobs[:12], 1):  # Limita a 12 por call (economia de tokens)
        desc = _strip_html(job.get('description', ''))
        jobs_text += f"""
VAGA {i}:
Título: {job.get('title', 'N/A')}
Empresa: {job.get('company', 'N/A')}
País/Local: {job.get('_country', 'Remoto')}
Descrição: {desc[:300]}
---
"""
    
    # PROMPT: Análise SEM termos RH
    prompt = f"""
Você é analisador de vagas de emprego. Analise estas vagas e retorne JSON estruturado.

REGRAS CRITICAS:
1. NUNCA use termos RH como "Junior", "Pleno", "Senior", "mid-level"
2. Use linguagem SIMPLES: "Com experiência", "Sem experiência", "Qualquer um"
3. Para educação: "Sim" (exige), "Não" (não exige), "Não importa"
4. Para inglês: "Fluente", "Intermediário", "Básico", "Não precisa"
5. Salário SEMPRE em USD/mês (divida anual por 12)
6. Se não informado, ESTIME baseado no cargo

VAGAS:
{jobs_text}

RETORNE UM JSON ARRAY (sem markdown) com este EXATO formato para cada vaga:

[
  {{
    "titulo": "Engenheiro de Software",
    "empresa": "Google",
    "pais_ou_remoto": "Remoto Global",
    "salario_usd_mes": 8000,
    "moeda": "USD",
    "descricao_curta": "Desenvolver APIs com Python para plataforma de pagamentos",
    "nivel_ingles": "Fluente",
    "texto_faculdade": "Sim",
    "texto_experiencia": "3+ anos",
    "aprovada": true,
    "motivo_rejeicao": null
  }}
]

IMPORTANTE:
- Descrição curta = MAX 80 caracteres, 1 linha
- texto_experiencia: "Qualquer um" OU "Sim" OU "X+ anos"
- Se algo não é mencionado, deixe em branco ou "Não informado"
- O campo "titulo" deve estar em português (traduza se estiver em inglês)
- Retorne APENAS o JSON array, nada mais
"""
    
    logger.info(f"📡 Analisando {len(jobs)} vagas com Gemini (1 batch call)...")
    
    response = call_gemini_api(prompt, timeout=timeout)
    
    if not response:
        logger.error("Gemini indisponível - rejeitando lote")
        return []
    
    # Parse JSON
    try:
        # Extrai JSON da resposta (pode ter markdown)
        import re
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if not json_match:
            logger.error(f"Sem JSON na resposta: {response[:200]}")
            return []
        
        analyses = json.loads(json_match.group())
        
    except json.JSONDecodeError as e:
        logger.error(f"Erro parseando JSON: {e}")
        logger.error(f"Resposta: {response[:500]}")
        return []
    
    # Mapeia análises para JobAnalysis
    results = []
    
    for i, analysis in enumerate(analyses):
        if i >= len(jobs):
            break
        
        job = jobs[i]
        
        try:
            # Salário: usa informado ou estima
            salario = analysis.get('salario_usd_mes')
            if not salario or salario < 1000:
                salario = infer_salary(job.get('title', ''), job.get('_country', 'us'))
            
            result = JobAnalysis(
                titulo=analysis.get('titulo', job.get('title', '')),
                empresa=analysis.get('empresa', job.get('company', '')),
                pais_ou_remoto=analysis.get('pais_ou_remoto', job.get('_country', '')),
                salario_usd_mes=max(1000, salario),  # Mínimo 1000
                moeda=analysis.get('moeda', 'USD'),
                descricao_curta=analysis.get('descricao_curta', '')[:80],
                nivel_ingles=analysis.get('nivel_ingles', 'Não informado'),
                texto_faculdade=analysis.get('texto_faculdade', 'Não informado'),
                texto_experiencia=analysis.get('texto_experiencia', 'Não informado'),
                url_origem=job.get('source_url', ''),
                direct_url=job.get('_direct_url', ''),
                aprovada=analysis.get('aprovada', True),
                motivo_rejeicao=analysis.get('motivo_rejeicao'),
            )
            
            if result.aprovada and result.direct_url:
                results.append(result)
                logger.info(f"✅ {result.titulo} @ {result.empresa}")
            else:
                logger.warning(f"❌ {result.titulo} (rejeitada: {result.motivo_rejeicao})")
                
        except Exception as e:
            logger.error(f"Erro processando análise {i}: {e}")
            continue
    
    logger.info(f"✅ {len(results)} vagas aprovadas")
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    test_jobs = [
        {
            "title": "Software Engineer",
            "company": "Google",
            "_country": "us",
            "source_url": "https://weworkremotely.com/...",
            "_direct_url": "https://google.com/careers/...",
            "description": "Develop APIs with Python. 3+ years required. Fluent English needed.",
        },
        {
            "title": "Product Designer",
            "company": "Figma",
            "_country": "canada",
            "source_url": "https://linkedin.com/...",
            "_direct_url": "https://figma.com/careers/...",
            "description": "Design user experiences. No degree required. $6000-8000/month.",
        },
    ]
    
    results = batch_analyze_jobs(test_jobs)
    
    print("\n=== ANÁLISE COMPLETA ===\n")
    for job in results:
        print(f"✅ {job.titulo} @ {job.empresa}")
        print(f"   {job.descricao_curta}")
        print(f"   💰 {job.moeda} ${job.salario_usd_mes}/mês")
        print(f"   🗣 Inglês: {job.nivel_ingles}")
        print(f"   🎓 Educação: {job.texto_faculdade}")
        print(f"   💼 Experiência: {job.texto_experiencia}")
        print(f"   🔗 {job.direct_url}")
        print()
