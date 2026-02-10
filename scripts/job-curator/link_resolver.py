#!/usr/bin/env python3
"""
Link Resolver v2.1 - Resolve links de FONTE para SITE OFICIAL da empresa
CRÍTICO: Nunca posta link de agregador. SEMPRE site oficial.
"""

import requests
import logging
import re
from typing import Optional, Tuple
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

# Mapeamento de empresas para URLs de carreira
COMPANY_CAREER_PAGES = {
    "google": "https://www.google.com/careers",
    "amazon": "https://www.amazon.com/jobs",
    "microsoft": "https://careers.microsoft.com",
    "apple": "https://www.apple.com/jobs",
    "netflix": "https://jobs.netflix.com",
    "spotify": "https://www.spotifyjobs.com",
    "discord": "https://discord.com/jobs",
    "stripe": "https://stripe.com/jobs",
    "figma": "https://www.figma.com/careers",
    "notion": "https://www.notion.so/careers",
    "zapier": "https://zapier.com/jobs",
    "vercel": "https://vercel.com/careers",
    "gitlab": "https://about.gitlab.com/jobs",
    "netlify": "https://www.netlify.com/careers",
    "twilio": "https://www.twilio.com/en-us/careers",
    "slack": "https://slack.com/careers",
    "intercom": "https://www.intercom.com/careers",
    "segment": "https://segment.com/careers",
    "datadog": "https://careers.datadoghq.com",
    "cloudflare": "https://www.cloudflare.com/careers",
    "mongodb": "https://www.mongodb.com/careers",
    "elasticsearch": "https://www.elastic.co/careers",
    "hashicorp": "https://www.hashicorp.com/careers",
    "okta": "https://www.okta.com/careers",
    "auth0": "https://auth0.com/careers",
    "crowdstrike": "https://www.crowdstrike.com/careers",
    "databox": "https://careers.databox.com",
    "mailchimp": "https://mailchimp.com/careers",
    "hubspot": "https://www.hubspot.com/careers",
    "salesforce": "https://www.salesforce.com/careers",
    "uber": "https://www.uber.com/careers",
    "airbnb": "https://www.airbnb.com/careers",
    "etsy": "https://www.etsy.com/careers",
    "shopify": "https://www.shopify.com/careers",
    "wix": "https://www.wix.com/en/careers",
    "squarespace": "https://www.squarespace.com/careers",
    "flickr": "https://www.flickr.com/jobs",
    "pixar": "https://www.pixar.com/careers",
    "disney": "https://jobs.disneycareers.com",
    "netflix": "https://jobs.netflix.com",
    "hulu": "https://www.hulu.com/careers",
    "warner": "https://www.warnerbros.com/careers",
    "sony": "https://www.sony.com/en_US/SCA/company-news/careers",
    "ibm": "https://www.ibm.com/careers",
    "intel": "https://www.intel.com/content/www/us/en/careers/careers-home.html",
    "qualcomm": "https://www.qualcomm.com/careers",
    "amd": "https://jobs.amd.com",
    "nvidia": "https://www.nvidia.com/en-us/about-nvidia/careers",
    "tesla": "https://www.tesla.com/careers",
    "spacex": "https://www.spacex.com/careers",
    "airbnb": "https://www.airbnb.com/careers",
    "lyft": "https://www.lyft.com/careers",
    "doordash": "https://www.doordash.com/careers",
    "instacart": "https://careers.instacart.com",
    # Adicionar mais conforme necessário
}

# Agregadores CONHECIDOS (NUNCA postar estes links)
AGGREGATORS = {
    "linkedin", "indeed", "glassdoor", "monster", "careerbuilder",
    "weworkremotely", "remoteok", "himalayas", "workingnomads",
    "flexjobs", "virtualvocations", "jobspresso", "angel.co",
    "dribbble", "behance", "producthunt", "y-combinator",
}


def is_aggregator_url(url: str) -> bool:
    """Verifica se URL é de um agregador"""
    domain = urlparse(url).netloc.lower()
    
    for agg in AGGREGATORS:
        if agg in domain:
            return True
    
    return False


def normalize_company_name(name: str) -> str:
    """Normaliza nome da empresa para busca"""
    return (
        name.lower()
        .replace("inc.", "")
        .replace("ltd.", "")
        .replace("llc", "")
        .replace("gmbh", "")
        .replace("sarl", "")
        .strip()
    )


