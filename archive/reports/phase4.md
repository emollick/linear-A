# Phase 4: inscription-level tests and competing readings

Research date: 14 September 2026. Status: exploratory computational research, not a decipherment or externally reviewed publication.

## Findings in brief

The investigation now has a working, checksum-pinned inscription corpus rather than only a historical word index. The numerical search independently treats each candidate label in the same way and recovers the known association of KU-RO with summation. It does not use the source's English translations. Conversely, candidate ME endings remain highly sensitive to source segmentation: after selected editorial checks, four machine-unflagged base/extended pairs reduce to one tentative comparison. A new administrative comparison prioritized in this pass, DA-KU-SE-NE / DA-KU-SE-NE-TI, raises a testable distinction between grammatical suffixes and repeated commodity signs; the published commentary already records that ambiguity.

These are reproducible results of this investigation, not claims that the underlying ancient examples are newly discovered. A known positive control, rejected false positives, and a prioritized rival-hypothesis test are separate kinds of progress.

## 1. Source scope and integrity

The input is `LinearAInscriptions.js` from the Linear A Explorer, pinned to `mwenge/lineara.xyz` commit `43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a`.[1] Its SHA-256 is `4da8e1f9693d30880ee505e56541fc189add70605bad88436c44a8e11a57764c`. The script checks both that hash and Git blob `ef41c58802a3135f295072ba60fc0df39450a10c` before analysis. It parses the inscriptions array as data; it never evaluates downloaded JavaScript.

The file contains 1,722 Map entries and 1,721 distinct record IDs. KH101 occurs twice with different contents; the loader preserves the second entry and logs both token counts, reproducing the source Map's last-wins behavior. Record KNZg57b has ten original-sign tokens and no transliterated tokens; its alignment failure is explicitly excluded. This is one pinned digital corpus, not a claim to encompass every known inscription or all recent readings. Faces are sometimes separate records. Stripping terminal face letters produces 1,600 provisional object IDs, a heuristic rather than an independently checked object catalogue.

Within a deliberately restricted multi-sign label grammar, there are initially 885 machine-unflagged occurrences of 605 types and 422 flagged occurrences of 383 types; their union contains 933 types. These are not counts of securely complete ancient words. The strict label grammar excludes some mixed or unusual labels and single-sign expressions.

A consequential result: **412 candidate lexical occurrences contain the source loss marker U+1076B in the original-sign field without that marker in the corresponding transliteration.** Therefore a corpus constructed from the transliterated field alone can silently turn fragments into apparent whole words. Original-sign and transliteration fields are aligned and retained together. The `translatedWords` English-gloss field is not used.

Even that is insufficient: underlining, erasure conventions, alternative readings, ligature interpretations, and continuations across object faces are not all represented in the raw tokens. Selected corrections live separately in `data/editorial_reviews.json`, preserving the original data and source blob IDs. The six reviewed token exclusions remove five previously machine-unflagged tokens; one other occurrence was already flagged for damage. The boundary-review queue has 32 candidates, not 32 proven errors, and does not automatically concatenate adjacent rows.

## 2. A positive control: recovering arithmetic behavior without English glosses

The search asks whether the quantity following any candidate label equals the sum of between two and twelve immediately preceding eligible entries. Every label receives the same treatment. This is not a researcher-blind experiment: KU-RO was already known and studied in earlier phases. It is a translation-free computational positive control.

Only tablet records are used. Eligible quantities must be positive integers independently decoded from raw Aegean number characters and must agree with their displayed numeric values.[8] Unknown or fractional quantities, visible loss, and invalid rows interrupt a run; the program does not bridge them. Units and commodity identity are not inferred from equality.

Two additive-row rules are reported because the first is unnecessarily restrictive for commodity accounts. The narrow rule requires a multi-sign candidate word on every addend. The numerical rule also permits intact single-sign commodity labels or other intact sign groups as addends, while retaining the restrictive candidate-label rule for the prospective sum marker. A third analysis excludes the entire HT127 object after reviewing its erasure. This is a retrospective sensitivity analysis, not a preregistered selection process.

| Analysis | Eligible integer rows | Blocks of at least 3 | Potential labels | KU-RO matching objects | Max-statistic permutation diagnostic |
|---|---:|---:|---:|---:|---:|
| Narrow word-labelled addends | 373 | 36 | 79 | 3 | 0.0108 |
| Numerical addends, literal corpus | 606 | 70 | 117 | 7 | 0.0002 |
| Numerical addends, excluding HT127 | 599 | 69 | 117 | 6 | 0.0002 |

