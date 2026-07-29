#!/usr/bin/env python3
"""Check or refresh the copyable SKILL.md block in docs/framework.html."""

from __future__ import annotations

import argparse
import html
from pathlib import Path


START_MARKER = '<pre id="skilltext"><code>'
END_MARKER = "</code></pre>"


def normalize(text: str) -> str:
    """Ignore platform line endings and insignificant trailing blank lines."""

    return text.replace("\r\n", "\n").rstrip("\n") + "\n"


def split_embedded_block(page: str) -> tuple[str, str, str]:
    if page.count(START_MARKER) != 1:
        raise ValueError(f"expected exactly one {START_MARKER!r} marker")

    before, remainder = page.split(START_MARKER, 1)
    if remainder.count(END_MARKER) != 1:
        raise ValueError(f"expected exactly one {END_MARKER!r} marker after the start marker")

    embedded, after = remainder.split(END_MARKER, 1)
    return before, embedded, after


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="refresh the HTML block from SKILL.md")
    parser.add_argument("--skill", default="SKILL.md")
    parser.add_argument("--html", default="docs/framework.html")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    skill_path = (repo_root / args.skill).resolve()
    html_path = (repo_root / args.html).resolve()

    skill_text = skill_path.read_text(encoding="utf-8")
    page_text = html_path.read_text(encoding="utf-8")

    try:
        before, embedded_html, after = split_embedded_block(page_text)
    except ValueError as error:
        print(f"docs sync check failed: {error}")
        return 1

    embedded_text = html.unescape(embedded_html)
    if normalize(skill_text) == normalize(embedded_text):
        print("docs sync check passed: Full SKILL.md matches SKILL.md")
        return 0

    if not args.write:
        print("docs sync check failed: Full SKILL.md differs from SKILL.md")
        print("Run: python scripts/check_docs_sync.py --write")
        return 1

    rendered = html.escape(normalize(skill_text).rstrip("\n"), quote=False)
    updated_page = before + START_MARKER + rendered + "\n" + END_MARKER + after
    html_path.write_text(updated_page, encoding="utf-8")
    print(f"Updated {html_path.relative_to(repo_root)} from {skill_path.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
