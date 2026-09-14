import itertools
import json
from math import fsum
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import phase4 as p
import phase5 as q

class Distributions(unittest.TestCase):
    def test_convolution(self):
        self.assertEqual(q.convolve([.5,.5],[.5,.5]),[.25,.5,.25])
    def test_degenerate_bernoulli(self):
        self.assertEqual(q.bernoulli_distribution([0,1,1]),[0.,0.,1.])
    def test_bad_probability(self):
        with self.assertRaises(ValueError):q.bernoulli_distribution([1.1])
    def test_hypergeom_enumeration(self):
        counts=[0,0,0]
        for sample in itertools.combinations(range(5),2):counts[sum(x<2 for x in sample)]+=1
        self.assertEqual(q.hypergeom_distribution(5,2,2),[c/10 for c in counts])
    def test_hypergeom_degenerate(self):
        self.assertEqual(q.hypergeom_distribution(0,0,0),[1.])
        self.assertEqual(q.hypergeom_distribution(5,5,2),[0.,0.,1.])
    def test_bad_hypergeom(self):
        with self.assertRaises(ValueError):q.hypergeom_distribution(2,3,1)
    def test_tail(self):
        self.assertEqual(q.upper_tail([.25,.5,.25],2),.25)
        self.assertEqual(q.upper_tail([.25,.5,.25],4),0)
    def test_unknown_vowel(self):
        self.assertEqual(q.vowel_group('*301'),'unassigned:*301')
        self.assertEqual(q.vowel_group('PA3'),'unassigned:PA3')
        self.assertEqual(q.vowel_group('TE'),'E')
    def test_holm(self):
        rows=[dict(sign='A',p=.01),dict(sign='B',p=.04),dict(sign='C',p=.03)]
        q.holm(rows,'p')
        self.assertEqual([r['holm_p'] for r in rows],[.03,.06,.06])
    def test_type_dedup(self):
        self.assertEqual(q.edge_tests(['PA-NA-JA']*4),q.edge_tests(['PA-NA-JA']))
    def test_models_against_tiny_exact_example(self):
        row=next(x for x in q.edge_tests(['PA-NA-JA','KU-TA-JA'])['tests'] if x['sign']=='JA')
        self.assertEqual(row['observed_final_types'],2)
        self.assertAlmostEqual(row['m1_p'],.25)
        self.assertAlmostEqual(row['m2_p'],1/6)
        self.assertAlmostEqual(row['m3_p'],.25)
    def test_vowel_only_pattern_is_conditioned_out(self):
        row=next(x for x in q.edge_tests(['DA-RA-TE','NA-KA-TE'])['tests'] if x['sign']=='TE')
        self.assertAlmostEqual(row['m1_p'],.25)
        self.assertAlmostEqual(row['m2_p'],1.)
        self.assertAlmostEqual(row['m3_p'],1.)
    def test_two_sign_types_have_no_movable_end(self):
        for x in q.edge_tests(['PA-TI','NA-JA'])['tests']:
            self.assertEqual(x['m1_p'],1.)
    def test_single_sign_rejected(self):
        with self.assertRaises(ValueError):q.edge_tests(['TI'])

@unittest.skipUnless((ROOT/'data/LinearAInscriptions.js').exists(),'pinned source required')
class CorpusChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data=(ROOT/'data/LinearAInscriptions.js').read_bytes();p.verify_source(data)
        cls.docs,_=p.parse_corpus(data.decode())
        cls.excluded=q.load_exclusions(cls.docs,[ROOT/'data/editorial_reviews.json',ROOT/'data/phase5_reviews.json'])
        cls.summary,cls.detail=q.run(cls.docs,cls.excluded)
    def test_record_count(self):self.assertEqual(len(self.docs),1721)
    def test_sam_not_independent_pair(self):
        self.assertNotIn('JA-SA',self.detail['scope_forms']['all'])
        self.assertFalse(any(x['base']=='JA-SA' for x in self.detail['suffix_pairs']))
    def test_ti_flag_counts(self):
        self.assertEqual(self.detail['ti']['counts'],{'final:unflagged':33,'final:flagged':16,'standalone:unflagged':4,'standalone:flagged':8})
    def test_ti_three_pairs(self):
        bases={x['base'] for x in self.detail['suffix_pairs'] if x['edge']=='TI'}
        self.assertEqual(bases,{'DA-KU-SE-NE','JA-KU','RI-RU-MA'})
    def test_ja_five_pairs(self):
        self.assertEqual(self.summary['suffix_pair_counts']['JA'],5)
    def test_ht104_exclusion_scope(self):
        forms=self.detail['scope_forms']['tablets_without_HT104']
        for s in ['DA-KU-SE-NE-TI','I-DU-TI','PA-DA-SU-TI']:self.assertNotIn(s,forms)
    def test_all_adjusted_vowel_tests_non_decisive(self):
        rows=self.detail['edge_tests']['all']['tests']
        self.assertTrue(all(x['holm_m2_p']>.05 and x['holm_m3_p']>.05 for x in rows))
    def test_original_damage_retained(self):
        o=next(x for x in self.detail['ti']['occurrences'] if x['document']=='MA2b' and x['form']=='RE-TI')
        self.assertIn('loss_marker',o['flags'])
    def test_alt_reading_not_counted_as_standalone(self):
        o=next(x for x in self.detail['ti']['occurrences'] if x['document']=='PHWc46')
        self.assertIn('editorially_excluded',o['flags'])
    def test_other_category_after_final_ti(self):
        o=next(x for x in self.detail['ti']['occurrences'] if x['document']=='KN1a')
        self.assertEqual(o['intervening_labels_before_quantity'],['E'])
    def test_faces_not_independent_objects(self):
        os={x['object'] for x in self.detail['ti']['occurrences'] if x['document'].startswith('ZA12')}
        self.assertEqual(os,{'ZA12'})

if __name__=='__main__':unittest.main()
