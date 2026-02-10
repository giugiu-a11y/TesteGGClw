#!/usr/bin/env python3
"""
Job Sources v2.2 - 100% FREE (sem APIs pagas)
RSS feeds + Scraping leve + APIs públicas grátis
"""

import requests
import logging
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from datetime import datetime
from bs4 import BeautifulSoup
import time

logger = logging.getLogger(__name__)

# Request headers para não ser bloqueado
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


class JobSource:
    name: str = "base"
    
    def fetch_jobs(self, limit: int = 20) -> List[Dict[str, Any]]:
        raise NotImplementedError


class WeWorkRemotelyRSS(JobSource):
    """
    We Work Remotely RSS Feed - GRÁTIS, rápido, sem limite
    """
    name = "weworkremotely_rss"
    
    def fetch_jobs(self, limit: int = 20) -> List[Dict[str, Any]]:
        try:
            response = requests.get(
                "https://weworkremotely.com/remote-jobs.rss",
                headers=HEADERS,
                timeout=10
            )
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            jobs = []
            
            # Parse RSS
            for item in root.findall(".//item")[:limit]:
                try:
                    title = item.find("title")
                    link = item.find("link")
                    description = item.find("description")
                    
                    # WWR format: "Company: Position"
                    title_text = title.text if title is not None else ""
                    company = ""
                    position = title_text
                    
                    if ":" in title_text:
                        parts = title_text.split(":", 1)
                        company = parts[0].strip()
                        position = parts[1].strip()
                    
                    jobs.append({
                        "source": self.name,
                        "source_url": link.text if link is not None else "",
                        "title": position,
                        "company": company,
                        "description": description.text if description is not None else "",
                        "location": "Remote",
                    })
                except:
                    continue
            
            logger.info(f"  ✓ {len(jobs)} vagas via RSS")
            return jobs
            
        except Exception as e:
            logger.warning(f"  ✗ RSS erro: {e}")
            return []


class RemoteOKRSS(JobSource):
    """
    RemoteOK RSS Feed - GRÁTIS, rápido
    """
    name = "remoteok_rss"
    
    def fetch_jobs(self, limit: int = 20) -> List[Dict[str, Any]]:
        try:
            response = requests.get(
                "https://remoteok.com/feed.rss",
                headers=HEADERS,
                timeout=10
            )
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            jobs = []
            
            for item in root.findall(".//item")[:limit]:
                try:
                    title = item.find("title")
                    link = item.find("link")
                    description = item.find("description")
                    
                    jobs.append({
                        "source": self.name,
                        "source_url": link.text if link is not None else "",
                        "title": title.text if title is not None else "",
                        "company": "Unknown",  # RemoteOK não inclui no RSS
                        "description": description.text if description is not None else "",
                        "location": "Remote",
                    })
                except:
                    continue
            
            logger.info(f"  ✓ {len(jobs)} vagas via RSS")
            return jobs
            
        except Exception as e:
            logger.warning(f"  ✗ RSS erro: {e}")
            return []


