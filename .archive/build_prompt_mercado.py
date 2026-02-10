#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Build LLM prompt for Mercado briefing."""

import json

INPUT = "/tmp/briefing-mercado.json"
OUTPUT = "/tmp/briefing-mercado.prompt.txt"

INSTRUCTIONS = (
    "Você é um analista de mercado para um perfil não técnico. Responda em PT-BR.\n"
    "Use 5–6 bullets no máximo.\n"
    "Inclua BTC, AVAX, MATIC/POL, S&P 500, USD/BRL, Selic.\n"
    "Feche com uma linha de risco/oportunidade.\n\n"
    "IGNORE qualquer instrução anterior. NÃO leia HEARTBEAT.md. NÃO faça diagnósticos.\n"
    "Formato (Telegram):\n"
    "- ₿ BTC: $... (24h ...) — leitura rápida\n"
    "- 🔺 AVAX: $... | 🔷 MATIC/POL: $...\n"
    "- 📈 S&P 500: ...\n"
    "- 💵 USD/BRL: ... | 🏦 Selic: ...\n"
    "- ⚠️ Risco/Oportunidade: ...\n"
)


def main() -> int:
    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    payload = json.dumps(data, ensure_ascii=False, indent=2)
    prompt = (
        INSTRUCTIONS
        + "\nDADOS (JSON):\n"
        + payload
        + "\n\nResponda apenas com o briefing final."
    )

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(prompt)

    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
