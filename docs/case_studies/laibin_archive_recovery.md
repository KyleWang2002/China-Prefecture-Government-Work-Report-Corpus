# Case study: recovering Laibin reports from yearbooks

## Why this case matters

Laibin is the clearest example of the difference between **current website coverage** and **historical document availability**.

In 2025, a researcher asked the Laibin municipal government for the full 2011-2014 government work reports because they could not be found online. The official reply stated that, because of website-system data migration, the city was temporarily unable to provide electronic copies of reports from 2014 or earlier; reports from 2015 onward were available on the municipal portal.

For this project, that was not the end of the search.

## Recovery

I recovered the **2005-2014** Laibin government work reports from *Laibin Yearbook* volumes.

The 2010 report provides a concrete example. The yearbook identifies it as:

- Government Work Report
- delivered at the seventh session of the second Laibin Municipal People's Congress
- 21 January 2010
- Mayor Yang Herong (杨和荣)

The public repository does not redistribute the full yearbook scan. Short excerpts are available in:

- `examples/laibin_2010_naive_pdf_extraction_excerpt.txt`
- `examples/laibin_2010_clean_excerpt.txt`

## Why ordinary PDF extraction fails

The first yearbook page is not a clean report page. It contains the end of the preceding article on the left, the report title in the lower-left area, and the beginning of the report in the right column.

A plain PDF text extractor therefore has no reliable way to infer the intended reading order. The result contains heavy spacing, mixed columns, and unrelated text.

The recovery workflow was:

1. identify the report's exact page range in the yearbook;
2. render pages at sufficient resolution;
3. split column regions where necessary;
4. OCR columns in reading order;
5. join page-level output;
6. repair spacing, punctuation, headers, and page breaks;
7. manually compare the result with the scan;
8. use contextual / LLM-assisted review only for suspicious OCR segments.

## What this demonstrates

The value of the corpus is not just that a scraper visited many municipal sites. In this case, the municipal authority itself could not supply the old electronic files, while the historical reports remained recoverable from a different archival source.
