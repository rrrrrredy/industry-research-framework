#!/usr/bin/env python3
"""Deterministic synthetic adapter used only to test pilot plumbing."""

from __future__ import annotations

import hashlib
import json
import sys


def main() -> int:
    request = json.load(sys.stdin)
    task = request["model_input"]["task"]
    digest = hashlib.sha256(
        json.dumps(
            request["model_input"],
            ensure_ascii=False,
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()[:12]
    response = {
        "interface_version": "pilot-adapter-v1",
        "status": "completed",
        "final_text": (
            f"# {task['title']}\n\n"
            "Synthetic plumbing output. It is not research evidence and must not "
            f"be used as a pilot result. Request digest: {digest}."
        ),
        "metadata": {
            "provider": "synthetic",
            "request_id": f"synthetic-{request['run_id']}",
            "actual_model": "synthetic-fake-adapter-v1",
            "system_fingerprint": "synthetic",
            "seed_supported": False,
            "isolation_attestation": True,
            "synthetic": True,
            "adapter_version": "fake-adapter-v1",
            "actual_sampling": {
                key: value
                for key, value in request["model"].items()
                if key not in {"snapshot", "snapshot_kind"}
            },
            "usage": {
                "input_tokens": 0,
                "output_tokens": 0
            },
            "stop_reason": "synthetic_complete",
            "tool_transcript": []
        },
        "artifacts": {},
        "provider_request": {
            "synthetic": True,
            "request_digest": digest
        },
        "provider_response": {
            "synthetic": True,
            "response_digest": digest
        }
    }
    json.dump(response, sys.stdout, ensure_ascii=False, sort_keys=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
