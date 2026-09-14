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

For every initial or final sign, count eligible types of at least three signs whose remainder after removing that edge is also attested. The two-sign minimum for the remainder avoids comparing complete multi-sign types to isolated signs. The scopes contain 599 eligible types and a 437-type tablet subset.[3]

**Default: fixed-margin conditional model.** At length L, let N be the number of eligible longer types, K the number with attested remainders, and n the number bearing the candidate edge sign. Under exchangeability within this length, X follows Hypergeometric(N, K, n). Convolve these distributions over lengths and compare the observed total with the resulting upper tail. Holm-adjust across all tested edge signs on the same side and in the same scope. The expected count is the sum of nK/N over lengths.

**Retained sensitivity: fitted-rate model.** Estimate each type's probability from the proportion of same-length types carrying other edge signs with attested remainders; use the former fallback when the group is empty. Treat those estimates as fixed in a Bernoulli sum. This exactly calculates a fitted model's tail, but does not account for uncertainty in the fitted rates. Small comparison groups can yield p = 0 without persuasive evidence; the [review](review.md) gives a reproducible counterexample.

The default [conditional implementation](../scripts/conditional_affix_controls.py) emits schema version 2: `controls` holds the conditional results; `fitted_rate_sensitivity` holds the original model. The original [implementation](../scripts/affix_controls.py) remains available for reproducing the earlier output. `research.py affixes` uses the conditional implementation and records both in its input manifest.

Both analyses assume comparability within length strata; neither preserves all lexical, phonotactic, site or scribal dependencies. Correction is within a side and scope, not across every exploratory choice. A nonsignificant result does not prove chance, and even a robust excess would not identify a morpheme or its meaning.

## Fraction-aware summation search

The integer search accepts only rows whose quantity is a whole number of Aegean numerals. The fraction-aware search reads a numeric run of an optional intact integer followed by fraction signs whose source labels have exact rational values (`1/2`, `1/4`, `3/4`, `1/3`, `1/5`, `1/8`, `3/8`, `1/16`, and any other exact ratio the source writes). Labels marked approximate, unassigned fraction signs, weight notation, and damaged numerals still interrupt a run. Addend and candidate rules are those of the numeric integer mode, and the search, permutation null, and max-statistic adjustment are unchanged, computed with exact rational arithmetic.[3]

The analysis also lists candidate-labelled integer rows that the strict rule rejects only because loss markers sit in their raw signs, when the preceding intact entries sum exactly to the written number (HT 85a). These are reported, not scored. Results are conditional on the source's conventional fraction values, so agreement tests those values as much as the label; equality still does not establish commensurate units.

## What is not implemented

There is no general Linear A translator, recovered lexicon, validated language-family identification, or semantic model that selects H1 or H2. The translation hypotheses are argued from particular comparisons in their [case studies](../hypotheses/README.md). Numerical agreement and repeated spellings cannot by themselves decide the meanings of reassessment or responsibility.

Software tests check parser behavior, quantity and fraction decoding, explicit exclusions, probability calculations, heading inference, edge-sign controls, and recorded invariants. They do not certify ancient readings, demonstrate linguistic priority, or constitute peer review.

## Detailed technical records

[1] [Original accounting/corpus report](../archive/reports/phase4.md) and its unchanged implementation, [scripts/phase4.py](../scripts/phase4.py).

[2] [Original endings/origin report](../archive/reports/phase5.md) and implementations [scripts/phase5.py](../scripts/phase5.py) and [scripts/phase5_anchor.py](../scripts/phase5_anchor.py). Historical filenames are retained for compatibility; use the topic-based [reproduction commands](reproduction.md).

[3] Implementations [headings.py](../scripts/headings.py), [conditional_affix_controls.py](../scripts/conditional_affix_controls.py), and [fraction_accounting.py](../scripts/fraction_accounting.py). The original fitted-rate [affix_controls.py](../scripts/affix_controls.py) is retained as sensitivity. See [reviewed highlights](../results/review_highlights.json) and the unchanged [original extension highlights](../results/extension_highlights.json). The distribution and Holm routines are those of the ending analysis.
