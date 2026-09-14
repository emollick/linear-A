# Source data and reading decisions

[Overview](../README.md) | [Methods](../docs/methods.md) | [Source provenance](../docs/sources.md)

The downloaded `LinearAInscriptions.js` is a pinned external input, not a project-authored translation corpus. Obtain it with `python research.py all --fetch` or reuse an already downloaded, checksum-matching copy. It is not committed here.

| File | Purpose | Used by |
|---|---|---|
| [editorial_reviews.json](editorial_reviews.json) | Selected cross-face continuations, commodity notation, and reading cautions | Accounting/corpus review; also inherited by the ending and origin analyses |
| [phase5_reviews.json](phase5_reviews.json) | Additional script-mixing and standalone-TI exclusions | Ending and origin analyses |
| [phase5_semantic_anchors.json](phase5_semantic_anchors.json) | Published museum origin hypothesis, source references, and cautions | Origin comparison only |
| [heading_comparanda.json](heading_comparanda.json) | Anchor and comparison records for the HT 95 / HT 86 heading comparison, the heading words to census, and source references | Heading comparison only |

Historical filenames are retained so the validated implementations and old commands remain compatible. They do not prescribe a reading order.

The first two files are **selected editorial overlays, not a complete critical edition**. Each names its source version and concrete targets. The scripts fail when a review no longer matches the input, rather than applying it to a different token. Cautions need not imply exclusions. The raw data are not silently rewritten.

The origin file is a prior interpretation used to generate a test. It is not a validated bilingual label, an answer key, or evidence that the project discovered that meaning. The comparanda file records which records to compare and why, following a cross-reference in the published commentary; it supplies no readings. The H1/H2 translation hypotheses are documented separately under [hypotheses](../hypotheses/README.md).
