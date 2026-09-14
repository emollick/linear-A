# Linear A: reproducible exploratory research

A staged investigation of Linear A sign patterns, accounting contexts, and possible morphology. This is not a decipherment and does not assign unverified translations.

## Start here

Read the [phase 5 report](reports/phase5.md), inspect its [compact results](results/phase5_highlights.json), and review the [new editorial decisions](data/phase5_reviews.json) and [published semantic hypothesis](data/phase5_semantic_anchors.json).

Phase 5 compares candidate endings under three different sign-order and vowel-conditioned reference models. It separates a possible origin/affiliation interpretation from a generic JA-suffix claim, checks TI against independent accounting uses, and removes a mixed-script false positive. The eligible set has 599 multi-sign types, not 599 securely complete words. Neither JA nor TI survives a 0.05 Holm threshold in either vowel-controlled all-corpus analysis; no grammatical meaning is established.

The [phase 4 report](reports/phase4.md), [phase 4 results](results/highlights.json), and [earlier editorial decisions](data/editorial_reviews.json) remain available. Phase 4 processes 1,721 unique digital record IDs, preserves loss markers missing from the transliteration, and recovers KU-RO summation behavior as a known positive control, not a new translation.

## Reproduce

Python 3.13.5 was used for the archived results. All analyses use only the standard library.

```sh
# Acquire and verify the source; zero permutations is acquisition-only here.
python scripts/phase4.py --fetch --permutations 0
python scripts/phase5.py
python scripts/phase5_anchor.py
python -m unittest discover -s tests -v

# To reproduce the archived phase-four permutation analysis separately:
python scripts/phase4.py --permutations 4999 --seed 20260914
```

An existing source file can be supplied with `--source PATH`. Both SHA-256 and Git blob checks reject changed inputs. No downloaded JavaScript is evaluated. The corpus's speculative `translatedWords` field is not used.

All 64 tests passed locally and in [phase 5 GitHub Actions run 34873792613](https://github.com/emollick/linear-A/actions/runs/34873792613), at research commit `9133aabe53c497c9955cf3ac4393261812d31be0`. Nine code/review inputs and all three generated phase-five result files matched byte-for-byte. The artifact contains the complete results, test log, and integrity manifest. Artifacts expire after 30 days; code, pinned acquisition commands, reports, and compact results remain in the repository. The [earlier phase 4 run](https://github.com/emollick/linear-A/actions/runs/34869921158) independently reproduced that phase's 33 tests and four output files.

## Interpretation and provenance

The source is `mwenge/lineara.xyz` at commit `43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a`. It derives from published editions and does not replace original photographs, drawings, or critical apparatus. Source references and hashes appear in the reports, scripts, and review files. The source corpus and copyrighted scholarly commentaries are not relicensed by this repository.

Absence of a machine-readable damage flag is not proof of completeness or certainty. Distinct faces are not independent objects. An exact string extension is not automatically an affix. Numerical equality does not establish common units. Retrospective statistical diagnostics are not probabilities that translations are correct. Vowel-conditioned models assume conventional sound classes without independently validating Linear A phonology. Published interpretations are distinguished from our calculations and from new hypotheses.

Prepared with ChatGPT at Ethan Mollick's request on 14 September 2026. No external researchers have reviewed these results.
