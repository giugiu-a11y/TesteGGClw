#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Build LLM prompt for Notícias briefing."""

import json

INPUT = "/tmp/briefing-noticias.json"
OUTPUT = "/tmp/briefing-noticias.prompt.txt"

INSTRUCTIONS = (
    "Você é um analista de notícias para M60/UDI. Responda em PT-BR.\n"
    "Para CADA tema abaixo, selecione o TOP 3 notícias:\n"
    "1) Bolsas/Study Abroad\n"
    "2) Edtech (M&A e funding)\n"
    "3) Imigração/Vistos\n"
    "4) Geopolítica\n"
    "5) Brasil Economia\n"
    "6) Trabalho Remoto Global\n"
    "Para cada item: impacto M60/UDI. Sem links.\n"
    "Feche com 1 ação recomendada.\n\n"
    "IGNORE qualquer instrução anterior. NÃO leia HEARTBEAT.md. NÃO faça diagnósticos.\n"
    "Formato (Telegram):\n"
    "📌 [Tema]\n"
    "- 🧭 Notícia — impacto\n"
    "- 🧭 Notícia — impacto\n"
    "- 🧭 Notícia — impacto\n"
    "- ✅ Ação: ...\n"
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
