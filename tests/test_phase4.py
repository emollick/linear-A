"""Regression tests for mechanics, not certification of ancient readings."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import phase4 as p


def integer(n):
    if not 1 <= n < 100000:
        raise ValueError(n)
    out = ''
    for power in range(4, -1, -1):
        digit = n // (10 ** power) % 10
        if digit:
            out += chr(0x10107 + 9 * power + digit - 1)
    return out


def token(label, raw=None, index=0):
    if raw is None:
        raw = integer(int(label)) if label.isdigit() else '\U00010600' * len(label.split('-'))
    return dict(label=label, raw=raw, token_index=index)


def doc(rows, site='X', support='Tablet'):
    labels, raw = [], []
    for i, row in enumerate(rows):
        if i:
            labels.append('\n'); raw.append('\n')
        for t in row:
            labels.append(t['label']); raw.append(t['raw'])
    return dict(words=raw, transliteratedWords=labels, translatedWords=['DO NOT USE'],
                site=site, support=support, scribe='')


def simple_rows():
    return [[token('A-BA'), token('2')], [token('C-DA'), token('3')],
            [token('E-FA'), token('5')]]


class ParserTests(unittest.TestCase):
    def test_trailing_commas_and_braced_codepoint(self):
        text = r'var inscriptions = new Map([["X1",{"words":["\u{1076b}",],"transliteratedWords":["A",],},],]);'
        d, audit = p.parse_corpus(text)
        self.assertEqual(d['X1']['words'], [p.LOSS])
        self.assertFalse(audit)

    def test_trailing_comma_in_string_is_not_removed(self):
        record = dict(words=[',]'], transliteratedWords=[',]'])
        d, _ = p.parse_corpus('var inscriptions = new Map(' + json.dumps([['X', record]]) + ');')
        self.assertEqual(d['X']['words'], [',]'])

    def test_duplicate_last_wins_and_audited(self):
        first = dict(words=[], transliteratedWords=[])
        second = dict(words=['x'], transliteratedWords=['y'])
        d, audit = p.parse_corpus('var inscriptions = new Map(' + json.dumps([['X', first], ['X', second]]) + ');')
        self.assertEqual(d['X'], second)
        self.assertEqual(len(audit), 1)
        self.assertFalse(audit[0]['identical'])

    def test_javascript_not_executed(self):
        text = 'var inscriptions = new Map([]); throw new Error("must not execute");'
        self.assertEqual(p.parse_corpus(text), ({}, []))

    def test_expressions_inside_array_rejected(self):
        with self.assertRaises(ValueError):
            p.parse_corpus('var inscriptions = new Map([dangerous()]);')

    def test_wrong_wrapper_rejected(self):
        with self.assertRaises(ValueError):
            p.parse_corpus('var other = [];')

    def test_malformed_tokens_rejected(self):
        with self.assertRaises(ValueError):
            p.parse_corpus('var inscriptions = new Map([["X", {"words":[1], "transliteratedWords":[]}]]);')

    def test_wrong_source_hash_rejected(self):
        with self.assertRaises(ValueError):
            p.verify_source(b'changed source')


class TokenTests(unittest.TestCase):
    def test_raw_loss_survives_romanization(self):
        self.assertIn('loss_marker', p.word_flags('A-BA', '\U00010600' + p.LOSS))

    def test_question_mark_is_uncertain(self):
        self.assertIn('editorial_uncertainty', p.word_flags('A-BA?', '\U00010600'))

    def test_subscript_sign_variants_only(self):
        self.assertEqual(p.normalize_label('PA\u2083-QE\u2082'), 'PA3-QE2')
        self.assertEqual(p.normalize_label('\u00b9\u20442'), '\u00b9\u20442')

    def test_lexical_scope(self):
        self.assertTrue(p.is_lexical('A-*301'))
        self.assertFalse(p.is_lexical('A'))
        self.assertFalse(p.is_lexical('MA+RU-ME'))
        self.assertFalse(p.is_lexical('A-AROM'))

    def test_faces_not_independent_objects(self):
        self.assertEqual(p.object_id('HT96b'), 'HT96')
        self.assertEqual(p.object_id('HTWc3024'), 'HTWc3024')

    def test_alignment_failure(self):
        self.assertIsNone(p.aligned_rows(dict(words=['a'], transliteratedWords=[])))
        self.assertIsNone(p.aligned_rows(dict(words=['a', '\n'], transliteratedWords=['\n', 'a'])))

    def test_boundary_review_does_not_merge(self):
        d = doc([[token('JA-SA-SA-RA')], [token('ME')]])
        _, details = p.morphology({'X1': d})
        self.assertNotIn('JA-SA-SA-RA-ME', details['unflagged_occurrences'])
        self.assertEqual(len(details['line_boundary_review']), 1)

    def test_editorial_overlay_preserves_original(self):
        d = doc([[token('JA-SA-SA-RA')], [token('ME')]])
        _, original = p.morphology({'X1': d})
        _, reviewed = p.morphology({'X1': d}, {('X1', 0)})
        self.assertIn('JA-SA-SA-RA', original['unflagged_occurrences'])
        self.assertNotIn('JA-SA-SA-RA', reviewed['unflagged_occurrences'])
        self.assertIn('JA-SA-SA-RA', reviewed['flagged_occurrences'])

    def test_english_glosses_are_unused(self):
        docs = {'X1': doc(simple_rows())}
        changed = copy.deepcopy(docs)
        changed['X1']['translatedWords'] = ['KU-RO means anything'] * 99
        self.assertEqual(p.morphology(docs), p.morphology(changed))
        self.assertEqual(p.arithmetic(docs, 9, 7), p.arithmetic(changed, 9, 7))


class ArithmeticTests(unittest.TestCase):
    def test_integer_round_trip(self):
        for n in [1, 9, 10, 11, 45, 95, 180, 292, 99999]:
            self.assertEqual(p.raw_integer(integer(n)), n)

    def test_fraction_and_damaged_number_not_integer(self):
        self.assertIsNone(p.raw_integer('\U00010746'))
        self.assertIsNone(p.raw_integer(integer(6) + p.LOSS))

    def test_romanized_number_must_match_raw(self):
        row = [token('A-BA'), token('6', raw=integer(7))]
        self.assertIsNone(p.eligible_integer_row(row, 'numeric'))

    def test_numeric_addend_need_not_have_word(self):
        row = [token('KA'), token('7')]
        self.assertIsNone(p.eligible_integer_row(row, 'narrow'))
        entry = p.eligible_integer_row(row, 'numeric')
        self.assertEqual(entry['quantity'], 7)
        self.assertIsNone(entry['form'])

    def test_fraction_does_not_get_silently_dropped(self):
        row = [token('A-BA'), token('4'), token('1/2', '\U00010746')]
        self.assertIsNone(p.eligible_integer_row(row, 'numeric'))

    def test_arbitrary_label_recovered_not_just_ku_ro(self):
        blocks, _ = p.integer_blocks({'X1': doc(simple_rows())})
        scores, matches = p.score_blocks(blocks)
        self.assertEqual(scores, {'E-FA': 1})
        self.assertEqual(matches[0]['terms'], [2, 3])

    def test_invalid_row_breaks_sum(self):
        rows = simple_rows()
        rows.insert(2, [token('?', p.LOSS)])
        blocks, _ = p.integer_blocks({'X1': doc(rows)}, 'numeric')
        self.assertEqual(p.score_blocks(blocks)[0], {})

    def test_damaged_label_not_an_intact_numeric_row(self):
        row = [token('A-BA', '\U00010600' + p.LOSS), token('5')]
        self.assertIsNone(p.eligible_integer_row(row, 'numeric'))

    def test_duplicate_faces_count_once(self):
        blocks, _ = p.integer_blocks({'X1a': doc(simple_rows()), 'X1b': doc(simple_rows())})
        scores, matches = p.score_blocks(blocks)
        self.assertEqual(scores['E-FA'], 1)
        self.assertEqual(len(matches), 2)

    def test_maximum_window_is_enforced(self):
        rows = [[token('A-BA'), token('1')] for _ in range(13)] + [[token('E-FA'), token('13')]]
        blocks, _ = p.integer_blocks({'X1': doc(rows)})
        self.assertEqual(p.score_blocks(blocks, max_terms=12)[0], {})
        self.assertEqual(p.score_blocks(blocks, max_terms=13)[0], {'E-FA': 1})

    def test_seed_and_max_statistic(self):
        docs = {'X1': doc(simple_rows())}
        one = p.arithmetic(docs, 99, 123)
        self.assertEqual(one, p.arithmetic(docs, 99, 123))
        for row in one[0]['ranking']:
            self.assertGreaterEqual(row['max_statistic_adjusted_p'], row['permutation_p'])

    def test_support_filter(self):
        blocks, _ = p.integer_blocks({'X1': doc(simple_rows(), support='Roundel')})
        self.assertFalse(blocks)


@unittest.skipUnless((ROOT/'data/LinearAInscriptions.js').exists(), 'pinned corpus not downloaded')
class CorpusRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = (ROOT/'data/LinearAInscriptions.js').read_bytes()
        p.verify_source(raw)
        cls.docs, cls.duplicates = p.parse_corpus(raw.decode('utf-8'))

    def test_census_and_duplicate(self):
        self.assertEqual(len(self.docs), 1721)
        self.assertEqual([x['document'] for x in self.duplicates], ['KH101'])

    def test_raw_loss_and_alignment_census(self):
        summary, _ = p.morphology(self.docs)
        self.assertEqual(summary['machine_unflagged_types'], 605)
        self.assertEqual(summary['lexical_tokens_with_loss_hidden_in_romanization'], 412)
        self.assertEqual(summary['alignment_exclusions'][0]['document'], 'KNZg57b')

    def test_me_overlay_reduces_four_to_one(self):
        reviews = json.loads((ROOT/'data/editorial_reviews.json').read_text())
        exclude = {(x['document'], x['token_index']) for x in reviews['exclude_as_independent_words']}
        before, _ = p.morphology(self.docs)
        after, _ = p.morphology(self.docs, exclude)
        self.assertEqual(before['affix_candidate_counts']['suffix:ME'], 4)
        self.assertEqual(after['affix_candidate_counts']['suffix:ME'], 1)

    def test_numeric_counts_and_erasure_sensitivity(self):
        blocks, _ = p.integer_blocks(self.docs, 'numeric')
        scores, _ = p.score_blocks(blocks)
        self.assertEqual(scores['KU-RO'], 7)
        subset = {k:v for k,v in self.docs.items() if p.object_id(k) != 'HT127'}
        blocks, _ = p.integer_blocks(subset, 'numeric')
        self.assertEqual(p.score_blocks(blocks)[0]['KU-RO'], 6)


if __name__ == '__main__':
    unittest.main()
