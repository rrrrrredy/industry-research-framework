#!/usr/bin/env python3
"""Read-only comparison of installed research payload with an explicit local Git commit."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def canonical_hash(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


def reference_payload(repository: Path, reference: str) -> tuple[str, dict[str, bytes]]:
    def git(*args: str) -> bytes:
        return subprocess.run(["git", *args], cwd=repository, capture_output=True, check=True).stdout

    commit = git("rev-parse", "--verify", "--end-of-options", reference + "^{commit}").decode().strip()
    paths = git("ls-tree", "-r", "--name-only", commit, "--", "SKILL.md", "references", "scripts/check_delivery.py").decode("utf-8").splitlines()
    paths = [path for path in paths if path.endswith((".md", ".py"))]
    if "SKILL.md" not in paths or "scripts/check_delivery.py" not in paths:
        raise ValueError("Reference lacks the expected research payload.")
    return commit, {path: git("show", f"{commit}:{path}") for path in paths}


def compare_payload(installed: Path, payload: dict[str, bytes]) -> dict:
    root = installed.resolve()
    files = []
    for relative, expected in payload.items():
        path = (root / relative).resolve()
        item = {"path": relative, "expected_sha256": canonical_hash(expected)}
        try:
            path.relative_to(root)
            actual = path.read_bytes()
        except (OSError, ValueError):
            item.update(status="missing_or_unreadable", actual_sha256=None)
        else:
            actual_hash = canonical_hash(actual)
            item.update(status="match" if actual_hash == item["expected_sha256"] else "modified", actual_sha256=actual_hash)
        files.append(item)
    return {
        "payload_matches": all(item["status"] == "match" for item in files),
        "scope": "SKILL.md, reference Markdown, and the standalone delivery checker only; other files and runtime loading are not verified",
        "files": files,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("installed", type=Path)
    parser.add_argument("--reference", required=True, help="Trusted tag or full commit already present in the local reference repository")
    parser.add_argument("--repository", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        commit, payload = reference_payload(args.repository.resolve(), args.reference)
        result = compare_payload(args.installed, payload)
    except (OSError, ValueError, subprocess.CalledProcessError):
        print("Unable to read the requested local reference. No fetch, install, or overwrite was attempted.")
        return 2
    result["reference_commit"] = commit
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Reference: {commit}")
        for item in result["files"]:
            print(f"{item['status']}: {item['path']}")
        print(result["scope"])
        print("MATCH: selected payload matches." if result["payload_matches"] else "DIFFERENT: inspect local changes before deciding whether to update.")
    return 0 if result["payload_matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
