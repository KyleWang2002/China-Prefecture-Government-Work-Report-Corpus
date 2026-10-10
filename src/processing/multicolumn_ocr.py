"""
Multi-column OCR helper for historical Chinese PDFs.

The working notebooks used fixed two/three-column splits with PaddleOCR.
This cleaned version adds an optional gutter detector while keeping manual
split ratios, because historical yearbook layouts are not uniform.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np


def detect_two_column_split(gray: np.ndarray, search=(0.38, 0.62)) -> int:
    """Estimate the central gutter using vertical ink density."""
    if gray.ndim != 2:
        raise ValueError("gray must be a 2D grayscale image")

    _, width = gray.shape
    binary = gray < 210
    density = binary.mean(axis=0)

    lo = max(0, int(width * search[0]))
    hi = min(width, int(width * search[1]))
    window = max(5, int(width * 0.01))

    best_x = width // 2
    best_score = float("inf")

    for x in range(lo, hi):
        left = max(lo, x - window)
        right = min(hi, x + window + 1)
        score = float(density[left:right].mean())
        if score < best_score:
            best_score = score
            best_x = x

    return best_x


def split_columns(
    image: np.ndarray,
    columns: int = 2,
    split_ratios: list[float] | None = None,
    auto_gutter: bool = True,
) -> list[np.ndarray]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    _, width = gray.shape

    if columns == 1:
        return [gray]

    if split_ratios:
        cuts = [int(width * r) for r in split_ratios]
    elif columns == 2 and auto_gutter:
        cuts = [detect_two_column_split(gray)]
    else:
        cuts = [int(width * i / columns) for i in range(1, columns)]

    bounds = [0] + cuts + [width]
    return [gray[:, bounds[i]:bounds[i + 1]] for i in range(len(bounds) - 1)]


def ocr_columns(
    image_path: str | Path,
    columns: int = 2,
    split_ratios: list[float] | None = None,
    lang: str = "ch",
) -> list[str]:
    # Lazy import because OCR dependencies are heavy.
    from paddleocr import PaddleOCR

    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(image_path)

    parts = split_columns(image, columns=columns, split_ratios=split_ratios)
    engine = PaddleOCR(use_angle_cls=False, lang=lang)

    lines: list[str] = []
    for part in parts:
        result = engine.ocr(part)
        if not result or not result[0]:
            continue

        for item in result[0]:
            text = str(item[1][0]).strip()
            if text:
                lines.append(text)

    return lines


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    parser.add_argument("--columns", type=int, default=2, choices=[1, 2, 3])
    parser.add_argument(
        "--split-ratios",
        nargs="*",
        type=float,
        help="Manual cuts as fractions of width, e.g. 0.50 or 0.33 0.67",
    )
    parser.add_argument("--output")
    args = parser.parse_args()

    lines = ocr_columns(args.image, args.columns, args.split_ratios)
    text = "\n".join(lines)

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
