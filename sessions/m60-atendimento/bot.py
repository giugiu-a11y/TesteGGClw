#!/usr/bin/env python3
"""Bot M60 Atendimento - Isolado"""
import os
import json
import anthropic
import re
import builtins
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
_env_clawdbot = "/home/ubuntu/.clawdbot/.env"
if os.path.exists(_env_clawdbot):
    load_dotenv(_env_clawdbot, override=False)

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ANTHROPIC_KEY = None

# Redact sensitive values from prints
_TOKEN_RE = re.compile(r"\b\d{9,}:[A-Za-z0-9_-]{20,}\b")
_SECRETS = [
    os.getenv("TELEGRAM_BOT_TOKEN"),
    os.getenv("TELEGRAM_GROUP_ID"),
    os.getenv("TELEGRAM_CHAT_ID"),
    os.getenv("GEMINI_API_KEY"),
    os.getenv("GOOGLE_API_KEY"),
]
_SECRETS = [s for s in _SECRETS if s]


def _redact_text(text: str) -> str:
    if not text:
        return text
    text = _TOKEN_RE.sub("<redacted-token>", text)
    for secret in _SECRETS:
        text = text.replace(secret, "<redacted>")
    return text


def print(*args, **kwargs):
    redacted = [_redact_text(str(a)) for a in args]
    return builtins.print(*redacted, **kwargs)

try:
    with open('/etc/llm.env') as f:
        for line in f:
            if line.startswith('ANTHROPIC_API_KEY='):
                ANTHROPIC_KEY = line.strip().split('=', 1)[1]
                break
except PermissionError:
    ANTHROPIC_KEY = ANTHROPIC_KEY or os.getenv('ANTHROPIC_API_KEY')

client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')
with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)

from guard import validate

SYSTEM_PROMPT = """Você é o assistente de atendimento da M60/UDI.
Foco: bolsas de estudo, intercâmbio, carreiras internacionais.
Público: alunos e interessados.
Tom: profissional, motivador, educado.
Idioma: Português BR.

NUNCA faça: tweets, conteúdo viral, posts de redes sociais.
SEMPRE: responda dúvidas sobre bolsas, documentos, processos."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Olá! Sou o assistente da M60. Como posso ajudar com sua jornada internacional?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    
    ok, reason = validate(msg)
    if not ok:
        await update.message.reply_text(f"❌ {reason}")
        return
    
    response = client.messages.create(
        model=CONFIG.get('model', 'claude-haiku-4-5'),
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": msg}]
    )
    
    await update.message.reply_text(response.content[0].text)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print(f"📚 M60 Atendimento starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
