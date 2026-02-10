#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path

def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def fmt_virais(data):
    lines = []
    lines.append("📌 YouTube")
    yt = data.get('youtube_top') or []
    yt_titles = [i.get('title','') for i in yt if isinstance(i, dict) and i.get('title')]
    if yt_titles:
        for t in yt_titles[:5]:
            lines.append(f"- 🔥 {t}")
    else:
        lines.append("- 🔥 sem dados")

    lines.append("📌 TikTok")
    tt = data.get('tiktok_trends') or []
    tt_titles = [i.get('title','') for i in tt if isinstance(i, dict) and i.get('title')]
    if tt_titles:
        for t in tt_titles[:5]:
            lines.append(f"- 🔥 {t}")
    else:
        lines.append("- 🔥 sem dados")

    lines.append("📌 Google Trends")
    trends = data.get('google_trends') or []
    trend_titles = [i.get('query','') for i in trends if isinstance(i, dict) and i.get('query')]
    if trend_titles:
        for t in trend_titles[:5]:
            lines.append(f"- 🔥 {t}")
    else:
        lines.append("- 🔥 sem dados")

    return "\n".join(lines)


def fmt_noticias(data):
    items = data.get('items') or []
    queries = data.get('queries') or []
    buckets = {}
    for item in items:
        q = item.get('query','Outros')
        buckets.setdefault(q, [])
        title = item.get('title','')
        if title:
            buckets[q].append(title)
    lines = []
    order = queries if queries else list(buckets.keys())
    for q in order:
        titles = buckets.get(q, [])
        lines.append(f"📌 {q}")
        if titles:
            for t in titles[:3]:
                lines.append(f"- 🧭 {t}")
        else:
            lines.append("- 🧭 sem dados")
    lines.append("- ✅ Ação: revisar impacto e atualizar briefing manualmente se necessário.")
    return "\n".join(lines)


def fmt_mercado(data):
    lines = []
    crypto = data.get('crypto') or {}
    crypto_fb = data.get('crypto_fallback') or {}
    crypto_src = crypto if isinstance(crypto, dict) and 'bitcoin' in crypto else crypto_fb
    if isinstance(crypto_src, dict) and 'bitcoin' in crypto_src:
        btc = crypto_src.get('bitcoin', {})
        lines.append(f"- ₿ BTC: ${btc.get('usd','?')} (24h {btc.get('usd_24h_change','?')}%)")
        avax = crypto_src.get('avalanche-2', {})
        matic = crypto_src.get('matic-network', {}) or crypto_src.get('polygon', {})
        lines.append(f"- 🔺 AVAX: ${avax.get('usd','?')} | 🔷 MATIC/POL: ${matic.get('usd','?')}")
    else:
        lines.append("- ₿ Crypto: sem dados")

    yahoo = data.get('yahoo') or {}
    stooq = data.get('stooq') or {}
    sp_line = None
    fx_line = None
    if isinstance(yahoo, dict) and 'quoteResponse' in yahoo:
        q = (yahoo.get('quoteResponse') or {}).get('result') or []
        sp = next((x for x in q if x.get('symbol') == '^GSPC'), None)
        fx = next((x for x in q if x.get('symbol') == 'USDBRL=X'), None)
        if sp:
            sp_line = f"- 📈 S&P 500: {sp.get('regularMarketChangePercent','?')}%"
        if fx:
            fx_line = f"- 💵 USD/BRL: {fx.get('regularMarketPrice','?')}"
    if not sp_line and isinstance(stooq, dict):
        spx = stooq.get('spx') or {}
        if spx:
            sp_line = f"- 📈 S&P 500: {spx.get('Close','?')}"
    if not fx_line and isinstance(stooq, dict):
        fx = stooq.get('usdbrl') or {}
        if fx:
            fx_line = f"- 💵 USD/BRL: {fx.get('Close','?')}"
    if sp_line:
        lines.append(sp_line)
    if fx_line:
        lines.append(fx_line)
    if not sp_line and not fx_line:
        lines.append("- 📈 S&P/FX: sem dados")

    selic = data.get('selic')
    selic_fb = data.get('selic_fallback')
    if isinstance(selic, dict) and 'valor' in selic:
        lines.append(f"- 🏦 Selic: {selic.get('valor','?')}%")
    elif isinstance(selic_fb, dict) and 'valor' in selic_fb:
        lines.append(f"- 🏦 Selic: {selic_fb.get('valor','?')}%")
    else:
        lines.append("- 🏦 Selic: sem dados")

    lines.append("- ⚠️ Risco/Oportunidade: dados parciais hoje; validar manualmente se necessário.")
    return "\n".join(lines)


def main():
    kind = sys.argv[1]
    if kind == 'virais':
        data = load('/tmp/briefing-virais.json')
        print(fmt_virais(data))
    elif kind == 'noticias':
        data = load('/tmp/briefing-noticias.json')
        print(fmt_noticias(data))
    elif kind == 'mercado':
        data = load('/tmp/briefing-mercado.json')
        print(fmt_mercado(data))
    else:
        raise SystemExit('usage: format_fallback.py virais|noticias|mercado')

if __name__ == '__main__':
    main()
