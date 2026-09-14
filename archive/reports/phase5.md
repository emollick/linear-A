# Phase 5: testing word endings against accounting and spelling alternatives

Research date: 14 September 2026. Status: exploratory research, not a decipherment or externally reviewed linguistic result.

## Main result

The most useful next semantic hypothesis is a relationship between names and expressions of origin or affiliation. This phase prioritizes five candidate X / X-JA pairs and separately checks the published SU-KI-RI-TA / SU-KI-RI-TE-I-JA comparison against a museum interpretation. The two patterns must not be collapsed into a single suffix rule. TI remains ambiguous between grammatical and accounting functions in specific contexts. Its corpus-wide final-position signal weakens when HT104 is removed.

A second result is methodological but directly affects the linguistic argument: a strong apparent TE ending largely disappears after conditioning on conventional vowel classes. JA is less affected by one such control, but neither JA nor TI clears a 0.05 threshold after correction across all tested signs in either vowel-controlled all-corpus analysis. These outcomes support prioritizing further tests, not assigning meanings to endings.

The work is new analysis in this conversation. The inscriptions, the published geographical interpretation, and affix analysis as a research approach are not claimed as new discoveries. No inscription photographs were independently examined in this phase.

## 1. Source, scope, and additional exclusions

This uses the same immutable Linear A Explorer source as phase 4: `mwenge/lineara.xyz` commit `43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a`, file `LinearAInscriptions.js`, SHA-256 `4da8e1f9693d30880ee505e56541fc189add70605bad88436c44a8e11a57764c`.[1] The 1,721 unique record IDs include separate faces. Original signs and transliterations are aligned; the English `translatedWords` field is not used.

Existing phase-four exclusions remain. New source-linked reviews identify two additional problems:

* **SAMWa1 mixes scripts.** Younger identifies the impressed seal inscription as Cretan Hieroglyphic, transcribed `JA-SA <-SA-RA>`, CHIC 137. The corpus's `JA-SA` and `SA-RA` are not two independently preserved Linear A words. Excluding them removes a spurious `JA-SA / JA-SA-JA` comparison.[2]
* **PHWc46 does not supply a secure standalone TI.** The corpus presents `*328-E approx TI`, whereas the commentary lists `*328 E` as logogram notation with no separate TI. Both the word-like `*328-E` and the independent TI use are excluded pending reconciliation.[3]

The resulting eligible set contains **599 distinct multi-sign strings with no current machine flag**, using 108 sign labels. This is not a census of 599 securely complete Minoan words. The tablet subset has 437 types; removing HT104 leaves 433, because its unique header as well as three TI forms disappear. Each spelling contributes once to a type analysis, regardless of repeated occurrences or seal impressions. All surviving source contexts and exclusions are retained in the generated JSON files.

## 2. A semantic lead, with an explicit prediction test

The checked digital readings are:

```
PHWa32:   SU-KI-RI-TA
HTZb158b: SU-KI-RI-TE-I-JA
```

The first is on a nodule; the second on a pithos. Younger's commentary records both forms.[4,5] The Heraklion Archaeological Museum identifies the pithos as catalogue Pi3915 and states that its two inscriptions were incised before firing. The museum interprets SU-KI-RI-TE-I-JA as probably indicating origin at Sybrita/Syvrita.[6,7]

This gives a published candidate meaning for a particular expression in an archaeological context, rather than selecting an English word because it resembles the transliteration. The proposed geographical connection is still not a validated translation. Pre-firing inscription does not distinguish the maker, owner, affiliation, container origin, or intended contents' origin. A personal-name reading has also been proposed in a Hurrian interpretation; that language-family claim has not been tested here.[8]

Most importantly, the observed pair is not:

```
SU-KI-RI-TA + JA
```

It is the surface alternation:

```
SU-KI-RI | TA
SU-KI-RI | TE-I-JA
```

The divisions are analytical, not ancient word separators. The new exact-tail search checks all 599 eligible types. Results:

