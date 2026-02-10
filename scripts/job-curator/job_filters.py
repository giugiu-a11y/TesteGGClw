#!/usr/bin/env python3
"""
Job Filters v2.1 - Filtros por País, Setor, Idioma
ZERO LLM - Tudo é regex/lógica booleana
"""

import logging
import re
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Países PERMITIDOS (Europa, Austrália, EUA, Canadá)
ALLOWED_COUNTRIES = {
    # Europa
    "germany", "deutschland", "de", "alemanha",
    "france", "franca", "fr",
    "netherlands", "holanda", "nl",
    "portugal", "pt",
    "uk", "united kingdom", "england", "inglaterra", "gb",
    "italy", "italia", "it",
    "spain", "españa", "es",
    "sweden", "suecia", "se",
    "norway", "noruega", "no",
    "denmark", "dinamarca", "dk",
    "switzerland", "suiza", "ch",
    "austria", "at",
    "belgium", "belgica", "be",
    # Austrália
    "australia", "au",
    # EUA
    "usa", "united states", "us", "america", "eua", "estados unidos",
    "new york", "california", "texas", "florida", "washington",
    # Canadá
    "canada", "ca",
    # Remoto (aceita se global/internacional)
    "remote", "remoto", "global", "worldwide", "international",
}

# Países BLOQUEADOS (LATAM, Ásia, etc)
BLOCKED_COUNTRIES = {
    # Brasil/LATAM
    "brasil", "brazil", "br",
    "mexico", "méxico", "mx",
    "argentina", "ar",
    "colombia", "colômbia", "co",
    "chile", "cl",
    "venezuela", "ve",
    "peru", "pe",
    "ecuador", "ec",
    "paraguay", "py",
    "uruguay", "uy",
    # Ásia (bloqueada)
    "india", "índia", "in",
    "philippines", "filipinas", "ph",
    "pakistan", "paquistão", "pk",
    "bangladesh", "bangladesh", "bd",
    "sri lanka", "srilanka",
    "vietnam", "vietnã", "vn",
    "china", "cn",
    "singapore", "sg",
    "malaysia", "malásia", "my",
    "thailand", "tailândia", "th",
    "indonesia", "indonésia", "id",
    # Middle East
    "saudi", "uae", "united arab emirates", "dubai", "qatar",
}

# Setores para categorização
SECTORS = {
    "technology": [
        "software", "engineer", "developer", "devops", "data", "ai", "ml",
        "cloud", "fullstack", "frontend", "backend", "python", "javascript",
        "react", "node", "java", "golang", "rust", "platform", "infra",
        "sre", "qa", "test", "automation", "cybersecurity", "security"
    ],
    "design": [
        "designer", "ux", "ui", "product design", "graphic", "visual",
        "web design", "interaction", "prototyping", "figma"
    ],
    "business": [
        "manager", "analyst", "account", "sales", "marketing", "business",
        "operations", "project", "scrum", "agile", "consulting", "strategy",
        "growth", "product manager"
    ],
    "healthcare": [
        "nurse", "doctor", "medical", "health", "therapist", "psychiatrist",
        "physician", "cardiologist", "dentist", "veterinarian", "pharmacist",
        "midwife", "counselor", "mental health", "clinical"
    ],
    "education": [
        "teacher", "tutor", "instructor", "professor", "educator",
        "trainer", "coach", "curriculum", "academic"
    ],
    "creative": [
        "writer", "editor", "content", "video", "photographer", "artist",
        "creative", "copywriter", "storytelling", "animator", "illustrator"
    ],
    "finance": [
        "accountant", "finance", "cfo", "controller", "bookkeeper",
        "financial analyst", "auditor", "tax", "payroll", "treasurer"
    ],
}


def normalize_text(text: str) -> str:
    """Normaliza texto para busca (lowercase, sem acentos)"""
    if not text:
        return ""
    return text.lower().strip()


