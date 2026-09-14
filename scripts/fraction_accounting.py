#!/usr/bin/env python3
"""Summation-marker search extended to rows with conventional fraction values.

The accounting analysis in phase4.py accepts only whole-number rows, so an
account such as HT 104 (45 J, 20 J, 29, KU-RO 95) never enters the search.
This extension reads the source's own exact fraction labels (1/2, 1/4, 3/4,
1/16, ...) as rational numbers and repeats the same backward exact-sum search
with exact arithmetic. Approximate labels, unassigned fraction signs, weights
such as "double mina", and damaged numerals still interrupt a run. The result
is conditional on the source's conventional fraction values; it tests those
values against the account structure as much as it tests any label. Equality
does not establish commensurate units, and the diagnostic is retrospective.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import json
from pathlib import Path
import random
import re
import sys

import phase4 as p

ROOT = Path(__file__).resolve().parents[1]
SUPERSCRIPT = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789')
SUBSCRIPT = str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')
VULGAR = {'½': Fraction(1, 2), '¼': Fraction(1, 4), '¾': Fraction(3, 4),
          '⅓': Fraction(1, 3), '⅔': Fraction(2, 3), '⅕': Fraction(1, 5),
          '⅙': Fraction(1, 6), '⅛': Fraction(1, 8), '⅜': Fraction(3, 8),
          '⅝': Fraction(5, 8), '⅞': Fraction(7, 8)}
RATIO = re.compile(r'(\d+)/(\d+)')


def fraction_value(label: str) -> Fraction | None:
    """Exact rational for a source fraction label; None for approximate or unassigned."""
    if label in VULGAR:
        return VULGAR[label]
    text = label.translate(SUPERSCRIPT).translate(SUBSCRIPT).replace('⁄', '/')
    match = RATIO.fullmatch(text)
    if match is None:
        return None
    numerator, denominator = int(match[1]), int(match[2])
    if not 0 < numerator < denominator:
        return None
    return Fraction(numerator, denominator)


def is_fraction_sign(raw: str) -> bool:
    return bool(raw) and all(0x10740 <= ord(c) <= 0x1075a for c in raw)


def format_quantity(value: Fraction) -> str:
    whole, part = divmod(value, 1)
    if part == 0:
        return str(int(whole))
    return (str(int(whole)) + '+' if whole else '') + f'{part.numerator}/{part.denominator}'


def read_quantity(tokens: list[dict]) -> tuple[Fraction, bool] | None:
    """Read a numeric run: an optional intact integer, then exact fraction signs."""
    total = Fraction(0)
    fractional = False
    for position, token in enumerate(tokens):
        if is_fraction_sign(token['raw']):
            value = fraction_value(token['label'])
            if value is None:
                return None
            total += value
            fractional = True
        else:
            integer = p.raw_integer(token['raw'])
            if position or integer is None or integer <= 0 or token['label'] != str(integer):
                return None
            total += integer
    if total <= 0:
        return None
    return total, fractional


def eligible_quantity_row(row: list[dict]) -> dict | None:
    """Like phase4's numeric rule, but the quantity may carry exact fractions."""
    tokens = [t for t in row if t['label'] != p.DIVIDER]
    if not tokens or any(p.LOSS in t['raw'] or any(c in t['label'] for c in '[]?')
                         or t['label'] in p.RULES for t in tokens):
        return None
    numeric = [i for i, t in enumerate(tokens) if p.has_quantity(t['raw'], t['label'])]
    if not numeric or numeric != list(range(numeric[0], len(tokens))) or numeric[0] == 0:
        return None
    head, tail = tokens[:numeric[0]], tokens[numeric[0]:]
    quantity = read_quantity(tail)
    if quantity is None:
        return None
    if any(p.word_flags(t['label'], t['raw']) for t in head):
        return None
    words = [t for t in head if p.is_lexical(t['label'])]
    target = words[0] if len(words) == 1 else None
    if target is not None and any(t is not target and len(t['raw']) != 1 for t in head):
        target = None
    return dict(form=target['label'] if target else None, quantity=quantity[0],
                fractional=quantity[1], label_group=' '.join(t['label'] for t in head),
                token_index=(target or head[0])['token_index'],
                context=' '.join(t['label'] for t in row))


