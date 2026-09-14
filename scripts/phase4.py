#!/usr/bin/env python3
"""Damage-aware Linear A corpus audit and exploratory arithmetic-marker test.

The source is pinned and hashed. JavaScript is parsed as data, never evaluated.
No translatedWords field is used. Machine-unflagged does not mean epigraphically
certain: editorial segmentation and ligature errors are reviewed separately.
All statistics are retrospective diagnostics, not decipherment probabilities.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import random
import re
import sys
from typing import Any
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_COMMIT = '43fe7cf1abc8e6bb1ea3228c3a1bd5938709620a'
SOURCE_URL = ('https://raw.githubusercontent.com/mwenge/lineara.xyz/'
              + UPSTREAM_COMMIT + '/LinearAInscriptions.js')
SOURCE_SHA256 = '4da8e1f9693d30880ee505e56541fc189add70605bad88436c44a8e11a57764c'
SOURCE_GIT_BLOB = 'ef41c58802a3135f295072ba60fc0df39450a10c'
LOSS = '\U0001076b'
DIVIDER = '\U00010101'
RULES = {'\u2014', '\u2013'}
SUBSCRIPTS = str.maketrans({'\u2082': '2', '\u2083': '3', '\u2084': '4'})
SIGN = re.compile(r'(?:[A-Z]{1,2}[2-4]?|\*\d{1,3}[MFab]?)')
STRING_OR_COMMA = re.compile(r'("(?:\\.|[^"\\])*")|,(\s*[}\]])')
JS_BRACED_ESCAPE = re.compile(r'\\u\{([0-9a-fA-F]+)\}')
PHASE1_OBJECTS = {'HT9', 'HT85', 'HT88', 'HT89', 'HT94', 'HT104',
                  'HT117', 'HT118', 'HT122'}


def verify_source(data: bytes) -> dict[str, Any]:
    sha = hashlib.sha256(data).hexdigest()
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    if sha != SOURCE_SHA256 or blob != SOURCE_GIT_BLOB:
        raise ValueError('Source checksum mismatch; do not silently use a changed corpus.')
    return dict(url=SOURCE_URL, upstream_commit=UPSTREAM_COMMIT,
                sha256=sha, git_blob_sha=blob, bytes=len(data))


def fetch_source(path: Path) -> None:
    with urlopen(SOURCE_URL, timeout=60) as response:
        data = response.read(3_000_001)
    if len(data) > 3_000_000:
        raise ValueError('Unexpected source size')
    verify_source(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def parse_corpus(text: str) -> tuple[dict[str, dict], list[dict]]:
    """Read only the inscriptions Map's data; do not evaluate source functions."""
    match = re.search(r'\bvar\s+inscriptions\s*=\s*new\s+Map\(', text)
    if match is None:
        raise ValueError('Expected inscriptions Map not found')
    body = text[match.end():].lstrip()
    body = STRING_OR_COMMA.sub(
        lambda m: m[1] if m[1] is not None else m[2], body)
    # Convert JS code-point escapes only inside double-quoted strings. The input
    # array uses double-quoted keys/values; the remainder of the JS is not read.
    def convert_string(m: re.Match) -> str:
        return JS_BRACED_ESCAPE.sub(
            lambda e: json.dumps(chr(int(e[1], 16)), ensure_ascii=True)[1:-1], m[0])
    body = re.sub(r'"(?:\\.|[^"\\])*"', convert_string, body)
    pairs, end = json.JSONDecoder().raw_decode(body)
    if not body[end:].lstrip().startswith(');'):
        raise ValueError('Unexpected content after inscriptions array')
    if not isinstance(pairs, list):
        raise ValueError('Expected a list of record pairs')
    docs: dict[str, dict] = {}
    duplicates = []
    for pair in pairs:
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError('Malformed Map entry')
        key, value = pair
        if not isinstance(key, str) or not isinstance(value, dict):
            raise ValueError('Malformed record ID or value')
        for field in ('words', 'transliteratedWords'):
            if not isinstance(value.get(field), list) or not all(
                    isinstance(t, str) for t in value[field]):
                raise ValueError(f'Malformed {field} in {key}')
        if key in docs:
            duplicates.append(dict(document=key, identical=docs[key] == value,
                earlier_transliterated_tokens=len(docs[key]['transliteratedWords']),
                later_transliterated_tokens=len(value['transliteratedWords']),
                policy='last entry wins, matching JavaScript Map semantics'))
        docs[key] = value
    return docs, duplicates


