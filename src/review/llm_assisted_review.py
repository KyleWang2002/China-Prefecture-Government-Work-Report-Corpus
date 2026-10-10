"""
Prepare human-in-the-loop LLM review packets for suspicious OCR spans.

This module never overwrites corpus text automatically.

It was added while packaging the repository to formalize the author's
manual / LLM-assisted review workflow. It is not presented as the exact
historical script used for every file.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SUSPICIOUS = [
    re.compile(r"�"),
    re.compile(r"[\u4e00-\u9fff]\s[\u4e00-\u9fff]\s[\u4e00-\u9fff]"),
    re.compile(r"[A-Za-z0-9][\u4e00-\u9fff][A-Za-z0-9]"),
]


def suspicious_lines(text: str) -> list[tuple[int, str]]:
    hits = []
    for i, line in enumerate(text.splitlines(), start=1):
        if any(pattern.search(line) for pattern in SUSPICIOUS):
            hits.append((i, line))
    return hits


def review_prompt(line: str, before: str = "", after: str = "") -> str:
    return (
        "You are checking OCR from a Chinese municipal government work report. "
        "Do not paraphrase or modernize the language. Correct only characters, "
        "punctuation, or broken spacing when the correction is strongly supported "
        "by the local context. If uncertain, keep the original. Return JSON with "
        "keys original, proposed, confidence, reason.\n\n"
        f"PREVIOUS: {before}\n"
        f"TARGET: {line}\n"
        f"NEXT: {after}\n"
    )


def build_packets(text: str, source_id: str) -> list[dict]:
    lines = text.splitlines()
    packets = []

    for line_no, line in suspicious_lines(text):
        before = lines[line_no - 2] if line_no >= 2 else ""
        after = lines[line_no] if line_no < len(lines) else ""

        packets.append({
            "source_id": source_id,
            "line_no": line_no,
            "original": line,
            "prompt": review_prompt(line, before, after),
            "status": "pending_human_review",
        })

    return packets


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("text_file")
    parser.add_argument("--source-id")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    path = Path(args.text_file)
    text = path.read_text(encoding="utf-8-sig")
    packets = build_packets(text, args.source_id or path.stem)

    with open(args.output, "w", encoding="utf-8") as f:
        for packet in packets:
            f.write(json.dumps(packet, ensure_ascii=False) + "\n")

    print(f"Wrote {len(packets)} review packets to {args.output}")


if __name__ == "__main__":
    main()