def damaged_total(row: list[dict]) -> dict | None:
    """A candidate-labelled integer row rejected only by loss marks in its raw signs.

    Used to list exact sums the strict rule hides; never counted as evidence.
    """
    tokens = [t for t in row if t['label'] != p.DIVIDER]
    if len(tokens) < 2 or not any(p.LOSS in t['raw'] for t in tokens):
        return None
    if any(any(c in t['label'] for c in '[]?') or t['label'] in p.RULES for t in tokens):
        return None
    head, last = tokens[:-1], tokens[-1]
    integer = p.raw_integer(last['raw'].replace(p.LOSS, ''))
    if integer is None or integer <= 0 or last['label'] != str(integer):
        return None
    if any(p.has_quantity(t['raw'], t['label']) for t in head):
        return None
    words = [t for t in head if p.is_lexical(t['label'].replace(p.LOSS, ''))]
    if len(words) != 1 or any(t is not words[0] and len(t['raw'].replace(p.LOSS, '')) != 1
                              for t in head):
        return None
    return dict(form=words[0]['label'], quantity=Fraction(integer),
                context=' '.join(t['label'] for t in row))


def quantity_blocks(docs: dict[str, dict], max_terms: int = 12) -> tuple[list[dict], dict, list[dict]]:
    blocks = []
    hidden = []
    eligible = Counter()
    for doc_id, doc in docs.items():
        if doc['support'].lower() != 'tablet':
            continue
        rows = p.aligned_rows(doc)
        if rows is None:
            continue
        run: list[dict] = []
        for index, row in enumerate(rows + [[]]):
            entry = eligible_quantity_row(row)
            if entry is not None:
                entry['parsed_row'] = index + 1
                run.append(entry)
                eligible['fractional' if entry['fractional'] else 'integer'] += 1
                continue
            damaged = damaged_total(row) if row else None
            if damaged is not None and len(run) >= 2:
                subtotal = Fraction(0)
                for start in range(len(run) - 1, max(-1, len(run) - max_terms - 1), -1):
                    subtotal += run[start]['quantity']
                    if len(run) - start >= 2 and subtotal == damaged['quantity']:
                        hidden.append(dict(document=doc_id, object=p.object_id(doc_id),
                            form=damaged['form'], parsed_row=index + 1, context=damaged['context'],
                            terms=[format_quantity(e['quantity']) for e in run[start:]],
                            total=format_quantity(damaged['quantity'])))
                    if subtotal >= damaged['quantity']:
                        break
            if len(run) >= 3:
                blocks.append(dict(document=doc_id, object=p.object_id(doc_id),
                                   site=doc['site'], scribe=doc['scribe'], entries=run))
            run = []
    summary = dict(eligible_rows=sum(eligible.values()),
                   eligible_integer_rows=eligible['integer'],
                   eligible_fractional_rows=eligible['fractional'],
                   blocks_of_at_least_three=len(blocks),
                   objects_with_blocks=len({b['object'] for b in blocks}))
    return blocks, summary, hidden


def arithmetic(docs: dict[str, dict], permutations: int, seed: int) -> tuple[dict, dict]:
    """Same search and null as phase4.arithmetic, over fraction-aware blocks."""
    blocks, summary, hidden = quantity_blocks(docs)
    observed, matches = p.score_blocks(blocks)
    tested_forms = sorted({e['form'] for b in blocks for e in b['entries'][2:]
                           if e['form'] is not None})
    uncorrected: Counter = Counter()
    max_null_histogram: Counter = Counter()
    rng = random.Random(seed)
    for _ in range(permutations):
        shuffled = [[e['quantity'] for e in b['entries']] for b in blocks]
        for amounts in shuffled:
            rng.shuffle(amounts)
        scores, _ = p.score_blocks(blocks, shuffled)
        max_null_histogram[max(scores.values(), default=0)] += 1
        for form, count in observed.items():
            uncorrected[form] += scores.get(form, 0) >= count
    for match in matches:
        match['terms'] = [format_quantity(x) for x in match['terms']]
        match['total'] = format_quantity(match['total'])
        match['fractional'] = any('/' in x for x in match['terms'] + [match['total']])
    ranking = []
    for form, score in sorted(observed.items(), key=lambda kv: (-kv[1], kv[0])):
        adjusted = sum(n for maximum, n in max_null_histogram.items() if maximum >= score)
        own = [m for m in matches if m['form'] == form]
        ranking.append(dict(form=form, matching_objects=score,
            object_ids=sorted({m['object'] for m in own}),
            objects_with_fractional_matches=sorted({m['object'] for m in own if m['fractional']}),
            match_windows=len(own),
            permutation_p=(1 + uncorrected[form]) / (1 + permutations),
            max_statistic_adjusted_p=(1 + adjusted) / (1 + permutations)))
    for block in blocks:
        for entry in block['entries']:
            entry['quantity'] = format_quantity(entry['quantity'])
    summary.update(dict(seed=seed, permutations=permutations, max_terms=12,
        tested_forms=len(tested_forms), ranking=ranking,
        null_max_score_histogram=dict(sorted(max_null_histogram.items())),
        exact_sums_hidden_by_damage=hidden,
        interpretation=('Same within-block amount permutations as the integer search, with '
                        'exact rational amounts. Results are conditional on the source\'s '
                        'conventional fraction values and do not establish units or meanings.')))
    return summary, dict(blocks=blocks, matches=matches, tested_forms=tested_forms)


