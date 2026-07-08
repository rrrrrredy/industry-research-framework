#!/usr/bin/env python3
"""Build a small sanitized evaluation set from local AI knowledge repositories."""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SELECTED_TITLES = [
    "AI Agent研究报告",
    "近期 AI Agent 趋势",
    "从 R1 到 Sonnet 3.7，Reasoning Model 首轮竞赛中有哪些关键信号？",
    "主流AI视频生成产品报告",
    "AI视频生成市场概况",
    "大模型降价潮分析",
    "AI行业月度观察202602",
    "AI行业月度观察202512",
    "大模型行业近期市场信息：腾讯、阿里、字节及DeepSeek",
    "字节AI全景解析",
    "腾讯AI全景解析",
    "OpenAI近期信息报告-2024年初",
]


CASE_TEMPLATES = [
    {
        "case_id": "ai_agent_market_landscape_zh",
        "title": "AI Agent 市场格局行业报告",
        "task_type": "industry_report",
        "language": "zh",
        "source_titles": [
            "AI Agent研究报告",
            "近期 AI Agent 趋势",
            "AI行业月度观察202602",
            "AI行业月度观察202512",
        ],
        "prompt": (
            "面向战略读者，写一份 AI Agent 市场格局报告。需要覆盖平台型玩家、"
            "工作流产品、协议与生态、商业化路径、采用阻力、失败模式和反证。"
        ),
        "target_reader": "strategy and product leaders",
        "expected_depth": "standard report, 3000-5000 Chinese characters for eval runs",
        "min_final_nonspace_chars": 2400,
        "thin_final_nonspace_chars": 1200,
        "must_cover_entities": ["AI Agent", "OpenAI", "Anthropic", "DeepSeek", "MCP", "多模态"],
        "required_sections": ["核心判断", "范围与证据", "竞争格局", "采用阻力", "反证与不确定性"],
    },
    {
        "case_id": "reasoning_model_competition_zh",
        "title": "Reasoning Model 竞争技术路线研究",
        "task_type": "technical_route_research",
        "language": "zh",
        "source_titles": [
            "从 R1 到 Sonnet 3.7，Reasoning Model 首轮竞赛中有哪些关键信号？",
            "AI行业月度观察202602",
            "OpenAI近期信息报告-2024年初",
        ],
        "prompt": (
            "研究 reasoning model 从 DeepSeek R1 到 Claude Sonnet 风格混合推理的竞争。"
            "解释技术路径、产品后果、对 coding agent 的影响和仍不确定的问题。"
        ),
        "target_reader": "technical strategy readers",
        "expected_depth": "deep memo, 2500-4500 Chinese characters for eval runs",
        "min_final_nonspace_chars": 2000,
        "thin_final_nonspace_chars": 1000,
        "must_cover_entities": ["Reasoning Model", "DeepSeek", "Claude", "OpenAI", "AI编程", "强化学习"],
        "required_sections": ["核心判断", "技术路径", "产品后果", "竞争变量", "不确定性"],
    },
    {
        "case_id": "ai_video_generation_investment_memo_zh",
        "title": "AI 视频生成市场投资 Memo",
        "task_type": "investment_memo",
        "language": "zh",
        "source_titles": [
            "主流AI视频生成产品报告",
            "AI视频生成市场概况",
            "字节AI全景解析",
            "AI行业月度观察202512",
        ],
        "prompt": (
            "写一份 AI 视频生成市场投资 memo。重点分析品类时机、关键公司、"
            "技术壁垒、价格压力、GTM、采用风险和反证。"
        ),
        "target_reader": "investors",
        "expected_depth": "investment memo, 2500-4500 Chinese characters for eval runs",
        "min_final_nonspace_chars": 2000,
        "thin_final_nonspace_chars": 1000,
        "must_cover_entities": ["AI视频生成", "文生视频", "字节跳动", "多模态", "生成式AI"],
        "required_sections": ["投资判断", "市场结构", "技术壁垒", "商业化", "风险与反证"],
    },
    {
        "case_id": "model_price_war_competitive_analysis_zh",
        "title": "大模型降价潮竞品分析",
        "task_type": "competitive_analysis",
        "language": "zh",
        "source_titles": [
            "大模型降价潮分析",
            "大模型行业近期市场信息：腾讯、阿里、字节及DeepSeek",
            "腾讯AI全景解析",
            "字节AI全景解析",
        ],
        "prompt": (
            "分析大模型降价潮对腾讯、阿里、字节、DeepSeek 等玩家的竞争影响。"
            "区分 API 定价、云计算绑定、模型能力、分发入口和利润压力。"
        ),
        "target_reader": "business and product strategy readers",
        "expected_depth": "competitive memo, 2500-4500 Chinese characters for eval runs",
        "min_final_nonspace_chars": 2000,
        "thin_final_nonspace_chars": 1000,
        "must_cover_entities": ["大模型价格战", "API定价", "腾讯", "字节跳动", "DeepSeek", "云计算"],
        "required_sections": ["核心判断", "价格战机制", "玩家对比", "利润与分发", "反证"],
    },
    {
        "case_id": "monthly_observation_synthesis_zh",
        "title": "AI 行业月度观察综合",
        "task_type": "monthly_observation",
        "language": "zh",
        "source_titles": [
            "AI行业月度观察202602",
            "AI行业月度观察202512",
            "近期 AI Agent 趋势",
            "大模型行业近期市场信息：腾讯、阿里、字节及DeepSeek",
        ],
        "prompt": (
            "为管理层写一份 AI 行业月度观察。综合模型发布、Agent 基础设施、"
            "产品竞争、开源动态、中美差异和下一步影响。"
        ),
        "target_reader": "executive readers",
        "expected_depth": "monthly observation, 2500-4500 Chinese characters for eval runs",
        "min_final_nonspace_chars": 2000,
        "thin_final_nonspace_chars": 1000,
        "must_cover_entities": ["AI行业趋势", "AI Agent", "大语言模型", "中美AI竞争", "开源模型"],
        "required_sections": ["本月主线", "关键变化", "中美差异", "影响判断", "下月观察点"],
    },
]


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            f.write("\n")