def extract_country(job: Dict[str, Any]) -> str:
    """
    Extrai país/localização da vaga.
    Busca em: location (prioridade), description, title
    """
    location = normalize_text(job.get('location', ''))
    description = normalize_text(job.get('description', ''))
    title = normalize_text(job.get('title', ''))
    
    # 1. Tenta match em location primeiro (prioridade máxima)
    if location:
        for allowed in ALLOWED_COUNTRIES:
            if re.search(rf'\b{re.escape(allowed)}\b', location):
                return allowed
        
        # Se location tem país bloqueado
        for blocked in BLOCKED_COUNTRIES:
            if re.search(rf'\b{re.escape(blocked)}\b', location):
                return f"BLOCKED_{blocked}"
    
    # 2. Se location não deu, busca em description + title
    combined = f"{description} {title}"
    
    for allowed in ALLOWED_COUNTRIES:
        if re.search(rf'\b{re.escape(allowed)}\b', combined):
            return allowed
    
    for blocked in BLOCKED_COUNTRIES:
        if re.search(rf'\b{re.escape(blocked)}\b', combined):
            return f"BLOCKED_{blocked}"
    
    # 3. Default: Remote Global se menciona remote
    if any(x in location for x in ["remote", "remoto", "global", "worldwide", "international"]):
        return "remote_global"
    
    # 4. Desconhecido
    return "UNKNOWN"