The last analysis searches blocks from 56 provisional objects. Its six KU-RO successes are:

| Record | Addends | KU-RO quantity |
|---|---|---:|
| HT9b | 3 + 3 + 8 + 2 + 2 + 2 + 4 | 24 |
| HT11b | 40 + 30 + 50 + 30 + 30 | 180 |
| HT88 | six entries of 1 | 6 |
| HT89 | 23 + 22 + 24 + 13 + 5 | 87 |
| HT94b | five entries of 1 | 5 |
| HT117a | ten entries of 1 | 10 |

These are six matches among **14 eligible KU-RO positions with at least two preceding entries**, not a perfect success rate. Eligible but unmatched positions remain on HT11a, HT94a, HT100, HT102, HT118, HT119, HT122a, and HT122b. These failures can reflect our conservative interrupted-run selection, incomplete accounts, differing units/columns, source problems, or arithmetic discrepancies; the program does not resolve them by altering numbers. The denominator is a selected opportunity set, not all KU-RO occurrences.

For the diagnostic, amounts are shuffled within each eligible block while labels, records, and amount inventories stay fixed. Each of 4,999 permutations is scored by the best-performing label across the entire search. Scores count distinct provisional objects, not faces. With HT127 excluded, the maximum null scores are: 1 in 3,526 permutations; 2 in 1,115; 3 in 296; 4 in 56; and 5 in 6. None reaches six. The plus-one estimate is consequently 1/5000 = 0.0002, the simulation's reporting floor, not proof of zero probability.

Other expressions produce isolated arithmetic coincidences; none matches on more than one object in these runs. This distinguishes a repeated structural association from merely finding some adjacent numbers that add up. But this null does not reproduce every dependence in ancient accounts, the analysis was developed after inspecting data, and numerical equality does not establish commensurate units. **The diagnostic is not the probability that KU-RO means total, nor a claim of a new translation.** Five of the six surviving objects were already in phase 1; only HT11 adds a computationally recovered object relative to that earlier selected set. It is not independent holdout validation.

### Why HT127 is reported separately

The literal file yields `156 + 72 + 24 + 15 + 11 + 14 = 292`, with KU-RO marking both 156 and 292. Younger's commentary explicitly identifies the 14 entry as erased and notes that the 292 includes it.[2] Omitting the erased 14 gives 278. Several other readings are underlined, and the corpus KI+MU labels differ from the commentary's KI+ME. No silent normalization is imposed.

A possible accounting-history explanation is that a total and a later cancellation represent different states of the record. That is an inference, not a demonstrated sequence of scribal acts. Its practical implication is clear: erased entries cannot be treated as ordinary intact data, but deleting every trace of them also loses information relevant to checking an account. This example was already recognized in the published commentary.

## 3. ME: whole words, continuations, and commodity notation must be separated

Four base/extended pairs initially pass the machine damage filter. Checking the published readings changes their evidential status:

| Pair | Editorial result |
|---|---|
| A-RA-TU / A-RA-TU-ME | Retain as a tentative comparison; final ME on HTWc3024 is underlined.[6] |
| JA-SA-SA-RA / JA-SA-SA-RA-ME | The supposedly short IOZa16 form continues with ME on the next face.[3] |
| SA-RA / SA-RA-ME | The IOZa12 extended form is the second portion of JA-SA-SA-RA-ME, split across faces.[4] |
| MA-RU / MA-RU-ME | HT24's extended forms are published as commodity notation MA+RU ME (*561), not established syllabic words.[5] |

Thus four apparent pairs reduce to one candidate under these selected reviews. This is not a frequency claim about every ME occurrence or a disproof of a ME suffix. Nor should it be conflated with the previous phase's four pairs from a different historical index. Here the failures arise from continuations and commodity notation, not just missing signs.

The surviving A-RA-TU / A-RA-TU-ME comparison links ZA7a and HTWc3024. Its final sign is uncertain in the commentary. The roundel's six seal impressions are not a written numeral six, and an animal-sign disagreement between the corpus and commentary means livestock-based semantic arguments should be withheld.[6]

## 4. Initial A: one more comparison, no new grammatical meaning

The corpus search retains six initial-A type pairs under the selected editorial exclusions: KA-RU / A-KA-RU; KI-RO / A-KI-RO; PA-RA-NE / A-PA-RA-NE; SA-RA2 / A-SA-RA2; SI-KI-RA / A-SI-KI-RA; and TA-NA-TE / A-TA-NA-TE. These are exact sign-string relations, not six established morphological paradigms.

