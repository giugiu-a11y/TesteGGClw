#!/usr/bin/env python3
import json
import os
import re
import sys
import urllib.parse

try:
    import requests
except Exception:
    requests = None

try:
    from requests_oauthlib import OAuth1Session
except Exception:
    OAuth1Session = None


def load_env_file(path):
    if not path or not os.path.exists(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" not in line or line.strip().startswith("#"):
                    continue
                k, v = line.strip().split("=", 1)
                if k and k not in os.environ:
                    os.environ[k] = v
    except Exception:
        pass


def oauth1_session():
    ck = os.environ.get("TWITTER_CONSUMER_KEY")
    cs = os.environ.get("TWITTER_CONSUMER_SECRET")
    at = os.environ.get("TWITTER_ACCESS_TOKEN")
    ats = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
    if not all([ck, cs, at, ats]) or OAuth1Session is None:
        return None
    return OAuth1Session(ck, client_secret=cs, resource_owner_key=at, resource_owner_secret=ats)


def bearer_headers():
    token = os.environ.get("TWITTER_BEARER_TOKEN")
    if not token:
        return None
    t = token.strip()
    if t.startswith("${") or "$" in t:
        return None
    return {"Authorization": f"Bearer {t}"}


def parse_items(payload, limit):
    min_score = int(os.environ.get("TWITTER_MIN_SCORE", "0") or "0")
    langs = [p.strip().lower() for p in os.environ.get("TWITTER_LANGS", "").split(",") if p.strip()]
    require_terms = [p.strip().lower() for p in os.environ.get("TWITTER_REQUIRE_TERMS", "").split(",") if p.strip()]
    data = payload.get("data") or []
    users = {u.get("id"): u.get("username") for u in (payload.get("includes", {}).get("users") or [])}
    out = []
    url_re = re.compile(r"(https?://\S+|www\.\S+)")
    for item in data:
        lang = (item.get("lang") or "").lower()
        if langs and lang and lang not in langs:
            continue
        metrics = item.get("public_metrics") or {}
        likes = metrics.get("like_count", 0)
        retweets = metrics.get("retweet_count", 0)
        replies = metrics.get("reply_count", 0)
        quotes = metrics.get("quote_count", 0)
        score = likes + retweets
        author = users.get(item.get("author_id"), "i")
        text = (item.get("text") or "").replace("\n", " ").strip()
        if text.startswith("RT @"):
            continue
        text = url_re.sub("", text)
        text = re.sub(r"\s+", " ", text).strip()
        text_l = text.lower()
        if require_terms and not any(t in text_l for t in require_terms):
            continue
        if score < min_score:
            continue
        out.append(
            {
                "title": text[:120],
                "likes": likes,
                "retweets": retweets,
                "replies": replies,
                "quotes": quotes,
                "score": score,
                "url": f"https://x.com/{author}/status/{item.get('id')}",
                "source": "Twitter",
            }
        )
    out.sort(key=lambda x: x.get("score", 0), reverse=True)
    return out[:limit]


def fetch_recent(query, limit):
    if requests is None:
        return []
    langs = os.environ.get("TWITTER_LANGS", "en,pt").strip()
    max_age_hours = int(os.environ.get("TWITTER_MAX_AGE_HOURS", "24") or "24")
    start_time = None
    try:
        from datetime import datetime, timedelta, timezone
        start_time = (datetime.now(timezone.utc) - timedelta(hours=max_age_hours)).isoformat().replace("+00:00", "Z")
    except Exception:
        start_time = None
    lang_filter = ""
    if langs:
        parts = [p.strip() for p in langs.split(",") if p.strip()]
        if parts:
            lang_filter = "(" + " OR ".join([f"lang:{p}" for p in parts]) + ")"
    full_query = f"{query} -is:retweet -is:reply"
    if lang_filter:
        full_query = f"{full_query} {lang_filter}"
    enc = urllib.parse.quote(full_query)
    max_results = max(10, min(100, int(limit) * 10))
    url = (
        "https://api.twitter.com/2/tweets/search/recent"
        f"?query={enc}&max_results={max_results}&sort_order=relevancy"
        "&tweet.fields=public_metrics,created_at,lang"
        "&expansions=author_id&user.fields=username"
    )
    if start_time:
        url = url + f"&start_time={urllib.parse.quote(start_time)}"
    headers = bearer_headers()
    if headers:
        resp = requests.get(url, headers=headers, timeout=12)
    else:
        session = oauth1_session()
        if session is None:
            return []
        resp = session.get(url, timeout=12)
    if resp.status_code != 200:
        if os.environ.get("DEBUG_TWITTER") == "1":
            sys.stderr.write(f"twitter_api status={resp.status_code}\n")
            sys.stderr.write((resp.text or "")[:500] + "\n")
        return []
    try:
        payload = resp.json()
    except Exception:
        return []
    if os.environ.get("DEBUG_TWITTER") == "1" and payload.get("data"):
        try:
            first = payload["data"][0]
            sys.stderr.write("twitter_api sample keys: " + ",".join(sorted(first.keys())) + "\n")
            sys.stderr.write("public_metrics: " + json.dumps(first.get("public_metrics")) + "\n")
        except Exception:
            pass
    return parse_items(payload, limit)


def main():
    if len(sys.argv) < 2:
        print("[]")
        return 0
    query = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    env_file = os.environ.get("TWITTER_ENV_FILE")
    if env_file:
        load_env_file(env_file)
    items = fetch_recent(query, limit)
    print(json.dumps(items, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
