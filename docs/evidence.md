# Evidence and claim register

[Overview](../README.md) | [Hypotheses](../hypotheses/README.md) | [Methods](methods.md) | [Sources](sources.md)

The project contains three different kinds of claims: **published interpretations**, **computational observations about a fixed corpus**, and **proposed new meanings**. A result in one category does not automatically establish a claim in another.

## Claim map

| Claim | Category | Current assessment | Inspect |
|---|---|---|---|
| `DA-DU-MA-TA` means "reassessed allotment" | Project hypothesis H1 | Low confidence; the heading's semantic class is unknown. | [H1](../hypotheses/adjusted-assessment.md) |
| Selected `A-X` forms express responsibility | Project hypothesis H2 | Low confidence; responsibility is not distinguished from possession, origin, or distinct names. | [H2](../hypotheses/administrative-responsibility.md) |
| `KU-RO` marks totals | Prior scholarly interpretation, used as a positive control | The computational search recovers the known behavior, with unmatched cases retained. | [Accounting highlights](../results/highlights.json) |
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

H1 and H2 assign specific meanings proposed by this project. Their priority and correctness are unestablished. The audit and sensitivity calculations are project results, but comprehensive first-in-literature priority has not been checked for those either.

The ritual readings involving a dedicant giving an offering, the probable Sybrita identification, and the interpretations of total/deficit/grand total come from prior scholarship. They are not new translations supplied by this repository. Neither original proposal is a consequence of a statistically significant semantic test.

## References

[1] [Accounting report and source references](../archive/reports/phase4.md); [machine-readable highlights](../results/highlights.json).

[2] [Ending and origin report with methods, complete qualifications, and sources](../archive/reports/phase5.md); [machine-readable highlights](../results/phase5_highlights.json).

[3] [Published origin hypothesis and museum references](../data/phase5_semantic_anchors.json).