| Test | Result in this selected type set |
|---|---|
| Simple-JA prediction `SU-KI-RI-TA-JA` | Not found |
| Proposed intermediate `SU-KI-RI-TE` | Not found |
| Other pairs sharing the exact `TA -> TE-I-JA` replacement | None; the SU-KI-RI pair is the sole match |

Absence in this type set does not prove that a form never existed. Nor does one surface replacement establish a productive rule. The result blocks a specific overgeneralization: the museum interpretation cannot be used to translate every final JA as "from". The complex ending and simple JA extension remain separate hypotheses.

## 3. Five simple JA comparisons

After the selected editorial exclusions, the corpus scan returns these exact pairs:

| Base candidate | Extended candidate | Selected base / extended contexts |
|---|---|---|
| `*306-TU` | `*306-TU-JA` | HT119, quantity 2 / HT115b, quantity 1 |
| `A-MA` | `A-MA-JA` | MA1b, before *47 / KH14, before CYP 6 |
| `A-SE` | `A-SE-JA` | HT93a, before grain notation / HT115a, before fractional notation |
| `KU-PA` | `KU-PA-JA` | ZA11a/b, before grain notation / HT116a, before GRA 16 |
| `PA-SE` | `PA-SE-JA` | HT18, before grain notation / HTWc3001 and HTWc3002, roundels |

These are exact sign-string relations from the pinned digital transcription, not five established grammatical paradigms.[1] Complete occurrence contexts, raw signs, support types, sites, and any machine flags are in `phase5_details.json`. This is not a full sign-by-sign re-edition of every example.

A plausible hypothesis is that at least some pairs relate a name or nominal expression to a derived expression of affiliation, origin, or possession. The museum example makes that semantic domain worth testing, but it does not validate the five pairs: its actual ending is different. Lexically distinct names, orthographic variation, and a written-together particle remain alternatives.

The quantities do not determine grammatical number. For example, the longer forms occur with a recorded 1, CYP 6, and GRA 16 in different contexts. This prevents treating every JA form as an entry mechanically associated with a quantity of one. It does not exclude grammatical singularity of a name receiving many units.

## 4. Three competing reference models for final-position preference

A sign may be common at word ends because it marks grammar, but also because of spelling or sound-pattern restrictions. The calculations compare three deliberately different null models. None is claimed as a complete generative model of the unknown language.

**M1: sign inventory within each word.** Hold the first sign fixed and uniformly permute the remaining signs. For word w and candidate sign s, the probability of s at the end is its count among the noninitial signs divided by the number of those positions. Sum these independent conditional Bernoulli variables exactly. This preserves each word's length and sign inventory, but not its vowel pattern.

**M2: length and conventional vowel pattern.** Hold each first sign and all vowel-position labels fixed. Reassign noninitial sign labels across words only within word-length by vowel strata. For a stratum with N eligible positions, K final positions and n copies of a target sign, the final count follows Hypergeometric(N,K,n). Convolve the strata exactly. This retains vowel-position frequencies but not individual word inventories or consonant transitions.

**M3: each word's inventory and vowel pattern.** Hold the first sign fixed and permute only same-vowel signs within the remaining positions of each word. Again sum the final-position Bernoulli variables exactly. This is more restrictive than M2 and can condition away genuine morphological regularities; its low power is not evidence that morphology is absent.

Vowel assignments in M2/M3 are conditional on the conventional Linear-B-derived labels. Only unambiguous bare one- or two-letter labels ending in A/E/I/O/U are grouped. Unknown and variant labels are kept in their own exact-sign groups, without invented sound values. Thus these controls investigate a plausible spelling confound; they do not independently establish Linear A phonology.

The all-corpus calculation tests every one of the 108 observed signs, not only the candidates shown below:

