#!/usr/bin/env python3
"""Validate only cases added or modified in manifest.json."""

import argparse
from http.client import HTTPException
from ipaddress import IPv6Address
import json
import mimetypes
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
from urllib.parse import quote, urlsplit
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener


def git(*args):
    try:
        return subprocess.check_output(["git", *args], stderr=subprocess.PIPE).decode("utf-8")
    except subprocess.CalledProcessError as error:
        detail = error.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(
            f"Couldn't compare the Git trees. Git command {show(list(args))} failed: {detail}. "
            "Check that the base ref exists and actions/checkout uses fetch-depth: 0, "
            "then rerun the directories step."
        ) from error


def show(value):
    return json.dumps(value, ensure_ascii=False)


def log(message):
    # The runner also recognizes legacy ##[commands] anywhere in a log line.
    safe = message.replace("\r", "\\r").replace("\n", "\\n").replace("##[", r"\u0023\u0023[")
    print(safe, file=sys.stderr)


def report_error(message):
    if os.environ.get("GITHUB_ACTIONS") == "true":
        # Workflow commands need percent escaping before CR/LF escaping.
        escaped = message.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::error title=Case structure check::{escaped}", file=sys.stderr)
    else:
        log("ERROR: " + message)


def file_problem(path):
    if path.is_symlink():
        return f"{show(str(path))} is a symlink. Replace it with the actual file and commit it."
    return (f"Couldn't find the file {show(str(path))}. Add or rename the file so it has "
            "the same name as its case directory, including letter case, then commit it.")


def kebab_case(title):
    title = "".join(c for c in unicodedata.normalize("NFKD", title)
                    if not unicodedata.combining(c))
    title = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1-\2", title)
    title = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", title)
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def regular_file(path):
    return path.is_file() and not path.is_symlink()


def is_image_filename(filename):
    # Check the image extension without reading or downloading resource bodies.
    if not isinstance(filename, str):
        return False
    # Literal colons and question marks must not be parsed as a URL scheme/query.
    media_type, encoding = mimetypes.guess_type(quote(filename, safe=""))
    return bool(media_type and media_type.startswith("image/") and encoding is None)


def is_science_url(url):
    if not isinstance(url, str) or not url or re.search(r"[\s\x00-\x1f\x7f]", url):
        return False
    try:
        parsed = urlsplit(url)
        # Accessing port rejects malformed and out-of-range port numbers.
        _ = parsed.port
        # Python 3.9 does not validate bracketed hosts during URL splitting.
        if "[" in parsed.netloc:
            IPv6Address(parsed.hostname)
        # Check the asset path so download query parameters remain valid.
        return (parsed.scheme in ("http", "https") and bool(parsed.hostname)
                and parsed.path.endswith(".science"))
    except ValueError:
        return False


def resolve_base(base, merge_base=False, new_branch_base=None):
    if re.fullmatch(r"0{40}|0{64}", base) and new_branch_base:
        base, merge_base = new_branch_base, True
    if re.fullmatch(r"0{40}|0{64}", base):
        # The initial push of the default branch has no previous tree.
        log("This is the first push of the default branch. Checking all manifest entries.")
        return None
    base = git("rev-parse", "--verify", base + "^{commit}").strip()
    if merge_base:
        base = git("merge-base", base, "HEAD").strip()
    log(f"Comparing HEAD with {base} to find relevant case changes.")
    return base


def case_folders(paths):
    return {path.split("/", 1)[0] for path in paths if "/" in path and not path.startswith(".")}


def entry_folders(entry, known):
    matches = {directory for directory in known if kebab_case(directory) == entry.get("name")}
    if len(matches) == 1:
        return matches
    title = entry.get("title")
    if isinstance(title, str) and title in known:
        return {title}
    # Paths help locate a case even when its manifest name/title was misspelled.
    for key in ("cover", "case", "introduction"):
        resource = entry.get(key)
        path = resource.get("path") if isinstance(resource, dict) else None
        if isinstance(path, str) and path.split("/", 1)[0] in known:
            matches.add(path.split("/", 1)[0])
    return matches


def manifest_entries(text, source):
    entries = read_json(text, source)
    if not isinstance(entries, list) or any(not isinstance(entry, dict) for entry in entries):
        raise ValueError(f"{source} must contain a JSON array of case objects, such as [{{\"title\": ...}}]. "
                         "Put the entries inside square brackets and make each entry an object.")
    return entries


