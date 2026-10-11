#!/usr/bin/env python3
"""Check one optional evidence record; no truth, approval or delivery certification."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import stat
import sys

MAX_RECORD_BYTES = 1024 * 1024
MAX_ARTIFACT_BYTES = 32 * 1024 * 1024
ID = re.compile(r"[SC][1-9][0-9]*\Z")
MARKER = re.compile(r"\[\[(source|claim):([^\]\r\n]*)\]\]")
LIMITS = ("LIMITS: structural checks only; source truth, semantic support, arithmetic, "
          "freshness, complete claim coverage, rendering, review approval, consent, "
          "authority and delivery remain unchecked.")


class InvalidInput(ValueError):
    pass


def require(condition, location, message):
    if not condition:
        raise InvalidInput("{}: {}".format(location, message))


def fields(value, required, location):
    require(type(value) is dict, location, "expected object")
    require(set(value) == set(required.split()), location,
            "expected exactly these fields: " + required)


def text(value, location):
    require(type(value) is str and bool(value.strip()), location, "expected nonempty text")


def choice(value, options, location):
    require(type(value) is str and value in options.split(), location,
            "expected one of: " + options)


def strings(value, location):
    require(type(value) is list, location, "expected list")
    for i, item in enumerate(value):
        text(item, "{}[{}]".format(location, i))
    require(len(value) == len(set(value)), location, "duplicate list entries")


def date(value, location):
    text(value, location)
    if value == "unknown":
        return
    require(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)), location,
            "expected YYYY-MM-DD or unknown")
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        raise InvalidInput(location + ": invalid calendar date") from None


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InvalidInput("duplicate JSON key: " + key)
        result[key] = value
    return result


def bounded_read(path, limit):
    # Open only command-line paths. Refuse devices, directories and pipes.
    require(stat.S_ISREG(path.stat().st_mode), str(path), "expected regular file")
    with path.open("rb") as stream:
        data = stream.read(limit + 1)
    require(len(data) <= limit, str(path), "exceeds {} byte limit".format(limit))
    return data


def load_record(path):
    data = bounded_read(path, MAX_RECORD_BYTES)
    return json.loads(data.decode("utf-8"), object_pairs_hook=unique_object,
                      parse_constant=lambda value: reject_constant(value))


def reject_constant(value):
    raise InvalidInput("non-JSON constant: " + value)


def validate(record):
    """Return stable (label, location, detail) findings; reject malformed schemas."""
    fields(record, "version sources claims review", "record")
    require(type(record["version"]) is int and record["version"] == 1,
            "version", "expected integer 1")
    findings = []

    def find(label, location, detail):
        findings.append((label, location, detail))

    indexes = {}
    for group, prefix in (("sources", "S"), ("claims", "C")):
        require(type(record[group]) is list, group, "expected list")
        indexes[group] = {}
        for i, item in enumerate(record[group]):
            location = "{}[{}]".format(group, i)
            require(type(item) is dict, location, "expected object")
            identifier = item.get("id")
            require(type(identifier) is str and bool(ID.fullmatch(identifier))
                    and identifier.startswith(prefix), location, "invalid " + prefix + " ID")
            if identifier in indexes[group]:
                find("DUPLICATE_ID", location, identifier)
            indexes[group][identifier] = item
    sources, claims = indexes["sources"], indexes["claims"]
    for source in record["sources"]:
        loc = source["id"]
        fields(source, "id title location type access read_extent publication_date accessed_date origin_ids passages", loc)
        for key in ("title", "location", "read_extent"):
            text(source[key], loc + "." + key)
        choice(source["type"], "primary secondary discovery", loc + ".type")
        choice(source["access"], "full partial supplied unread inaccessible", loc + ".access")
        for key in ("publication_date", "accessed_date"):
            date(source[key], loc + "." + key)
        for key in ("origin_ids", "passages"):
            strings(source[key], loc + "." + key)
        for origin in source["origin_ids"]:
            if origin not in sources:
                find("UNKNOWN_ORIGIN", loc, origin)
            elif origin == loc:
                find("SELF_ORIGIN", loc, origin)
        read = source["access"] in {"full", "partial", "supplied"}
        if read and (source["read_extent"] == "none" or not source["passages"]):
            find("READ_EVIDENCE_MISSING", loc, "read access needs actual extent and passage locators")
        if not read and (source["read_extent"] != "none" or source["passages"]):
            find("UNREAD_EVIDENCE_CONFLICT", loc, "unread/inaccessible needs extent none and no passages")
    for claim in record["claims"]:
        loc = claim["id"]
        fields(claim, "id text status source_ids depends_on rationale counterevidence artifact_locations", loc)
        for key in ("text", "rationale"):
            text(claim[key], loc + "." + key)
        choice(claim["status"], "supported inferred disputed unresolved", loc + ".status")
        for key in ("source_ids", "depends_on", "counterevidence", "artifact_locations"):
            strings(claim[key], loc + "." + key)
        for key, known, label in (("source_ids", sources, "UNKNOWN_SOURCE"),
                                  ("depends_on", claims, "UNKNOWN_DEPENDENCY")):
            for ref in claim[key]:
                if ref not in known:
                    find(label, loc, ref)
        if claim["status"] != "unresolved" and not claim["source_ids"]:
            find("CLAIM_SOURCES_MISSING", loc, claim["status"] + " needs a source")
        if claim["status"] in {"supported", "inferred"} and not any(
                sources[ref]["access"] in {"full", "partial", "supplied"}
                and sources[ref]["type"] != "discovery" and sources[ref]["passages"]
                for ref in claim["source_ids"] if ref in sources):
            find("NO_READ_SUPPORT", loc, "needs at least one read, non-discovery source")
        if claim["status"] == "disputed" and not claim["counterevidence"]:
            find("COUNTEREVIDENCE_MISSING", loc, "name the conflicting passage or evidence")
    # Iterative graph walk bounds stack usage even for long material claim chains.
    finished = set()
    for start in claims:
        if start in finished:
            continue
        active = set()
        stack = [(start, False)]
        while stack:
            node, leaving = stack.pop()
            if leaving:
                active.discard(node)
                finished.add(node)
            elif node in active:
                find("DEPENDENCY_CYCLE", node, "claim dependencies must be acyclic")
            elif node not in finished:
                active.add(node)
                stack.append((node, True))
                stack.extend((ref, False) for ref in reversed(claims[node]["depends_on"]) if ref in claims)
    review = record["review"]
    fields(review, "reviewed_sha256 requirements_verdict evidence_verdict findings", "review")
    digest = review["reviewed_sha256"]
    require(type(digest) is str and (digest == "unknown" or bool(re.fullmatch(r"[0-9a-f]{64}", digest))),
            "review.reviewed_sha256", "expected lowercase SHA256 or unknown")
    for key in ("requirements_verdict", "evidence_verdict"):
        choice(review[key], "pass fail unreviewed", "review." + key)
        if review[key] != "pass":
            find("REVIEW_INCOMPLETE", "review." + key, review[key])
    require(type(review["findings"]) is list, "review.findings", "expected list")
    for i, issue in enumerate(review["findings"]):
        loc = "review.findings[{}]".format(i)
        fields(issue, "severity state location detail resolution", loc)
        choice(issue["severity"], "critical important minor", loc + ".severity")
        choice(issue["state"], "open resolved", loc + ".state")
        for key in ("location", "detail", "resolution"):
            text(issue[key], loc + "." + key)
        if issue["state"] == "open" and issue["severity"] in {"critical", "important"}:
            find("REVIEW_BLOCKER", loc, issue["severity"] + ": " + issue["detail"])
    return findings


def check_artifact(record, path):
    data = bounded_read(path, MAX_ARTIFACT_BYTES)
    findings = []
    if not data:
        findings.append(("EMPTY_ARTIFACT", str(path), "file has no bytes"))
    reviewed = record["review"]["reviewed_sha256"]
    if reviewed == "unknown":
        findings.append(("ARTIFACT_UNREVIEWED", str(path), "no reviewed SHA256 recorded"))
    elif hashlib.sha256(data).hexdigest() != reviewed:
        findings.append(("ARTIFACT_CHANGED", str(path), "bytes differ from recorded reviewed SHA256"))
    if path.suffix.lower() in {".md", ".markdown"}:
        content = data.decode("utf-8")
        known = {"source": {s["id"] for s in record["sources"]},
                 "claim": {c["id"] for c in record["claims"]}}
        for match in MARKER.finditer(content):
            kind, ref = match.groups()
            if ref not in known[kind]:
                findings.append(("UNKNOWN_ARTIFACT_REFERENCE", str(path), kind + ":" + ref))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, epilog=LIMITS)
    parser.add_argument("record", type=Path, help="explicit UTF-8 JSON record, at most 1 MiB")
    parser.add_argument("--artifact", type=Path, help="explicit artifact, at most 32 MiB; never read from record paths")
    args = parser.parse_args(argv)
    try:
        record = load_record(args.record)
        findings = validate(record)
        if args.artifact is not None:
            findings.extend(check_artifact(record, args.artifact))
        for label, location, detail in findings:
            print("{} {}: {}".format(label, location, detail))
        print("FINDINGS: {}".format(len(findings)) if findings else "CONSISTENT: checked structure only")
        if args.artifact is None:
            print("ARTIFACT_NOT_CHECKED: no --artifact supplied; review identity unverified")
        elif args.artifact.suffix.lower() not in {".md", ".markdown"}:
            print("ARTIFACT_IDENTITY_ONLY: non-Markdown content was not parsed or rendered")
        print(LIMITS)
        return 1 if findings else 0
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        print("INVALID_INPUT: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
