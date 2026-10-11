"""Materialize a complete user-authored skill brief in a new directory. No generation claims."""
from __future__ import annotations

import argparse
import json
import hashlib
import stat
import zipfile
import os
import re
import shutil
import tempfile
from pathlib import Path

from .common import HectlError
from .evaluation import (MAX_ARTIFACT, disjoint, read_record, relative, require, safe_path, snapshot, text)
from .packaging import check_skill, NAME_RE, LINK_RE


def initialize(brief_path, output):
    brief = read_record(brief_path)
    require(brief.get("kind") == "he-author-brief" and type(brief.get("schema_version")) is int
            and brief["schema_version"] == 1, "expected he-author-brief schema_version1")
    name = brief.get("name")
    require(isinstance(name, str) and NAME_RE.fullmatch(name), "invalid skill name")
    require(text(brief.get("description")) and "\n" not in brief["description"], "single-line description required")
    require(text(brief.get("instructions")), "provide the complete authored instructions; init does not write them for you")
    require(brief.get("status") in ("draft", "candidate"), "status must be draft or candidate; init never qualifies a skill")
    files = brief.get("files")
    require(isinstance(files, list), "files must be a list (possibly empty)")
    out = safe_path(output)
    require(out.name == name and not out.exists(), "output must be a new directory matching the skill name")
    disjoint(out, safe_path(brief_path))
    prepared = []
    seen = {"skill.md"}
    for f in files:
        require(isinstance(f, dict), "resource must be an object")
        path = relative(f.get("path"))
        require(path.casefold() not in seen and path != "SKILL.md", "duplicate/reserved resource")
        seen.add(path.casefold())
        require(path.split("/")[0] in ("playbooks", "references", "scripts", "assets", "agents"), "resource must use a declared skill resource directory")
        require(isinstance(f.get("content"), str) and len(f["content"].encode()) <= MAX_ARTIFACT, "resource content must be bounded UTF-8 text")
        mode = f.get("mode", 0o644)
        require(type(mode) is int and mode in (0o644, 0o755), "resource mode must be 420 or493 (0644/0755)")
        prepared.append((path, f["content"], mode))
    # Reject file/directory collisions before writing.
    all_names = [p for p, _, _ in prepared]
    for a in all_names:
        for b in all_names:
            require(a == b or not b.casefold().startswith(a.casefold() + "/"), "resource file/directory collision")
    front = "---\nname: %s\ndescription: %s\n---\n\n" % (name, json.dumps(brief["description"], ensure_ascii=False))
    out.parent.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix=".he-author-", dir=str(out.parent)))
    candidate = scratch / name
    try:
        candidate.mkdir()
        (candidate / "SKILL.md").write_text(front + brief["instructions"].rstrip() + "\n", encoding="utf-8")
        os.chmod(candidate / "SKILL.md", 0o644)
        for rel, content, mode in prepared:
            file = candidate / rel
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(content, encoding="utf-8")
            os.chmod(file, mode)
        result = check_skill(candidate)
        if brief["status"] == "candidate":
            require(result["ok"], "candidate format/resource validation failed: " + "; ".join(result["errors"]))
        require(not out.exists() and not out.is_symlink(), "output appeared during authoring")
        # Reserve destination before moving only our own prepared files.
        out.mkdir()
        for child in candidate.iterdir():
            shutil.move(str(child), str(out / child.name))
    finally:
        shutil.rmtree(scratch)
    return {"status": "authored-" + brief["status"], "path": str(out), "validation": check_skill(out),
            "snapshot": snapshot(out), "behavioral_qualification": "not-run",
            "note": "Supplied instructions/resources were materialized. Structural validity is not behavior proof."}


PACKAGE_MAX_TOTAL = 64 * 1024 * 1024
PACKAGE_BLOCKED_DIRS = {".git", ".hg", ".svn", "node_modules", "__pycache__", ".pytest_cache", "evals", "evidence", "sessions", "logs"}
PACKAGE_SECRET_NAMES = {"credentials", "credentials.json", "credentials.yaml", "credentials.yml", "token.json", "tokens.json", "secrets.json", "secrets.yaml", "secrets.yml", "id_rsa", "id_ed25519", "id_dsa", "known_hosts"}
PACKAGE_SECRET_CONTENT = re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----|(?:sk-proj-|ghp_|github_pat_)[A-Za-z0-9_-]{20,}")


