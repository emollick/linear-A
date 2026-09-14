# Reading guide and sources

[Overview](../README.md) | [Evidence](evidence.md) | [Hypotheses](../hypotheses/README.md)

## Read the notation first

| Notation | Meaning in this repository |
|---|---|
| `HT 95a`, `ZA 10` | Catalogue identifiers, not translations. HT refers to Haghia Triada and ZA to Zakros. A trailing a/b identifies a face or side, not its date. |
| `DA-DU-MA-TA` | Conventional sign labels joined as a sign group. The labels do not guarantee the original pronunciation. |
| `*301`, `*118` | Sign identifiers; the asterisk does not supply a sound or meaning. |
| `PA3`, `RA2` | Distinct numbered sign labels. They are not syllables followed by quantities. Subscripts may be rendered as ordinary digits in code. |
| `GRA`, `OLE`, `FIC` | Conventional logogram labels used for grain, oil, and figs in editions. They are not newly translated syllabic words. |
| `J`, `E`, `K` | Editorial fractional-sign labels in the relevant accounts; context matters because a letter can also occur in other transcription roles. |
| Square brackets, underlining, erasures | Editorial information about missing, doubtful, or cancelled writing. Flattened digital text may lose it. |
| Type / occurrence / object | A distinct spelling / an instance of a spelling / an inferred physical item. These are not interchangeable sample sizes. |

Conventional sign readings, accounting labels, and editorial readings come from the editions behind the source corpus and the cited commentary. The project does not independently establish them. See each case study for object-specific qualifications.

## Fixed computational source

| Field | Pinned value |
|---|---|
| Repository | `mwenge/lineara.xyz` |
| File | `LinearAInscriptions.js` |
| Commit | `43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a` |
| Git blob | `ef41c58802a3135f295072ba60fc0df39450a10c` |
| SHA-256 | `4da8e1f9693d30880ee505e56541fc189add70605bad88436c44a8e11a57764c` |

[Inspect the pinned source](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/LinearAInscriptions.js). The corpus derives from published editions and is not an independent ancient witness. It does not guarantee coverage of all inscriptions or all revised readings. Primary photographs and the full editorial apparatus have not been comprehensively re-examined by this project.

## Sources for the original hypotheses

| Source | Role |
|---|---|
| [Younger: HT 95](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/HT95.html) | H1's headings and quantities. The general assessment interpretation is prior scholarship, cited there to Schoep 2002, p. 106. |
| [Younger: HT 96](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/HT96.html) and [HT 115](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/HT115.html) | H2's Parane comparisons, scribal assignments, and reading cautions. |
| [Younger: ZA 10](https://github.com/mwenge/lineara.xyz/blob/43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a/commentary/ZA10.html) | H2's two Tanate forms on the same tablet. |

The reassessment and responsibility meanings are this project's conjectures, **not translations supplied by those sources**. They have not been validated or shown to be first in the literature.

## Prior semantic and methodological work

The [Heraklion Archaeological Museum's pithos description](https://www.heraklionmuseum.gr/en/exhibit/large-pithos-with-incised-linear-a-inscription/) gives the probable Sybrita-origin interpretation; [the object catalogue](https://ca.heraklionmuseum.gr/ca/pawtucket/index.php/Detail/objects/744) identifies Pi3915. The [machine-readable source record](../data/phase5_semantic_anchors.json) preserves that interpretation as a prior hypothesis, not a new translation.

[Rose Thomas, *Reflections on Morphology in the Language of the Linear A Libation Formula*](https://www.finnishsyntax.co.uk/wp-content/uploads/sites/3/2022/01/Reflections_on_Morphology_in_the_Language_of_the_Linear_A_Libation_Formula.pdf) discusses proposed ritual structure and readings drawing on earlier scholarship. English paraphrases about dedicants giving offerings or seeking favor belong to that literature; they are not original findings of this project.

[Brent Davis, *Linear A Morphology*](https://www.cambridge.org/core/books/abs/undeciphered-aegean-scripts/linear-a-morphology/7E1FCC59D897E6D04129FFEA0B3CA342) is relevant prior morphological research. Only its public abstract was consulted for the archived analyses, not the full chapter. No replication, refutation, or priority comparison with its full results is asserted.

The [Unicode Aegean Numbers chart](https://www.unicode.org/charts/nameslist/n_10100.html) supplies the numeric character reference used in the accounting implementation.

## Attribution and reuse

The repository is AI-assisted research developed with ChatGPT at Ethan Mollick's request. The claims have not received external scholarly review. Citing this repository would document these particular proposals or calculations, not an accepted decipherment.

Cite original editions for inscription readings and a specific repository commit for project calculations. Upstream datasets, museum materials, and scholarly texts retain their respective rights. No blanket relicensing of those sources is intended.
