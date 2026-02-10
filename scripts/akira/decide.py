#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
import time
import random
import urllib.request
import urllib.error


API_HOST = "https://generativelanguage.googleapis.com"
API_VERSION = os.environ.get("GEMINI_API_VERSION", "v1beta").strip() or "v1beta"
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-lite").strip() or "gemini-2.5-flash-lite"
TIMEOUT_S = float(os.environ.get("GEMINI_TIMEOUT_S", "30"))

# No máximo 2 tentativas no total (0 e 1).
MAX_TOTAL_ATTEMPTS = 2
BASE_BACKOFF_S = float(os.environ.get("GEMINI_BACKOFF_BASE_S", "0.8"))
MAX_BACKOFF_S = float(os.environ.get("GEMINI_BACKOFF_MAX_S", "8.0"))
JITTER_S = float(os.environ.get("GEMINI_BACKOFF_JITTER_S", "0.25"))


def _log(msg: str) -> None:
    print(msg, file=sys.stderr)


def _sleep_with_backoff(attempt: int, reason: str) -> None:
    base = BASE_BACKOFF_S * (2 ** attempt)
    wait = min(MAX_BACKOFF_S, base) + random.uniform(0.0, JITTER_S)
    _log(f"[akira-decide] tentativa {attempt + 1}/{MAX_TOTAL_ATTEMPTS} falhou ({reason}); aguardando {wait:.2f}s")
    time.sleep(wait)


def _stdout_json(obj: dict) -> None:
    # stdout: sempre 1 linha de JSON válido. Nada além disso.
    sys.stdout.write(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def _fail(code: str, details: str = "") -> None:
    _stdout_json({"error": code, "details": (details or "")[:2000]})
    sys.exit(1)


def _read_stdin_json() -> dict:
    raw = sys.stdin.read()
    if raw is None or raw.strip() == "":
        _fail("EMPTY_STDIN", "stdin vazio")
    try:
        return json.loads(raw)
    except Exception as e:
        _fail("INVALID_INPUT_JSON", f"stdin não é JSON válido: {e}")


def _build_prompt(payload: dict) -> str:
    clean_text = payload.get("clean_text", "")
    task = payload.get("task", "")
    meta = payload.get("meta", {})

    # Contrato do pipeline: este script deve devolver JSON (1 linha).
    # Força o modelo a responder só JSON.
    return (
        "Responda APENAS com 1 linha de JSON válido. Sem markdown, sem texto extra.\n"
        "Se não der para cumprir, responda com JSON de erro no formato "
        '{"error":"MODEL_CANNOT_COMPLY","details":"..."}.\n\n'
        f"TAREFA:\n{task}\n\n"
        f"TEXTO (clean_text):\n{clean_text}\n\n"
        f"META:\n{json.dumps(meta, ensure_ascii=False, separators=(',', ':'))}\n"
    )


def _extract_text(resp_obj: dict) -> str:
    # Estrutura típica: candidates[0].content.parts[0].text
    cands = resp_obj.get("candidates") or []
    if not cands:
        return ""
    content = (cands[0] or {}).get("content") or {}
    parts = content.get("parts") or []
    if not parts:
        return ""
    text = (parts[0] or {}).get("text")
    return text if isinstance(text, str) else ""


def _clean_model_text(text: str) -> str:
    t = (text or "").strip()

    # Remove fences comuns.
    if t.startswith("```"):
        lines = t.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        t = "\n".join(lines).strip()

    # Garante JSON em 1 linha (compacta).
    try:
        obj = json.loads(t)
    except Exception:
        return ""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def _http_post_json(url: str, body_obj: dict, headers: dict, timeout_s: float) -> dict:
    data = json.dumps(body_obj, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        resp_bytes = resp.read()
    try:
        return json.loads(resp_bytes.decode("utf-8", errors="replace"))
    except Exception:
        return {"_raw": resp_bytes.decode("utf-8", errors="replace")}


def _call_gemini(prompt: str, api_key: str) -> dict:
    url = f"{API_HOST}/{API_VERSION}/models/{MODEL}:generateContent?key={api_key}"

    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.0,
            "maxOutputTokens": int(os.environ.get("GEMINI_MAX_TOKENS", "512")),
        },
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "akira-decide/1.0",
    }
    return _http_post_json(url, body, headers, TIMEOUT_S)


def main() -> None:
    payload = _read_stdin_json()

    api_key = os.environ.get("GOOGLE_API_KEY", "")
    api_key = api_key.strip() if isinstance(api_key, str) else ""

    if not api_key:
        # stderr só texto simples. stdout carrega o JSON de erro.
        print("GOOGLE_API_KEY ausente", file=sys.stderr)
        _fail("GEMINI_API_KEY_MISSING", "GOOGLE_API_KEY/GEMINI_API_KEY não definido no ambiente")

    prompt = _build_prompt(payload)

    last_err = ""
    for attempt in range(MAX_TOTAL_ATTEMPTS):
        try:
            resp_obj = _call_gemini(prompt, api_key)

            # Erros da API costumam vir em {"error": {...}}
            if isinstance(resp_obj, dict) and "error" in resp_obj:
                err = resp_obj.get("error") or {}
                code = str(err.get("code") or "")
                msg = str(err.get("message") or "")
                status = str(err.get("status") or "")
                last_err = f"api error code={code} status={status} message={msg}".strip()

                # Retry só na primeira falha, e só para classes plausíveis de rede/quota.
                if attempt == 0 and (code in {"429", "500", "503"} or status in {"RESOURCE_EXHAUSTED", "UNAVAILABLE"}):
                    _sleep_with_backoff(attempt, "api_error")
                    continue

                _fail("GEMINI_API_ERROR", last_err)

            text = _extract_text(resp_obj if isinstance(resp_obj, dict) else {})
            one_line_json = _clean_model_text(text)

            if not one_line_json:
                last_err = "modelo não retornou JSON válido"
                _fail("MODEL_RETURNED_NON_JSON", last_err)

            # Sucesso: stdout 1 linha JSON válido, exit 0.
            sys.stdout.write(one_line_json + "\n")
            sys.stdout.flush()
            sys.exit(0)

        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode("utf-8", errors="replace")
            except Exception:
                body = ""
            last_err = f"http {getattr(e, 'code', '')} {getattr(e, 'reason', '')} {body}".strip()

            if attempt + 1 < MAX_TOTAL_ATTEMPTS and getattr(e, "code", None) in (429, 500, 503):
                _sleep_with_backoff(attempt, "http_error")
                continue

            _fail("GEMINI_API_NETWORK_ERROR", last_err)

        except urllib.error.URLError as e:
            last_err = f"url error: {e}".strip()
            if attempt + 1 < MAX_TOTAL_ATTEMPTS:
                _sleep_with_backoff(attempt, "url_error")
                continue
            _fail("GEMINI_API_NETWORK_ERROR", last_err)

        except Exception as e:
            last_err = f"exception: {e}".strip()
            if attempt + 1 < MAX_TOTAL_ATTEMPTS:
                _sleep_with_backoff(attempt, "exception")
                continue
            _fail("GEMINI_API_NETWORK_ERROR", last_err)

    _fail("GEMINI_API_NETWORK_ERROR", last_err or "falha desconhecida")


if __name__ == "__main__":
    main()
