#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fetch trends/virais data:
- Google Trends daily RSS (BR)
- YouTube search (top viewCount) for defined topics (optional if API key exists)

Output: /tmp/briefing-virais.json
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

OUTPUT = "/tmp/briefing-virais.json"

TOPICS = [
    "bolsa de estudo",
    "bolsas de estudo exterior",
    "intercâmbio",
    "exchange student",
    "carreira internacional",
    "trabalho remoto",
    "estudar fora",
    "visa estudante",
    "scholarship",
    "study abroad",
    "remote work",
]

TRENDS_RSS = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=BR"


def _http_get(url: str, timeout: int = 10) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "briefings/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_google_trends() -> list[dict]:
    rss_urls = [
        TRENDS_RSS,
        "https://trends.google.com/trends/trendingsearches/daily/rss?geo=BR&hl=pt-BR",
    ]
    for url in rss_urls:
        try:
            xml_text = _http_get(url)
            root = ET.fromstring(xml_text)
            items = []
            for item in root.findall(".//item"):
                title = (item.findtext("title") or "").strip()
                link = (item.findtext("link") or "").strip()
                traffic = ""
                # Google Trends RSS uses ht:approx_traffic, but namespace can vary.
                for child in item:
                    if child.tag.endswith("approx_traffic"):
                        traffic = (child.text or "").strip()
                        break
                if not title:
                    continue
                items.append({
                    "query": title,
                    "traffic": traffic,
                    "link": link,
                    "source": "google_trends_rss",
                })
            if items:
                return items[:10]
        except Exception:
            continue

    # Fallback: dailytrends API
    try:
        api_url = "https://trends.google.com/trends/api/dailytrends?geo=BR&hl=pt-BR"
        raw = _http_get(api_url)
        if raw.startswith(")]}'"):
            raw = raw.split("\n", 1)[1]
        data = json.loads(raw)
        days = data.get("default", {}).get("trendingSearchesDays", [])
        if not days:
            raise ValueError("no_trending_days")
        searches = days[0].get("trendingSearches", [])
        items = []
        for s in searches:
            title = s.get("title", {}).get("query", "")
            if not title:
                continue
            items.append({
                "query": title,
                "traffic": s.get("formattedTraffic", ""),
                "link": s.get("shareUrl", ""),
                "source": "google_trends_api",
            })
        return items[:10]
    except Exception as e:
        return [{"error": f"google_trends_failed: {e}"}]


def _youtube_api_key() -> str:
    return (os.getenv("YOUTUBE_API_KEY") or os.getenv("GOOGLE_API_KEY") or "").strip()


def _youtube_search(topic: str, api_key: str, published_after: str) -> list[dict]:
    params = {
        "part": "snippet",
        "type": "video",
        "maxResults": "5",
        "order": "viewCount",
        "q": topic,
        "publishedAfter": published_after,
        "key": api_key,
    }
    url = "https://www.googleapis.com/youtube/v3/search?" + urllib.parse.urlencode(params)
    data = json.loads(_http_get(url))
    items = data.get("items") or []
    ids = [i.get("id", {}).get("videoId") for i in items if i.get("id", {}).get("videoId")]
    if not ids:
        return []

    v_params = {
        "part": "snippet,statistics",
        "id": ",".join(ids),
        "key": api_key,
    }
    v_url = "https://www.googleapis.com/youtube/v3/videos?" + urllib.parse.urlencode(v_params)
    v_data = json.loads(_http_get(v_url))
    out = []
    for v in v_data.get("items") or []:
        stats = v.get("statistics") or {}
        snippet = v.get("snippet") or {}
        vid = v.get("id")
        if not vid:
            continue
        out.append({
            "title": snippet.get("title", ""),
            "channel": snippet.get("channelTitle", ""),
            "publishedAt": snippet.get("publishedAt", ""),
            "views": int(stats.get("viewCount", "0") or 0),
            "url": f"https://www.youtube.com/watch?v={vid}",
            "topic": topic,
            "source": "youtube_api",
        })
    return out


