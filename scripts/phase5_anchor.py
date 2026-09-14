#!/usr/bin/env python3
"""Test precise sign-tail predictions from a published origin hypothesis.

This is descriptive, post-hoc candidate testing. No probabilities are assigned
to meanings, and a absent predicted form is not proof that the language forbids it.
"""
import argparse
import json
from pathlib import Path
import phase4 as p
import phase5 as q
ROOT = Path(__file__).resolve().parents[1]


def tail_pairs(forms, old_tail, new_tail):
    old_tail, new_tail = tuple(old_tail), tuple(new_tail)
    if not old_tail or not new_tail:
        raise ValueError('Both tails must be nonempty')
    words = {tuple(form.split('-')) for form in forms}
    return [{'base': '-'.join(w), 'extended': '-'.join(w[:-len(old_tail)]+new_tail)}
            for w in sorted(words)
            if len(w)>len(old_tail) and w[-len(old_tail):]==old_tail
            and w[:-len(old_tail)]+new_tail in words]


def run(docs, reviews, anchors):
    if anchors['upstream_commit'] != p.UPSTREAM_COMMIT:
        raise ValueError('Anchor source version mismatch')
    _, morph = p.morphology(docs, reviews)
    occurrences = morph['unflagged_occurrences']
    results = []
    for anchor in anchors['anchors']:
        for form, record in [(anchor['base'],anchor['base_record']),
                             (anchor['extended'],anchor['extended_record'])]:
            if not any(o['document']==record for o in occurrences.get(form,[])):
                raise ValueError('Expected source candidate missing: '+form)
        old = anchor['attested_alternation']['old_tail']
        new = anchor['attested_alternation']['new_tail']
        prediction = anchor['base']+'-JA'
        results.append(dict(id=anchor['id'], base=anchor['base'],extended=anchor['extended'],
            source_occurrences={w:occurrences[w] for w in [anchor['base'],anchor['extended']]},
            simple_JA_prediction=prediction,
            simple_JA_prediction_attested_in_eligible_types=prediction in occurrences,
            direct_intermediate=anchor['extended'].removesuffix('-I-JA'),
            direct_intermediate_attested=anchor['extended'].removesuffix('-I-JA') in occurrences,
            exact_tail_replacement_pairs=tail_pairs(occurrences,old,new)))
    return dict(types=len(occurrences),anchors=results,
        limitation='Exact matches in selected machine-unflagged types, not proof of grammatical identity or nonexistence elsewhere.')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,default=ROOT/'data/LinearAInscriptions.js')
    ap.add_argument('--output',type=Path,default=ROOT/'results')
    args=ap.parse_args();body=args.source.read_bytes();p.verify_source(body)
    docs,_=p.parse_corpus(body.decode())
    reviews=q.load_exclusions(docs,[ROOT/'data/editorial_reviews.json',ROOT/'data/phase5_reviews.json'])
    anchors=json.loads((ROOT/'data/phase5_semantic_anchors.json').read_text())
    result=run(docs,reviews,anchors)
    p.write_json(args.output/'phase5_anchor_results.json',result)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
