# Case study: two-column yearbook extraction in Linyi

The 2010 Linyi government work report is reproduced in *Linyi Yearbook 2011*.

The report header identifies:

- date: 19 January 2010;
- meeting: third session of the seventeenth Linyi Municipal People's Congress;
- speaker: Mayor Zhang Shaojun (张少军).

The page layout is a conventional two-column yearbook design. The text is visually easy for a human to read, but naive extraction can interleave the left and right columns or insert large amounts of spacing.

The original working notebook used a simple but practical strategy:

1. render the PDF page as an image;
2. split the page into two or three vertical regions;
3. OCR each region separately;
4. concatenate the results in reading order.

The public version in `src/processing/multicolumn_ocr.py` keeps the manual split option and adds a simple gutter detector for two-column pages. Manual overrides remain important because yearbook layouts can change within the same volume.

A short processed excerpt is in `examples/linyi_2010_clean_excerpt.txt`.
