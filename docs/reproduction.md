# Reproducing the analyses

[Overview](../README.md) | [Methods](methods.md) | [Outputs](../results/README.md)

## Requirements and first run

Use Python 3.10 or newer and a local checkout of this repository. The archived reference runs used Python 3.13.5. There are no third-party Python package dependencies. Downloading the fixed corpus requires network access; analysis can run offline once the verified file is present.

From the repository root:

```sh
python research.py all --fetch
python -m unittest discover -s tests -v
```

The default input location is `data/LinearAInscriptions.js`. `--fetch` downloads it only when missing; an existing file with the wrong checksum fails rather than being overwritten. The standard run uses 4,999 accounting permutations and seed 20260914.

The runner does **not** translate an arbitrary inscription or validate H1/H2. It runs the corpus/accounting audit, the ending reference models, and the published-origin comparison described in [Methods](methods.md).

## Choose a research question

```sh
# Can the accounting search recover a known summation marker?
python research.py accounting --fetch

# How sensitive are candidate final signs to spelling controls?
python research.py endings --fetch

# Does the published origin comparison support a general ending rule?
python research.py origin --fetch
```

Use `--source PATH` for an existing copy and `--output DIRECTORY` to keep experiments separate. For example:

```sh
python research.py accounting --source data/LinearAInscriptions.js --output results/check --permutations 4999 --seed 20260914
```

A zero-permutation run is useful for a mechanical smoke test, but **does not reproduce the archived permutation evidence**. Use 4,999 for the reference comparison. Permutation and seed options affect accounting only; the ending and origin analyses are deterministic conditional on their inputs.

## Outputs and integrity

The default output directory is `results/generated/`. Its [seven JSON products](../results/README.md) have descriptive names. `run_manifest.json` records the source identity, relevant parameters, Python version, and input/output hashes. Logs retain the underlying scripts' console output. A failed analysis does not replace previously generated results; the runner stages all requested jobs before publishing their outputs.

A single-topic run reports only its own outputs in the manifest. Use a fresh directory to avoid mixing them with earlier files. Run the tests after acquiring the source: some corpus-dependent tests are intentionally skipped when it is absent, so a source-free passing test run is not a complete reproduction.

## Relationship to archived implementations

The mathematical implementations and review files retain their historical filenames. The topic interface calls them without modifying their calculations and renames their output files:

| Topic command | Implementation | Legacy output -> current output |
|---|---|---|
| `accounting` | `scripts/phase4.py` | `phase4_summary.json` -> `accounting_summary.json` |
| | | `phase4_arithmetic.json` -> `accounting_search.json` |
| | | `phase4_morphology.json` -> `candidate_forms.json` |
| | | `phase4_reviewed_morphology.json` -> `reviewed_candidate_forms.json` |
| `endings` | `scripts/phase5.py` | `phase5_summary.json` -> `endings_summary.json` |
| | | `phase5_details.json` -> `endings_details.json` |
| `origin` | `scripts/phase5_anchor.py` | `phase5_anchor_results.json` -> `origin_comparison.json` |

Legacy script commands still work. The [archive](../archive/README.md) retains their detailed run records and historic result hashes. Committed highlights refer to those specific runs, not to every later edit or number of tests.

## Automated checks

The `Reproduce analyses and check documentation` workflow runs the topic interface and test suite. Its artifact contains generated results, logs, and the run manifest. Artifacts have limited retention; the fixed input identity, code, and committed reference highlights provide the durable reproduction path.

Tests cover computation, declared data exclusions, topic-interface behavior, and local documentation links. Passing them is not external review, an epigraphic validation, or proof of any proposed translation.