def fetch_youtube() -> list[dict]:
    api_key = _youtube_api_key()
    results = []
    if api_key:
        published_after = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        for topic in TOPICS:
            try:
                results.extend(_youtube_search(topic, api_key, published_after))
                time.sleep(0.2)
            except Exception as e:
                results.append({"error": f"youtube_search_failed:{topic}:{e}"})

        # Keep top 8 by views
        results = [r for r in results if isinstance(r, dict) and "views" in r]
        results.sort(key=lambda x: x.get("views", 0), reverse=True)

    if results:
        return results[:8]

    # Fallback: HTML search sorted by view count (no API key needed)
    html_results = []
    for topic in TOPICS:
        try:
            html_results.extend(_youtube_search_html(topic))
            time.sleep(0.2)
        except Exception as e:
            html_results.append({"error": f"youtube_html_failed:{topic}:{e}"})

    return html_results[:8] if html_results else [{"error": "youtube_no_data"}]


def _youtube_search_html(topic: str) -> list[dict]:
    params = {
        "search_query": topic,
        # Sort by view count
        "sp": "CAM%3D",
    }
    url = "https://www.youtube.com/results?" + urllib.parse.urlencode(params, safe="%")
    html = _http_get(url)

    def extract_json_blob(text: str) -> dict:
        markers = ["var ytInitialData = ", "ytInitialData = ", "window[\"ytInitialData\"] = "]
        for marker in markers:
            idx = text.find(marker)
            if idx == -1:
                continue
            start = text.find("{", idx + len(marker))
            if start == -1:
                continue
            # brace matching
            depth = 0
            in_str = False
            esc = False
            for i in range(start, len(text)):
                ch = text[i]
                if in_str:
                    if esc:
                        esc = False
                    elif ch == "\\":
                        esc = True
                    elif ch == "\"":
                        in_str = False
                else:
                    if ch == "\"":
                        in_str = True
                    elif ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            blob = text[start:i+1]
                            return json.loads(blob)
            break
        return {}

    data = extract_json_blob(html)
    titles = []

    def walk(obj):
        if isinstance(obj, dict):
            if "videoRenderer" in obj:
                vr = obj.get("videoRenderer") or {}
                title_runs = (vr.get("title") or {}).get("runs") or []
                if title_runs:
                    t = title_runs[0].get("text", "")
                    if t:
                        titles.append(t)
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)

    walk(data)

    stop = {"Search filters", "Keyboard shortcuts", "Playback", "Sign in", "Search", "YouTube"}
    out = []
    seen = set()
    for title in titles:
        if title in seen or title in stop:
            continue
        seen.add(title)
        out.append({
            "title": title,
            "topic": topic,
            "source": "youtube_html",
        })
        if len(out) >= 3:
            break
    return out


def fetch_tiktok() -> list[dict]:
    # TikTok Creative Center (hashtags)
    url = "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en?country=BR"
    try:
        html = _http_get(url)
        m = re.search(r'__NEXT_DATA__\" type=\"application/json\">(.*?)</script>', html)
        if not m:
            return [{"error": "tiktok_no_next_data"}]
        data = json.loads(m.group(1))
        tags = []

        def walk(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == "hashtagList" and isinstance(v, list):
                        for item in v:
                            name = item.get("hashtagName") or item.get("hashtag") or ""
                            if name:
                                tags.append(name)
                    else:
                        walk(v)
            elif isinstance(obj, list):
                for v in obj:
                    walk(v)

        walk(data)
        tags = list(dict.fromkeys(tags))  # de-dup, preserve order
        if not tags:
            return [{"error": "tiktok_no_tags"}]
        return [{"title": f"#{t}", "source": "tiktok_creative_center"} for t in tags[:8]]
    except Exception as e:
        return [{"error": f"tiktok_failed:{e}"}]


def main() -> int:
    cached = None
    if os.path.exists(OUTPUT):
        try:
            with open(OUTPUT, "r", encoding="utf-8") as f:
                cached = json.load(f)
        except Exception:
            cached = None

    payload = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "google_trends": fetch_google_trends(),
        "youtube_top": fetch_youtube(),
        "tiktok_trends": fetch_tiktok(),
        "topics": TOPICS,
    }

    def _has_queries(items):
        return any(isinstance(i, dict) and i.get("query") for i in (items or []))

    def _has_titles(items):
        return any(isinstance(i, dict) and i.get("title") for i in (items or []))

    if cached:
        if not _has_queries(payload.get("google_trends")) and _has_queries(cached.get("google_trends")):
            payload["google_trends"] = cached.get("google_trends")
        if not _has_titles(payload.get("youtube_top")) and _has_titles(cached.get("youtube_top")):
            payload["youtube_top"] = cached.get("youtube_top")
        if not _has_titles(payload.get("tiktok_trends")) and _has_titles(cached.get("tiktok_trends")):
            payload["tiktok_trends"] = cached.get("tiktok_trends")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
