#!/usr/bin/env python3
"""
Diversity Validator v2.1 - Valida que as 3 vagas do dia têm diversidade
ZERO LLM - Tudo é lógica booleana
"""

import logging
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)

# Requisitos de diversidade que DEVEM ser atendidos
DIVERSITY_RULES = {
    "countries": 2,  # Mínimo 2 países diferentes
    "with_education": 1,  # Pelo menos 1 que EXIGE diploma
    "without_education": 1,  # Pelo menos 1 que NÃO exige
    "sectors": 3,  # Mínimo 3 setores diferentes
    "without_fluent_english": 1,  # Pelo menos 1 sem inglês fluente
    "without_experience": 1,  # Pelo menos 1 sem experiência necessária
    "with_experience": 1,  # Pelo menos 1 com experiência
}


def validate_diversity(jobs: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """
    Valida que batch de 3 vagas tem diversidade garantida.
    
    Retorna:
        (valid: bool, failing_rules: List[str])
    """
    
    if len(jobs) != 3:
        return False, ["Deve ter exatamente 3 vagas"]
    
    failing_rules = []
    
    # 1. Países mesclados
    countries = set(j.get('_country', 'unknown') for j in jobs)
    if len(countries) < DIVERSITY_RULES["countries"]:
        failing_rules.append(f"❌ Países: {len(countries)}/{DIVERSITY_RULES['countries']} (tem: {countries})")
    else:
        logger.info(f"✅ Países: {len(countries)} diferentes")
    
    # 2. Com e sem faculdade
    with_education = sum(1 for j in jobs if j.get('_education') == 'yes')
    without_education = sum(1 for j in jobs if j.get('_education') == 'no')
    
    if with_education < DIVERSITY_RULES["with_education"]:
        failing_rules.append(f"❌ Com faculdade: {with_education}/{DIVERSITY_RULES['with_education']}")
    else:
        logger.info(f"✅ Com faculdade: {with_education}")
    
    if without_education < DIVERSITY_RULES["without_education"]:
        failing_rules.append(f"❌ Sem faculdade: {without_education}/{DIVERSITY_RULES['without_education']}")
    else:
        logger.info(f"✅ Sem faculdade: {without_education}")
    
    # 3. Setores variados
    sectors = set(j.get('_sector', 'unknown') for j in jobs)
    if len(sectors) < DIVERSITY_RULES["sectors"]:
        failing_rules.append(f"❌ Setores: {len(sectors)}/{DIVERSITY_RULES['sectors']} (tem: {sectors})")
    else:
        logger.info(f"✅ Setores: {len(sectors)} diferentes")
    
    # 4. Sem inglês fluente obrigatório
    non_fluent = sum(1 for j in jobs if j.get('_english') in ['basic', 'intermediate', 'none'])
    if non_fluent < DIVERSITY_RULES["without_fluent_english"]:
        failing_rules.append(f"❌ Sem inglês fluente: {non_fluent}/{DIVERSITY_RULES['without_fluent_english']}")
    else:
        logger.info(f"✅ Sem inglês fluente obrigatório: {non_fluent}")
    
    # 5. Sem experiência e com experiência
    without_exp = sum(1 for j in jobs if j.get('_experience') == 'no')
    with_exp = sum(1 for j in jobs if j.get('_experience') == 'yes')
    
    if without_exp < DIVERSITY_RULES["without_experience"]:
        failing_rules.append(f"❌ Sem experiência: {without_exp}/{DIVERSITY_RULES['without_experience']}")
    else:
        logger.info(f"✅ Sem experiência: {without_exp}")
    
    if with_exp < DIVERSITY_RULES["with_experience"]:
        failing_rules.append(f"❌ Com experiência: {with_exp}/{DIVERSITY_RULES['with_experience']}")
    else:
        logger.info(f"✅ Com experiência: {with_exp}")
    
    # Resumo
    valid = len(failing_rules) == 0
    
    if valid:
        logger.info("\n✅ BATCH VALIDADO - Atende todos os requisitos de diversidade")
    else:
        logger.warning("\n❌ BATCH REJEITADO - Não atende requisitos:")
        for rule in failing_rules:
            logger.warning(f"   {rule}")
    
    return valid, failing_rules


def print_batch_summary(jobs: List[Dict[str, Any]]) -> str:
    """
    Gera resumo legível do batch.
    """
    summary = "\n=== RESUMO DO BATCH ===\n"
    
    for i, job in enumerate(jobs, 1):
        summary += f"{i}. {job.get('title')} @ {job.get('company')}\n"
        summary += f"   📍 {job.get('_country')}\n"
        summary += f"   🎯 {job.get('_sector')}\n"
        summary += f"   🗣 Inglês: {job.get('_english')}\n"
        summary += f"   🎓 Educação: {job.get('_education')}\n"
        summary += f"   💼 Experiência: {job.get('_experience')} ({job.get('_experience_years', 0)}+ anos)\n\n"
    
    return summary


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Teste VÁLIDO
    valid_jobs = [
        {
            "title": "Software Engineer",
            "company": "Google",
            "_country": "us",
            "_sector": "technology",
            "_education": "yes",
            "_english": "fluent",
            "_experience": "yes",
            "_experience_years": 3,
        },
        {
            "title": "Nurse",
            "company": "AU Health",
            "_country": "australia",
            "_sector": "healthcare",
            "_education": "no",
            "_english": "none",
            "_experience": "no",
            "_experience_years": 0,
        },
        {
            "title": "Product Designer",
            "company": "Figma",
            "_country": "canada",
            "_sector": "design",
            "_education": "unknown",
            "_english": "basic",
            "_experience": "yes",
            "_experience_years": 2,
        },
    ]
    
    # Teste INVÁLIDO (falta diversidade)
    invalid_jobs = [
        {
            "title": "Software Engineer 1",
            "company": "Google",
            "_country": "us",
            "_sector": "technology",
            "_education": "yes",
            "_english": "fluent",
            "_experience": "yes",
            "_experience_years": 5,
        },
        {
            "title": "Software Engineer 2",
            "company": "Amazon",
            "_country": "us",
            "_sector": "technology",
            "_education": "yes",
            "_english": "fluent",
            "_experience": "yes",
            "_experience_years": 3,
        },
        {
            "title": "Software Engineer 3",
            "company": "Microsoft",
            "_country": "us",
            "_sector": "technology",
            "_education": "yes",
            "_english": "fluent",
            "_experience": "yes",
            "_experience_years": 4,
        },
    ]
    
    print("\n🟢 TESTE 1: BATCH VÁLIDO\n")
    print(print_batch_summary(valid_jobs))
    valid, failing = validate_diversity(valid_jobs)
    print(f"Resultado: {'✅ APROVADO' if valid else '❌ REPROVADO'}\n")
    
    print("\n🔴 TESTE 2: BATCH INVÁLIDO\n")
    print(print_batch_summary(invalid_jobs))
    valid, failing = validate_diversity(invalid_jobs)
    print(f"Resultado: {'✅ APROVADO' if valid else '❌ REPROVADO'}\n")
