"""Fraction-aware summation mechanics and corpus regressions; not unit identification."""
from fractions import Fraction
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'tests'))
import phase4 as p
import fraction_accounting as f
from test_phase4 import doc, integer, token

HALF, QUARTER, SIXTH = '\U00010746', '\U00010743', '\U00010745'


def half(index=0):
    return token('¹⁄2', HALF, index)


def quarter(index=0):
    return token('¹⁄4', QUARTER, index)


class ValueTests(unittest.TestCase):
    def test_exact_labels(self):
        self.assertEqual(f.fraction_value('¹⁄2'), Fraction(1, 2))
        self.assertEqual(f.fraction_value('³⁄4'), Fraction(3, 4))
        self.assertEqual(f.fraction_value('¹⁄₁₆'), Fraction(1, 16))
        self.assertEqual(f.fraction_value('13/20'), Fraction(13, 20))
        self.assertEqual(f.fraction_value('⅝'), Fraction(5, 8))

    def test_approximate_unassigned_and_weights_rejected(self):
        for label in ['≈ ¹⁄₆', 'double mina', '.3', '?', 'L', '\U00010753', '3/2', '0/4']:
            self.assertIsNone(f.fraction_value(label), label)

    def test_format_round_trip(self):
        for value in [Fraction(29), Fraction(91, 2), Fraction(3, 4), Fraction(187, 2)]:
            self.assertEqual(f.parse_fraction_string(f.format_quantity(value)), value)
        self.assertEqual(f.format_quantity(Fraction(91, 2)), '45+1/2')


class RowTests(unittest.TestCase):
    def test_integer_plus_fraction(self):
        entry = f.eligible_quantity_row([token('A-BA'), token('45'), half()])
        self.assertEqual((entry['form'], entry['quantity'], entry['fractional']), ('A-BA', Fraction(91, 2), True))

    def test_fraction_only_and_multiple_fractions(self):
        self.assertEqual(f.eligible_quantity_row([token('A-BA'), half()])['quantity'], Fraction(1, 2))
        self.assertEqual(f.eligible_quantity_row([token('A-BA'), token('2'), half(), quarter()])['quantity'], Fraction(11, 4))

    def test_integer_after_fraction_rejected(self):
        self.assertIsNone(f.eligible_quantity_row([token('A-BA'), half(), token('2')]))

    def test_unassigned_or_approximate_fraction_interrupts(self):
        self.assertIsNone(f.eligible_quantity_row([token('A-BA'), token('2'), token('≈ ¹⁄₆', SIXTH)]))
        self.assertIsNone(f.eligible_quantity_row([token('A-BA'), token('\U00010753', '\U00010753')]))

    def test_integer_rule_still_applies(self):
        self.assertIsNone(f.eligible_quantity_row([token('A-BA'), token('6', raw=integer(7))]))
        self.assertIsNone(f.eligible_quantity_row([token('A-BA', '\U00010600' + p.LOSS), token('5')]))
        self.assertIsNone(f.eligible_quantity_row([token('5')]))

    def test_integer_rows_agree_with_phase4(self):
        row = [token('KA'), token('7')]
        self.assertEqual(f.eligible_quantity_row(row)['quantity'], p.eligible_integer_row(row, 'numeric')['quantity'])
        self.assertIsNone(f.eligible_quantity_row(row)['form'])


class SearchTests(unittest.TestCase):
    def test_fractional_sum_recovered(self):
        rows = [[token('A-BA'), token('45'), half()], [token('C-DA'), token('20'), half()],
                [token('E-FA'), token('29')], [token('KU-RO'), token('95')]]
        summary, details = f.arithmetic({'X1': doc(rows)}, 0, 1)
        self.assertEqual(summary['ranking'][0]['form'], 'KU-RO')
        self.assertEqual(details['matches'][0]['terms'], ['45+1/2', '20+1/2', '29'])
        self.assertTrue(details['matches'][0]['fractional'])
        self.assertEqual(summary['eligible_fractional_rows'], 2)

    def test_exact_sum_hidden_by_damage_is_listed_not_scored(self):
        rows = [[token('A-BA'), token('12')], [token('C-DA'), token('12')], [token('E-FA'), token('6')],
                [token('KU-RO', '\U00010600\U00010600' + p.LOSS), token('30', p.LOSS + integer(30))]]
        summary, details = f.arithmetic({'X1': doc(rows)}, 0, 1)
        self.assertEqual(summary['exact_sums_hidden_by_damage'][0]['terms'], ['12', '12', '6'])
        self.assertEqual(summary['ranking'], [])

    def test_seed_and_max_statistic(self):
        rows = [[token('A-BA'), token('2'), half()], [token('C-DA'), token('2'), half()], [token('E-FA'), token('5')]]
        docs = {'X1': doc(rows)}
        one = f.arithmetic(docs, 50, 3)
        self.assertEqual(one, f.arithmetic(docs, 50, 3))
        for row in one[0]['ranking']:
            self.assertGreaterEqual(row['max_statistic_adjusted_p'], row['permutation_p'])

    def test_comparison_lists_unmatched_positions(self):
        rows = [[token('A-BA'), token('2')], [token('C-DA'), token('3')], [token('KU-RO'), token('9')]]
        docs = {'X1': doc(rows)}
        summary, details = f.arithmetic(docs, 0, 1)
        comparison = f.compare(docs, summary, details)
        self.assertEqual(comparison['eligible_positions'], 1)
        self.assertEqual(comparison['unmatched_positions'][0]['sum_of_preceding_block_entries'], '5')
        self.assertEqual(comparison['unmatched_positions'][0]['written'], '9')


@unittest.skipUnless((ROOT / 'data/LinearAInscriptions.js').exists(), 'pinned corpus not downloaded')
class CorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = (ROOT / 'data/LinearAInscriptions.js').read_bytes()
        p.verify_source(raw)
        cls.docs, _ = p.parse_corpus(raw.decode('utf-8'))
        cls.summary, cls.details = f.arithmetic(cls.docs, 0, 20260914)
        cls.comparison = f.compare(cls.docs, cls.summary, cls.details)

    def test_ht104_enters_and_sums(self):
        self.assertEqual(self.comparison['objects_matched_only_with_fractions'], ['HT104'])
        self.assertEqual(self.comparison['objects_lost_with_fractions'], [])
        match = next(m for m in self.details['matches'] if m['document'] == 'HT104')
        self.assertEqual((match['terms'], match['total']), (['45+1/2', '20+1/2', '29'], '95'))

    def test_counts(self):
        self.assertEqual(self.summary['eligible_fractional_rows'], 152)
        self.assertEqual(self.summary['eligible_integer_rows'], 606)
        self.assertEqual(self.comparison['eligible_positions'], 19)
        self.assertEqual(next(r for r in self.summary['ranking'] if r['form'] == 'KU-RO')['matching_objects'], 8)

    def test_known_discrepancies_are_reported_not_repaired(self):
        unmatched = {x['document']: x for x in self.comparison['unmatched_positions']}
        self.assertEqual(unmatched['HT13']['written'], '130+1/2')
        self.assertEqual(unmatched['HT9a']['written'], '31+3/4')
        self.assertEqual(unmatched['HT9a']['sum_of_preceding_block_entries'], '31')

    def test_ht85a_exact_sum_hidden_by_damage(self):
        hidden = self.summary['exact_sums_hidden_by_damage']
        self.assertEqual([(h['document'], h['total']) for h in hidden], [('HT85a', '66')])
        self.assertEqual(hidden[0]['terms'], ['12', '12', '6', '24', '5', '3', '4'])


if __name__ == '__main__':
    unittest.main()
