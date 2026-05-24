#!/usr/bin/env python3
"""Build a compact manuscript-review packet for external GPT review.

The script does not upload anything. It creates a Markdown packet that can be
pasted manually or sent through an explicitly approved browser automation step.
"""

from __future__ import annotations

import argparse
from pathlib import Path


DEFAULT_QUESTIONS = [
    "Identify blocking issues that would weaken journal submission.",
    "Find unsupported, overstated, or unclear claims.",
    "Check whether the corpus/method description matches a narrative survey rather than a systematic review.",
    "Flag missing close surveys, comparator studies, or target-journal positioning risks.",
    "Check citation/reference, table/figure numbering, and page-limit risks when evidence is provided.",
    "Return a concise, actionable revision prompt that another coding/writing agent can execute.",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def clip(text: str, limit: int) -> str:
    if limit <= 0 or len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n\n[TRUNCATED FOR REVIEW PACKET]\n"


def build_packet(args: argparse.Namespace) -> str:
    draft = clip(read_text(args.draft), args.max_draft_chars)
    note_blocks = []
    for note in args.notes:
        note_text = clip(read_text(note), args.max_note_chars)
        note_blocks.append(f"## Supporting Note: {note.name}\n\n{note_text}")

    questions = "\n".join(f"{idx}. {q}" for idx, q in enumerate(DEFAULT_QUESTIONS, 1))
    extra = f"\n\nAdditional user instructions:\n{args.instructions.strip()}\n" if args.instructions else ""

    return f"""# External GPT Manuscript Review Packet

Target journal: {args.target_journal or "Not specified"}
Manuscript stage: {args.stage}

## Review Task

You are reviewing an academic survey manuscript. Be strict but practical. Separate blocking issues from optional improvements. Do not invent missing papers, claims, or journal rules. If a concern depends on unavailable evidence, mark it as a check rather than a fact.

Please answer these questions:

{questions}
{extra}
## Manuscript Draft

{draft}

{"\n\n".join(note_blocks) if note_blocks else "## Supporting Notes\n\nNo supporting notes were provided."}

## Required Output Format

1. Overall readiness score out of 100.
2. Critical issues.
3. High-priority revisions.
4. Medium-priority improvements.
5. Citation/mechanical checks.
6. One concise revision prompt for Codex to execute.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an external GPT review packet.")
    parser.add_argument("--draft", required=True, type=Path, help="Path to the current manuscript draft.")
    parser.add_argument("--out", required=True, type=Path, help="Output Markdown packet path.")
    parser.add_argument("--target-journal", default="", help="Target journal or venue.")
    parser.add_argument("--stage", default="pre-submission revision", help="Manuscript stage label.")
    parser.add_argument("--instructions", default="", help="Extra review instructions.")
    parser.add_argument("--notes", nargs="*", type=Path, default=[], help="Optional audit/checklist files.")
    parser.add_argument("--max-draft-chars", type=int, default=120000, help="Maximum draft characters to include.")
    parser.add_argument("--max-note-chars", type=int, default=20000, help="Maximum characters per supporting note.")
    args = parser.parse_args()

    for path in [args.draft, *args.notes]:
        if not path.exists():
            raise SystemExit(f"Missing input file: {path}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(build_packet(args), encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
