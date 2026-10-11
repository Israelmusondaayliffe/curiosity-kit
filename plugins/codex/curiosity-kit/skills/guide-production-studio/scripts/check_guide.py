#!/usr/bin/env python3
"""Read-only declared-record, review, link and advisory checks. Python 3.9+."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


AUDIENCES = {"author", "presenter", "participant", "public"}


def strings(value):
    return isinstance(value, list) and all(isinstance(x, str) and x.strip() for x in value)


def member(value, allowed):
    return isinstance(value, str) and value in allowed


def local_file(root, name):
    if not isinstance(name, str) or not name.strip() or Path(name).is_absolute():
        raise ValueError("Expected a nonempty relative file path")
    try:
        root = Path(root).resolve()
        path = (root / name).resolve()
    except (OSError, RuntimeError):
        raise ValueError("File path cannot be resolved safely") from None
    try:
        path.relative_to(root)
    except ValueError:
        raise ValueError("File path leaves the allowed root")
    if not path.is_file():
        raise ValueError("Referenced file does not exist")
    return path


def index_rows(value, label, errors):
    if not isinstance(value, list):
        errors.append(label + " must be a list")
        return {}
    rows = {}
    for n, row in enumerate(value):
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"].strip():
            errors.append("{}[{}] needs a nonempty string id".format(label, n))
            continue
        if row["id"] in rows:
            errors.append(label + " has duplicate id " + row["id"])
        rows[row["id"]] = row
    return rows


def check_record(data, root):
    errors = []
    if not isinstance(data, dict):
        return ["Record must be an object"]
    sources = index_rows(data.get("sources"), "sources", errors)
    items = index_rows(data.get("items"), "items", errors)
    artifacts = index_rows(data.get("artifacts"), "artifacts", errors)
    for sid, source in sources.items():
        if type(source.get("may_inform")) is not bool:
            errors.append(sid + ": may_inform must be boolean")
        for field in ("direct_audiences", "transform_audiences"):
            val = source.get(field)
            if not strings(val) or any(a not in AUDIENCES for a in val):
                errors.append(sid + ": invalid " + field)
        if type(source.get("attribution_required")) is not bool:
            errors.append(sid + ": attribution_required must be boolean")
    for aid, artifact in artifacts.items():
        if not member(artifact.get("audience"), AUDIENCES):
            errors.append(aid + ": invalid artifact audience")
        try:
            local_file(root, artifact.get("path"))
        except ValueError as exc:
            errors.append(aid + ": " + str(exc))

    # Resolve indirect evidence too, so a public example cannot launder a private claim.
    closure_cache = {}

    def source_closure(iid, visiting):
        if iid in closure_cache:
            return closure_cache[iid]
        if iid in visiting:
            errors.append(iid + ": cyclic evidence reference")
            return set()
        item = items[iid]
        result = set(item.get("source_ids", [])) if strings(item.get("source_ids")) else set()
        refs = item.get("evidence_ids", [])
        if strings(refs):
            for ref in refs:
                if ref not in items:
                    errors.append(iid + ": unresolved evidence id " + ref)
                else:
                    result.update(source_closure(ref, visiting | {iid}))
        closure_cache[iid] = result
        return result

    for iid, item in items.items():
        if not member(item.get("kind"), {"claim", "example", "visual"}):
            errors.append(iid + ": kind must be claim, example or visual")
        for field in ("source_ids", "evidence_ids", "artifact_ids"):
            if not strings(item.get(field)):
                errors.append(iid + ": " + field + " must be a list of nonempty strings")
        mode = item.get("mode")
        if not member(mode, {"direct", "transform"}):
            errors.append(iid + ": mode must be direct or transform")
        state = item.get("state")
        if not member(state, {"observed", "documented", "derived", "illustrative", "unresolved"}):
            errors.append(iid + ": invalid evidence state")
        if state == "observed" and not (isinstance(item.get("observation"), str) and item["observation"].strip()):
            errors.append(iid + ": observed state needs an evidence description")
        source_ids = source_closure(iid, set())
        if not source_ids and state != "illustrative":
            errors.append(iid + ": non-illustrative item needs source evidence")
        aids = item.get("artifact_ids", [])
        audiences = set()
        if strings(aids):
            for aid in aids:
                if aid not in artifacts:
                    errors.append(iid + ": unresolved artifact id " + aid)
                else:
                    audience = artifacts[aid].get("audience")
                    if isinstance(audience, str):
                        audiences.add(audience)
        for sid in sorted(source_ids):
            if sid not in sources:
                errors.append(iid + ": unresolved source id " + sid)
                continue
            source = sources[sid]
            if source.get("may_inform") is not True:
                errors.append(iid + ": source " + sid + " is not permitted to inform")
            allowed = source.get(str(mode) + "_audiences", [])
            if not strings(allowed) or not audiences.issubset(set(allowed)):
                errors.append(iid + ": source " + sid + " disallows declared use/audience")
            if audiences & {"participant", "public"} and source.get("attribution_required") is True:
                if not (isinstance(item.get("attribution"), str) and item["attribution"].strip()):
                    errors.append(iid + ": required attribution is missing")
    return sorted(set(errors))


def check_review(data, root):
    errors = []
    if not isinstance(data, dict):
        return ["Review must be an object"]
    verdict = data.get("verdict")
    if not member(verdict, {"draft", "ready", "blocked"}):
        errors.append("Invalid verdict")
    kind = data.get("kind")
    if not member(kind, {"author", "independent", "human"}):
        errors.append("Invalid review kind")
    evidence = data.get("evidence")
    if not strings(evidence):
        errors.append("evidence must be a list of descriptions")
    elif (member(kind, {"independent", "human"}) or verdict == "ready") and not evidence:
        errors.append("Claimed review needs actual evidence descriptions")
    criticals = data.get("unresolved_criticals")
    if not strings(criticals):
        errors.append("unresolved_criticals must be a list")
    elif criticals and verdict == "ready":
        errors.append("Ready verdict conflicts with unresolved critical failures")
    for field in ("learner_observed", "human_approved"):
        if type(data.get(field)) is not bool:
            errors.append(field + " must be boolean")
    if data.get("learner_observed") is True:
        if not (isinstance(data.get("learner_evidence"), str) and data["learner_evidence"].strip()):
            errors.append("Learner observation claim needs actual evidence")
    if data.get("human_approved") is True:
        decision = data.get("human_decision")
        if not isinstance(decision, dict) or not all(isinstance(decision.get(k), str) and decision[k].strip() for k in ("by", "date", "evidence")) or decision.get("decision") != "approved":
            errors.append("Human approval claim needs a recorded approved decision")
    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("Review needs at least one exact artifact")
    else:
        for n, artifact in enumerate(artifacts):
            if not isinstance(artifact, dict):
                errors.append("Invalid artifact at index " + str(n))
                continue
            try:
                path = local_file(root, artifact.get("path"))
                expected = artifact.get("sha256")
                if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
                    errors.append("Artifact needs a lowercase SHA256")
                elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    errors.append("Reviewed artifact bytes have changed at index " + str(n))
            except ValueError as exc:
                errors.append("Artifact {}: {}".format(n, exc))
    return errors


def scan_text(text, audience="participant", excluded=()):
    patterns = [("private-path", r"(?:/Users/|/home/|/workspace/|\.codex/|\.claude/|CODEX-OUTPUTS/|CLAUDE-OUTPUTS/)")]
    patterns += [("unfinished-placeholder", r"(?:\bTODO\b|\bTBD\b|\[INSERT[^\]]*\])")]
    if audience in {"participant", "public"}:
        patterns += [("possible-production-note", r"(?:internal reviewer|author-only|private presenter notes)")]
    findings = []
    for number, line in enumerate(text.splitlines(), 1):
        for category, pattern in patterns:
            if re.search(pattern, line, re.I):
                findings.append({"line": number, "category": category})
        if any(value and value in line for value in excluded):
            findings.append({"line": number, "category": "excluded-text"})
    return findings


def check_links(path, root):
    errors = []
    root = Path(root).resolve()
    path = Path(path).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return ["Input file leaves the allowed root"]
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for target in re.findall(r"\]\(([^\s)]+)\)", line):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            candidate = path.parent / unquote(parsed.path)
            try:
                local_file(root, str(candidate.relative_to(root)))
            except (ValueError, OSError):
                errors.append("Line {}: missing or out-of-root local link".format(n))
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("record", "review", "scan", "links"))
    parser.add_argument("file")
    parser.add_argument("--root", default=".")
    parser.add_argument("--audience", choices=sorted(AUDIENCES), default="participant")
    parser.add_argument("--exclude-file", help="UTF-8 file containing one sensitive literal per line; contents are never printed")
    args = parser.parse_args(argv)
    try:
        path = Path(args.file)
        if args.mode == "scan":
            excluded = Path(args.exclude_file).read_text(encoding="utf-8").splitlines() if args.exclude_file else []
            findings = scan_text(path.read_text(encoding="utf-8"), args.audience, excluded)
            print(json.dumps({"status": "warnings" if findings else "no-pattern-warnings", "findings": findings,
                              "limit": "Advisory patterns only; no privacy, rights or completion certification."}, indent=2))
            return 1 if findings else 0
        if args.mode == "links":
            errors = check_links(path, args.root)
        else:
            data = json.loads(path.read_text(encoding="utf-8"))
            errors = check_record(data, args.root) if args.mode == "record" else check_review(data, args.root)
        print(json.dumps({"status": "invalid" if errors else "consistent", "errors": errors,
                          "limit": "Declared structure/bytes only; evidence truth, permission and quality need actual review."}, indent=2))
        return 1 if errors else 0
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        # Do not echo input excerpts, sensitive paths or JSON parse snippets.
        print(json.dumps({"status": "input-error", "error_type": type(exc).__name__}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
