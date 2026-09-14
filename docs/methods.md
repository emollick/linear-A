# Methods and limitations

[Overview](../README.md) | [Evidence](evidence.md) | [Reproduce](reproduction.md) | [Sources](sources.md)

## Data and scope

The input is a single immutable version of `LinearAInscriptions.js` from Linear A Explorer. SHA-256 and Git-blob checks reject changed inputs. The loader parses the `inscriptions` array as data and never evaluates the downloaded JavaScript. The source's speculative English `translatedWords` field is not used.

The source contains 1,722 map entries and 1,721 unique record IDs. A duplicate KH101 is logged and resolved by retaining the second entry, matching the source's map semantics. KNZg57b has unmatched original/transliterated token arrays and is excluded from aligned analysis. These are properties of this source version, not counts of every known ancient object.[1]

Terminal face letters are stripped to infer shared objects for certain counts. That is a heuristic, not a checked archaeological catalogue. The source includes records for separate faces, fragments, and different supports.

## Reading status and exclusions

Original-sign tokens and transliterations are aligned. Loss markers in the original-sign field are retained even when the transliteration lacks them. The multi-sign eligibility grammar excludes single-sign expressions and several mixed or unusual labels. Consequently, neither "type" nor "machine-unflagged" means "securely complete word."

The baseline automatic filter gives 605 unflagged types. Six selected boundary/commodity exclusions reduce this to 602; the subsequent script/context exclusions leave 599 for the ending analysis. The historical accounting analysis and the ending analysis deliberately retain different review scopes; their results are not silently merged into one sample.[1,2]

The [data guide](../data/README.md) identifies both review files. Reviews name document, token, form, reason, and an upstream source reference. They do not overwrite the raw corpus. Underlining, erasures, alternate readings, ligatures, and continuations are not comprehensively encoded, so selected manual exclusions do not create a complete critical edition.

## Summation-marker search

The accounting analysis uses tablet records and positive integers independently decoded from raw Aegean number characters. The displayed quantity must agree with that raw reading. Damage, fractions, or invalid rows interrupt a run; the program does not add across those gaps.

For each eligible candidate expression, the search asks whether its following quantity equals two to twelve immediately preceding eligible amounts. One version requires multi-sign word labels on addends; another permits intact single-sign or commodity labels. A separate run excludes HT 127 because an erased entry affects its total. Equality alone does not establish commensurate commodities or units.

Amounts are shuffled within eligible blocks. Each permutation is scored using the best-performing expression across the entire search; scores count inferred objects, not faces. The default is 4,999 permutations with seed 20260914. These are retrospective reference-model diagnostics, not probabilities that a translation is true. The search is a known-function positive control, not a blind discovery experiment.[1]

## Word-ending reference models

The ending analysis counts each eligible spelling once. It evaluates three models, with first signs fixed:

| Model | What is preserved | What the comparison asks |
|---|---|---|
| M1: within-word inventory | Each word's length and noninitial sign inventory | Is a sign unusually often final relative to rearrangements within each word? |
| M2: pooled vowel-position control | Length and conventional vowel pattern; signs reassigned within length/vowel strata | Is final preference more than a consequence of that vowel-position pattern? |
| M3: within-word vowel control | Each word's inventory and vowel pattern | Does preference remain under the more constrained within-word comparison? |

M1 and M3 sum conditional Bernoulli distributions exactly. M2 convolves hypergeometric distributions across length/vowel strata. Bare conventional labels are grouped by their final vowel; unassigned and variant signs remain in exact-sign groups. This is conditional on conventional transliteration, **not a decipherment of the sound system**.

Holm adjustments cover all signs in one model and scope, not every exploratory model choice. The all-corpus sample contains 599 types and 108 sign labels. Tablet-only and HT104-excluded subsets test sensitivity; they are not independent replications. Related word types need not be independent observations, and restrictive models can condition away real grammatical effects.[2]

## Origin comparison

