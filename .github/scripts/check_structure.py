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


def is_resource_url(url, kind=None):
    if not isinstance(url, str) or not url or re.search(r"[\s\x00-\x1f\x7f]", url):
        return False
    try:
        parsed = urlsplit(url)
        _ = parsed.port
        if "[" in parsed.netloc:
            IPv6Address(parsed.hostname)
        return (parsed.scheme in ("http", "https") and bool(parsed.hostname)
                and not parsed.username and not parsed.password
                and (kind != "case" or parsed.path.endswith(".science")))
    except ValueError:
        return False


def is_science_url(url):
    return is_resource_url(url, "case")


def validate_resource_path(resource):
    path, filename = resource.get("path"), resource.get("file_name")
    if (not isinstance(path, str) or re.search(r"[\x00-\x1f\x7f\\]", path)
            or re.match(r"^[A-Za-z]:", path)
            or any(part in ("", ".", "..") for part in path.split("/"))
            or not isinstance(filename, str) or filename != path.split("/")[-1]):
        raise ValueError("invalid resource path or file_name")


def catalog_errors(entries, legacy=False):
    errors, catalogs = [], {}
    for entry in entries:
        label = "manifest.json / " + show(entry.get("name"))
        if legacy and not {"catalog", "catalog_name"} & entry.keys():
            continue
        catalog, name = entry.get("catalog"), entry.get("catalog_name")
        if not isinstance(catalog, str) or not isinstance(name, str):
            errors.append(label + ": catalog and catalog_name must both be strings; use two empty strings for no classification")
            continue
        if catalog == name == "":
            continue
        if (not catalog.strip() or catalog in (".", "..")
                or re.search(r"[\x00-\x1f\x7f/\\]", catalog) or re.match(r"^[A-Za-z]:", catalog)):
            errors.append(label + ": catalog must be a nonempty, safe single directory name")
            continue
        if not catalog.isascii():
            errors.append(label + ": catalog " + show(catalog)
                          + " cannot be converted to ASCII kebab-case; rename it manually (no translation or character removal)")
            continue
        expected = kebab_case(catalog)
        if not expected or name != expected:
            errors.append(label + ": catalog_name must equal the nonempty kebab-case conversion of catalog "
                          + show(catalog) + ": " + show(expected))
            continue
        if name in catalogs and catalogs[name] != catalog:
            errors.append(label + ": catalog_name collision " + show(name) + " between "
                          + show(catalogs[name]) + " and " + show(catalog) + "; rename one catalog")
        catalogs[name] = catalog
        for kind in ("cover", "case", "introduction"):
            resource = entry.get(kind)
            path = resource.get("path") if isinstance(resource, dict) else None
            if not isinstance(path, str) or not path.startswith(catalog + "/"):
                errors.append(label + "/" + kind + ": path must start with catalog directory " + show(catalog + "/"))
    return errors


