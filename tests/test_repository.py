"""Navigation and topic-interface tests; these do not validate translations."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import research


class NavigationTests(unittest.TestCase):
    def test_local_markdown_targets_exist(self):
        # Current documentation, navigation stubs, and the archive index.
        pages = [ROOT/'README.md', ROOT/'archive/README.md']
        for directory in ('docs', 'hypotheses', 'data', 'results', 'reports'):
            pages += list((ROOT/directory).glob('*.md'))
        checked = 0
        for page in pages:
            text = re.sub(r'```.*?```', '', page.read_text(), flags=re.S)
            for match in re.finditer(r'\[[^\]\n]*\]\(([^\s]+?)(?:\s+"[^"]*")?\)', text):
                target = unquote(match[1])
                parsed = urlsplit(target)
                if parsed.scheme or target.startswith(('#', '//')):
                    continue
                path = (page.parent/parsed.path).resolve()
                with self.subTest(page=str(page.relative_to(ROOT)), target=target):
                    self.assertTrue(path.is_relative_to(ROOT), 'Link escapes repository')
                    self.assertTrue(path.exists(), 'Broken local documentation link')
                checked += 1
        self.assertGreater(checked, 50)

    def test_readme_leads_with_hypotheses_not_phases(self):
        text = (ROOT/'README.md').read_text()
        self.assertIn('hypotheses/adjusted-assessment.md', text)
        self.assertIn('hypotheses/administrative-responsibility.md', text)
        self.assertNotRegex(text.lower(), r'phase\s+[0-9]')

    def test_hypothesis_status_is_explicit(self):
        for name in ('adjusted-assessment.md', 'administrative-responsibility.md'):
            text = (ROOT/'hypotheses'/name).read_text().lower()
            self.assertIn('low-confidence', text)
            self.assertIn('priority', text)


class InterfaceTests(unittest.TestCase):
    def test_outputs_have_unique_descriptive_names(self):
        names = [new for _, mapping in research.ANALYSES.values() for new in mapping.values()]
        self.assertEqual(len(names), 10)
        self.assertEqual(len(set(names)), len(names))
        self.assertFalse(any('phase' in name for name in names))

    def test_unknown_topic_rejected(self):
        with self.assertRaises(ValueError):
            research.run('invalid', Path('none'), Path('none'))

    def test_negative_permutations_rejected(self):
        with self.assertRaises(ValueError):
            research.run('accounting', Path('none'), Path('none'), permutations=-1)

    def test_missing_source_requires_fetch(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError, 'Source missing'):
                research.run('origin', Path(d)/'missing', Path(d)/'out')

    def test_wrong_source_rejected_without_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d)/'source'; source.write_text('invalid corpus')
            with self.assertRaisesRegex(ValueError, 'checksum'):
                research.run('origin', source, Path(d)/'out', fetch=True)
            self.assertEqual(source.read_text(), 'invalid corpus')

    @unittest.skipUnless((ROOT/'data/LinearAInscriptions.js').exists(), 'pinned source required')
    def test_failed_job_does_not_publish_results(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            old = out/'origin_comparison.json'; old.write_text('{"previous": true}')
            failed = subprocess.CompletedProcess([], 1, '', 'test failure')
            with patch.object(research.subprocess, 'run', return_value=failed):
                with self.assertRaisesRegex(RuntimeError, 'test failure'):
                    research.run('origin', ROOT/'data/LinearAInscriptions.js', out)
            self.assertEqual(json.loads(old.read_text()), {'previous': True})
            self.assertFalse((out/'run_manifest.json').exists())

    @unittest.skipUnless((ROOT/'data/LinearAInscriptions.js').exists(), 'pinned source required')
    def test_origin_alias_is_byte_identical(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            result = research.run('origin', ROOT/'data/LinearAInscriptions.js', out/'alias')
            completed = subprocess.run([sys.executable, str(ROOT/'scripts/phase5_anchor.py'),
                '--source', str(ROOT/'data/LinearAInscriptions.js'), '--output', str(out/'legacy')],
                capture_output=True, text=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual((out/'alias/origin_comparison.json').read_bytes(),
                             (out/'legacy/phase5_anchor_results.json').read_bytes())
            self.assertEqual(set(result['output_sha256']), {'origin_comparison.json'})
            self.assertEqual(result['parameters'], {})


if __name__ == '__main__':
    unittest.main()
