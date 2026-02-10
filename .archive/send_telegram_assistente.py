#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Send a text file to the Assistente Clawd Opus bot only."""

import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ENV_PATH = Path("/home/ubuntu/clawd/sessions/assistente-opus/.env.assistente")


def load_env():
    token = None
    chat_id = None
    if not ENV_PATH.exists():
        return None, None
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        k = k.strip(); v = v.strip().strip('"').strip("'")
        if k == 'TELEGRAM_BOT_TOKEN':
            token = v
        elif k == 'ALLOWED_USER_ID':
            chat_id = v
    return token, chat_id


def send_message(token: str, chat_id: str, text: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    # Telegram limit ~4096 chars; keep margin
    max_len = 3800
    chunks = [text[i:i+max_len] for i in range(0, len(text), max_len)] or [""]
    for chunk in chunks:
        payload = {
            "chat_id": chat_id,
            "text": chunk,
            "disable_web_page_preview": False,
        }
        data = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=20) as resp:
            resp.read()


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: send_telegram_assistente.py <text_file>")
        return 2
    text_path = Path(sys.argv[1])
    if not text_path.exists():
        print(f"File not found: {text_path}")
        return 2

    token, chat_id = load_env()
    if not token or not chat_id:
        print("Missing TELEGRAM_BOT_TOKEN or ALLOWED_USER_ID for Assistente.")
        return 1

    text = text_path.read_text().strip()
    if not text:
        print("Empty message; nothing to send.")
        return 1

    send_message(token, chat_id, text)
    print("Sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
