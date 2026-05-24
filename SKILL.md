---
name: literature-survey-writer
description: |
  Use this skill as a production overlay on top of an existing literature-review/search skill and Zotero MCP. It coordinates the real survey-paper workflow: start from user keywords, reuse the baseline literature-reviewer skill for English-first search and candidate exports, import candidates into Zotero, retrieve full text, screen, enforce a mandatory reading gate, hand off to manuscript-writing, iterate with Web GPT/ChatGPT Pro review when approved, choose a target journal, revise to journal requirements, run reviewer-mode critique, and finish submission QA. Trigger for survey paper production, Zotero MCP literature workflows, Web GPT review loops, target-journal adaptation, reviewer mode, or manuscript hardening.
---

# Literature Survey Writer

This is not a replacement for a literature-search skill. It is the layer that makes the whole paper-production loop behave.

Use the baseline literature-reviewer skill for what it already does well:

- turn keywords into English-first search queries
- search scholarly platforms
- deduplicate candidates
- export `references.md`, `references.bib`, and `references.ris`
- create first-pass paper lists and metadata

Use this skill for the parts that usually break after that:

```text
keywords
  -> baseline literature-reviewer search/export
  -> Zotero MCP import and attachment audit
  -> screening
  -> mandatory reading gate
  -> evidence matrix
  -> manuscript-writing skill
  -> Web GPT review loop
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
keywords_and_queries.md          # produced by baseline literature-reviewer skill
candidate_export_status.md       # where references.md/BibTeX/RIS came from
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

Start from the user's keywords/topic. Invoke or follow the baseline literature-reviewer skill for search, deduplication, and export. Do not duplicate that skill's full search protocol here.

Expected outputs:

- raw or deduplicated candidate list
- `references.md`
- `references.bib`
- `references.ris`
- search notes or query log

Record what exists in `candidate_export_status.md`.

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

If the user asks to write too early, draft only safe scaffolding: outline, method wording, table shells, or reading plan. Do not synthesize unread papers as if they were read.

### 6. Evidence Matrix And Writing Handoff

After reading, build `evidence_matrix.md`:

```markdown
| ID | Citation | Evidence level | Theme | Method/System | Key finding | Limitation | Claim supported | Section |
|---|---|---|---|---|---|---|---|---|
```

Then write `writing_handoff.md` for the manuscript-writing skill:

- review question and scope
- corpus counts and evidence hierarchy
- target structure
- central claims and supporting evidence
- tables/figures to build
- claims to avoid or soften
- citation style preference if known

### 7. Manuscript Writing

Use a writing skill or manuscript-writing workflow after the reading gate passes.

Writing rules:

- synthesize across papers; do not summarize one paper per paragraph
- build analytical tables before long prose when the field is broad
- cite read evidence for central claims
- position against close surveys
- state corpus limitations honestly
- keep emerging areas marked as emerging when evidence is thin

### 8. Web GPT Review Loop

Use `scripts/build_external_review_packet.py` to create a local review packet.

Before uploading anything externally:

1. Say what will be sent.
2. Say whether it includes unpublished manuscript text, references, author metadata, Zotero notes, or reviewer materials.
3. Ask for explicit approval.

After Web GPT / ChatGPT Pro returns feedback:

- save it in `web_gpt_review_log.md`
- extract the revision prompt
- convert the critique into critical/high/medium/optional tasks
- revise only where the evidence supports the change
- repeat until the draft stabilizes

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
