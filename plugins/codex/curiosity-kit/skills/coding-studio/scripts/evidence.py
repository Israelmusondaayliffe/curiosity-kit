#!/usr/bin/env python3
"""Compare explicitly selected file bytes and caller-supplied context. Python 3.9+."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

FORMAT = "coding-studio-selected-inputs-v1"
MAX_FILES = 512
MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_TOTAL_BYTES = 256 * 1024 * 1024
MAX_JSON_BYTES = 1024 * 1024
CHUNK = 1024 * 1024


class Invalid(Exception):
    pass


class Missing(Invalid):
    pass


def absolute(value):
    return Path(os.path.abspath(value))


def identity(info):
    return info.st_dev, info.st_ino, info.st_mode


def signature(info):
    return identity(info) + (info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def inspect_path(path, kind="file"):
    """Reject symlinks, special files and non-directory ancestors before opening."""
    ancestors = []
    for part in reversed((path,) + tuple(path.parents)):
        try:
            info = part.lstat()
        except FileNotFoundError:
            raise Missing("missing input: {}".format(path))
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise Invalid("symlink or reparse point is not allowed: {}".format(part))
        expected = stat.S_ISDIR if part != path or kind == "directory" else stat.S_ISREG
        if not expected(info.st_mode):
            raise Invalid("not a regular {}: {}".format(kind if part == path else "directory", part))
        ancestors.append((str(part), identity(info)))
    return info, ancestors


def same_state(path, before, chain):
    after, current_chain = inspect_path(path)
    if signature(before) != signature(after) or chain != current_chain:
        raise Invalid("input changed while being read: {}".format(path))


def read_file(path, limit, keep=False):
    before, chain = inspect_path(path)
    if before.st_size > limit:
        raise Invalid("input exceeds {} byte limit: {}".format(limit, path))
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    flags |= getattr(os, "O_NONBLOCK", 0)
    fd = os.open(str(path), flags)
    digest, count, chunks = hashlib.sha256(), 0, []
    try:
        if signature(os.fstat(fd)) != signature(before):
            raise Invalid("input changed before read: {}".format(path))
        while True:
            block = os.read(fd, min(CHUNK, limit - count + 1))
            if not block:
                break
            count += len(block)
            if count > limit:
                raise Invalid("input exceeds {} byte limit: {}".format(limit, path))
            digest.update(block)
            if keep:
                chunks.append(block)
        if count != before.st_size or signature(os.fstat(fd)) != signature(before):
            raise Invalid("input changed while being read: {}".format(path))
        same_state(path, before, chain)
    finally:
        os.close(fd)
    return {"bytes": count, "sha256": digest.hexdigest()}, b"".join(chunks), (path, before, chain)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Invalid("duplicate JSON key: {}".format(key))
        result[key] = value
    return result


def bad_constant(value):
    raise Invalid("non-finite JSON value: {}".format(value))


def read_json(path):
    _, contents, observed = read_file(path, MAX_JSON_BYTES, keep=True)
    try:
        result = json.loads(contents.decode("utf-8"), object_pairs_hook=unique_object,
                            parse_constant=bad_constant)
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise Invalid("invalid UTF-8 JSON in {}: {}".format(path, exc))
    return result, observed


def context_file(path):
    value, observed = read_json(absolute(path))
    if not isinstance(value, dict) or any(not isinstance(v, str) for v in value.values()):
        raise Invalid("context must be a JSON object with string values")
    return value, observed


def relative_name(value):
    if (not isinstance(value, str) or not value or len(value) > 4096
            or value.startswith("/") or "\\" in value or ":" in value
            or any(ord(c) < 32 or ord(c) == 127 for c in value)
            or any(part in ("", ".", "..") for part in value.split("/"))):
        raise Invalid("file path must be a literal normalized relative path: {!r}".format(value))
    return value


def selected_names(names):
    if not names or len(names) > MAX_FILES:
        raise Invalid("select between 1 and {} files".format(MAX_FILES))
    checked = [relative_name(name) for name in names]
    if len(checked) != len(set(os.path.normcase(name) for name in checked)):
        raise Invalid("duplicate selected file path")
    return checked


def root_path(value):
    path = absolute(value)
    inspect_path(path, "directory")
    return path


def validate_snapshot(value):
    if not isinstance(value, dict) or set(value) != {"format", "root", "files", "context"}:
        raise Invalid("snapshot requires exactly format, root, files and context")
    if value["format"] != FORMAT:
        raise Invalid("unsupported snapshot format")
    root = value["root"]
    if not isinstance(root, str) or not os.path.isabs(root) or "\x00" in root:
        raise Invalid("snapshot root must be an absolute path")
    context = value["context"]
    if context is not None and (not isinstance(context, dict)
                               or any(not isinstance(v, str) for v in context.values())):
        raise Invalid("snapshot context must be null or an object with string values")
    rows = value["files"]
    if not isinstance(rows, list):
        raise Invalid("snapshot files must be a list")
    names, total = [], 0
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "bytes", "sha256"}:
            raise Invalid("each file requires exactly path, bytes and sha256")
        if type(row["bytes"]) is not int or not 0 <= row["bytes"] <= MAX_FILE_BYTES:
            raise Invalid("invalid snapshot byte count")
        if not isinstance(row["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", row["sha256"]):
            raise Invalid("invalid snapshot SHA-256")
        names.append(row["path"])
        total += row["bytes"]
    selected_names(names)
    if total > MAX_TOTAL_BYTES:
        raise Invalid("snapshot exceeds total byte limit")
    return value


def emit(value):
    print(json.dumps(value, ensure_ascii=True, sort_keys=True))


def snapshot(args):
    root = root_path(args.root)
    names = selected_names(args.file)
    out = absolute(args.out)
    inspect_path(out.parent, "directory")
    if os.path.lexists(out):
        raise Invalid("output already exists; refusing overwrite: {}".format(out))
    paths = [root.joinpath(*name.split("/")) for name in names]
    context_path = absolute(args.context) if args.context is not None else None
    if out in paths or out == context_path:
        raise Invalid("snapshot output collides with an input")
    context, observations = None, []
    if context_path is not None:
        context, observed = context_file(context_path)
        observations.append(observed)
    rows, total = [], 0
    for name, path in zip(names, paths):
        data, _, observed = read_file(path, min(MAX_FILE_BYTES, MAX_TOTAL_BYTES - total))
        rows.append(dict(path=name, **data))
        observations.append(observed)
        total += data["bytes"]
        if total > MAX_TOTAL_BYTES:
            raise Invalid("selected files exceed {} total bytes".format(MAX_TOTAL_BYTES))
    value = {"format": FORMAT, "root": str(root), "files": rows, "context": context}
    payload = (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + "\n").encode("utf-8")
    if len(payload) > MAX_JSON_BYTES:
        raise Invalid("snapshot JSON exceeds {} bytes".format(MAX_JSON_BYTES))
    # Validate all inputs again before the only write. This is not an atomic filesystem snapshot.
    for observed in observations:
        same_state(*observed)
    inspect_path(out.parent, "directory")
    # Exclusive creation also rejects an output created since the preflight check.
    with out.open("xb") as handle:
        handle.write(payload)
    emit({"status": "snapshotted", "snapshot": str(out), "files": len(rows),
          "bytes": total, "context": "recorded" if context is not None else "not_recorded"})
    return 0


def check(args):
    value, snapshot_observed = read_json(absolute(args.snapshot))
    value = validate_snapshot(value)
    root = root_path(args.root if args.root is not None else value["root"])
    observations = [snapshot_observed]
    context, differences, unavailable = None, [], []
    if args.context is not None:
        context, observed = context_file(args.context)
        observations.append(observed)
    elif value["context"] is not None:
        raise Invalid("current context is required; supply --context JSONFILE")
    if context != value["context"]:
        expected, actual = value["context"] or {}, context or {}
        keys = sorted(k for k in set(expected) | set(actual) if expected.get(k) != actual.get(k))
        differences.append({"kind": "context", "keys": keys,
                            "recorded": value["context"] is not None,
                            "supplied": args.context is not None})
    total = 0
    for row in value["files"]:
        path = root.joinpath(*row["path"].split("/"))
        try:
            actual, _, observed = read_file(path, min(MAX_FILE_BYTES, MAX_TOTAL_BYTES - total))
            observations.append(observed)
            total += actual["bytes"]
            if total > MAX_TOTAL_BYTES:
                raise Invalid("current selected files exceed total byte limit")
            if actual != {"bytes": row["bytes"], "sha256": row["sha256"]}:
                differences.append({"kind": "changed", "path": row["path"], "actual": actual})
        except Missing:
            differences.append({"kind": "missing", "path": row["path"]})
        except (Invalid, OSError) as exc:
            unavailable.append({"path": row["path"], "error": str(exc)})
    for observed in observations:
        same_state(*observed)
    status = "unavailable" if unavailable else "drift" if differences else "match"
    emit({"status": status, "root": str(root), "files": len(value["files"]),
          "context": "compared" if args.context is not None else "not_recorded",
          "differences": differences, "unavailable": unavailable,
          "scope": "Only listed files and supplied context; unlisted inputs are unknown."})
    return 2 if unavailable else 1 if differences else 0


class Once(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if getattr(namespace, self.dest, None) is not None:
            parser.error("{} may be supplied only once".format(option_string))
        setattr(namespace, self.dest, value)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    commands = parser.add_subparsers(dest="command", required=True)
    take = commands.add_parser("snapshot", allow_abbrev=False)
    take.add_argument("--root", required=True, action=Once)
    take.add_argument("--file", action="append", required=True, metavar="REL")
    take.add_argument("--out", required=True, action=Once)
    take.add_argument("--context", metavar="JSONFILE", action=Once)
    verify = commands.add_parser("check", allow_abbrev=False)
    verify.add_argument("snapshot", metavar="SNAPSHOT")
    verify.add_argument("--root", action=Once)
    verify.add_argument("--context", metavar="JSONFILE", action=Once)
    args = parser.parse_args(argv)
    try:
        return snapshot(args) if args.command == "snapshot" else check(args)
    except (Invalid, OSError, ValueError, RecursionError) as exc:
        print("error: {}".format(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