| Sign | Observed final types | M1 expected | M1 upper-tail p | M2 expected | M2 upper-tail p | M2 Holm-adjusted p | M3 upper-tail p |
|---|---:|---:|---:|---:|---:|---:|---:|
| JA | 29 | 21.08 | 0.004836 | 19.86 | 0.000582 | 0.06285 | 0.01227 |
| TI | 30 | 23.28 | 0.02538 | 20.95 | 0.001180 | 0.12624 | 0.16884 |
| TE | 32 | 19.32 | 0.00002566 | 27.28 | 0.05584 | 1.00000 | 0.08681 |

TE has M1 Holm-adjusted p=0.00277, but that apparent strength does not survive either vowel control. JA remains a candidate in the ranking under M2, but its corrected result is 0.06285, not below 0.05. No sign in the all-corpus M2 or M3 analyses has Holm-adjusted p below 0.05. All M3 corrected values for these three signs are 1.

Holm adjustment covers every tested sign within one model and one scope. It does not additionally correct for all model choices or exploratory decisions. The different models are sensitivity analyses, not independent replications. Word types may be genealogically or lexically related, and the digital corpus remains imperfect. These are reference-model tail probabilities, not posterior probabilities that a sign is an affix or that a translation is correct.

## 5. Does HT104 drive the TI result?

The tablet-only sensitivity test repeats the same procedure with and without the entire HT104 object:

| Scope | JA final types | JA M2 p | TI final types | TI M2 p |
|---|---:|---:|---:|---:|
| All eligible tablets, 437 types | 19 | 0.001105 | 20 | 0.02763 |
| Without HT104, 433 types | 19 | 0.001155 | 17 | 0.11351 |

These tabled p-values are unadjusted. Neither scope gives a Holm-adjusted result below 0.05 for either sign. JA's M2 adjusted values are approximately 0.11156 and 0.11666; TI's are both 1. M3 gives TI p=0.75 in both tablet scopes.

Thus TI's particular final-position pattern is partly dependent on the tablet whose segmentation was already disputed. JA is not dependent on that same tablet. This improves the prioritization of examples but is not a blind holdout test: HT104 and the competing interpretations were known before the analysis.

## 6. TI contexts: reject a universal shortcut, preserve the local ambiguity

The complete selected scan returns 49 final-TI occurrences: 33 machine-unflagged and 16 flagged. The 12 standalone TI entries divide into four currently unflagged and eight flagged or editorially excluded after the PHWc46 review. These are occurrences, not independent types or independent objects. Final TI also occurs outside tablet accounts.

Three unflagged base/extended pairs are mechanically identifiable:

```
DA-KU-SE-NE / DA-KU-SE-NE-TI    HT103 / HT104
JA-KU      / JA-KU-TI          MA2b / KN1a
RI-RU-MA   / RI-RU-MA-TI       HT118 / PH(?)31b
```

They are candidates, not established inflectional paradigms. In particular, PH(?)31b has uncertain provenance and its item reading-spec marks signs as `none`, not as affirmatively certain.[9]

Several source contexts are informative:

```
KN1a:       JA-KU-TI     E 240
KN1b:       JA-DU-RA-TI  E 105
PH(?)31b:   RI-RU-MA-TI  *21M
```

These entries are inconsistent with the universal mechanical rule "final TI is always a separate category sign immediately before a numeral." There is other notation after TI. That narrow failure does not prove TI is grammatical and does not refute the context-specific separate-sign reading on HT104.

Standalone TI is independently plausible as accounting notation. Younger places TI 7 in the logogram column of HT119, and TI 13 on both faces of ZA12.[10,11] The two ZA12 faces are one object; the first face's numeral is partly underlined and ends at damage. MA1c supplies an isolated TI without an adjacent amount. The HT119 list totals 159 rather than the written KU-RO 160; the program does not change either figure.

For HT104 specifically, the published alternatives remain:

```
Joined expression               Separate-sign alternative
DA-KU-SE-NE-TI 45+J              DA-KU-SE-NE TI 45+J
I-DU-TI       20+J              I-DU       TI 20+J
PA-DA-SU-TI   29                PA-DA-SU   TI 29
KU-RO        95                KU-RO         95
```

