#!/usr/bin/env python3
"""Scaffold the production-state files for a survey-paper workflow."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", text.strip().lower()).strip("_")
    return slug or "literature_survey"


FILES = {
    "session_log.md": "# Session Log\n\n",
    "keywords_and_queries.md": "# Keywords And Queries\n\nRecord user keywords, expanded terms, Boolean queries, source plans, and exclusion terms here.\n",
    "candidate_export_status.md": "# Candidate Export Status\n\n- references.md: pending\n- references.bib: pending\n- references.ris: pending\n",
    "zotero_import_log.md": "# Zotero Import Log\n\nRecord MCP imports, duplicate checks, fallback RIS/BibTeX imports, and failures here.\n",
    "screening_matrix.csv": "id,citation,doi_or_url,theme,full_text_status,screening_decision,reason,notes\n",
    "reading_queue.md": "# Reading Queue\n\nCentral-claim papers must reach `full_text_read` before manuscript drafting.\n\n",
    "reading_notes.md": "# Reading Notes\n\n",
    "evidence_matrix.md": "# Evidence Matrix\n\n| ID | Citation | Evidence level | Theme | Method/System | Key finding | Limitation | Claim supported | Section |\n|---|---|---|---|---|---|---|---|---|\n",
    "claim_audit.md": "# Claim Audit\n\n| Claim | Supporting papers | Evidence level | Risk | Safe wording | Needs more reading? |\n|---|---|---|---|---|---|\n",
    "writing_handoff.md": "# Writing Handoff\n\n## Scope\n\n## Corpus Counts\n\n## Evidence Hierarchy\n\n## Central Claims\n\n## Claims To Avoid Or Soften\n\n## Draft Structure\n\n",
    "web_gpt_review_log.md": "# Web GPT Review Log\n\nDo not paste unpublished material into external services without explicit approval.\n",
    "journal_requirements.md": "# Journal Requirements\n\n## Target Journal\n\n## Scope Fit\n\n## Formatting\n\n## Declarations\n\n## Submission Artifacts\n\n",
    "reviewer_mode_report.md": "# Reviewer Mode Report\n\n## Critical Issues\n\n## High-Priority Revisions\n\n## Medium-Priority Revisions\n\n## Optional Improvements\n\n",
    "pre_submission_checklist.md": "# Pre-Submission Checklist\n\n- [ ] Central claims map to read evidence\n- [ ] Citation/reference mapping checked\n- [ ] Tables and figures checked\n- [ ] Target-journal requirements checked\n- [ ] Declarations checked\n- [ ] Author metadata confirmed by human\n- [ ] No private artifacts included in public repo\n",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize a survey-paper production session.")
    parser.add_argument("--topic", required=True, help="Short project topic or keyword set.")
    parser.add_argument("--root", default="sessions", help="Root directory for session folders.")
    parser.add_argument("--date", default=date.today().strftime("%Y%m%d"), help="Date prefix, default today.")
    args = parser.parse_args()

    session = Path(args.root) / f"{args.date}_{slugify(args.topic)}"
    session.mkdir(parents=True, exist_ok=True)
    (session / "output").mkdir(exist_ok=True)

    for name, content in FILES.items():
        path = session / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    print(session)


if __name__ == "__main__":
    main()
