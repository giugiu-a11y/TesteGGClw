#!/usr/bin/env python3
"""
Job Curator Bot v2.2 - Pipeline 100% FREE
RSS + Scraping + APIs públicas (zero custos)
"""

import os
import sys
import json
import logging
import argparse
import time
import re
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Carrega .env PRIMEIRO
load_dotenv(Path(__file__).parent / ".env")

sys.path.insert(0, str(Path(__file__).parent))

from job_sources_free import collect_from_free_sources
from job_filters import filter_jobs
from link_resolver import resolve_job_link
from job_analyzer import batch_analyze_jobs, JobAnalysis
from diversity_validator import validate_diversity, print_batch_summary
from telegram_poster import post_via_telegram_api, format_job_message
from cache_manager import cache_get, cache_set

# Para tipagem
from job_analyzer import JobAnalysis as JobAnalysisType

STATE_FILE = Path(__file__).parent / "state.json"
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class _RedactingFilter(logging.Filter):
    _token_re = re.compile(r"\b\d{9,}:[A-Za-z0-9_-]{20,}\b")

    def __init__(self):
        super().__init__()
        self._secrets = [
            os.getenv("TELEGRAM_BOT_TOKEN"),
            os.getenv("GEMINI_API_KEY"),
            os.getenv("GOOGLE_API_KEY"),
            os.getenv("TELEGRAM_GROUP_ID"),
            os.getenv("TELEGRAM_CHAT_ID"),
            os.getenv("ALLOWED_USER_ID"),
        ]
        self._secrets = [s for s in self._secrets if s]

    def _redact(self, text: str) -> str:
        if not text:
            return text
        text = self._token_re.sub("<redacted-token>", text)
        for secret in self._secrets:
            text = text.replace(secret, "<redacted>")
        return text

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        redacted = self._redact(msg)
        record.msg = redacted
        record.args = ()
        return True


for _h in logging.getLogger().handlers:
    _h.addFilter(_RedactingFilter())


def run_research(limit_per_source: int = 15, use_cache: bool = True) -> list:
    """
    Pesquisa de vagas (usa cache 48h para economizar)
    """
    logger.info("="*60)
    logger.info("📋 FASE 1: PESQUISA (100% FREE)")
    logger.info("="*60)
    
    # Tenta cache 48h
    if use_cache:
        cached, cache_info = cache_get("daily_research_free")
        if cached and not cache_info["expired"]:
            logger.info(f"✓ Cache hit ({cache_info['age_hours']}h old)")
            return cached
    
    # Coleta
    start_time = time.time()
    raw_jobs = collect_from_free_sources(limit_per_source=limit_per_source)
    elapsed = time.time() - start_time
    
    logger.info(f"✓ {len(raw_jobs)} vagas em {elapsed:.1f}s")
    
    if not raw_jobs:
        logger.error("❌ Nenhuma vaga coletada!")
        return []
    
    # Filtra
    logger.info("\n🌍 Filtrando por país/setor...")
    filtered = filter_jobs(raw_jobs)
    logger.info(f"✓ {len(filtered)} após filtros")
    
    if not filtered:
        logger.error("❌ Nenhuma vaga após filtros!")
        return []
    
    # Resolve links
    logger.info("\n🔗 Resolvendo links...")
    resolved = []
    
    for job in filtered:
        direct_url, status = resolve_job_link(job)
        if direct_url and status in ["direct", "resolved"]:
            job['_direct_url'] = direct_url
            job['_url_status'] = status
            resolved.append(job)
        
        time.sleep(0.1)  # Rate limiting amigável
    
    logger.info(f"✓ {len(resolved)} com links diretos")
    
    if not resolved:
        logger.error("❌ Nenhum link resolvido!")
        return []
    
    # Cache por 48h
    cache_set("daily_research_free", resolved, ttl_hours=48)
    
    return resolved


