"""Heading-comparison mechanics and corpus regressions; not readings of the objects."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'tests'))
import phase4 as p
import phase5 as q
import headings as h
from test_phase4 import doc, token


def plan(anchor, comparison=('C1',), words=('X-DU',)):
    return dict(upstream_commit=p.UPSTREAM_COMMIT,
                anchor=dict(documents=list(anchor)), comparison=dict(documents=list(comparison)),
                heading_words=list(words))


class SectionTests(unittest.TestCase):
    def test_quantity_free_row_becomes_heading_for_following_rows(self):
        rows = [[token('X-DU'), token(p.DIVIDER, p.DIVIDER)], [token('A-BA'), token('2')],
                [token('—', '—')], [token('Y-DU')], [token('C-DA'), token('3')]]
        layout = h.sections(rows)
        self.assertEqual([s['heading'] for s in layout], ['X-DU', 'X-DU', 'X-DU', 'Y-DU', 'Y-DU'])
        self.assertEqual([s['is_heading'] for s in layout], [True, False, False, True, False])

    def test_damage_only_row_does_not_reset_heading(self):
        rows = [[token('X-DU')], [token(p.LOSS, p.LOSS), token(p.DIVIDER, p.DIVIDER)],
                [token('A-BA'), token('2')]]
        self.assertEqual([s['heading'] for s in h.sections(rows)], ['X-DU', 'X-DU', 'X-DU'])

    def test_entry_labels_come_only_from_quantity_rows(self):
        rows = [[token('X-DU')], [token('A-BA'), token('2')], [token('C-DA'), token('3')],
                [token('A-BA'), token('4')]]
        self.assertEqual(h.entry_labels(rows), ['A-BA', 'C-DA'])


class RunTests(unittest.TestCase):
    def test_matrix_and_heading_census(self):
        docs = {
            'A1': doc([[token('X-DU'), token(p.DIVIDER, p.DIVIDER)], [token('A-BA'), token('2')], [token('C-DA'), token('3')]]),
            'C1': doc([[token('Y-DU')], [token('C-DA'), token('5')], [token('X-DU')], [token('A-BA'), token('7')]]),
            'Z9': doc([[token('X-DU'), token('9')]], site='Elsewhere'),
        }
        result = h.run(docs, set(), plan(['A1']))
        summary = result['summary']
        self.assertEqual(summary['anchor_entry_labels'], ['A-BA', 'C-DA'])
        self.assertEqual(summary['documents_with_at_least_two'], ['A1', 'C1'])
        self.assertEqual(result['label_matrix'], {'A-BA': {'A1': '2', 'C1': '7'}, 'C-DA': {'A1': '3', 'C1': '5'}})
        c1 = next(e for e in result['shared_label_documents'] if e['document'] == 'C1')
        self.assertEqual([x['section_heading'] for x in c1['labels']], ['Y-DU', 'X-DU'])
        census = summary['heading_words']['X-DU']
        self.assertEqual(census['occurrences'], 3)
        self.assertEqual(census['sites'], ['Elsewhere', 'X'])
        self.assertEqual(census['heading_row_occurrences'], 2)
        self.assertEqual(census['first_row_occurrences'], 2)

    def test_editorial_exclusion_is_reported_not_hidden(self):
        docs = {'A1': doc([[token('X-DU')], [token('A-BA'), token('2')], [token('C-DA'), token('3')]])}
        result = h.run(docs, {('A1', 2)}, plan(['A1']))  # token 1 is the row break
        hit = result['label_occurrences']['A-BA'][0]
        self.assertIn('editorial_not_independent_word', hit['flags'])

    def test_wrong_commit_and_missing_labels_rejected(self):
        docs = {'A1': doc([[token('X-DU')]])}
        bad = plan(['A1']); bad['upstream_commit'] = 'other'
        with self.assertRaises(ValueError):
            h.run(docs, set(), bad)
        with self.assertRaises(ValueError):
            h.run(docs, set(), plan(['A1']))


@unittest.skipUnless((ROOT / 'data/LinearAInscriptions.js').exists(), 'pinned corpus not downloaded')
class CorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = (ROOT / 'data/LinearAInscriptions.js').read_bytes()
        p.verify_source(raw)
        docs, _ = p.parse_corpus(raw.decode('utf-8'))
        excluded = q.load_exclusions(docs, [ROOT / 'data/editorial_reviews.json',
                                            ROOT / 'data/phase5_reviews.json'])
        cls.result = h.run(docs, excluded, json.loads((ROOT / 'data/heading_comparanda.json').read_text()))

    def test_six_anchor_labels_and_four_sharing_records(self):
        summary = self.result['summary']
        self.assertEqual(summary['anchor_entry_labels'],
                         ['DA-ME', 'MI-NU-TE', 'SA-RU', 'KU-NI-SU', 'DI-DE-RU', 'QE-RA2-U'])
        self.assertEqual(summary['documents_with_at_least_two'], ['HT95a', 'HT95b', 'HT86a', 'HT86b'])

    def test_ht95_quantities_and_ht86_headings(self):
        matrix = self.result['label_matrix']
        self.assertEqual([matrix[l]['HT95a'] for l in self.result['summary']['anchor_entry_labels']],
                         ['10', '10', '20', '10', '10', '7'])
        self.assertEqual([matrix[l]['HT95b'] for l in self.result['summary']['anchor_entry_labels']],
                         ['10'] * 6)
        ht86a = next(e for e in self.result['shared_label_documents'] if e['document'] == 'HT86a')
        self.assertEqual({x['form']: x['section_heading'] for x in ht86a['labels']},
                         {'KU-NI-SU': 'A-KA-RU', 'SA-RU': 'A-KA-RU', 'DI-DE-RU': 'A-KA-RU',
                          'DA-ME': 'A-DU', 'MI-NU-TE': 'A-DU'})
        self.assertEqual(ht86a['scribe'], 'HT Scribe 6')

    def test_heading_word_census(self):
        words = self.result['summary']['heading_words']
        self.assertEqual(words['DA-DU-MA-TA']['occurrences'], 1)
        self.assertEqual(words['A-DU']['occurrences'], 10)
        self.assertEqual(words['A-DU']['sites'], ['Haghia Triada', 'Khania', 'Tylissos'])
        self.assertEqual(words['A-DU']['first_row_occurrences'], 7)
        self.assertEqual(words['A-KA-RU']['objects'], ['HT2', 'HT86'])

    def test_gloss_field_is_not_consulted(self):
        text = (ROOT / 'scripts/headings.py').read_text()
        self.assertNotIn('translatedWords', text)


if __name__ == '__main__':
    unittest.main()
