"""Fixed-margin checks, including the fitted zero-rate counterexample."""
from collections import Counter
from itertools import combinations
from math import comb, fsum
from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
sys.path.insert(0, str(ROOT))
import affix_controls as fitted
import conditional_affix_controls as c
import phase4 as p
import phase5 as q
import research


def row(result, sign):
    return next(r for r in result['tests'] if r['sign'] == sign)


class ConditionalTests(unittest.TestCase):
    def test_tiny_zero_estimate_is_not_zero_conditional_probability(self):
        forms = ['A-PA-RA', 'PA-RA', 'KI-NA-TE']
        self.assertEqual(row(fitted.attested_remainder_control(forms, 'prefix'), 'A')['p'], 0)
        self.assertEqual(row(c.conditional_control(forms, 'prefix'), 'A')['p'], .5)

    def test_only_one_edge_sign_is_uninformative(self):
        r = row(c.conditional_control(['A-PA-RA', 'A-NA-TE', 'PA-RA'], 'prefix'), 'A')
        self.assertEqual(r['p'], 1)
        self.assertEqual(r['observed_attested'], r['expected_attested'])

    def test_empty_and_short_only_inputs(self):
        self.assertEqual(c.conditional_control([], 'prefix')['tests'], [])
        self.assertEqual(c.conditional_control(['PA-RA'], 'suffix')['tests'], [])

    def test_input_validation(self):
        for args in [([], 'other'), (['A'], 'prefix'), ([], 'prefix', 2)]:
            with self.assertRaises(ValueError):
                c.conditional_control(*args)

    def test_type_deduplication(self):
        forms = ['A-PA-RA', 'PA-RA', 'KI-NA-TE']
        self.assertEqual(c.conditional_control(forms, 'prefix'), c.conditional_control(forms*3, 'prefix'))

    def test_reversing_words_swaps_edges(self):
        forms = ['A-PA-RA', 'PA-RA', 'KI-NA-TE']
        reversed_forms = ['-'.join(reversed(f.split('-'))) for f in forms]
        a, b = c.conditional_control(forms, 'prefix'), c.conditional_control(reversed_forms, 'suffix')
        for sign in ['A', 'KI']:
            for field in ['types', 'observed_attested', 'expected_attested', 'p', 'holm_p']:
                self.assertEqual(row(a, sign)[field], row(b, sign)[field])

    def test_length_strata_are_separate(self):
        forms = ['A-PA-RA', 'PA-RA', 'KI-NA-TE', 'A-PA-RA-NE', 'PA-RA-NE', 'KI-KU-NA-JA']
        r = row(c.conditional_control(forms, 'prefix'), 'A')
        self.assertEqual([s['length'] for s in r['strata']], [3, 4])
        self.assertEqual(r['observed_attested'], 2)
        self.assertGreater(r['p'], 0)

    def test_hypergeom_exhaustive_284_cases(self):
        cases = 0
        for N in range(1, 9):
            for K in range(N+1):
                for n in range(N+1):
                    counts = Counter(sum(i < K for i in sample) for sample in combinations(range(N), n))
                    dist = q.hypergeom_distribution(N, K, n)
                    self.assertAlmostEqual(fsum(dist), 1)
                    for k, prob in enumerate(dist):
                        self.assertAlmostEqual(prob, counts[k]/comb(N, n))
                    cases += 1
        self.assertEqual(cases, 284)

    def test_holm_adjustment_never_smaller(self):
        result = c.conditional_control(['A-PA-RA', 'PA-RA', 'KI-NA-TE', 'SU-NA-TE'], 'prefix')
        self.assertEqual(result['tested_signs'], 3)
        self.assertTrue(all(r['holm_p'] >= r['p'] for r in result['tests']))


@unittest.skipUnless((ROOT/'data/LinearAInscriptions.js').exists(), 'pinned corpus required')
class CorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        body = (ROOT/'data/LinearAInscriptions.js').read_bytes()
        p.verify_source(body)
        docs, _ = p.parse_corpus(body.decode())
        excluded = q.load_exclusions(docs, [ROOT/'data/editorial_reviews.json', ROOT/'data/phase5_reviews.json'])
        cls.result = c.run(docs, excluded)

    def test_scopes_and_pairs_preserved(self):
        for scope, count in [('all', 599), ('tablets', 437)]:
            current = self.result['controls'][scope]['prefix']
            old = self.result['fitted_rate_sensitivity'][scope]['prefix']
            self.assertEqual(current['types'], count)
            self.assertEqual(row(current, 'A')['observed_attested'], 6)
            self.assertEqual({r['extended'] for r in row(current, 'A')['pairs']},
                             {r['extended'] for r in row(old, 'A')['pairs']})

    def test_independent_recheck_values(self):
        a = row(self.result['controls']['all']['prefix'], 'A')
        t = row(self.result['controls']['tablets']['prefix'], 'A')
        self.assertAlmostEqual(a['p'], .15367117586741164, places=12)
        self.assertAlmostEqual(t['p'], .007646839794734983, places=12)
        self.assertAlmostEqual(t['holm_p'], .45881038768409893, places=12)

    def test_fitted_sensitivity_is_preserved(self):
        r = row(self.result['fitted_rate_sensitivity']['tablets']['prefix'], 'A')
        self.assertAlmostEqual(r['p'], .0010451920842132032, places=12)
        self.assertAlmostEqual(r['holm_p'], .06271152505279219, places=12)

    def test_no_corrected_rejections(self):
        for sides in self.result['summary']['scopes'].values():
            for scope in sides.values():
                self.assertEqual(scope['signs_below_0_05_after_holm'], [])

    def test_runner_selects_and_hashes_new_implementation(self):
        self.assertEqual(research.ANALYSES['affixes'][0], 'conditional_affix_controls.py')
        self.assertIn('scripts/conditional_affix_controls.py', research.INPUTS)

    def test_committed_highlights_match(self):
        highlights = json.loads((ROOT/'results/review_highlights.json').read_text())
        self.assertEqual(highlights['affix_summary'], self.result['summary'])


if __name__ == '__main__':
    unittest.main()
