#!/usr/bin/env python3
"""
Telegram Poster v2.1 - Posta vagas no Telegram
Formato simples, sem RH jargão.
CRÍTICO: Sempre posta link DIRETO da empresa, nunca agregador.
"""

import logging
import requests
from typing import Optional
from job_analyzer import JobAnalysis

logger = logging.getLogger(__name__)

# Símbolos de moeda
CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "BRL": "R$",
    "CAD": "C$",
    "AUD": "A$",
    "CHF": "CHF",
}


def format_job_message(job: JobAnalysis) -> str:
    """
    Formata vaga para Telegram.
    
    Formato:
    🎯 [TÍTULO]
    
    [EMPRESA]
    📍 [PAÍS/REMOTO]
    💰 [MOEDA] $[SALÁRIO]/mês
    
    ✓ [Descrição 1 linha]
    
    Requisitos:
    • Inglês: [...]
    • Faculdade: [...]
    • Experiência: [...]
    
    APLICAR: [LINK DIRETO]
    """
    
    symbol = CURRENCY_SYMBOLS.get(job.moeda, "$")
    
    # Formata salário com separador
    salario_fmt = f"{job.salario_usd_mes:,}".replace(",", ".")
    
    message = f"""🎯 {job.titulo}

{job.empresa}
📍 {job.pais_ou_remoto}
💰 {job.moeda} {symbol}{salario_fmt}/mês

✓ {job.descricao_curta}

Requisitos:
• Inglês: {job.nivel_ingles}
• Faculdade: {job.texto_faculdade}
• Experiência: {job.texto_experiencia}

APLICAR: {job.direct_url}"""
    
    return message


def post_to_telegram(
    job: JobAnalysis,
    bot_token: str,
    chat_id: str
) -> bool:
    """
    Posta vaga no Telegram via API.
    CRÍTICO: job.direct_url DEVE ser link direto (não agregador).
    """
    
    # Validação: DEVE ter link direto
    if not job.direct_url:
        logger.error(f"❌ Bloqueado: {job.titulo} - sem link direto")
        return False
    
    # Validação: não pode ser agregador
    aggregators = ["linkedin", "indeed", "glassdoor", "weworkremotely", "remoteok"]
    if any(agg in job.direct_url.lower() for agg in aggregators):
        logger.error(f"❌ Bloqueado: {job.titulo} - link é agregador ({job.direct_url})")
        return False
    
    message = format_job_message(job)
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if result.get("ok"):
            logger.info(f"✅ Postado: {job.titulo} @ {job.empresa}")
            logger.info(f"   Link: {job.direct_url}")
            return True
        else:
            logger.error(f"Telegram error: {result}")
            return False
            
    except requests.RequestException as e:
        logger.error(f"Erro postando: {e}")
        return False


def post_via_telegram_api(
    job: JobAnalysis,
    bot_token: str,
    chat_id: str
) -> bool:
    """
    Posta direto na Telegram API (método que funcionava antes).
    """
    if not job.direct_url:
        logger.error(f"❌ Sem link direto: {job.titulo}")
        return False
    
    message = format_job_message(job)
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        response = requests.post(
            url,
            json={
                "chat_id": int(chat_id),
                "text": message,
                "disable_web_page_preview": True,
            },
            timeout=30
        )
        
        if response.ok:
            logger.info(f"✅ Postado: {job.titulo}")
            return True
        else:
            logger.error(f"Telegram erro: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Erro postando: {e}")
        return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Teste
    test_job = JobAnalysis(
        titulo="Software Engineer",
        empresa="Google",
        pais_ou_remoto="Remoto Global",
        salario_usd_mes=8000,
        moeda="USD",
        descricao_curta="Desenvolver APIs com Python para plataforma de pagamentos",
        nivel_ingles="Fluente",
        texto_faculdade="Sim",
        texto_experiencia="3+ anos",
        url_origem="https://weworkremotely.com/...",
        direct_url="https://google.com/careers/...",
        aprovada=True,
    )
    
    print("\n=== PREVIEW TELEGRAM ===\n")
    print(format_job_message(test_job))
    print("\n" + "="*50)