def normalize_label(text: str) -> str:
    return text.translate(SUBSCRIPTS)


def is_lexical(text: str) -> bool:
    """Syntactic multi-sign candidate; not a claim that this is a true word."""
    parts = normalize_label(text).split('-')
    return len(parts) >= 2 and all(SIGN.fullmatch(p) for p in parts)


def word_flags(label: str, raw: str) -> list[str]:
    flags = []
    if LOSS in raw or LOSS in label:
        flags.append('loss_marker')
    if any(c in label for c in '[]?'):
        flags.append('editorial_uncertainty')
    if not raw or any(not 0x10600 <= ord(c) <= 0x10736 for c in raw):
        flags.append('raw_not_only_linear_a_signs')
    return flags


def object_id(record_id: str) -> str:
    """Join a/b/c faces only when a final lowercase letter follows a digit."""
    return re.sub(r'(?<=\d)[a-z]$', '', record_id)


def raw_integer(raw: str) -> int | None:
    """Read only complete positive Aegean integers, not inferred fractions."""
    if not raw or not all(0x10107 <= ord(c) <= 0x10133 for c in raw):
        return None
    return sum(((ord(c) - 0x10107) % 9 + 1)
               * 10 ** ((ord(c) - 0x10107) // 9) for c in raw)


def has_quantity(raw: str, label: str) -> bool:
    return (any(0x10107 <= ord(c) <= 0x10133 or 0x10740 <= ord(c) <= 0x1075a
                for c in raw)
            or bool(re.fullmatch(r'\d+(?:\.\d+)?', label))
            or '\u2044' in label)


def aligned_rows(record: dict) -> list[list[dict]] | None:
    """Rows are Explorer's parsed rows, NOT necessarily original physical lines."""
    a, b = record['transliteratedWords'], record['words']
    if len(a) != len(b) or any((t == '\n') != (r == '\n') for t, r in zip(a, b)):
        return None
    rows: list[list[dict]] = [[]]
    for i, (label, raw) in enumerate(zip(a, b)):
        if label == '\n':
            rows.append([])
        else:
            rows[-1].append(dict(label=normalize_label(label), raw=raw,
                                  token_index=i))
    return rows


def morphology(docs: dict[str, dict],
               excluded_tokens: set[tuple[str, int]] | None=None) -> tuple[dict, dict]:
    unflagged: dict[str, list] = defaultdict(list)
    flagged: dict[str, list] = defaultdict(list)
    mismatches = []
    boundary_candidates = []
    raw_damage_hidden = 0
    for doc_id, doc in docs.items():
        rows = aligned_rows(doc)
        if rows is None:
            mismatches.append(dict(document=doc_id, raw_tokens=len(doc['words']),
                             transliterated_tokens=len(doc['transliteratedWords'])))
            continue
        first_quantity_row = next((i for i, row in enumerate(rows)
            if any(has_quantity(t['raw'], t['label']) for t in row)), None)
        for ri, row in enumerate(rows):
            for t in row:
                label, raw = t['label'], t['raw']
                if not is_lexical(label):
                    continue
                flags = word_flags(label, raw)
                if (doc_id, t['token_index']) in (excluded_tokens or set()):
                    flags.append('editorial_not_independent_word')
                if LOSS in raw and LOSS not in label:
                    raw_damage_hidden += 1
                entry = dict(document=doc_id, object=object_id(doc_id),
                    site=doc['site'], support=doc['support'], scribe=doc['scribe'],
                    parsed_row=ri+1, token_index=t['token_index'], form=label,
                    raw=raw, flags=flags,
                    context=' '.join(t['label'] for t in row),
                    initial_unnumbered_block=(None if first_quantity_row is None
                        else ri < first_quantity_row))
                (flagged if flags else unflagged)[label].append(entry)
        # This is a REVIEW queue, not an automatic license to concatenate words.
        for i in range(len(rows)-1):
            if not rows[i] or not rows[i+1]:
                continue
            left, right = rows[i][-1], rows[i+1][0]
            if (all(SIGN.fullmatch(z) for z in left['label'].split('-'))
                and all(SIGN.fullmatch(z) for z in right['label'].split('-'))
                and not word_flags(left['label'], left['raw'])
                and not word_flags(right['label'], right['raw'])):
                boundary_candidates.append(dict(document=doc_id,
                    left=left['label'], right=right['label'],
                    left_token_index=left['token_index'],
                    right_token_index=right['token_index'],
                    hypothetical_join=left['label']+'-'+right['label']))
    pairs = []
    for longer in sorted(unflagged):
        parts = longer.split('-')
        for width in (1, 2):
            if len(parts) < width+2:
                continue
            for side in ('prefix', 'suffix'):
                base = '-'.join(parts[width:] if side=='prefix' else parts[:-width])
                edge = '-'.join(parts[:width] if side=='prefix' else parts[-width:])
                if base not in unflagged:
                    continue
                left, right = unflagged[base], unflagged[longer]
                common_objects = sorted({x['object'] for x in left}
                                        & {x['object'] for x in right})
                common_scribes = sorted({x['scribe'] for x in left if x['scribe']}
                                        & {x['scribe'] for x in right if x['scribe']})
                pairs.append(dict(side=side, edge=edge, base=base, extended=longer,
                    base_occurrences=left, extended_occurrences=right,
                    same_objects=common_objects, same_scribes=common_scribes,
                    status='machine-unflagged candidates; editorial review required'))
    summary = dict(machine_unflagged_tokens=sum(map(len, unflagged.values())),
                   machine_unflagged_types=len(unflagged),
                   flagged_tokens=sum(map(len, flagged.values())),
                   flagged_types=len(flagged),
                   union_types=len(set(unflagged)|set(flagged)),
                   lexical_tokens_with_loss_hidden_in_romanization=raw_damage_hidden,
                   alignment_exclusions=mismatches,
                   affix_candidate_counts=dict(sorted(Counter(
                       f"{p['side']}:{p['edge']}" for p in pairs).items())),
                   line_boundary_review_candidates=len(boundary_candidates))
    details = dict(unflagged_occurrences=dict(sorted(unflagged.items())),
                   flagged_occurrences=dict(sorted(flagged.items())),
                   affix_candidates=pairs, line_boundary_review=boundary_candidates)
    return summary, details


def eligible_integer_row(row: list[dict], mode: str="narrow") -> dict | None:
    """A final intact integer; candidate labels are evaluated separately.

    narrow: every addend must have exactly one lexical candidate label.
    numeric: addends may instead have logograms or multiple intact sign groups.
    A numerical equality does not establish that units are commensurate.
    """
    if mode not in {"narrow", "numeric"}:
        raise ValueError("Unknown arithmetic eligibility mode")
    tokens = [t for t in row if t['label'] != DIVIDER]
    if not tokens or any(LOSS in t['raw'] or any(c in t['label'] for c in '[]?')
                         or t['label'] in RULES for t in tokens):
        return None
    numeric_positions = [i for i,t in enumerate(tokens)
                         if has_quantity(t['raw'], t['label'])]
    if numeric_positions != [len(tokens)-1]:
        return None
    quantity = raw_integer(tokens[-1]['raw'])
    if quantity is None or quantity <= 0:
        return None
    # The independently decoded raw integer must match the romanized field.
    if tokens[-1]['label'] != str(quantity):
        return None
    if len(tokens) < 2:
        return None
    words = [t for t in tokens[:-1] if is_lexical(t['label'])]
    target = words[0] if len(words) == 1 else None
    if target is not None and (word_flags(target['label'], target['raw']) or
        any(t is not target and len(t['raw']) != 1 for t in tokens[:-1])):
        target = None
    if mode == 'narrow' and target is None:
        return None
    # Broader addend eligibility still rejects unknown, lost, or non-sign text.
    if mode == 'numeric' and any(word_flags(t['label'], t['raw'])
                                 for t in tokens[:-1]):
        return None
    return dict(form=target['label'] if target else None, quantity=quantity,
                label_group=' '.join(t['label'] for t in tokens[:-1]),
                token_index=(target or tokens[0])['token_index'],
                context=' '.join(t['label'] for t in row))


def integer_blocks(docs: dict[str, dict], mode: str="narrow") -> tuple[list[dict], dict]:
    blocks = []
    eligible_count = 0
    eligible_forms: Counter = Counter()
    for doc_id, doc in docs.items():
        if doc['support'].lower() != 'tablet':
            continue
        rows = aligned_rows(doc)
        if rows is None:
            continue
        run = []
        for ri, row in enumerate(rows + [[]]):
            entry = eligible_integer_row(row, mode)
            if entry is not None:
                entry['parsed_row'] = ri+1
                run.append(entry)
                eligible_count += 1
                if entry['form'] is not None:
                    eligible_forms[entry['form']] += 1
            else:
                if len(run) >= 3:
                    blocks.append(dict(document=doc_id, object=object_id(doc_id),
                        site=doc['site'], scribe=doc['scribe'], entries=run))
                run = []
    return blocks, dict(eligibility_mode=mode, eligible_integer_rows=eligible_count,
                        eligible_form_counts=dict(sorted(eligible_forms.items())),
                        blocks_of_at_least_three=len(blocks),
                        objects_with_blocks=len({b['object'] for b in blocks}))


def score_blocks(blocks: list[dict], quantities: list[list[int]] | None=None,
                 max_terms: int=12) -> tuple[dict[str,int], list[dict]]:
    """Count distinct objects with a backward exact-sum closure for each label."""
    objects: dict[str,set] = defaultdict(set)
    matches = []
    for bi, block in enumerate(blocks):
        entries = block['entries']
        q = quantities[bi] if quantities is not None else [e['quantity'] for e in entries]
        for end in range(2, len(q)):
            if entries[end]['form'] is None:
                continue
            subtotal = 0
            for start in range(end-1, max(-1, end-max_terms-1), -1):
                subtotal += q[start]
                if end-start >= 2 and subtotal == q[end]:
                    form = entries[end]['form']
                    objects[form].add(block['object'])
                    matches.append(dict(form=form, document=block['document'],
                        object=block['object'], start_row=entries[start]['parsed_row'],
                        end_row=entries[end]['parsed_row'], terms=q[start:end],
                        total=q[end], addend_forms=[e['form'] for e in entries[start:end]],
                        addend_labels=[e.get('label_group', e['form']) for e in entries[start:end]],
                        earlier_phase1_object=block['object'] in PHASE1_OBJECTS))
                if subtotal >= q[end]:
                    break
    return {k:len(v) for k,v in sorted(objects.items())}, matches


def arithmetic(docs: dict[str,dict], permutations: int, seed: int,
               mode: str="narrow") -> tuple[dict,dict]:
    blocks, summary = integer_blocks(docs, mode)
    observed, matches = score_blocks(blocks)
    tested_forms = sorted({e['form'] for b in blocks for e in b['entries'][2:]
                           if e['form'] is not None})
    uncorrected = Counter()
    max_null_histogram = Counter()
    rng = random.Random(seed)
    for _ in range(permutations):
        q = [[e['quantity'] for e in b['entries']] for b in blocks]
        for row in q:
            rng.shuffle(row)
        scores,_ = score_blocks(blocks, q)
        max_null_histogram[max(scores.values(), default=0)] += 1
        for form, obs in observed.items():
            uncorrected[form] += scores.get(form,0) >= obs
    ranking = []
    for form, score in sorted(observed.items(), key=lambda kv:(-kv[1],kv[0])):
        adjusted = sum(n for maximum,n in max_null_histogram.items() if maximum >= score)
        ranking.append(dict(form=form, matching_objects=score,
            object_ids=sorted({m['object'] for m in matches if m['form']==form}),
            match_windows=sum(m['form']==form for m in matches),
            new_to_phase1_objects=sorted({m['object'] for m in matches
                if m['form']==form and not m['earlier_phase1_object']}),
            permutation_p=(1+uncorrected[form])/(1+permutations),
            max_statistic_adjusted_p=(1+adjusted)/(1+permutations)))
    summary.update(dict(seed=seed, permutations=permutations, max_terms=12,
        tested_forms=len(tested_forms), ranking=ranking,
        null_max_score_histogram=dict(sorted(max_null_histogram.items())),
        interpretation=('Within-block amount permutations preserve the record, label, '
            'and quantity inventories. Scores count objects, not independent faces. '
            'This is a retrospective structural diagnostic; it does not establish '
            'units, lexical meanings, epigraphic certainty, or independent validation.')))
    return summary, dict(blocks=blocks, matches=matches, tested_forms=tested_forms)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, sort_keys=True, indent=2)+'\n')


