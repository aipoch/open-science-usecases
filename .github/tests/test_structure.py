import copy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import runpy
import sys
import tempfile
import threading
import unittest
from urllib.parse import quote, unquote, urlsplit


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_structure.py"
TITLE = "New AI Case—Does It Work"
NAME = "new-ai-case-does-it-work"
URL = "https://example.com/releases/new-case.science"
CHECKER = runpy.run_path(str(SCRIPT))


class AssetHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.server.requests.append((self.command, self.path))
        if self.path in self.server.delays:
            import time
            time.sleep(self.server.delays[self.path])
        default = (200, {"Content-Length": "15"})
        path = unquote(urlsplit(self.path).path)
        if path.startswith("/repository/"):
            file = self.server.root / path[len("/repository/"):]
            default = (200, {"Content-Length": str(file.stat().st_size)}) if file.is_file() else (404, {})
        status, headers = self.server.responses.get(self.path, default)
        self.send_response(status)
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()

    def do_GET(self):
        self.server.requests.append((self.command, self.path))
        self.send_error(405)

    def log_message(self, *args):
        pass


class StructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http = ThreadingHTTPServer(("127.0.0.1", 0), AssetHandler)
        cls.thread = threading.Thread(target=cls.http.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.http.server_port}/case.science"

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown()
        cls.http.server_close()
        cls.thread.join()

    def setUp(self):
        self.http.requests = []
        self.http.responses = {}
        self.http.delays = {}
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.http.root = self.root
        self.git("init", "-q")
        self.git("config", "user.name", "Structure Test")
        self.git("config", "user.email", "structure@example.invalid")
        self.write("manifest.json", "[]")
        self.write("Existing Case/README.md", "Legacy case")
        self.commit()
        self.base = self.git("rev-parse", "HEAD").strip()

    def git(self, *args):
        return subprocess.check_output(
            ["git", *args], cwd=self.root, text=True, stderr=subprocess.STDOUT
        )

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def commit(self):
        self.git("add", ".")
        self.git("-c", "commit.gpgsign=false", "commit", "--allow-empty", "-qm", "test: fixture")

    def case(self, remote=False, cover_extension="png", title=TITLE):
        resources = {}
        for key, extension in (("cover", cover_extension), ("introduction", "md"), ("case", "science")):
            filename = f"{title}.{extension}"
            path = f"usecases/{title}/{filename}"
            content = f"fixture {extension}"
            resources[key] = {
                "file_name": filename,
                "path": path,
                "bytes": len(content.encode()),
                "sha256": "a" * 64,
                "release_url": "",
            }
            if key != "case" or not remote:
                self.write(path, content)
        resources["case"]["release_url"] = self.url if remote else ""
        entry = {"title": title, "name": CHECKER["kebab_case"](title), **resources}
        self.manifest([entry])
        return entry

    def manifest(self, entries):
        self.write("manifest.json", json.dumps(entries, ensure_ascii=False))

    def run_stage(self, stage, *args, cases=None, extra_env=None):
        output = self.root / ".step-output"
        output.write_text("")
        env = {**os.environ, "GITHUB_OUTPUT": str(output), "GITHUB_ACTIONS": "false",
               "CASE_FILE_BASE_URL": f"http://127.0.0.1:{self.http.server_port}/repository"}
        env.pop("CASES_JSON", None)
        if cases is not None:
            env["CASES_JSON"] = json.dumps(cases)
        env.update(extra_env or {})
        result = subprocess.run(
            [sys.executable, str(SCRIPT), stage, *args], cwd=self.root,
            env=env, text=True, capture_output=True,
        )
        values = dict(line.split("=", 1) for line in output.read_text().splitlines())
        return result, values

    def scan(self, **kwargs):
        return self.run_stage("directories", "--base", self.base, **kwargs)

    def check_manifest(self, expected=0):
        scan, values = self.scan()
        if scan.returncode:
            self.assertEqual(scan.returncode, expected, scan.stdout + scan.stderr)
            return scan
        result, _ = self.run_stage("manifest", cases=json.loads(values["cases"]))
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_local_case_uses_stat_and_never_downloads_or_hashes(self):
        entry = self.case()
        self.commit()
        self.check_manifest()
        self.assertEqual(self.http.requests, [])
        # A syntactically valid but deliberately false SHA is admission-valid.
        self.assertEqual(entry['cover']['sha256'], 'a' * 64)

    def test_all_eight_local_remote_combinations(self):
        import itertools
        for flags in itertools.product((False, True), repeat=3):
            with self.subTest(flags=flags):
                entry = self.case()
                self.http.requests = []
                for kind, remote in zip(('cover', 'case', 'introduction'), flags):
                    resource = entry[kind]
                    if remote:
                        resource['release_url'] = self.url + '?kind=' + kind
                        self.http.responses['/case.science?kind=' + kind] = (200, {'Content-Length': str(resource['bytes'])})
                        (self.root / resource['path']).unlink()
                if all(flags):
                    import shutil
                    shutil.rmtree(self.root / 'usecases')
                self.manifest([entry]); self.commit()
                self.check_manifest()
                self.assertEqual(len(self.http.requests), sum(flags))
                self.assertTrue(all(method == 'HEAD' for method, _ in self.http.requests))

    def test_cover_extensions_and_independent_directory_title_name(self):
        for extension in ('png', 'jpg', 'JPEG', 'webp', 'gif', 'svg', 'avif', 'bmp', 'tiff', 'ico'):
            entry = self.case(cover_extension=extension, title='NVDA: Why?')
            entry.update(name='independent-name', title='Display only')
            self.manifest([entry]); self.commit(); self.check_manifest()
        for extension in ('txt', 'pdf', 'mp4', 'unknown', 'png.gz'):
            self.case(cover_extension=extension); self.commit(); self.check_manifest(expected=1)

    def test_schema_fields_and_safe_paths(self):
        original = self.case()
        for kind in ('cover', 'case', 'introduction'):
            for field, value in [('bytes', True), ('bytes', -1), ('bytes', '8'), ('file_name', None),
                                 ('path', '../escape'), ('path', '/absolute/file.md'), ('path', 'usecases/a/../x.md'),
                                 ('path', 'usecases//x.md'), ('path', 'usecases/a/x\\x.md'),
                                 ('path', 'usecases/a/x\n.md'), ('path', 'Old/x.md'),
                                 ('sha256', None), ('sha256', 'g'*64), ('sha256', 'a'*63),
                                 ('sha256', 'a'*65), ('sha256', 'a'*64+' '),
                                 ('release_url', None), ('release_url', ' '), ('release_url', 0),
                                 ('release_url', 'file:///tmp/a.science')]:
                with self.subTest(kind=kind, field=field, value=value):
                    entry = copy.deepcopy(original); entry[kind][field] = value
                    self.manifest([entry]); self.commit(); self.check_manifest(expected=1)
            for field in original[kind]:
                entry = copy.deepcopy(original); del entry[kind][field]
                self.manifest([entry]); self.commit(); self.check_manifest(expected=1)
        for field, value in [('name', 'Bad Name'), ('name', None), ('title', ''), ('title', 1), ('cover', [])]:
            entry = copy.deepcopy(original); entry[field] = value
            self.manifest([entry]); self.commit(); self.check_manifest(expected=1)
        entry = copy.deepcopy(original); entry['extra'] = 1
        self.manifest([entry]); self.commit(); self.check_manifest(expected=1)

    def test_missing_resource_and_entry_fields(self):
        original = self.case()
        for field in original:
            entry = copy.deepcopy(original); del entry[field]
            self.manifest([entry]); self.commit(); self.check_manifest(expected=1)

    def test_duplicate_names_including_unchanged_entries(self):
        entry = self.case(); self.commit(); self.base = self.git('rev-parse', 'HEAD').strip()
        second = copy.deepcopy(entry); second['title'] = 'Alias'
        self.manifest([entry, second]); self.commit(); self.check_manifest(expected=1)

    def test_local_size_and_symlinks(self):
        entry = self.case()
        for kind in ('cover', 'case', 'introduction'):
            path = self.root / entry[kind]['path']; data = path.read_bytes()
            path.write_bytes(b'wrong'); self.commit(); self.check_manifest(expected=1)
            path.unlink(); path.symlink_to('../../manifest.json'); self.commit(); self.check_manifest(expected=1)
            path.unlink(); path.write_bytes(data)
        self.commit(); self.check_manifest()
        directory = self.root / 'usecases' / TITLE
        directory.rename(self.root / 'outside')
        directory.symlink_to(self.root / 'outside', target_is_directory=True)
        self.commit(); self.check_manifest(expected=1)

    def test_package_requires_exactly_one_source_for_mixed_local_case(self):
        entry = self.case(); entry['case']['release_url'] = self.url
        self.manifest([entry]); self.commit(); self.check_manifest(expected=1)
        (self.root / entry['case']['path']).unlink()
        self.commit(); self.check_manifest()
        entry['case']['release_url'] = ''
        self.manifest([entry]); self.commit(); self.check_manifest(expected=1)

    def test_remote_head_redirects_keep_method(self):
        for code in (301, 302, 303, 307, 308):
            entry = self.case(remote=True)
            self.http.requests = []
            self.http.responses['/case.science'] = (code, {'Location': '/redirected.science'})
            self.manifest([entry]); self.commit(); self.check_manifest()
            self.assertEqual(self.http.requests, [('HEAD', '/case.science'), ('HEAD', '/redirected.science')])

    def test_remote_head_failures_no_get_fallback(self):
        for status, headers in [(404, {}), (403, {}), (500, {}), (405, {}), (501, {}),
                                (200, {}), (200, {'Content-Length': 'bad'}),
                                (200, {'Content-Length': '99'}), (206, {'Content-Length': '15'})]:
            entry = self.case(remote=True); self.http.requests = []
            self.http.responses['/case.science'] = (status, headers)
            self.manifest([entry]); self.commit(); self.check_manifest(expected=1)
            self.assertEqual(self.http.requests, [('HEAD', '/case.science')])

    def test_remote_head_timeout_and_unreachable(self):
        from unittest.mock import patch
        from urllib.error import URLError
        errors = []
        with patch.dict(CHECKER['validate_head_size'].__globals__, build_opener=lambda *a: type('Opener', (), {
                'open': lambda *a, **kw: (_ for _ in ()).throw(URLError(TimeoutError('timed out')))})()):
            CHECKER['validate_head_size'](self.url, 15, 'fixture', errors, timeout=0.01)
        self.assertIn('timeout', errors[0])
        errors = []
        CHECKER['validate_head_size']('http://127.0.0.1:1/a.science', 15, 'fixture', errors, timeout=0.01)
        self.assertTrue(errors)

    def test_real_http_timeout_never_falls_back_to_get(self):
        self.http.delays['/slow.science'] = 0.1
        errors = []
        CHECKER['validate_head_size'](self.url.replace('/case.science', '/slow.science'),
                                     15, 'slow fixture', errors, timeout=0.01)
        self.assertTrue(errors)
        self.assertIn('timed out', errors[0])
        self.assertEqual(self.http.requests, [('HEAD', '/slow.science')])

    def test_science_urls_and_other_resource_urls(self):
        for url in (self.url, self.url+'?download=1', self.url+'#file'):
            self.assertTrue(CHECKER['is_science_url'](url))
        for url in ('', ' ', 'file:///x.science', 'https://example.com/readme',
                    'http://[not-ip]/a.science', 'https://host:99999/a.science', 'https://host/a.science\n'):
            self.assertFalse(CHECKER['is_science_url'](url))
        self.assertTrue(CHECKER['is_resource_url']('https://example.com/download?id=1', 'cover'))

    def test_unchanged_manifest_file_changes_and_unlisted_directories_are_ignored(self):
        entry = self.case(); self.commit(); self.base = self.git('rev-parse', 'HEAD').strip()
        (self.root / entry['cover']['path']).unlink()
        self.write('Unlisted/a.science', 'ignored'); self.commit()
        result, values = self.scan()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(values['cases']), [])

    def test_manifest_only_edit_rechecks_affected_entry_only(self):
        entry = self.case(); self.commit(); self.base = self.git('rev-parse', 'HEAD').strip()
        other = self.case(title='Other')
        entry['title'] = 'Changed title'
        self.manifest([entry, other]); self.commit(); self.base = self.git('rev-parse', 'HEAD').strip()
        (self.root / other['cover']['path']).unlink()
        entry['title'] = 'Changed again'
        self.manifest([entry, other]); self.commit(); self.check_manifest()
        (self.root / entry['cover']['path']).unlink(); self.commit(); self.check_manifest(expected=1)

    def test_order_format_and_deletion_do_not_select_entries(self):
        first = self.case(); second = self.case(title='Other')
        self.manifest([first, second]); self.commit(); self.base = self.git('rev-parse', 'HEAD').strip()
        for entries in ([second, first], [first], []):
            self.write('manifest.json', json.dumps(entries, indent=4)); self.commit()
            result, values = self.scan()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(values['cases']), [])

    def test_name_and_path_changes_select_entry(self):
        entry = self.case(); self.commit(); self.base = self.git('rev-parse', 'HEAD').strip()
        entry['name'] = 'new-prefix'
        self.manifest([entry]); self.commit(); self.check_manifest()
        self.git('mv', 'usecases/'+TITLE, 'usecases/Renamed')
        for kind in ('cover', 'case', 'introduction'):
            entry[kind]['path'] = entry[kind]['path'].replace('usecases/'+TITLE+'/', 'usecases/Renamed/')
        self.manifest([entry]); self.commit(); self.check_manifest()

    def test_missing_manifest_and_invalid_git_base_fail(self):
        result, _ = self.run_stage('directories', '--base', 'missing-ref')
        self.assertNotEqual(result.returncode, 0)
        self.case(); self.git('mv', 'manifest.json', 'renamed.json'); self.commit()
        result, _ = self.scan(); self.assertNotEqual(result.returncode, 0)

    def test_json_and_workflow_input_errors_are_actionable(self):
        for content in ('{', '{}', '[1]', '[{"name":"one","name":"two"}]'):
            self.write('manifest.json', content); self.commit()
            result, _ = self.scan(); self.assertNotEqual(result.returncode, 0)
            self.assertNotIn('Traceback', result.stderr)
        result, _ = self.run_stage('manifest')
        self.assertNotEqual(result.returncode, 0); self.assertIn('CASES_JSON', result.stderr)
        result, _ = self.run_stage('manifest', cases=[{}])
        self.assertNotEqual(result.returncode, 0)

    def test_initial_push_and_common_ancestor_selection(self):
        self.case(); self.commit()
        result, values = self.run_stage('directories', '--base', '0'*40)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(values['cases'])), 1)
        result, values = self.run_stage('directories', '--base', '0'*40, '--new-branch-base', 'HEAD')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(values['cases']), [])
        result, values = self.run_stage('directories', '--base', self.base, '--merge-base')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(values['cases'])), 1)

    def test_boolean_metadata_change_not_equal_to_integer(self):
        entry = self.case(); entry['cover']['bytes'] = 1
        self.manifest([entry]); self.commit(); self.base = self.git('rev-parse', 'HEAD').strip()
        entry['cover']['bytes'] = True
        self.manifest([entry]); self.commit(); self.check_manifest(expected=1)

    def test_actions_annotations_escape_control_sequences(self):
        entry = self.case(title='Title##[error]unsafe')
        entry['cover']['sha256'] = 'bad'
        self.manifest([entry]); self.commit()
        scan, values = self.scan()
        self.assertNotIn('##[error]', scan.stdout)
        result, _ = self.run_stage('manifest', cases=json.loads(values['cases']), extra_env={'GITHUB_ACTIONS':'true'})
        self.assertIn('::error title=', result.stderr)
        self.assertIn('::endgroup::', result.stderr)
