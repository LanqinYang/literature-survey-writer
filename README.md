# Literature Review + Zotero MCP Workflow

[English](README.md) | [简体中文](README.zh-CN.md)

This fork is based on [AI-Powered-Literature-Review-Skills](https://github.com/stephenlzc/AI-Powered-Literature-Review-Skills).

The upstream skill already does a lot: keyword expansion, English-first literature search, database browsing, deduplication, Markdown/BibTeX/RIS export, citation formatting, paper analysis, and draft/review/final synthesis.

This version keeps that base, but leans hard into the part that gets messy in real projects: turning search results into an **evidence-controlled survey manuscript** through Zotero MCP, reading gates, claim audits, and review loops.

In one sentence:

> A Codex skill for moving from literature search results to survey drafts without letting "imported into Zotero" quietly become "read and understood."

The workflow looks like this:

```text
keywords
  -> search/export from the literature-review workflow
  -> Zotero MCP import or RIS/BibTeX fallback
  -> PDF / full-text audit
  -> screening and role assignment
  -> mandatory reading gate
  -> evidence matrix and claim audit
  -> manuscript writing from read evidence
  -> optional Atlas / ChatGPT Pro review through GitHub source
  -> target-journal adaptation
  -> reviewer-mode stress test
  -> final submission QA
```

The core idea is simple:

> Finding papers is not the same as reading papers.  
> Importing papers into Zotero is not the same as understanding them.  
> A claim in the manuscript should trace back to read evidence.

## What Upstream Already Covers

The original skill already covers the front half well:

- turning a topic into search keywords and Boolean queries
- searching English-first scholarly sources
- optional Chinese/CNKI flow
- collecting title/author/year/venue/DOI/abstract metadata
- deduplicating candidates
- exporting `references.md`, `references.bib`, and `references.ris`
- formatting citations
- creating paper analysis and literature-review drafts
- running a draft review/finalization phase

So this fork should not pretend those are new.

## What This Fork Adds

The extra focus here is what happens after the paper list exists:

- Zotero MCP import instead of only Zotero-compatible exports.
- A fallback path for manual RIS/BibTeX import when MCP write mode is unavailable.
- Full-text / PDF attachment audit inside Zotero.
- Explicit states for metadata-only, abstract-only, readable PDF, missing PDF, duplicate/version, and parked papers.
- A stricter reading gate before evidence-heavy writing.
- `evidence_matrix.md` and `claim_audit.md` as handoff files.
- An optional external GPT review packet, plus a tested Atlas / ChatGPT Pro path using the GitHub source connector.
- Target-journal requirements and reviewer-mode QA.

Or, less politely:

> It tries to stop the workflow from saying "we reviewed the literature" when all we really did was import a pile of records.

## Who This Is For

Good fit:

- PhD/MSc students writing survey papers.
- Researchers preparing journal literature-review sections.
- Codex users who want Zotero-backed evidence control, not just citation collection.
- Anyone who needs every central claim to trace back to reading notes.

Not the right promise:

- It is not a one-click paper generator.
- It does not replace reading core papers.
- It does not make private manuscripts safe to paste into external GPT tools.

## The Rule

> Zotero import is not reading.

Central claims should come from papers marked as `full_text_read`, with notes that explain what the paper actually supports.

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

## Atlas / External GPT Review

The helper script builds a local review packet:

```bash
python3 scripts/build_external_review_packet.py \
  --draft path/to/current_draft.md \
  --out path/to/external_review_packet.md \
  --target-journal "Target Journal Name" \
  --notes path/to/evidence_matrix.md path/to/claim_audit.md
```

The script does **not** upload anything.

If an agent will paste the packet into Web GPT / ChatGPT Pro, or ask Web GPT to read a GitHub URL, it must first state what will be shared and get explicit approval.

Tested Atlas route on 2026-05-25:

1. Push the public, sanitized repo state to GitHub.
2. In ChatGPT Atlas, open the prompt composer.
3. Click `+`.
4. Choose `More`.
5. Choose `GitHub` as the source.
6. Ask ChatGPT Pro to read the public GitHub README or specific repo files and return feedback plus a revision prompt.
7. Bring the feedback back to Codex, save it in `web_gpt_review_log.md`, revise, commit, and repeat.

Directly pasting a GitHub URL without selecting the GitHub source was not reliable in testing. Treat the source-selection step as required.

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
