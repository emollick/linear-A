# Linear A: reproducible exploratory research

A staged investigation of Linear A sign patterns, accounting contexts, and possible morphology. This is not a decipherment and does not assign unverified translations.

## Start here

Read the [phase 4 report](reports/phase4.md), inspect the [compact results](results/highlights.json), and review the [source-linked editorial decisions](data/editorial_reviews.json).

Phase 4 processes a checksum-pinned digital corpus with 1,721 distinct record IDs, preserves loss markers that disappear from the transliteration, searches affix candidates, and tests repeated arithmetic associations without using English glosses. KU-RO is a positive control, not a newly discovered translation. Apparent ME pairs are checked against face continuations and commodity notation. Alternative readings of TI on HT104 remain unresolved.

## Reproduce

Python 3.13.5 was used for the archived results. The analysis uses only the standard library.

```sh
python scripts/phase4.py --fetch --permutations 4999 --seed 20260914
python -m unittest discover -s tests -v
```

An existing source file can be supplied with `--source PATH`. Both SHA-256 and Git blob checks reject changed inputs. No downloaded JavaScript is evaluated. The corpus's speculative `translatedWords` field is not used.

All 33 tests passed locally and in [GitHub Actions run 34869921158](https://github.com/emollick/linear-A/actions/runs/34869921158). The three analysis inputs and four generated JSON outputs matched byte-for-byte. The workflow artifact contains complete occurrence tables, arithmetic blocks, matches, selected editorial exclusions, and the build manifest. Artifacts expire after 30 days; the code and pinned acquisition command remain reproducible. The report and compact results are committed permanently.

## Interpretation and provenance

The source is `mwenge/lineara.xyz` at commit `43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a`. It derives from published editions and does not replace original photographs, drawings, or critical apparatus. Source references and hashes appear in the report, script, and editorial-review file. The source corpus and copyrighted scholarly commentaries are not relicensed by this repository.

Absence of a machine-readable damage flag is not proof of completeness or certainty. Distinct faces are not independent objects. An exact string extension is not automatically an affix. Numerical equality does not establish common units. Retrospective permutation diagnostics are not probabilities that translations are correct.

Prepared with ChatGPT at Ethan Mollick's request on 14 September 2026. No external researchers have reviewed these results.
