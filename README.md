# Longform Industry Narrative Research

A Codex skill for producing source-backed, publishable longform industry narrative research.

This skill is designed for complex research-and-writing tasks where an agent must collect materials, structure evidence, analyze companies or actors, synthesize narrative mechanisms, and then rewrite the result into a clean author-facing article rather than a process report.

It was distilled from a long AI industry narrative research project covering company narratives, founder interviews, podcasts, official blogs, media translation, market reports, advertising, pricing, talent flow, and cross-market China-overseas narrative diffusion.

## What This Skill Helps With

Use this skill when you need to produce substantial industry analysis such as:

- company-by-company narrative studies
- AI or technology industry longform essays
- cross-market narrative analysis
- podcast and interview synthesis
- official blog and product narrative analysis
- media and capital-market narrative mapping
- counter-narrative and risk analysis
- final cleanup of a research draft into a publishable article

The central idea is simple:

> Keep the research backend rigorous, but keep the final article clean.

The skill separates two layers:

- **Backstage research system**: sources, claims, uncertainty, logs, checkpoints, audits, inaccessible materials.
- **Frontstage article**: thesis, argument, company analysis, narrative mechanisms, counter-narratives, conclusions, reader-facing references.

## Core Method

For each company, actor, or topic, the skill recommends a five-part analysis card:

1. **Narrative history**: how the external story changed over time.
2. **Current narrative position**: what default language, workflow, or market frame the actor tries to own.
3. **Construction and diffusion mechanism**: product, API, docs, keynote, blog, podcast, pricing, ads, community, capital reports.
4. **External behavior change**: how the narrative changes developers, markets, media, capital, practitioners, or society.
5. **Counter-narrative and boundary**: what could weaken, narrow, or invalidate the story.

The final article should not read like a source-processing log. It should read like an author's argument.

## Repository Structure

```text
longform-industry-narrative-research/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── research-workflow.md
    ├── writing-style.md
    ├── quality-gates.md
    └── postmortem-lessons.md
```

## Installation

Clone this repository into your Codex skills directory.

### macOS / Linux

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/rrrrrredy/longform-industry-narrative-research.git \
  ~/.codex/skills/longform-industry-narrative-research
```

### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills" | Out-Null
git clone https://github.com/rrrrrredy/longform-industry-narrative-research.git `
  "$env:USERPROFILE\.codex\skills\longform-industry-narrative-research"
```

Restart Codex or start a new Codex thread after installation so the skill can be discovered.

## Example Prompts

```text
Use $longform-industry-narrative-research to plan a longform essay on how AI coding companies are reshaping developer workflows.
```

```text
Use $longform-industry-narrative-research to turn these source notes into a publishable company-by-company industry narrative report.
```

```text
Use $longform-industry-narrative-research to review this draft and remove process language, source-log language, and assistant-first phrasing.
```

## Writing Principles

The skill pushes Codex to:

- decide the thesis before collecting more material
- process sources by analytical use, not just by summary
- draft complex reports section by section
- integrate podcasts and interviews as narrative translation mechanisms
- keep counter-narratives inside the analysis
- avoid visible source IDs in final body text
- remove phrases like "the user provided", "the material shows", and "supplementary evidence"
- build a reader-facing reference appendix instead of dumping the full source registry

## What This Is Not

This is not a citation manager, a scraping tool, or a generic report template.

It is a writing and research workflow skill for long, judgment-heavy industry analysis where both evidence discipline and final prose quality matter.

## Chinese Version / 中文说明

# 长篇产业叙事研究 Skill

这是一个用于 Codex 的研究写作 skill，适合处理资料量大、周期长、需要形成可发布文章的产业研究任务。

它的核心目标不是生成一份过程报告，而是帮助 Codex 完成：

- 资料收集
- 来源管理
- 公司逐个分析
- 播客和访谈处理
- 媒体与资本叙事拆解
- 反叙事分析
- 最终长文写作
- 终稿去过程化改写

一句话概括：

> 后台研究要严谨，前台文章要干净。

## 适用场景

这个 skill 适合用于：

- AI 公司外部叙事研究
- 科技公司成长史和叙事演化分析
- 中外产业叙事比较
- 播客、访谈、公众号和媒体材料综合分析
- 公司官网、官方 blog、技术报告和产品发布拆解
- 资本报告、市场报告和广告传播分析
- 长篇行业文章的结构化写作
- 把研究草稿改成可发布文章

## 核心方法

每家公司或研究对象都建议按五个部分处理：

1. **叙事成长史**：公司对外叙事如何随时间变化。
2. **当前叙事定位**：公司试图占据什么默认语言、入口、工作流或市场框架。
3. **叙事构建与扩散机制**：产品、API、文档、发布会、博客、播客、广告、定价、社区和资本报告。
4. **外部行为变化**：如何影响市场、开发者、媒体、资本、从业者和社会认知。
5. **反叙事和边界**：哪些因素可能削弱或限制这套叙事。

最终文章不应该像资料处理日志，而应该像作者自己的研究判断。

## 关键写作原则

使用这个 skill 时，Codex 会被引导去：

- 先确定文章主线，再继续搜集资料
- 把来源台账和正文写作分开
- 一家公司一家公司写，不一次性糊完整篇
- 把播客和访谈当成叙事转译机制，而不是简单摘要
- 把反叙事写进正文，而不是只写公司想让外界相信的故事
- 终稿中不显示 `[Sxxx]` 这类来源编号
- 删除“用户提供材料”“材料显示”“补充材料”“证据缺口”等过程语言
- 文末参考资料按读者可理解的类别整理，而不是直接贴完整审计台账

## 安装方式

### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills" | Out-Null
git clone https://github.com/rrrrrredy/longform-industry-narrative-research.git `
  "$env:USERPROFILE\.codex\skills\longform-industry-narrative-research"
```

### macOS / Linux

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/rrrrrredy/longform-industry-narrative-research.git \
  ~/.codex/skills/longform-industry-narrative-research
```

安装后重启 Codex，或开启一个新的 Codex 线程。

## 示例提示词

```text
Use $longform-industry-narrative-research to plan and write a longform Chinese article about AI company narrative competition.
```

```text
Use $longform-industry-narrative-research to turn these notes into a publishable industry narrative essay.
```

```text
Use $longform-industry-narrative-research to clean this draft and remove process-language, audit-language, and assistant-first phrasing.
```

## 设计理念

复杂产业研究不能只靠一次性生成。更可靠的方式是：

1. 先确定主线。
2. 再建立来源和判断台账。
3. 按公司或主题逐块处理。
4. 合稿时围绕主线重组。
5. 最后做一次专门的“去过程化改写”。

这个 skill 的重点，就是帮助 Codex 同时做到两件事：

- 后台证据可追溯；
- 前台文章可阅读、可发布。
