#!/usr/bin/env python3
"""Refresh the Field Notes block in README.md from the mdm.tools RSS feed.

Standard library only, so the workflow needs no dependency install and no
third-party action with write access to this repository.
"""

from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

FEED_URL = "https://mdm.tools/blog/feed.xml"
README = Path(__file__).resolve().parent.parent / "README.md"
START = "<!-- FIELD-NOTES:START -->"
END = "<!-- FIELD-NOTES:END -->"
MAX_POSTS = 5
MAX_SUMMARY = 200
TIMEOUT = 30
MAX_BYTES = 5 * 1024 * 1024

# ElementTree never resolves external entities, but an inline DTD can still
# declare a nested entity bomb. Nothing legitimate in an RSS feed needs a
# doctype, so refusing one closes that off without a third-party parser.
DOCTYPE = re.compile(rb"<!DOCTYPE", re.IGNORECASE)


def fetch(url: str) -> bytes:
    request = urllib.request.Request(
        url, headers={"User-Agent": "r4828-profile-field-notes/1.0"}
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        body = response.read(MAX_BYTES + 1)
    if len(body) > MAX_BYTES:
        raise ValueError(f"feed exceeded {MAX_BYTES} bytes")
    if DOCTYPE.search(body):
        raise ValueError("feed declares a doctype; refusing to parse")
    return body


def published(item: ET.Element) -> datetime:
    raw = (item.findtext("pubDate") or "").strip()
    if not raw:
        return datetime.min.replace(tzinfo=timezone.utc)
    try:
        parsed = parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        return datetime.min.replace(tzinfo=timezone.utc)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def flatten(text: str | None) -> str:
    """Collapse a feed field to a single line of plain text."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def escape_markdown(text: str) -> str:
    return text.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")


def truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip(" ,.;:—-") + "…"


def render(items: list[ET.Element]) -> str:
    lines = []
    for item in items:
        title = escape_markdown(flatten(item.findtext("title")) or "Untitled")
        link = (item.findtext("link") or "").strip()
        summary = truncate(flatten(item.findtext("description")), MAX_SUMMARY)
        date = published(item).date().isoformat()

        heading = f"**[{title}](<{link}>)**" if link else f"**{title}**"
        lines.append(f"- {heading} · {date}  ")
        lines.append(f"  {summary}" if summary else "  ")
    return "\n".join(lines)


def main() -> int:
    try:
        raw = fetch(FEED_URL)
    except (urllib.error.URLError, OSError, ValueError) as error:
        print(f"error: could not fetch {FEED_URL}: {error}", file=sys.stderr)
        return 1

    try:
        channel = ET.fromstring(raw).find("channel")
    except ET.ParseError as error:
        print(f"error: could not parse feed: {error}", file=sys.stderr)
        return 1

    items: list[ET.Element] = []
    if channel is not None:
        items = sorted(channel.findall("item"), key=published, reverse=True)
    if not items:
        print("error: feed contained no items", file=sys.stderr)
        return 1

    block = render(items[:MAX_POSTS])
    original = README.read_text(encoding="utf-8")

    pattern = re.compile(
        re.escape(START) + r".*?" + re.escape(END), re.DOTALL
    )
    if not pattern.search(original):
        print(f"error: {README.name} is missing the {START} / {END} markers", file=sys.stderr)
        return 1

    updated = pattern.sub(f"{START}\n{block}\n{END}", original, count=1)
    if updated == original:
        print("Field Notes already current")
        return 0

    README.write_text(updated, encoding="utf-8")
    print(f"Field Notes updated with {min(len(items), MAX_POSTS)} posts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
