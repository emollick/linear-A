# Results and output guide

[Evidence register](../docs/evidence.md) | [Methods](../docs/methods.md) | [Reproduce](../docs/reproduction.md)

## Committed reference highlights

[Accounting and corpus highlights](highlights.json) contain the 4,999-permutation reference results, the selected corpus counts, and their recorded provenance. [Ending and origin highlights](phase5_highlights.json) contain candidate pairs, adjusted and unadjusted statistics, and origin-comparison results. [Extension highlights](extension_highlights.json) contain the HT 95 / HT 86 label matrix and heading census, the attested-remainder controls, and the fraction-aware summation results. Their historical field names and test counts are retained; they refer to their recorded runs, not every later repository state.

For the reviewed conditional affix results and corrected heading counts, use [review_highlights.json](review_highlights.json). `extension_highlights.json` is retained unchanged as the original fitted-rate reference; it is not the current default affix output. [Review notes](../docs/review.md) explain the difference.

These are computational results and candidate lists, **not validated translations**. The [hypothesis pages](../hypotheses/README.md) are the place to evaluate proposed meanings.

## Generated outputs

`python research.py all --fetch` writes the following into `results/generated/`:

| Output | Contents |
|---|---|
| `accounting_summary.json` | Corpus scope, duplicates/exclusions, and all three accounting search summaries |
| `accounting_search.json` | Blocks, candidate matches, tested labels, and permutation details |
| `candidate_forms.json` | Automatically flagged/unflagged occurrences and candidate relations |
| `reviewed_candidate_forms.json` | Candidate relations after the accounting analysis's selected reading review |
| `endings_summary.json` | Reference-model highlights and sample definitions |
| `endings_details.json` | Complete final-sign tests, TI contexts, paired forms, and eligible type lists |
| `origin_comparison.json` | Exact-tail and simple-JA predictions for the published origin hypothesis |
| `heading_comparanda.json` | Anchor entry labels, the documents sharing them, inferred section headings, and the heading-word census |
| `affix_controls.json` | Schema 2: fixed-margin conditional controls, former fitted-rate sensitivity, strata, observed pairs and adjusted tails |
| `fraction_accounting.json` | Fraction-aware blocks, matches, permutation diagnostics, unmatched positions, and exact sums hidden by damage |
| `run_manifest.json` | Command, source checksums, parameters, and hashes of inputs and generated outputs |

For the original implementations the new names are aliases for their unchanged output files; the later implementations write these names directly. The [reproduction guide](../docs/reproduction.md) gives the mapping. A single-topic command writes only its outputs; its manifest lists only those files even when the directory also contains older runs. Use a fresh output directory to keep separate experiments apart.

Generated data and logs are ignored by Git. GitHub workflow artifacts are temporary downloads, not permanent storage. Regeneration from the pinned source is the durable reproduction path; the recorded highlights stay committed.
