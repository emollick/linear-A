"""Exact attested-remainder controls on small cases and corpus regressions."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import phase4 as p
import phase5 as q
import affix_controls as a


class ControlTests(unittest.TestCase):
    def test_exact_small_case(self):
        # A-initial: A-PA-RA (remainder PA-RA attested), A-KU-TE (KU-TE absent).
        # Other three-sign words: KI-PA-RA (PA-RA attested), KI-KU-TE (absent),
        # TA-NA-JA (absent), so the other-sign rate at this length is 1/3.
        forms = ['A-PA-RA', 'A-KU-TE', 'KI-PA-RA', 'KI-KU-TE', 'TA-NA-JA', 'PA-RA']
        result = a.attested_remainder_control(forms, 'prefix')
        row = next(r for r in result['tests'] if r['sign'] == 'A')
        self.assertEqual((row['types'], row['observed_attested']), (2, 1))
        self.assertAlmostEqual(row['expected_attested'], 2 / 3)
        # P(at least one of two Bernoulli(1/3)) = 1 - (2/3)^2
        self.assertAlmostEqual(row['p'], 1 - (2 / 3) ** 2)
        self.assertEqual(row['pairs'], [dict(remainder='PA-RA', extended='A-PA-RA')])
        self.assertEqual(result['types_at_least_min_length'], 5)

    def test_suffix_side_mirrors_prefix_side(self):
        prefix = a.attested_remainder_control(['A-PA-RA', 'PA-RA', 'KI-NA-TE'], 'prefix')
        suffix = a.attested_remainder_control(['RA-PA-A', 'RA-PA', 'TE-NA-KI'], 'suffix')
        rows = lambda r: [(x['sign'], x['observed_attested'], x['expected_attested'], x['p']) for x in r['tests']]
        self.assertEqual(rows(prefix), rows(suffix))

    def test_length_stratification(self):
        # The four-sign A word is compared only with other four-sign words (none attested),
        # not with the three-sign words whose remainders are attested.
        forms = ['A-PA-RA-NE', 'KI-TA-NA-JA', 'KU-TA-NA', 'TA-NA', 'SI-TA-NA', 'PA-RA-NE']
        row = next(r for r in a.attested_remainder_control(forms, 'prefix')['tests'] if r['sign'] == 'A')
        self.assertEqual(row['observed_attested'], 1)
        self.assertEqual(row['expected_attested'], 0.0)

    def test_holm_and_input_validation(self):
        result = a.attested_remainder_control(['A-PA-RA', 'PA-RA', 'KI-NA-TE', 'KA-TA-JA'], 'prefix')
        self.assertTrue(all(r['holm_p'] >= r['p'] for r in result['tests']))
        with self.assertRaises(ValueError):
            a.attested_remainder_control(['A-PA-RA'], 'infix')
        with self.assertRaises(ValueError):
            a.attested_remainder_control(['A'], 'prefix')
        with self.assertRaises(ValueError):
            a.attested_remainder_control(['A-PA-RA'], 'prefix', min_length=2)


@unittest.skipUnless((ROOT / 'data/LinearAInscriptions.js').exists(), 'pinned corpus not downloaded')
class CorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = (ROOT / 'data/LinearAInscriptions.js').read_bytes()
        p.verify_source(raw)
        docs, _ = p.parse_corpus(raw.decode('utf-8'))
        excluded = q.load_exclusions(docs, [ROOT / 'data/editorial_reviews.json',
                                            ROOT / 'data/phase5_reviews.json'])
        cls.summary, cls.results = a.run(docs, excluded)

    def row(self, scope, side, sign):
        return next(r for r in self.results[scope][side]['tests'] if r['sign'] == sign)

    def test_initial_a_all_corpus_is_within_chance(self):
        row = self.row('all', 'prefix', 'A')
        self.assertEqual((row['types'], row['observed_attested']), (66, 6))
        self.assertAlmostEqual(row['expected_attested'], 3.42, places=2)
        self.assertGreater(row['p'], 0.1)
        self.assertEqual({x['remainder'] for x in row['pairs']},
                         {'KA-RU', 'KI-RO', 'PA-RA-NE', 'SA-RA2', 'SI-KI-RA', 'TA-NA-TE'})

    def test_initial_a_tablets_excess_does_not_survive_holm(self):
        row = self.row('tablets', 'prefix', 'A')
        self.assertEqual((row['types'], row['observed_attested']), (41, 6))
        self.assertLess(row['p'], 0.002)
        self.assertGreater(row['holm_p'], 0.05)

    def test_final_ja_pairs_recovered(self):
        row = self.row('all', 'suffix', 'JA')
        self.assertEqual(row['observed_attested'], 5)
        self.assertEqual({x['remainder'] for x in row['pairs']}, {'*306-TU', 'A-MA', 'A-SE', 'KU-PA', 'PA-SE'})

    def test_no_edge_sign_below_threshold_after_holm(self):
        for scope in self.summary['scopes'].values():
            for side in scope.values():
                self.assertEqual(side['signs_below_0_05_after_holm'], [])

    def test_scope_sizes_match_endings_analysis(self):
        self.assertEqual(self.results['all']['prefix']['types'], 599)
        self.assertEqual(self.results['tablets']['prefix']['types'], 437)


if __name__ == '__main__':
    unittest.main()
