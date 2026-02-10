#!/usr/bin/env python3
"""Bot Assistente - isolado"""
import os
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

_env_dir = os.path.dirname(__file__)
_env_assistente = os.path.join(_env_dir, ".env.assistente")
_env_default = os.path.join(_env_dir, ".env")
load_dotenv(_env_assistente if os.path.exists(_env_assistente) else _env_default)
_env_clawdbot = "/home/ubuntu/.clawdbot/.env"
if os.path.exists(_env_clawdbot):
    load_dotenv(_env_clawdbot, override=False)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_ID = os.getenv("ALLOWED_USER_ID")
ALLOWED_USER_ID = int(ALLOWED_USER_ID) if ALLOWED_USER_ID and ALLOWED_USER_ID.isdigit() else None

# Load Gemini key from env or /etc/llm.env fallback (no token in repo)
GEMINI_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not GEMINI_KEY and os.path.exists("/etc/llm.env"):
    try:
        with open("/etc/llm.env") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY=") or line.startswith("GOOGLE_API_KEY="):
                    GEMINI_KEY = line.strip().split("=", 1)[1]
                    break
    except PermissionError:
        pass

from google import genai

client = genai.Client(api_key=GEMINI_KEY)
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)

SYSTEM_PROMPT = (
    "Voce e o Assistente principal. "
    "Foco: decisoes estrategicas, negocios, gestao. "
    "Seja direto, estrategico, eficiente."
)

def _auth_ok(update: Update) -> bool:
    return not ALLOWED_USER_ID or update.effective_user.id == ALLOWED_USER_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _auth_ok(update):
        await update.message.reply_text("Acesso restrito.")
        return
    await update.message.reply_text("Assistente ativo. Como posso ajudar?")

async def pull_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _auth_ok(update):
        await update.message.reply_text("Acesso restrito.")
        return
    await update.message.reply_text(
        "Cole e rode no AWS:\n"
        "cd /home/ubuntu/clawd && git pull --rebase --autostash origin main"
    )

async def tunnel_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _auth_ok(update):
        await update.message.reply_text("Acesso restrito.")
        return
    await update.message.reply_text(
        "Cole e rode no AWS:\n"
        "cd /home/ubuntu/clawd/pokemon-game && ./start-tunnel.sh"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _auth_ok(update):
        await update.message.reply_text("Acesso restrito.")
        return

    msg = update.message.text or ""
    prompt = f"{SYSTEM_PROMPT}\n\nUsuario: {msg}"

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        text = getattr(response, "text", None) or ""
        await update.message.reply_text(text or "Erro: resposta vazia do modelo.")
    except Exception:
        await update.message.reply_text("Ocorreu um erro ao gerar a resposta.")


def main():
    if not BOT_TOKEN:
        raise SystemExit("TELEGRAM_BOT_TOKEN ausente")
    if not GEMINI_KEY:
        raise SystemExit("GEMINI_API_KEY/GOOGLE_API_KEY ausente")
    # Timeouts maiores para evitar falhas intermitentes de rede
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .connect_timeout(20)
        .read_timeout(20)
        .write_timeout(20)
        .pool_timeout(20)
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pull", pull_cmd))
    app.add_handler(CommandHandler("tunnel", tunnel_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()


if __name__ == "__main__":
    main()
