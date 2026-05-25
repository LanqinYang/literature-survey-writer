---
name: literature-survey-writer
description: |
  Use this skill for a complete literature review / survey manuscript workflow linked with Zotero MCP. It starts from user keywords, searches for candidate papers, captures DOI/BibTeX/RIS/URL metadata, imports candidates into Zotero through Zotero MCP or manual RIS/BibTeX fallback, retrieves full text, screens the corpus, enforces mandatory reading before central claims are written, builds evidence matrices and claim audits, drafts the manuscript, iterates with approved Atlas/ChatGPT Pro review through the GitHub source connector or local review packets, adapts the paper to a target journal, runs reviewer-mode critique, and finishes submission QA. Trigger for 文献综述, literature review, survey paper, Zotero MCP, paper search, RIS/BibTeX import, full-text reading, Atlas GitHub review, Web GPT review, journal adaptation, reviewer mode, or manuscript submission preparation.
---

# Literature Review + Zotero MCP Workflow

This skill coordinates the full paper-production loop:

```text
keywords
  -> paper search
  -> DOI / URL / BibTeX / RIS capture
  -> Zotero MCP import
  -> full-text retrieval
  -> screening
  -> mandatory reading gate
  -> evidence matrix
  -> manuscript writing
  -> optional Atlas / ChatGPT Pro review through GitHub source
  -> target-journal adaptation
  -> reviewer-mode critique
  -> submission QA
```

## Hard Rules

- Do not write evidence-heavy manuscript sections from metadata alone.
- Papers that support central claims must be marked `full_text_read`.
- Zotero import is not reading. A paper in Zotero is only a managed record until its full text is read or explicitly downgraded.
- Abstract-only and metadata-only records may support gap checking, not central arguments.
- If Zotero MCP cannot write, use RIS/BibTeX fallback imports and record the fallback.
- If Zotero MCP cannot read full text, log whether the paper needs attachment repair, external retrieval, replacement, or parking.
- Do not upload drafts, Zotero notes, PDFs, author metadata, or reviewer materials to Web GPT/ChatGPT/other services without explicit user approval.
- Once a target journal is chosen, journal requirements override generic formatting preferences.
- Reviewer-mode feedback is a stress test, not generic polishing.

## Minimal State Files

Create or maintain these files in the working session:

```text
keywords_and_queries.md          # keywords, synonyms, Boolean queries, source plan
candidate_export_status.md       # candidate lists and references.md/BibTeX/RIS status
zotero_import_log.md             # MCP import or fallback import record
screening_matrix.csv             # include/support/park/exclude decisions
reading_queue.md                 # selected papers that must be read
reading_notes.md                 # actual paper notes after reading
evidence_matrix.md               # read evidence mapped to claims/sections
claim_audit.md                   # central claims, supporting papers, and wording boundaries
writing_handoff.md               # instructions for manuscript-writing phase
web_gpt_review_log.md            # external review packets, feedback, prompts
journal_requirements.md          # target-journal constraints
reviewer_mode_report.md          # reviewer-style critique after journal adaptation
pre_submission_checklist.md      # final QA and human-confirmation items
```

Use `scripts/init_survey_loop.py` to scaffold these files when starting a new project.

## Workflow

### 1. Keywords To Candidate Papers

Start from the user's keywords/topic. Generate:

- core English keywords
- synonyms and adjacent terms
- Boolean query strings
- database/platform-specific query plans
- exclusion terms for false positives

Use scholarly sources appropriate to the topic, such as Google Scholar, Semantic Scholar, OpenAlex, Crossref, IEEE Xplore, ACM Digital Library, arXiv, PubMed, ScienceDirect, SpringerLink, Wiley, Taylor & Francis, SAGE, JSTOR, and publisher DOI pages.

For each candidate paper, capture:

```text
title
authors
year
venue
DOI or URL
source
abstract if available
initial theme
why it may matter
```

Deduplicate by DOI first, then normalized title. Save candidate status in `candidate_export_status.md`. Create `references.md`, `references.bib`, or `references.ris` when useful for Zotero import.

### 2. Import Candidates Into Zotero

Use Zotero MCP when available:

- search Zotero first to avoid duplicates
- add candidates by DOI or URL
- inspect item children and attachment state
- tag records by workflow state
- record failures and fallbacks

Suggested tags:

```text
candidate
screened-in
screened-out
core
supporting
full-text-needed
full-text-read
parked
duplicate
```

If MCP write mode is unavailable, keep Zotero-importable `references.bib` / `references.ris` and tell the user to import them manually. Log this in `zotero_import_log.md`.

Manual RIS/BibTeX import fallback:

1. Open Zotero.
2. Use `File -> Import...`.
3. Choose `A file`.
4. Select the generated `.ris` or `.bib` file.
5. Import into a new collection or move imported items into the project collection.
6. Run duplicate detection or search by DOI/title before treating the import as clean.
7. Tag imported items as `candidate` or another project-specific workflow tag.

Zotero also supports importing raw RIS/BibTeX from the clipboard through `File -> Import from Clipboard`; use this only for small batches.

### 3. Retrieve Full Text And Audit Readability

For each candidate, record one state:

```text
zotero_pdf_readable
zotero_metadata_only
external_fulltext_available
abstract_only
needs_pdf_attachment
unavailable
duplicate_or_version
```

Do not treat `zotero_metadata_only` as read evidence. It is a retrieval status, not an evidence status.

Full-text retrieval sequence:

