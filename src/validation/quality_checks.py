"""Simple quality-control checks used to flag documents for review."""

from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher


@dataclass
class QCResult:
    character_count: int
    cjk_ratio: float
    has_report_phrase: bool
    suspicious_replacement_chars: int
    flags: list[str]


def cjk_ratio(text: str) -> float:
    chars = [c for c in text if not c.isspace()]
    if not chars:
        return 0.0
    cjk = sum("\u4e00" <= c <= "\u9fff" for c in chars)
    return cjk / len(chars)


def inspect_text(text: str, short_threshold: int = 8000) -> QCResult:
    n = len(text)
    ratio = cjk_ratio(text)
    replacement = text.count("�")
    has_phrase = "政府工作报告" in text or "代表市人民政府" in text

    flags = []
    if n < short_threshold:
        flags.append("short_text")
    if ratio < 0.45:
        flags.append("low_cjk_ratio")
    if replacement:
        flags.append("replacement_characters")
    if not has_phrase:
        flags.append("report_identity_uncertain")
    if re.search(r"[\u4e00-\u9fff]\s[\u4e00-\u9fff]\s[\u4e00-\u9fff]\s[\u4e00-\u9fff]", text):
        flags.append("possible_spaced_ocr")

    return QCResult(n, ratio, has_phrase, replacement, flags)


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()
