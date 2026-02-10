#!/usr/bin/env python3
"""
Job Sources v2.1 - Coleta de MÚLTIPLAS FONTES
IMPORTANTE: Links das fontes são APENAS para pesquisa.
Nunca são postados. Links postados são SEMPRE do site oficial da empresa.
"""

import requests
import logging
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# Válidos: Europa, Austrália, EUA, Canadá
ALLOWED_COUNTRIES = {
    # Europa
    "germany", "germany ", "alemanha", "de", "berlin", "münchen",
    "france", "france ", "franca", "fr", "paris",
    "netherlands", "netherlands ", "holanda", "nl", "amsterdam",
    "portugal", "portugal ", "portugal", "pt", "lisbon", "lisboa",
    "uk", "united kingdom", "england", "londres", "london",
    "italy", "italy ", "italia", "italia", "it", "roma", "rome",
    "spain", "spain ", "españa", "es", "madrid", "barcelona",
    "sweden", "sweden ", "suecia", "se", "stockholm",
    "norway", "norway ", "noruega", "no", "oslo",
    "denmark", "denmark ", "dinamarca", "dk", "copenhagen",
    "switzerland", "switzerland ", "suiza", "ch", "zurich",
    "austria", "austria ", "austria", "at", "vienna",
    "belgium", "belgium ", "belgica", "be", "brussels",
    # Austrália
    "australia", "australia ", "australasia", "au", "sydney", "melbourne",
    # EUA
    "usa", "united states", "us", "america", "eua", "estados unidos",
    "new york", "california", "texas", "florida", "washington",
    # Canadá
    "canada", "canada ", "canadian", "ca", "toronto", "vancouver", "montreal",
    # Remoto
    "remote", "remoto", "global", "worldwide", "international"
}

BLOCKED_COUNTRIES = {
    "brasil", "brazil", "br",
    "mexico", "méxico", "mx",
    "argentina", "ar",
    "colombia", "colômbia", "co",
    "chile", "cl",
    "venezuela", "ve",
    "india", "índia", "in",
    "philippines", "filipinas", "ph",
    "pakistan", "paquistão", "pk",
    "bangladesh", "bangladesh", "bd",
    "sri lanka", "srilanka",
}

# Setores para categorização
SECTORS = {
    "technology": ["software", "engineer", "developer", "devops", "data", "ai", "ml", "cloud", "fullstack", "frontend", "backend"],
    "design": ["designer", "ux", "ui", "product design", "graphic"],
    "business": ["manager", "analyst", "account", "sales", "marketing", "business"],
    "healthcare": ["nurse", "doctor", "medical", "health", "therapist", "psychiatrist"],
    "education": ["teacher", "tutor", "instructor", "professor", "educator"],
    "creative": ["writer", "editor", "content", "video", "photographer", "artist"],
    "finance": ["accountant", "finance", "cfo", "controller", "bookkeeper"],
}


class JobSource:
    """Base para todas as fontes"""
    name: str = "base"
    
    def fetch_jobs(self, limit: int = 20) -> List[Dict[str, Any]]:
        raise NotImplementedError


class GoogleJobsSource(JobSource):
    """
    Google Jobs - busca via web scraping
    NOTA: Links são do Google Jobs (agregador). Usamos só para achar empresa+cargo.
    """
    name = "google_jobs"
    
    def fetch_jobs(self, limit: int = 20) -> List[Dict[str, Any]]:
        try:
            # Busca remoto
            response = requests.get(
                "https://www.google.com/search",
                params={
                    "q": "remote jobs site:google.com/jobs OR site:linkedin.com/jobs",
                    "tbm": "lcm",  # Local/Jobs
                    "filter": "1"
                },
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )
            
            # Fallback: usar busca genérica
            jobs = self._parse_google_jobs(response.text)
            return jobs[:limit]
        except Exception as e:
            logger.debug(f"Google Jobs erro: {e}")
            return []
    
    def _parse_google_jobs(self, html: str) -> List[Dict[str, Any]]:
        """Parse simplificado de resultados"""
        results = []
        # Implementação básica - em produção usaria Selenium
        return results


