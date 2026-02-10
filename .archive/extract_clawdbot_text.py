#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Extract assistant text from clawdbot agent JSON output."""

import json
import sys


def extract_text(obj):
    # Common shapes
    if isinstance(obj, dict):
        for key in ("output", "message", "result", "content", "text", "response"):
            if key in obj:
                t = extract_text(obj[key])
                if t:
                    return t
        # messages list
        msgs = obj.get("messages") if isinstance(obj.get("messages"), list) else None
        if msgs:
            for m in msgs[::-1]:
                t = extract_text(m)
                if t:
                    return t
        # content list
        content = obj.get("content") if isinstance(obj.get("content"), list) else None
        if content:
            for c in content:
                t = extract_text(c)
                if t:
                    return t
        # assistant field
        if obj.get("role") == "assistant":
            return obj.get("text") or obj.get("content") or ""
    elif isinstance(obj, list):
        for it in obj[::-1]:
            t = extract_text(it)
            if t:
                return t
    elif isinstance(obj, str):
        return obj
    return ""


def main():
    data = json.load(sys.stdin)
    text = extract_text(data)
    if not text:
        sys.exit(1)
    sys.stdout.write(text.strip() + "\n")


if __name__ == "__main__":
    main()
