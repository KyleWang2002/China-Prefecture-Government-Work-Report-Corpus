# Case study: standard HTML archive collection

Not every city requires archival reconstruction.

Some municipal and provincial portals maintain well-structured government-work-report archive pages. In those cases, the appropriate workflow is intentionally simple:

1. open the archive index;
2. discover report links;
3. visit each report page;
4. extract the article body;
5. normalize text and encoding;
6. infer / verify the report year;
7. save the output using a consistent naming convention.

`src/collection/html_archive.py` implements this generic pattern.

The repository does **not** hard-code the project's city-specific source pages or selectors. Those links remain in the private maintenance inventory because they are the basis for annual updates and because municipal website structures change over time.
