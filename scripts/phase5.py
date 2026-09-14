#!/usr/bin/env python3
"""Exploratory TI-context and suffix tests with explicit competing nulls.

No translations or downloaded code are evaluated. This extends phase4's pinned
source and retains its machine-reading caveats. Type-level exchangeability is
an assumption, not a model of Minoan grammar. Vowel groups are CONDITIONAL on
conventional Linear-B-derived transliteration. Statistical tails are not
probabilities that a proposed affix or translation is correct.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import json
from math import comb, fsum
from pathlib import Path
import re
import sys
import phase4 as p

ROOT = Path(__file__).resolve().parents[1]


def convolve(a: list[float], b: list[float]) -> list[float]:
    out = [0.0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i+j] += x*y
    return out


def bernoulli_distribution(probabilities: list[float]) -> list[float]:
    result = [1.0]
    offset = 0
    for prob in probabilities:
        if not 0.0 <= prob <= 1.0:
            raise ValueError('Probability outside [0,1]')
        if prob == 1.0:
            offset += 1
        elif prob != 0.0:
            result = convolve(result, [1-prob, prob])
    return [0.0]*offset + result


def hypergeom_distribution(population: int, successes: int, draws: int) -> list[float]:
    if not 0 <= successes <= population or not 0 <= draws <= population:
        raise ValueError('Invalid hypergeometric parameters')
    denominator = comb(population, draws)
    return [(comb(successes, k)*comb(population-successes, draws-k)/denominator
             if 0 <= draws-k <= population-successes else 0.0)
            for k in range(min(draws, successes)+1)]


def upper_tail(distribution: list[float], observed: int) -> float:
    if observed < 0:
        raise ValueError('Negative observed count')
    return min(1.0, max(0.0, fsum(distribution[observed:])))


def vowel_group(sign: str) -> str:
    # Unknown/variant signs are NOT silently assigned a vowel. In vowel-
    # conditioned nulls their group contains only that exact sign.
    if re.fullmatch(r'[A-Z]{1,2}', sign) and sign[-1] in 'AEIOU':
        return sign[-1]
    return 'unassigned:' + sign


def holm(rows: list[dict], field: str) -> None:
    ordered = sorted(rows, key=lambda x: (x[field], x['sign']))
    running = 0.0
    for rank, row in enumerate(ordered):
        running = max(running, min(1.0, (len(rows)-rank)*row[field]))
        row['holm_' + field] = running


def edge_tests(forms: list[str]) -> dict:
    # A spelling contributes once, not once per seal impression or copied text.
    words = [form.split('-') for form in sorted(set(forms))]
    if any(len(w) < 2 for w in words):
        raise ValueError('Multi-sign forms required')
    signs = sorted({s for w in words for s in w})
    strata = defaultdict(lambda: {'pool': Counter(), 'final': Counter()})
    for w in words:
        for s in w[1:]:
            strata[len(w), vowel_group(s)]['pool'][s] += 1
        strata[len(w), vowel_group(w[-1])]['final'][w[-1]] += 1
    results = []
    for sign in signs:
        observed = sum(w[-1] == sign for w in words)
        # M1: fix each initial sign; permute the remaining signs within its word.
        unrestricted = [w[1:].count(sign)/(len(w)-1) for w in words]
        # M3: additionally preserve EACH word's vowel pattern and sign inventory.
        within_vowel = []
        for w in words:
            if vowel_group(w[-1]) != vowel_group(sign):
                within_vowel.append(0.0)
            else:
                pool = [s for s in w[1:] if vowel_group(s) == vowel_group(sign)]
                within_vowel.append(pool.count(sign)/len(pool))
        # M2: preserve length, initial signs, and every vowel-position label,
        # reallocating signs across words only within length x vowel strata.
        pooled = [1.0]
        pooled_mean = 0.0
        for (length, group), values in sorted(strata.items()):
            if group != vowel_group(sign):
                continue
            N = sum(values['pool'].values())
            K = sum(values['final'].values())
            n = values['pool'][sign]
            pooled = convolve(pooled, hypergeom_distribution(N, K, n))
            pooled_mean += n*K/N
        results.append(dict(sign=sign, observed_final_types=observed,
            m1_expected=fsum(unrestricted), m1_p=upper_tail(bernoulli_distribution(unrestricted), observed),
            m2_expected=pooled_mean, m2_p=upper_tail(pooled, observed),
            m3_expected=fsum(within_vowel), m3_p=upper_tail(bernoulli_distribution(within_vowel), observed)))
    for field in ('m1_p', 'm2_p', 'm3_p'):
        holm(results, field)
    return dict(types=len(words), tested_signs=len(signs), tests=results,
                type_length_counts=dict(sorted(Counter(map(len, words)).items())))


def load_exclusions(docs: dict, paths: list[Path]) -> set[tuple[str, int]]:
    excluded = set()
    for path in paths:
        reviews = json.loads(path.read_text())
        if reviews['upstream_commit'] != p.UPSTREAM_COMMIT:
            raise ValueError('Review source version mismatch')
        for r in reviews['exclude_as_independent_words']:
            actual = p.normalize_label(docs[r['document']]['transliteratedWords'][r['token_index']])
            if actual != r['form']:
                raise ValueError('Review target mismatch: ' + str(r))
            excluded.add((r['document'], r['token_index']))
    return excluded


def ti_contexts(docs: dict, excluded: set[tuple[str, int]]) -> dict:
    occurrences = []
    for key, doc in docs.items():
        for row_index, row in enumerate(p.aligned_rows(doc) or []):
            for i, token in enumerate(row):
                form = token['label']
                if form != 'TI' and not form.endswith('-TI'):
                    continue
                flags = p.word_flags(form, token['raw'])
                if (key, token['token_index']) in excluded:
                    flags.append('editorially_excluded')
                following = row[i+1:]
                numeric = next((j for j,t in enumerate(following)
                                if p.has_quantity(t['raw'],t['label'])), None)
                before_quantity = following if numeric is None else following[:numeric]
                intervening = [t['label'] for t in before_quantity if t['label'] != p.DIVIDER]
                occurrences.append(dict(document=key, object=p.object_id(key),
                    form=form, kind='standalone' if form=='TI' else 'final',
                    site=doc['site'], support=doc['support'], scribe=doc['scribe'],
                    token_index=token['token_index'], parsed_row=row_index+1, flags=flags,
                    context=' '.join(t['label'] for t in row),
                    next_quantity_in_parsed_row=numeric is not None,
                    intervening_labels_before_quantity=intervening))
    counts = Counter((o['kind'], bool(o['flags'])) for o in occurrences)
    return dict(counts={f'{k}:{"flagged" if f else "unflagged"}':v
                        for (k,f),v in sorted(counts.items())}, occurrences=occurrences)


def run(docs: dict, excluded: set[tuple[str, int]]) -> tuple[dict, dict]:
    summary, morph = p.morphology(docs, excluded)
    occurrences = morph['unflagged_occurrences']
    sets = {
        'all': list(occurrences),
        'tablets': [w for w, os in occurrences.items() if any(o['support']=='Tablet' for o in os)],
        'tablets_without_HT104': [w for w, os in occurrences.items()
            if any(o['support']=='Tablet' and o['object']!='HT104' for o in os)],
    }
    tests = {name: edge_tests(forms) for name, forms in sets.items()}
    suffix_pairs = [x for x in morph['affix_candidates']
                    if x['side']=='suffix' and x['edge'] in ('JA','TI','TE','ME')]
    pairs_counts = Counter(x['edge'] for x in suffix_pairs)
    details = dict(edge_tests=tests, ti=ti_contexts(docs, excluded),
                   suffix_pairs=suffix_pairs,
                   scope_forms={name: sorted(forms) for name,forms in sets.items()})
    short = dict(corpus_records=len(docs), morphology=summary,
        suffix_pair_counts=dict(sorted(pairs_counts.items())), ti_counts=details['ti']['counts'],
        contrasts={name:dict(types=result['types'],tested_signs=result['tested_signs'],
                    selected=[r for r in result['tests'] if r['sign'] in ('JA','TI','TE','ME','NA','NE')])
                   for name,result in tests.items()},
        limitations=['Exploratory and retrospective; not a held-out or preregistered discovery.',
          'Vowel-conditioned models assume conventional sound classes, not a deciphered phonology.',
          'Word types and consonant distributions are not independent random observations.',
          'Each Holm correction covers all tested signs in one model/scope, not all model choices.',
          'Source segmentation and partial apparatus remain potential errors.',
          'A preferred word ending does not establish a morpheme or its meaning.'])
    return short, details


def main(argv: list[str] | None=None) -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,default=ROOT/'data/LinearAInscriptions.js')
    ap.add_argument('--output',type=Path,default=ROOT/'results')
    a=ap.parse_args(argv)
    data=a.source.read_bytes(); provenance=p.verify_source(data)
    docs, duplicates=p.parse_corpus(data.decode('utf-8'))
    exclusions=load_exclusions(docs,[ROOT/'data/editorial_reviews.json',ROOT/'data/phase5_reviews.json'])
    summary,details=run(docs,exclusions)
    summary['source']=provenance;summary['duplicate_policy']=duplicates
    p.write_json(a.output/'phase5_summary.json',summary)
    p.write_json(a.output/'phase5_details.json',details)
    print(json.dumps(summary,indent=2))
    return 0


if __name__=='__main__':
    try:
        sys.exit(main())
    except (ValueError,OSError) as exc:
        print('ERROR: '+str(exc),file=sys.stderr);sys.exit(1)
