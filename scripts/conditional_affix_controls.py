#!/usr/bin/env python3
"""Fixed-margin reference tests for affix pairs, with fitted-rate sensitivity.

Within each word-length stratum, condition on the number of longer types,
attested remainders, and types bearing the candidate edge sign. Under assumed
exchangeability the count is hypergeometric. This avoids fixing a rate estimated
from a tiny comparison group at zero. It does not model all linguistic
relationships or establish a morpheme, a direction of derivation, or a meaning.
The original fitted-rate calculation is retained separately, not overwritten.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from math import fsum
from pathlib import Path
import sys

import affix_controls as fitted
import phase4 as p
import phase5 as q

ROOT = Path(__file__).resolve().parents[1]


def conditional_control(forms: list[str], side: str, min_length: int = 3) -> dict:
    """Convolve length-stratified hypergeometrics and adjust across edge signs."""
    if side not in {'prefix', 'suffix'} or min_length < 3:
        raise ValueError('Use prefix/suffix and a minimum length of at least three')
    types = set(forms)
    words = [form.split('-') for form in sorted(types)]
    if any(len(word) < 2 for word in words):
        raise ValueError('Multi-sign forms required')
    strata = defaultdict(list)
    for word in words:
        if len(word) >= min_length:
            strata[len(word)].append(word)
    signs = sorted({fitted.edge_sign(w, side) for ws in strata.values() for w in ws})
    results = []
    for sign in signs:
        distribution = [1.0]
        expectations, details, pairs = [], [], []
        own_count = 0
        for length, ws in sorted(strata.items()):
            own = [w for w in ws if fitted.edge_sign(w, side) == sign]
            if not own:
                continue
            hits = [w for w in ws if fitted.remainder(w, side) in types]
            own_hits = [w for w in own if fitted.remainder(w, side) in types]
            N, K, n = len(ws), len(hits), len(own)
            distribution = q.convolve(distribution, q.hypergeom_distribution(N, K, n))
            expectations.append(n * K / N)
            own_count += n
            details.append(dict(length=length, population=N, attested_remainders=K,
                                candidate_types=n, candidate_matches=len(own_hits)))
            pairs.extend(dict(remainder=fitted.remainder(w, side), extended='-'.join(w))
                         for w in own_hits)
        results.append(dict(sign=sign, side=side, types=own_count,
                            observed_attested=len(pairs), expected_attested=fsum(expectations),
                            p=q.upper_tail(distribution, len(pairs)), pairs=pairs, strata=details))
    q.holm(results, 'p')
    results.sort(key=lambda r: (r['p'], -r['observed_attested'], r['sign']))
    return dict(model='length_stratified_fixed_margins', side=side, min_length=min_length,
                types=len(words), tested_signs=len(signs), tests=results)


def run(docs: dict, excluded: set[tuple[str, int]]) -> dict:
    _, morph = p.morphology(docs, excluded)
    controls = {}
    sensitivity = {}
    selected = {}
    for scope, forms in fitted.scopes(morph).items():
        controls[scope], sensitivity[scope], selected[scope] = {}, {}, {}
        for side in ('prefix', 'suffix'):
            current = conditional_control(forms, side)
            previous = fitted.attested_remainder_control(forms, side)
            controls[scope][side] = current
            sensitivity[scope][side] = previous
            old = {r['sign']: r for r in previous['tests']}
            selected[scope][side] = [dict(
                sign=r['sign'], types=r['types'], observed=r['observed_attested'],
                expected_conditional=r['expected_attested'], p_conditional=r['p'],
                holm_conditional=r['holm_p'], expected_fitted=old[r['sign']]['expected_attested'],
                p_fitted=old[r['sign']]['p'], holm_fitted=old[r['sign']]['holm_p'])
                for r in current['tests'] if r['sign'] in ('A', 'I', 'JA', 'TI', 'TE', 'ME')]
    toy = ['A-PA-RA', 'PA-RA', 'KI-NA-TE']
    toy_cond = next(r for r in conditional_control(toy, 'prefix')['tests'] if r['sign'] == 'A')
    toy_fit = next(r for r in fitted.attested_remainder_control(toy, 'prefix')['tests'] if r['sign'] == 'A')
    summary = dict(model='length_stratified_fixed_margins', selected=selected,
        scopes={scope: {side: dict(types=result['types'], tested_signs=result['tested_signs'],
                    signs_below_0_05_after_holm=[r['sign'] for r in result['tests'] if r['holm_p'] < .05])
                       for side, result in sides.items()} for scope, sides in controls.items()},
        tiny_sample=dict(forms=toy, sign='A', fitted_p=toy_fit['p'], conditional_p=toy_cond['p']),
        limitations=[
            'Exact conditional on fixed margins and within-length exchangeability; not a generative language model.',
            'Lexical, spelling, site and scribal dependencies are not fully controlled.',
            'Holm correction is within each side and scope, not across all analytical choices.',
            'A nonsignificant result does not prove coincidence; an excess does not assign a meaning.',
            'The fitted-rate model is retained as sensitivity only; its probabilities are estimated then treated as fixed.'])
    return dict(schema_version=2, summary=summary, controls=controls,
                fitted_rate_sensitivity=sensitivity)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT/'data/LinearAInscriptions.js')
    parser.add_argument('--output', type=Path, default=ROOT/'results')
    args = parser.parse_args(argv)
    body = args.source.read_bytes()
    source = p.verify_source(body)
    docs, _ = p.parse_corpus(body.decode('utf-8'))
    excluded = q.load_exclusions(docs, [ROOT/'data/editorial_reviews.json', ROOT/'data/phase5_reviews.json'])
    result = run(docs, excluded)
    result['source'] = source
    p.write_json(args.output/'affix_controls.json', result)
    print('Wrote fixed-margin affix tests and separately labelled fitted-rate sensitivity.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
