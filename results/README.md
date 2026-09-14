# Results and output guide

[Evidence register](../docs/evidence.md) | [Methods](../docs/methods.md) | [Reproduce](../docs/reproduction.md)

## Committed reference highlights

[Accounting and corpus highlights](highlights.json) contain the 4,999-permutation reference results, the selected corpus counts, and their recorded provenance. [Ending and origin highlights](phase5_highlights.json) contain candidate pairs, adjusted and unadjusted statistics, and origin-comparison results. Their historical field names and test counts are retained; they refer to their recorded runs, not every later repository state.

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
| `run_manifest.json` | Command, source checksums, parameters, and hashes of inputs and generated outputs |

The new names are aliases for the unchanged analytical implementations' output files. The [reproduction guide](../docs/reproduction.md) gives the mapping. A single-topic command writes only its outputs; its manifest lists only those files even when the directory also contains older runs. Use a fresh output directory to keep separate experiments apart.

Generated data and logs are ignored by Git. GitHub workflow artifacts are temporary downloads, not permanent storage. Regeneration from the pinned source is the durable reproduction path; the recorded highlights stay committed.
