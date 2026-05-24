---
name: literature-survey-writer
description: |
  Use this skill to run an evidence-grounded, English-first academic literature survey workflow from topic intake or an existing Zotero corpus through screening, synthesis-heavy manuscript drafting, external GPT review, revision, and submission-package QA. It is especially useful when the user mentions literature review, survey paper, Zotero MCP, BibTeX/RIS export, manuscript drafting, reviewer-style critique, Web GPT Pro review, or journal submission preparation. Chinese/CNKI workflows are opt-in only.
---

# Literature Survey Writer

This skill upgrades a basic literature-review workflow into a full survey-paper production loop:

1. Build or audit a corpus.
2. Separate evidence levels.
3. Draft a synthesis-first manuscript.
4. Run an external review loop when authorized.
5. Convert review feedback into actionable prompts.
6. Revise, package, and QA the submission artifacts.

Default language for papers, searches, citations, and outputs is English unless the user asks otherwise.

## Operating Rules

- Prefer English scholarly sources and metadata platforms. Use Chinese/CNKI sources only when explicitly requested.
- Treat Zotero as a reference manager, corpus workspace, and audit layer, not as a search engine.
- Do not send manuscripts, Zotero libraries, PDFs, annotations, or unpublished drafts to third-party services without explicit user approval.
- Distinguish full-text-backed claims, abstract/metadata-level observations, and parked/excluded records.
- Do not call a narrative survey a systematic review unless the search, screening, and reporting protocol actually supports that label.
- Preserve numbered citations if the target journal/package uses numeric references.
- Keep final claims bounded by the corpus. Avoid invented novelty, fake publications, or unsupported "first/novel" wording.
- Continue from existing session files when present; do not restart a corpus workflow just because the user asks a new revision question.

## Mode Selection

Choose the mode before acting:

- **Search-first**: The user has a topic but no corpus. Generate queries, search public scholarly sources, deduplicate, and export references.
- **Zotero-first**: The user has a Zotero collection, BibTeX/RIS, or local corpus. Audit it first, then fill only meaningful gaps.
- **Continuation**: A `sessions/<date>_<topic>/` folder or previous outputs already exist. Read the current state files and continue from the latest draft/package.
- **Manuscript-hardening**: A draft already exists. Focus on claim audit, external review, revision prompts, citations, formatting, and submission QA.

## Recommended Session Layout

Use a stable session folder such as:

```text
sessions/YYYYMMDD_topic_short/
  session_log.md
  metadata.json
  papers_raw.json
  papers_deduplicated.json
  output/
    references.md
    references.bib
    references.ris
    corpus_audit.md
    reading_matrix.md
    review_outline.md
    literature_review_draft_v01.md
    submission_package_vNN_label_YYYYMMDD/
```

For continuation work, create a `README_current_state_YYYYMMDD.md` or equivalent entry point that identifies the authoritative files and marks older files as historical.

## Corpus Workflow

### 1. Audit Existing Sources

When Zotero or local exports exist, audit before searching:

- Count top-level records, attachments, notes, duplicates, missing DOI/URL, and missing PDFs.
- Classify each record as core, supporting, context, parked, duplicate, or excluded.
- Record whether evidence is full text, abstract/metadata only, or externally recovered.
- If Zotero MCP cannot write because it is local-only, export RIS/BibTeX/CSV fallback files and tell the user to import them manually.

Useful Zotero MCP actions when available:

- Search: semantic search, item search, tag search, collection listing.
- Read: metadata, child items, annotations, full text when an attachment exists.
- Organize: add by DOI/URL, batch tags, duplicate detection, collection management.

Never treat missing Zotero full text as proof that a paper is unusable. Log it as one of:

- metadata present
- no suitable attachment/full text in Zotero
- externally readable fallback exists
- needs PDF attachment repair before extraction

### 2. Fill Gaps Deliberately

Use public metadata and literature platforms to fill clear gaps:

- Google Scholar for discovery and related work.
- Semantic Scholar, OpenAlex, and Crossref for DOI and metadata.
- Publisher pages for authoritative metadata and abstracts.
- IEEE Xplore, ACM Digital Library, arXiv, PubMed, ScienceDirect, SpringerLink, Wiley, Taylor & Francis, SAGE, and JSTOR as domain-appropriate.

Search expansion should target gaps such as recency, missing baselines, undercovered methods, or target-journal positioning. Avoid expanding the corpus simply to increase paper count.

### 3. Build Evidence Matrices

For survey papers, build synthesis assets before expanding prose:

```markdown
| ID | Citation | Role | Theme | Method/System | Deployment level | AI task/model | Evidence type | Key contribution | Limitation/Gaps | Status |
|---|---|---|---|---|---|---|---|---|---|---|
```

