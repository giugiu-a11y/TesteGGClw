#!/usr/bin/env python3
import json
import random
import sys
import time
import traceback

from pytrends.request import TrendReq


def _fetch_trending(pytrends, pn, limit):
    df = pytrends.trending_searches(pn=pn)
    # First column contains trending terms
    col = df.columns[0]
    items = df[col].head(limit).tolist()
    return [
        {"theme": "Trending", "trend": t, "now": 0, "peak": 0}
        for t in items
    ]


def main():
    limit = 10
    retries = 3
    backoff_base = 1.5

    last_err = None
    for attempt in range(retries):
        try:
            pytrends = TrendReq(hl="en-US", tz=0, timeout=(10, 25), retries=1, backoff_factor=0.1)
            brasil = _fetch_trending(pytrends, "brazil", limit)
            mundo = _fetch_trending(pytrends, "united_states", limit)
            out = {
                "brasil": brasil,
                "mundo": mundo,
                "timeframe_br": "daily",
                "timeframe_world": "daily",
                "ok": True,
                "source": "pytrends.trending_searches",
            }
            print(json.dumps(out, ensure_ascii=True))
            return 0
        except Exception as exc:  # noqa: BLE001
            last_err = str(exc)
            try:
                with open("/tmp/virals_trends.err", "w", encoding="utf-8") as f:
                    f.write("Attempt %s\n" % (attempt + 1))
                    f.write(traceback.format_exc())
            except Exception:
                pass
            sleep_s = backoff_base ** (attempt + 1) + random.random()
            time.sleep(sleep_s)

    out = {
        "brasil": [
            {"theme": "Error", "trend": "Google Trends Error", "now": 0, "peak": 0}
        ],
        "mundo": [
            {"theme": "Error", "trend": "Google Trends Error", "now": 0, "peak": 0}
        ],
        "timeframe_br": "unknown",
        "timeframe_world": "unknown",
        "ok": False,
        "error": last_err or "unknown",
    }
    print(json.dumps(out, ensure_ascii=True))
    return 1


if __name__ == "__main__":
    sys.exit(main())
