#!/usr/bin/env python3
import sys, json, subprocess, hashlib, os

DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN = os.path.join(DIR, "clean.py")
DECIDE = os.path.join(DIR, "decide.py")
CACHE_MOD = os.path.join(DIR, "hash_cache.py")

TTL_DECIDE = 14 * 24 * 3600  # 14 dias

def run(cmd, input_text):
    p = subprocess.run(cmd, input=input_text.encode("utf-8"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout.decode("utf-8", errors="replace"), p.stderr.decode("utf-8", errors="replace")

def cache_load(kind, h):
    code = f"""
import importlib.util, json
spec=importlib.util.spec_from_file_location("hc","{CACHE_MOD}")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
v=m.load("{kind}","{h}")
print(json.dumps(v) if v is not None else "")
"""
    p = subprocess.run([sys.executable, "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s = p.stdout.decode("utf-8", errors="replace").strip()
    if not s:
        return None
    return json.loads(s)

def cache_save(kind, h, obj, ttl):
    payload = json.dumps(obj, ensure_ascii=False)
    code = f"""
import importlib.util, json
spec=importlib.util.spec_from_file_location("hc","{CACHE_MOD}")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.save("{kind}","{h}",json.loads({payload!r}),{ttl})
print("OK")
"""
    subprocess.run([sys.executable, "-c", code], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    raw = sys.stdin.read()
    if not raw.strip():
        print(json.dumps({"error":"empty_input"}))
        return 1

    rc, out, err = run([CLEAN], raw)
    if rc != 0:
        print(json.dumps({"error":"clean_failed","clean_stderr": err[-2000:]}))
        return 2

    cj = json.loads(out)
    clean_text = cj.get("clean_text","")
    meta = cj.get("meta",{})

    h = hashlib.sha256(clean_text.encode("utf-8")).hexdigest()

    cached = cache_load("decide", h)
    if cached is not None:
        print(json.dumps({"ok": True, "cached": True, "meta": meta, "result": cached}, ensure_ascii=False))
        return 0

    prompt = json.dumps({
        "clean_text": clean_text,
        "meta": meta,
        "task": "decida ações e devolva JSON curto"
    }, ensure_ascii=False)

    rc, out, err = run([DECIDE], prompt)
    if rc != 0:
        detail = None
        try:
            detail = json.loads(out) if out.strip().startswith("{") else {"raw": out[-2000:]}
        except Exception:
            detail = {"raw": out[-2000:]}
        print(json.dumps({
            "ok": False,
            "error":"decide_failed",
            "meta": meta,
            "decide_detail": detail,
            "decide_stderr": err[-2000:]
        }, ensure_ascii=False))
        return 3

    result = json.loads(out)
    cache_save("decide", h, result, TTL_DECIDE)

    print(json.dumps({"ok": True, "cached": False, "meta": meta, "result": result}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
