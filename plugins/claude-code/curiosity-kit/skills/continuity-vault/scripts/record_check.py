#!/usr/bin/env python3
"""Read one bounded JSON record; check recorded structure and internal consistency.

No source lookup, artifact write, command execution, approval, or truth verification.
See ../references/record-checks.md for the complete version 1 contract.
"""

import datetime
import json
import os
from pathlib import Path
import re
import stat
import sys

MAX_BYTES = 1024 * 1024
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
AUDIENCE = re.compile(r"(?:public|(?:person|group):[A-Za-z0-9][A-Za-z0-9._:@/-]{0,199})\Z")
UNVERIFIED = ["actual_permission", "actual_user_selection", "source_truth",
              "semantic_support", "artifact_existence", "redaction_completeness"]


class DuplicateKey(ValueError):
    pass


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKey("duplicate JSON object key: " + key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("non-JSON numeric constant: " + value)


def read_input(name):
    """Open each path component without following symlinks, on POSIX hosts."""
    path = Path(name)
    if ".." in path.parts:
        raise OSError("input path must not contain '..'")
    path = Path(os.path.abspath(name))
    if not hasattr(os, "O_NOFOLLOW") or os.open not in os.supports_dir_fd:
        raise OSError("this host lacks the required no-symlink file-open support")
    directory = os.open(path.anchor, os.O_RDONLY | os.O_DIRECTORY)
    descriptor = None
    try:
        for part in path.parts[1:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=directory)
            os.close(directory)
            directory = child
        if len(path.parts) < 2:
            raise OSError("input must be a regular file")
        descriptor = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                             dir_fd=directory)
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise OSError("input must be a regular file")
        if before.st_size > MAX_BYTES:
            raise OSError("input exceeds the 1 MiB limit")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = None
            data = stream.read(MAX_BYTES + 1)
            after = os.fstat(stream.fileno())
        if len(data) > MAX_BYTES:
            raise OSError("input exceeds the 1 MiB limit")
        if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
                after.st_size, after.st_mtime_ns, after.st_ctime_ns):
            raise OSError("input changed while being read; retry a stable copy")
        return data.decode("utf-8")
    finally:
        if descriptor is not None:
            os.close(descriptor)
        os.close(directory)


