# Evidence and claim register

[Overview](../README.md) | [Hypotheses](../hypotheses/README.md) | [Methods](methods.md) | [Sources](sources.md)

The project contains three different kinds of claims: **published interpretations**, **computational observations about a fixed corpus**, and **proposed new meanings**. A result in one category does not automatically establish a claim in another.

## Claim map

| Claim | Category | Current assessment | Inspect |
|---|---|---|---|
| `DA-DU-MA-TA` means "reassessed allotment" | Project hypothesis H1 | Not preferred; its semantic class is unknown, and HT 86 shares five exact labels under two other headings. | [H1](../hypotheses/adjusted-assessment.md) |
| HT 95's headings independently identify reference versus revision | Premise of H1 | **Not established.** HT 86a partitions five exact shared labels plus a different sixth label. It supplies an alternative, not a direct test of `DA-DU-MA-TA`, which is absent there. | [Headings](#headings-ht-86-and-a-du) |
| Selected `A-X` forms express responsibility | Project hypothesis H2 | Not preferred; responsibility is not distinguished from possession, origin, another grammatical relation, or distinct names. | [H2](../hypotheses/administrative-responsibility.md) |
| The six `A-X / X` pairs outnumber chance | Premise of H2 | Model-dependent: conditional p = 0.154 across the corpus; tablet-only p = 0.00765, Holm = 0.459. Non-rejection does not establish coincidence. | [Affix controls](#affix-pairs-reference-model-sensitivity) |
| `KU-RO` marks totals | Prior scholarly interpretation, used as a positive control | The computational search recovers the known behavior, with unmatched cases retained; with the source's fraction values HT 104 joins the matches. | [Accounting highlights](../results/highlights.json), [fraction highlights](../results/extension_highlights.json) |
| Damage warnings can disappear in transliteration | Corpus audit result | 412 candidate lexical occurrences contain an original-sign loss marker absent from the corresponding transliteration. | [Corpus audit](../archive/reports/phase4.md) |
| JA, TI, or TE has a special word-final distribution | Model-dependent calculation | Results change with spelling controls; they establish no grammatical meaning. | [Ending highlights](../results/phase5_highlights.json) |
| `SU-KI-RI-TE-I-JA` probably indicates Sybrita origin | Published museum interpretation | Prior semantic hypothesis, not this project's new translation. | [Origin source record](../data/phase5_semantic_anchors.json) |
| An independent semantic prediction validates H1 or H2 | Validation claim | **Not achieved.** | [Hypothesis status](../hypotheses/README.md) |

## Accounting: a known positive control

The search applies the same summation test to each eligible multi-sign label. With commodity-labelled addends allowed and HT 127 excluded after reviewing an erased entry, `KU-RO` matches on **six objects out of fourteen eligible positions**. The objects are HT 9, HT 11, HT 88, HT 89, HT 94, and HT 117. Other expressions match on at most one object in these runs.[1]

| Addend rule | Expressions tested | Objects with KU-RO matches | Search-adjusted permutation diagnostic |
|---|---:|---:|---:|
| Multi-sign word label required | 79 | 3 | 0.0108 |
| Commodity signs also permitted | 117 | 7 | 0.0002 |
| Commodity signs permitted; HT 127 excluded | 117 | 6 | 0.0002 |

The last diagnostic is the floor of a 4,999-permutation simulation with a plus-one calculation. It is not the probability that a translation is correct. The analysis was developed with knowledge of `KU-RO` and several examples, so it is **not a blind decipherment or independent holdout**. Unmatched positions, differences between accounting scope and simple adjacency, and possible unit differences remain.[1]

HT 127 illustrates why erasures matter: including an erased 14 gives 292; excluding it gives 278. The existing commentary already notes that the written 292 includes the erased entry. A change in the state of the account is a possible explanation, not a demonstrated order of scribal actions.[1]

## Accounting with the source's fraction values

The integer-only rule keeps every row with a fraction sign out of the search. Reading the source's exact conventional fraction labels (`1/2`, `1/4`, `3/4`, `1/16`, and the others it assigns) as rational numbers admits 152 more rows and repeats the same search with exact arithmetic. Approximate labels, unassigned fraction signs, and weight notation still interrupt a run.[4]

| Search | Eligible rows | Expressions tested | Objects with KU-RO matches | Eligible KU-RO positions | Adjusted diagnostic |
|---|---:|---:|---:|---:|---:|
| Integers only, HT 127 excluded (above) | 599 | 117 | 6 | 14 | 0.0002 |
| With exact fractions, HT 127 excluded | 751 | 148 | 7 | 18 | 0.0002 |
| With exact fractions, literal corpus | 758 | 148 | 8 | 19 | 0.0002 |

The one object gained is HT 104, where `45+1/2`, `20+1/2`, and `29` sum to the written `KU-RO 95` under either published segmentation of its entries. No integer match is lost. For HT 9a, the listed entries total 31 against the written `31+3/4`. For HT 13, the strict machine run retains only a partial block totaling `125+1/2`; adding the damaged `5+1/2` in the published reading gives 131, against the written `130+1/2`. The partial-block shortfall is not the same as the published full-reading discrepancy. These are conditional comparisons of transcribed amounts, not new readings of the objects; the program does not repair them.[4]

HT 85a is a separate case. Its seven entries (12, 12, 6, 24, 5, 3, 4) sum exactly to the written `KU-RO 66`, but the source marks damage beside both the label and the numeral, so the strict rule excludes the row. The fraction analysis lists such exact sums hidden by damage without counting them.[4]

## Headings: HT 86 and A-DU

The heading comparison collects six entry labels from HT 95. Four records contain at least two of those labels: HT 95a, HT 95b, HT 86a, and HT 86b. Individual labels also occur elsewhere. HT 86a shares five exact labels, not all six. Younger's HT 95 commentary already cross-references HT 86. On HT 86a the five shared labels and a different sixth label are split under two headings on one face: `A-KA-RU` over KU-NI-SU (with `GRA+K+L`), SA-RU, DI-DE-RU, and QA-RA2-WA, then a ruled line, then `A-DU` over DA-ME (with `GRA+B`) and MI-NU-TE, at 20 each except one 10.[5]

| Label | HT 95b (`A-DU`) | HT 95a (`DA-DU-MA-TA GRA`) | HT 86a (heading) |
|---|---:|---:|---|
| DA-ME | 10 | 10 | 20 (`A-DU`) |
| MI-NU-TE | 10 | 10 | 20 (`A-DU`) |
| SA-RU | 10 | 20 | 20 (`A-KA-RU`) |
| KU-NI-SU | 10 | 10 | 20 (`A-KA-RU`) |
| DI-DE-RU | 10 | 10 | 20 (`A-KA-RU`) |
| QE-RA2-U | 10 | 7 | absent; `QA-RA2-WA 10` under `A-KA-RU` |

`A-DU` has ten occurrences across three sites: seven in a first parsed row, five in a row classified as a heading by the quantity-free-row heuristic, and seven without a machine flag. These overlapping counts are not interchangeable. Recurrence in heading contexts does not establish a common noun, transaction term, or name. Different grain-related signs establish different notation, not a proven contrast between commodity and accounting state.[5]

## Affix pairs: reference-model sensitivity

The default `affixes` command now uses a length-stratified fixed-margin conditional test. For every length it holds fixed the number of longer types, attested remainders, and types bearing the candidate edge sign. It then tests their association under within-length exchangeability. The former calculation estimates rates from other edge signs and treats those estimates as fixed; it is preserved as fitted-rate sensitivity, not silently replaced.[6]

| Scope | Initial-A pairs | Conditional expected | Conditional p | Conditional Holm | Fitted-rate p | Fitted-rate Holm |
|---|---:|---:|---:|---:|---:|---:|
| All 599 eligible types | 6 | 3.75 | 0.15367 | 1.00000 | 0.12162 | 1.00000 |
| 437 tablet types | 6 | 2.00 | 0.00765 | 0.45881 | 0.00105 | 0.06271 |

Holm adjustment covers 66 initial signs in the all-type scope and 60 in the tablet scope. No edge sign is below 0.05 after correction in either conditional scope. These are model-dependent tests, not probabilities that a meaning is true or that all six pairs are accidental. Neither model independently identifies responsibility, possession, origin, or grammatical status.

The [review](review.md) documents a two-word comparison where the fitted-rate calculation returns p = 0 because its comparison sample has no successes, while the fixed-margin test returns p = 0.5. The conditional model avoids this fitted-zero issue but still does not preserve every linguistic, lexical, site, or scribal dependency. Current values are in [review highlights](../results/review_highlights.json); [extension highlights](../results/extension_highlights.json) retain the original fitted-rate reference run.

## Endings: sensitivity rather than confirmed morphology

In the selected set of 599 machine-unflagged multi-sign types, a reference model preserving conventional vowel-position patterns gives:[2]

| Final sign | Observed types | Expected types | Unadjusted upper-tail p | Holm-adjusted p across 108 signs |
|---|---:|---:|---:|---:|
| JA | 29 | 19.86 | 0.000582 | 0.06285 |
| TI | 30 | 20.95 | 0.001180 | 0.12624 |
| TE | 32 | 27.28 | 0.05584 | 1.00000 |

No sign passes a 0.05 Holm threshold in either of the two vowel-controlled all-corpus analyses. This does not prove there are no suffixes. It shows that these tests do not establish them. The controls assume conventional sound classes rather than independently recovering Linear A phonology.[2]

Removing HT 104 changes the tablet-only unadjusted TI result from 0.0276 to 0.1135 under this model. That matters because the tablet's final TI signs have a published alternative interpretation as separate accounting signs. The JA result is less dependent on that object, but also does not cross the corrected threshold in either tablet subset.[2]

## Candidate patterns are not dictionary entries

Five simple JA pairs survive the selected reviews: `*306-TU / *306-TU-JA`, `A-MA / A-MA-JA`, `A-SE / A-SE-JA`, `KU-PA / KU-PA-JA`, and `PA-SE / PA-SE-JA`. Three corresponding TI pairs are `DA-KU-SE-NE`, `JA-KU`, and `RI-RU-MA`, each with an extended TI form. These are exact string comparisons, not established same-word paradigms.[2]

The museum-linked `SU-KI-RI-TA / SU-KI-RI-TE-I-JA` pair is a different pattern. It replaces `TA` with `TE-I-JA`; it does not simply add JA. The exact replacement search found only that pair among eligible types, not a productive rule. "JA means from" therefore does not follow.[2,3]

## False positives that have been identified

Some apparent ME variants are continuations across object faces; others are commodity notation. SAM Wa1 also includes a Cretan Hieroglyphic seal impression that must not be treated as two independent Linear A words. These exclusions are attached to source readings in the two [editorial review files](../data/README.md). Several underlying observations were already in the scholarship: documenting their effects on a digital analysis is not discovering new ancient readings.[1,2]

## What is original, and what is not?

H1 and H2 assign specific meanings proposed by this project. Their priority and correctness are unestablished. The audit, sensitivity, heading, control, and fraction calculations are project results, but comprehensive first-in-literature priority has not been checked for those either; the HT 86 cross-reference and the arithmetic discrepancies on HT 9, HT 13, HT 94, HT 118, and HT 119 were already in Younger's commentary.

The ritual readings involving a dedicant giving an offering, the probable Sybrita identification, and the interpretations of total/deficit/grand total come from prior scholarship. They are not new translations supplied by this repository. Neither original proposal is a consequence of a statistically significant semantic test.

## References

[1] [Accounting report and source references](../archive/reports/phase4.md); [machine-readable highlights](../results/highlights.json).

[2] [Ending and origin report with methods, complete qualifications, and sources](../archive/reports/phase5.md); [machine-readable highlights](../results/phase5_highlights.json).

[3] [Published origin hypothesis and museum references](../data/phase5_semantic_anchors.json).

[4] [Fraction-aware summation search](methods.md#fraction-aware-summation-search), implementation [scripts/fraction_accounting.py](../scripts/fraction_accounting.py); results in the [extension highlights](../results/extension_highlights.json). Younger's notes on HT 9, HT 13, HT 85, HT 94, HT 100, HT 118, and HT 119 are in the pinned commentary mirror listed in [Sources](sources.md).

[5] [Heading comparison](methods.md#heading-comparison), targets in [heading_comparanda.json](../data/heading_comparanda.json), implementation [scripts/headings.py](../scripts/headings.py).

[6] [Attested-remainder controls](methods.md#attested-remainder-controls), current implementation [conditional_affix_controls.py](../scripts/conditional_affix_controls.py), with the unchanged fitted-rate calculation in [affix_controls.py](../scripts/affix_controls.py).