def directories(base, merge_base=False, new_branch_base=None):
    from manifest_diff import changed_entries

    base = resolve_base(base, merge_base, new_branch_base)
    previous_paths = set(git("ls-tree", "-r", "--name-only", "-z", base).split("\0")) if base else set()
    current_paths = set(git("ls-tree", "-r", "--name-only", "-z", "HEAD").split("\0"))
    previous, current = case_folders(previous_paths), case_folders(current_paths)
    # Compare path sets rather than file contents: additions, removals and renames
    # affect structure; editing a file in place does not.
    structural = case_folders(previous_paths ^ current_paths)
    # Keep both paths when a file is renamed, including manifest.json's old path.
    changed_paths = set(git("diff", "--no-renames", "--name-only", "-z", base, "HEAD").split("\0")) if base else current_paths
    changed = case_folders(changed_paths)
    manifest_changed = "manifest.json" in changed_paths
    log(f"Cases with file changes: {len(changed)}. Cases with path changes: {len(structural)}. "
        f"manifest.json changed: {manifest_changed}.")
    if not manifest_changed:
        log("manifest.json is unchanged. Skipping case resource checks.")
        return [], []

    manifest = manifest_entries(Path("manifest.json").read_text(encoding="utf-8"), "manifest.json")
    selected = set()
    errors = []
    known = previous | current
    old_manifest = []
    if base and "manifest.json" in previous_paths:
        try:
            old_manifest = manifest_entries(git("show", f"{base}:manifest.json"), "baseline manifest.json")
        except ValueError:
            log("The baseline manifest could not be parsed. Rechecking all current entries so it can be repaired.")
    # Only surviving additions/edits select cases. File changes and removed entries
    # never opt a directory into publication checks on their own.
    for entry in changed_entries(old_manifest, manifest):
        matches = entry_folders(entry, known) & current
        selected.update(matches)
        if not matches:
            errors.append(f"manifest.json: changed entry {show(entry.get('name'))} has no matching case directory. "
                          "Correct its name, title, and resource paths, or add the case directory.")
        for directory in matches:
            # Do not let a bad alias hide behind an unchanged canonical entry.
            expected_name = kebab_case(directory)
            if entry.get("name") != expected_name:
                errors.append(f"manifest.json: changed entry has name {show(entry.get('name'))}, "
                              f"but its case directory {show(directory)} requires {show(expected_name)}. "
                              "Correct this entry's name and keep exactly one entry for the case.")

    cases = []
    for directory in sorted(selected):
        folder = Path(directory)
        name = kebab_case(directory)
        problems = []
        if directory in structural and not name:
            problems.append("The directory name becomes empty after conversion to kebab-case. "
                            "Rename it to include Latin letters or digits, such as My New Case.")
        if directory in structural:
            if not regular_file(folder / f"{directory}.md"):
                problems.append(file_problem(folder / f"{directory}.md"))
            # Keep the same-name rule while allowing any recognized image format.
            if not any(path.stem == directory and is_image_filename(path.name) and regular_file(path)
                       for path in folder.glob("*")):
                covers = [entry.get("cover", {}).get("path") for entry in manifest
                          if entry.get("name") == name and isinstance(entry.get("cover"), dict)]
                problems.append(f"Couldn't find an image cover with the same name as its case directory. "
                                f"Add a same-named image file and update cover.file_name and cover.path "
                                f"in manifest.json (declared paths: {show(covers)}).")
        else:
            log(f"Skipping directory/name checks for {show(directory)}: its paths are unchanged. "
                "Rechecking its manifest entry and resources for file or metadata changes.")
        local = regular_file(folder / f"{directory}.science")
        log(f"Selected case {show(directory)} (manifest name: {show(name)}). "
            + ("Found the local .science file; case.release_url must be empty."
               if local else "No same-named .science file; the manifest step will require case.release_url."))
        cases.append({
            "directory": directory, "name": name, "valid": not problems,
            "has_local_science": local,
        })
        errors.extend(f"Directory {show(directory)}: {problem}" for problem in problems)
    return cases, errors


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"The key {show(key)} appears more than once in the same object. "
                             "Keep one value for this key and remove the duplicate.")
        result[key] = value
    return result


def read_json(text, source):
    try:
        return json.loads(text, object_pairs_hook=unique_keys)
    except json.JSONDecodeError as error:
        raise ValueError(f"Couldn't read {source} as JSON at line {error.lineno}, column {error.colno}: "
                         f"{error.msg}. Check the commas, quotes, and brackets at that location.") from error
    except ValueError as error:
        raise ValueError(f"{source}: {error}") from error