class Check:
    def __init__(self):
        self.errors = []
        self.ids = set()

    def error(self, path, message):
        # Keep malformed-file diagnostics bounded as well as the input.
        if len(self.errors) < 100:
            self.errors.append({"path": path, "message": message})

    def obj(self, value, path, fields):
        if not isinstance(value, dict):
            self.error(path, "must be an object")
            return False
        for key in fields:
            if key not in value:
                self.error(path + "." + key, "required field is missing")
        for key in value:
            if key not in fields:
                self.error(path + "." + key, "unknown field in record version 1")
        return True

    def text(self, value, path, nullable=False):
        if nullable and value is None:
            return True
        if not isinstance(value, str) or not value.strip():
            self.error(path, "must be a nonblank string" + (" or null" if nullable else ""))
            return False
        return True

    def enum(self, value, path, options):
        if not isinstance(value, str) or value not in options:
            self.error(path, "must be one of: " + ", ".join(options))

    def boolean(self, value, path):
        if type(value) is not bool:
            self.error(path, "must be a boolean")

    def date(self, value, path, nullable=False):
        if nullable and value is None:
            return
        if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            try:
                datetime.date.fromisoformat(value)
                return
            except ValueError:
                pass
        self.error(path, "must be an actual YYYY-MM-DD date" + (" or null" if nullable else ""))

    def identifier(self, value, path, register=False):
        if not isinstance(value, str) or not ID.fullmatch(value):
            self.error(path, "must be a 1-128 character identifier using letters, digits, . _ : -")
            return
        if register:
            if value in self.ids:
                self.error(path, "duplicate ID across this record: " + value)
            self.ids.add(value)

    def strings(self, value, path, nonempty=False, identifiers=False, audiences=False):
        if not isinstance(value, list):
            self.error(path, "must be a list")
            return []
        if nonempty and not value:
            self.error(path, "must not be empty")
        seen = set()
        for index, entry in enumerate(value):
            where = "%s[%d]" % (path, index)
            if not self.text(entry, where):
                continue
            if entry in seen:
                self.error(where, "duplicate list entry")
            seen.add(entry)
            if identifiers:
                self.identifier(entry, where)
            if audiences and not AUDIENCE.fullmatch(entry):
                self.error(where, "use public, person:<stable-id>, or group:<stable-id>; ambiguous audiences are invalid")
        return value

    def rows(self, value, path, fields):
        if not isinstance(value, list):
            self.error(path, "must be a list")
            return []
        good = []
        for index, row in enumerate(value):
            where = "%s[%d]" % (path, index)
            if self.obj(row, where, fields):
                self.identifier(row.get("id"), where + ".id", register=True)
                good.append((row, where))
        return good

    def sources(self, data):
        rows = self.rows(data.get("sources"), "$.sources", ("id", "location", "version", "status"))
        if not rows:
            self.error("$.sources", "declare at least one bounded source, including a missing source if blocked")
        for row, path in rows:
            self.text(row.get("location"), path + ".location")
            self.text(row.get("version"), path + ".version", nullable=True)
            self.enum(row.get("status"), path + ".status", ("available", "missing"))
        return rows

    def known_value(self, row, key, path):
        value = row.get(key)
        evidence = row.get(key + "_evidence")
        if key == "date":
            self.date(value, path + ".date", nullable=True)
        else:
            self.text(value, path + "." + key, nullable=True)
        self.text(evidence, path + "." + key + "_evidence", nullable=True)
        if value is None and evidence is not None:
            self.error(path + "." + key + "_evidence", "must be null when the value is unknown")
        if value is not None and evidence is None:
            self.error(path + "." + key + "_evidence", "recorded values need evidence; use null for unknown values")

    def session(self, data, source_rows):
        meta = data.get("session")
        if self.obj(meta, "$.session", ("id", "purpose", "participants", "date", "completeness")):
            self.identifier(meta.get("id"), "$.session.id", register=True)
            self.text(meta.get("purpose"), "$.session.purpose")
            self.strings(meta.get("participants"), "$.session.participants")
            self.date(meta.get("date"), "$.session.date", nullable=True)
            self.enum(meta.get("completeness"), "$.session.completeness", ("complete", "partial", "unknown"))
        items = self.rows(data.get("items"), "$.items", (
            "id", "kind", "content", "source_id", "evidence", "reuse", "reuse_reason", "audience",
            "attribution", "deidentify", "identifiers", "owner", "owner_evidence", "date", "date_evidence"))
        for row, path in items:
            self.enum(row.get("kind"), path + ".kind", ("decision", "follow_up", "knowledge", "proposal", "fiction"))
            for key in ("content", "evidence"):
                self.text(row.get(key), path + "." + key)
            self.identifier(row.get("source_id"), path + ".source_id")
            self.enum(row.get("reuse"), path + ".reuse", ("allowed", "restricted", "unknown", "prohibited"))
            self.text(row.get("reuse_reason"), path + ".reuse_reason", nullable=True)
            self.strings(row.get("audience"), path + ".audience", audiences=True)
            self.text(row.get("attribution"), path + ".attribution", nullable=True)
            self.enum(row.get("deidentify"), path + ".deidentify", ("permitted", "required", "prohibited", "unknown"))
            self.strings(row.get("identifiers"), path + ".identifiers")
            self.known_value(row, "owner", path)
            self.known_value(row, "date", path)
        candidates = self.rows(data.get("candidates"), "$.candidates", (
            "id", "description", "item_ids", "audience", "selected", "selection_evidence", "state", "reason"))
        for row, path in candidates:
            self.text(row.get("description"), path + ".description")
            self.strings(row.get("item_ids"), path + ".item_ids", nonempty=True, identifiers=True)
            self.strings(row.get("audience"), path + ".audience", audiences=True)
            self.boolean(row.get("selected"), path + ".selected")
            self.text(row.get("selection_evidence"), path + ".selection_evidence", nullable=True)
            self.enum(row.get("state"), path + ".state", ("proposed", "blocked", "created"))
            self.text(row.get("reason"), path + ".reason", nullable=True)
        outputs = self.rows(data.get("outputs"), "$.outputs", (
            "id", "candidate_id", "item_ids", "audience", "location", "content", "deidentified", "redaction_note"))
        for row, path in outputs:
            self.identifier(row.get("candidate_id"), path + ".candidate_id")
            self.strings(row.get("item_ids"), path + ".item_ids", nonempty=True, identifiers=True)
            self.strings(row.get("audience"), path + ".audience", nonempty=True, audiences=True)
            for key in ("location", "content"):
                self.text(row.get(key), path + "." + key)
            self.boolean(row.get("deidentified"), path + ".deidentified")
            self.text(row.get("redaction_note"), path + ".redaction_note", nullable=True)
        self.text(data.get("no_output_reason"), "$.no_output_reason", nullable=True)
        if self.errors:
            return
        sources = {row["id"]: row for row, _ in source_rows}
        by_item = {row["id"]: row for row, _ in items}
        by_candidate = {row["id"]: row for row, _ in candidates}
        for row, path in items:
            if row["source_id"] not in sources:
                self.error(path + ".source_id", "must name a declared source")
            if row["reuse"] in ("unknown", "prohibited") and row["audience"]:
                self.error(path + ".audience", "must be empty for unknown or prohibited reuse")
            if row["reuse"] in ("allowed", "restricted") and not row["audience"]:
                self.error(path + ".audience", "reusable items need a specific audience")
            if row["reuse"] != "allowed" and row["reuse_reason"] is None:
                self.error(path + ".reuse_reason", "record the restriction or what remains unknown")
            if row["deidentify"] == "required" and not row["identifiers"]:
                self.error(path + ".identifiers", "required de-identification needs concrete terms to omit")
        if not candidates and data["no_output_reason"] is None:
            self.error("$.no_output_reason", "explain an inspected session with no candidates")
        if candidates and data["no_output_reason"] is not None:
            self.error("$.no_output_reason", "must be null when candidates are recorded")
        counts = {row["id"]: 0 for row, _ in candidates}
        for row, path in candidates:
            if row["selected"] != (row["selection_evidence"] is not None):
                self.error(path + ".selection_evidence", "selection evidence is required exactly when selected is true")
            if row["state"] == "blocked":
                if row["reason"] is None:
                    self.error(path + ".reason", "blocked candidates need a clearing condition or prohibition reason")
            elif row["reason"] is not None:
                self.error(path + ".reason", "must be null for proposed or created candidates")
            problems = []
            if not row["audience"]:
                problems.append("no specific audience")
            for item_id in row["item_ids"]:
                item = by_item.get(item_id)
                if item is None:
                    self.error(path + ".item_ids", "unknown source item: " + item_id)
                    continue
                source = sources.get(item["source_id"])
                if source is None or source["status"] != "available":
                    problems.append("unavailable source for " + item_id)
                if item["reuse"] not in ("allowed", "restricted"):
                    problems.append("reuse is " + item["reuse"] + " for " + item_id)
                if not set(row["audience"]).issubset(item["audience"]):
                    problems.append("audience exceeds recorded scope for " + item_id)
            if problems and row["state"] != "blocked":
                self.error(path + ".state", "must be blocked: " + "; ".join(problems))
            if row["state"] == "created" and not row["selected"]:
                self.error(path + ".selected", "created candidates must be selected")
        for row, path in outputs:
            candidate = by_candidate.get(row["candidate_id"])
            if candidate is None:
                self.error(path + ".candidate_id", "must name a declared candidate")
                continue
            counts[candidate["id"]] += 1
            if candidate["state"] != "created" or not candidate["selected"]:
                self.error(path + ".candidate_id", "an output needs a selected candidate in created state")
            if set(row["item_ids"]) != set(candidate["item_ids"]):
                self.error(path + ".item_ids", "must exactly match the selected candidate's source item set")
            if set(row["audience"]) != set(candidate["audience"]):
                self.error(path + ".audience", "must exactly match the selected candidate's audience")
            terms = []
            for item_id in row["item_ids"]:
                item = by_item.get(item_id)
                if item is None:
                    self.error(path + ".item_ids", "unknown source item: " + item_id)
                    continue
                if item["attribution"] is not None and item["attribution"] not in row["content"]:
                    self.error(path + ".content", "missing required attribution text for " + item_id)
                if item["deidentify"] == "required" and not row["deidentified"]:
                    self.error(path + ".deidentified", "required for " + item_id)
                if row["deidentified"] and item["deidentify"] not in ("permitted", "required"):
                    self.error(path + ".deidentified", "de-identification is not recorded as permitted for " + item_id)
                terms.extend(item["identifiers"])
            if row["deidentified"]:
                if not terms or row["redaction_note"] is None:
                    self.error(path + ".redaction_note", "a de-identification claim needs listed identifiers and a concrete change note")
                for term in terms:
                    if term.casefold() in row["content"].casefold():
                        self.error(path + ".content", "still contains a listed identifier")
            elif row["redaction_note"] is not None:
                self.error(path + ".redaction_note", "must be null when deidentified is false")
        for row, path in candidates:
            expected = 1 if row["state"] == "created" else 0
            if counts[row["id"]] != expected:
                self.error(path + ".state", "created means exactly one output; proposed or blocked means none")

    def audit(self, data, source_rows):
        self.text(data.get("scope"), "$.scope")
        self.date(data.get("reviewed_at"), "$.reviewed_at")
        self.enum(data.get("result"), "$.result", ("clear", "needs_review", "blocked"))
        self.text(data.get("block_reason"), "$.block_reason", nullable=True)
        findings = self.rows(data.get("findings"), "$.findings", (
            "id", "source_ids", "claim", "evidence", "consequence", "action", "blocking"))
        for row, path in findings:
            self.strings(row.get("source_ids"), path + ".source_ids", nonempty=True, identifiers=True)
            for key in ("claim", "evidence", "consequence", "action"):
                self.text(row.get(key), path + "." + key)
            self.boolean(row.get("blocking"), path + ".blocking")
        if self.errors:
            return
        source_ids = {row["id"] for row, _ in source_rows}
        for row, path in findings:
            for source_id in row["source_ids"]:
                if source_id not in source_ids:
                    self.error(path + ".source_ids", "unknown source: " + source_id)
        blocked = any(row["status"] == "missing" for row, _ in source_rows) or any(
            row["blocking"] for row, _ in findings)
        if data["result"] == "clear" and findings:
            self.error("$.result", "clear requires zero findings")
        if data["result"] == "needs_review" and not findings:
            self.error("$.findings", "needs_review requires a finding")
        if blocked and data["result"] != "blocked":
            self.error("$.result", "missing bounded sources or blocking findings require blocked")
        if data["result"] == "blocked" and data["block_reason"] is None:
            self.error("$.block_reason", "blocked audits need a reason and clearing condition")
        if data["result"] != "blocked" and data["block_reason"] is not None:
            self.error("$.block_reason", "must be null unless the result is blocked")

    def run(self, data):
        if not isinstance(data, dict):
            self.error("$", "record must be an object")
            return
        kind = data.get("kind")
        self.enum(kind, "$.kind", ("session", "audit"))
        if type(data.get("version")) is not int or data["version"] != 1:
            self.error("$.version", "must be integer 1")
        if kind not in ("session", "audit"):
            return
        fields = ("version", "kind", "sources") + (
            ("session", "items", "candidates", "outputs", "no_output_reason") if kind == "session"
            else ("scope", "reviewed_at", "result", "block_reason", "findings"))
        self.obj(data, "$", fields)
        sources = self.sources(data)
        if kind == "session":
            self.session(data, sources)
        else:
            self.audit(data, sources)


