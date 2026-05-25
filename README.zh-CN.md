# 文献综述 + Zotero MCP 联动工作流

[English](README.md) | [简体中文](README.zh-CN.md)

这个 fork 基于 [AI-Powered-Literature-Review-Skills](https://github.com/stephenlzc/AI-Powered-Literature-Review-Skills)。

原版已经做了很多事：关键词扩展、英文优先文献检索、浏览器访问数据库、去重、Markdown/BibTeX/RIS 导出、引用格式化、单篇分析、综述草稿和 review/final 阶段。

这个版本保留这些基础，但重点补我们真实写综述时后面更容易乱的部分：**Zotero MCP、全文阅读状态、证据到文章的控制链**。

流程大概是：

```text
关键词
  -> 文献检索和导出
  -> Zotero MCP 导入或 RIS/BibTeX fallback
  -> PDF / 全文状态检查
  -> 筛选和文献角色分层
  -> 强制阅读 gate
  -> evidence matrix 和 claim audit
  -> 基于已读证据写文章
  -> Web GPT / ChatGPT Pro review loop
  -> 按目标期刊修改
  -> reviewer mode 压力测试
  -> 最终投稿 QA
```

核心原则很简单：

> 找到文献不等于读过文献。  
> 导入 Zotero 不等于理解文献。  
> 文章里的中心论点应该能追溯到已读证据。

## 原版已经覆盖什么

原版已经覆盖前半段，而且做得不少：

- 从主题生成关键词和布尔检索式
- 英文优先学术数据库检索
- 可选中文/CNKI 流程
- 抓取标题、作者、年份、期刊、DOI、摘要等元数据
- 候选文献去重
- 导出 `references.md`、`references.bib`、`references.ris`
- 引用格式化
- 单篇文献分析
- 综述草稿、审查、润色

所以这些不应该算成这个 fork 自己的新功能。

## 这个 Fork 补什么

这个版本重点补的是文献列表之后的流程：

- Zotero MCP 直接导入，而不只是导出 Zotero 可导入文件。
- Zotero MCP 不能写入时，保留 RIS/BibTeX 手动导入 fallback。
- 检查 Zotero 里的 PDF / 全文附件。
- 明确记录 metadata-only、abstract-only、readable PDF、missing PDF、duplicate/version、parked 等状态。
- 写 evidence-heavy 正文前，必须过 reading gate。
- 用 `evidence_matrix.md` 和 `claim_audit.md` 接住已读证据。
- Web GPT / ChatGPT Pro review packet 循环。
- 定目标期刊、按 guide 修改、reviewer mode 和投稿 QA。

说白了，它是为了防止流程变成：

> 我们导入了一堆 Zotero 条目，所以我们已经完成文献综述了。

## 核心规则

> Zotero import is not reading.

导入 Zotero 不等于读过。中心论点应该来自 `full_text_read` 的文献，并且要有 reading notes 说明这篇文献到底支撑了什么。

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
Use $literature-survey-writer to start from these keywords, find papers, import them into Zotero with Zotero MCP, screen them, read the selected papers, and prepare the manuscript-writing handoff.
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

`SKILL.md` 是 agent 真正读取的工作流说明。README 是给人看的入口。

## 初始化项目状态

```bash
python3 scripts/init_survey_loop.py --topic "your survey topic"
```

它会创建这些文件：

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

这些文件用来记录：找到了什么、什么进了 Zotero、筛掉了什么、读了什么、哪些 claim 有证据、后面还缺什么。

## Zotero MCP 和 RIS/BibTeX

有 Zotero MCP 时，这个 skill 可以：

- 先查本地 Zotero，避免重复导入。
- 按 DOI 或 URL 添加条目。
- 检查 child items 和附件。
- 在有可读附件时读取全文。
- 给文献打 workflow tag。
- 查重。

如果 Zotero MCP 不能写入，走手动 RIS/BibTeX 导入：

```text
Zotero -> File -> Import... -> A file -> 选择 references.ris 或 references.bib
```

导入后：

1. 把条目移动到项目 collection。
2. 用 DOI / 标题查重。
3. 给导入条目打 `candidate` 等 tag。
4. 在 `zotero_import_log.md` 里记录导入文件、数量和问题。

Zotero 也可以用 `File -> Import from Clipboard` 从剪贴板导入 RIS/BibTeX，这适合小批量。

## 在 Zotero 获取全文

每篇导入的文章都要检查全文状态：

1. 看 Zotero item 下有没有 PDF attachment。
2. 有 PDF 时，尽量通过 Zotero MCP 读取。
3. 只有 metadata 时，尝试 Zotero 的 PDF/full-text 获取路径，或用 Zotero Connector 从出版商、DOI、arXiv 页面保存。
4. 如果在合法开放来源找到 PDF，把它挂到正确的 Zotero parent item 下，或标记为 externally readable。
5. 找不到全文时，明确标记，不要假装读过。

常用全文状态：

```text
zotero_pdf_readable
zotero_metadata_only
external_fulltext_available
abstract_only
needs_pdf_attachment
unavailable
duplicate_or_version
```

## 阅读 Gate

开始写 evidence-heavy 的正文前，筛选进入核心证据的文献必须读。

每篇核心文献至少记录：

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

- 所有 `include_core` 文献必须读。
- 重要 `include_supporting` 文献应该读；不读就降级它的作用。
- 只有 `full_text_read` 可以支撑中心论点。
- `skimmed` 最多用于背景。
- metadata-only / abstract-only 只能做 gap checking。
- 没有 reading notes，就不能说“都读完了”。

## Web GPT / ChatGPT Pro 审稿

脚本会生成本地 review packet：

```bash
python3 scripts/build_external_review_packet.py \
  --draft path/to/current_draft.md \
  --out path/to/external_review_packet.md \
  --target-journal "Target Journal Name" \
  --notes path/to/evidence_matrix.md path/to/claim_audit.md
```

这个脚本**不会上传任何东西**。

如果要让 agent 把 packet 粘贴到 Web GPT / ChatGPT Pro，必须先说明会分享什么，并得到明确同意。

## 定刊和 Reviewer Mode

稿件稳定后：

1. 确认目标期刊。
2. 记录期刊要求：范围、文章类型、字数/页数、引用格式、图表、声明、AI disclosure、data availability、所需文件。
3. 按期刊要求修改。
4. 运行 reviewer mode。
5. 再修改。
6. 最后做投稿 QA。

这一步的目标不是“写得更好看”，而是让稿件更像能投出去的文章。

## 隐私

不要把这些活项目文件提交到公开仓库：

- 未发表稿件
- PDF 或 DOCX
- 活项目 Zotero 导出
- external review packet
- 作者信息
- 审稿意见
- 投稿表单

`.gitignore` 故意写得保守。

## License

目前还没加 license。开放复用前建议补一个。
