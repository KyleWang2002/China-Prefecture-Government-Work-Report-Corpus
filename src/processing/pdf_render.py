"""Render PDF pages to PNG files with PyMuPDF."""

from __future__ import annotations

import argparse
from pathlib import Path
import fitz


def render_pdf(pdf_path: str | Path, output_dir: str | Path, dpi: int = 220) -> list[Path]:
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    scale = dpi / 72.0
    matrix = fitz.Matrix(scale, scale)
    outputs: list[Path] = []

    with fitz.open(pdf_path) as doc:
        for page_no, page in enumerate(doc, start=1):
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            target = output_dir / f"page_{page_no:03d}.png"
            pix.save(target)
            outputs.append(target)

    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")
    parser.add_argument("output_dir")
    parser.add_argument("--dpi", type=int, default=220)
    args = parser.parse_args()

    outputs = render_pdf(args.pdf, args.output_dir, args.dpi)
    print(f"Rendered {len(outputs)} pages.")


if __name__ == "__main__":
    main()