class RemotiveAPI(JobSource):
    """
    Remotive API Pública - GRÁTIS
    """
    name = "remotive_api"

    def fetch_jobs(self, limit: int = 20) -> List[Dict[str, Any]]:
        try:
            response = requests.get(
                "https://remotive.com/api/remote-jobs",
                headers=HEADERS,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            jobs = []
            for item in data.get("jobs", [])[:limit]:
                jobs.append({
                    "source": self.name,
                    "source_url": item.get("url", ""),
                    "title": item.get("title", ""),
                    "company": item.get("company_name", ""),
                    "description": item.get("description", "") or "",
                    "location": item.get("candidate_required_location", "Remote"),
                })
            logger.info(f"  ✓ {len(jobs)} vagas via Remotive API")
            return jobs
        except Exception as e:
            logger.warning(f"  ✗ Remotive API erro: {e}")
            return []


class GreenhousePublicAPI(JobSource):
    """
    Greenhouse API Pública - GRÁTIS para vagas públicas
    Busca de empresas conhecidas com boards públicos
    """
    name = "greenhouse_public"
    
    # Top 30 empresas com Greenhouse boards públicos
    COMPANIES = [
        "gitlab", "zapier", "notion", "figma", "vercel", "stripe",
        "hashicorp", "twilio", "cloudflare", "mongodb", "elastic",
        "netlify", "dbt-labs", "airbyte", "okta", "guidepoint",
        "mailchimp", "hubspot", "redfin", "gusto", "flexport",
        "carta", "airtable", "asana", "calendly", "deel",
        "getdbt", "anthropic", "openai", "deepmind", "databricks"
    ]
    
    def fetch_jobs(self, limit: int = 20) -> List[Dict[str, Any]]:
        jobs = []
        jobs_per_company = max(1, limit // 10)  # Distribui entre 10 empresas
        
        for company in self.COMPANIES[:10]:  # Limita a 10 para não demorar
            try:
                # Greenhouse API pública
                response = requests.get(
                    f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true",
                    timeout=10
                )
                response.raise_for_status()
                
                data = response.json()
                
                for job in data.get("jobs", [])[:jobs_per_company]:
                    job_id = job.get("id")
                    direct_url = f"https://boards.greenhouse.io/{company}/jobs/{job_id}"
                    
                    jobs.append({
                        "source": f"{self.name}:{company}",
                        "source_url": direct_url,  # JÁ é direto!
                        "title": job.get("title", ""),
                        "company": job.get("company_name", company.title()),
                        "description": job.get("content", "")[:1000],
                        "location": self._extract_location(job),
                    })
                
                time.sleep(0.2)  # Rate limiting amigável
                
            except Exception as e:
                logger.debug(f"  Greenhouse {company}: {e}")
                continue
        
        logger.info(f"  ✓ {len(jobs)} vagas via Greenhouse API")
        return jobs
    
    def _extract_location(self, job):
        location = job.get("location", {})
        if isinstance(location, dict):
            return location.get("name", "Remote")
        return str(location) if location else "Remote"


class LeverPublicAPI(JobSource):
    """
    Lever API Pública - GRÁTIS
    """
    name = "lever_public"
    
    COMPANIES = [
        "netflix", "spotify", "discord", "webflow", "linear",
        "tailscale", "glitch", "figma", "replit", "notion"
    ]
    
    def fetch_jobs(self, limit: int = 20) -> List[Dict[str, Any]]:
        jobs = []
        jobs_per_company = max(1, limit // len(self.COMPANIES))
        
        for company in self.COMPANIES[:8]:
            try:
                response = requests.get(
                    f"https://api.lever.co/v0/postings/{company}?mode=json",
                    timeout=10
                )
                response.raise_for_status()
                
                company_jobs = response.json()
                
                for job in company_jobs[:jobs_per_company]:
                    direct_url = job.get("hostedUrl", "")
                    
                    jobs.append({
                        "source": f"{self.name}:{company}",
                        "source_url": direct_url,  # JÁ é direto!
                        "title": job.get("text", ""),
                        "company": company.title(),
                        "description": job.get("descriptionPlain", "")[:1000],
                        "location": job.get("workplaceType", "Remote"),
                    })
                
                time.sleep(0.2)
                
            except Exception as e:
                logger.debug(f"  Lever {company}: {e}")
                continue
        
        logger.info(f"  ✓ {len(jobs)} vagas via Lever API")
        return jobs


class HiringNowScraper(JobSource):
    """
    Scraping ultra-leve de hiring.com (público, sem JavaScript)
    """
    name = "hiring_now"
    
    def fetch_jobs(self, limit: int = 20) -> List[Dict[str, Any]]:
        try:
            # Hiring Now agregador (é público)
            response = requests.get(
                "https://www.hiring.com/search?q=remote",
                headers=HEADERS,
                timeout=15
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs = []
            
            # Busca job cards (estrutura pode variar)
            job_cards = soup.find_all('div', class_='job-card')[:limit]
            
            for card in job_cards:
                try:
                    title_elem = card.find('h2')
                    company_elem = card.find('span', class_='company-name')
                    location_elem = card.find('span', class_='location')
                    link_elem = card.find('a')
                    
                    if title_elem and link_elem:
                        jobs.append({
                            "source": self.name,
                            "source_url": link_elem.get('href', ''),
                            "title": title_elem.text.strip(),
                            "company": company_elem.text.strip() if company_elem else "Unknown",
                            "description": "",
                            "location": location_elem.text.strip() if location_elem else "Remote",
                        })
                except:
                    continue
            
            logger.info(f"  ✓ {len(jobs)} vagas via scraping")
            return jobs
            
        except Exception as e:
            logger.warning(f"  ✗ Scraping erro: {e}")
            return []


def collect_from_free_sources(limit_per_source: int = 15) -> List[Dict[str, Any]]:
    """
    Coleta vagas de FONTES 100% GRÁTIS.
    
    Estratégia (CORRIGIDA 29 JAN 2026):
    - RSS feeds (WWR, RemoteOK) — achamos empresa+cargo
    - Scraping leve — achamos empresa+cargo
    - DEPOIS: resolver para site oficial (não postar Greenhouse/Lever direto)
    
    APIs Greenhouse/Lever SÓ como referência, depois resolver para oficial.
    """
    
    sources = [
        # RSS feeds — achamos vagas + empresa (depois resolvemos link)
        WeWorkRemotelyRSS(),
        # RemoteOKRSS(),  # 403 recorrente; manter desativado para reduzir custo/tempo
        RemotiveAPI(),
        # APIs públicas (USAR SÓ COMO REFERÊNCIA, depois resolver para oficial)
        # GreenhousePublicAPI(),  # Remover — todos links ficam greenhouse.io
        # LeverPublicAPI(),       # Remover — todos links ficam lever.co
    ]
    
    all_jobs = []
    
    logger.info("🔍 Coletando vagas de FONTES GRÁTIS...")
    
    for source in sources:
        try:
            logger.info(f"  {source.name}...")
            jobs = source.fetch_jobs(limit=limit_per_source)
            all_jobs.extend(jobs)
            time.sleep(0.5)  # Rate limiting amigável
        except Exception as e:
            logger.warning(f"  Erro: {e}")
            continue
    
    # Deduplica
    seen = set()
    unique_jobs = []
    
    for job in all_jobs:
        key = f"{job['title'].lower()}|{job['company'].lower()}"
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)
    
    logger.info(f"📊 Total: {len(unique_jobs)} vagas únicas de {len(all_jobs)} coletadas\n")
    
    return unique_jobs


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    start = time.time()
    jobs = collect_from_free_sources(limit_per_source=10)
    elapsed = time.time() - start
    
    print(f"\n=== {len(jobs)} vagas em {elapsed:.1f}s ===\n")
    
    for i, job in enumerate(jobs[:5], 1):
        print(f"{i}. {job['title']}")
        print(f"   {job['company']} | {job['location']}")
        print(f"   Fonte: {job['source']}")
        print()
    
    print(f"⏱ Tempo total: {elapsed:.1f}s")
    print(f"💰 Custo: $0 (totalmente grátis)")
