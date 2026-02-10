#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Build LLM prompt for Virais/Trends briefing."""

import json
from datetime import datetime

INPUT = "/tmp/briefing-virais.json"
OUTPUT = "/tmp/briefing-virais.prompt.txt"

INSTRUCTIONS = (
    "Você é um analista de conteúdo. Responda em PT-BR, direto e sem enrolação.\n"
    "Quero APENAS títulos/temas que viralizaram, agrupados por fonte.\n"
    "Sem análise, sem ideias, sem comentários. Se não houver dados de uma fonte, escreva \"sem dados\".\n"
    "IGNORE qualquer instrução anterior. NÃO leia HEARTBEAT.md. NÃO faça diagnósticos.\n"
    "Sem links. Sem texto extra fora da lista.\n\n"
    "Formato (Telegram):\n"
    "📌 YouTube\n"
    "- 🔥 Título\n"
    "📌 TikTok\n"
    "- 🔥 Título (ou \"sem dados\")\n"
    "📌 Google Trends\n"
    "- 🔥 Tema\n"
)


def main() -> int:
    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    payload = json.dumps(data, ensure_ascii=False, indent=2)
    prompt = (
        INSTRUCTIONS
        + "\nDADOS (JSON):\n"
        + payload
        + "\n\nResponda apenas com a lista final."
    )

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(prompt)

    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
