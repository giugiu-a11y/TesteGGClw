#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fetch news via Google News RSS for specific queries.
Output: /tmp/briefing-noticias.json
"""

import json
import os
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

OUTPUT = "/tmp/briefing-noticias.json"

QUERIES = [
    "bolsas de estudo",
    "study abroad scholarships",
    "edtech M&A",
    "edtech funding",
    "imigração",
    "visto estudante",
    "geopolítica",
    "Brasil economia",
    "mercado de trabalho remoto",
]

ALLOWLIST = {
    "g1.globo.com", "valor.globo.com", "oglobo.globo.com", "agenciabrasil.ebc.com.br",
    "estadao.com.br", "folha.uol.com.br", "uol.com.br", "cnnbrasil.com.br",
    "bbc.com", "reuters.com", "apnews.com", "ft.com", "wsj.com",
    "bloomberg.com", "theguardian.com", "economist.com",
    "timeshighereducation.com", "insidehighered.com", "universityworldnews.com",
    "edsurge.com", "techcrunch.com", "thepienews.com",
    "exame.com", "infomoney.com.br", "investnews.com.br", "moneytimes.com.br",
    "startups.com.br", "pipelinevalor.com.br", "tecmundo.com.br",
    "gov.br", "uscis.gov", "state.gov",
}

KEYWORDS = {
    "bolsas de estudo": [
        "bolsa de estudo", "scholarship", "study abroad", "intercâmbio",
        "fellowship", "universidade", "university", "college", "tuition",
        "bolsas no exterior", "programa de bolsas",
    ],
    "study abroad scholarships": ["scholarship", "study abroad", "fellowship", "funding", "grant"],
    "edtech M&A": ["edtech", "m&a", "fusão", "aquisição", "acquisition", "merge", "compra"],
    "edtech funding": ["edtech", "funding", "invest", "captação", "rodada", "seed", "series", "investimento", "aporte"],
    "imigração": ["imigra", "immigration", "visa", "visto", "ice", "uscis", "fronteira", "asilo", "deport"],
    "visto estudante": ["visto", "student", "study", "visa", "f-1", "f1", "j-1", "j1"],
    "geopolítica": ["geopol", "geopolit", "guerra", "conflito", "sanção", "segurança", "nato", "otan"],
    "Brasil economia": ["economia", "ibovespa", "selic", "inflação", "pib", "dólar", "real", "copom", "taxa de juros"],
    "mercado de trabalho remoto": ["remoto", "remote", "home office", "freelance", "trabalho remoto", "nomad", "offshore"],
}


def _http_get(url: str, timeout: int = 10) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "briefings/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _domain(link: str) -> str:
    try:
        return link.split("//", 1)[1].split("/", 1)[0].lower()
    except Exception:
        return ""


def _allowed(link: str) -> bool:
    d = _domain(link)
    if not d:
        return False
    if d in ALLOWLIST:
        return True
    # allow subdomains
    return any(d.endswith("." + a) for a in ALLOWLIST)


def _match_keywords(title: str, q: str) -> bool:
    keys = KEYWORDS.get(q, [])
    t = (title or "").lower()
    return any(k in t for k in keys) if keys else True


def fetch_query(q: str) -> list[dict]:
    params = {
        "q": q,
        "hl": "pt-BR",
        "gl": "BR",
        "ceid": "BR:pt-419",
    }
    url = "https://news.google.com/rss/search?" + urllib.parse.urlencode(params)
    xml_text = _http_get(url)
    root = ET.fromstring(xml_text)

    out = []
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = (item.findtext("pubDate") or "").strip()
        source_el = item.find("source")
        source = (source_el.text or "").strip() if source_el is not None else ""
        source_url = (source_el.get("url") if source_el is not None else "") or ""
        if not title or not link:
            continue
        if _allowed(source_url or link) and _match_keywords(title, q):
            out.append({
                "title": title,
                "link": link,
                "source": source,
                "source_url": source_url,
                "published": pub,
                "query": q,
            })
        # If we already have 3 good items, stop early.
        if len(out) >= 3:
            break

    return out


def main() -> int:
    cached = None
    if os.path.exists(OUTPUT):
        try:
            with open(OUTPUT, "r", encoding="utf-8") as f:
                cached = json.load(f)
        except Exception:
            cached = None

    all_items = []
    for q in QUERIES:
        try:
            all_items.extend(fetch_query(q))
        except Exception as e:
            all_items.append({"error": f"news_failed:{q}:{e}"})

    payload = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "queries": QUERIES,
        "items": all_items,
        "source": "google_news_rss",
    }
    if cached and not all_items:
        cached["timestamp"] = payload["timestamp"]
        payload = cached
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