def filter_by_country(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filtra vagas por país.
    ✅ Europa, Austrália, EUA, Canadá, Remoto Global
    ❌ Brasil/LATAM, Ásia, Middle East
    """
    valid_jobs = []
    rejected_country = []
    rejected_unknown = []
    
    for job in jobs:
        country = extract_country(job)
        
        if country.startswith("BLOCKED_"):
            rejected_country.append((job['company'], job['title'], country))
            continue
        
        if country == "UNKNOWN":
            rejected_unknown.append((job['company'], job['title']))
            continue
        
        # Adiciona país ao job
        job['_country'] = country
        valid_jobs.append(job)
    
    if rejected_country:
        logger.info(f"🚫 {len(rejected_country)} vagas rejeitadas (país bloqueado)")
    if rejected_unknown:
        logger.info(f"❓ {len(rejected_unknown)} vagas rejeitadas (país desconhecido)")
    
    return valid_jobs


def extract_sector(job: Dict[str, Any]) -> str:
    """Categoriza setor da vaga"""
    title = normalize_text(job.get('title', ''))
    description = normalize_text(job.get('description', ''))
    
    combined = f"{title} {description}"
    
    for sector, keywords in SECTORS.items():
        for keyword in keywords:
            if keyword in combined:
                return sector
    
    return "technology"  # Default


def detect_english_requirement(job: Dict[str, Any]) -> str:
    """
    Detecta requisito de inglês.
    Retorna: "fluent", "intermediate", "basic", "none", "unknown"
    """
    text = normalize_text(job.get('description', '') + " " + job.get('title', ''))
    
    # Fluente
    if any(x in text for x in ["fluent english", "fluent english required", "native english", "english fluency"]):
        return "fluent"
    
    # Intermediário
    if any(x in text for x in ["intermediate english", "good english", "english required", "english skills"]):
        return "intermediate"
    
    # Básico
    if any(x in text for x in ["basic english", "english helpful", "english preferred"]):
        return "basic"
    
    # Português OK (sem inglês)
    if any(x in text for x in ["português", "portuguese", "english not required", "english optional"]):
        return "none"
    
    # Indeterminado
    return "unknown"


def detect_education_requirement(job: Dict[str, Any]) -> str:
    """
    Detecta requisito de educação.
    Retorna: "yes" (exige), "no" (não exige), "unknown"
    """
    text = normalize_text(job.get('description', '') + " " + job.get('title', ''))
    
    # Não exige
    if any(x in text for x in [
        "no degree required", "degree not required", "self-taught", "bootcamp",
        "without degree", "sem diploma", "não exige diploma"
    ]):
        return "no"
    
    # Exige
    if any(x in text for x in [
        "bachelor's", "bachelor degree", "master's", "phd",
        "degree required", "diploma", "diploma required", "diploma exigido",
        "bachelor required", "university degree"
    ]):
        return "yes"
    
    return "unknown"


def detect_experience_requirement(job: Dict[str, Any]) -> tuple[str, int]:
    """
    Detecta requisito de experiência.
    Retorna: (tipo: "yes"|"no"|"unknown", anos: int|0)
    """
    text = normalize_text(job.get('description', '') + " " + job.get('title', ''))
    
    # Detecta anos
    import re
    years_match = re.search(r'(\d+)\+?\s*(?:years?|anos|year|ano)', text)
    years = int(years_match.group(1)) if years_match else 0
    
    # Sem experiência
    if any(x in text for x in ["no experience required", "entry level", "fresh", "trainee", "junior", "sem experiência"]):
        return "no", 0
    
    # Com experiência
    if years > 0 or any(x in text for x in ["experienced", "experienced required", "expertise", "com experiência"]):
        return "yes", years
    
    return "unknown", 0


def validate_citizenship_restriction(job: Dict[str, Any]) -> bool:
    """
    Valida que não há restrição de cidadania/residência.
    Retorna: True se OK (permite internacional), False se restrição
    """
    text = normalize_text(job.get('description', ''))
    
    # Blocos que indicam restrição
    blocked_phrases = [
        "citizens only",
        "permanent resident",
        "pr required",
        "visa sponsorship not available",
        "only for",
        "must be a citizen",
        "residency required",
        "residência exigida",
    ]
    
    for phrase in blocked_phrases:
        if phrase in text:
            return False
    
    return True


def filter_by_diversity_requirements(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Enriquece jobs com metadados de diversidade.
    Não rejeita nada aqui - apenas adiciona campos para validação posterior.
    """
    for job in jobs:
        job['_sector'] = extract_sector(job)
        job['_english'] = detect_english_requirement(job)
        job['_education'] = detect_education_requirement(job)
        job['_experience'], job['_experience_years'] = detect_experience_requirement(job)
        job['_citizenship_ok'] = validate_citizenship_restriction(job)
    
    return jobs


def filter_jobs(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Pipeline de filtros.
    """
    logger.info(f"📌 Filtrando {len(jobs)} vagas...")
    
    # 1. Filtra por país
    jobs = filter_by_country(jobs)
    logger.info(f"   ✓ Após filtro país: {len(jobs)} vagas")
    
    # 2. Adiciona metadados de diversidade
    jobs = filter_by_diversity_requirements(jobs)
    logger.info(f"   ✓ Após análise diversidade: {len(jobs)} vagas")
    
    # 3. Rejeita se tiver restrição de cidadania
    jobs = [j for j in jobs if j.get('_citizenship_ok', True)]
    logger.info(f"   ✓ Após validação cidadania: {len(jobs)} vagas")
    
    return jobs


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Testes
    test_jobs = [
        {
            "title": "Software Engineer",
            "company": "Google",
            "location": "Remote (EU preferred)",
            "description": "Join our team in Germany. Fluent English required. 3+ years experience.",
        },
        {
            "title": "Designer",
            "company": "Local Brazil",
            "location": "São Paulo, Brazil",
            "description": "Designer needed for local team.",
        },
        {
            "title": "Nurse",
            "company": "AU Health",
            "location": "Australia - Remote",
            "description": "Healthcare professional. No degree required. English optional.",
        },
    ]
    
    filtered = filter_jobs(test_jobs)
    
    print("\n=== RESULTADO APÓS FILTROS ===\n")
    for job in filtered:
        print(f"✅ {job['company']} - {job['title']}")
        print(f"   País: {job.get('_country')}")
        print(f"   Setor: {job.get('_sector')}")
        print(f"   Inglês: {job.get('_english')}")
        print(f"   Educação: {job.get('_education')}")
        print(f"   Experiência: {job.get('_experience')}")
        print()
