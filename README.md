# Literature Survey Writer

[English](README.md) | [简体中文](README.zh-CN.md)

The missing middle of a serious survey-paper workflow.

This is **not** trying to replace a literature-search skill. A lot of that work is already handled well by existing literature reviewer skills: take keywords, search Google Scholar / Semantic Scholar / OpenAlex / publisher sites, deduplicate, and export BibTeX/RIS.

This skill starts where that usually stops being enough.

```text
keywords
  -> baseline literature-reviewer skill finds candidate papers
  -> Zotero MCP imports and audits them
  -> selected papers are screened
  -> screened-in papers must be read
  -> read evidence becomes an evidence matrix
  -> writing skill drafts the manuscript
  -> Web GPT / ChatGPT Pro reviews it
  -> target journal is chosen
  -> paper is revised to that journal
  -> reviewer mode attacks the draft again
  -> final submission QA
```

That is the workflow this repo is for.

## Why This Exists

Most AI literature-review workflows are fine at the first step:

> "Here are 50 papers about your topic."

The real pain starts after that:

- Which papers actually belong in Zotero?
- Which ones have full text?
- Which ones have been read, not just imported?
- Which claims are supported by read evidence?
- When is the corpus enough to start writing?
- How do you stop the draft from becoming one paragraph per paper?
- How do you use Web GPT / ChatGPT Pro as a reviewer without manually copy-pasting forever?
- After choosing a journal, how do you modify the paper to that journal instead of generic academic taste?
- How do you run a reviewer-style attack before real reviewers do?

This skill is the coordinator for that loop.

## What It Adds On Top Of A Normal Literature Reviewer Skill

The baseline literature reviewer skill should handle:

- keyword expansion
- English-first scholarly search
- metadata capture
- deduplication
- BibTeX/RIS/Markdown exports

This skill adds:

- Zotero MCP import and fallback logging
- full-text availability audit
- screening decisions
- a mandatory reading gate
- evidence matrix and claim audit
- handoff to a manuscript-writing workflow
- local review-packet generation for Web GPT / ChatGPT Pro
- journal requirement tracking
- reviewer-mode critique
- pre-submission QA

The key rule is simple:

> Zotero import is not reading.

Central claims should come from papers marked as `full_text_read`.

## Install

Recommended: ask Codex to install it for you.

```text
帮我安装这个 skill: https://github.com/LanqinYang/literature-survey-writer
```

If you want to install manually, clone it into your Codex skills folder:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/LanqinYang/literature-survey-writer.git "${CODEX_HOME:-$HOME/.codex}/skills/literature-survey-writer"
```

Restart Codex after installation.

Example prompt:

```text
Use $literature-survey-writer with my existing literature-reviewer skill and Zotero MCP. Start from these keywords, import candidate papers to Zotero, screen them, force a reading queue, then prepare the writing handoff.
```

## Files

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

`SKILL.md` is the agent-facing workflow. This README is for humans deciding whether the skill fits their project.

## Session Scaffold

Create a production session:

```bash
python3 scripts/init_survey_loop.py --topic "your survey topic"
```

It creates files like:

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

These files are intentionally boring. Their job is to stop the workflow from lying to itself.

## Zotero MCP Role

Zotero MCP is used for:

- checking whether a candidate already exists
- importing DOI/URL records
- inspecting attachments
- reading full text when available
- separating metadata-only records from readable papers
- tagging workflow states

If MCP write mode is unavailable, the skill falls back to RIS/BibTeX imports and records that fallback in `zotero_import_log.md`.

Manual RIS/BibTeX import fallback:

```text
Zotero -> File -> Import... -> A file -> choose references.ris or references.bib
```

Then move imported items into the project collection, check duplicates by DOI/title, and tag them as candidates.

For full text, the workflow checks whether Zotero already has a readable PDF attachment. If not, it tries Zotero's PDF/full-text retrieval path or uses the publisher/DOI/arXiv page with Zotero Connector. Missing PDFs are logged instead of quietly ignored.

## Reading Gate

Before writing evidence-heavy sections, every core paper should have:

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

Allowed statuses:

```text
unread
skimmed
full_text_read
cannot_read
parked
```

Only `full_text_read` should support central claims.

The intended rule is stronger than "sample a few papers": all core screened-in papers must be read, and every central claim should map back to reading notes.

## Web GPT / ChatGPT Pro Review

The helper script builds a local packet:

```bash
python3 scripts/build_external_review_packet.py \
  --draft path/to/current_draft.md \
  --out path/to/external_review_packet.md \
  --target-journal "Target Journal Name" \
  --notes path/to/evidence_matrix.md path/to/claim_audit.md
```

The script does **not** upload anything.

If an agent is going to paste the packet into Web GPT / ChatGPT Pro, it should ask first and state exactly what will be shared.

## Journal And Reviewer Loop

After the manuscript stabilizes:

1. Choose or confirm the target journal.
2. Record the journal's requirements.
3. Revise the paper to that journal.
4. Run reviewer mode.
5. Revise again.
6. Run final QA.

This is where the paper becomes submission-shaped rather than just "well written."

## Privacy

Do not commit live project artifacts to a public repo:

- manuscripts
- PDFs or DOCX files
- Zotero exports from an active project
- review packets
- author metadata
- reviewer comments
- submission forms

The `.gitignore` is conservative on purpose.

## License

No license file has been added yet. Add one before inviting reuse or contributions.