class LinkedInSource(JobSource):
    """
    LinkedIn Jobs - scraping com BeautifulSoup
    NOTA: Links são do LinkedIn. Usamos só para achar empresa+cargo.
    """
    name = "linkedin"
    
    def fetch_jobs(self, limit: int = 20) -> List[Dict[str, Any]]:
        try:
            jobs = []
            
            # Busca múltiplas keywords para variar setores
            keywords = [
                "Software Engineer Remote",
                "Product Designer Remote",
                "Project Manager Remote",
                "Data Analyst Remote",
                "Business Analyst Remote",
            ]
            
            for keyword in keywords[:5]:
                try:
                    response = requests.get(
                        "https://www.linkedin.com/jobs/search/",
                        params={
                            "keywords": keyword,
                            "location": "Remote",
                            "distance": "any",
                            "f_TP": ["1", "2", "3", "4"],  # Employment types
                        },
                        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
                        timeout=15
                    )
                    
                    # Parse HTML
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Busca job cards
                    job_cards = soup.find_all('div', class_='base-card')[:limit//len(keywords) + 1]
                    
                    for card in job_cards:
                        try:
                            title_elem = card.find('h3', class_='base-search-card__title')
                            company_elem = card.find('h4', class_='base-search-card__subtitle')
                            location_elem = card.find('span', class_='job-search-card__location')
                            link_elem = card.find('a', class_='base-card__full-link')
                            
                            if not (title_elem and company_elem):
                                continue
                            
                            jobs.append({
                                "source": self.name,
                                "source_url": link_elem.get('href', '') if link_elem else "",
                                "title": title_elem.text.strip(),
                                "company": company_elem.text.strip(),
                                "location": location_elem.text.strip() if location_elem else "Remote",
                                "description": "",
                                "salary_min": None,
                                "salary_max": None,
                            })
                        except:
                            continue
                            
                except Exception as e:
                    logger.debug(f"LinkedIn keyword '{keyword}' erro: {e}")
                    continue
            
            return jobs[:limit]
            
        except Exception as e:
            logger.debug(f"LinkedIn fonte erro: {e}")
            return []


class IndeedSource(JobSource):
    """
    Indeed - scraping
    NOTA: Links são do Indeed (agregador). Usamos só para empresa+cargo.
    """
    name = "indeed"
    
    def fetch_jobs(self, limit: int = 20) -> List[Dict[str, Any]]:
        try:
            jobs = []
            
            keywords = [
                "software engineer remote",
                "designer remote",
                "manager remote",
                "analyst remote",
            ]
            
            for keyword in keywords[:4]:
                try:
                    response = requests.get(
                        "https://www.indeed.com/jobs",
                        params={
                            "q": keyword,
                            "l": "Remote",
                            "jt": "fulltime",
                        },
                        headers={"User-Agent": "Mozilla/5.0"},
                        timeout=15
                    )
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Indeed job divs
                    job_cards = soup.find_all('div', class_='job_seen_beacon')[:limit//len(keywords) + 1]
                    
                    for card in job_cards:
                        try:
                            title_elem = card.find('h2', class_='jobTitle')
                            company_elem = card.find('span', {'data-testid': 'company-name'})
                            location_elem = card.find('div', class_='companyLocation')
                            
                            if not (title_elem and company_elem):
                                continue
                            
                            # Extract text properly
                            title_text = title_elem.text.strip() if title_elem else ""
                            company_text = company_elem.text.strip() if company_elem else ""
                            location_text = location_elem.text.strip() if location_elem else ""
                            
                            jobs.append({
                                "source": self.name,
                                "source_url": card.find('a').get('href', '') if card.find('a') else "",
                                "title": title_text,
                                "company": company_text,
                                "location": location_text,
                                "description": "",
                                "salary_min": None,
                                "salary_max": None,
                            })
                        except:
                            continue
                            
                except Exception as e:
                    logger.debug(f"Indeed keyword '{keyword}' erro: {e}")
                    continue
            
            return jobs[:limit]
            
        except Exception as e:
            logger.debug(f"Indeed fonte erro: {e}")
            return []


class WeWorkRemotelySource(JobSource):
    """
    We Work Remotely - API simples
    NOTA: Links são do WWR. Usamos só para empresa+cargo.
    """
    name = "weworkremotely"
    
    def fetch_jobs(self, limit: int = 20) -> List[Dict[str, Any]]:
        try:
            response = requests.get(
                "https://weworkremotely.com/remote-jobs.json",
                timeout=15
            )
            data = response.json()
            
            jobs = []
            for job in data.get('remote_jobs', [])[:limit]:
                jobs.append({
                    "source": self.name,
                    "source_url": job.get('url', ''),
                    "title": job.get('title', ''),
                    "company": job.get('company_name', ''),
                    "location": job.get('location', 'Remote'),
                    "description": job.get('description', ''),
                    "salary_min": None,
                    "salary_max": None,
                })
            
            return jobs
            
        except Exception as e:
            logger.debug(f"We Work Remotely erro: {e}")
            return []


class RemoteOKSource(JobSource):
    """
    RemoteOK - Scraping simples
    NOTA: Links são do RemoteOK. Usamos só para empresa+cargo.
    """
    name = "remoteok"
    
    def fetch_jobs(self, limit: int = 20) -> List[Dict[str, Any]]:
        try:
            response = requests.get(
                "https://remoteok.com",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            jobs = []
            job_rows = soup.find_all('tr', class_='job')[:limit]
            
            for row in job_rows:
                try:
                    job_elem = row.find('a', class_='job-title-link')
                    company_elem = row.find('h3')
                    
                    if not job_elem:
                        continue
                    
                    title = job_elem.text.strip()
                    company = company_elem.text.strip() if company_elem else ""
                    link = job_elem.get('href', '')
                    
                    jobs.append({
                        "source": self.name,
                        "source_url": link,
                        "title": title,
                        "company": company,
                        "location": "Remote",
                        "description": "",
                        "salary_min": None,
                        "salary_max": None,
                    })
                except:
                    continue
            
            return jobs
            
        except Exception as e:
            logger.debug(f"RemoteOK erro: {e}")
            return []


def collect_from_all_sources(limit_per_source: int = 15) -> List[Dict[str, Any]]:
    """
    Coleta vagas de TODAS as fontes (Google, LinkedIn, Indeed, WWR, RemoteOK).
    
    ⚠️ IMPORTANTE:
    - source_url = link da FONTE (agregador) - NUNCA será postado
    - company + title = usados para resolver para site oficial da empresa
    
    Returns:
        Lista de vagas brutas com source_url (ainda NÃO é link de posting)
    """
    sources = [
        WeWorkRemotelySource(),
        RemoteOKSource(),
        IndeedSource(),
        LinkedInSource(),
        # GoogleJobsSource(),  # TODO: Implementar scraping melhor
    ]
    
    all_jobs = []
    
    for source in sources:
        logger.info(f"🔍 Buscando em {source.name}...")
        try:
            jobs = source.fetch_jobs(limit=limit_per_source)
            logger.info(f"   ✓ {len(jobs)} vagas encontradas")
            all_jobs.extend(jobs)
        except Exception as e:
            logger.warning(f"   ✗ Erro: {e}")
            continue
    
    # Deduplica por (title, company)
    seen = set()
    unique_jobs = []
    
    for job in all_jobs:
        key = f"{job['title'].lower()}|{job['company'].lower()}"
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)
    
    logger.info(f"📊 Total: {len(unique_jobs)} vagas únicas de {len(all_jobs)} coletadas")
    
    return unique_jobs


def categorize_sector(title: str, description: str = "") -> str:
    """Categoriza setor baseado em título/descrição"""
    combined = (title + " " + description).lower()
    
    for sector, keywords in SECTORS.items():
        if any(kw in combined for kw in keywords):
            return sector
    
    return "technology"  # Default


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    jobs = collect_from_all_sources(limit_per_source=10)
    
    print(f"\n=== {len(jobs)} vagas coletadas ===\n")
    
    for i, job in enumerate(jobs[:5], 1):
        print(f"{i}. [{job['source'].upper()}]")
        print(f"   Título: {job['title']}")
        print(f"   Empresa: {job['company']}")
        print(f"   Local: {job['location']}")
        print(f"   Setor: {categorize_sector(job['title'])}")
        print(f"   ℹ️ Fonte (não postar): {job['source_url'][:50]}...")
        print()
