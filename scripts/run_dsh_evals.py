#!/usr/bin/env python3
"""Run DeepSeek Harness integration smoke tests and live framework evals."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from run_evals import create_skeletons, evaluate_case, load_cases, load_sources


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "industry-research-framework"
DEFAULT_CASE_ID = "source_instruction_boundary_zh"
DEFAULT_DSH_PACKAGE = "@deepseek-ai/dsh@0.1.2-rc.1"
SMOKE_MARKER = "DSH_SKILL_SMOKE_OK"
SKILL_BODY_MARKERS = (
    "<skill_content name=",
    "Base directory for this skill:",
    "# Industry Research Framework",
    "references/research-workflow.md",
)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def parse_command_json(raw: str | None, package: str) -> list[str]:
    raw = raw or os.environ.get("DSH_EVAL_COMMAND_JSON")
    if raw:
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid DSH command JSON: {exc}") from exc
        if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
            raise ValueError("DSH command JSON must be a non-empty JSON array of non-empty strings.")
        return value

    dsh = shutil.which("dsh")
    if dsh:
        return [dsh]
    npx = shutil.which("npx")
    if npx:
        return [npx, "--yes", package]
    raise FileNotFoundError(
        "No dsh or npx executable was found. Install DeepSeek Harness or pass "
        "--dsh-command-json / DSH_EVAL_COMMAND_JSON."
    )


def new_output_dir(mode: str, requested: str | None) -> Path:
    if requested:
        output_dir = Path(requested).resolve()
        if output_dir.exists() and any(output_dir.iterdir()):
            raise FileExistsError(f"Output directory is not empty: {output_dir}")
    else:
        output_dir = REPO_ROOT / "evals" / "runs" / "dsh" / f"{mode}-{utc_stamp()}-{os.getpid()}"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def stage_skill(workspace: Path) -> Path:
    # DSH resolves project Skills from the nearest ancestor containing .git.
    # Eval workspaces live inside this repository, so give each one its own
    # project boundary instead of letting discovery jump to the outer repo.
    project_marker = workspace / ".git"
    if not project_marker.exists():
        project_marker.mkdir()
    destination = workspace / ".dsh" / "skills" / SKILL_NAME
    destination.mkdir(parents=True, exist_ok=False)
    shutil.copy2(REPO_ROOT / "SKILL.md", destination / "SKILL.md")
    shutil.copytree(REPO_ROOT / "references", destination / "references")
    scripts_dir = destination / "scripts"
    scripts_dir.mkdir()
    shutil.copy2(REPO_ROOT / "scripts" / "check_delivery.py", scripts_dir / "check_delivery.py")
    return destination


def read_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"Missing YAML frontmatter in {path}")
    result: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            break
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def select_case(case_id: str) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    cases = load_cases(REPO_ROOT / "evals" / "cases")
    matches = [case for case in cases if case["case_id"] == case_id]
    if not matches:
        known = ", ".join(case["case_id"] for case in cases)
        raise ValueError(f"Unknown case {case_id!r}. Known cases: {known}")
    return matches[0], load_sources(REPO_ROOT / "evals")


def stage_case_inputs(workspace: Path, case: dict[str, Any]) -> None:
    source_pack = str(case.get("source_pack", "ai_knowledge_sanitized"))
    source = REPO_ROOT / "evals" / "source_packs" / source_pack
    destination = workspace / "evals" / "source_packs" / source_pack
    if not source.is_dir():
        raise FileNotFoundError(f"Source pack not found: {source}")
    shutil.copytree(source, destination)

    conversation_pack = case.get("conversation_pack")
    if conversation_pack:
        conversation_source = REPO_ROOT / "evals" / "conversation_packs" / str(conversation_pack)
        conversation_destination = workspace / "evals" / "conversation_packs" / str(conversation_pack)
        if not conversation_source.is_dir():
            raise FileNotFoundError(f"Conversation pack not found: {conversation_source}")
        shutil.copytree(conversation_source, conversation_destination)


def validate_adapter(case_id: str) -> dict[str, Any]:
    frontmatter = read_frontmatter(REPO_ROOT / "SKILL.md")
    failures: list[str] = []
    if frontmatter.get("name") != SKILL_NAME:
        failures.append(f"frontmatter name must be {SKILL_NAME!r}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", frontmatter.get("name", "")):
        failures.append("frontmatter name is not DSH-compatible kebab-case")
    description = frontmatter.get("description", "")
    if not description:
        failures.append("frontmatter description is empty")
    if len(description) > 500:
        failures.append(f"frontmatter description has {len(description)} characters; DSH catalog default is 500")

    skill_text = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
    resource_paths = sorted(set(re.findall(r"`((?:references|scripts)/[^`\s]+)`", skill_text)))
    missing_resources = [relative for relative in resource_paths if not (REPO_ROOT / relative).is_file()]
    if missing_resources:
        failures.append("missing referenced resources: " + ", ".join(missing_resources))

    case, sources_by_id = select_case(case_id)
    with tempfile.TemporaryDirectory(prefix="irf-dsh-adapter-") as temp_dir:
        temp_root = Path(temp_dir)
        create_skeletons([case], temp_root, sources_by_id, REPO_ROOT / "evals")
        workspace = temp_root / case_id
        staged_skill = stage_skill(workspace)
        stage_case_inputs(workspace, case)
        expected_paths = [
            staged_skill / "SKILL.md",
            staged_skill / "references" / "research-workflow.md",
            staged_skill / "scripts" / "check_delivery.py",
            workspace / "prompt.md",
            workspace / "evals" / "source_packs" / str(case["source_pack"]) / "sources.jsonl",
        ]
        missing_staged = [str(path.relative_to(workspace)) for path in expected_paths if not path.is_file()]
        if missing_staged:
            failures.append("staged DSH workspace is incomplete: " + ", ".join(missing_staged))
        if not (workspace / ".git").exists():
            failures.append("staged DSH workspace has no local .git project boundary")

    return {
        "status": "pass" if not failures else "fail",
        "skill": SKILL_NAME,
        "descriptionCharacters": len(description),
        "referencedResources": resource_paths,
        "case": case_id,
        "failures": failures,
    }


class SmokeState:
    """Thread-safe, content-minimizing observations from the mock endpoint."""

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.request_count = 0
        self.skill_call_sent = False
        self.skill_tool_advertised = False
        self.catalog_entry_observed = False
        self.skill_result_observed = False
        self.marker_hits = {marker: False for marker in SKILL_BODY_MARKERS}
        self.request_summaries: list[dict[str, Any]] = []

    def observe(self, payload: dict[str, Any], names: list[str]) -> tuple[bool, bool]:
        messages = payload.get("messages")
        if not isinstance(messages, list):
            messages = []
        serialized = json.dumps(messages, ensure_ascii=False)
        roles = [str(message.get("role", "")) for message in messages if isinstance(message, dict)]
        marker_hits = {marker: marker in serialized for marker in SKILL_BODY_MARKERS}
        catalog_entry = "<available_skills>" in serialized and f"`{SKILL_NAME}`" in serialized
        tool_result = all(marker_hits.values())

        with self.lock:
            self.request_count += 1
            self.skill_tool_advertised = self.skill_tool_advertised or "skill" in names
            self.catalog_entry_observed = self.catalog_entry_observed or catalog_entry
            self.skill_result_observed = self.skill_result_observed or tool_result
            for marker, hit in marker_hits.items():
                self.marker_hits[marker] = self.marker_hits[marker] or hit
            should_call_skill = "skill" in names and not self.skill_call_sent and not tool_result
            if should_call_skill:
                self.skill_call_sent = True
            self.request_summaries.append(
                {
                    "request": self.request_count,
                    "messageCount": len(messages),
                    "roles": roles,
                    "toolNames": names,
                    "catalogEntry": catalog_entry,
                    "skillBodyMarkers": marker_hits,
                }
            )
        return should_call_skill, tool_result

    def snapshot(self) -> dict[str, Any]:
        with self.lock:
            return {
                "requestCount": self.request_count,
                "skillToolAdvertised": self.skill_tool_advertised,
                "catalogEntryObserved": self.catalog_entry_observed,
                "skillCallSent": self.skill_call_sent,
                "skillResultObserved": self.skill_result_observed,
                "skillBodyMarkers": dict(self.marker_hits),
                "requests": list(self.request_summaries),
            }


def tool_names(payload: dict[str, Any]) -> list[str]:
    names: list[str] = []
    tools = payload.get("tools")
    if not isinstance(tools, list):
        return names
    for tool in tools:
        if not isinstance(tool, dict):
            continue
        function = tool.get("function")
        name = function.get("name") if isinstance(function, dict) else tool.get("name")
        if isinstance(name, str) and name:
            names.append(name)
    return names


def sse_chunk(
    *,
    delta: dict[str, Any],
    finish_reason: str | None = None,
    model: str = "deepseek-v4-flash",
) -> bytes:
    payload = {
        "id": "chatcmpl-irf-dsh-smoke",
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "delta": delta,
                "finish_reason": finish_reason,
            }
        ],
    }
    if finish_reason is not None:
        payload["usage"] = {
            "prompt_tokens": 1,
            "completion_tokens": 1,
            "total_tokens": 2,
            "prompt_cache_hit_tokens": 0,
            "prompt_cache_miss_tokens": 1,
        }
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n".encode("utf-8")


def make_smoke_handler(state: SmokeState) -> type[BaseHTTPRequestHandler]:
    class SmokeHandler(BaseHTTPRequestHandler):
        server_version = "IRFDSHSmoke/1.0"

        def log_message(self, format: str, *args: Any) -> None:
            return

        def send_json(self, status: int, payload: dict[str, Any]) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            if self.path.rstrip("/").endswith("/models"):
                self.send_json(
                    200,
                    {
                        "object": "list",
                        "data": [{"id": "deepseek-v4-flash", "object": "model"}],
                    },
                )
                return
            self.send_json(404, {"error": {"message": "not found"}})

        def do_POST(self) -> None:
            try:
                content_length = int(self.headers.get("Content-Length", "0"))
                raw = self.rfile.read(content_length)
                payload = json.loads(raw.decode("utf-8"))
            except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
                self.send_json(400, {"error": {"message": f"invalid JSON: {exc}"}})
                return

            if not isinstance(payload, dict):
                self.send_json(400, {"error": {"message": "request must be an object"}})
                return

            names = tool_names(payload)
            should_call_skill, skill_result = state.observe(payload, names)
            if should_call_skill:
                chunks = [
                    sse_chunk(delta={"role": "assistant", "reasoning_content": ""}),
                    sse_chunk(
                        delta={
                            "tool_calls": [
                                {
                                    "index": 0,
                                    "id": "call_irf_skill_smoke",
                                    "type": "function",
                                    "function": {
                                        "name": "skill",
                                        "arguments": json.dumps({"name": SKILL_NAME}),
                                    },
                                }
                            ]
                        }
                    ),
                    sse_chunk(delta={}, finish_reason="tool_calls"),
                ]
            else:
                content = SMOKE_MARKER if skill_result else "DSH_SKILL_SMOKE_FAIL"
                chunks = [
                    sse_chunk(delta={"role": "assistant", "reasoning_content": ""}),
                    sse_chunk(delta={"content": content}),
                    sse_chunk(delta={}, finish_reason="stop"),
                ]

            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "close")
            self.end_headers()
            for chunk in chunks:
                self.wfile.write(chunk)
                self.wfile.flush()
            self.wfile.write(b"data: [DONE]\n\n")
            self.wfile.flush()

    return SmokeHandler


def start_smoke_server(state: SmokeState) -> tuple[ThreadingHTTPServer, threading.Thread, str]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_smoke_handler(state))
    thread = threading.Thread(target=server.serve_forever, name="irf-dsh-smoke", daemon=True)
    thread.start()
    host, port = server.server_address
    return server, thread, f"http://{host}:{port}"


def scrub_smoke_environment(dsh_home: Path, base_url: str) -> dict[str, str]:
    env = os.environ.copy()
    secret_suffixes = ("_API_KEY", "_ACCESS_TOKEN", "_AUTH_TOKEN")
    for name in list(env):
        if name.upper().endswith(secret_suffixes):
            env.pop(name, None)
    env.update(
        {
            "DSH_HOME": str(dsh_home),
            "DSH_MODEL": "deepseek-v4-flash",
            "DEEPSEEK_API_KEY": "dsh-smoke-local-placeholder",
            "DEEPSEEK_BASE_URL": base_url,
            "NO_COLOR": "1",
            "FORCE_COLOR": "0",
        }
    )
    return env


def run_process(
    command: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    timeout: int,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def command_version(command: list[str], env: dict[str, str], timeout: int) -> dict[str, Any]:
    result = run_process(command + ["--version"], cwd=REPO_ROOT, env=env, timeout=timeout)
    return {
        "exitCode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def run_smoke(args: argparse.Namespace) -> int:
    adapter = validate_adapter(args.case)
    command = parse_command_json(args.dsh_command_json, args.package)
    output_dir = new_output_dir("smoke", args.output_dir)
    workspace = output_dir / "workspace"
    workspace.mkdir()
    staged_skill = stage_skill(workspace)

    state = SmokeState()
    server, server_thread, base_url = start_smoke_server(state)
    env = scrub_smoke_environment(output_dir / "dsh-home", base_url)
    runtime_error = ""
    result: subprocess.CompletedProcess[str] | None = None
    version: dict[str, Any] = {}
    prompt = (
        "Run the DSH native Skill integration smoke test. You must call the skill tool "
        f"with the exact name {SKILL_NAME}, inspect the loaded instructions, and then finish."
    )
    try:
        version = command_version(command, env, min(args.timeout, 90))
        result = run_process(
            command + ["--profile", "headless", prompt],
            cwd=workspace,
            env=env,
            timeout=args.timeout,
        )
    except subprocess.TimeoutExpired as exc:
        runtime_error = f"DSH timed out after {exc.timeout} seconds"
        stdout = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        result = subprocess.CompletedProcess(command, 124, stdout, stderr)
    finally:
        server.shutdown()
        server.server_close()
        server_thread.join(timeout=5)

    stdout = result.stdout if result is not None else ""
    stderr = result.stderr if result is not None else ""
    (output_dir / "dsh.stdout.txt").write_text(stdout, encoding="utf-8")
    (output_dir / "dsh.stderr.txt").write_text(stderr, encoding="utf-8")
    observations = state.snapshot()
    checks = {
        "adapterValidation": adapter["status"] == "pass",
        "versionCommand": version.get("exitCode") == 0,
        "headlessExitZero": result is not None and result.returncode == 0,
        "skillToolAdvertised": observations["skillToolAdvertised"],
        "catalogEntryObserved": observations["catalogEntryObserved"],
        "skillToolCalled": observations["skillCallSent"],
        "skillResultObserved": observations["skillResultObserved"],
        "allSkillBodyMarkersObserved": all(observations["skillBodyMarkers"].values()),
        "successMarkerInStdout": SMOKE_MARKER in stdout,
    }
    status = "pass" if all(checks.values()) and not runtime_error else "fail"
    report = {
        "mode": "smoke",
        "status": status,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "scope": (
            "Real DSH headless discovery and skill-tool invocation against a local scripted "
            "DeepSeek-compatible streaming endpoint; this is not a model-quality result."
        ),
        "workspace": str(workspace),
        "stagedSkill": str(staged_skill.relative_to(workspace)),
        "runtime": {
            "command": command,
            "profile": "headless",
            "version": version,
            "exitCode": result.returncode if result is not None else None,
            "error": runtime_error,
        },
        "checks": checks,
        "adapter": adapter,
        "observations": observations,
        "artifacts": {
            "stdout": "dsh.stdout.txt",
            "stderr": "dsh.stderr.txt",
        },
    }
    report_path = output_dir / "dsh-smoke.json"
    write_json(report_path, report)
    print(f"DSH smoke: {status}")
    print(f"Report: {report_path}")
    if status != "pass":
        failed = [name for name, passed in checks.items() if not passed]
        print("Failed checks: " + ", ".join(failed))
        if runtime_error:
            print(runtime_error)
    return 0 if status == "pass" else 1


def run_live(args: argparse.Namespace) -> int:
    adapter = validate_adapter(args.case)
    if adapter["status"] != "pass":
        raise ValueError("DSH adapter validation failed: " + "; ".join(adapter["failures"]))

    command = parse_command_json(args.dsh_command_json, args.package)
    output_dir = new_output_dir("live", args.output_dir)
    case, sources_by_id = select_case(args.case)
    create_skeletons([case], output_dir, sources_by_id, REPO_ROOT / "evals")
    workspace = output_dir / args.case
    staged_skill = stage_skill(workspace)
    stage_case_inputs(workspace, case)

    prompt = (
        f"First load the DSH Skill named {SKILL_NAME}. Then read prompt.md and complete the "
        "research task in this current workspace. Read only the staged source and conversation "
        "packs referenced by prompt.md. Create or update every required artifact at its exact "
        "relative path, including final.md. Follow the Skill's evidence, review, and completion "
        "rules. Do not merely describe what you would do."
    )
    env = os.environ.copy()
    env.update({"NO_COLOR": "1", "FORCE_COLOR": "0"})
    version = command_version(command, env, min(args.timeout, 90))
    started = time.monotonic()
    runtime_error = ""
    try:
        result = run_process(
            command + ["--profile", "headless", prompt],
            cwd=workspace,
            env=env,
            timeout=args.timeout,
        )
    except subprocess.TimeoutExpired as exc:
        runtime_error = f"DSH timed out after {exc.timeout} seconds"
        stdout = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        result = subprocess.CompletedProcess(command, 124, stdout, stderr)
    elapsed = round(time.monotonic() - started, 3)
    (output_dir / "dsh.stdout.txt").write_text(result.stdout, encoding="utf-8")
    (output_dir / "dsh.stderr.txt").write_text(result.stderr, encoding="utf-8")

    evaluation = evaluate_case(case, workspace, sources_by_id)
    if result.returncode != 0:
        status = "runtime_fail"
    else:
        status = evaluation["conformance_status"]
    report = {
        "mode": "live",
        "status": status,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "case": args.case,
        "workspace": str(workspace),
        "stagedSkill": str(staged_skill.relative_to(workspace)),
        "runtime": {
            "command": command,
            "profile": "headless",
            "version": version,
            "exitCode": result.returncode,
            "elapsedSeconds": elapsed,
            "error": runtime_error,
        },
        "evaluation": evaluation,
        "artifacts": {
            "stdout": "dsh.stdout.txt",
            "stderr": "dsh.stderr.txt",
            "final": f"{args.case}/final.md",
        },
    }
    report_path = output_dir / "dsh-live-eval.json"
    write_json(report_path, report)
    print(
        f"DSH live conformance: {status} "
        f"({evaluation['conformance_score']}/{evaluation['max_conformance_score']}); "
        "research quality not evaluated"
    )
    print(f"Report: {report_path}")
    if result.returncode != 0:
        print(runtime_error or "DSH exited non-zero; inspect dsh.stderr.txt.")
        return 1
    allowed = {"pass"}
    if args.allow_review:
        allowed.add("review")
    return 0 if evaluation["conformance_status"] in allowed else 1


def add_runtime_arguments(parser: argparse.ArgumentParser, *, default_timeout: int) -> None:
    parser.add_argument("--case", default=DEFAULT_CASE_ID, help="Eval case id to stage and validate.")
    parser.add_argument("--output-dir", help="Empty output directory; defaults under evals/runs/dsh/.")
    parser.add_argument("--timeout", type=int, default=default_timeout, help="DSH timeout in seconds.")
    parser.add_argument(
        "--dsh-command-json",
        help=(
            "JSON argv array for DSH, for example "
            "'[\"npx\",\"--yes\",\"@deepseek-ai/dsh@0.1.2-rc.1\"]'. "
            "DSH_EVAL_COMMAND_JSON is the environment alternative."
        ),
    )
    parser.add_argument(
        "--package",
        default=DEFAULT_DSH_PACKAGE,
        help="Pinned npm package used only when dsh is absent and npx is available.",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="mode", required=True)

    validate_parser = subparsers.add_parser(
        "validate",
        help="Offline validation of the DSH Skill layout and eval staging contract.",
    )
    validate_parser.add_argument("--case", default=DEFAULT_CASE_ID)

    smoke_parser = subparsers.add_parser(
        "smoke",
        help="Run real DSH headless discovery/invocation against a local scripted endpoint.",
    )
    add_runtime_arguments(smoke_parser, default_timeout=240)

    live_parser = subparsers.add_parser(
        "live",
        help="Run a configured model through DSH headless and score the produced artifacts.",
    )
    add_runtime_arguments(live_parser, default_timeout=1800)
    live_parser.add_argument(
        "--allow-review",
        action="store_true",
        help="Return success for the evaluator's review status as well as pass.",
    )

    args = parser.parse_args()
    try:
        if args.mode == "validate":
            result = validate_adapter(args.case)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result["status"] == "pass" else 1
        if args.mode == "smoke":
            return run_smoke(args)
        return run_live(args)
    except (FileNotFoundError, FileExistsError, ValueError) as exc:
        parser.exit(2, f"error: {exc}\n")
    except subprocess.TimeoutExpired as exc:
        parser.exit(2, f"error: DSH timed out after {exc.timeout} seconds\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