def schema_errors(entry, legacy=False):
    errors = catalog_errors([entry], legacy=legacy)
    label = "manifest.json / " + show(entry.get("name"))
    required = {"title", "name", "cover", "case"} | (set() if legacy else {"introduction"})
    if not require_keys(entry, required, label, errors, optional=("introduction", "catalog", "catalog_name")):
        return errors
    if not isinstance(entry["title"], str) or not entry["title"].strip():
        errors.append(label + ": title must be a nonempty string")
    if not isinstance(entry["name"], str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", entry["name"]):
        errors.append(label + ": name must be kebab-case")
    destinations = set()
    for kind in ("cover", "case", "introduction"):
        if kind not in entry:
            continue
        resource = entry[kind]
        keys = {"file_name", "path", "bytes", "sha256", "release_url"}
        if legacy and kind != "case":
            keys.remove("release_url")
        if not require_keys(resource, keys, label + "/" + kind, errors, optional=("release_url",)):
            continue
        try:
            validate_resource_path(resource)
        except ValueError as error:
            errors.append(label + ": " + str(error))
        filename = resource["file_name"]
        if not (is_image_filename(filename) if kind == "cover" else
                isinstance(filename, str) and filename.endswith(".science" if kind == "case" else ".md")):
            errors.append(label + "/" + kind + ": invalid file type")
        if isinstance(filename, str):
            if filename in destinations:
                errors.append(label + ": Duplicate upload destination")
            destinations.add(filename)
        if type(resource["bytes"]) is not int or resource["bytes"] < 0:
            errors.append(label + "/" + kind + ": bytes must be a nonnegative integer")
        if not isinstance(resource["sha256"], str) or not re.fullmatch(r"[0-9a-fA-F]{64}", resource["sha256"]):
            errors.append(label + "/" + kind + ": sha256 must be 64 hexadecimal digits")
        url = resource.get("release_url", "")
        if url != "" and not is_resource_url(url, kind):
            errors.append(label + "/" + kind + ": invalid release_url")
    return errors


def source_errors(root, entry):
    """All-remote entries do not consult the local filesystem."""
    if all(entry[kind]["release_url"] for kind in ("cover", "case", "introduction")):
        return []
    errors = []
    for kind in ("cover", "case", "introduction"):
        resource = entry[kind]
        path = root / resource["path"]
        # Resource subdirectories remain independent within the classification.
        if resource["release_url"] and kind != "case":
            continue
        parts = resource["path"].split("/")
        parents = [root.joinpath(*parts[:length]) for length in range(1, len(parts))]
        if any(parent.is_symlink() for parent in parents):
            errors.append("Invalid resource directory (symlink): " + resource["path"])
        elif resource["release_url"]:
            if path.exists() or path.is_symlink():
                errors.append("Package requires exactly one source: " + resource["path"])
        elif any(not parent.is_dir() for parent in parents):
            errors.append("Missing or invalid resource directory: " + resource["path"])
        elif not regular_file(path):
            errors.append("Local resource must be a regular file (missing or symlink): " + resource["path"])
        elif path.stat().st_size != resource["bytes"]:
            errors.append("Local resource byte size mismatch: " + resource["path"])
    return errors


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


def manifest_entries(text, source):
    entries = read_json(text, source)
    if not isinstance(entries, list) or any(not isinstance(entry, dict) for entry in entries):
        raise ValueError(f"{source} must contain a JSON array of case objects, such as [{{\"title\": ...}}]. "
                         "Put the entries inside square brackets and make each entry an object.")
    return entries


def selected_cases(entries):
    # Selection is by entry, including entries with no local directory.
    return [{"entry": entry, "name": entry.get("name"), "valid": True,
             "directory": str(entry.get("cover", {}).get("path", "")).rsplit("/", 1)[0]
             if isinstance(entry.get("cover"), dict) else "",
             "has_local_science": not bool(entry.get("case", {}).get("release_url"))
             if isinstance(entry.get("case"), dict) else False} for entry in entries]


def directories(base, merge_base=False, new_branch_base=None):
    from manifest_diff import changed_entries
    base = resolve_base(base, merge_base, new_branch_base)
    text = git("show", "HEAD:manifest.json")
    if Path("manifest.json").read_text(encoding="utf-8") != text:
        raise ValueError("Checkout manifest differs from HEAD")
    old = manifest_entries(git("show", base + ":manifest.json"), "baseline manifest.json") if base else []
    current = manifest_entries(text, "manifest.json")
    return selected_cases(changed_entries(old, current)), catalog_errors(current)


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
                      "Correct release_url or use a host that supports HEAD.")
        error.close()
    except (URLError, OSError, HTTPException, ValueError) as error:
        errors.append(f"{label}: HEAD could not finish: {error}. "
                      "Check the download URL, network connection, and server certificate, then rerun the workflow. "
                      f"Each connection has a {timeout}-second timeout.")


def validate_manifest(cases, declared_only=False):
    if not isinstance(cases, list) or any(not isinstance(case, dict) or "entry" not in case for case in cases):
        raise ValueError("CASES_JSON must contain selected entries from the directories step")
    manifest = manifest_entries(Path("manifest.json").read_text(encoding="utf-8"), "manifest.json")
    errors = catalog_errors(manifest)
    if errors:
        return errors
    for case in cases:
        entry = case["entry"]
        if entry not in manifest:
            errors.append("Selected entry differs from checkout manifest")
            continue
        problems = schema_errors(entry)
        if sum(item.get("name") == entry.get("name") for item in manifest) != 1:
            problems.append("Duplicate name: " + show(entry.get("name")))
        errors.extend(problems)
        if problems:
            continue
        errors.extend(source_errors(Path.cwd(), entry))
        for kind in ("cover", "case", "introduction"):
            resource = entry[kind]
            if resource["release_url"]:
                validate_head_size(resource["release_url"], resource["bytes"], entry["name"] + "/" + kind, errors)
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
        listing = range_git(root, "--literal-pathspecs", "ls-tree", after, "--", path).split()
        if not listing or listing[0] not in ("100644", "100755"):
            errors.append(f"{key}: local resource must be a committed regular file.")
            continue
        if prior and (prior["path"] != path or path in changed):
            # A file-only batch may have removed this path without changing its
            # declaration. Restoring it has no prior regular-file object to compare.
            old_listing = range_git(root, "--literal-pathspecs", "ls-tree", before, "--", prior["path"]).split()
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
