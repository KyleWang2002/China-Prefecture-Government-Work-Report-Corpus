# Collection methodology

The collection is semi-automated. That description is intentional: fully automated scraping works well for some cities and badly for others.

## Source hierarchy

The working search order was generally:

1. municipal government portals;
2. municipal people's congress pages and government-information disclosure sections;
3. government gazettes and other official repositories;
4. local yearbooks and gazetteers;
5. local newspapers or other archival copies;
6. secondary copies used only to locate or verify a better source.

The exact route varies by city and year.

The private maintenance workbook retains source links and informal notes. The public repository removes those links.

## Standard HTML collection

When a site exposes a stable archive page, the process is straightforward:

- discover report links;
- visit each report page;
- identify the article body;
- extract text;
- normalize whitespace and encoding;
- save by city and report year;
- run basic quality checks.

See `src/collection/html_archive.py`.

## Historical archive recovery

A missing online report was treated as a search problem, not immediately as a missing observation.

Typical recovery steps:

1. confirm the current official archive boundary;
2. search yearbooks, gazetteers, newspapers, and archived copies;
3. identify whether the recovered item is a full report or an excerpt;
4. record the report year and administrative unit carefully;
5. extract or OCR the document;
6. compare suspicious passages with another source when available;
7. manually inspect the final text.

## PDF and image processing

Historical documents are heterogeneous. The working tools include:

- PyMuPDF for PDF rendering and text extraction;
- CnOCR and PaddleOCR for scanned Chinese text;
- fixed two/three-column splitting in early notebooks;
- a later gutter-based helper for more reusable two-column splitting;
- conservative text cleaning;
- manual correction when automated output is not reliable.

The goal is not to maximize automation. The goal is to produce text that is usable for research without hiding uncertain cases.

## LLM-assisted review

Large language models can be useful as a review aid for suspicious OCR segments, especially when the likely correction is obvious from the surrounding Chinese sentence.

The repository formalizes this idea in `src/review/llm_assisted_review.py`. The utility prepares review packets and requires human acceptance. It does not silently rewrite the corpus.

This module was written while packaging the project. It represents the current review workflow, not a claim that one identical LLM script was used on every document during the original collection.
