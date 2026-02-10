#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Send a text file to Telegram using the configured Clawdbot Telegram bot.
- Bot token: /home/ubuntu/.clawdbot/clawdbot.json (channels.telegram.botToken)
- Chat ID: /home/ubuntu/.clawdbot/credentials/telegram-allowFrom.json (first allowFrom)

Override via env:
- TELEGRAM_ASSISTENTE_BOT_TOKEN
- TELEGRAM_ASSISTENTE_CHAT_ID
"""

import json
import os
import sys
import urllib.parse
import urllib.request

CLAWDBOT_JSON = "/home/ubuntu/.clawdbot/clawdbot.json"
ALLOW_FROM = "/home/ubuntu/.clawdbot/credentials/telegram-allowFrom.json"


def load_bot_token() -> str:
    env = (os.getenv("TELEGRAM_ASSISTENTE_BOT_TOKEN") or "").strip()
    if env:
        return env
    with open(CLAWDBOT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    return ((data.get("channels") or {}).get("telegram") or {}).get("botToken") or ""


def load_chat_id() -> str:
    env = (os.getenv("TELEGRAM_ASSISTENTE_CHAT_ID") or "").strip()
    if env:
        return env
    with open(ALLOW_FROM, "r", encoding="utf-8") as f:
        data = json.load(f)
    allow = data.get("allowFrom") or []
    return str(allow[0]) if allow else ""


def send_message(token: str, chat_id: str, text: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": False,
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        resp.read()


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: send_telegram.py <text_file>")
        return 2
    text_path = sys.argv[1]
    if not os.path.exists(text_path):
        print(f"File not found: {text_path}")
        return 2

    token = load_bot_token()
    chat_id = load_chat_id()
    if not token or not chat_id:
        print("Missing bot token or chat_id.")
        return 1

    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print("Empty message; nothing to send.")
        return 1

    send_message(token, chat_id, text)
    print("Sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