def require_keys(value, keys, label, errors, optional=()):
    if not isinstance(value, dict):
        errors.append(f"{label}: expected a JSON object, but found {show(value)}. "
                      f"Replace it with an object containing these fields: {', '.join(sorted(keys))}.")
        return False
    allowed = keys | set(optional)
    missing, extra = keys - value.keys(), value.keys() - allowed
    if missing:
        errors.append(f"{label}: missing fields: {', '.join(sorted(missing))}. "
                      "Add these fields to this object in manifest.json.")
    if extra:
        errors.append(f"{label}: unrecognized fields: {', '.join(sorted(extra))}. "
                      f"Remove them or correct their spelling. Allowed fields: {', '.join(sorted(allowed))}.")
    return not missing


class HeadRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urlsplit(newurl).scheme not in ("http", "https"):
            raise HTTPError(newurl, code, "redirect must use HTTP(S)", headers, fp)
        # Older Python versions turn redirected HEAD requests into GET requests.
        redirected = super().redirect_request(req, fp, 307 if code == 308 else code,
                                              msg, headers, newurl)
        if redirected is not None:
            redirected.method = "HEAD"
        return redirected

    http_error_308 = HTTPRedirectHandler.http_error_302


def validate_head_size(url, size, label, errors, timeout=15):
    log(f"{label}: sending HEAD to check file availability and size; no download or checksum computation.")
    request = Request(url, method="HEAD", headers={"Accept-Encoding": "identity"})
    try:
        with build_opener(HeadRedirectHandler()).open(request, timeout=timeout) as response:
            if response.status != 200:
                errors.append(f"{label}: HEAD returned HTTP {response.status}. "
                              "Check the resource URL; it must return HTTP 200 for HEAD requests.")
                return
            length = response.headers.get("Content-Length")
            if length is None or not re.fullmatch(r"[0-9]+", length):
                errors.append(f"{label}.bytes: HEAD returned Content-Length {show(length)}, "
                              "so the file size could not be verified. Use a download host that returns "
                              "a valid Content-Length for HEAD requests.")
                return
            actual_size = int(length)
            if actual_size != size:
                errors.append(f"{label}.bytes: manifest says {size}, but HEAD reports {actual_size} bytes. "
                              f"Update bytes to {actual_size}, or correct the resource URL to point to the intended file.")
            else:
                log(f"{label}: HEAD confirmed HTTP 200 and {actual_size} bytes.")
    except HTTPError as error:
        errors.append(f"{label}: HEAD failed with HTTP {error.code} ({error.reason}). "
                      "Check that the asset exists, is publicly accessible, and its host supports HEAD. "
                      "For repository files, check CASE_FILE_BASE_URL and the PR head commit; "
                      "for external files, correct release_url.")
        error.close()
    except (URLError, OSError, HTTPException, ValueError) as error:
        errors.append(f"{label}: HEAD could not finish: {error}. "
                      "Check the download URL, network connection, and server certificate, then rerun the workflow. "
                      f"Each connection has a {timeout}-second timeout.")