SI-KI-RA on HT8a and A-SI-KI-RA on KH20 add a comparison to the earlier five-pair shortlist. KH20's word precedes commodity notation and a break, so a secure attached quantity or intact heading cannot be inferred.[7] Its different site also leaves regional and lexical alternatives open.

The previously prioritized same-object TA-NA-TE / A-TA-NA-TE contrast on ZA10 remains the most controlled A comparison. The same-scribe PA-RA-NE / A-PA-RA-NE relation remains useful, but multiple faces of HT96/HT115 do not make four independent documents. Neither quantity differences nor unnumbered position establish grammatical number or case. The earlier counterexample to a universal A = heading rule remains in force.

## 5. TI: a more specific next discrimination, not three confirmed suffixes

HT103 and HT104 supply the candidate DA-KU-SE-NE / DA-KU-SE-NE-TI comparison. HT104 also contains I-DU-TI and PA-DA-SU-TI. In the conventional joined reading, its three amounts are 45+J, 20+J, and 29, followed by KU-RO 95.[9]

Two models fit the same arrangement:

```
Morphological model             Commodity-sign model
DA-KU-SE-NE-TI  45+J            DA-KU-SE-NE  TI  45+J
I-DU-TI        20+J            I-DU         TI  20+J
PA-DA-SU-TI     29              PA-DA-SU     TI   29
KU-RO          95              KU-RO            95
```

Younger's commentary explicitly gives the commodity-sign alternative for all three expressions.[9] The sum condition yields J = 1/2 under the stated entries and common interpretation of the two J signs, but is identical under the two segmentations. It cannot decide whether TI is a suffix. The first expression has an uncertain KU; the third expression is underlined. I-DU and PA-DA-SU are not independently attested standalone candidates in this particular normalized source, so these are not three independently established base/extended pairs.

The contrast to test is now concrete: does TI follow several demonstrably independent bases across accounts with differing commodity signs and syntactic roles, or does it behave as a repeated category sign within one kind of accounting entry? Standalone TI occurrences are compatible with the latter but do not prove the reading on HT104. A successful model must predict held-out contexts rather than choose a segmentation after seeing the quantities. On present evidence both analyses remain live.

## 6. Reproducibility and limits

Run with Python 3.13.5 (used for the archived results; standard library only):

```sh
python scripts/phase4.py --fetch --permutations 4999 --seed 20260914
python -m unittest discover -s tests -v
```

For an already downloaded source, use `--source PATH` instead of `--fetch`. Four detailed result JSON files retain corpus summaries, all candidate occurrences, selected editorial flags, candidate affix pairs, arithmetic blocks, matches, and tested labels. A source mismatch fails rather than silently updating the dataset.

All 33 local tests pass. GitHub Actions run [34869921158](https://github.com/emollick/linear-A/actions/runs/34869921158) ran at research commit `536361b619bc4ab7c0392c84475e0ef23d10a954` and passed the same tests. The downloaded build manifest confirms byte-for-byte matching SHA-256 values for the three analysis inputs and all four generated result JSON files between local and GitHub executions. This verifies computational reproduction, not the truth of a linguistic hypothesis or the reliability of each ancient reading.

Morphological analysis is established scholarship. Davis's 2026 chapter describes a refinement of Packard's statistical approach.[10] Only its public abstract was consulted here, not the full chapter, and these calculations are not a replication or refutation of it. Full original photographs, all editorial apparatus, complete literature priority, language-family identification, and predictive translations have not been established in this pass. The repository distinguishes known evidence, fresh calculations, competing explanations, and unresolved readings.

## Primary and source references

[1] [Pinned Linear A Explorer corpus](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/LinearAInscriptions.js). The digital transcription is derivative of published editions; it is not an independent epigraphic witness.

[2] [John Younger, HT127 commentary, pinned mirror](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/HT127.html).

[3] [Younger, IOZa16](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/IOZa16.html).

[4] [Younger, IOZa12](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/IOZa12.html).

[5] [Younger, HT24](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/HT24.html).

[6] [Younger, HTWc3024](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/HTWc3024.html).

[7] [Younger, KH20](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/KH20.html).

[8] [Unicode Consortium, Aegean Numbers](https://www.unicode.org/charts/nameslist/n_10100.html).

[9] [Younger, HT104](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/HT104.html).

[10] [Brent Davis, Linear A Morphology, public abstract, Cambridge University Press, online 20 March 2026](https://www.cambridge.org/core/books/abs/undeciphered-aegean-scripts/linear-a-morphology/7E1FCC59D897E6D04129FFEA0B3CA342).
