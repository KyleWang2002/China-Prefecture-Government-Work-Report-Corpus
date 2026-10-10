# Code provenance

This repository does not pretend that the original collection was built from one polished package.

The working project accumulated several notebooks and one-off scripts over time. Among the working notebooks:

- one notebook used `requests` + `BeautifulSoup` for government-report pages;
- one used PyMuPDF to render PDFs;
- OCR experiments used both CnOCR and PaddleOCR;
- two- and three-column pages were split before OCR;
- a separate notebook extracted sentences containing energy-security keywords;
- some scripts contained local Windows paths and source-specific URLs.

For the public repository, those routines were reorganized into small modules under `src/`.

Changes made during packaging:
- local absolute paths removed;
- city-specific source URLs removed;
- reusable CLI arguments added;
- layout/OCR code cleaned up;
- quality checks separated from extraction;
- the LLM review packet utility added as a transparent, human-in-the-loop review tool.

This distinction is deliberate. The public code is a reproducible reconstruction of the actual workflow, not a claim that every file in the historical corpus passed through one identical script.