def _package_relative(value):
    name = relative(value)
    require(not any(ord(c) < 32 or ord(c) == 127 for c in name), "control character in package path")
    parts = name.split("/")
    require(not any(p.startswith(".") or ":" in p or p.lower() in PACKAGE_BLOCKED_DIRS for p in parts),
            "hidden, metadata, evidence, or unsafe package path: " + name)
    basename = parts[-1].lower()
    require(basename not in PACKAGE_SECRET_NAMES and not basename.startswith((".env", "credentials.", "secrets."))
            and not basename.endswith((".pem", ".key", ".p12", ".pfx", ".skill", ".pyc")),
            "sensitive or accidental archive/cache file refused: " + name)
    return name


def _license_files(root):
    """Discover notice names only; never export unlisted files or follow directories."""
    answer = set()
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d.lower() not in PACKAGE_BLOCKED_DIRS
                         and not (Path(directory) / d).is_symlink())
        rel_dir = Path(directory).relative_to(root)
        for filename in files:
            lower = filename.lower()
            if (re.match(r"^(?:licen[cs]e|copying|copyright|notice|attributions?)(?:[._-]|$)", lower)
                    or any(p.lower() in ("licenses", "licences") for p in rel_dir.parts)):
                answer.add((rel_dir / filename).as_posix())
    return answer