def main(argv: list[str] | None=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT/'data/LinearAInscriptions.js')
    parser.add_argument('--output', type=Path, default=ROOT/'results')
    parser.add_argument('--fetch', action='store_true', help='Fetch missing pinned source')
    parser.add_argument('--permutations', type=int, default=4999)
    parser.add_argument('--seed', type=int, default=20260914)
    parser.add_argument('--reviews', type=Path,
                        default=ROOT/'data/editorial_reviews.json')
    args = parser.parse_args(argv)
    if args.permutations < 0:
        parser.error('--permutations must be nonnegative')
    if not args.source.exists():
        if not args.fetch:
            parser.error('Source missing: supply --source or use --fetch')
        fetch_source(args.source)
    data = args.source.read_bytes()
    provenance = verify_source(data)
    docs, duplicates = parse_corpus(data.decode('utf-8'))
    m_summary, m_details = morphology(docs)
    reviews = json.loads(args.reviews.read_text())
    if reviews['upstream_commit'] != UPSTREAM_COMMIT:
        raise ValueError('Editorial reviews refer to a different source commit')
    exclusions = set()
    for r in reviews['exclude_as_independent_words']:
        actual = docs[r['document']]['transliteratedWords'][r['token_index']]
        if normalize_label(actual) != r['form']:
            raise ValueError('Editorial review target does not match source token')
        exclusions.add((r['document'], r['token_index']))
    reviewed_summary, reviewed_details = morphology(docs, exclusions)
    a_summary, a_details = {}, {}
    for mode in ('narrow', 'numeric'):
        a_summary[mode], a_details[mode] = arithmetic(
            docs, args.permutations, args.seed, mode)
    sensitivity_docs = {k:v for k,v in docs.items() if object_id(k) != 'HT127'}
    a_summary['numeric_excluding_HT127'], a_details['numeric_excluding_HT127'] = (
        arithmetic(sensitivity_docs, args.permutations, args.seed, 'numeric'))
    a_summary['numeric_excluding_HT127']['editorial_excluded_objects'] = ['HT127']
    summary = dict(source=provenance, source_map_entries=len(docs)+len(duplicates),
        unique_record_ids=len(docs), inferred_objects=len({object_id(k) for k in docs}),
        duplicate_entries=duplicates,
        sites=dict(sorted(Counter(d['site'] for d in docs.values()).items())),
        supports=dict(sorted(Counter(d['support'] for d in docs.values()).items())),
        morphology=m_summary, reviewed_morphology=reviewed_summary,
        editorial_review_tokens=len(exclusions), arithmetic=a_summary)
    write_json(args.output/'phase4_summary.json', summary)
    write_json(args.output/'phase4_morphology.json', m_details)
    write_json(args.output/'phase4_arithmetic.json', a_details)
    write_json(args.output/'phase4_reviewed_morphology.json', reviewed_details)
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(1)
