#!/usr/bin/env python3
"""Deterministic blind preparation and independent review gates (stdlib only).

The coordinator supplies dispatch receipts and freshly recomputed hashes, never
reviewer self-attestations. Receipt authenticity and actual host isolation remain
operational trust boundaries. Different directories do not establish blindness
or deny workers access to a shared filesystem. No models are called here.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import operator
import re
import struct
import sys
import zlib
from pathlib import Path


class ReviewError(ValueError):
    """Inputs cannot authorize a passing review."""


HASH = re.compile(r"sha256:[a-f0-9]{64}\Z")
ROLES = ("quality", "integrity")
RESULTS = ("pass", "fail", "cannot-verify")


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def string_list(value, minimum=0):
    return (isinstance(value, list) and len(value) >= minimum
            and all(nonempty(item) for item in value)
            and len(set(value)) == len(value))


def canonical_bytes(value):
    """Canonical strict JSON, rejecting non-string object keys and NaN."""
    def check(v):
        if isinstance(v, dict):
            if any(not isinstance(k, str) for k in v):
                raise ReviewError("JSON keys must be strings")
            for item in v.values():
                check(item)
        elif isinstance(v, list):
            for item in v:
                check(item)
        elif v is not None and type(v) not in (str, int, float, bool):
            raise ReviewError("value is not JSON-compatible")
    check(value)
    try:
        return json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (ValueError, UnicodeError) as exc:
        raise ReviewError(str(exc)) from exc


def hash_bytes(data):
    if not isinstance(data, bytes):
        raise ReviewError("hash_bytes requires bytes")
    return "sha256:" + hashlib.sha256(data).hexdigest()


def contract_hash(contract):
    """Hash every supplied field, not a selected success-criteria subsection.

    Coordinator must include all criteria, bar and test digests, acceptance rules,
    inspection methods, reader profiles/questions, constraints and review policy.
    Use freeze_contract for an explicit content-hashed dependency manifest.
    """
    if not isinstance(contract, dict) or not contract:
        raise ReviewError("contract must be a nonempty object")
    return hash_bytes(canonical_bytes(contract))


def freeze_contract(contract, root, files):
    """Return full contract plus hashes of every explicitly declared dependency.

    No external reads are inferred. Paths must resolve within root; symlinks are
    rejected so a dependency cannot silently escape the frozen tree. Include
    reader-question files, tests, benchmark inputs and reference artifacts.
    """
    contract_hash(contract)
    if not string_list(files, 1):
        raise ReviewError("files must be a nonempty unique path list")
    root = Path(root).resolve(strict=True)
    manifest = {}
    for name in sorted(files):
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ReviewError("dependency must be a relative contained path")
        path = root / relative
        if any(p.is_symlink() for p in [path, *path.parents] if p != root.parent):
            raise ReviewError("symlink dependency is not permitted")
        path.resolve(strict=True).relative_to(root)
        if not path.is_file():
            raise ReviewError("dependency is not a regular file: " + name)
        key = relative.as_posix()
        if key in manifest:
            raise ReviewError("duplicate normalized dependency path")
        manifest[key] = hash_bytes(path.read_bytes())
    return {"schema_version": 1, "contract": contract, "dependency_hashes": manifest}


def check_frozen_contract(frozen, root, expected_hash):
    """Re-read all frozen dependencies; editing a reader question changes result."""
    if not isinstance(frozen, dict) or not isinstance(frozen.get("dependency_hashes"), dict):
        raise ReviewError("frozen contract missing dependency_hashes")
    if not isinstance(expected_hash, str) or not HASH.fullmatch(expected_hash):
        raise ReviewError("expected hash must be a SHA-256 label")
    current = freeze_contract(frozen.get("contract"), root, list(frozen["dependency_hashes"]))
    recorded_hash, current_hash = contract_hash(frozen), contract_hash(current)
    return {"matched": recorded_hash == current_hash == expected_hash,
            "expected_hash": expected_hash, "recorded_hash": recorded_hash,
            "current_hash": current_hash,
            "changed_dependencies": [name for name, digest in current["dependency_hashes"].items()
                                     if frozen["dependency_hashes"].get(name) != digest]}


def prepare_reader_packet(artifact, reader_profile, questions):
    """Reader sees only full artifact, intended-reader profile and frozen questions.

    Does not infer or rewrite questions. Store the packet digest in the dispatch
    record; put the original question file digest in the evaluation contract.
    No goal, bar, round number, author, prior verdict or run state is included.
    """
    if not nonempty(reader_profile) or not string_list(questions, 1):
        raise ReviewError("reader profile and unique frozen questions are required")
    data, media, note = sanitize_artifact(artifact)
    return {"artifact": {"media_type": media, "content_base64": base64.b64encode(data).decode("ascii")},
            "reader_profile": reader_profile, "questions": list(questions),
            "instructions": "Answer these exact questions from the artifact alone. Quote locations. Record every guess, unanswered question or instruction you cannot follow.",
            "limitation": note}


def default_policy():
    """Source default; freeze 2+2 explicitly for a five-helper verification run."""
    return {"quality_count": 3, "integrity_count": 3,
            "quality_rule": "strict-majority", "integrity_rule": "all-pass",
            "cannot_verify_rule": "blocks", "consecutive_wins": 2}


def validate_policy(policy):
    if not isinstance(policy, dict):
        return ["policy must be an object"]
    errors = []
    for role in ROLES:
        count = policy.get(role + "_count")
        if type(count) is not int or count < 2:
            errors.append(role + "_count must be an integer >= 2")
    for key in ("quality_rule", "integrity_rule", "cannot_verify_rule"):
        if policy.get(key) != default_policy()[key]:
            errors.append("unsupported consensus policy: " + key)
    if type(policy.get("consecutive_wins", 2)) is not int or policy.get("consecutive_wins", 2) < 2:
        errors.append("consecutive_wins must be an integer >= 2")
    return errors


_METADATA = re.compile(r"^\s*(author|by|date|created|updated|modified|source|origin|file|filename|path|version|draft|generated(?:-by)?|model|agent|session|run(?:[-_]id)?|piece|round)\s*[:=]", re.I)
_PNG = b"\x89PNG\r\n\x1a\n"


def _sanitize_png(raw):
    """Strip only metadata-bearing ancillary chunks, verify complete PNG structure.

    This does not decode or certify pixels. Host must render and inspect output.
    Unsupported color-profile/animation PNGs must first be normalized by a real
    renderer; silently dropping a profile could change the comparison's colors.
    """
    allowed = {b"IHDR", b"PLTE", b"IDAT", b"IEND", b"tRNS", b"gAMA", b"cHRM", b"sRGB"}
    out, pos, kinds, idat_ended = bytearray(_PNG), 8, [], False
    while pos < len(raw):
        if pos + 12 > len(raw):
            raise ReviewError("truncated PNG chunk")
        size = struct.unpack(">I", raw[pos:pos + 4])[0]
        end = pos + 12 + size
        if end > len(raw):
            raise ReviewError("truncated PNG payload")
        kind, data = raw[pos + 4:pos + 8], raw[pos + 8:end - 4]
        if not re.fullmatch(b"[A-Za-z]{4}", kind):
            raise ReviewError("invalid PNG chunk type")
        if zlib.crc32(kind + data) & 0xffffffff != struct.unpack(">I", raw[end - 4:end])[0]:
            raise ReviewError("PNG CRC mismatch")
        if kind in {b"iCCP", b"acTL", b"fcTL", b"fdAT"}:
            raise ReviewError("render profile/animated PNG to a normalized static PNG first")
        if not kinds and kind != b"IHDR":
            raise ReviewError("PNG missing initial IHDR")
        if kind == b"IHDR":
            if kinds or size != 13:
                raise ReviewError("invalid PNG header")
            width, height, depth, color, compression, filtering, interlace = struct.unpack(">IIBBBBB", data)
            valid_depths = {0: {1, 2, 4, 8, 16}, 2: {8, 16}, 3: {1, 2, 4, 8}, 4: {8, 16}, 6: {8, 16}}
            if not width or not height or depth not in valid_depths.get(color, set()) or compression or filtering or interlace not in (0, 1):
                raise ReviewError("unsupported/invalid PNG header values")
        if kind not in allowed and not (kind[0] & 32):
            raise ReviewError("unknown critical PNG chunk")
        if kind == b"IDAT" and idat_ended:
            raise ReviewError("non-contiguous PNG image data")
        if b"IDAT" in kinds and kind != b"IDAT":
            idat_ended = True
        if kind in {b"PLTE", b"tRNS", b"gAMA", b"cHRM", b"sRGB"} and (kind in kinds or b"IDAT" in kinds):
            raise ReviewError("duplicate or misplaced PNG rendering chunk")
        if kind in allowed:
            out.extend(raw[pos:end])
        kinds.append(kind)
        pos = end
        if kind == b"IEND":
            if size or pos != len(raw):
                raise ReviewError("invalid PNG ending/trailing bytes")
            break
    if not kinds or kinds[-1] != b"IEND" or b"IDAT" not in kinds:
        raise ReviewError("incomplete PNG")
    return bytes(out)


def sanitize_artifact(raw):
    """Return bytes, media type and disclosure. Opaque binaries fail closed."""
    if not isinstance(raw, bytes) or not raw:
        raise ReviewError("artifact must contain bytes")
    if raw.startswith(_PNG):
        return _sanitize_png(raw), "image/png", "PNG metadata removed; pixels may reveal provenance. Pixel rendering still requires inspection."
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeError as exc:
        raise ReviewError("unsupported binary; provide normalized PNG or UTF-8 inspection output") from exc
    if any(ord(c) < 32 and c not in "\t\n\r" for c in text):
        raise ReviewError("binary/control bytes are not text inspection output")
    if text.lstrip().startswith(("%PDF", "<svg", "<?xml")):
        raise ReviewError("render document/vector formats to normalized PNG first")
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() in ("---", "...")), None)
        if end is None:
            raise ReviewError("unclosed metadata frontmatter")
        lines = lines[end + 1:]
    while lines:
        first = lines[0].strip()
        if not first or _METADATA.match(first):
            lines.pop(0)
        elif first.startswith("<!--"):
            end = next((i for i, line in enumerate(lines) if "-->" in line), None)
            if end is None or lines[end].split("-->", 1)[1].strip():
                raise ReviewError("ambiguous leading metadata comment")
            lines = lines[end + 1:]
        else:
            break
    cleaned = "\n".join(lines).strip("\n")
    if not cleaned.strip():
        raise ReviewError("artifact empty after metadata removal")
    return (cleaned + "\n").encode(), "text/plain", "Leading metadata removed; body content/style may still reveal provenance."


def prepare_blind_pair(ours, reference, contract, seed):
    """Pure packet/map construction; never include source paths or seed in packet.

    Only neutral goal/bar-description/acceptance strings enter the packet. Their
    author must remove provenance leaks before dispatch. Contract hashes remain
    in the coordinator envelope because they can fingerprint known sources.
    """
    if type(seed) is not int:
        raise ReviewError("seed must be an integer")
    contract_hash(contract)
    a, ma, na = sanitize_artifact(ours)
    b, mb, nb = sanitize_artifact(reference)
    if ma != mb:
        raise ReviewError("blind artifacts must share their inspection format")
    if ma == "image/png" and a[16:24] != b[16:24]:
        raise ReviewError("blind PNG artifacts must use identical viewport dimensions")
    ours_label = "A" if hashlib.sha256(str(seed).encode()).digest()[0] & 1 else "B"
    payloads = {ours_label: a, "B" if ours_label == "A" else "A": b}
    packet = {"schema_version": 1,
              "items": {key: {"media_type": ma, "content_base64": base64.b64encode(value).decode("ascii")}
                        for key, value in sorted(payloads.items())},
              "instructions": "Inspect both complete artifacts. Do not seek provenance. Return A, B, tie or unable_to_evaluate, with one largest actionable gap and gap_is_actionable; if the artifact you prefer has no material gap, say so and set gap_is_actionable false. Stop if forbidden context appears.",
              "limitations": sorted({na, nb})}
    for field in ("goal", "bar_description", "acceptance_criterion"):
        if not nonempty(contract.get(field)):
            raise ReviewError("blind contract missing " + field)
        packet[field] = contract[field]
    sealed = {"schema_version": 1, "seed": seed, "ours_label": ours_label,
              "contract_hash": contract_hash(contract),
              "source_hashes": {"ours": hash_bytes(ours), "reference": hash_bytes(reference)},
              "sanitized_hashes": {key: hash_bytes(value) for key, value in payloads.items()},
              "packet_hash": hash_bytes(canonical_bytes(packet))}
    return {"packet": packet, "sealed_map": sealed}


def write_blind_pair(prepared, packet_path, sealed_path):
    """Explicit exclusive artifact write, creating only requested parent directories.

    Different parent directories are organizational separation, NOT isolation.
    An interrupted write leaves an incomplete pair; refuse judgment until both
    files and their hashes validate. Never overwrite or alter canonical state.
    """
    packet_path, sealed_path = Path(packet_path).resolve(), Path(sealed_path).resolve()
    if (packet_path.parent == sealed_path.parent
            or packet_path.parent in sealed_path.parent.parents
            or sealed_path.parent in packet_path.parent.parents):
        raise ReviewError("packet/map must have separate non-nested parent directories")
    if packet_path.exists() or sealed_path.exists():
        raise ReviewError("refusing to overwrite sealed comparison")
    packet_bytes = canonical_bytes(prepared["packet"])
    map_bytes = canonical_bytes(prepared["sealed_map"])
    if hash_bytes(packet_bytes) != prepared["sealed_map"].get("packet_hash"):
        raise ReviewError("packet/map mismatch")
    for path, data in ((sealed_path, map_bytes), (packet_path, packet_bytes)):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(data + b"\n")
    return {"packet_path": str(packet_path), "packet_hash": hash_bytes(packet_bytes),
            "limitations": "Paths are separated; host access isolation is not established by this write."}


def validate_context(context, panel=False):
    if not isinstance(context, dict):
        return ["coordinator context must be an object"]
    errors = []
    for key in ("piece_id", "verification_id"):
        if not nonempty(context.get(key)):
            errors.append("missing coordinator " + key)
    for key in ("artifact_hash", "contract_hash"):
        if not isinstance(context.get(key), str) or not HASH.fullmatch(context[key]):
            errors.append("invalid coordinator " + key)
    for key in ("excluded_authors", "used_sessions"):
        if not string_list(context.get(key)):
            errors.append("coordinator " + key + " must be a unique string list")
    if not string_list(context.get("criteria_ids"), 1):
        errors.append("coordinator must supply unique frozen criteria_ids")
    manifest = context.get("evidence_manifest")
    if not isinstance(manifest, dict) or not manifest or any(not nonempty(k) or not isinstance(v, str) or not HASH.fullmatch(v) for k, v in manifest.items()):
        errors.append("coordinator must supply nonempty current evidence_manifest")
    if not isinstance(context.get("expected_sessions"), dict) or not context["expected_sessions"]:
        errors.append("coordinator must supply recorded dispatch receipts")
    if panel:
        if context.get("eligible") is not True:
            errors.append("required work is unready/capped or verification eligibility is unknown")
        if not string_list(context.get("required_perspectives"), 3):
            errors.append("panel requires at least three frozen perspectives")
        required = context.get("required_criteria_ids", context.get("criteria_ids"))
        if (not string_list(required) or not string_list(context.get("criteria_ids"), 1)
                or not set(required).issubset(context["criteria_ids"])):
            errors.append("required_criteria_ids must be a unique subset of frozen criteria_ids")
    return errors


def _binding_errors(verdict, context):
    errors = validate_context(context)
    if not isinstance(verdict, dict):
        return errors + ["verdict must be an object"]
    if errors:
        return errors
    for key in ("piece_id", "artifact_hash", "contract_hash", "verification_id"):
        if verdict.get(key) != context[key]:
            errors.append("missing/mismatched " + key)
    author, session = verdict.get("author_id"), verdict.get("session_id")
    if not nonempty(author) or not nonempty(session):
        errors.append("author_id and session_id required")
    if nonempty(author) and author in context["excluded_authors"]:
        errors.append("reviewer authored/built artifact or is excluded")
    if nonempty(session) and session in context["used_sessions"]:
        errors.append("stale/reused review session")
    receipt = context["expected_sessions"].get(session) if isinstance(session, str) else None
    if not isinstance(receipt, dict) or receipt.get("author_id") != author:
        errors.append("missing coordinator dispatch receipt")
    else:
        if receipt.get("fresh_context") is not True or type(receipt.get("inherited_turns")) is not int or receipt.get("inherited_turns") != 0:
            errors.append("fresh context not established by coordinator")
        if receipt.get("forbidden_context_seen") is not False:
            errors.append("forbidden context seen or unknown")
        if receipt.get("verification_id") != context["verification_id"]:
            errors.append("stale dispatch generation")
        if receipt.get("role") != verdict.get("verifier_type", "critic"):
            errors.append("review role does not match dispatch receipt")
        perspectives = verdict.get("perspectives")
        if not string_list(perspectives, 1) or not string_list(receipt.get("perspectives"), 1) or set(perspectives) != set(receipt["perspectives"]):
            errors.append("review perspectives must match recorded dispatch assignment")
    if verdict.get("plan_hash_matched") is not True:
        errors.append("frozen evaluation contract mismatch/unconfirmed")
    if not nonempty(verdict.get("reason")):
        errors.append("reason is required")
    evidence = verdict.get("evidence_inspected")
    if not isinstance(evidence, list) or not evidence:
        errors.append("inspection evidence required")
    else:
        seen = set()
        for row in evidence:
            if not isinstance(row, dict) or not nonempty(row.get("id")) or not nonempty(row.get("observation")):
                errors.append("evidence needs id, sha256 and concrete observation")
                continue
            eid = row["id"]
            if eid in seen:
                errors.append("duplicate evidence reference")
            seen.add(eid)
            if eid not in context["evidence_manifest"] or row.get("sha256") != context["evidence_manifest"].get(eid):
                errors.append("missing/stale evidence: " + eid)
    checked = verdict.get("criteria_checked")
    if not string_list(checked, 1) or set(checked) != set(context["criteria_ids"]):
        errors.append("review must cover every frozen criterion exactly once")
    return errors


def validate_critic(verdict, context):
    errors = _binding_errors(verdict, context)
    if not isinstance(verdict, dict):
        return errors
    if verdict.get("winner") not in ("A", "B", "tie", "unable_to_evaluate"):
        errors.append("invalid critic winner")
    if "winner_is_ours" in verdict:
        errors.append("critic must not declare candidate identity")
    gap, actionable = verdict.get("largest_gap"), verdict.get("gap_is_actionable")
    if verdict.get("winner") in ("A", "B"):
        # A decisive pick may honestly report no material gap; a verdict against the candidate is checked at unseal.
        if type(actionable) is not bool:
            errors.append("decisive critic verdict must state gap_is_actionable as a boolean")
        elif actionable and not nonempty(gap):
            errors.append("an actionable gap must be stated")
    elif not nonempty(gap):
        errors.append("one largest actionable gap required")
    if verdict.get("confidence") not in ("low", "medium", "high"):
        errors.append("invalid confidence")
    if isinstance(context, dict) and context.get("domain") == "prose" and actionable is True and verdict.get("gap_dimension") not in ("density", "argument-order", "deletability", "evidence", "reader-task"):
        errors.append("prose gap must improve function, not imitate reference voice")
    return errors


_OPERATORS = {">=": operator.ge, ">": operator.gt, "<=": operator.le,
              "<": operator.lt, "==": operator.eq, "!=": operator.ne}


def _finite_number(value):
    return type(value) in (int, float) and (type(value) is int or math.isfinite(value))


def validate_judging_policy(policy, criteria_ids):
    """Explicit nonblind declaration; every frozen criterion has a numeric gate."""
    if not isinstance(policy, dict):
        return ["nonblind judging policy must be a frozen object"]
    errors = []
    if policy.get("mode") != "rubric" or policy.get("blind_feasible") is not False or not nonempty(policy.get("reason")):
        errors.append("nonblind mode needs rubric, blind_feasible:false and a concrete reason")
    thresholds = policy.get("thresholds")
    if not string_list(criteria_ids, 1) or not isinstance(thresholds, dict) or set(thresholds) != set(criteria_ids):
        errors.append("numeric thresholds must cover exactly every frozen criterion")
    elif any(not isinstance(row, dict) or not isinstance(row.get("operator"), str)
             or row["operator"] not in _OPERATORS or not _finite_number(row.get("value"))
             for row in thresholds.values()):
        errors.append("thresholds require supported numeric operator and finite value")
    return errors


def validate_rubric_critic(verdict, context):
    """Validate actual evidence-bound observations; never invent an A/B comparison."""
    errors = _binding_errors(verdict, context)
    if not isinstance(context, dict):
        return errors
    errors += validate_judging_policy(context.get("judging_policy"), context.get("criteria_ids"))
    if not isinstance(verdict, dict):
        return errors
    if "winner_is_ours" in verdict or "winner" in verdict:
        errors.append("rubric critic reports observations, not a winner or candidate identity")
    if verdict.get("result") not in RESULTS:
        errors.append("rubric result must be pass, fail or cannot-verify")
    gap, actionable = verdict.get("largest_gap"), verdict.get("gap_is_actionable")
    if verdict.get("result") == "fail" and not (actionable is True and nonempty(gap)):
        errors.append("failing rubric verdict needs a concrete actionable gap")
    elif verdict.get("result") == "pass" and type(actionable) is not bool:
        errors.append("rubric pass must state gap_is_actionable as a boolean")
    elif verdict.get("result") == "pass" and actionable and not nonempty(gap):
        errors.append("an actionable gap must be stated")
    elif verdict.get("result") == "cannot-verify" and not nonempty(gap):
        errors.append("state what could not be verified")
    if verdict.get("confidence") not in ("low", "medium", "high"):
        errors.append("invalid confidence")
    observed = verdict.get("criterion_observations")
    criteria = context.get("criteria_ids")
    if not isinstance(observed, dict) or not string_list(criteria, 1) or set(observed) != set(criteria):
        errors.append("observations must cover exactly every frozen criterion")
    else:
        evidence = verdict.get("evidence_inspected")
        inspected = {row["id"] for row in evidence if isinstance(row, dict) and nonempty(row.get("id"))} if isinstance(evidence, list) else set()
        for criterion, row in observed.items():
            if not isinstance(row, dict) or not nonempty(row.get("observation")) or not string_list(row.get("evidence_ids"), 1):
                errors.append("criterion observation needs value, observation and evidence_ids: " + criterion)
                continue
            if not set(row["evidence_ids"]).issubset(inspected):
                errors.append("criterion references evidence not actually inspected: " + criterion)
            if not _finite_number(row.get("value")) and not (row.get("value") is None and verdict.get("result") == "cannot-verify"):
                errors.append("criterion value must be finite or explicitly uninspectable: " + criterion)
    return errors


def evaluate_rubric_critic(verdict, context):
    """Compute gate result from frozen thresholds, preserving inability to inspect.

    Numeric subjective rubric scores remain reviewer judgments. This checks the
    arithmetic and evidence bindings; it cannot certify the truth of a score.
    No extra helper, arbitrary default score or fabricated reference is needed.
    """
    errors = validate_rubric_critic(verdict, context)
    if errors:
        raise ReviewError("; ".join(errors))
    comparisons = {}
    for criterion, gate in context["judging_policy"]["thresholds"].items():
        value = verdict["criterion_observations"][criterion]["value"]
        comparisons[criterion] = None if value is None else _OPERATORS[gate["operator"]](value, gate["value"])
    if verdict["result"] == "cannot-verify" or any(value is None for value in comparisons.values()):
        result, winner = "cannot-verify", "unable_to_evaluate"
    else:
        result = "pass" if all(comparisons.values()) else "fail"
        if verdict["result"] != result:
            raise ReviewError("reported rubric result contradicts frozen numeric thresholds")
        winner = "artifact_wins" if result == "pass" else "bar_wins"
    return {**verdict, "result": result, "winner": winner,
            "winner_is_ours": result == "pass", "blind": False,
            "criterion_comparisons": comparisons,
            "judging_policy_hash": hash_bytes(canonical_bytes(context["judging_policy"]))}


def unseal_critic(verdict, context, packet, sealed_map):
    errors = validate_critic(verdict, context)
    if not isinstance(sealed_map, dict) or not isinstance(packet, dict):
        raise ReviewError("packet and sealed map must be objects")
    packet_digest = hash_bytes(canonical_bytes(packet))
    map_digest = hash_bytes(canonical_bytes(sealed_map))
    if sealed_map.get("packet_hash") != packet_digest:
        errors.append("sealed packet hash mismatch")
    if not isinstance(context, dict):
        raise ReviewError("; ".join(errors))
    if context.get("packet_hash") != packet_digest or context.get("sealed_map_hash") != map_digest:
        errors.append("packet/map not bound to immutable pre-dispatch coordinator record")
    if sealed_map.get("contract_hash") != context.get("contract_hash"):
        errors.append("sealed contract mismatch")
    sources = sealed_map.get("source_hashes")
    if not isinstance(sources, dict) or sources.get("ours") != context.get("artifact_hash"):
        errors.append("sealed candidate mismatch")
    if sealed_map.get("ours_label") not in ("A", "B"):
        errors.append("invalid sealed label")
    if errors:
        raise ReviewError("; ".join(errors))
    ours = verdict["winner"] == sealed_map["ours_label"]
    if verdict["winner"] in ("A", "B") and not ours and not (verdict.get("gap_is_actionable") is True and nonempty(verdict.get("largest_gap"))):
        raise ReviewError("a verdict against the candidate needs a concrete actionable gap")
    return {**verdict, "winner_is_ours": ours}


def _criterion_results(verdict, context):
    """Return explicit criterion outcomes, errors and legacy-all-pass flag.

    Omitted outcomes are compatible only with an entirely passing legacy vote.
    A dissenting vote must identify what failed; it cannot quietly override a
    required criterion through majority arithmetic. Materiality comes from the
    frozen coordinator context, never from a judge's own classification.
    """
    if not isinstance(verdict, dict) or not isinstance(context, dict) or not string_list(context.get("criteria_ids"), 1):
        return {}, ["criterion outcomes need valid verdict and frozen criteria"], False
    criteria = context["criteria_ids"]
    if "criterion_results" not in verdict:
        if verdict.get("result") == "pass":
            return {criterion: "pass" for criterion in criteria}, [], True
        return {}, ["non-pass vote requires explicit criterion_results for every criterion"], False
    outcomes = verdict["criterion_results"]
    if not isinstance(outcomes, dict) or set(outcomes) != set(criteria) or any(value not in RESULTS for value in outcomes.values()):
        return {}, ["criterion_results must map every frozen criterion to pass, fail or cannot-verify"], False
    result = verdict.get("result")
    values = list(outcomes.values())
    errors = []
    if result == "pass" and any(value != "pass" for value in values):
        errors.append("overall pass contradicts non-passing criterion outcome")
    elif result in ("fail", "cannot-verify") and result not in values:
        errors.append("non-pass overall result needs a matching criterion outcome")
    return outcomes, errors, False


def compute_consensus(verdicts, context, policy=None):
    """Source table after strict panel validity/eligibility checks.

    Invalid votes yield unverifiable with errors, never a partial-panel majority.
    Quality strict majority only for explicitly nonmaterial dissent. Any required
    criterion failure vetoes, as does integrity failure; cannot-verify blocks.
    Three perspectives may be distributed among the same four/six judges.
    Failed/unverifiable outcomes remain exportable evidence, not completion.
    """
    policy = default_policy() if policy is None else policy
    errors = validate_policy(policy) + validate_context(context, panel=True)
    if not isinstance(verdicts, list):
        verdicts = []
        errors.append("verdicts must be a list")
    counts = {r: {v: 0 for v in RESULTS} for r in ROLES}
    authors, sessions, perspectives, dissent = set(), set(), set(), []
    required_failures, criterion_inabilities, legacy_all_pass_votes = [], [], 0
    required = context.get("required_criteria_ids", context.get("criteria_ids", [])) if isinstance(context, dict) else []
    required = set(required) if string_list(required) else set()
    for index, verdict in enumerate(verdicts):
        local = _binding_errors(verdict, context)
        if not isinstance(verdict, dict):
            errors.extend("vote %d: %s" % (index, e) for e in local)
            continue
        outcomes, criterion_errors, legacy = _criterion_results(verdict, context)
        local += criterion_errors
        legacy_all_pass_votes += int(legacy)
        for criterion, outcome in outcomes.items():
            finding = {"criterion_id": criterion, "author_id": verdict.get("author_id"),
                       "verifier_type": verdict.get("verifier_type"), "reason": verdict.get("reason")}
            if outcome == "fail" and criterion in required:
                required_failures.append(finding)
            if outcome == "cannot-verify":
                criterion_inabilities.append(finding)
        author, session = verdict.get("author_id"), verdict.get("session_id")
        for name, value, seen in (("author", author, authors), ("session", session, sessions)):
            if nonempty(value):
                if value in seen:
                    local.append("duplicate " + name)
                seen.add(value)
        role, result = verdict.get("verifier_type"), verdict.get("result")
        if role not in ROLES:
            local.append("unknown verifier_type")
        if result not in RESULTS:
            local.append("unknown result")
        if role in ROLES and result in RESULTS:
            counts[role][result] += 1
        if string_list(verdict.get("perspectives"), 1):
            perspectives.update(verdict["perspectives"])
        if result != "pass":
            dissent.append({"author_id": author, "verifier_type": role, "result": result, "reason": verdict.get("reason")})
        errors.extend("vote %d: %s" % (index, e) for e in local)
    if isinstance(policy, dict):
        for role in ROLES:
            if sum(counts[role].values()) != policy.get(role + "_count"):
                errors.append("panel must contain exactly frozen " + role + "_count")
    if isinstance(context, dict) and string_list(context.get("required_perspectives"), 3):
        if not set(context["required_perspectives"]).issubset(perspectives):
            errors.append("panel does not cover all frozen perspectives")
        expected = context.get("expected_sessions")
        if isinstance(expected, dict) and sessions != set(expected):
            errors.append("panel must include exactly all dispatched review sessions")
    if errors:
        outcome = "unverifiable"
    elif counts["integrity"]["fail"] or required_failures:
        outcome = "failed"
    elif criterion_inabilities or any(c["cannot-verify"] for c in counts.values()):
        outcome = "unverifiable"
    elif not counts["quality"]["fail"]:
        outcome = "verified"
    elif counts["quality"]["pass"] > counts["quality"]["fail"]:
        outcome = "verified-with-dissent"
    else:
        outcome = "failed"
    return {"consensus": outcome, "quality_votes": counts["quality"],
            "integrity_votes": counts["integrity"], "dissent": dissent,
            "required_criteria_failures": required_failures,
            "criterion_inabilities": criterion_inabilities,
            "legacy_all_pass_votes": legacy_all_pass_votes,
            "validation_errors": errors, "computed_by": "review.py", "policy": policy,
            "input_hash": hash_bytes(canonical_bytes({"verdicts": verdicts, "context": context, "policy": policy}))}


def _load(path):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ReviewError("duplicate JSON key: " + key)
            out[key] = value
        return out
    def reject_constant(value):
        raise ReviewError("nonfinite JSON number: " + value)
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique, parse_constant=reject_constant)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("consensus", "validate-critic", "unseal", "rubric"):
        command = sub.add_parser(name)
        command.add_argument("--input", required=True, help="JSON containing verdicts/verdict, context, policy; unseal also packet/sealed_map")
    h = sub.add_parser("hash")
    h.add_argument("--contract", required=True)
    c = sub.add_parser("check-hash")
    c.add_argument("--contract", required=True)
    c.add_argument("--expected", required=True)
    cf = sub.add_parser("check-frozen")
    cf.add_argument("--frozen", required=True)
    cf.add_argument("--root", required=True)
    cf.add_argument("--expected", required=True)
    f = sub.add_parser("freeze-contract")
    f.add_argument("--contract", required=True)
    f.add_argument("--root", required=True)
    f.add_argument("--files", required=True, help="JSON list of explicitly declared dependencies")
    b = sub.add_parser("blind")
    for name in ("ours", "reference", "contract", "packet", "sealed-map"):
        b.add_argument("--" + name, required=True)
    b.add_argument("--seed", type=int, required=True)
    args = parser.parse_args(argv)
    try:
        code = 0
        if args.command in ("consensus", "validate-critic", "unseal", "rubric"):
            data = _load(args.input)
            if not isinstance(data, dict):
                raise ReviewError("input must be an object")
            if args.command == "consensus":
                result = compute_consensus(data.get("verdicts"), data.get("context"), data.get("policy"))
                code = 0 if result["consensus"] in ("verified", "verified-with-dissent") else 1
            elif args.command == "validate-critic":
                errors = validate_critic(data.get("verdict"), data.get("context"))
                result, code = {"valid": not errors, "errors": errors}, int(bool(errors))
            elif args.command == "rubric":
                result = evaluate_rubric_critic(data.get("verdict"), data.get("context"))
                code = 0 if result["result"] == "pass" else 1
            else:
                result = unseal_critic(data.get("verdict"), data.get("context"), data.get("packet"), data.get("sealed_map"))
        elif args.command == "blind":
            prepared = prepare_blind_pair(Path(args.ours).read_bytes(), Path(args.reference).read_bytes(), _load(args.contract), args.seed)
            result = write_blind_pair(prepared, args.packet, args.sealed_map)
        elif args.command == "check-frozen":
            result = check_frozen_contract(_load(args.frozen), args.root, args.expected)
            code = int(not result["matched"])
        elif args.command == "freeze-contract":
            result = freeze_contract(_load(args.contract), args.root, _load(args.files))
        else:
            digest = contract_hash(_load(args.contract))
            result = {"contract_hash": digest}
            if args.command == "check-hash":
                result["matched"] = digest == args.expected
                code = int(not result["matched"])
        print(json.dumps(result, sort_keys=True, indent=2, allow_nan=False))
        return code
    except (ReviewError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
