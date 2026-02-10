#!/usr/bin/env python3
import json
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None
import subprocess
import requests

CONFIG_PATH = Path("/home/ubuntu/.openclaw/openclaw.json")
SESSIONS_PATH = Path("/home/ubuntu/.openclaw/agents/main/sessions/sessions.json")
STATE_PATH = Path("/tmp/openclaw_usage_report_state.json")
ENV_ASSISTENTE = Path("/home/ubuntu/clawd/sessions/assistente-opus/.env.assistente")
BRIEFINGS_USAGE = Path("/tmp/briefings_llm_usage.jsonl")
JESUS_LOG = Path("/home/ubuntu/clawd/sessions/personajes/logs/posting.log")
JESUS_ERR = Path("/home/ubuntu/clawd/sessions/personajes/logs/error.log")
VAGAS_LOG = Path("/home/ubuntu/projects/job-curator-bot/logs/post_next.log")
ASSISTENTE_OPUS_PROC = "/home/ubuntu/clawd/sessions/assistente-opus/bot.py"


def load_env(path: Path):
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        v = v.strip().strip("\"'")
        os.environ[k] = v


def systemctl_active():
    try:
        out = subprocess.check_output(
            ["systemctl", "--user", "is-active", "openclaw-gateway.service"],
            text=True,
        ).strip()
        return out
    except Exception:
        return "unknown"


def read_json(path: Path, default):
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def format_dt(ts: str):
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return "n/a"


def fmt_dt_local(dt: datetime):
    try:
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return "n/a"


def count_briefing_logs(kind: str, cutoff: datetime):
    # /tmp/{kind}-briefing-YYYYMMDD_HHMMSS.log
    from glob import glob
    total = 0
    for p in glob(f"/tmp/{kind}-briefing-*.log"):
        name = Path(p).name
        try:
            ts = name.split("-briefing-")[1].split(".log")[0]
            dt = datetime.strptime(ts, "%Y%m%d_%H%M%S").replace(tzinfo=timezone.utc)
        except Exception:
            continue
        if dt >= cutoff:
            total += 1
    return total


def proc_running(match: str) -> bool:
    try:
        out = subprocess.check_output(["pgrep", "-af", match], text=True)
        return bool(out.strip())
    except Exception:
        return False


def last_mtime(path: Path):
    try:
        return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    except Exception:
        return None