def find_company_careers_page(company: str) -> Optional[str]:
    """
    Busca página de carreiras da empresa.
    Tenta: mapeamento pré-definido > busca no site > domain padrão
    """
    company_norm = normalize_company_name(company)
    
    # 1. Tenta mapeamento direto
    if company_norm in COMPANY_CAREER_PAGES:
        return COMPANY_CAREER_PAGES[company_norm]
    
    # 2. Tenta domain padrão (company.com/careers ou company.jobs)
    domain = company_norm.replace(" ", "")
    
    candidates = [
        f"https://{domain}.com/careers",
        f"https://{domain}.jobs",
        f"https://www.{domain}.com/careers",
        f"https://www.{domain}.jobs",
        f"https://careers.{domain}.com",
        f"https://jobs.{domain}.com",
    ]
    
    for url in candidates:
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            if response.status_code < 400:
                logger.debug(f"✓ Encontrado: {url}")
                return url
        except:
            pass
    
    return None


def search_job_on_company_site(company_careers_url: str, title: str) -> Optional[str]:
    """
    Busca vaga específica no site de carreiras da empresa.
    Estratégia:
    1. Tenta /search?q=
    2. Tenta /jobs?q=
    3. Retorna a URL base (usuário encontrará)
    """
    if not company_careers_url:
        return None
    
    # Limpa título para busca
    title_search = title.lower().replace(" ", "+")
    
    candidates = [
        f"{company_careers_url}/search?q={title_search}",
        f"{company_careers_url}/jobs?search={title_search}",
        f"{company_careers_url}/search?query={title_search}",
    ]
    
    for url in candidates:
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            if response.status_code < 400:
                logger.debug(f"✓ Vaga encontrada: {url}")
                return url
        except:
            pass
    
    # Se não achar, retorna página base de carreiras
    # (usuário pode encontrar manualmente)
    logger.debug(f"Retornando base: {company_careers_url}")
    return company_careers_url


def resolve_job_link(job: dict) -> Tuple[Optional[str], str]:
    """
    Resolve link de fonte agregadora para site oficial da empresa.
    
    Args:
        job: Dict com 'company' e 'source_url'
    
    Returns:
        (url_direto, status: "direct"|"resolved"|"failed")
    """
    company = job.get('company', '')
    source_url = job.get('source_url', '')
    title = job.get('title', '')
    
    # Se source_url JÁ é direto (não agregador), usa ele
    if source_url and not is_aggregator_url(source_url):
        logger.debug(f"✓ Link já é direto: {source_url}")
        return source_url, "direct"
    
    # Tenta encontrar site oficial da empresa
    careers_page = find_company_careers_page(company)
    
    if not careers_page:
        logger.warning(f"✗ Não encontrou site de carreiras para {company}")
        return None, "failed"
    
    # Tenta buscar vaga específica
    job_url = search_job_on_company_site(careers_page, title)
    
    if job_url:
        logger.info(f"✓ Resolvido para: {job_url}")
        return job_url, "resolved"
    
    logger.warning(f"✗ Não encontrou vaga no site de {company}")
    return None, "failed"


def validate_direct_url(url: str) -> bool:
    """
    Valida que URL é direto (não agregador).
    """
    if not url:
        return False
    
    # Rejeita agregadores
    if is_aggregator_url(url):
        logger.warning(f"✗ URL ainda é agregador: {url}")
        return False
    
    # Tenta acessar (opcional - pode ser custoso)
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        if response.status_code < 400:
            return True
    except:
        pass
    
    # Mesmo sem validação HTTP, se é um domínio válido é OK
    domain = urlparse(url).netloc
    if "." in domain and len(domain) > 4:
        return True
    
    return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    # Testes
    test_jobs = [
        {
            "company": "Google",
            "title": "Software Engineer",
            "source_url": "https://weworkremotely.com/jobs/123",
        },
        {
            "company": "Netflix",
            "title": "Product Designer",
            "source_url": "https://linkedin.com/jobs/456",
        },
        {
            "company": "Unknown Corp",
            "title": "Manager",
            "source_url": "https://indeed.com/jobs/789",
        },
    ]
    
    print("\n=== TESTE: Resolver Links ===\n")
    
    for job in test_jobs:
        direct_url, status = resolve_job_link(job)
        print(f"📌 {job['company']} - {job['title']}")
        print(f"   Fonte: {job['source_url']}")
        print(f"   Resolvido: {direct_url}")
        print(f"   Status: {status}")
        print()
