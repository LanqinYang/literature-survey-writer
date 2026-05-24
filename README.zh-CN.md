# Literature Survey Writer

[English](README.md) | [简体中文](README.zh-CN.md)

严肃综述论文工作流里，最容易缺掉的中间层。

这个 skill **不是**用来替代原本的 literature reviewer/search skill。关键词扩展、英文文献检索、Google Scholar / Semantic Scholar / OpenAlex / 出版商页面检索、去重、导出 BibTeX/RIS 这些事情，原始 literature reviewer skill 已经能做。

这个 skill 解决的是后半段真正麻烦的部分：

```text
关键词
  -> 原始 literature-reviewer skill 找候选论文
  -> Zotero MCP 导入和检查附件
  -> 筛选论文
  -> 筛选后的核心论文必须读
  -> 已读证据进入 evidence matrix
  -> 写作 skill 开始写稿
  -> Web GPT / ChatGPT Pro 反复审稿
  -> 确定目标期刊
  -> 按期刊要求修改
  -> reviewer mode 再攻击一遍
  -> 最终投稿 QA
```

一句话：它不是“帮你找 50 篇 paper”，而是防止“找完 50 篇 paper 以后开始乱写”。

## 为什么需要这个

很多 AI 文献综述流程第一步都还可以：

> 这是与你主题相关的 50 篇文献。

真正的问题在后面：

- 哪些文章应该进 Zotero？
- 哪些文章有全文？
- 哪些文章只是导入了，哪些是真的读过？
- 哪些 claim 有已读证据支撑？
- 什么时候 corpus 足够开始写？
- 怎么避免写成“一篇 paper 一段话”的堆砌？
- 怎么把 Web GPT / ChatGPT Pro 作为审稿人反复用，而不是一直手动复制粘贴？
- 定了期刊以后，怎么按期刊 guide 改，而不是泛泛地“润色一下”？
- 真投稿前，怎么先用 reviewer mode 把自己打一遍？

这个 skill 就是这条链路的 coordinator。

## 它在原始 literature reviewer skill 之上补什么

原始 literature reviewer skill 负责：

- 关键词扩展
- 英文优先检索
- 元数据抓取
- 去重
- 导出 Markdown / BibTeX / RIS

这个 skill 补上：

- Zotero MCP 导入与 fallback 记录
- RIS/BibTeX 手动导入 Zotero 的步骤
- Zotero 全文/附件获取与可读性检查
- 筛选矩阵
- 强制阅读 gate
- reading notes
- evidence matrix 和 claim audit
- 写作 skill 的 handoff
- Web GPT / ChatGPT Pro review packet
- 目标期刊要求记录
- reviewer mode
- 投稿前 QA

核心规则：

> Zotero import is not reading.

导入 Zotero 不等于读过。支撑中心论点的文章必须是 `full_text_read`。

## 安装

推荐直接在 Codex 里输入：

```text
帮我安装这个 skill: https://github.com/LanqinYang/literature-survey-writer
```