def main():
    load_env(ENV_ASSISTENTE)
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("ALLOWED_USER_ID") or os.environ.get("BOT_ASSISTENTE_CHAT")
    if not token or not chat_id:
        return 1

    cfg = read_json(CONFIG_PATH, {})
    sessions = read_json(SESSIONS_PATH, {}) if SESSIONS_PATH.exists() else {}

    total_tokens = 0
    window_tokens = 0
    session_rows = []
    last_updated = None
    last_updated_window = None
    model_totals = {}
    model_totals_window = {}
    channel_totals_window = {}
    kind_totals_window = {}
    now_utc = datetime.now(timezone.utc)
    cutoff = now_utc - timedelta(hours=24)
    for sid, s in sessions.items():
        tt = int(s.get("totalTokens") or 0)
        total_tokens += tt
        updated = s.get("updatedAt")
        updated_dt = None
        if updated:
            try:
                updated_dt = datetime.fromtimestamp(updated/1000, tz=timezone.utc)
            except Exception:
                updated_dt = None
        if updated and (last_updated is None or updated > last_updated):
            last_updated = updated
        # fallback: use session file mtime if updatedAt missing
        sf = s.get("sessionFile")
        if (not updated) and sf:
            try:
                mtime_dt = datetime.fromtimestamp(Path(sf).stat().st_mtime, tz=timezone.utc)
                if last_updated is None or mtime_dt.isoformat() > str(last_updated):
                    last_updated = mtime_dt.isoformat()
                if updated_dt is None:
                    updated_dt = mtime_dt
            except Exception:
                pass
        model = s.get("model") or "unknown"
        model_totals[model] = model_totals.get(model, 0) + tt
        if updated_dt and updated_dt >= cutoff:
            window_tokens += tt
            model_totals_window[model] = model_totals_window.get(model, 0) + tt
            if (last_updated_window is None) or (updated_dt > last_updated_window):
                last_updated_window = updated_dt
            # channel + kind for last 24h
            channel = None
            try:
                channel = (s.get("deliveryContext") or {}).get("channel")
            except Exception:
                channel = None
            if not channel:
                try:
                    channel = (s.get("origin") or {}).get("provider")
                except Exception:
                    channel = None
            if not channel:
                channel = "unknown"
            channel_totals_window[channel] = channel_totals_window.get(channel, 0) + tt
            kind = "cron" if ":cron:" in sid else "main"
            kind_totals_window[kind] = kind_totals_window.get(kind, 0) + tt
        session_rows.append((tt, sid, model, updated))

    session_rows.sort(reverse=True)
    # Top models by tokens in last 24h (max 5)
    top_models = sorted(model_totals_window.items(), key=lambda x: x[1], reverse=True)[:5]
    top_channels = sorted(channel_totals_window.items(), key=lambda x: x[1], reverse=True)[:5]
    top_kinds = sorted(kind_totals_window.items(), key=lambda x: x[1], reverse=True)[:5]

    STATE_PATH.write_text(json.dumps({"total_tokens_24h": window_tokens, "ts": datetime.now(timezone.utc).isoformat()}))

    agent_defaults = (cfg.get("agents") or {}).get("defaults") or {}
    max_conc = agent_defaults.get("maxConcurrent")
    sub_conc = (agent_defaults.get("subagents") or {}).get("maxConcurrent")
    memory_slot = ((cfg.get("plugins") or {}).get("slots") or {}).get("memory")
    cooldowns = (cfg.get("auth") or {}).get("cooldowns") or {}

    # Briefings (Gemini direct) usage
    brief_calls = 0
    brief_tokens = 0
    brief_tokens_known = False
    if BRIEFINGS_USAGE.exists():
        for line in BRIEFINGS_USAGE.read_text().splitlines():
            try:
                row = json.loads(line)
            except Exception:
                continue
            ts = row.get("ts")
            if not ts:
                continue
            try:
                ts_dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except Exception:
                continue
            if ts_dt < cutoff:
                continue
            brief_calls += 1
            usage = row.get("usage") or {}
            # Gemini usage metadata usually has prompt_token_count / candidates_token_count / total_token_count
            total = usage.get("total_token_count")
            if total is None:
                # try other common keys
                total = usage.get("total_tokens") or usage.get("totalTokens")
            if isinstance(total, int):
                brief_tokens += total
                brief_tokens_known = True

    # Briefings runs (last 24h)
    news_runs = count_briefing_logs("news", cutoff)
    market_runs = count_briefing_logs("market", cutoff)
    virals_runs = count_briefing_logs("virals", cutoff)

    # Other bots (no LLM)
    assistente_opus_running = proc_running(ASSISTENTE_OPUS_PROC)
    jesus_last = last_mtime(JESUS_LOG)
    vagas_last = last_mtime(VAGAS_LOG)

    lines = []
    tz = ZoneInfo("America/Sao_Paulo") if ZoneInfo else timezone.utc
    lines.append("📊 OpenClaw — Relatório Diário")
    lines.append(f"Data: {datetime.now(tz).strftime('%Y-%m-%d')} (BRT)")
    lines.append("")
    lines.append(f"Gateway: {systemctl_active()}")
    lines.append("Janela: últimas 24h")
    lines.append(f"Tokens total (24h): {window_tokens}")
    lines.append("")
    if top_models:
        lines.append("Top modelos (tokens):")
        for model, tt in top_models:
            if model == "unknown" or tt == 0:
                continue
            lines.append(f"- {model}: {tt}")
        lines.append("")
    if top_channels:
        lines.append("Top canais (tokens):")
        for ch, tt in top_channels:
            if ch == "unknown" or tt == 0:
                continue
            lines.append(f"- {ch}: {tt}")
        lines.append("")
    if top_kinds:
        lines.append("Top origens (tokens):")
        for k, tt in top_kinds:
            if tt == 0:
                continue
            lines.append(f"- {k}: {tt}")
        lines.append("")
    # Briefings summary (Gemini direct)
    lines.append("Briefings (24h):")
    lines.append(f"- execuções: news={news_runs}, market={market_runs}, virals={virals_runs}")
    if brief_calls == 0:
        lines.append("- LLM: 0 chamadas")
    else:
        if brief_tokens_known:
            lines.append(f"- LLM: {brief_calls} chamadas | {brief_tokens} tokens")
        else:
            lines.append(f"- LLM: {brief_calls} chamadas | tokens: sem dados")
    lines.append("")

    lines.append("Outros bots (24h):")
    lines.append(f"- assistente-opus: {'rodando' if assistente_opus_running else 'parado'}")
    if jesus_last:
        lines.append(f"- jesus sincero: última postagem {fmt_dt_local(jesus_last)}")
    else:
        lines.append("- jesus sincero: sem dados")
    if vagas_last:
        lines.append(f"- vagas remotas: última postagem {fmt_dt_local(vagas_last)}")
    else:
        lines.append("- vagas remotas: sem dados")

    msg = "\n".join(lines)

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": msg, "disable_web_page_preview": True}
    r = requests.post(url, json=payload, timeout=20)
    return 0 if r.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
