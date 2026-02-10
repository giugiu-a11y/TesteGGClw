#!/usr/bin/env python3
"""
Job Curator Bot v2.1 - MAIN PIPELINE
Ciclo de 24h: Pesquisa → Filtra → Resolve → Analisa → Valida → Posta (3x/dia)
"""

import os
import sys
import json
import logging
import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Setup path
sys.path.insert(0, str(Path(__file__).parent))

from job_sources import collect_from_all_sources, categorize_sector
from job_filters import filter_jobs
from link_resolver import resolve_job_link
from job_analyzer import batch_analyze_jobs, JobAnalysis
from diversity_validator import validate_diversity, print_batch_summary
from telegram_poster import post_to_telegram, post_via_clawdbot_message
from cache_manager import cache_get, cache_set

# Config
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


def load_state() -> dict:
    """Carrega estado (vagas já postadas, etc)"""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except:
            return {}
    return {}


def save_state(state: dict):
    """Salva estado"""
    STATE_FILE.write_text(json.dumps(state, indent=2))


def run_daily_research(limit_per_source: int = 20) -> List[Dict[str, Any]]:
    """
    FASE 1: Pesquisa diária (uma vez por dia)
    Coleta de múltiplas fontes, filtra, resolve links.
    """
    logger.info("="*60)
    logger.info("📋 FASE 1: PESQUISA DIÁRIA")
    logger.info("="*60)
    
    # Tenta cache (24h)
    cached, cache_info = cache_get("daily_research")
    if cached and not cache_info["expired"]:
        logger.info(f"✓ Usando cache ({cache_info['age_hours']}h old)")
        return cached
    
    # Coleta das fontes
    logger.info("🔍 Coletando vagas de múltiplas fontes...")
    raw_jobs = collect_from_all_sources(limit_per_source=limit_per_source)
    
    if not raw_jobs:
        logger.error("❌ Nenhuma vaga coletada!")
        return []
    
    logger.info(f"✓ {len(raw_jobs)} vagas coletadas")
    
    # Filtra por país/setor/idioma
    logger.info("\n🌍 Filtrando por país, setor, idioma...")
    filtered_jobs = filter_jobs(raw_jobs)
    logger.info(f"✓ {len(filtered_jobs)} vagas após filtros")
    
    if not filtered_jobs:
        logger.error("❌ Nenhuma vaga após filtros!")
        return []
    
    # Resolve links (fonte → site oficial)
    logger.info("\n🔗 Resolvendo links para sites oficiais...")
    resolved_jobs = []
    
    for job in filtered_jobs:
        direct_url, status = resolve_job_link(job)
        
        if direct_url and status in ["direct", "resolved"]:
            job['_direct_url'] = direct_url
            job['_url_status'] = status
            resolved_jobs.append(job)
        else:
            logger.debug(f"❌ Não resolvido: {job['company']} - {job['title']}")
    
    logger.info(f"✓ {len(resolved_jobs)} vagas com links diretos")
    
    if not resolved_jobs:
        logger.error("❌ Nenhuma vaga com link direto!")
        return []
    
    # Salva em cache por 24h
    cache_set("daily_research", resolved_jobs, ttl_hours=24)
    
    return resolved_jobs


def run_daily_analysis(jobs: List[Dict[str, Any]]) -> List[JobAnalysis]:
    """
    FASE 2: Análise com Claude (1 batch call)
    """
    logger.info("="*60)
    logger.info("📊 FASE 2: ANÁLISE COM CLAUDE")
    logger.info("="*60)
    
    if not jobs:
        logger.error("Nenhuma vaga para analisar")
        return []
    
    # Limita a 20 para análise (máximo eficiente por call)
    to_analyze = jobs[:20]
    
    logger.info(f"🤖 Analisando {len(to_analyze)} vagas em 1 batch call...")
    analyzed = batch_analyze_jobs(to_analyze)
    
    logger.info(f"✓ {len(analyzed)} vagas aprovadas após análise")
    
    return analyzed