Also maintain:

- `corpus_audit.md`
- `reading_matrix.md`
- `claim_audit.md`
- `citation_consistency_audit.md`
- `table_rebuild_plan.md` when the article depends on analytical tables

## Manuscript Drafting Workflow

Draft around synthesis, not paper-by-paper summaries.

1. Create a review question and scope boundary.
2. Write a transparent corpus/method paragraph appropriate to the evidence level.
3. Build a taxonomy or comparison framework.
4. Create analytical tables before long prose when the field is broad.
5. Draft sections around patterns, tensions, and deployment constraints.
6. Add a positioning table against close surveys when novelty or journal fit is a risk.
7. Add open challenges that arise from the evidence tables, not generic future work.

Use precise wording:

- Prefer "structured narrative survey" or "criteria-based corpus" unless systematic-review reporting is available.
- Say "Zotero was used to manage, deduplicate, tag, and audit the corpus"; do not say Zotero produced the literature.
- Mark emerging areas as emerging when evidence is mostly recent, prototype-level, or abstract-level.

## External GPT Review Loop

This replaces the manual pattern: user pastes the manuscript into Web GPT Pro, receives critique/prompt, then pastes that prompt back into Codex.

### Consent Gate

Before using ChatGPT/Web GPT Pro, another web model, or any third-party service:

1. State what will be uploaded.
2. State whether it includes unpublished manuscript text, references, author metadata, or review notes.
3. Ask for explicit approval.
4. If approval is not given, generate a local review prompt packet instead.

### Review Packet

Prepare a compact packet rather than dumping the whole workspace:

- Current draft or selected sections.
- Target journal and constraints.
- Corpus counts and evidence-level summary.
- Known high-risk claims.
- Citation/reference audit results.
- Specific review questions.

Use `scripts/build_external_review_packet.py` to assemble a Markdown packet:

```bash
python3 skills/literature-survey-writer/scripts/build_external_review_packet.py \
  --draft path/to/current_draft.md \
  --out path/to/external_review_packet.md \
  --target-journal "Target Journal Name" \
  --notes path/to/corpus_audit.md path/to/citation_consistency_audit.md
```

### Browser Automation

If the user approves and an authenticated browser is available:

1. Open the user's logged-in ChatGPT/Web GPT Pro page with the browser or Chrome tool.
2. Paste the review packet or upload the allowed file.
3. Ask for a structured critique plus an actionable revision prompt.
4. Save the returned critique/prompt into the session output.
5. Apply only the feedback that is consistent with the evidence and target journal.

If automation is unavailable, provide the generated packet and wait for the user to paste back the external model's critique.

### External Review Prompt

Ask the external reviewer for:

- Blocking issues.
- Unsupported claims.
- Missing close surveys or baselines.
- Method/corpus transparency risks.
- Citation and numbering risks.
- Journal-fit and page-limit risks.
- A concise revision prompt that Codex can execute.

## Revision and QA Workflow

After each external or internal review:

1. Convert feedback into a checklist with critical, high, medium, and optional items.
2. Apply revisions to the manuscript source.
3. Re-run citation/reference consistency checks.
4. Rebuild DOCX/PDF if requested or needed.
5. Render pages or otherwise visually inspect the final artifact.
6. Write a change log and remaining human-confirmation checklist.

Submission-package artifacts commonly include:

- current manuscript Markdown
- DOCX and/or PDF
- figures and source figures
- highlights file when the journal requires it
- `README_submission_package.md`
- `docx_qa_report_YYYYMMDD.md`
- `author_submission_checklist_YYYYMMDD.md`
- `pre_submission_skill_checklist_YYYYMMDD.md`
- reference exports if useful: `references.bib`, `references.ris`

## Quality Gates

Before declaring a manuscript ready, check:

- All in-text citations map to reference-list entries.
- Reference numbering is continuous if numeric style is used.
- Tables and figures are numbered continuously.
- Figure files exist and render correctly.
- Page count fits the target journal when there is a page limit.
- Title-page metadata is explicitly marked for human confirmation.
- Data availability, generative-AI disclosure, conflicts/funding, and CRediT statements match journal requirements.
- Any optional systematic-review appendix is described as optional unless required.

## Output Style

Give direct sufficiency judgments:

- "Enough to draft now" when corpus coverage is broad and gaps are manageable.
- "Enough for a narrative survey, not enough for a systematic review" when protocol reporting is incomplete.
- "Need targeted supplement" only when a specific gap affects the argument.

Keep user-facing updates concise and evidence-led. The purpose of the skill is to help finish an article, not to keep searching indefinitely.
