#!/usr/bin/env python3
import json
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime


def _strip_ns(tag):
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _parse_date(value):
    if not value:
        return None
    try:
        return parsedate_to_datetime(value).astimezone(timezone.utc)
    except Exception:
        try:
            v = value.replace("Z", "+00:00")
            return datetime.fromisoformat(v).astimezone(timezone.utc)
        except Exception:
            return None


def parse(source, limit=10, max_age_hours=None):
    if source == "-":
        data = sys.stdin.buffer.read().replace(b"\x00", b"")
    else:
        with open(source, "rb") as f:
            data = f.read().replace(b"\x00", b"")
    root = ET.fromstring(data)
    items = []
    cutoff = None
    if max_age_hours is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
    root_tag = _strip_ns(root.tag)
    if root_tag == "feed":
        # Atom feed (e.g., Reddit)
        for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
            title = (entry.findtext("{http://www.w3.org/2005/Atom}title") or "").replace("\n", " ").strip()
            link = ""
            updated = (entry.findtext("{http://www.w3.org/2005/Atom}updated") or "").strip()
            published_dt = _parse_date(updated)
            if cutoff and published_dt and published_dt < cutoff:
                continue
            for link_el in entry.findall("{http://www.w3.org/2005/Atom}link"):
                rel = link_el.attrib.get("rel", "")
                href = link_el.attrib.get("href", "")
                if rel == "alternate" and href:
                    link = href
                    break
                if not link and href:
                    link = href
            if title:
                items.append({"title": title, "link": link, "published": updated})
            if len(items) >= limit:
                break
    else:
        # RSS 2.0
        for item in root.findall("./channel/item"):
            title = (item.findtext("title") or "").replace("\n", " ").strip()
            link = (item.findtext("link") or "").replace("\n", " ").strip()
            pub = (item.findtext("pubDate") or "").strip()
            published_dt = _parse_date(pub)
            if cutoff and published_dt and published_dt < cutoff:
                continue
            if title:
                items.append({"title": title, "link": link, "published": pub})
            if len(items) >= limit:
                break
    return items


def main():
    if len(sys.argv) < 2:
        print("[]")
        return 0
    path = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    max_age_hours = None
    if len(sys.argv) > 3:
        try:
            max_age_hours = int(sys.argv[3])
        except Exception:
            max_age_hours = None
    items = parse(path, limit=limit, max_age_hours=max_age_hours)
    print(json.dumps({"items": items, "fetched_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
