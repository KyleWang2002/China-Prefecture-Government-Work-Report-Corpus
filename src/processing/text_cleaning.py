"""Conservative text cleaning for Chinese government-work-report OCR."""

from __future__ import annotations

import re
import unicodedata


PAGE_MARKER = re.compile(r"^\s*[—-]?\s*\d{1,4}\s*[—-]?\s*$")
SPACE_BETWEEN_CJK = re.compile(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])")
MANY_SPACES = re.compile(r"[ \t]{2,}")
MANY_BLANKS = re.compile(r"\n{3,}")


def normalize_unicode(text: str) -> str:
    return unicodedata.normalize("NFKC", text).replace("\ufeff", "").replace("\u00a0", " ")


def remove_page_noise(lines: list[str]) -> list[str]:
    cleaned = []
    for line in lines:
        s = line.strip()
        if not s:
            cleaned.append("")
            continue
        if PAGE_MARKER.match(s):
            continue
        cleaned.append(s)
    return cleaned


def repair_spacing(text: str) -> str:
    text = SPACE_BETWEEN_CJK.sub("", text)
    return MANY_SPACES.sub(" ", text)


def normalize_punctuation(text: str) -> str:
    replacements = {
        "﹐": "，", "﹑": "、", "﹒": "。",
        "“ ": "“", " ”": "”", "（ ": "（", " ）": "）",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def clean_text(text: str) -> str:
    text = normalize_unicode(text)
    text = "\n".join(remove_page_noise(text.splitlines()))
    text = repair_spacing(text)
    text = normalize_punctuation(text)
    text = MANY_BLANKS.sub("\n\n", text)
    return text.strip() + "\n"
