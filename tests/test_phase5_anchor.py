import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import phase4 as p
import phase5 as q
import phase5_anchor as a

class TailTests(unittest.TestCase):
    def test_exact_sign_boundaries(self):
        forms=['SU-KI-RI-TA','SU-KI-RI-TE-I-JA','TA','TE-I-JA','PA-TA','PA-TA-JA']
        self.assertEqual(a.tail_pairs(forms,['TA'],['TE','I','JA']),
          [{'base':'SU-KI-RI-TA','extended':'SU-KI-RI-TE-I-JA'}])
    def test_not_simple_ja(self):
        self.assertEqual(a.tail_pairs(['SU-KI-RI-TA','SU-KI-RI-TE-I-JA'],['TA'],['TA','JA']),[])
    def test_empty_tail_rejected(self):
        with self.assertRaises(ValueError):a.tail_pairs([],[],['JA'])

@unittest.skipUnless((ROOT/'data/LinearAInscriptions.js').exists(),'pinned corpus required')
class AnchorCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        body=(ROOT/'data/LinearAInscriptions.js').read_bytes();p.verify_source(body)
        d,_=p.parse_corpus(body.decode())
        reviews=q.load_exclusions(d,[ROOT/'data/editorial_reviews.json',ROOT/'data/phase5_reviews.json'])
        cls.result=a.run(d,reviews,json.loads((ROOT/'data/phase5_semantic_anchors.json').read_text()))
    def test_one_attested_alternation(self):
        pairs=self.result['anchors'][0]['exact_tail_replacement_pairs']
        self.assertEqual(pairs,[{'base':'SU-KI-RI-TA','extended':'SU-KI-RI-TE-I-JA'}])
    def test_prediction_not_found(self):
        anchor=self.result['anchors'][0]
        self.assertFalse(anchor['simple_JA_prediction_attested_in_eligible_types'])
        self.assertFalse(anchor['direct_intermediate_attested'])
    def test_source_records(self):
        anchor=self.result['anchors'][0]
        self.assertEqual(anchor['source_occurrences']['SU-KI-RI-TA'][0]['document'],'PHWa32')
        self.assertEqual(anchor['source_occurrences']['SU-KI-RI-TE-I-JA'][0]['document'],'HTZb158b')

if __name__=='__main__':unittest.main()
