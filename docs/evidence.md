# Evidence and claim register

[Overview](../README.md) | [Hypotheses](../hypotheses/README.md) | [Methods](methods.md) | [Sources](sources.md)

The project contains three different kinds of claims: **published interpretations**, **computational observations about a fixed corpus**, and **proposed new meanings**. A result in one category does not automatically establish a claim in another.

## Claim map

| Claim | Category | Current assessment | Inspect |
|---|---|---|---|
| `DA-DU-MA-TA` means "reassessed allotment" | Project hypothesis H1 | Low confidence; the heading's semantic class is unknown, and HT 86 carries the same labels under two other headings. | [H1](../hypotheses/adjusted-assessment.md) |
| `DA-DU-MA-TA` and `A-DU` form a reference/revision pair specific to HT 95 | Premise of H1 | **Not supported.** HT 86a partitions the same six labels under `A-KA-RU` and `A-DU` at equal amounts; `A-DU` heads ten records at three sites. | [Headings](#headings-ht-86-and-a-du) |
| Selected `A-X` forms express responsibility | Project hypothesis H2 | Low confidence; responsibility is not distinguished from possession, origin, or distinct names. | [H2](../hypotheses/administrative-responsibility.md) |
| The six `A-X / X` pairs outnumber chance | Premise of H2 | Not across the corpus (6 observed, 3.4 expected, p = 0.12). Suggestive within tablets only (6 vs 1.3, p = 0.0010, Holm 0.063 across 60 initial signs). | [Affix controls](#affix-pairs-what-chance-produces) |
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

The one object gained is HT 104, where `45+1/2`, `20+1/2`, and `29` sum to the written `KU-RO 95` under either published segmentation of its entries. No integer match is lost. Two newly eligible positions fail by the amounts Younger's commentary already records: HT 9a is written `31+3/4` against entries summing to 31, and HT 13 is written `130+1/2` against entries that total 131 once the damaged `5+1/2` is included. Both are discrepancies on the tablets, not in the method, and the program does not repair them.[4]

HT 85a is a separate case. Its seven entries (12, 12, 6, 24, 5, 3, 4) sum exactly to the written `KU-RO 66`, but the source marks damage beside both the label and the numeral, so the strict rule excludes the row. The fraction analysis lists such exact sums hidden by damage without counting them.[4]

## Headings: HT 86 and A-DU

The heading comparison collects the six entry labels of HT 95 and finds them on four records only: HT 95a, HT 95b, HT 86a, and HT 86b. Younger's HT 95 commentary already cross-references HT 86. On HT 86a the labels are split under two headings on one face: `A-KA-RU` over KU-NI-SU (with `GRA+K+L`), SA-RU, DI-DE-RU, and QA-RA2-WA, then a ruled line, then `A-DU` over DA-ME (with `GRA+B`) and MI-NU-TE, at 20 each except one 10.[5]

| Label | HT 95b (`A-DU`) | HT 95a (`DA-DU-MA-TA GRA`) | HT 86a (heading) |
|---|---:|---:|---|
| DA-ME | 10 | 10 | 20 (`A-DU`) |
| MI-NU-TE | 10 | 10 | 20 (`A-DU`) |
| SA-RU | 10 | 20 | 20 (`A-KA-RU`) |
| KU-NI-SU | 10 | 10 | 20 (`A-KA-RU`) |
| DI-DE-RU | 10 | 10 | 20 (`A-KA-RU`) |
| QE-RA2-U | 10 | 7 | absent; `QA-RA2-WA 10` under `A-KA-RU` |

`A-DU` occurs on ten records at Haghia Triada, Khania, and Tylissos, seven times as the first row, before grain, people, oil, and cyperus. It is a general heading term. This is a descriptive comparison of exact labels in the pinned corpus; it assigns no meaning to any heading and does not order the tablets in time.[5]

## Affix pairs: what chance produces

Removing one sign from a word often leaves another attested word by coincidence. The attested-remainder control compares each edge sign with words of the same length carrying any other edge sign, using an exact tail and Holm adjustment across all edge signs in a scope.[6]

| Scope | Edge | Types | Remainder attested | Expected | Exact tail | Holm |
|---|---|---:|---:|---:|---:|---:|
| All types (599) | initial `A` | 66 | 6 | 3.42 | 0.12 | 1.00 |
| All types (599) | initial `I` | 25 | 4 | 1.39 | 0.045 | 1.00 |
| All types (599) | final `JA` | 22 | 5 | 1.82 | 0.028 | 1.00 |
| All types (599) | final `TI` | 23 | 3 | 1.26 | 0.12 | 1.00 |
| Tablet types (437) | initial `A` | 41 | 6 | 1.27 | 0.0010 | 0.063 |
| Tablet types (437) | final `JA` | 16 | 3 | 1.17 | 0.10 | 1.00 |

No edge sign falls below 0.05 after Holm adjustment in any scope. The five JA pairs and six A pairs are real exact-string relations, but their number does not by itself show a recurring element; the tablet-only excess for `A` is the one result worth a further, independently designed test.[6]

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

[6] [Attested-remainder controls](methods.md#attested-remainder-controls), implementation [scripts/affix_controls.py](../scripts/affix_controls.py).