def sanitize_text(value: Any, source_ids: set[str]) -> Any:
    if isinstance(value, list):
        return [sanitize_text(item, source_ids) for item in value]
    if isinstance(value, dict):
        return {key: sanitize_text(item, source_ids) for key, item in value.items()}
    if not isinstance(value, str):
        return value

    text = value
    text = re.sub(r"https?://[^\s)\]]*/[A-Za-z0-9_-]+/\d{6,}[^\s)\]]*", "[internal_url_redacted]", text)
    text = re.sub(r"https?://[^\s)\]]*(?:internal|private|corp|intranet)[^\s)\]]*", "[internal_url_redacted]", text, flags=re.IGNORECASE)
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[email_redacted]", text)
    text = re.sub(r"\b1[3-9]\d{9}\b", "[phone_redacted]", text)
    text = re.sub(r"\b[A-Za-z][A-Za-z0-9_-]*\s+AI\s+知识库\b", "private AI knowledge base", text)
    text = re.sub(r"\b[A-Za-z][A-Za-z0-9_-]*\s+API\b", "internal knowledge API", text)
    for source_id in sorted(source_ids, key=len, reverse=True):
        text = text.replace(source_id, "[redacted_id]")
    return text


def load_category_by_id(knowledge_graph_dir: Path | None) -> dict[str, str]:
    if not knowledge_graph_dir:
        return {}
    docs_path = knowledge_graph_dir / "data" / "docs.json"
    if not docs_path.exists():
        return {}
    docs = read_json(docs_path)
    if not isinstance(docs, list):
        return {}
    return {str(doc.get("id")): str(doc.get("type") or "unknown") for doc in docs}