A separately stored museum interpretation motivates the `SU-KI-RI-TA / SU-KI-RI-TE-I-JA` comparison. The program checks the exact `TA -> TE-I-JA` replacement and the simpler JA-addition prediction against eligible types. It does not estimate the probability of an English meaning. Absence from the selected type set is not proof that a form never existed.[2]

## Heading comparison

The [comparanda file](../data/heading_comparanda.json) names an anchor (HT 95a/b) and the comparison the published commentary points to (HT 86a/b). The program collects the anchor's entry labels from rows carrying a quantity, searches every aligned record for those exact labels, and records the section each occurrence sits in. A section heading is the most recent parsed row that carries signs but no quantity; rules and damage-only rows leave the heading unchanged. It also lists every occurrence of the named heading words (`DA-DU-MA-TA`, `A-DU`, `A-KA-RU`) with row position, following labels, site, support, and flags.[3]

The output is a label-by-document matrix and a census, not a reading. Inferred sections are a reading aid for tabular accounts; the source's gloss field is not consulted; and the comparison neither identifies the labels as names nor orders the tablets in time.

## Attested-remainder controls

For each edge sign and side (initial or final), the control takes every eligible type of three or more signs carrying that sign, and asks whether the remainder after removing the sign is itself an eligible type. The expected count comes from types of the same length carrying any other edge sign; when no such types exist at a length, the overall rate for other signs is used. The observed count is compared with the exact distribution of a sum of independent Bernoulli trials, and the tails are Holm-adjusted across all edge signs on that side. The type set is the same 599-type all-corpus scope as the ending analysis, with a 437-type tablet scope for sensitivity.[3]

The control tests one premise only: whether a sign's pairs outnumber coincidence. An excess would show that a sign string recurs at the edge of longer words; it would not identify a morpheme, a direction of derivation, or a meaning. Type sets are conditional on the pinned transliteration and on the selected editorial exclusions.

## Fraction-aware summation search

The integer search accepts only rows whose quantity is a whole number of Aegean numerals. The fraction-aware search reads a numeric run of an optional intact integer followed by fraction signs whose source labels have exact rational values (`1/2`, `1/4`, `3/4`, `1/3`, `1/5`, `1/8`, `3/8`, `1/16`, and any other exact ratio the source writes). Labels marked approximate, unassigned fraction signs, weight notation, and damaged numerals still interrupt a run. Addend and candidate rules are those of the numeric integer mode, and the search, permutation null, and max-statistic adjustment are unchanged, computed with exact rational arithmetic.[3]

The analysis also lists candidate-labelled integer rows that the strict rule rejects only because loss markers sit in their raw signs, when the preceding intact entries sum exactly to the written number (HT 85a). These are reported, not scored. Results are conditional on the source's conventional fraction values, so agreement tests those values as much as the label; equality still does not establish commensurate units.

## What is not implemented

There is no general Linear A translator, recovered lexicon, validated language-family identification, or semantic model that selects H1 or H2. The translation hypotheses are argued from particular comparisons in their [case studies](../hypotheses/README.md). Numerical agreement and repeated spellings cannot by themselves decide the meanings of reassessment or responsibility.

Software tests check parser behavior, quantity and fraction decoding, explicit exclusions, probability calculations, heading inference, edge-sign controls, and recorded invariants. They do not certify ancient readings, demonstrate linguistic priority, or constitute peer review.

## Detailed technical records

[1] [Original accounting/corpus report](../archive/reports/phase4.md) and its unchanged implementation, [scripts/phase4.py](../scripts/phase4.py).

[2] [Original endings/origin report](../archive/reports/phase5.md) and implementations [scripts/phase5.py](../scripts/phase5.py) and [scripts/phase5_anchor.py](../scripts/phase5_anchor.py). Historical filenames are retained for compatibility; use the topic-based [reproduction commands](reproduction.md).

[3] Implementations [scripts/headings.py](../scripts/headings.py), [scripts/affix_controls.py](../scripts/affix_controls.py), and [scripts/fraction_accounting.py](../scripts/fraction_accounting.py); reference results in the [extension highlights](../results/extension_highlights.json). The distribution and Holm routines are those of the ending analysis.