def emit(errors, kind=None):
    print(json.dumps({"record_valid": not errors, "check_scope": "structural_consistency_only",
                      "record_kind": kind, "unverified": UNVERIFIED, "errors": errors},
                     ensure_ascii=True, indent=2))


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if args == ["--help"]:
        print(json.dumps({"usage": "python3 /path/to/continuity-vault/scripts/record_check.py RECORD.json",
                          "scope": "Read-only structural consistency checks. No permission or readiness decision.",
                          "exit_codes": {"0": "consistent record, including safely blocked records",
                                         "1": "record inconsistency, including duplicate JSON keys",
                                         "2": "unreadable input, invalid JSON, or invalid CLI"}}, indent=2))
        return 0
    if len(args) != 1 or args[0].startswith("-"):
        emit([{"path": "$cli", "message": "expected one input path; use --help"}])
        return 2
    try:
        data = json.loads(read_input(args[0]), object_pairs_hook=unique_object,
                          parse_constant=reject_constant)
    except DuplicateKey as exc:
        emit([{"path": "$", "message": str(exc)}])
        return 1
    except (OSError, ValueError, RecursionError, OverflowError) as exc:
        emit([{"path": "$input", "message": str(exc)}])
        return 2
    check = Check()
    check.run(data)
    kind = data.get("kind") if isinstance(data, dict) and isinstance(data.get("kind"), str) else None
    emit(check.errors, kind)
    return 1 if check.errors else 0


if __name__ == "__main__":
    sys.exit(main())
