"""
Generic HTML archive collector.

No city-specific source URLs are hard-coded here. The author keeps the
per-document source inventory private for maintenance.

Example
-------
python -m src.collection.html_archive \
    --index-url "https://example.gov.cn/reports/" \
    --link-selector "a" \
    --article-selector ".article-content" \
    --output-dir "data/demo"
"""

from __future__ import annotations

import argparse
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124 Safari/537.36"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.5",
}


def fetch_html(url: str, timeout: int = 30) -> str:
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    response.encoding = response.apparent_encoding or "utf-8"
    return response.text


def discover_report_links(
    index_url: str,
    link_selector: str = "a",
    include_pattern: str = r"政府工作报告|工作报告",
) -> list[tuple[str, str]]:
    soup = BeautifulSoup(fetch_html(index_url), "lxml")
    pattern = re.compile(include_pattern)
    found: list[tuple[str, str]] = []
    seen: set[str] = set()

    for tag in soup.select(link_selector):
        href = tag.get("href")
        if not href:
            continue
        label = (tag.get("title") or tag.get_text(" ", strip=True) or "").strip()
        if not pattern.search(label):
            continue
        url = urljoin(index_url, href)
        if url in seen:
            continue
        seen.add(url)
        found.append((label, url))
    return found


def extract_article_text(url: str, article_selector: str) -> str:
    soup = BeautifulSoup(fetch_html(url), "lxml")
    node = soup.select_one(article_selector)
    if node is None:
        raise ValueError(f"article selector did not match: {article_selector!r}")

    for unwanted in node.select("script, style, noscript"):
        unwanted.decompose()

    lines = [x.strip() for x in node.stripped_strings if x.strip()]
    return "\n".join(lines)


def guess_year(label: str, url: str) -> int | None:
    for source in (label, url):
        match = re.search(r"(?<!\d)((?:19|20)\d{2})(?!\d)", source)
        if match:
            return int(match.group(1))
    return None


def safe_name(text: str) -> str:
    text = re.sub(r'[\\/:*?"<>|]+', "_", text)
    return re.sub(r"\s+", "_", text).strip("_")[:120]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index-url", required=True)
    parser.add_argument("--link-selector", default="a")
    parser.add_argument("--article-selector", required=True)
    parser.add_argument("--include-pattern", default=r"政府工作报告|工作报告")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--sleep", type=float, default=0.8)
    args = parser.parse_args()

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    links = discover_report_links(
        args.index_url,
        link_selector=args.link_selector,
        include_pattern=args.include_pattern,
    )

    for i, (label, url) in enumerate(links, start=1):
        year = guess_year(label, url)
        name = safe_name(label)
        if year is not None and str(year) not in name:
            name = f"{name}_{year}"

        print(f"[{i}/{len(links)}] {label}")
        text = extract_article_text(url, args.article_selector)
        (out / f"{name}.txt").write_text(text, encoding="utf-8")
        time.sleep(args.sleep)


if __name__ == "__main__":
    main()
