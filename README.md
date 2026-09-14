# Linear A: translation hypotheses and evidence

Can the structure of Linear A accounts help identify the meanings of otherwise unread expressions? This repository investigates that question through proposed translations, source-linked inscription comparisons, and reproducible computational tests.

**The two translation proposals are unvalidated conjectures, not currently preferred readings.** The useful results are inscription comparisons and reproducible tests of their premises. Neither proposed meaning has passed an independent semantic test, and first-in-literature priority has not been established. Published interpretations, calculations, and conjectures are kept separate.

## The translation proposals

| Hypothesis | Proposed reading | Evidence to examine | Status |
|---|---|---|---|
| [H1: adjusted assessment](hypotheses/adjusted-assessment.md) | `DA-DU-MA-TA`: **"reassessed allotment"** | HT 95 records the same six labels on both faces, with a uniform schedule on one and two changed amounts on the other. | Not preferred; one occurrence. HT 86 shares five exact labels and supplies concrete alternatives to reassessment. |
| [H2: administrative responsibility](hypotheses/administrative-responsibility.md) | `A-PA-RA-NE`: **"under Parane's responsibility"** | Compare `PA-RA-NE` in entries with `A-PA-RA-NE` in headings, and `TA-NA-TE / A-TA-NA-TE` within one tablet. | Not preferred; the responsibility meaning is not identified. Pair-count evidence is model- and scope-dependent. |

Each hypothesis page presents the English reading, the exact claim being added, its source evidence, competing explanations, and observations that could support or undermine it. The proposed meanings are not outputs of the statistical tests.

## What the project actually establishes

The computational work is most useful for testing how much evidence survives alternative readings and models. It recovers the **already-known** association of `KU-RO` with totals as a positive control (also with the source's fraction values, which admit HT 104), quantifies missing damage information in one digital corpus, and tests whether apparent word endings remain unusual under different reference models. Two further analyses test the premises of the hypotheses themselves: a heading comparison that follows the published cross-reference from HT 95 to HT 86, and a control for how many prefix or suffix pairs chance produces. It has not established a new grammatical meaning.

The distinction matters: **reproducing a calculation does not validate a translation.** Familiar proposals such as "from Sybrita" and ritual interpretations of giving an offering come from prior scholarship, not discoveries made by this project. See the [evidence and claim register](docs/evidence.md).

## Review outcome

The [review and corrections](docs/review.md) incorporate the HT 86 comparison and fraction-aware search, replace the default fitted-rate affix test with a length-stratified conditional test, and preserve the former calculation as sensitivity analysis. The six initial-A pairs remain; their tablet-only Holm-adjusted value is about **0.459** under the conditional model, versus **0.063** under the fitted-rate model. Neither number validates or disproves a translation.

## Read by question

| What do you want to know? | Start here |
|---|---|
| What are the proposed translations, and why? | [Translation hypotheses](hypotheses/README.md) |
| Which claims are observations, results, or speculation? | [Evidence and claim register](docs/evidence.md) |
| How were the corpus and statistical tests handled? | [Methods and limitations](docs/methods.md) |
| What do inscription codes and sign labels mean? | [Reading guide and sources](docs/sources.md) |
| How do I rerun the analyses or inspect their outputs? | [Reproduction guide](docs/reproduction.md) |
| Where are the detailed original reports? | [Research archive](archive/README.md) |

## Run the analyses

Use Python 3.10 or newer; the archived reference runs used Python 3.13.5. Only the Python standard library is required.

```sh
# Run from the repository root. --fetch downloads the pinned source if missing.
python research.py all --fetch
python -m unittest discover -s tests -v
```

Individual commands are `accounting`, `endings`, `origin`, `headings`, `affixes`, and `fractions`. The source is checksum-verified before analysis; downloaded JavaScript is parsed as data, not executed. Results are written to `results/generated/` with descriptive filenames and a run manifest. The [reproduction guide](docs/reproduction.md) explains options, exclusions, and the relationship to archived results.

## Repository map

```text
hypotheses/   Proposed meanings, evidence, alternatives, and falsification tests
docs/         Evidence register, methods, reading guide, and reproduction
data/         Source-linked reading decisions and a published origin hypothesis
results/      Reference highlights and an output guide
research.py   Topic-based command-line entry point
scripts/      Analytical implementations; the numbered originals are retained unchanged
tests/        Computational regression and repository-navigation checks
archive/      Historical reports; not required to understand the current claims
```

## Provenance and attribution

The input is the [Linear A Explorer corpus](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/LinearAInscriptions.js), fixed to one version. It derives from published editions; it is not an independent reading of the ancient objects or a guarantee of complete corpus coverage. References and reading qualifications accompany individual claims.

This is AI-assisted exploratory research developed at Ethan Mollick's request, first with ChatGPT and later extended with Claude Code. No external scholarly review or first-in-literature claim is asserted. Source datasets and scholarly texts retain their original rights; this repository does not relicense them.
