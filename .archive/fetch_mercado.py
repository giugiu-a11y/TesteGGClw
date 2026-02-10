#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fetch market data:
- Crypto (BTC, AVAX, MATIC/POL) via CoinGecko
- S&P 500 and USD/BRL via Yahoo Finance quote
- Selic via Banco Central API

Output: /tmp/briefing-mercado.json
"""

import json
import os
import urllib.request
import csv
import io
from datetime import datetime, timezone

OUTPUT = "/tmp/briefing-mercado.json"


def _http_get(url: str, timeout: int = 10) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "briefings/1.0",
            "Accept": "application/json,text/xml;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_crypto():
    url = (
        "https://api.coingecko.com/api/v3/simple/price?"
        "ids=bitcoin,avalanche-2,matic-network&vs_currencies=usd"
        "&include_24hr_change=true&include_market_cap=true"
    )
    return json.loads(_http_get(url))


def fetch_crypto_binance():
    symbols = {
        "bitcoin": "BTCUSDT",
        "avalanche-2": "AVAXUSDT",
        "matic-network": "MATICUSDT",
    }
    out = {}
    for k, sym in symbols.items():
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={sym}"
        data = json.loads(_http_get(url))
        out[k] = {
            "usd": float(data.get("lastPrice", "0") or 0),
            "usd_24h_change": float(data.get("priceChangePercent", "0") or 0),
        }
    return out


def fetch_yahoo():
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=%5EGSPC,USDBRL=X"
    return json.loads(_http_get(url))


def fetch_stooq():
    def _csv(url):
        raw = _http_get(url)
        reader = csv.DictReader(io.StringIO(raw))
        rows = list(reader)
        return rows[-1] if rows else {}

    spx = _csv("https://stooq.com/q/l/?s=^spx&i=d")
    fx = _csv("https://stooq.com/q/l/?s=usdbrl&i=d")
    return {"spx": spx, "usdbrl": fx}


def fetch_selic():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json"
    data = json.loads(_http_get(url))
    return data[-1] if data else None


def fetch_selic_target():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json"
    data = json.loads(_http_get(url))
    return data[-1] if data else None


def main() -> int:
    cached = None
    if os.path.exists(OUTPUT):
        try:
            with open(OUTPUT, "r", encoding="utf-8") as f:
                cached = json.load(f)
        except Exception:
            cached = None

    def _safe(fn, name):
        try:
            return fn()
        except Exception as e:
            return {"error": f"{name}_failed", "details": str(e)[:200]}

    payload = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "crypto": _safe(fetch_crypto, "crypto"),
        "crypto_fallback": _safe(fetch_crypto_binance, "crypto_binance"),
        "yahoo": _safe(fetch_yahoo, "yahoo"),
        "stooq": _safe(fetch_stooq, "stooq"),
        "selic": _safe(fetch_selic, "selic"),
        "selic_fallback": _safe(fetch_selic_target, "selic_target"),
        "source": {
            "crypto": "coingecko",
            "crypto_fallback": "binance",
            "yahoo": "yahoo_finance",
            "stooq": "stooq",
            "selic": "bcb_sgs_11",
            "selic_fallback": "bcb_sgs_432",
        },
    }

    # If all sources failed and we have cache, reuse it.
    if cached and all(isinstance(payload[k], dict) and payload[k].get("error") for k in ("crypto", "yahoo", "selic")):
        cached["timestamp"] = payload["timestamp"]
        payload = cached
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
