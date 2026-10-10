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
        self.git("-c", "commit.gpgsign=false", "commit", "-qm", "test: fixture")

    def case(self, remote=False, cover_extension="png", title=TITLE):
        resources = {}
        for key, extension in (("cover", cover_extension), ("introduction", "md"), ("case", "science")):
            filename = f"{title}.{extension}"
            path = f"{title}/{filename}"
            content = f"fixture {extension}"
            resources[key] = {
                "file_name": filename,
                "path": path,
                "bytes": len(content.encode()),
                "sha256": "a" * 64,
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

    def test_local_case_passes_both_stages_and_exports_state(self):
        self.case()
        self.commit()
        result, values = self.scan()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(values["cases"]), [{
            "directory": TITLE, "name": NAME, "valid": True,
            "has_local_science": True,
        }])
        self.check_manifest()

    # Exercise the actual directory and manifest commands for each image format.
    def test_cover_with_url_punctuation_passes_both_stages(self):
        self.case(title="NVDA: ALL AT ONCE OR FOUR WEEKS?")
        self.commit()
        self.check_manifest()
        self.assertIn(("HEAD", "/repository/NVDA%3A%20ALL%20AT%20ONCE%20OR%20FOUR%20WEEKS%3F/"
                              "NVDA%3A%20ALL%20AT%20ONCE%20OR%20FOUR%20WEEKS%3F.png"),
                      self.http.requests)
        self.assertTrue(all(method == "HEAD" for method, _ in self.http.requests))

    def test_image_covers_pass_both_stages_using_declared_path(self):
        for extension in ("png", "jpg", "JPEG", "webp", "gif", "svg", "avif", "bmp", "tiff", "ico"):
            with self.subTest(extension=extension):
                entry = self.case(cover_extension=extension)
                self.commit()
                self.http.requests = []
                self.check_manifest()
                self.assertIn(("HEAD", "/repository/" + quote(entry["cover"]["path"])),
                              self.http.requests)
                self.assertTrue(all(method == "HEAD" for method, _ in self.http.requests))
                (self.root / entry["cover"]["path"]).unlink()

    def test_nonimage_cover_is_rejected_even_with_an_unlisted_png(self):
        for extension in ("txt", "pdf", "mp4", "unknown", "png.gz"):
            with self.subTest(extension=extension):
                self.case(cover_extension=extension)
                self.write(f"{TITLE}/{TITLE}.png", "unlisted image")
                self.commit()
                result = self.check_manifest(expected=1)
                self.assertIn("image", result.stderr)

    def test_all_repository_resources_use_head_without_recomputing_checksums(self):
        entry = self.case()
        self.commit()
        self.check_manifest()
        expected = [("HEAD", "/repository/" + quote(entry[key]["path"]))
                    for key in ("cover", "case", "introduction")]
        self.assertEqual(self.http.requests, expected)

    def test_resource_checksums_must_be_64_hexadecimal_characters(self):
        entry = self.case(remote=True)
        self.commit()
        for key in ("cover", "case", "introduction"):
            for checksum in (None, False, 123, {}, [], "", " ", "a" * 63,
                             "a" * 65, "g" * 64, "a" * 63 + "é",
                             "a" * 64 + "\n", " " + "a" * 64):
                with self.subTest(key=key, checksum=checksum):
                    changed = copy.deepcopy(entry)
                    changed[key]["sha256"] = checksum
                    self.manifest([changed])
                    result = self.check_manifest(expected=1)
                    self.assertIn(key, result.stderr)
                    self.assertIn("sha256", result.stderr)
                    self.assertIn("64", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)

    def test_uppercase_and_mixed_case_checksums_are_valid(self):
        entry = self.case(remote=True)
        entry["cover"]["sha256"] = "ABCDEF0123456789" * 4
        entry["case"]["sha256"] = "aBcDeF0123456789" * 4
        self.manifest([entry]); self.commit()
        self.check_manifest()
        self.assertTrue(all(method == "HEAD" for method, _ in self.http.requests))

    def test_remote_resource_checksum_is_required(self):
        entry = self.case(remote=True)
        del entry["case"]["sha256"]
        self.manifest([entry]); self.commit()
        result = self.check_manifest(expected=1)
        self.assertIn("missing fields: sha256", result.stderr)

    def test_repository_size_is_checked_against_head_not_local_stat(self):
        entry = self.case()
        path = "/repository/" + quote(entry["cover"]["path"])
        self.http.responses[path] = (200, {"Content-Length": "123456"})
        self.commit()
        result = self.check_manifest(expected=1)
        self.assertIn("HEAD reports 123456", result.stderr)

    def test_declaration_stage_rejects_legacy_optional_sha_on_new_cases(self):
        entry = self.case()
        del entry["cover"]["sha256"]
        self.manifest([entry]); self.commit()
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "declarations", "--base", self.base,
             "--after", self.git("rev-parse", "HEAD").strip()], cwd=self.root,
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("64-digit", result.stderr)

    def test_checked_cases_publish_with_valid_checksums(self):
        publisher = SCRIPT.with_name("publish.py")
        fake = self.root / 'bin'; fake.mkdir()
        aws = fake / 'aws'
        aws.write_text('#!' + sys.executable + '\n' + Path(__file__).with_name('fake_s3.py').read_text())
        aws.chmod(0o755)
        s3 = self.root / 's3'; s3.mkdir()
        for remote in (False, True):
            with self.subTest(remote=remote):
                entry = self.case(remote=remote)
                if remote:
                    (self.root / entry["case"]["path"]).unlink(missing_ok=True)
                self.manifest([entry]); self.commit()
                self.check_manifest()
                result = subprocess.run(
                    [sys.executable, str(publisher), "--dry-run",
                     "--after", self.git("rev-parse", "HEAD").strip()], cwd=self.root,
                    env={**os.environ, "AWS_TARGET_FOLDER": "s3://test-bucket/cases",
                         "PATH": str(fake) + os.pathsep + os.environ['PATH'], "FAKE_S3_ROOT": str(s3)},
                    text=True, capture_output=True,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("Prepared {} files".format(3 if remote else 4), result.stdout)
                self.assertTrue(all(method == "HEAD" for method, _ in self.http.requests))

    def test_science_source_requires_exactly_one_local_file_or_release_url(self):
        for local, release, expected, detail in (
            (True, False, 0, ""), (False, True, 0, ""),
            (True, True, 1, "both"), (False, False, 1, "neither"),
        ):
            with self.subTest(local=local, release=release):
                entry = self.case(remote=not local)
                if not local:
                    (self.root / entry["case"]["path"]).unlink(missing_ok=True)
                entry["case"]["release_url"] = self.url if release else ""
                self.manifest([entry]); self.commit()
                result = self.check_manifest(expected=expected)
                if detail:
                    self.assertIn(detail, result.stderr)

    def test_remote_case_without_readme_passes_using_manifest_url(self):
        self.case(remote=True)
        self.commit()
        result, values = self.scan()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(json.loads(values["cases"])[0]["has_local_science"])
        self.check_manifest()

    def test_unrelated_root_files_and_hidden_tooling_are_skipped(self):
        self.write("README.md", "updated")
        self.write(".github/workflows/check.yml", "name: test")
        self.commit()
        result, values = self.scan()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(values["cases"]), [])
        self.check_manifest()

    def test_required_files_cannot_be_replaced_by_readme_or_wrong_names(self):
        self.case()
        self.commit()
        for extension in ("md", "png"):
            path = self.root / TITLE / f"{TITLE}.{extension}"
            renamed = path.with_name(f"wrong.{extension}")
            path.rename(renamed)
            with self.subTest(extension=extension):
                result, values = self.scan()
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertFalse(json.loads(values["cases"])[0]["valid"])
            renamed.rename(path)

    def test_remote_readme_is_not_read_or_used_for_validation(self):
        self.case(remote=True)
        self.commit()
        for content in (b"no download", b"[Download](https://example.com/other.science)", b"\xff"):
            with self.subTest(content=content):
                (self.root / TITLE / "README.md").write_bytes(content)
                self.check_manifest()

    def test_remote_manifest_url_accepts_science_paths_with_query_or_fragment(self):
        for url in (URL, "http://example.com/other.science", "https://[::1]/case.science",
                    "https://example.com:443/case.science", URL + "?download=1#asset",
                    URL + "?token=abc!", URL + "#asset;"):
            with self.subTest(url=url):
                self.assertTrue(CHECKER["is_science_url"](url))

    def test_remote_head_checks_size_without_recomputing_sha256_or_get(self):
        entry = self.case(remote=True)
        entry["case"]["release_url"] += "?download=1#asset"
        self.manifest([entry]); self.commit()
        self.check_manifest()
        self.assertIn(("HEAD", "/case.science?download=1"), self.http.requests)
        self.assertTrue(all(method == "HEAD" for method, _ in self.http.requests))

    def test_remote_head_redirects_never_switch_to_get(self):
        self.case(remote=True); self.commit()
        for status in (301, 302, 303, 307, 308):
            with self.subTest(status=status):
                self.http.requests = []
                self.http.responses = {"/case.science": (status, {"Location": "/asset"})}
                self.check_manifest()
                remote_requests = [(method, path) for method, path in self.http.requests
                                   if not path.startswith("/repository/")]
                self.assertEqual(remote_requests, [("HEAD", "/case.science"), ("HEAD", "/asset")])
                self.assertTrue(all(method == "HEAD" for method, _ in self.http.requests))

    def test_remote_head_failures_explain_how_to_fix_the_url_or_size(self):
        self.case(remote=True); self.commit()
        for status, headers, detail in (
            (404, {}, "404"), (405, {}, "405"),
            (204, {}, "204"), (206, {"Content-Length": "15"}, "206"),
            (302, {"Location": "/case.science"}, "302"),
            (302, {"Location": "ftp://127.0.0.1/asset.science"}, "HTTP(S)"),
            (200, {}, "Content-Length"),
            (200, {"Content-Length": "invalid"}, "Content-Length"),
            (200, {"Content-Length": "-1"}, "Content-Length"),
            (200, {"Content-Length": "123"}, "123"),
        ):
            with self.subTest(status=status, headers=headers):
                self.http.responses = {"/case.science": (status, headers)}
                result = self.check_manifest(expected=1)
                self.assertIn(detail, result.stderr)
                self.assertIn("HEAD", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_remote_head_timeout_is_an_actionable_error(self):
        # Bind a real server without serving responses to force a read timeout.
        with ThreadingHTTPServer(("127.0.0.1", 0), AssetHandler) as server:
            errors = []
            CHECKER["validate_head_size"](
                f"http://127.0.0.1:{server.server_port}/case.science", 15, "case", errors,
                timeout=0.05)
        self.assertEqual(len(errors), 1)
        self.assertIn("HEAD could not finish", errors[0])
        self.assertIn("timeout", errors[0])
        self.assertIn("rerun", errors[0])

    def test_missing_duplicate_or_wrong_manifest_name_fails(self):
        entry = self.case()
        self.commit()
        for entries in ([entry, entry], [{**entry, "name": "wrong-name"}]):
            with self.subTest(entries=entries):
                self.manifest(entries)
                self.check_manifest(expected=1)

    def test_manifest_keys_types_paths_and_sizes_are_checked(self):
        entry = self.case()
        self.commit()
        mutations = [
            ((), "title", "Wrong title"), ((), "introduction", None),
            ((), "unexpected", True), (("cover",), "file_name", "wrong.png"),
            (("cover",), "path", "../outside.png"), (("case",), "bytes", True),
            (("case",), "bytes", -1), (("case",), "bytes", "15"),
            (("cover",), "bytes", 999), (("case",), "release_url", URL),
        ]
        for parents, key, value in mutations:
            with self.subTest(parents=parents, key=key, value=value):
                changed = copy.deepcopy(entry)
                target = changed
                for parent in parents:
                    target = target[parent]
                target[key] = value
                self.manifest([changed])
                self.check_manifest(expected=1)

    def test_missing_keys_fail_at_each_level(self):
        entry = self.case()
        self.commit()
        for parent in (None, "cover", "case", "introduction"):
            target = entry if parent is None else entry[parent]
            for key in target:
                with self.subTest(parent=parent, key=key):
                    changed = copy.deepcopy(entry)
                    del (changed if parent is None else changed[parent])[key]
                    self.manifest([changed])
                    self.check_manifest(expected=1)

    def test_remote_release_url_must_be_a_nonempty_science_url(self):
        entry = self.case(remote=True)
        self.commit()
        for url in ("", None, 12, False, [], {}, " ", "file.science",
                    "https://example.com/file.zip", "https://example.com/page?file=.science",
                    "https://example.com/file.science/", "ftp://example.com/file.science",
                    "https:///file.science", "https://[invalid]/file.science",
                    "https://example.com:not-a-port/file.science", "https://example.com:99999/file.science",
                    "https://example.com/file.science\n", "https://exa mple.com/file.science"):
            with self.subTest(url=url):
                entry["case"]["release_url"] = url
                self.manifest([entry])
                result = self.check_manifest(expected=1)
                self.assertIn("release_url", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_readme_cannot_replace_missing_manifest_release_url(self):
        entry = self.case(remote=True)
        del entry["case"]["release_url"]
        self.manifest([entry])
        self.write(f"{TITLE}/README.md", f"[Download]({URL})")
        self.commit()
        self.check_manifest(expected=1)

    def test_wrongly_named_science_file_still_requires_release_url(self):
        self.case()
        (self.root / TITLE / f"{TITLE}.science").rename(self.root / TITLE / "wrong.science")
        self.commit()
        self.check_manifest(expected=1)

    def test_malformed_manifest_fails_cleanly(self):
        self.case()
        self.commit()
        for content in ("{", "{}", "[null]", '[{"name": "x", "name": "y"}]'):
            with self.subTest(content=content):
                self.write("manifest.json", content)
                result, _ = self.scan()
                self.assertEqual(result.returncode, 1)
                self.assertNotIn("Traceback", result.stderr)

    def test_invalid_base_fails_instead_of_silently_skipping(self):
        result, _ = self.run_stage("directories", "--base", "nonexistent-ref")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("nonexistent-ref", result.stderr)
        self.assertIn("fetch-depth: 0", result.stderr)

    def test_missing_file_log_identifies_case_and_tells_how_to_fix_it(self):
        self.case()
        (self.root / TITLE / f"{TITLE}.png").unlink()
        self.commit()
        result, _ = self.scan()
        self.assertEqual(result.returncode, 1)
        self.assertIn(f"{TITLE}/{TITLE}.png", result.stderr)
        self.assertIn("Add", result.stderr)
        self.assertIn("same name", result.stderr)

    def test_metadata_log_shows_current_values_and_replacements(self):
        entry = self.case()
        entry["cover"]["bytes"] = 12345
        entry["cover"]["sha256"] = "0" * 64
        self.manifest([entry])
        self.commit()
        result = self.check_manifest(expected=1)
        self.assertIn("12345", result.stderr)
        self.assertIn(str(len(b"fixture png")), result.stderr)
        self.assertNotIn("0" * 64, result.stderr)
        self.assertIn("Update", result.stderr)
        self.assertIn("1 problem", result.stderr)

    def test_manifest_json_error_includes_location_and_fix(self):
        self.case()
        self.commit()
        self.write("manifest.json", '[\n{"name": }\n]')
        result, _ = self.scan()
        self.assertEqual(result.returncode, 1)
        self.assertIn("manifest.json", result.stderr)
        self.assertIn("line 2", result.stderr)
        self.assertIn("column", result.stderr)
        self.assertIn("JSON", result.stderr)

    def test_workflow_input_errors_explain_step_wiring(self):
        for extra in ({}, {"CASES_JSON": "{"}, {"CASES_JSON": "[null]"},
                      {"CASES_JSON": '[{"directory": "New Case"}]'}):
            with self.subTest(extra=extra):
                result, _ = self.run_stage("manifest", extra_env=extra)
                self.assertEqual(result.returncode, 1)
                self.assertIn("CASES_JSON", result.stderr)
                self.assertIn("directories", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_actions_error_annotations_are_escaped_and_group_is_closed(self):
        entry = self.case()
        entry["cover"]["path"] = "wrong%0A\n::warning::injected"
        self.manifest([entry])
        self.commit()
        scan, values = self.scan()
        self.assertEqual(scan.returncode, 0)
        result, _ = self.run_stage("manifest", cases=json.loads(values["cases"]),
                                   extra_env={"GITHUB_ACTIONS": "true"})
        self.assertEqual(result.returncode, 1)
        self.assertIn("::group::", result.stderr)
        annotations = [line for line in result.stderr.splitlines() if line.startswith("::error")]
        self.assertEqual(len(annotations), 1)
        self.assertIn("%250A", annotations[0])
        self.assertNotIn("\n::warning::injected", result.stderr)
        self.assertTrue(result.stderr.rstrip().endswith("::endgroup::"))

    def test_no_new_cases_explains_skip_and_stdout_stays_json(self):
        result, _ = self.scan()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), [])
        self.assertIn("No relevant case changes", result.stderr)

    def test_directory_names_cannot_inject_legacy_actions_commands(self):
        directory = "Case ##[error]injected ##[endgroup]"
        for extension in ("md", "png", "science"):
            self.write(f"{directory}/{directory}.{extension}", "fixture")
        self.manifest([{"title": directory, "name": CHECKER["kebab_case"](directory)}])
        self.commit()
        result, values = self.scan(extra_env={"GITHUB_ACTIONS": "true"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("##[", result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)[0]["directory"], directory)
        self.assertEqual(json.loads(values["cases"])[0]["directory"], directory)
        self.assertEqual(result.stderr.count("::endgroup::"), 1)

    def test_initial_repository_push_checks_only_declared_directories(self):
        self.case()
        self.commit()
        result, values = self.run_stage("directories", "--base", "0" * 40)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual([case["directory"] for case in json.loads(values["cases"])],
                         [TITLE])

    def test_first_feature_branch_push_does_not_recheck_legacy_cases(self):
        self.case()
        self.commit()
        result, values = self.run_stage(
            "directories", "--base", "0" * 40, "--new-branch-base", self.base)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual([case["directory"] for case in json.loads(values["cases"])], [TITLE])

    def test_first_feature_branch_push_without_new_cases_passes(self):
        result, values = self.run_stage(
            "directories", "--base", "0" * 40, "--new-branch-base", self.base)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(values["cases"]), [])

    def test_pr_uses_common_ancestor_when_base_branch_diverged(self):
        self.git("checkout", "-qb", "base-branch")
        self.case()
        self.commit()
        base_head = self.git("rev-parse", "HEAD").strip()
        self.git("checkout", "-qb", "proposed-branch", self.base)
        self.case()
        (self.root / TITLE / f"{TITLE}.png").unlink()
        self.commit()
        result, values = self.run_stage("directories", "--base", base_head, "--merge-base")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(json.loads(values["cases"])[0]["directory"], TITLE)

    def test_multiple_declared_directories_cannot_share_the_same_kebab_case_name(self):
        entry = self.case()
        other = TITLE.replace("—", " ")
        for extension in ("md", "png", "science"):
            self.write(f"{other}/{other}.{extension}", "fixture")
        self.manifest([entry, {**entry, "title": other}])
        self.commit()
        result = self.check_manifest(expected=1)
        self.assertIn("multiple new directories", result.stderr)

    def test_pr_after_force_push_still_checks_earlier_case_changes(self):
        self.case()
        (self.root / TITLE / f"{TITLE}.png").unlink()
        self.commit()
        self.write("README.md", "documentation update")
        self.commit()
        before = self.git("rev-parse", "HEAD").strip()
        self.write("README.md", "rewritten documentation update")
        self.git("add", "README.md")
        self.git("-c", "commit.gpgsign=false", "commit", "--amend", "--no-edit", "-q")

        checkout = self.root / "fresh-checkout"
        self.git("clone", "--no-local", "--quiet", str(self.root), str(checkout))
        old_commit = subprocess.run(
            ["git", "cat-file", "-e", before], cwd=checkout, capture_output=True)
        self.assertNotEqual(old_commit.returncode, 0)
        original_root = self.root
        try:
            self.root = checkout
            result, values = self.run_stage("directories", "--base", self.base, "--merge-base")
        finally:
            self.root = original_root
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual([case["directory"] for case in json.loads(values["cases"])], [TITLE])
        self.assertIn(f"{TITLE}.png", result.stderr)
        self.assertNotIn("Couldn't compare the Git trees", result.stderr)

    def test_renamed_unlisted_case_is_ignored(self):
        self.git("mv", "Existing Case", "Renamed Case")
        self.commit()
        result, values = self.scan()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(values["cases"]), [])

    def test_symlink_resources_do_not_count_as_case_files(self):
        self.case()
        cover = self.root / TITLE / f"{TITLE}.png"
        cover.unlink()
        cover.symlink_to("../manifest.json")
        self.commit()
        result, _ = self.scan()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def existing_case(self):
        entry = self.case()
        self.commit()
        self.base = self.git("rev-parse", "HEAD").strip()
        return entry

    # Undeclared files may be staged in the repository ahead of publication.
    def test_new_directories_without_manifest_changes_are_ignored(self):
        for title in ("Extra One", "Extra Two", "Extra Three"):
            self.write(f"{title}/notes.txt", "not ready for publication")
        self.commit()
        result, values = self.scan()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(values["cases"]), [])
        self.assertEqual(self.http.requests, [])

    def test_new_manifest_entry_ignores_unlisted_directories(self):
        self.case()
        for title in ("Extra One", "Extra Two"):
            self.write(f"{title}/notes.txt", "not ready for publication")
        self.commit()
        result, values = self.scan()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([case["directory"] for case in json.loads(values["cases"])], [TITLE])
        self.check_manifest()

    def test_removed_entry_with_broken_files_skips_checks(self):
        self.existing_case()
        self.git("rm", f"{TITLE}/{TITLE}.png")
        self.manifest([]); self.commit()
        result, values = self.scan()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(values["cases"]), [])
        self.assertEqual(self.http.requests, [])

    def test_changed_manifest_entry_does_not_select_other_file_changes(self):
        entry = self.case()
        legacy = {"title": "Existing Case", "name": "existing-case"}
        self.manifest([entry, legacy]); self.commit()
        self.base = self.git("rev-parse", "HEAD").strip()
        self.write("Existing Case/README.md", "still not ready")
        entry["cover"]["sha256"] = "b" * 64
        self.manifest([entry, legacy]); self.commit()
        result, values = self.scan()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([case["directory"] for case in json.loads(values["cases"])], [TITLE])
        self.check_manifest()

    def test_only_file_contents_changed_skips_case_checksums(self):
        for key in ("cover", "case", "introduction"):
            with self.subTest(key=key):
                entry = self.case()
                del entry[key]["sha256"]
                self.manifest([entry]); self.commit()
                self.base = self.git("rev-parse", "HEAD").strip()
                # Resource edits alone do not declare anything for publication.
                path = self.root / entry[key]["path"]
                self.write(entry[key]["path"], "x" * path.stat().st_size)
                self.commit()
                result, values = self.scan()
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(values["cases"]), [])
                self.check_manifest()
                self.assertEqual(self.http.requests, [])

    def test_renaming_resource_with_manifest_edit_triggers_directory_validation(self):
        entry = self.existing_case()
        self.git("mv", f"{TITLE}/{TITLE}.png", f"{TITLE}/wrong.png")
        entry["cover"]["sha256"] = "b" * 64
        self.manifest([entry])
        self.commit()
        result, values = self.scan()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(values["cases"])[0]["directory"], TITLE)
        self.assertIn(f"{TITLE}.png", result.stderr)

    def test_deleting_resource_with_manifest_edit_triggers_directory_validation(self):
        entry = self.existing_case()
        self.git("rm", f"{TITLE}/{TITLE}.md")
        entry["cover"]["sha256"] = "b" * 64
        self.manifest([entry])
        self.commit()
        result, _ = self.scan()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(f"{TITLE}.md", result.stderr)

    def test_adding_file_in_existing_case_without_manifest_edit_is_ignored(self):
        self.existing_case()
        self.write(f"{TITLE}/notes.txt", "new file")
        self.commit()
        result, values = self.scan()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(values["cases"]), [])
        self.check_manifest()

    def test_manifest_only_change_selects_case_and_skips_directory_checks(self):
        entry = self.existing_case()
        entry["cover"]["bytes"] = 54321
        self.manifest([entry])
        self.commit()
        scan, values = self.scan()
        self.assertEqual(scan.returncode, 0, scan.stderr)
        self.assertEqual([item["directory"] for item in json.loads(values["cases"])], [TITLE])
        self.assertIn("Skipping directory/name checks", scan.stderr)
        result = self.check_manifest(expected=1)
        self.assertIn("54321", result.stderr)

    def test_manifest_only_change_does_not_recheck_unchanged_invalid_case(self):
        entry = self.case()
        legacy = {"title": "Existing Case", "name": "existing-case"}
        self.manifest([entry, legacy])
        self.commit()
        self.base = self.git("rev-parse", "HEAD").strip()
        content = "updated introduction"
        self.write(f"{TITLE}/{TITLE}.md", content)
        entry["introduction"]["bytes"] = len(content)
        self.manifest([entry, legacy])
        self.commit()
        self.check_manifest()
        _, values = self.scan()
        self.assertEqual([item["directory"] for item in json.loads(values["cases"])], [TITLE])

    def test_manifest_formatting_and_reordering_do_not_revalidate_cases(self):
        entry = self.case()
        legacy = {"title": "Existing Case", "name": "existing-case"}
        self.manifest([entry, legacy])
        self.commit()
        self.base = self.git("rev-parse", "HEAD").strip()
        self.write("manifest.json", json.dumps([legacy, entry], indent=4, sort_keys=True))
        self.commit()
        result, values = self.scan()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(values["cases"]), [])

    def test_manifest_name_change_without_directory_change_fails(self):
        entry = self.existing_case()
        entry["name"] = "wrong-name"
        self.manifest([entry]); self.commit()
        self.check_manifest(expected=1)

    def test_removing_manifest_entry_while_directory_remains_passes(self):
        self.existing_case()
        self.manifest([]); self.commit()
        self.check_manifest()
        _, values = self.scan()
        self.assertEqual(json.loads(values["cases"]), [])
        self.assertEqual(self.http.requests, [])

    def test_renaming_manifest_cannot_skip_validation(self):
        self.existing_case()
        self.git("mv", "manifest.json", "renamed.json")
        self.commit()
        result, _ = self.scan()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("manifest.json", result.stderr)
        self.assertIn("Couldn't access", result.stderr)

    def test_removing_case_and_manifest_entry_together_passes(self):
        self.existing_case()
        self.git("rm", "-r", TITLE)
        self.manifest([]); self.commit()
        result, values = self.scan()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(values["cases"]), [])

    def test_changed_manifest_entry_referring_to_removed_directory_fails(self):
        entry = self.existing_case()
        self.git("rm", "-r", TITLE)
        entry["cover"]["sha256"] = "b" * 64
        self.manifest([entry]); self.commit()
        result, _ = self.scan()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(NAME, result.stderr)
        self.assertIn("manifest", result.stderr)

    def test_added_manifest_entry_without_a_directory_fails(self):
        self.manifest([{"title": "Ghost Case", "name": "ghost-case"}]); self.commit()
        result, _ = self.scan()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("ghost-case", result.stderr)

    def test_science_removal_with_release_url_update_passes(self):
        entry = self.existing_case()
        self.git("rm", f"{TITLE}/{TITLE}.science")
        entry["case"]["release_url"] = self.url
        self.manifest([entry]); self.commit()
        self.check_manifest()

    def test_bad_new_entry_cannot_hide_behind_an_unchanged_good_entry(self):
        entry = self.existing_case()
        duplicate = copy.deepcopy(entry)
        duplicate["name"] = "wrong-name"
        duplicate["cover"]["bytes"] = -1
        self.manifest([entry, duplicate]); self.commit()
        result = self.check_manifest(expected=1)
        self.assertIn("wrong-name", result.stderr)
        self.assertIn(NAME, result.stderr)

    def rename_complete_case(self, title, name):
        entry = self.existing_case()
        self.git("mv", TITLE, title)
        for key, extension in (("cover", "png"), ("case", "science"), ("introduction", "md")):
            filename = f"{title}.{extension}"
            self.git("mv", f"{title}/{TITLE}.{extension}", f"{title}/{filename}")
            entry[key]["file_name"] = filename
            entry[key]["path"] = f"{title}/{filename}"
        entry["title"], entry["name"] = title, name
        self.manifest([entry]); self.commit()
        result, values = self.scan()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([item["directory"] for item in json.loads(values["cases"])], [title])
        self.check_manifest()

    def test_complete_case_rename_selects_new_directory_only(self):
        self.rename_complete_case("Renamed Case", "renamed-case")

    def test_case_rename_preserving_kebab_name_is_not_a_stale_entry(self):
        self.rename_complete_case(TITLE.replace("—", " - "), NAME)

    def test_manifest_boolean_is_not_equal_to_numeric_metadata(self):
        entry = self.case()
        self.write(f"{TITLE}/{TITLE}.png", "x")
        entry["cover"]["bytes"] = 1
        self.manifest([entry]); self.commit()
        self.base = self.git("rev-parse", "HEAD").strip()
        entry["cover"]["bytes"] = True
        self.manifest([entry]); self.commit()
        result = self.check_manifest(expected=1)
        self.assertIn("cover.bytes", result.stderr)


if __name__ == "__main__":
    unittest.main()
