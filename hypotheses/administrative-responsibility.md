# H2: an administrative relationship in selected A-X forms

[All hypotheses](README.md) | [Evidence register](../docs/evidence.md)

**Status: low-confidence translation hypothesis.** The proposed relationship is not independently identified, and the number of `A-X / X` pairs is within what chance produces across the whole corpus. Neither application below is a held-out prediction, and literature priority has not been established.

## Proposed readings

The hypothesis is that, in selected related pairs, a bare expression identifies an entity while initial `A` marks an administrative relationship to it:

```text
PA-RA-NE    -> Parane
A-PA-RA-NE  -> on Parane's account / under Parane's responsibility
```

The proposed rendering of the **HT 96b heading** is:

> **Under Parane's responsibility.**

The application to two **nonadjacent entries on ZA 10a** is:

> **Tanate: two. ... On Tanate's account: one.**

"Parane" and "Tanate" are readable versions of conventional sign labels, not independently established pronunciations or personal identities. "Account" renders the proposed relation; it is not a separately decoded noun. The ellipsis represents intervening entries, not a continuous ancient sentence.

## Evidence from administrative roles

| Form | Context in the published reading | What is observable |
|---|---|---|
| `PA-RA-NE` | HT 115a/b | Appears among accounting entries. |
| `A-PA-RA-NE` | HT 96a/b | Appears in heading material. |
| `TA-NA-TE 2` | ZA 10a | Bare form followed by two. |
| `A-TA-NA-TE 1` | ZA 10a | Extended form followed by one on the same tablet. |

HT 96 and HT 115 are assigned to **HT Scribe 8**. This controls for one source of writing variation; it does not prove the expressions refer to the same entity. Separate faces do not make four independent tablets.[1,2]

HT 115 is a palimpsest. The numeral beside `PA-RA-NE` on its a face is doubtful; the b-face occurrence is followed by fraction sign `J`, with preceding text broken. These qualifications belong to the evidence, not to the proposed meaning.[2]

On HT 96b, the following `QA-*118-RA-RE` and additional notation remain uninterpreted. The commodity list is conventionally read as grain `40+J+E`, `OLE+U 4`, and `FIC 2+K`; `J` is doubtful. No oil grade, grain variety, or physical unit is being translated.[1]

## How many such pairs does chance produce?

Removing a first sign often leaves another attested word by coincidence, because short sign strings recur. The [attested-remainder control](../docs/methods.md#attested-remainder-controls) counts, for every initial sign, how many word types of three or more signs have their remainder attested as a type, and compares that count with words of the same length carrying any other initial sign. The tail probability is exact and is Holm-adjusted across all initial signs in the scope.[5]

| Scope | A-initial types | Remainder attested | Expected | Exact upper tail | Holm-adjusted |
|---|---:|---:|---:|---:|---:|
| All eligible types (599) | 66 | 6 | 3.42 | 0.12 | 1.00 |
| Tablet types (437) | 41 | 6 | 1.27 | 0.0010 | 0.063 |

`A` is the commonest initial sign in the type set, so six pairs is close to what other initial signs yield across the whole corpus; initial `I` gives four pairs against 1.4 expected in the same scope. Within tablets the excess is larger, because all six pairs are tablet words and tablet remainders are attested less often in general, but it does not cross a 0.05 threshold after correction across 60 initial signs. The pairs are a scope-dependent lead, not a demonstrated pattern.

Two of the six pairs also sit awkwardly with the proposed meaning: `KI-RO / A-KI-RO` and `SA-RA2 / A-SA-RA2`, where the shorter member is an accounting term (`KI-RO` is conventionally read as a deficit marker; `SA-RA2` heads eighteen HT records), not an entity name. H2 as stated applies only to selected name pairs, and the control shows that the selection cannot be justified by the pair count alone.

## Why this specific relationship?

A contrast between an entity as an entry and an account assigned to that entity could explain the Parane pair without requiring different regional spellings. The same-tablet Tanate pair allows the relationship to operate within a list rather than solely in headings.[3]

**The new semantic proposal is administrative responsibility, not the existence of these shorter and longer forms.** But the observations do not select responsibility over possession, origin, or another grammatical relation. Nor do they rule out two distinct names. The hypothesis is a candidate explanation, not the most likely meaning established by a formal comparison.

The quantities on ZA 10 do not identify grammatical number: a named entity can be associated with multiple units. Neither what is counted nor a distinction between "two people" and "one person" is established by this pair.[3]

## Boundaries and counterexamples

This is not a rule that removes `A` from every expression beginning with it. The added material might be a prefix, an element written together with a name, or something else. Its grammatical status is unresolved.

A universal `A = heading` rule is not proposed: the documented `KA-RU / A-KA-RU` comparison includes heading uses for both forms, and `A-KA-RU` heads a section of HT 86a beside `A-DU`. The role interpretation must predict more than physical position on a tablet.[4]

ZA 10a also carries `A-KU-MI-NA 1` and `A-DU-KU-MI-NA 1` three rows apart. They differ by an inserted `DU`, and `A-DU` is itself a heading word on ten records. The exact-string pair search cannot see this relation, and no reading of it is proposed here; it is recorded because any account of initial `A` on this tablet has to accommodate it.

## Tests that could change the assessment

A stronger case would require independently related name pairs with a consistent difference in administrative role. Readable evidence that each apparent pair designates two different people or places would weaken the same-entity premise. A separately anchored case or origin function could favor a competitor over responsibility.

The Parane and Tanate examples were both available when H2 was formulated. Their compatibility cannot be reported as independent predictive success. H2 currently supplies **one proposed meaning with two English applications**, not two validated findings.

## Sources and audit trail

[1] [Younger, HT 96](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/HT96.html), blob `eff86bbdf84ab994a2a85602f85abdf2e8a73450`.

[2] [Younger, HT 115](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/HT115.html), including scribal assignment and palimpsest cautions.

[3] [Younger, ZA 10](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/ZA10.html), blob `ae05a6934579931d3341ec1fd926f68298c3c5da`.

[4] [Candidate comparison and limits](../archive/reports/phase4.md), section on initial A; [original semantic proposal](../archive/translation-proposals-2026-09-14.md).

[5] [Attested-remainder controls](../docs/methods.md#attested-remainder-controls), with the counts, exact tails, and pair lists in the [reference highlights](../results/extension_highlights.json); regenerated by the `affixes` command.