def build_sources(aiknowledge_cli_dir: Path, knowledge_graph_dir: Path | None) -> tuple[list[dict[str, Any]], dict[str, str]]:
    kb_path = aiknowledge_cli_dir / "data" / "knowledge_base_public.json"
    docs = read_json(kb_path)
    if not isinstance(docs, list):
        raise ValueError(f"Expected a list in {kb_path}")

    category_by_id = load_category_by_id(knowledge_graph_dir)
    by_title = {doc.get("title"): doc for doc in docs}
    source_ids = {str(doc.get("id")) for doc in docs if doc.get("id")}

    rows: list[dict[str, Any]] = []
    title_to_source_id: dict[str, str] = {}
    for idx, title in enumerate(SELECTED_TITLES, start=1):
        doc = by_title.get(title)
        if not doc:
            raise ValueError(f"Missing selected source title: {title}")

        source_id = f"S{idx:03d}"
        original_id = str(doc.get("id", ""))
        relations = doc.get("relations") or []
        if isinstance(relations, list):
            relations = relations[:25]

        row = {
            "source_id": source_id,
            "title": sanitize_text(doc.get("title", ""), source_ids),
            "source_type": category_by_id.get(original_id, "sanitized_research_note"),
            "date": sanitize_text(doc.get("date", ""), source_ids),
            "summary": sanitize_text(doc.get("summary", ""), source_ids),
            "key_points": sanitize_text(doc.get("key_points", []), source_ids),
            "entities": sanitize_text((doc.get("entities") or [])[:20], source_ids),
            "relations": sanitize_text(relations, source_ids),
            "limitations": (
                "Sanitized evaluation source. Internal URLs and original document IDs were removed. "
                "Treat as a source pack for testing research workflow, not as a public factual authority."
            ),
        }
        rows.append(row)
        title_to_source_id[title] = source_id

    return rows, title_to_source_id


def build_cases(title_to_source_id: dict[str, str]) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for template in CASE_TEMPLATES:
        source_ids = [title_to_source_id[title] for title in template["source_titles"]]
        case = dict(template)
        case.pop("source_titles")
        case["source_pack"] = "ai_knowledge_sanitized"
        case["source_ids"] = source_ids
        case["artifact_requirements"] = [
            "state/task_spec.md",
            "state/progress.json",
            "data/source_registry.csv",
            "data/claims_registry.csv",
            "logs/review.jsonl",
            "final.md",
        ]
        case["quality_focus"] = [
            "brief_gate",
            "state_recovery",
            "claim_discipline",
            "counter_evidence",
            "depth_budget",
            "reader_cleanup",
        ]
        case["banned_process_phrases"] = [
            "用户提供的资料",
            "材料显示",
            "该来源补充",
            "this source supplements",
            "the user provided",
            "the material shows",
            "section passed audit",
        ]
        cases.append(case)
    return cases


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aiknowledge-cli", default=os.environ.get("AIKNOWLEDGE_CLI_DIR"))
    parser.add_argument("--knowledge-graph", default=os.environ.get("AI_KNOWLEDGE_GRAPH_DIR"))
    parser.add_argument("--out", default="evals")
    args = parser.parse_args()

    if not args.aiknowledge_cli:
        parser.error("--aiknowledge-cli or AIKNOWLEDGE_CLI_DIR is required")

    aiknowledge_cli_dir = Path(args.aiknowledge_cli).resolve()
    knowledge_graph_dir = Path(args.knowledge_graph).resolve() if args.knowledge_graph else None
    out_dir = Path(args.out).resolve()

    sources, title_to_source_id = build_sources(aiknowledge_cli_dir, knowledge_graph_dir)
    cases = build_cases(title_to_source_id)

    pack_dir = out_dir / "source_packs" / "ai_knowledge_sanitized"
    write_jsonl(pack_dir / "sources.jsonl", sources)
    write_json(
        pack_dir / "manifest.json",
        {
            "source_pack_id": "ai_knowledge_sanitized",
            "title": "Sanitized AI Knowledge Evaluation Source Pack",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_count": len(sources),
            "source_ids": [row["source_id"] for row in sources],
            "sanitization": [
                "Removed internal URLs.",
                "Removed original internal document IDs.",
                "Redacted emails and phone numbers.",
                "Replaced internal knowledge-system references with generic labels.",
            ],
            "limitations": [
                "This pack is for workflow evaluation.",
                "It is not a complete public benchmark.",
                "Keep private source packs out of public releases unless rights and sensitivity are cleared.",
            ],
        },
    )

    case_dir = out_dir / "cases"
    for case in cases:
        write_json(case_dir / f"{case['case_id']}.json", case)

    write_json(
        out_dir / "source_packs" / "ai_knowledge_sanitized" / "coverage_hints.json",
        {
            "source_pack_id": "ai_knowledge_sanitized",
            "case_source_map": {case["case_id"]: case["source_ids"] for case in cases},
            "note": "Coverage hints are used by the offline runner and human reviewers; they are not gold answers.",
        },
    )

    print(f"Wrote {len(sources)} sanitized sources and {len(cases)} cases to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
