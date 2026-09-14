#!/usr/bin/env python3
"""Compare heading words and shared entry labels across documents.

H1 reads the two headings of HT 95 as a reference assessment and a revision.
This descriptive pass collects the entry labels of an anchor document, finds
every document in the pinned corpus that shares them, records the heading each
shared label sits under, and lists every occurrence of the heading words. It
assigns no meanings: it shows which comparisons exist for a hypothesis to
explain. Section headings are inferred from parsed rows, not from the edition.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import sys

import phase4 as p
import phase5 as q

ROOT = Path(__file__).resolve().parents[1]


def is_content(token: dict) -> bool:
    """A token that can carry a heading: not a divider, rule, or bare loss mark."""
    label = token['label']
    return (label != p.DIVIDER and label not in p.RULES
            and label.replace(p.LOSS, '') != '')


def row_has_quantity(row: list[dict]) -> bool:
    return any(p.has_quantity(t['raw'], t['label']) for t in row)


def sections(rows: list[list[dict]]) -> list[dict]:
    """Attach each row to the most recent quantity-free content row.

    A row without a quantity that still carries signs is treated as a heading
    for the rows that follow it. Rules and damage-only rows leave the current
    heading unchanged. This is a reading aid for tabular accounts, not a
    reconstruction of the original layout.
    """
    heading = None
    result = []
    for index, row in enumerate(rows):
        content = [t['label'] for t in row if is_content(t)]
        if content and not row_has_quantity(row):
            heading = ' '.join(content)
            result.append(dict(parsed_row=index + 1, heading=heading, is_heading=True))
        else:
            result.append(dict(parsed_row=index + 1, heading=heading, is_heading=False))
    return result


def entry_labels(rows: list[list[dict]]) -> list[str]:
    """Lexical labels in rows that carry a quantity, in order of first appearance."""
    labels = []
    for row in rows:
        if not row_has_quantity(row):
            continue
        for t in row:
            if p.is_lexical(t['label']) and t['label'] not in labels:
                labels.append(t['label'])
    return labels


def occurrence(doc_id: str, doc: dict, row: list[dict], token: dict,
               section: dict, excluded: set[tuple[str, int]]) -> dict:
    flags = p.word_flags(token['label'], token['raw'])
    if (doc_id, token['token_index']) in excluded:
        flags.append('editorial_not_independent_word')
    position = row.index(token)
    after = [t['label'] for t in row[position + 1:] if t['label'] != p.DIVIDER]
    quantity = [label for label in after if p.has_quantity('', label)
                or any(0x10107 <= ord(c) <= 0x10133 or 0x10740 <= ord(c) <= 0x1075a
                       for c in label)]
    return dict(document=doc_id, object=p.object_id(doc_id), site=doc['site'],
                support=doc['support'], scribe=doc['scribe'],
                parsed_row=section['parsed_row'], is_heading_row=section['is_heading'],
                section_heading=section['heading'], form=token['label'],
                following_labels=after, quantity_labels=quantity,
                flags=flags, context=' '.join(t['label'] for t in row))


def scan(docs: dict[str, dict], targets: set[str],
         excluded: set[tuple[str, int]]) -> dict[str, list[dict]]:
    found: dict[str, list[dict]] = defaultdict(list)
    for doc_id, doc in docs.items():
        rows = p.aligned_rows(doc)
        if rows is None:
            continue
        layout = sections(rows)
        for row, section in zip(rows, layout):
            for token in row:
                if token['label'] in targets:
                    found[token['label']].append(
                        occurrence(doc_id, doc, row, token, section, excluded))
    return dict(sorted(found.items()))


def run(docs: dict[str, dict], excluded: set[tuple[str, int]], plan: dict) -> dict:
    if plan['upstream_commit'] != p.UPSTREAM_COMMIT:
        raise ValueError('Heading comparanda refer to a different source commit')
    labels: list[str] = []
    for record in plan['anchor']['documents']:
        rows = p.aligned_rows(docs[record])
        if rows is None:
            raise ValueError('Anchor record is not aligned: ' + record)
        for label in entry_labels(rows):
            if label not in labels:
                labels.append(label)
    if not labels:
        raise ValueError('No entry labels found on the anchor documents')
    label_hits = scan(docs, set(labels), excluded)
    per_document: dict[str, dict] = {}
    for label, hits in label_hits.items():
        for hit in hits:
            entry = per_document.setdefault(hit['document'], dict(
                document=hit['document'], object=hit['object'], site=hit['site'],
                support=hit['support'], scribe=hit['scribe'], labels=[], headings=[]))
            entry['labels'].append(dict(form=label, parsed_row=hit['parsed_row'],
                section_heading=hit['section_heading'], following_labels=hit['following_labels'],
                quantity_labels=hit['quantity_labels'], flags=hit['flags']))
            if hit['section_heading'] not in entry['headings']:
                entry['headings'].append(hit['section_heading'])
    for entry in per_document.values():
        entry['labels'].sort(key=lambda x: x['parsed_row'])
        entry['distinct_labels'] = len({x['form'] for x in entry['labels']})
    shared = sorted(per_document.values(), key=lambda e: (-e['distinct_labels'], e['document']))
    heading_hits = scan(docs, set(plan['heading_words']), excluded)
    heading_summary = {}
    for word in plan['heading_words']:
        hits = heading_hits.get(word, [])
        heading_summary[word] = dict(
            occurrences=len(hits), documents=sorted({h['document'] for h in hits}),
            objects=sorted({h['object'] for h in hits}), sites=sorted({h['site'] for h in hits}),
            heading_row_occurrences=sum(h['is_heading_row'] for h in hits),
            first_row_occurrences=sum(h['parsed_row'] == 1 for h in hits),
            unflagged_occurrences=sum(not h['flags'] for h in hits))
    matrix = {label: {h['document']: ' '.join(h['quantity_labels']) or None
                      for h in label_hits.get(label, [])} for label in labels}
    summary = dict(anchor_documents=plan['anchor']['documents'],
        comparison_documents=plan['comparison']['documents'],
        anchor_entry_labels=labels,
        documents_with_any_anchor_label=len(shared),
        documents_with_at_least_two=[e['document'] for e in shared if e['distinct_labels'] >= 2],
        headings_over_anchor_labels=dict(sorted(Counter(
            x['section_heading'] or '(no heading row)' for e in shared
            for x in e['labels']).items(), key=lambda kv: (-kv[1], kv[0]))),
        heading_words=heading_summary,
        interpretation=('Descriptive comparison of exact labels and inferred section headings '
                        'in one pinned digital corpus. It shows which documents share the '
                        'anchor labels and under which headings; it does not assign meanings, '
                        'establish that labels are names, or order the documents in time.'))
    return dict(source_plan=plan, summary=summary, label_matrix=matrix,
                shared_label_documents=shared, label_occurrences=label_hits,
                heading_word_occurrences=heading_hits)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT / 'data/LinearAInscriptions.js')
    parser.add_argument('--output', type=Path, default=ROOT / 'results')
    parser.add_argument('--plan', type=Path, default=ROOT / 'data/heading_comparanda.json')
    args = parser.parse_args(argv)
    data = args.source.read_bytes()
    provenance = p.verify_source(data)
    docs, _ = p.parse_corpus(data.decode('utf-8'))
    excluded = q.load_exclusions(docs, [ROOT / 'data/editorial_reviews.json',
                                        ROOT / 'data/phase5_reviews.json'])
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    result = run(docs, excluded, plan)
    result['source'] = provenance
    p.write_json(args.output / 'heading_comparanda.json', result)
    print(json.dumps(result['summary'], ensure_ascii=True, indent=2))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        sys.exit(1)