如果要手动安装：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/LanqinYang/literature-survey-writer.git "${CODEX_HOME:-$HOME/.codex}/skills/literature-survey-writer"
```

安装后重启 Codex。

示例用法：

```text
Use $literature-survey-writer with my existing literature-reviewer skill and Zotero MCP. Start from these keywords, import candidate papers to Zotero, screen them, force a reading queue, then prepare the writing handoff.
```

## 文件结构

```text
literature-survey-writer/
├── SKILL.md
├── agents/openai.yaml
├── scripts/
│   ├── build_external_review_packet.py
│   └── init_survey_loop.py
├── .gitignore
├── README.md
└── README.zh-CN.md
```

`SKILL.md` 是 agent 真正读取的工作流说明。README 只是给人看的入口。

## 初始化一个项目状态

```bash
python3 scripts/init_survey_loop.py --topic "your survey topic"
```

它会创建这些状态文件：

```text
keywords_and_queries.md
candidate_export_status.md
zotero_import_log.md
screening_matrix.csv
reading_queue.md
reading_notes.md
evidence_matrix.md
claim_audit.md
writing_handoff.md
web_gpt_review_log.md
journal_requirements.md
reviewer_mode_report.md
pre_submission_checklist.md
```

这些文件看起来很朴素，但作用很重要：让流程不能假装“已经读过”“已经检查过”“已经适配期刊”。

## RIS/BibTeX 怎么导入 Zotero

如果 Zotero MCP 可以写入，优先让 MCP 按 DOI/URL 导入，并记录在 `zotero_import_log.md`。

如果 MCP 不能写入，就走手动 fallback：

```text
Zotero -> File -> Import... -> A file -> 选择 references.ris 或 references.bib
```

导入后：

1. 把导入条目移动到项目 collection。
2. 用 DOI / 标题查重。
3. 给导入条目打上 `candidate` 等 workflow tag。
4. 在 `zotero_import_log.md` 里记录导入文件、时间、数量和问题。

Zotero 也支持 `File -> Import from Clipboard` 导入剪贴板里的 RIS/BibTeX，但这个更适合小批量。

## 怎么在 Zotero 获取原文

流程不是“导入完就读”，而是先检查全文状态：

1. 看 Zotero 条目下面有没有 PDF attachment。
2. 如果有 PDF，用 Zotero MCP 读取全文；读不到就记录原因。
3. 如果只有 metadata，尝试 Zotero 的可用 PDF / full-text 获取功能，或从 DOI、出版商页面、arXiv、机构仓储、作者主页等合法来源获取。
4. 找到 PDF 后，挂到正确的 Zotero parent item 下面。
5. 找不到全文的，不要假装读过。标记为 `cannot_read`、`abstract_gap_check`、`parked`，或者请求用户手动帮忙。

全文状态要记录清楚，例如：

```text
zotero_pdf_readable
zotero_metadata_only
external_fulltext_available
abstract_only
needs_pdf_attachment
unavailable
duplicate_or_version
```

## 必须读完再写

筛选后进入核心证据的文章，要进入 `reading_queue.md`。

每篇核心文章至少记录：

```text
citation
Zotero key / DOI / URL
read status
evidence type
main contribution
method/system
limitations
claim(s) it can support
planned manuscript section
```

允许的阅读状态：

```text
unread
skimmed
full_text_read
cannot_read
parked
```

规则：

- `include_core` 的文章必须读。
- 重要 `include_supporting` 尽量读；不读就降级它的作用。
- 只有 `full_text_read` 可以支撑中心论点。
- `skimmed` 最多用于背景。
- metadata-only / abstract-only 只能用于 gap checking。
- agent 不能在没有 reading note 的情况下说“已经读完”。

## Web GPT / ChatGPT Pro 反复 review

脚本可以生成本地 review packet：

```bash
python3 scripts/build_external_review_packet.py \
  --draft path/to/current_draft.md \
  --out path/to/external_review_packet.md \
  --target-journal "Target Journal Name" \
  --notes path/to/evidence_matrix.md path/to/claim_audit.md
```

这个脚本**不会上传任何东西**。

如果要让 agent 把 packet 粘贴到 Web GPT / ChatGPT Pro，必须先说明要上传什么，并得到明确同意。

Web GPT 返回 critique 和 revision prompt 后，记录在 `web_gpt_review_log.md`，再转成可执行修改任务。

## 定刊和 reviewer mode

稿件稳定后：

1. 确认目标期刊。
2. 记录期刊 guide：范围、文章类型、页数/字数、引用格式、图表、声明、AI disclosure、data availability 等。
3. 按期刊要求修改。
4. 进入 reviewer mode。
5. 从审稿人角度检查：缺文献、novelty 弱、claim 过强、方法不透明、图表无用、引用不闭合、期刊不匹配。
6. 再改一轮。
7. 最后做投稿 QA。

这一步的目标不是“写得更漂亮”，而是让文章更像能投出去的稿件。

## 隐私

不要把这些东西提交到公开仓库：

- 未发表稿件
- PDF / DOCX
- 活项目的 Zotero 导出
- review packet
- 作者信息
- 审稿意见
- 投稿表单

`.gitignore` 故意写得保守。

## License

目前还没加 license。真正开放复用前建议补一个。
