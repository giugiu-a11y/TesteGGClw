#!/usr/bin/env python3
import json
import sys
import time
import xml.etree.ElementTree as ET


def parse(path):
    with open(path, "rb") as f:
        data = f.read()
    root = ET.fromstring(data)
    items = []
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        if title:
            items.append({"theme": "Trending", "trend": title, "now": 0, "peak": 0})
    return items


def main():
    if len(sys.argv) < 2:
        print("[]")
        return 0
    path = sys.argv[1]
    items = parse(path)
    print(json.dumps({"items": items, "fetched_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