def run_daily_validation(analyzed_jobs: List[JobAnalysis]) -> List[JobAnalysis]:
    """
    FASE 3: Validação de diversidade
    Garante que as 3 vagas selecionadas têm diversidade.
    """
    logger.info("="*60)
    logger.info("✅ FASE 3: VALIDAÇÃO DE DIVERSIDADE")
    logger.info("="*60)
    
    if len(analyzed_jobs) < 3:
        logger.error(f"❌ Só {len(analyzed_jobs)} vagas aprovadas, precisa de 3 mínimo!")
        logger.warning("   Tentando novamente amanhã...")
        return []
    
    # Tenta diferentes combinações até encontrar 3 com diversidade
    for i in range(min(10, len(analyzed_jobs) - 2)):
        batch = analyzed_jobs[i:i+3]
        
        valid, failing = validate_diversity(batch)
        
        if valid:
            logger.info("\n✅ Batch validado com sucesso!")
            logger.info(print_batch_summary(batch))
            return batch
    
    logger.error("❌ Não conseguiu encontrar 3 vagas com diversidade garantida")
    logger.warning("   Tentando novamente amanhã...")
    
    return []


def post_jobs(jobs: List[JobAnalysis], bot_token: str, chat_id: str) -> int:
    """
    FASE 4: Posting (pode ser chamado até 3x/dia)
    """
    logger.info("="*60)
    logger.info(f"📤 POSTING: {len(jobs)} vaga(s)")
    logger.info("="*60)
    
    posted = 0
    
    for job in jobs:
        # Tenta com clawdbot message (mais simples)
        success = post_via_clawdbot_message(job, channel="telegram")
        
        if not success and bot_token and chat_id:
            # Fallback: API direto
            success = post_to_telegram(job, bot_token, chat_id)
        
        if success:
            posted += 1
    
    return posted


def main():
    parser = argparse.ArgumentParser(description="Job Curator Bot v2.1")
    parser.add_argument("--mode", choices=["research", "analyze", "validate", "post"], 
                       default="full", help="Modo execução")
    parser.add_argument("--dry-run", action="store_true", help="Simula sem postar")
    parser.add_argument("--bot-token", help="Telegram bot token")
    parser.add_argument("--chat-id", help="Telegram chat ID")
    parser.add_argument("--limit", type=int, default=20, help="Vagas por fonte")
    
    args = parser.parse_args()
    
    bot_token = args.bot_token or os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = args.chat_id or os.environ.get("TELEGRAM_CHAT_ID")
    
    logger.info("\n" + "="*60)
    logger.info("🚀 JOB CURATOR BOT v2.1")
    logger.info(f"   Timestamp: {datetime.now()}")
    logger.info("="*60)
    
    # PESQUISA (uma vez por dia, 00:00 UTC)
    logger.info("\n📋 Pesquisa Diária...")
    research_jobs = run_daily_research(limit_per_source=args.limit)
    
    if not research_jobs:
        logger.error("❌ Falha na pesquisa. Abortando.")
        return 1
    
    # ANÁLISE (uma vez por dia, logo após pesquisa)
    logger.info("\n📊 Análise...")
    analyzed_jobs = run_daily_analysis(research_jobs)
    
    if not analyzed_jobs:
        logger.error("❌ Falha na análise. Abortando.")
        return 1
    
    # VALIDAÇÃO (uma vez por dia)
    logger.info("\n✅ Validação...")
    validated_jobs = run_daily_validation(analyzed_jobs)
    
    if not validated_jobs:
        logger.error("❌ Falha na validação. Tentando amanhã.")
        return 1
    
    # POSTING (pode ser 3x/dia)
    if not args.dry_run:
        logger.info("\n📤 Posting...")
        posted = post_jobs(validated_jobs, bot_token, chat_id)
        logger.info(f"✅ {posted}/{len(validated_jobs)} vagas postadas")
    else:
        logger.info("\n[DRY RUN] Vagas prontas para posting:")
        for job in validated_jobs:
            logger.info(f"   • {job.titulo} @ {job.empresa}")
    
    logger.info("\n" + "="*60)
    logger.info("✅ PIPELINE COMPLETO")
    logger.info("="*60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