def package(skill, manifest_path, output, host="portable"):
    """Build a deterministic, declared-file .skill ZIP; never install or publish it."""
    root, manifest_file, out = safe_path(skill, True), safe_path(manifest_path, True), safe_path(output)
    require(root.is_dir() and NAME_RE.fullmatch(root.name), "skill must be a named directory")
    require(out.suffix == ".skill", "output must have .skill extension")
    require(not out.exists() and out.parent.is_dir(), "output must be new with an existing parent directory")
    disjoint(root, out)
    disjoint(manifest_file, out)
    declaration = read_record(manifest_file)
    require(set(declaration) == {"kind", "schema_version", "files"} and declaration.get("kind") == "he-skill-package"
            and type(declaration.get("schema_version")) is int and declaration["schema_version"] == 1,
            "expected he-skill-package schema_version1 with an explicit files list")
    files = declaration["files"]
    require(isinstance(files, list) and 1 <= len(files) <= 1000, "declare 1 to 1000 package files")
    names = [_package_relative(f) for f in files]
    require(len({p.casefold() for p in names}) == len(names), "duplicate or case-aliased package path")
    require("SKILL.md" in names, "SKILL.md must be explicitly declared")
    missing_notices = _license_files(root) - set(names)
    require(not missing_notices, "explicitly include required existing license/notice files: " + ", ".join(sorted(missing_notices)))
    entries, total = [], 0
    for name in sorted(names):
        path = safe_path(root / name, True)
        require(root in path.parents, "package file escapes skill root")
        info = path.stat()
        require(stat.S_ISREG(info.st_mode) and not info.st_mode & 0o7000, "package entries must be ordinary regular files")
        require(info.st_size <= MAX_ARTIFACT, "package file exceeds per-file size cap: " + name)
        # O_NOFOLLOW protects the final component during open on supported hosts.
        fd = os.open(str(path), os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        with os.fdopen(fd, "rb") as handle:
            opened = os.fstat(handle.fileno())
            require(stat.S_ISREG(opened.st_mode) and opened.st_ino == info.st_ino and opened.st_dev == info.st_dev,
                    "package file changed before capture: " + name)
            content = handle.read(MAX_ARTIFACT + 1)
        require(len(content) <= MAX_ARTIFACT, "package file changed beyond size cap: " + name)
        require(not PACKAGE_SECRET_CONTENT.search(content), "credential-shaped content refused in " + name)
        total += len(content)
        require(total <= PACKAGE_MAX_TOTAL, "package exceeds 64 MiB total file cap")
        entries.append((name, content, 0o755 if info.st_mode & 0o111 else 0o644))
    # The selected tree, not the broader source, must satisfy local reference validation.
    scratch = Path(tempfile.mkdtemp(prefix=".he-package-", dir=str(out.parent)))
    candidate = scratch / root.name
    archive = scratch / "candidate.skill"
    try:
        candidate.mkdir()
        for name, content, mode in entries:
            file = candidate / name
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_bytes(content)
            os.chmod(file, mode)
        for md in candidate.rglob("*.md"):
            for ref in LINK_RE.findall(md.read_text(encoding="utf-8", errors="replace")):
                # Informational URL schemes are not local file dependencies.
                if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", ref):
                    require(not ref.lower().startswith("file:"), "local file URL outside package refused")
                    continue
                resolved = (md.parent / ref).resolve()
                require(candidate == resolved or candidate in resolved.parents, "resource link escapes package: " + ref)
        validation = check_skill(candidate, host)
        require(validation["ok"], "selected package resources fail validation: " + "; ".join(validation["errors"]))
        expected = {}
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED, allowZip64=False) as zipped:
            for name, content, mode in entries:
                member = root.name + "/" + name
                info = zipfile.ZipInfo(member, (1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | mode) << 16
                info.compress_type = zipfile.ZIP_STORED
                zipped.writestr(info, content)
                expected[member] = (content, mode)
        with zipfile.ZipFile(archive, "r") as zipped:
            require(zipped.namelist() == list(expected) and zipped.testzip() is None, "archive member/CRC verification failed")
            for info in zipped.infolist():
                require(info.filename.startswith(root.name + "/"), "archive root mismatch")
                _package_relative(info.filename[len(root.name) + 1:])
                content, mode = expected[info.filename]
                require(zipped.read(info) == content and info.external_attr >> 16 == stat.S_IFREG | mode,
                        "archive bytes/mode verification failed")
        # Recheck captured source bytes and modes before exposing the archive.
        for name, content, mode in entries:
            original = safe_path(root / name, True)
            info = original.stat()
            require(stat.S_ISREG(info.st_mode) and info.st_size == len(content)
                    and original.read_bytes() == content and (0o755 if info.st_mode & 0o111 else 0o644) == mode,
                    "source changed during packaging: " + name)
        require(not out.exists() and not out.is_symlink(), "output appeared during packaging")
        with archive.open("rb") as handle:
            os.fsync(handle.fileno())
        os.link(archive, out)
        archive_digest = hashlib.sha256(out.read_bytes()).hexdigest()
    finally:
        shutil.rmtree(scratch)
    return {"status": "packaged-not-installed", "output": str(out), "sha256": archive_digest,
            "skill": root.name, "files": [{"path": name, "sha256": hashlib.sha256(content).hexdigest(), "size": len(content), "mode": mode}
                                           for name, content, mode in entries],
            "validation": validation, "behavioral_qualification": "not-run",
            "note": "Declared files only, fixed ZIP timestamps, regular 0644/0755 modes. Local resource checks do not prove dynamic dependencies or behavior. No installation or publication performed."}


def dispatch(argv=None):
    p = argparse.ArgumentParser(prog="hectl author", description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    q = sub.add_parser("init"); q.add_argument("--brief", required=True); q.add_argument("--output", required=True)
    q = sub.add_parser("check"); q.add_argument("skill"); q.add_argument("--host", choices=("portable", "codex", "claude-code"), default="portable")
    q = sub.add_parser("package"); q.add_argument("--skill", required=True); q.add_argument("--manifest", required=True); q.add_argument("--output", required=True); q.add_argument("--host", choices=("portable", "codex", "claude-code"), default="portable")
    args = p.parse_args(argv)
    try:
        if args.command == "init":
            result = initialize(args.brief, args.output)
        elif args.command == "package":
            result = package(args.skill, args.manifest, args.output, args.host)
        else:
            result = check_skill(safe_path(args.skill, True), args.host)
        print(json.dumps(result, indent=2))
        return 0 if args.command in ("init", "package") or result["ok"] else 1
    except (HectlError, OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(dispatch())
