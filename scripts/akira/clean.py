#!/usr/bin/env python3
import sys, re, json
from html import unescape

DEFAULT_MAX_CHARS = 30000
DEFAULT_MAX_CHUNKS = 40
DEFAULT_MAX_CHUNK_CHARS = 1200

BOILERPLATE_PATTERNS = [
    r'\b(cookie|cookies|política de privacidade|privacy policy|terms of service|termos de uso)\b',
    r'\b(assine|subscribe|newsletter|cadastre-se|sign up)\b',
    r'\b(all rights reserved|direitos reservados)\b',
    r'\b(compartilhar|share|follow us|siga-nos)\b',
]

def strip_scripts_styles(html: str) -> str:
    html = re.sub(r'(?is)<script\b.*?>.*?</script>', ' ', html)
    html = re.sub(r'(?is)<style\b.*?>.*?</style>', ' ', html)
    return html

def strip_tags(html: str) -> str:
    html = re.sub(r'(?is)<br\s*/?>', '\n', html)
    html = re.sub(r'(?is)</p\s*>', '\n', html)
    html = re.sub(r'(?is)</div\s*>', '\n', html)
    html = re.sub(r'(?is)<.*?>', ' ', html)
    return html

def normalize(text: str) -> str:
    text = unescape(text)
    text = re.sub(r'\r\n?', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def is_boilerplate(s: str) -> bool:
    low = s.lower()
    for pat in BOILERPLATE_PATTERNS:
        if re.search(pat, low):
            return True
    return False

def split_paragraphs(text: str):
    parts = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    seen = set()
    out = []
    for p in parts:
        key = re.sub(r'\s+', ' ', p).strip().lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out

def score_paragraph(p: str, keywords):
    low = p.lower()
    kscore = 0
    for kw in keywords:
        kw = kw.strip().lower()
        if not kw:
            continue
        kscore += low.count(kw)
    length = max(1, len(p))
    dens = kscore / (length / 500)
    penalty = 2.0 if is_boilerplate(p) else 0.0
    return dens - penalty

def truncate_by_relevance(text: str, max_chars: int, keywords):
    paragraphs = split_paragraphs(text)
    if not paragraphs:
        return "", {"kept": 0, "total": 0}

    scored = []
    for p in paragraphs:
        sp = p[:DEFAULT_MAX_CHUNK_CHARS]
        scored.append((score_paragraph(sp, keywords), sp))

    scored.sort(key=lambda x: x[0], reverse=True)

    kept = []
    total = 0
    for _, p in scored[:DEFAULT_MAX_CHUNKS]:
        if total + len(p) + 2 > max_chars:
            continue
        kept.append(p)
        total += len(p) + 2

    if not kept:
        total = 0
        for p in paragraphs[:DEFAULT_MAX_CHUNKS]:
            sp = p[:DEFAULT_MAX_CHUNK_CHARS]
            if total + len(sp) + 2 > max_chars:
                break
            kept.append(sp)
            total += len(sp) + 2

    return "\n\n".join(kept).strip(), {"kept": len(kept), "total": len(paragraphs)}

def main():
    raw = sys.stdin.read()
    if not raw.strip():
        print(json.dumps({"error": "empty_input"}))
        return 1

    max_chars = DEFAULT_MAX_CHARS
    keywords = []

    txt = strip_scripts_styles(raw)
    txt = strip_tags(txt)
    txt = normalize(txt)

    final, meta = truncate_by_relevance(txt, max_chars=max_chars, keywords=keywords)

    print(json.dumps({
        "clean_text": final,
        "meta": {
            "raw_chars": len(raw),
            "clean_chars": len(txt),
            "final_chars": len(final),
            "paragraphs_kept": meta["kept"],
            "paragraphs_total": meta["total"],
        }
    }, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
