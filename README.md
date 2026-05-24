# Literature Survey Writer

Turn a messy paper pile into a review article that can actually survive revision.

This is an Agent Skill for writing academic literature surveys with a real working loop:

```text
topic or Zotero library
  -> corpus audit
  -> evidence matrix
  -> synthesis-heavy draft
  -> external GPT review packet
  -> revision checklist
  -> submission QA
```

It started from the very practical problem most literature-review tools do not solve: finding papers is only the first 20%. The hard part is knowing whether the corpus is enough, which claims are actually supported, how to avoid turning the paper into a giant annotated bibliography, and how to keep revisions from drifting away from the evidence.

## Why This Exists

Most "literature review" prompts produce one of two things:

- a polite list of papers
- a generic mini-essay with citations sprinkled in

That is not enough for a serious survey manuscript.

This skill is built for the more annoying, more useful workflow:

- You already have papers in Zotero, but you do not know whether the corpus is balanced.
- Some papers have full text, some only have metadata, some are duplicates, and some are probably not worth reading.
- You need a survey that synthesizes patterns across papers, not one paragraph per paper.
- You want another model, such as ChatGPT / Web GPT Pro, to critique the draft, but you do not want to paste everything manually forever.
- You need submission-facing checks: citations, tables, figures, page count, declarations, and remaining author-confirmation items.

## What The Skill Does

It helps an agent:

- audit a Zotero collection or local reference export
- separate full-text evidence from abstract-only or metadata-only records
- build reading matrices and claim audits
- decide whether the corpus is enough to start writing
- draft around themes, systems, tensions, and gaps
- create a safe external-review packet for another GPT model
- turn critique into a concrete revision checklist
- prepare manuscript QA artifacts before submission

The default workflow is English-first. Chinese/CNKI workflows are opt-in, not the default.

## What It Is Not

This is not a magic paper generator.

It will not make unsupported novelty claims true. It will not turn a weak corpus into a systematic review. It will not upload your unpublished manuscript somewhere without permission. It is designed to keep the writing process honest, traceable, and less chaotic.

## Install

Clone the repo into your Codex skills folder:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/LanqinYang/literature-survey-writer.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/literature-survey-writer"
```

Restart Codex so it can discover the skill.

Then use it like this:

```text
Use $literature-survey-writer to audit my Zotero-backed corpus and tell me whether it is enough for a survey paper.
```

Or:

```text
Use $literature-survey-writer to turn this draft into a stronger synthesis-heavy survey and prepare a pre-submission checklist.
```

## Files

```text
literature-survey-writer/
├── SKILL.md                              # agent instructions
├── agents/openai.yaml                    # Codex-facing metadata
├── scripts/build_external_review_packet.py
├── .gitignore
└── README.md
```

`SKILL.md` is the real skill. This README is just the front door for humans browsing GitHub.

## Zotero Workflow

The skill works best when Zotero MCP is available, but it can still work from local exports.

Useful inputs include:

```text
references.md
references.bib
references.ris
corpus_audit.md
reading_matrix.md
claim_audit.md
citation_consistency_audit.md
```

The skill treats Zotero as a reference manager and audit workspace. It does not pretend Zotero is a scholarly search database.

If Zotero MCP can only read locally, the skill falls back to BibTeX/RIS/CSV exports instead of forcing direct writes.

## External GPT Review

One real use case is this loop:

1. Codex writes or revises the manuscript.
2. A stronger web model reviews it.
3. The web model returns critique and a revision prompt.
4. Codex applies the prompt, but only where the evidence supports it.

The helper script packages the draft and supporting notes into a Markdown review packet:

```bash
python3 scripts/build_external_review_packet.py \
  --draft path/to/current_draft.md \
  --out path/to/external_review_packet.md \
  --target-journal "Target Journal Name" \
  --notes path/to/corpus_audit.md path/to/citation_consistency_audit.md
```

The script does **not** upload anything. It only creates a local file.

If you want an agent to open ChatGPT / Web GPT Pro and paste the packet, the skill requires explicit approval first, because unpublished manuscripts and Zotero notes can be sensitive.

## Privacy Rules

By default, keep these out of public repos:

- unpublished manuscripts
- Zotero libraries and exported reading notes
- PDFs and DOCX files
- BibTeX/RIS/CSV files from a live project
- external GPT review packets
- author metadata, emails, ORCID IDs, and submission forms

The included `.gitignore` is intentionally conservative for that reason.

## A Good Run Looks Like

A good workflow usually produces artifacts like:

```text
corpus_audit.md
reading_matrix.md
claim_audit.md
review_outline.md
literature_review_draft_v01.md
external_review_packet.md
revision_checklist.md
pre_submission_checklist.md
```

The important part is not the filenames. The important part is that claims, citations, evidence level, and revision decisions stay connected.

## License

No license file has been added yet. Add one before inviting reuse or contributions.
