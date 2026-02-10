#!/usr/bin/env python3
"""
Test Pipeline - Testa o pipeline completo com dados de teste
Executa sem depender de APIs externas
"""

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from test_data import get_test_jobs
from job_filters import filter_jobs
from link_resolver import resolve_job_link
from job_analyzer import batch_analyze_jobs, JobAnalysis
from diversity_validator import validate_diversity, print_batch_summary
from telegram_poster import format_job_message

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


def test_pipeline():
    """Testa pipeline completo"""
    
    logger.info("\n" + "="*60)
    logger.info("🧪 TEST PIPELINE - Job Curator Bot v2.1")
    logger.info("="*60)
    
    # FASE 1: Obter dados de teste
    logger.info("\n📋 FASE 1: DADOS DE TESTE")
    raw_jobs = get_test_jobs()
    logger.info(f"✓ {len(raw_jobs)} vagas de teste carregadas")
    
    # FASE 2: Filtrar
    logger.info("\n🌍 FASE 2: FILTRAR POR PAÍS/SETOR/IDIOMA")
    filtered_jobs = filter_jobs(raw_jobs)
    logger.info(f"✓ {len(filtered_jobs)} vagas após filtros")
    
    if not filtered_jobs:
        logger.error("❌ Nenhuma vaga após filtros!")
        return False
    
    # FASE 3: Resolver links
    logger.info("\n🔗 FASE 3: RESOLVER LINKS PARA SITES OFICIAIS")
    resolved_jobs = []
    
    for job in filtered_jobs:
        direct_url, status = resolve_job_link(job)
        
        if direct_url:
            job['_direct_url'] = direct_url
            job['_url_status'] = status
            resolved_jobs.append(job)
            logger.info(f"✓ {job['company']:15} → {status:8} → {direct_url[:40]}...")
        else:
            logger.warning(f"✗ {job['company']:15} - falhou resolver")
    
    logger.info(f"✓ {len(resolved_jobs)} vagas com links resolvidos")
    
    if not resolved_jobs:
        logger.error("❌ Nenhuma vaga com link!")
        return False
    
    # FASE 4: Análise (sem Claude - usando dados predefinidos)
    logger.info("\n📊 FASE 4: ANÁLISE (simulado, sem Claude)")
    
    # Para teste, criamos como dicts para validação de diversidade
    analyzed_jobs_dicts = [
        {
            "titulo": "Software Engineer",
            "empresa": "Google",
            "pais_ou_remoto": "Remoto EUA",
            "salario_usd_mes": 13333,
            "moeda": "USD",
            "descricao_curta": "Construir sistemas escaláveis com Python",
            "nivel_ingles": "Fluente",
            "texto_faculdade": "Não importa",
            "texto_experiencia": "5+ anos",
            "url_origem": "https://weworkremotely.com/...",
            "direct_url": "https://google.com/careers/...",
            "_country": "us",
            "_sector": "technology",
            "_education": "yes",
            "_english": "fluent",
            "_experience": "yes",
            "_experience_years": 5,
        },
        {
            "titulo": "UX/UI Designer",
            "empresa": "Figma",
            "pais_ou_remoto": "Remoto Canadá",
            "salario_usd_mes": 5000,
            "moeda": "USD",
            "descricao_curta": "Design interfaces bonitas com Figma",
            "nivel_ingles": "Intermediário",
            "texto_faculdade": "Não importa",
            "texto_experiencia": "2+ anos",
            "url_origem": "https://linkedin.com/...",
            "direct_url": "https://figma.com/careers/...",
            "_country": "canada",
            "_sector": "design",
            "_education": "no",
            "_english": "intermediate",
            "_experience": "yes",
            "_experience_years": 2,
        },
        {
            "titulo": "Registered Nurse - Remote",
            "empresa": "TelaDoc Health",
            "pais_ou_remoto": "Remoto EUA",
            "salario_usd_mes": 6250,
            "moeda": "USD",
            "descricao_curta": "Profissional de saúde. Pode trabalhar em português.",
            "nivel_ingles": "Não precisa",
            "texto_faculdade": "Não importa",
            "texto_experiencia": "Qualquer um",
            "url_origem": "https://indeed.com/...",
            "direct_url": "https://teladoc.com/careers/...",
            "_country": "us",
            "_sector": "healthcare",
            "_education": "no",
            "_english": "none",
            "_experience": "no",
            "_experience_years": 0,
        },
    ]
    
    logger.info(f"✓ {len(analyzed_jobs_dicts)} vagas criadas (simulado)")
    
    # Para posting, convertemos para JobAnalysis
    analyzed_jobs = []
    for j in analyzed_jobs_dicts:
        analyzed_jobs.append(JobAnalysis(
            titulo=j["titulo"],
            empresa=j["empresa"],
            pais_ou_remoto=j["pais_ou_remoto"],
            salario_usd_mes=j["salario_usd_mes"],
            moeda=j["moeda"],
            descricao_curta=j["descricao_curta"],
            nivel_ingles=j["nivel_ingles"],
            texto_faculdade=j["texto_faculdade"],
            texto_experiencia=j["texto_experiencia"],
            url_origem=j["url_origem"],
            direct_url=j["direct_url"],
            aprovada=True,
        ))
    
    # FASE 5: Validação de diversidade
    logger.info("\n✅ FASE 5: VALIDAÇÃO DE DIVERSIDADE")
    
    valid, failing = validate_diversity(analyzed_jobs_dicts)
    
    if not valid:
        logger.error(f"❌ Validação falhou:")
        for rule in failing:
            logger.error(f"   {rule}")
        return False
    
    logger.info("✓ Batch validado com sucesso!")
    
    # FASE 6: Preview de posting
    logger.info("\n📤 FASE 6: PREVIEW TELEGRAM")
    
    for i, job in enumerate(analyzed_jobs, 1):
        logger.info(f"\n--- VAGA {i} ---")
        message = format_job_message(job)
        # Limpa para log (remove alguns caracteres especiais)
        print(message)
    
    logger.info("\n" + "="*60)
    logger.info("✅ TEST PIPELINE COMPLETO COM SUCESSO!")
    logger.info("="*60)
    logger.info("\nPróximos passos:")
    logger.info("1. Integrar APIs reais (Google Jobs, LinkedIn, Indeed, etc)")
    logger.info("2. Testar com Claude API para análise real")
    logger.info("3. Configurar cron para ciclo 24h")
    logger.info("4. Configurar Telegram bot token + chat ID")
    
    return True


if __name__ == "__main__":
    success = test_pipeline()
    sys.exit(0 if success else 1)
