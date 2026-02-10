#!/usr/bin/env python3
"""
Telegram master ops bot (allowlisted commands only).

Design goals:
- No third-party deps (stdlib only).
- Restrict access by chat_id and (optionally) user_id.
- No arbitrary shell execution; only a small allowlist of commands.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import signal
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text("utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


def _env_int(name: str, default: Optional[int] = None) -> Optional[int]:
    v = os.environ.get(name, "")
    if not v:
        return default
    try:
        return int(v)
    except ValueError:
        raise SystemExit(f"Invalid int env {name}={v!r}")


def _http_json(url: str, data: Optional[dict] = None, timeout: int = 30) -> dict:
    req_data = None
    headers = {"User-Agent": "telegram-master-control/1.0"}
    if data is not None:
        req_data = urllib.parse.urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, data=req_data, headers=headers, method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    return json.loads(raw)


def _run(cmd: list[str], cwd: Optional[str] = None, timeout: int = 60) -> Tuple[int, str]:
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        out = (p.stdout or "") + (("\n" + p.stderr) if p.stderr else "")
        return p.returncode, out.strip()
    except subprocess.TimeoutExpired:
        return 124, f"Timeout after {timeout}s: {' '.join(shlex.quote(x) for x in cmd)}"


def _clip(s: str, max_len: int = 3500) -> str:
    s = s.strip()
    if len(s) <= max_len:
        return s
    return s[: max_len - 50] + "\n...[truncated]...\n" + s[-40:]


@dataclass
class TunnelState:
    server_pid: Optional[int] = None
    tunnel_pid: Optional[int] = None
    url: str = ""
    password: str = ""


class Bot:
    def __init__(self) -> None:
        _load_dotenv(Path(__file__).with_name(".env"))

        self.token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
        if not self.token:
            raise SystemExit("TELEGRAM_BOT_TOKEN missing")

        self.allowed_chat_id = _env_int("TELEGRAM_ALLOWED_CHAT_ID")
        if self.allowed_chat_id is None:
            raise SystemExit("TELEGRAM_ALLOWED_CHAT_ID missing")

        self.allowed_user_id = _env_int("TELEGRAM_ALLOWED_USER_ID", default=None)

        self.repo = os.environ.get("CLAWD_REPO", "/home/ubuntu/clawd")
        self.poke_root = os.environ.get("POKE_ROOT", "/home/ubuntu/clawd/pokemon-game")
        self.poke_port = _env_int("POKE_PORT", default=8000) or 8000
        self.poll_timeout = _env_int("POLL_TIMEOUT_SECONDS", default=25) or 25

        self.api_base = f"https://api.telegram.org/bot{self.token}"
        self.offset = 0
        self.tunnel = TunnelState()

    def _send(self, chat_id: int, text: str) -> None:
        text = _clip(text)
        try:
            _http_json(f"{self.api_base}/sendMessage", {"chat_id": str(chat_id), "text": text})
        except Exception:
            # Avoid crash loops on transient errors.
            pass

    def _is_allowed(self, msg: dict) -> bool:
        try:
            chat_id = int(msg["chat"]["id"])
        except Exception:
            return False
        if chat_id != self.allowed_chat_id:
            return False
        if self.allowed_user_id is None:
            return True
        try:
            user_id = int(msg["from"]["id"])
        except Exception:
            return False
        return user_id == self.allowed_user_id

    def _cmd_help(self) -> str:
        return "\n".join(
            [
                "Commands:",
                "/status",
                "/git_pull",
                "/git_status",
                "/poke_tunnel",
                "/poke_stop",
            ]
        )

    def _cmd_status(self) -> str:
        rc1, head = _run(["git", "rev-parse", "--short", "HEAD"], cwd=self.repo)
        rc2, branch = _run(["git", "branch", "--show-current"], cwd=self.repo)
        git_part = f"git: {branch.strip() if rc2 == 0 else '?'} @ {head.strip() if rc1 == 0 else '?'}"
        t = self.tunnel
        if t.url:
            tun = f"tunnel: {t.url}\npassword: {t.password or '(unknown)'}"
        else:
            tun = "tunnel: (not running)"
        return f"{git_part}\n{tun}"

    def _cmd_git_pull(self) -> str:
        rc, out = _run(["git", "pull", "--rebase", "origin", "main"], cwd=self.repo, timeout=180)
        return f"git pull rc={rc}\n{out or '(no output)'}"

    def _cmd_git_status(self) -> str:
        rc1, st = _run(["git", "status", "--porcelain=v1"], cwd=self.repo)
        rc2, last = _run(["git", "log", "-1", "--oneline"], cwd=self.repo)
        return f"last: {last.strip() if rc2 == 0 else '?'}\nstatus:\n{st if st else '(clean)'}"

    def _poke_start_server(self) -> int:
        # Start python http.server in background
        log_dir = Path(self.poke_root) / ".runtime"
        log_dir.mkdir(parents=True, exist_ok=True)
        server_log = log_dir / "http-server.bot.log"
        p = subprocess.Popen(
            ["python3", "-m", "http.server", str(self.poke_port), "--directory", self.poke_root],
            stdout=server_log.open("ab"),
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        return int(p.pid)

    def _poke_start_tunnel(self) -> Tuple[int, str]:
        log_dir = Path(self.poke_root) / ".runtime"
        log_dir.mkdir(parents=True, exist_ok=True)
        tunnel_log = log_dir / "tunnel.bot.log"

        # Start localtunnel
        p = subprocess.Popen(
            ["npx", "--yes", "localtunnel", "--port", str(self.poke_port)],
            stdout=tunnel_log.open("ab"),
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

        # Scrape URL from log
        deadline = time.time() + 25
        url = ""
        url_re = re.compile(r"https://[a-z0-9-]+\\.loca\\.lt")
        while time.time() < deadline and not url:
            try:
                data = tunnel_log.read_text("utf-8", errors="replace")
            except FileNotFoundError:
                data = ""
            m = url_re.search(data)
            if m:
                url = m.group(0)
                break
            time.sleep(0.5)

        return int(p.pid), url

    def _poke_password(self) -> str:
        try:
            with urllib.request.urlopen("https://loca.lt/mytunnelpassword", timeout=10) as resp:
                return resp.read().decode("utf-8", errors="replace").strip()
        except Exception:
            return ""

    def _cmd_poke_tunnel(self) -> str:
        if self.tunnel.url:
            return f"Already running:\n{self.tunnel.url}\npassword: {self.tunnel.password or '(unknown)'}"

        # Start server + tunnel
        server_pid = self._poke_start_server()
        tunnel_pid, url = self._poke_start_tunnel()
        password = self._poke_password()

        self.tunnel = TunnelState(server_pid=server_pid, tunnel_pid=tunnel_pid, url=url, password=password)

        if not url:
            return (
                "Started, but could not capture tunnel URL yet.\n"
                f"Check: {self.poke_root}/.runtime/tunnel.bot.log"
            )

        return f"LINK:\n{url}\n\nSENHA:\n{password or '(unknown)'}"

    def _kill_pid(self, pid: int) -> None:
        try:
            os.killpg(pid, signal.SIGTERM)
        except Exception:
            try:
                os.kill(pid, signal.SIGTERM)
            except Exception:
                pass

    def _cmd_poke_stop(self) -> str:
        t = self.tunnel
        if not t.server_pid and not t.tunnel_pid:
            self.tunnel = TunnelState()
            return "Not running."

        if t.tunnel_pid:
            self._kill_pid(t.tunnel_pid)
        if t.server_pid:
            self._kill_pid(t.server_pid)

        self.tunnel = TunnelState()
        return "Stopped."

    def _handle(self, msg: dict) -> str:
        text = (msg.get("text") or "").strip()
        if not text:
            return ""

        cmd = text.split()[0].lower()
        if cmd in ("/start", "/help"):
            return self._cmd_help()
        if cmd == "/status":
            return self._cmd_status()
        if cmd == "/git_pull":
            return self._cmd_git_pull()
        if cmd == "/git_status":
            return self._cmd_git_status()
        if cmd == "/poke_tunnel":
            return self._cmd_poke_tunnel()
        if cmd == "/poke_stop":
            return self._cmd_poke_stop()
        return "Unknown command.\n\n" + self._cmd_help()

    def loop(self) -> None:
        print("telegram-master-control: polling...")
        while True:
            try:
                data = _http_json(
                    f"{self.api_base}/getUpdates",
                    {"timeout": str(self.poll_timeout), "offset": str(self.offset)},
                    timeout=self.poll_timeout + 10,
                )
                for upd in data.get("result", []):
                    self.offset = max(self.offset, int(upd.get("update_id", 0)) + 1)
                    msg = upd.get("message") or upd.get("edited_message")
                    if not msg:
                        continue
                    if not self._is_allowed(msg):
                        # Ignore silently
                        continue
                    chat_id = int(msg["chat"]["id"])
                    resp = self._handle(msg)
                    if resp:
                        self._send(chat_id, resp)
            except urllib.error.URLError:
                time.sleep(2)
            except Exception:
                time.sleep(1)


def main() -> None:
    Bot().loop()


if __name__ == "__main__":
    main()