1. Check Zotero child items with MCP or UI. If a PDF attachment exists, try reading it through Zotero MCP.
2. If Zotero has metadata only, use Zotero's available PDF/full-text retrieval action or the Zotero Connector from the publisher/DOI/arXiv page.
3. If Zotero cannot retrieve the PDF, search for legal open versions: publisher open access page, arXiv, institutional repository, author page, or DOI landing page.
4. If a PDF is found outside Zotero, attach it to the correct parent item or mark it as externally readable.
5. If no full text can be retrieved, decide explicitly: replace, park, keep for abstract-level gap checking, or request manual user help.

Record the result in `zotero_import_log.md` or a full-text audit section. Do not allow silent missing-PDF failures.

### 4. Screen Before Reading

Screen papers into:

```text
include_core
include_supporting
context_only
abstract_gap_check
park
exclude
duplicate
```

Screening criteria should include topic fit, method/system relevance, publication quality, recency/foundational value, duplicate/version relationship, and full-text availability.

Give a direct sufficiency judgment after screening:

- enough to write after reading gate
- enough for narrative survey, not systematic review
- needs targeted supplement
- not enough yet

### 5. Mandatory Reading Gate

Before manuscript writing, create `reading_queue.md` from `include_core` and important `include_supporting` papers.

Every paper used for a central claim needs:

```text
citation
Zotero key / DOI / URL
read status
evidence type
main contribution
method/system
task/data/deployment setting
limitations
claim(s) it can support
planned manuscript section
```

Allowed read statuses:

```text
unread
skimmed
full_text_read
cannot_read
parked
```

Only `full_text_read` can support central claims. `skimmed` can support background framing. `cannot_read` and metadata-only items should be parked, replaced, or used only for gap awareness.

Reading completion rule:

- All `include_core` papers must be `full_text_read` before evidence-heavy writing begins.
- Important `include_supporting` papers should also be read; if not, downgrade their role and state why.
- If a selected paper cannot be read, change its status to `cannot_read` and choose one action: retrieve manually, replace, park, or use only for gap awareness.
- The agent must not say "all papers were read" unless every paper claimed as read has a reading note.

If the user asks to write too early, draft only safe scaffolding: outline, method wording, table shells, or reading plan. Do not synthesize unread papers as if they were read.

### 6. Evidence Matrix And Writing Handoff

After reading, build `evidence_matrix.md`:

```markdown
| ID | Citation | Evidence level | Theme | Method/System | Key finding | Limitation | Claim supported | Section |
|---|---|---|---|---|---|---|---|---|
```

Then write `writing_handoff.md`:

- review question and scope
- corpus counts and evidence hierarchy
- target structure
- central claims and supporting evidence
- tables/figures to build
- claims to avoid or soften
- citation style preference if known

### 7. Manuscript Writing

Write after the reading gate passes.

Writing rules:

- synthesize across papers; do not summarize one paper per paragraph
- build analytical tables before long prose when the field is broad
- cite read evidence for central claims
- position against close surveys
- state corpus limitations honestly
- keep emerging areas marked as emerging when evidence is thin

Writing handoff must include enough material to write without redoing search:

- read-paper count
- support/background/gap-check counts
- evidence matrix
- claim audit
- section plan
- citation style preference if already known
- claims that must be softened or avoided

### 8. Atlas / External GPT Review

Use `scripts/build_external_review_packet.py` to create a local review packet.

Before uploading anything externally:

1. Say what will be sent.
2. Say whether it includes unpublished manuscript text, references, author metadata, Zotero notes, or reviewer materials.
3. Ask for explicit approval.

If Web GPT / ChatGPT Pro or another external reviewer returns feedback:

- save it in `web_gpt_review_log.md`
- extract the revision prompt
- convert the critique into critical/high/medium/optional tasks
- revise only where the evidence supports the change
- repeat until the draft stabilizes

Tested Atlas / ChatGPT Pro GitHub-source loop:

1. Push the sanitized public repo or branch to GitHub.
2. In ChatGPT Atlas, click `+`.
3. Choose `More`.
4. Choose `GitHub` as the source.
5. Ask ChatGPT Pro to read the public README or named repo files and return feedback plus a revision prompt.
6. Bring the feedback back to Codex, save it in `web_gpt_review_log.md`, revise, commit, push, and repeat.

Do not treat plain URL pasting as reliable. In testing, directly pasting a GitHub URL could be handled as search/chat text rather than as repo access. The GitHub source connector step is required.

### 9. Target Journal Selection And Adaptation

When the manuscript is stable, choose or confirm the journal.

Record in `journal_requirements.md`:

- aims and scope fit
- article type
- word/page limits
- citation style
- figure/table limits
- formatting/template rules
- required declarations
- data availability policy
- generative-AI disclosure policy
- highlights, graphical abstract, biographies, CRediT, conflicts/funding

Then revise the paper to the journal, not to a generic "good paper" standard.

### 10. Reviewer Mode

After journal adaptation, run reviewer mode:

- missing literature
- weak novelty
- unsupported claims
- method/corpus transparency
- structure problems
- table/figure usefulness
- citation consistency
- target-journal fit
- likely rejection reasons

Save to `reviewer_mode_report.md`, revise again, then run final QA.

### 11. Final QA

Before saying the package is ready:

- all central claims map to read evidence
- citation/reference mapping is closed
- tables and figures are numbered and referenced
- target-journal requirements are checked
- PDF/DOCX render is visually inspected when applicable
- declarations are present
- author metadata is marked for human confirmation
- no external-review packet or Zotero export is accidentally included in public repo

The final answer should state what is ready, what still needs human confirmation, and what remains optional.
