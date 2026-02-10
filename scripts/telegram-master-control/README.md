# Telegram Master Control (Ops Bot)

This is a small Telegram bot that lets you run a few **allowlisted** ops commands on this AWS box (push/pull, start/stop Pokemon tunnel, etc).

It does **not** magically turn "Codex" into Telegram. It just automates the repetitive terminal steps and sends the output back to Telegram.

## Setup

1. Create a bot with @BotFather and get `TELEGRAM_BOT_TOKEN`.
2. Get your chat id (or your private user id) and set allowlists.
3. Create `.env` (do NOT commit it):

```bash
cd /home/ubuntu/clawd/scripts/telegram-master-control
cp .env.example .env
nano .env
```

4. Run:

```bash
python3 bot.py
```

## Commands

- `/start` help
- `/status` shows git + tunnel status
- `/git_pull` `git pull --rebase origin main` in `/home/ubuntu/clawd`
- `/git_status` short status + last commit
- `/poke_tunnel` starts `/home/ubuntu/clawd/pokemon-game` http server + localtunnel and returns `URL + password`
- `/poke_stop` stops the running pokemon server/tunnel (if started by this bot)

## Security Notes

- Lock it down with `TELEGRAM_ALLOWED_CHAT_ID` and ideally `TELEGRAM_ALLOWED_USER_ID`.
- Do not add this bot to large groups.
- This bot intentionally does not support arbitrary shell commands.

