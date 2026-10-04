"""Regression checks for publish boundaries and incomplete content; no network."""
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location('check_site', Path(__file__).with_name('check_site.py'))
CHECK = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(CHECK)

class ReleaseChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.previous = CHECK.ROOT, CHECK.PUBLIC
        CHECK.ROOT, CHECK.PUBLIC = self.root, self.root / 'site'
        (CHECK.PUBLIC / 'assets').mkdir(parents=True)
        (CHECK.PUBLIC / 'assets/social.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>', encoding='utf-8')
        (CHECK.PUBLIC / 'assets/manifest.json').write_text(json.dumps({'assets': [{'path': 'assets/social.svg', 'public_approved': True}]}))
        (self.root / 'release.json').write_text(json.dumps({'title': 'Test project', 'site_url': 'https://example.org/project/', 'repository': 'example/project', 'branch': 'main', 'content_ready': True}))
        self.html = '<html><head><title>Test project</title><meta name="description" content="Test description"><meta property="og:title" content="Test project"><meta name="twitter:title" content="Test project"><meta property="og:url" content="https://example.org/project/"><link rel="canonical" href="https://example.org/project/"><meta property="og:image" content="https://example.org/project/assets/social.svg"><meta name="twitter:image" content="https://example.org/project/assets/social.svg"></head><body><h1>Test project</h1><p id="main">Text</p><a href="#main">Main</a><img src="assets/social.svg" alt="Test figure"></body></html>'
        self.write_html(self.html)
    def tearDown(self):
        CHECK.ROOT, CHECK.PUBLIC = self.previous
        self.temp.cleanup()
    def write_html(self, text): (CHECK.PUBLIC / 'index.html').write_text(text, encoding='utf-8')
    def errors(self): return CHECK.inspect(True)[0]
    def test_complete_site_passes(self): self.assertEqual(self.errors(), [])
    def test_placeholder_fails_only_release(self):
        self.write_html(self.html.replace('Text', '{{PENDING}}'))
        self.assertEqual(CHECK.inspect(False)[0], [])
        self.assertTrue(any('Unresolved' in x for x in self.errors()))
    def test_missing_and_wrong_case_assets(self):
        self.write_html(self.html.replace('src="assets/social.svg"', 'src="assets/SOCIAL.svg"'))
        self.assertTrue(any('Missing file' in x or 'case mismatch' in x for x in self.errors()))
    def test_root_relative_url_rejected(self):
        self.write_html(self.html.replace('src="assets/social.svg"', 'src="/assets/social.svg"'))
        self.assertTrue(any('project-relative' in x for x in self.errors()))
    def test_private_reference_rejected(self):
        self.write_html(self.html.replace('href="#main"', 'href="../materials/private.pdf"'))
        self.assertTrue(any('escapes' in x for x in self.errors()))
    def test_unapproved_media_rejected(self):
        path = CHECK.PUBLIC / 'assets/manifest.json'
        path.write_text(path.read_text().replace('true', 'false'))
        self.assertTrue(any('not marked' in x for x in self.errors()))
    def test_unregistered_pdf_rejected(self):
        (CHECK.PUBLIC / 'draft.pdf').write_bytes(b'%PDF fixture')
        self.assertTrue(any('not in public asset manifest' in x for x in self.errors()))
    def test_duplicate_id_and_broken_anchor(self):
        self.write_html(self.html.replace('Text', '<span id="main">Text</span>').replace('href="#main"', 'href="#missing"'))
        errors = self.errors()
        self.assertTrue(any('duplicate IDs' in x for x in errors))
        self.assertTrue(any('Broken anchor' in x for x in errors))
    @unittest.skipUnless(shutil.which('git'), 'Git is not installed')
    def test_tracked_private_file_rejected(self):
        subprocess.run(['git', 'init', '-q', '-b', 'main'], cwd=self.root, check=True)
        (self.root / 'materials').mkdir(); (self.root / 'materials/private.txt').write_text('private fixture')
        subprocess.run(['git', 'add', 'materials/private.txt'], cwd=self.root, check=True)
        self.assertTrue(any('Private file is tracked' in x for x in self.errors()))
    @unittest.skipUnless(shutil.which('git'), 'Git is not installed')
    def test_parent_repository_rejected(self):
        parent = self.root / 'parent'; child = parent / 'project_page'; child.mkdir(parents=True)
        subprocess.run(['git', 'init', '-q', '-b', 'main'], cwd=parent, check=True)
        (child / 'scripts').mkdir()
        source = Path(__file__).with_name('init_repository.py')
        shutil.copyfile(source, child / 'scripts/init_repository.py')
        import sys
        result = subprocess.run([sys.executable, 'scripts/init_repository.py'], cwd=child, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((child / '.git').exists())

if __name__ == '__main__': unittest.main()