Younger records these alternative segmentations.[12] Arithmetic is identical under both, and I-DU / PA-DA-SU are not independently established standalone types in this source. A model should allow a sign's role to depend on context rather than assigning the same meaning to every occurrence of its glyph.

## 7. What has and has not advanced

The leading semantic test now concerns nominal relationships and origin/affiliation, with simple JA extension and the complex TE-I-JA example deliberately separated. Useful competing predictions are explicit: Does one change recur with more independently anchored place/person names? Does it predict semantic or syntactic roles in texts not used to define it? Does a proposed TI analysis explain both accompanying category signs and isolated accounting uses?

No productive rule or new translation has passed such an independent semantic test in this phase. The museum interpretation is prior published evidence used for hypothesis generation, not a successful held-out prediction. Initial-A comparisons from previous phases are not refuted, but no new meaning for A was tested here. Full sign readings, language-family identification, and complete literature priority remain outside what these calculations establish.

Affix investigation itself is established scholarship. Davis's 2026 chapter describes a refinement of Packard's statistical approach and discusses origin/possession possibilities.[13] Only its public abstract was read here. These calculations cannot be represented as a replication, refutation, or extension of specific unpublished-to-us chapter results.

## 8. Reproduction

Python standard library only. Reuse the verified source acquisition from phase 4:

```sh
python scripts/phase4.py --fetch --permutations 0
python scripts/phase5.py
python scripts/phase5_anchor.py
python -m unittest discover -s tests -v
```

The first command uses zero permutations only to acquire and validate the corpus for this run; it must not be confused with the archived 4,999-permutation phase-four result. For a local source, both phase-five scripts accept `--source PATH` and `--output DIRECTORY`. The outputs are `phase5_summary.json`, `phase5_details.json`, and `phase5_anchor_results.json`.

All 64 local tests pass: 33 retained phase-four tests plus 31 new tests. Exact small enumerations check the probability calculations, and corpus regression tests check damage handling, script-mixing exclusions, type counts, paired-form searches, and the separation of simple and complex ending predictions. Passing tests establish that the implemented calculations and declared invariants reproduce, not that a linguistic hypothesis is true.

GitHub Actions run [34873792613](https://github.com/emollick/linear-A/actions/runs/34873792613), at research commit `9133aabe53c497c9955cf3ac4393261812d31be0`, also passed all 64 tests. Its downloaded build manifest matches the local SHA-256 hashes for all nine code/review input files and all three generated result files byte-for-byte. Both executions used Python 3.13.5. This verifies computational reproduction, not linguistic validity.

## Sources

[1] [Pinned digital source](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/LinearAInscriptions.js). Derivative of published editions, not an independent ancient witness.

[2] [Younger, SAMWa1 commentary](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/SAMWa1.html).

[3] [Younger, PHWc46 commentary](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/PHWc46.html).

[4] [Younger, PHWa32](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/PHWa32.html).

[5] [Younger, HTZb158](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/HTZb158.html).

[6] [Heraklion Archaeological Museum, large pithos with Linear A inscription](https://www.heraklionmuseum.gr/en/exhibit/large-pithos-with-incised-linear-a-inscription/).

[7] [Museum object catalogue, Pi3915](https://ca.heraklionmuseum.gr/ca/pawtucket/index.php/Detail/objects/744). Includes GORILA IV, HT Zb158a/b bibliographic identification.

[8] [Van Soesbergen, author's presentation of an alternative personal-name hypothesis](https://www.minoanscript.nl/). Cited only as an alternative interpretation, not as evidence of an accepted decipherment.

[9] [PH(?)31b item and reading-spec](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/items/PH(%3F)31b.html).

[10] [Younger, HT119](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/HT119.html).

[11] [Younger, ZA12](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/ZA12.html).

[12] [Younger, HT104](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/HT104.html).

[13] [Davis, Linear A Morphology, Cambridge University Press, 2026, public abstract](https://www.cambridge.org/core/books/abs/undeciphered-aegean-scripts/linear-a-morphology/7E1FCC59D897E6D04129FFEA0B3CA342).