def validate_resource(resource, case, key, extension, errors):
    directory = case["directory"]
    label = f"manifest.json / {show(directory)} / {key}"
    keys = {"file_name", "path", "bytes", "sha256"}
    if key == "case":
        keys.add("release_url")
    if not require_keys(resource, keys, label, errors):
        return
    checksum = resource["sha256"]
    if not isinstance(checksum, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", checksum):
        errors.append(f"{label}.sha256: found {show(checksum)}. Enter exactly 64 hexadecimal characters "
                      "(0-9, a-f, A-F), without whitespace. Compute SHA-256 from the file on your "
                      "device before committing and update manifest.json; CI checks the format only.")
    if key == "cover":
        if not is_image_filename(resource["file_name"]):
            errors.append(f"{label}.file_name: found {show(resource['file_name'])}. "
                          "Use a filename with an image/* extension, such as .jpg, .webp, or .svg.")
            return
        extension = Path(resource["file_name"]).suffix.lstrip(".")
    filename = f"{directory}.{extension}"
    expected_path = f"{directory}/{filename}"
    for field, expected in (("file_name", filename), ("path", expected_path)):
        if resource.get(field) != expected:
            errors.append(f"{label}.{field}: found {show(resource.get(field))}. "
                          f"Set it to {show(expected)} so it points to the same-named case file.")
    size = resource.get("bytes")
    size_valid = type(size) is int and size >= 0
    if not size_valid:
        errors.append(f"{label}.bytes: found {show(size)}. Enter the file size in bytes as "
                      "a whole number, without quotes, that is zero or greater.")
    if key == "case":
        release_url = resource.get("release_url")
        if case["has_local_science"]:
            if release_url != "":
                errors.append(f"{label}.release_url: found {show(release_url)} alongside local "
                              f"{show(expected_path)}. A local .science file and release_url must not both "
                              "be provided. Set release_url to an empty string (\"\").")
        elif isinstance(release_url, str) and not release_url.strip():
            errors.append(f"{label}.release_url: found neither a local {show(expected_path)} nor a "
                          "nonempty release_url. Provide exactly one: add the same-named .science file "
                          "or set release_url to a complete HTTP(S) .science download URL.")
        elif not is_science_url(release_url):
            errors.append(f"{label}.release_url: found {show(release_url)}, and there is no local "
                          f"{show(expected_path)}. Add a complete HTTP(S) download URL whose path ends in .science "
                          "(for example, https://example.com/case.science), or add the same-named .science file "
                          "and set release_url to an empty string. README links are not used.")
        elif size_valid:
            validate_head_size(release_url, size, label, errors)
    if key != "case" or case["has_local_science"]:
        path = Path(expected_path)
        if not regular_file(path):
            errors.append(f"{label}: {file_problem(path)}")
            return
        if size_valid:
            base_url = os.environ.get("CASE_FILE_BASE_URL")
            if not base_url:
                raise ValueError("CASE_FILE_BASE_URL is missing. Set it to the GitHub Raw URL for the "
                                 "PR head repository and commit so repository file sizes can be checked with HEAD.")
            validate_head_size(base_url.rstrip("/") + "/" + quote(expected_path), size, label, errors)


def validate_manifest(cases, declared_only=False):
    if not isinstance(cases, list):
        raise ValueError("CASES_JSON must be a JSON array from the directories step. "
                         "Pass steps.directories.outputs.cases to the manifest step's CASES_JSON environment variable.")
    if not cases:
        return []
    required = {"directory": str, "name": str, "valid": bool, "has_local_science": bool}
    for index, case in enumerate(cases):
        if not isinstance(case, dict) or any(type(case.get(key)) is not kind for key, kind in required.items()):
            raise ValueError(f"CASES_JSON item {index + 1} is incomplete or has the wrong field types. "
                             "Rerun the directories step and pass its complete cases output to this step.")
    manifest = manifest_entries(Path("manifest.json").read_text(encoding="utf-8"), "manifest.json")
    errors = []
    names = [case["name"] for case in cases]
    for case in cases:
        directory, name = case["directory"], case["name"]
        label = f"manifest.json / {show(directory)}"
        log(f"Checking manifest entry {show(name)} for directory {show(directory)}.")
        if not case["valid"]:
            errors.append(f"Directory {show(directory)} failed the directories step. "
                          "Fix its missing files or naming errors above, then rerun the workflow.")
            continue
        if names.count(name) != 1:
            collisions = [item["directory"] for item in cases if item["name"] == name]
            errors.append(f"Directory {show(directory)}: multiple new directories map to name {show(name)}: "
                          f"{show(collisions)}. Rename one directory and update its manifest name so each case has a unique name.")
        entries = [entry for entry in manifest if entry.get("name") == name]
        if len(entries) != 1:
            if not entries:
                errors.append(f"{label}: no entry has name {show(name)}. Add an entry with this name, "
                              "or correct the existing entry's name to match the directory's kebab-case name.")
            else:
                errors.append(f"{label}: found {len(entries)} entries with name {show(name)}. "
                              "Keep exactly one matching entry and remove or rename the duplicates.")
            continue
        entry = entries[0]
        # Publication supports legacy entries without an introduction, while PR
        # admission retains the existing requirement for new or edited cases.
        required_keys = {"title", "name", "cover", "case"}
        require_keys(entry, required_keys if declared_only else required_keys | {"introduction"},
                     label, errors, optional=("introduction",))
        if "title" in entry and entry["title"] != directory:
            errors.append(f"{label}.title: found {show(entry['title'])}. Set title to {show(directory)} "
                          "so it matches the directory name exactly.")
        for key, extension in (("cover", None), ("case", "science"), ("introduction", "md")):
            if key in entry:
                validate_resource(entry[key], case, key, extension, errors)
    return errors



def check_declarations(root, before, after):
    """Check Git object changes against declarations, without hashing file contents."""
    from manifest_diff import changed_entries, git as range_git, local_resources, manifests
    old, new, manifest_changed = manifests(root, before, after)
    if not manifest_changed:
        return []
    # Match directory selection: unrelated file changes and removed entries are ignored.
    affected = changed_entries(old, new)
    if not affected:
        return []
    previous, current = local_resources(old), local_resources(affected)
    changed = set(range_git(root, "diff", "--no-renames", "--diff-filter=AMT", "--name-only",
                            "-z", before, after).split("\0")) - {""}
    errors = []
    for key, resource in current.items():
        prior = previous.get(key)
        path = resource["path"]
        if prior == resource and path not in changed:
            continue
        declaration = resource.get("sha256")
        if not isinstance(declaration, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", declaration):
            errors.append(f"{key}: sha256 must be a 64-digit hexadecimal declaration.")
            continue
        listing = range_git(root, "ls-tree", after, "--", path).split()
        if not listing or listing[0] not in ("100644", "100755"):
            errors.append(f"{key}: local resource must be a committed regular file.")
            continue
        if prior and prior["path"] == path and path in changed:
            # A file-only batch may have removed this path without changing its
            # declaration. Restoring it has no prior regular-file object to compare.
            old_listing = range_git(root, "ls-tree", before, "--", path).split()
            if not old_listing or old_listing[0] not in ("100644", "100755"):
                continue
            old_object, new_object = old_listing[2], listing[2]
            previous_sha = prior.get("sha256")
            if old_object != new_object and isinstance(previous_sha, str) and previous_sha.lower() == declaration.lower():
                errors.append(f"{key}: file content changed; synchronize its manifest sha256 declaration.")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="stage", required=True)
    scan = commands.add_parser("directories")
    scan.add_argument("--base", required=True, help="Git base commit; all-zero SHA means an empty tree")
    scan.add_argument("--merge-base", action="store_true", help="Compare to the common ancestor for a PR")
    scan.add_argument("--new-branch-base", help="Default branch ref for a new feature branch's first push")
    manifest = commands.add_parser("manifest", help="Check selected manifest entries")
    manifest.add_argument("--plan", type=Path, help="Use the S3-based publication plan")
    declarations = commands.add_parser("declarations", help="Check changed local resource SHA declarations")
    declarations.add_argument("--base", required=True)
    declarations.add_argument("--after", required=True)
    args = parser.parse_args()
    if args.stage == "declarations":
        try:
            errors = check_declarations(Path.cwd(), args.base, args.after)
            for error in errors:
                report_error(error)
            return int(bool(errors))
        except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
            report_error(str(error))
            return 1
    stage = "Change detection and directory check" if args.stage == "directories" else "Manifest check"
    actions = os.environ.get("GITHUB_ACTIONS") == "true"
    if actions:
        print(f"::group::{stage}", file=sys.stderr)
    log(f"Starting {stage.lower()}.")
    try:
        if args.stage == "directories":
            cases, errors = directories(args.base, args.merge_base, args.new_branch_base)
            # Preserve the JSON data without emitting legacy runner commands.
            payload = json.dumps(cases, ensure_ascii=True, separators=(",", ":")).replace("##[", r"\u0023\u0023[")
            output = os.environ.get("GITHUB_OUTPUT")
            if output:
                with open(output, "a", encoding="utf-8") as stream:
                    stream.write(f"cases={payload}\n")
            print(payload)
        else:
            if args.plan:
                cases = read_json(args.plan.read_text(encoding="utf-8"), "publication plan")["cases"]
            elif not os.environ.get("CASES_JSON"):
                raise ValueError("CASES_JSON is missing or empty. Run the directories step first, then pass "
                                 "steps.directories.outputs.cases to the manifest step's CASES_JSON environment variable.")
            else:
                cases = read_json(os.environ["CASES_JSON"], "CASES_JSON (from the directories step)")
            errors = validate_manifest(cases, declared_only=bool(args.plan))
        for error in errors:
            report_error(error)
        if errors:
            noun = "problem" if len(errors) == 1 else "problems"
            log(f"FAIL: {stage} found {len(errors)} {noun}. Affected case directories: {len(cases)}. "
                "Follow the fixes above, commit the changes, and rerun the workflow.")
        elif not cases:
            log("PASS: No relevant case changes need validation. No manifest entries were added or modified. "
                "Skipping case resource checks; any changed manifest is still published.")
        else:
            log(f"PASS: {stage} finished. No problems found. Affected case directories: {len(cases)}.")
        return 1 if errors else 0
    except OSError as error:
        report_error(f"Couldn't access {show(error.filename)}: {error.strerror}. Check that the file exists "
                     "and is readable (or writable for workflow output files). If it belongs in the repository, "
                     "commit it at the expected path before rerunning the workflow.")
        log(f"FAIL: {stage} could not finish. Fix the file access problem above and rerun the workflow.")
        return 1
    except ValueError as error:
        report_error(str(error))
        log(f"FAIL: {stage} could not finish. Fix the input problem above and rerun the workflow.")
        return 1
    finally:
        if actions:
            print("::endgroup::", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
