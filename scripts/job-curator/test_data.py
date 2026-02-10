#!/usr/bin/env python3
"""
Test Data - Dados de teste para validar pipeline
Remove depois de integrar com APIs reais
"""

TEST_JOBS = [
    {
        "source": "test",
        "source_url": "https://weworkremotely.com/remote-jobs/123",
        "title": "Senior Software Engineer",
        "company": "Google",
        "location": "Remote USA",
        "description": "Build scalable systems. 5+ years experience required. Fluent English. Bachelor's degree preferred.",
        "salary_min": 150000,
        "salary_max": 200000,
    },
    {
        "source": "test",
        "source_url": "https://linkedin.com/jobs/456",
        "title": "UX/UI Designer",
        "company": "Figma",
        "location": "Remote Canada",
        "description": "Design beautiful interfaces. 2+ years. English intermediate. Degree not required.",
        "salary_min": None,
        "salary_max": None,
    },
    {
        "source": "test",
        "source_url": "https://indeed.com/jobs/789",
        "title": "Registered Nurse - Remote",
        "company": "TelaDoc Health",
        "location": "Remote USA",
        "description": "Healthcare professional. No experience required. Can work in Portuguese. No degree needed (nursing certification required).",
        "salary_min": 70000,
        "salary_max": 85000,
    },
    {
        "source": "test",
        "source_url": "https://remoteok.com/jobs/1011",
        "title": "Business Analyst",
        "company": "Netflix",
        "location": "Remote Europe Germany",
        "description": "Analyze business metrics. 3+ years required. English fluent. Bachelor's degree required.",
        "salary_min": 100000,
        "salary_max": 130000,
    },
    {
        "source": "test",
        "source_url": "https://himalayas.app/jobs/1213",
        "title": "Content Writer",
        "company": "Copyblogger",
        "location": "Remote Global",
        "description": "Write engaging content. Any level welcome. English intermediate. No formal education needed.",
        "salary_min": 2000,
        "salary_max": 4000,
    },
    {
        "source": "test",
        "source_url": "https://weworkremotely.com/jobs/1415",
        "title": "Data Scientist",
        "company": "Amazon",
        "location": "Remote UK",
        "description": "ML/AI role. 4+ years needed. Fluent English. Master's preferred. Salary £80-100k",
        "salary_min": 102000,
        "salary_max": 128000,
    },
]


def get_test_jobs():
    """Retorna jobs de teste"""
    return TEST_JOBS.copy()


if __name__ == "__main__":
    print(f"✓ {len(TEST_JOBS)} vagas de teste disponíveis")
    for job in TEST_JOBS:
        print(f"  • {job['title']} @ {job['company']}")
