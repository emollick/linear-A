# Review: what survives the objections?

[Overview](../README.md) | [Evidence register](evidence.md) | [Methods](methods.md)

**Neither proposed English meaning is currently a preferred translation.** The useful material is the inscription comparison and the explicit tests of its premises. This review incorporates Claude Code's [pull request #1](https://github.com/emollick/linear-A/pull/1), with statistical and wording corrections. It is AI-assisted critique, not external scholarly peer review.

## Reassessment: weakened justification, not direct falsification

The original HT 95 proposal omitted HT 86 despite the explicit cross-reference in its source. HT 86a partitions five exact shared labels under A-KA-RU and A-DU, supplying concrete account/category alternatives to a reference-and-revision interpretation. The sixth label differs: QA-RA2-WA versus HT 95's QE-RA2-U. The [revised H1 page](../hypotheses/adjusted-assessment.md) includes the comparison and its reading qualifications.

HT 86 does not contain DA-DU-MA-TA. It therefore does not test another occurrence of the proposed word and cannot be described as directly falsifying its meaning. It removes the reason to prefer the conjecture over plausible alternatives. Different grain-related notation alone does not decide commodity versus accounting state.

## Initial A: keep the pairs, not the responsibility gloss

The same-scribe Parane and same-tablet Tanate comparisons remain worth examining. They do not independently identify a grammatical relationship, still less its English meaning. [H2](../hypotheses/administrative-responsibility.md) now separates three questions: are the strings systematically related, is that relationship grammatical, and does it express responsibility?

## Why the statistical default changed

The original affix control estimates a success probability from other edge signs at the same length, then treats it as fixed in a sum of Bernoulli variables. This computes that fitted model's tail exactly, but omits uncertainty in the estimated probability. A minimal counterexample is:

```text
A-PA-RA    remainder PA-RA is attested
KI-NA-TE   remainder NA-TE is not attested
```

With PA-RA included in the type set, the fitted comparison rate for initial A is zero and its tail probability is zero. Under a fixed-margin conditional model, there is one success among two eligible longer words; assigning it to the A group has probability 1/2.

The new default conditions within every length on the population of longer types, number with attested remainders, and size of the candidate-edge group. It convolves the resulting hypergeometric distributions and uses the same within-side, within-scope Holm correction. The old model remains in the output as `fitted_rate_sensitivity`.

| Initial A | Fitted-rate p | Fitted-rate Holm | Conditional p | Conditional Holm |
|---|---:|---:|---:|---:|
| All eligible types | 0.12162 | 1.00000 | 0.15367 | 1.00000 |
| Tablet types | 0.00105 | 0.06271 | 0.00765 | 0.45881 |

The same six pairs underlie both calculations. The conditional expected counts are 3.75 and 2.00, versus fitted expectations of 3.42 and 1.27. These are different reference models, not independent replications or probabilities that a translation is true. The conditional model still assumes exchangeable types within lengths and does not control all phonotactic, lexical, site, or scribal dependencies. Non-rejection does not prove coincidence.

## Heading counts and fraction evidence

The A-DU census contains ten occurrences, seven first-row occurrences, five rows classified as headings by the quantity-free-row heuristic, and seven machine-unflagged occurrences. These counts overlap and must not be substituted for each other. A recurrent expression in headings could still be a name, institution, place, or category.

The fraction-aware extension is retained. Under the source's assigned fractions, HT 104 satisfies 45.5 + 20.5 + 29 = 95. This broadens the positive control but is not independent validation of those fractional values or a new translation. Damage-qualified sums and partial-block discrepancies remain distinct from fully readable accounts; the earlier integer-only results are preserved.

## Reproduce and inspect

```sh
python research.py all --fetch
python -m unittest discover -s tests -v
```

The [conditional implementation](../scripts/conditional_affix_controls.py) and [tests](../tests/test_conditional_affix_controls.py) include the tiny counterexample, 284 exhaustive small hypergeometric cases, scope/pair checks, and the independent review values. [Current highlights](../results/review_highlights.json) distinguish corrected counts from the unchanged [original PR highlights](../results/extension_highlights.json).

Source readings are linked from the individual hypothesis pages. Original reports and proposals remain in the [archive](../archive/README.md). Tests verify calculations and declared input invariants, not the ancient readings or proposed meanings. The published cross-reference, inscription readings and standard accounting interpretations are not discoveries made by this project.
