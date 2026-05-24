# Literature Survey Writer

An Agent Skill for building evidence-grounded academic survey papers with Zotero-backed corpus auditing, synthesis-first drafting, external GPT review loops, and submission-package QA.

This skill is designed for researchers who do not just want a list of papers. It helps an agent move from a topic or an existing Zotero library to a traceable literature corpus, a synthesis-heavy manuscript, an external review packet, and a final checklist for journal submission.

## What It Does

- Audits existing Zotero collections, BibTeX/RIS exports, or local session folders.
- Separates full-text evidence, abstract/metadata-level records, parked records, and duplicates.
- Builds reading matrices, corpus audits, claim audits, and citation consistency checks.
- Guides survey-paper drafting around themes, systems patterns, comparison tables, and evidence gaps.
- Generates external GPT review packets without uploading anything automatically.
- Supports revision loops that turn review feedback into actionable writing/checking tasks.
- Keeps manuscript claims bounded by the available corpus.

## When To Use It

Use this skill when you are working on:

- literature reviews or survey papers
- Zotero-backed manuscript workflows
- BibTeX/RIS export and cleanup
- paper-corpus auditing
- synthesis-heavy related-work sections
- reviewer-style critique and revision prompts
- pre-submission manuscript QA

Chinese/CNKI workflows are intentionally opt-in. The default workflow is English-first.

## Repository Layout

```text
literature-survey-writer/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── build_external_review_packet.py
├── .gitignore
└── README.md
```

`SKILL.md` is the main file read by compatible agents. `agents/openai.yaml` provides UI-facing metadata and declares the optional Zotero MCP dependency. The script folder contains a small deterministic helper for building review packets.

## Installation

Clone this repository into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/LanqinYang/literature-survey-writer.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/literature-survey-writer"
```

Restart Codex so it can discover the new skill metadata.

You can then invoke it naturally:

```text
Use $literature-survey-writer to audit my Zotero-backed corpus and draft a survey-paper revision plan.
```

Or describe the task directly:

```text
I have a Zotero collection and a draft survey paper. Check whether the corpus is enough, identify evidence gaps, and prepare a revision checklist.
```

## Zotero MCP

The skill works best with Zotero MCP enabled, but it can still use local exports.

With Zotero MCP, the agent can:

- search collections and metadata
- inspect item children and PDF availability
- read annotations or full text when attachments are available
- check duplicates and tags
- add records by DOI/URL when write mode is configured

If Zotero MCP is read-only or local-only, the skill falls back to export files such as:

```text
references.md
references.bib
references.ris
reading_matrix.md
corpus_audit.md
```

The skill treats Zotero as a reference manager and audit workspace, not as a bibliographic database or search engine.

## External GPT Review Packet

The included helper script builds a Markdown packet that can be pasted into ChatGPT, Web GPT Pro, or another external reviewer after the user explicitly approves sharing the manuscript text.

Example:

```bash
python3 scripts/build_external_review_packet.py \
  --draft path/to/current_draft.md \
  --out path/to/external_review_packet.md \
  --target-journal "Target Journal Name" \
  --notes path/to/corpus_audit.md path/to/citation_consistency_audit.md
```

The script does not upload files, call an API, or contact a third-party service. It only creates a local Markdown review packet.

## Privacy And Safety

This workflow may involve unpublished manuscripts, author metadata, Zotero libraries, PDFs, annotations, and reviewer feedback. The skill therefore requires an explicit consent gate before any external upload.

By default:

- no manuscript is sent to external GPT services automatically
- no Zotero collection is uploaded automatically
- no PDF, DOCX, BibTeX, RIS, or CSV artifact should be committed to a public repo
- generated review packets should stay local unless the user approves sharing

The `.gitignore` is intentionally conservative and excludes common manuscript and reference artifacts.

## Suggested Workflow

1. Start with a topic, Zotero collection, or existing manuscript session.
2. Audit the corpus and classify evidence levels.
3. Build a reading matrix and claim audit.
4. Draft or revise the survey around synthesis rather than paper-by-paper summaries.
5. Generate an external review packet if a second-model review is useful.
6. Convert feedback into critical, high, medium, and optional revision items.
7. Rebuild the submission package and run citation, figure, table, and page-count checks.

## Design Notes

This skill follows the Agent Skills pattern: keep `SKILL.md` as the primary agent-facing instruction file, use optional scripts for deterministic work, and keep detailed local manuscript artifacts outside the public skill repo.

The repository-level README is for human users browsing GitHub. Compatible agents should load `SKILL.md`, not this README, as the operational instruction source.

## License

No license file has been added yet. Add a license before redistributing or accepting external contributions.
