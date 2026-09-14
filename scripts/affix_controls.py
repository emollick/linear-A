#!/usr/bin/env python3
"""Attested-remainder controls for apparent prefixes and suffixes.

H2 rests on pairs such as PA-RA-NE / A-PA-RA-NE, where removing an initial sign
leaves another attested word. Because short sign strings recur by chance, the
number of such pairs must be compared with what other initial (or final) signs
produce. For each edge sign this control asks: among eligible word types that
begin (or end) with the sign, how many have their remainder attested as a type,
and how many would be expected if that sign's words behaved like words of the
same length carrying any other edge sign? The tail is exact (a sum of
independent Bernoulli trials) and Holm-adjusted across edge signs. Types are
conditional on the pinned transliteration; an excess would suggest a
recurring element, never a meaning.
"""
from __future__ import annotations

import argparse
import json
from math import fsum
from pathlib import Path
import sys

import phase4 as p
import phase5 as q

ROOT = Path(__file__).resolve().parents[1]


def edge_sign(word: list[str], side: str) -> str:
    return word[0] if side == 'prefix' else word[-1]


def remainder(word: list[str], side: str) -> str:
    return '-'.join(word[1:] if side == 'prefix' else word[:-1])


def attested_remainder_control(forms: list[str], side: str, min_length: int = 3) -> dict:
    """Observed and expected attested remainders for every edge sign on one side."""
    if side not in {'prefix', 'suffix'}:
        raise ValueError('side must be prefix or suffix')
    if min_length < 3:
        raise ValueError('A remainder needs at least two signs to be a multi-sign type')
    types = set(forms)
    words = [form.split('-') for form in sorted(types)]
    if any(len(w) < 2 for w in words):
        raise ValueError('Multi-sign forms required')
    long_words = [w for w in words if len(w) >= min_length]
    attested = {tuple(w): remainder(w, side) in types for w in long_words}
    results = []
    for sign in sorted({edge_sign(w, side) for w in long_words}):
        own = [w for w in long_words if edge_sign(w, side) == sign]
        others = [w for w in long_words if edge_sign(w, side) != sign]
        overall = (sum(attested[tuple(v)] for v in others) / len(others)) if others else 0.0
        probabilities = []
        pairs = []
        for w in own:
            pool = [v for v in others if len(v) == len(w)]
            rate = (sum(attested[tuple(v)] for v in pool) / len(pool)) if pool else overall
            probabilities.append(rate)
            if attested[tuple(w)]:
                pairs.append(dict(remainder=remainder(w, side), extended='-'.join(w)))
        observed = len(pairs)
        results.append(dict(sign=sign, side=side, types=len(own), observed_attested=observed,
                            expected_attested=fsum(probabilities),
                            p=q.upper_tail(q.bernoulli_distribution(probabilities), observed),
                            pairs=pairs))
    q.holm(results, 'p')
    results.sort(key=lambda r: (r['p'], -r['observed_attested'], r['sign']))
    base_rate = (sum(attested.values()) / len(attested)) if attested else 0.0
    return dict(side=side, min_length=min_length, types=len(words),
                types_at_least_min_length=len(long_words),
                overall_attested_rate=base_rate, tests=results)


def scopes(morph: dict) -> dict[str, list[str]]:
    occurrences = morph['unflagged_occurrences']
    return {'all': list(occurrences),
            'tablets': [w for w, os in occurrences.items()
                        if any(o['support'] == 'Tablet' for o in os)]}


def run(docs: dict, excluded: set[tuple[str, int]]) -> dict:
    _, morph = p.morphology(docs, excluded)
    results = {}
    for name, forms in scopes(morph).items():
        results[name] = {side: attested_remainder_control(forms, side)
                         for side in ('prefix', 'suffix')}
    selected = {}
    for name, sides in results.items():
        selected[name] = {}
        for side, result in sides.items():
            selected[name][side] = [
                dict(sign=r['sign'], types=r['types'], observed=r['observed_attested'],
                     expected=r['expected_attested'], p=r['p'], holm_p=r['holm_p'])
                for r in result['tests'] if r['sign'] in ('A', 'I', 'JA', 'TI', 'TE', 'ME', 'NA', 'NE')]
    summary = dict(
        scopes={name: {side: dict(types=r['types'], tested_signs=len(r['tests']),
                                  overall_attested_rate=r['overall_attested_rate'],
                                  signs_below_0_05_after_holm=[t['sign'] for t in r['tests']
                                                               if t['holm_p'] < 0.05])
                       for side, r in sides.items()} for name, sides in results.items()},
        selected=selected,
        interpretation=('Exact upper tails compare each edge sign with words of the same '
                        'length carrying other edge signs. A high count shows only that a '
                        'sign string recurs; it does not identify a morpheme, a meaning, or '
                        'which member of a pair is derived from the other.'))
    return summary, results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT / 'data/LinearAInscriptions.js')
    parser.add_argument('--output', type=Path, default=ROOT / 'results')
    args = parser.parse_args(argv)
    data = args.source.read_bytes()
    provenance = p.verify_source(data)
    docs, _ = p.parse_corpus(data.decode('utf-8'))
    excluded = q.load_exclusions(docs, [ROOT / 'data/editorial_reviews.json',
                                        ROOT / 'data/phase5_reviews.json'])
    summary, results = run(docs, excluded)
    p.write_json(args.output / 'affix_controls.json',
                 dict(source=provenance, summary=summary, controls=results))
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        sys.exit(1)
