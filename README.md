# Literature Review + Zotero MCP Workflow

[English](README.md) | [简体中文](README.zh-CN.md)

A Codex skill for turning keywords into a Zotero-backed literature review or survey manuscript.

It covers the whole loop:

```text
keywords
  -> paper search
  -> BibTeX/RIS/DOI capture
  -> Zotero MCP import
  -> full-text retrieval
  -> screening
  -> mandatory reading
  -> evidence matrix
  -> manuscript writing
  -> Web GPT / ChatGPT Pro review
  -> target-journal adaptation
  -> reviewer-mode critique
  -> final submission QA
```

The core idea is simple:

> Finding papers is not the same as reading papers.  
> Importing papers into Zotero is not the same as understanding them.  
> A claim in the manuscript should trace back to read evidence.

## Why This Exists

Most AI-assisted literature review workflows are good at the first step:

> "Here are papers related to your keywords."

The difficult part comes next:

- Which papers should actually enter the Zotero project?
- Which ones have real full text?
- Which papers were screened out, parked, or kept only for background?
- Which papers were fully read?
- Which claim can each paper support?
- When is the corpus strong enough to start writing?
- How do you avoid one-paper-one-paragraph writing?
- How do you use Web GPT / ChatGPT Pro as a reviewer without losing track of revisions?
- How do you adapt the paper to a chosen journal?
- How do you run reviewer mode before actual reviewers see the paper?

This skill keeps that chain explicit.

## What The Skill Does

- Expands user keywords into search terms and query plans.
- Captures candidate papers from scholarly sources.
- Exports or records candidate metadata as Markdown, BibTeX, RIS, DOI, or URL lists.
- Imports candidates into Zotero through Zotero MCP when available.
- Provides a manual RIS/BibTeX fallback when Zotero MCP write mode is unavailable.
- Checks PDF/full-text availability in Zotero.
- Tracks whether each paper is unread, skimmed, full-text-read, unavailable, or parked.
- Forces a reading gate before evidence-heavy writing.
- Builds evidence matrices and claim audits.
- Hands read evidence into manuscript writing.
- Builds external GPT review packets.
- Tracks target-journal requirements.
- Runs reviewer-mode critique and pre-submission QA.

## Install

Recommended: ask Codex to install it for you.

```text
帮我安装这个 skill: https://github.com/LanqinYang/literature-survey-writer
```

Manual install:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/LanqinYang/literature-survey-writer.git "${CODEX_HOME:-$HOME/.codex}/skills/literature-survey-writer"
```

Restart Codex after installation.

Example prompt:

```text
Use $literature-survey-writer to start from these keywords, find papers, import them into Zotero with Zotero MCP, screen them, read the selected papers, and prepare the manuscript-writing handoff.
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

These files keep the workflow honest: what was found, what entered Zotero, what was screened, what was read, what can be claimed, and what still needs work.

## Zotero MCP And RIS/BibTeX

With Zotero MCP, the skill can:

- search the local Zotero library before importing
- add records by DOI or URL
- inspect item children and attachments
- read full text when a readable attachment exists
- tag workflow states
- check duplicates

If Zotero MCP cannot write, use the manual import fallback:

```text
Zotero -> File -> Import... -> A file -> choose references.ris or references.bib
```

After import:

1. Move imported records into the project collection.
2. Check duplicates by DOI/title.
3. Tag imported items as candidates.
4. Record the import file, count, and problems in `zotero_import_log.md`.

Zotero can also import RIS/BibTeX from the clipboard with `File -> Import from Clipboard`; use that only for small batches.

## Full Text In Zotero

The workflow checks whether each imported paper has readable full text:

1. Check whether the Zotero item has a PDF attachment.
2. If a PDF exists, read it through Zotero MCP when possible.
3. If only metadata exists, try Zotero's PDF/full-text retrieval path or use the publisher/DOI/arXiv page with Zotero Connector.
4. If a legal PDF is found elsewhere, attach it to the correct Zotero parent item or mark it as externally readable.
5. If full text cannot be retrieved, mark it clearly instead of pretending it was read.

Useful full-text states:

```text
zotero_pdf_readable
zotero_metadata_only
external_fulltext_available
abstract_only
needs_pdf_attachment
unavailable
duplicate_or_version
```

## Reading Gate

Before writing evidence-heavy manuscript sections, core screened-in papers must be read.

Each core paper should have:

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

Rules:

- All `include_core` papers must be read.
- Important `include_supporting` papers should be read or downgraded.
- Only `full_text_read` should support central claims.
- `skimmed` is for background framing.
- metadata-only or abstract-only records are for gap checking, not central claims.
- The agent should not say "all papers were read" unless reading notes exist.

## Web GPT / ChatGPT Pro Review

The helper script builds a local review packet:

```bash
python3 scripts/build_external_review_packet.py \
  --draft path/to/current_draft.md \
  --out path/to/external_review_packet.md \
  --target-journal "Target Journal Name" \
  --notes path/to/evidence_matrix.md path/to/claim_audit.md
```

The script does **not** upload anything.

If an agent will paste the packet into Web GPT / ChatGPT Pro, it must first state what will be shared and get explicit approval.

## Journal And Reviewer Loop

After the manuscript stabilizes:

1. Choose or confirm the target journal.
2. Record journal requirements: scope, article type, word/page limits, citation style, figures, declarations, AI disclosure, data availability, and required files.
3. Revise the paper to the journal.
4. Run reviewer mode.
5. Revise again.
6. Run final QA.

This is where the manuscript becomes submission-shaped rather than merely "well written."

## Privacy

Do not commit live project artifacts to a public repo:

- unpublished manuscripts
- PDFs or DOCX files
- active Zotero exports
- external review packets
- author metadata
- reviewer comments
- submission forms

The `.gitignore` is conservative on purpose.

## License

No license file has been added yet. Add one before inviting reuse or contributions.