def positions(blocks: list[dict], form: str) -> list[dict]:
    """Every eligible position for a form, with the block sum before it."""
    out = []
    for block in blocks:
        entries = block['entries']
        for index, entry in enumerate(entries):
            if index >= 2 and entry['form'] == form:
                before = [parse_fraction_string(x['quantity']) if isinstance(x['quantity'], str)
                          else x['quantity'] for x in entries[:index]]
                out.append(dict(document=block['document'], object=block['object'],
                    parsed_row=entry['parsed_row'], written=entry['quantity'],
                    preceding_entries=index,
                    sum_of_preceding_block_entries=format_quantity(sum(before, Fraction(0))),
                    involves_fractions=entry['fractional'] or any(x['fractional'] for x in entries[:index])))
    return out


def compare(docs: dict[str, dict], summary: dict, details: dict, form: str = 'KU-RO') -> dict:
    """Relate the fraction-aware search to the integer-only numeric search."""
    integer_blocks, _ = p.integer_blocks(docs, 'numeric')
    integer_scores, integer_matches = p.score_blocks(integer_blocks)
    fraction_ranking = next((r for r in summary['ranking'] if r['form'] == form), None)
    fraction_objects = set(fraction_ranking['object_ids']) if fraction_ranking else set()
    integer_objects = {m['object'] for m in integer_matches if m['form'] == form}
    matched_documents = {m['document'] for m in details['matches'] if m['form'] == form}
    unmatched = [pos for pos in positions(details['blocks'], form)
                 if pos['document'] not in matched_documents]
    return dict(form=form,
        integer_only_matching_objects=sorted(integer_objects),
        fraction_aware_matching_objects=sorted(fraction_objects),
        objects_matched_only_with_fractions=sorted(fraction_objects - integer_objects),
        objects_lost_with_fractions=sorted(integer_objects - fraction_objects),
        eligible_positions=len(positions(details['blocks'], form)),
        unmatched_positions=unmatched)


def parse_fraction_string(text: str) -> Fraction:
    """Inverse of format_quantity: '45+1/2' -> 91/2, '3/4' -> 3/4, '29' -> 29."""
    whole, _, part = text.partition('+')
    if not part and '/' in whole:
        return Fraction(whole)
    return Fraction(int(whole)) + (Fraction(part) if part else Fraction(0))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT / 'data/LinearAInscriptions.js')
    parser.add_argument('--output', type=Path, default=ROOT / 'results')
    parser.add_argument('--permutations', type=int, default=4999)
    parser.add_argument('--seed', type=int, default=20260914)
    args = parser.parse_args(argv)
    if args.permutations < 0:
        parser.error('--permutations must be nonnegative')
    data = args.source.read_bytes()
    provenance = p.verify_source(data)
    docs, _ = p.parse_corpus(data.decode('utf-8'))
    results = {}
    for name, subset in (('fractions', docs),
                         ('fractions_excluding_HT127',
                          {k: v for k, v in docs.items() if p.object_id(k) != 'HT127'})):
        summary, details = arithmetic(subset, args.permutations, args.seed)
        summary['comparison_with_integer_search'] = compare(subset, summary, details)
        if name.endswith('HT127'):
            summary['editorial_excluded_objects'] = ['HT127']
        results[name] = dict(summary=summary, details=details)
    output = dict(source=provenance,
                  fraction_values=sorted({k: str(v) for k, v in VULGAR.items()}.items()),
                  analyses={name: r['summary'] for name, r in results.items()},
                  details={name: r['details'] for name, r in results.items()})
    p.write_json(args.output / 'fraction_accounting.json', output)
    print(json.dumps({name: {k: v for k, v in r['summary'].items() if k != 'ranking'}
                      for name, r in results.items()}, ensure_ascii=True, indent=2))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        sys.exit(1)