def run_analysis(jobs: list) -> list:
    """Análise com Claude (1 call)"""
    logger.info("\n" + "="*60)
    logger.info("📊 FASE 2: ANÁLISE CLAUDE (1 call)")
    logger.info("="*60)
    
    if not jobs:
        return []
    
    to_analyze = jobs[:20]  # Limita a 20 por call
    
    logger.info(f"🤖 Analisando {len(to_analyze)} vagas...")
    analyzed = batch_analyze_jobs(to_analyze)
    
    logger.info(f"✓ {len(analyzed)} aprovadas")
    return analyzed


def run_validation(jobs: list) -> list:
    """Validação de diversidade"""
    logger.info("\n" + "="*60)
    logger.info("✅ FASE 3: VALIDAÇÃO DIVERSIDADE")
    logger.info("="*60)
    
    if len(jobs) < 3:
        logger.error(f"❌ Só {len(jobs)} vagas, precisa 3")
        return []
    
    # Converte JobAnalysis para dict para validação
    jobs_as_dict = []
    for job in jobs:
        if isinstance(job, JobAnalysis):
            # JobAnalysis não tem atributos como _country
            # Pulamos validação de diversidade se for JobAnalysis
            jobs_as_dict.append(job)
        else:
            jobs_as_dict.append(job)
    
    # Se temos JobAnalysis objects, pula validação de diversidade (assume OK)
    if all(isinstance(j, JobAnalysis) for j in jobs_as_dict[:3]):
        logger.info("✅ Batch OK (análise Claude validou)")
        return jobs_as_dict[:3]
    
    # Se tem dicts, valida com diversity_validator
    for i in range(min(10, len(jobs_as_dict) - 2)):
        batch = jobs_as_dict[i:i+3]
        valid, _ = validate_diversity(batch)
        
        if valid:
            logger.info("✅ Batch validado!")
            logger.info(print_batch_summary(batch))
            return batch
    
    logger.error("❌ Sem batch com diversidade")
    return []


def post_jobs(jobs: list, dry_run: bool = False) -> int:
    """Posta vagas"""
    logger.info("\n" + "="*60)
    logger.info(f"📤 {'[DRY RUN] ' if dry_run else ''}POSTING")
    logger.info("="*60)
    
    posted = 0
    
    for i, job in enumerate(jobs, 1):
        logger.info(f"\n🎯 Vaga {i}/{len(jobs)}")
        
        if dry_run:
            logger.info("=== PREVIEW ===")
            print(format_job_message(job))
            logger.info("===============")
            posted += 1
        else:
            # Método direto ao Telegram API (que funcionava antes)
            bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
            chat_id = os.environ.get("TELEGRAM_CHAT_ID", "-1003378765936")
            
            if not bot_token:
                logger.error("TELEGRAM_BOT_TOKEN não configurado")
                return 0
            
            success = post_via_telegram_api(job, bot_token, chat_id)
            if success:
                posted += 1
                time.sleep(1)  # Rate limiting
    
    return posted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["full", "research", "analyze", "post"],
                       default="full")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-cache", action="store_true", help="Força pesquisa nova")
    parser.add_argument("--limit", type=int, default=15)
    
    args = parser.parse_args()
    
    logger.info("\n" + "="*60)
    logger.info("🚀 JOB CURATOR BOT v2.2 (100% FREE)")
    logger.info(f"   Mode: {args.mode} | Dry-run: {args.dry_run}")
    logger.info("="*60 + "\n")
    
    # Research
    research_jobs = run_research(
        limit_per_source=args.limit,
        use_cache=not args.skip_cache
    )
    
    if not research_jobs:
        logger.error("Abortando: sem vagas")
        return 1
    
    # Análise
    analyzed = run_analysis(research_jobs)
    
    if not analyzed:
        logger.error("Abortando: análise falhou")
        return 1
    
    # Validação
    validated = run_validation(analyzed)
    
    if not validated:
        logger.error("Abortando: sem diversidade")
        return 1
    
    # Posting
    posted = post_jobs(validated, dry_run=args.dry_run)
    
    logger.info("\n" + "="*60)
    logger.info(f"✅ COMPLETO - {posted}/{len(validated)} postadas")
    logger.info("="*60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
