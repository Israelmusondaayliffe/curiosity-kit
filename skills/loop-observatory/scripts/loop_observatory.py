#!/usr/bin/env python3
"""Read explicitly selected loop evidence; write derived JSON/Markdown outside sources.

Standard-library CLI; no execution, producer state mutation, model calls, scheduler,
network, or implicit account-home discovery. Derived records are not owner journals.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import statistics
import sys
import uuid

sys.dont_write_bytecode = True   # never write caches into the installed skill, whatever the interpreter flags
sys.path.insert(0, str(Path(__file__).resolve().parent))   # sibling module also under python -I
from observatory_io import (PARSER_VERSION, SCHEMA_VERSION, PROFILES, DEFAULT_LIMITS,
    EvidenceError, need, utc_now, canonical, digest, safe_id, safe_path, within,
    validate_output, atomic_json, atomic_bytes, load_json, number_value, bool_value,
    timestamp, nonempty, object_value, roots_config, capture, normalize, inventory)

METRIC_VERSION = "portfolio-calibration-2.0"
BINDING = ("task", "artifact", "criterion", "rubric")
EXHAUSTION_REASONS = {"iteration_limit", "iteration-limit", "max_iterations", "no_progress_limit",
                      "time_limit", "timeout", "token_limit", "cost_limit", "budget_exhausted", "budget-exhausted"}


def exclusion(identifier, reason, detail=None, **extra):
    out = {"id": str(identifier), "reason": reason, **extra}
    if detail:
        out["detail"] = str(detail)
    return out


def ratio(numerator, denominator):
    return {"numerator": numerator, "denominator": denominator,
            "value": numerator / denominator if denominator else None}


def logical_key(record):
    return canonical([record["producer"], record["namespace"], record["run_id"]]).decode()


def record_identity(record):
    # Source copy paths/pointers do not turn the same observation into a new trial.
    omit = {"record_id", "source_ids", "source_hashes", "field_pointers", "warnings", "coherence", "raw", "ingested_at"}
    body = {k: v for k, v in record.items() if k not in omit}
    return safe_id(record["producer"] + "-" + record["run_id"]) + "-" + digest(body)[:24]


def validate_record(record):
    r = deepcopy(record)
    for key in ("producer", "namespace", "run_id", "status", "profile"):
        nonempty(r.get(key), key)
    need(type(r.get("terminal")) is bool, "invalid-terminal", "Terminal must be explicitly boolean")
    if r.get("revision") is not None:
        number_value(r["revision"], integer=True)
    for key in ("event_time", "known_time"):
        r[key] = timestamp(r.get(key))
    r.setdefault("process_completion", None)
    bool_value(r["process_completion"])
    r.setdefault("machine_completion", None)
    bool_value(r["machine_completion"])
    for key in ("iteration", "duration_seconds", "tokens", "cost"):
        if r.get(key) is not None:
            number_value(r[key], integer=key in {"iteration", "tokens"})
    for key in ("goal", "model", "version", "cohort", "task", "artifact", "criterion", "rubric",
                "stop_reason", "escalation_reason", "judge_verdict", "human_label"):
        r.setdefault(key, None)
    for key in ("stop_reason", "escalation_reason", "cohort"):
        need(r.get(key) is None or isinstance(r[key], str), "invalid-field-type", key + " must be a string or null")
    for key in ("judgments", "measurements", "supersedes", "measurement_coverage"):
        r.setdefault(key, [])
        need(isinstance(r[key], list), "invalid-list", key + " must be a list")
    need(all(isinstance(x, str) for x in r["supersedes"]), "invalid-supersedes", "supersedes requires exact record IDs")
    # An explicitly named scalar seconds field has units. Generic cost/tokens are retained
    # only as raw data unless a complete measurement observation is supplied.
    if r.get("duration_seconds") is not None and not any(isinstance(m, dict) and m.get("metric") == "duration" for m in r["measurements"]):
        r["measurements"].append({"id": "duration-seconds", "metric": "duration", "value": r["duration_seconds"],
              "unit": "seconds", "basis": "measured", "scope": "run", "aggregation": "cumulative",
              "revision": r.get("revision") or 0, "provenance": "explicit duration_seconds field"})
    r["record_id"] = record_identity(r)
    return r


def read_previous(path):
    if path is None:
        return None
    path = safe_path(path)
    files, _ = capture(path, DEFAULT_LIMITS)
    previous = object_value(load_json(files[path.name]), "previous result")
    need(previous.get("schema_version") == SCHEMA_VERSION and previous.get("parser_version") == PARSER_VERSION,
         "incompatible-previous", "Previous output requires matching schema/parser; regenerate with current parser")
    need(isinstance(previous.get("records"), list), "invalid-previous", "Previous result records missing")
    for r in previous["records"]:
        need(isinstance(r, dict) and r.get("record_id") == record_identity(r), "invalid-previous", "Previous record identity mismatch")
    return previous


def ingest(manifest):
    all_records, source_manifest, exclusions = [], [], []
    counts = Counter(discovered=len(manifest["sources"]), sources_read=0, sources_failed=0,
                     records_read=0, records_rejected=0, duplicate_records=0)
    total_bytes = 0
    for source in manifest["sources"]:
        entry = dict(source)
        try:
            files, captured = capture(Path(source["path"]), manifest["limits"])
            total_bytes += captured["bytes"]
            need(total_bytes <= manifest["limits"]["max_total_bytes"], "total-byte-limit", "Manifest total bytes exceeded")
            entry.update(captured)
            raw_records, errors, coherence = normalize(source, files, manifest["limits"])
            entry.update(status="ok", coherence_basis=coherence)
            exclusions.extend(errors)
            counts["records_rejected"] += len(errors)
            for index, raw in enumerate(raw_records):
                try:
                    raw["coherence"] = coherence
                    raw["source_hashes"] = [captured["sha256"]]
                    record = validate_record(raw)
                    need(len(all_records) < manifest["limits"]["max_records"], "record-count-limit", "Manifest-wide record count exceeded")
                    all_records.append(record)
                    counts["records_read"] += 1
                except (EvidenceError, ValueError, TypeError, KeyError) as exc:
                    counts["records_rejected"] += 1
                    exclusions.append(exclusion(source["id"] + "#/record/" + str(index), getattr(exc, "code", "invalid-record"), str(exc)))
            counts["sources_read"] += 1
            if errors or any(x["id"].startswith(source["id"] + "#/record/") for x in exclusions):
                entry["status"] = "partial"
        except (OSError, EvidenceError, ValueError, TypeError, KeyError, RecursionError) as exc:
            counts["sources_failed"] += 1
            entry.update(status="error", error=getattr(exc, "code", "unreadable-source"), detail=str(exc))
            exclusions.append(exclusion(source["id"], entry["error"], str(exc)))
        source_manifest.append(entry)
    return all_records, source_manifest, exclusions, dict(counts)


def visible_time(value, cutoff, identifier, dimension, exclusions):
    if cutoff is None:
        return True
    if value is None:
        exclusions.append(exclusion(identifier, "missing-" + dimension, "Cannot place evidence relative to requested cutoff"))
        return False
    if timestamp(value) > cutoff:
        exclusions.append(exclusion(identifier, "after-" + dimension + "-cutoff"))
        return False
    return True


def record_index(fresh, previous, context, exclusions):
    """Preserve histories; select only currently supplied logical runs and ordered revisions."""
    merged, duplicate_count = {}, 0
    for record in (previous.get("records", []) if previous else []) + fresh:
        key = record["record_id"]
        if key in merged:
            duplicate_count += 1
            merged[key]["source_ids"] = sorted(set(merged[key]["source_ids"] + record["source_ids"]))
            merged[key]["source_hashes"] = sorted(set(merged[key].get("source_hashes", []) + record.get("source_hashes", [])))
        else:
            merged[key] = deepcopy(record)
    fresh_keys = {logical_key(r) for r in fresh}
    fresh_ids = {r["record_id"] for r in fresh}
    grouped = defaultdict(list)
    for record in merged.values():
        key = logical_key(record)
        if key not in fresh_keys:
            exclusions.append(exclusion(record["record_id"], "not-in-current-selection", "Retained history is not promoted when its current input is absent or unreadable"))
            continue
        if not visible_time(record.get("event_time"), context["as_of"], record["record_id"], "event-time", exclusions):
            continue
        if not visible_time(record.get("known_time"), context["known_as_of"], record["record_id"], "knowledge-time", exclusions):
            continue
        grouped[key].append(record)
    current, conflicts, history = [], [], []
    for key, group in sorted(grouped.items()):
        revisions = [r.get("revision") for r in group]
        # Explicit bound supersession can retire an unordered correction, but never a
        # foreign run. It cannot legalize a terminal reopen forbidden by the producer.
        ids = {r["record_id"] for r in group}
        superseded = set()
        for r in group:
            for old in r.get("supersedes", []):
                if old not in ids or old == r["record_id"]:
                    exclusions.append(exclusion(r["record_id"], "invalid-supersession", "Superseded revision must be a different supplied revision of this logical run"))
                else:
                    superseded.add(old)
        candidates = [r for r in group if r["record_id"] not in superseded]
        if len(candidates) > 1:
            if all(r.get("revision") is not None for r in candidates):
                maximum = max(r["revision"] for r in candidates)
                candidates = [r for r in candidates if r["revision"] == maximum]
        invalid_reopen = False
        if len(candidates) == 1 and candidates[0]["profile"] in {"loopkit-snapshot-v2", "loopkit-legacy"}:
            chosen = candidates[0]
            invalid_reopen = any(r["terminal"] and r["status"] != chosen["status"] and r.get("revision") is not None
                                 and chosen.get("revision") is not None and r["revision"] < chosen["revision"] for r in group)
        if len(candidates) != 1 or invalid_reopen:
            reason = "unsupported-terminal-reopen" if invalid_reopen else "conflicting-run-revisions"
            conflict = {"logical_run": key, "record_ids": sorted(ids), "reason": reason}
            conflicts.append(conflict)
            exclusions.extend(exclusion(r["record_id"], reason) for r in group)
            history.extend(group)
            continue
        chosen = candidates[0]
        if not context["as_of"] and not context["known_as_of"] and chosen["record_id"] not in fresh_ids:
            reason = "current-revision-not-reobserved"
            conflicts.append({"logical_run": key, "record_ids": sorted(ids), "reason": reason})
            exclusions.append(exclusion(chosen["record_id"], reason, "The latest retained revision is absent from this capture; an older source cannot silently restore a stale success"))
            history.extend(group)
            continue
        history.extend(r for r in group if r["record_id"] != chosen["record_id"])
        if context["cohort"] is not None and chosen.get("cohort") != context["cohort"]:
            exclusions.append(exclusion(chosen["record_id"], "outside-cohort"))
        else:
            current.append(chosen)
    return sorted(merged.values(), key=lambda r: r["record_id"]), current, history, conflicts, duplicate_count


def records(current, exclusions):
    eligible = []
    for r in current:
        if r["terminal"]:
            eligible.append(r)
        else:
            exclusions.append(exclusion(r["record_id"], "nonterminal-current", "Current authoritative revision retires older terminal evidence"))
    return eligible


def judgment_view(record, context, exclusions):
    grouped = defaultdict(lambda: {"machine": [], "human": []})
    seen, poisoned_ids, raw_ids = {}, set(), {}
    for item in record["judgments"]:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            if item["id"] in raw_ids and raw_ids[item["id"]] != item:
                poisoned_ids.add(item["id"])
            raw_ids[item["id"]] = item
    for bad_id in sorted(poisoned_ids):
        exclusions.append(exclusion(record["record_id"] + "#judgment:" + bad_id, "conflicting-judgment-id", "All contradictory copies of this observation identity are quarantined"))
    for index, raw in enumerate(record["judgments"]):
        identifier = record["record_id"] + "#/judgments/" + str(index)
        try:
            j = deepcopy(object_value(raw, "judgment"))
            nonempty(j.get("id"), "judgment.id")
            identifier = record["record_id"] + "#judgment:" + j["id"]
            need(j.get("kind") in {"machine", "human"}, "invalid-judgment-kind", "kind must be machine or human")
            bool_value(j.get("label"))
            for field in BINDING:
                nonempty(j.get(field), "judgment." + field)
            nonempty(j.get("reviewer"), "judgment.reviewer")
            need(j.get("purpose") == "output-acceptance", "nonacceptance-approval", "Launch, upload and other approvals do not label output acceptance")
            j["event_time"], j["known_time"] = timestamp(j.get("event_time")), timestamp(j.get("known_time"))
            if not visible_time(j["event_time"], context["as_of"], identifier, "event-time", exclusions):
                continue
            if not visible_time(j["known_time"], context["known_as_of"], identifier, "knowledge-time", exclusions):
                continue
            need(j["task"] == record.get("task") and j["artifact"] == record.get("artifact"),
                 "stale-judgment-target", "Judgment concerns a different task or artifact")
            if j["id"] in seen:
                if seen[j["id"]] != j:
                    poisoned_ids.add(j["id"])
                    raise EvidenceError("conflicting-judgment-id", "Same judgment ID has conflicting evidence; all copies are quarantined")
                continue
            seen[j["id"]] = j
            grouped[tuple(j[x] for x in BINDING)][j["kind"]].append(j)
        except (EvidenceError, TypeError) as exc:
            exclusions.append(exclusion(identifier, getattr(exc, "code", "invalid-judgment"), str(exc)))
    pairs, assessments, primary_human, primary_machine = [], [], None, None
    primary = tuple(record.get(x) for x in BINDING)
    for binding, kinds in sorted(grouped.items()):
        for kind in kinds:
            kinds[kind] = [j for j in kinds[kind] if j["id"] not in poisoned_ids]
        selected = {}
        issues = []
        for kind, observations in kinds.items():
            reviewer = context.get("reference_reviewer") if kind == "human" else context.get("machine_reviewer")
            if reviewer:
                observations = [o for o in observations if o["reviewer"] == reviewer]
            superseded = set()
            available = {o["id"] for o in observations}
            for o in observations:
                replacements = o.get("supersedes", [])
                if not isinstance(replacements, list) or not all(x in available and x != o["id"] for x in replacements):
                    issues.append("invalid-" + kind + "-supersession")
                    continue
                superseded.update(replacements)
            observations = [o for o in observations if o["id"] not in superseded]
            if len(observations) == 1:
                selected[kind] = observations[0]
                if observations[0]["label"] is None:
                    issues.append("unknown-" + kind + "-label")
            elif not observations:
                issues.append("missing-" + kind + "-label")
            else:
                issues.append("conflicting-" + kind + "-labels" if len({o["label"] for o in observations}) > 1 else "multiple-" + kind + "-observations")
        assessment = {"record_id": record["record_id"], "run_id": record["run_id"],
                      "binding": dict(zip(BINDING, binding)), "selected": selected, "issues": issues}
        assessments.append(assessment)
        if binding == primary:
            primary_human = selected.get("human", {}).get("label") if not any("human" in x for x in issues) else None
            primary_machine = selected.get("machine", {}).get("label") if not any("machine" in x for x in issues) else None
        if not issues and set(selected) == {"machine", "human"}:
            pair = {"pair_id": record["record_id"] + ":" + digest(list(binding))[:12],
                    "record_id": record["record_id"], "run_id": record["run_id"], "binding": dict(zip(BINDING, binding)),
                    "machine_id": selected["machine"]["id"], "human_id": selected["human"]["id"],
                    "machine": selected["machine"]["label"], "human": selected["human"]["label"],
                    "source_ids": record["source_ids"]}
            pairs.append(pair)
        else:
            for issue in issues:
                exclusions.append(exclusion(record["record_id"] + ":" + digest(list(binding))[:12], issue))
    if not grouped:
        exclusions.append(exclusion(record["record_id"], "no-bound-judgments"))
    return primary_human, primary_machine, pairs, assessments


def measurement_totals(record, history, context, exclusions):
    """Distinct charged operations accumulate; revised cumulative scopes replace.

No cost is inferred from models/tokens. Parent totals may cover children only with
explicit bound observation IDs; ambiguous overlap makes the series unknown.
"""
    observations, invalid = {}, set()
    relevant = [r for r in history if logical_key(r) == logical_key(record)]
    for r in relevant:
        if r.get("revision") is not None and record.get("revision") is not None and r["revision"] > record["revision"]:
            continue
        if context["as_of"] and (r.get("event_time") is None or r["event_time"] > context["as_of"]):
            continue
        if context["known_as_of"] and (r.get("known_time") is None or r["known_time"] > context["known_as_of"]):
            continue
        for index, raw in enumerate(r.get("measurements", [])):
            identifier = r["record_id"] + "#/measurements/" + str(index)
            series = None
            try:
                m = deepcopy(object_value(raw, "measurement"))
                nonempty(m.get("id"), "measurement.id")
                identifier = r["record_id"] + "#measurement:" + m["id"]
                need(m.get("metric") in {"cost", "tokens", "duration"}, "invalid-metric", "Unknown metric")
                nonempty(m.get("unit"), "measurement.unit")
                need(m.get("basis") in {"measured", "estimated", "reserved"}, "invalid-measurement-basis", "Missing measurement basis")
                series = (m["metric"], m["unit"], m["basis"])
                number_value(m.get("value"), integer=m["metric"] == "tokens")
                if m["metric"] == "cost":
                    need(len(m["unit"]) == 3 and m["unit"].isascii() and m["unit"].isupper() and m["unit"].isalpha(), "invalid-currency", "Cost needs explicit three-letter currency")
                else:
                    need(m["unit"] == {"tokens": "tokens", "duration": "seconds"}[m["metric"]], "invalid-unit", "Wrong measurement unit")
                nonempty(m.get("scope"), "measurement.scope")
                need(m.get("aggregation") in {"incremental", "cumulative"}, "invalid-aggregation", "Missing incremental/cumulative scope")
                number_value(m.get("revision", r.get("revision", 0)), integer=True)
                m["revision"] = m.get("revision", r.get("revision", 0))
                if m["aggregation"] == "incremental":
                    nonempty(m.get("attempt_id"), "measurement.attempt_id")
                    nonempty(m.get("operation_id"), "measurement.operation_id")
                for key in ("event_time", "known_time"):
                    m[key] = timestamp(m.get(key, r.get(key)))
                if not visible_time(m["event_time"], context["as_of"], identifier, "event-time", exclusions):
                    continue
                if not visible_time(m["known_time"], context["known_as_of"], identifier, "knowledge-time", exclusions):
                    continue
                m.setdefault("covers", [])
                need(isinstance(m["covers"], list) and all(isinstance(x, str) for x in m["covers"]), "invalid-measurement-coverage", "covers must list measurement IDs")
                key = (m["id"], m["revision"])
                if key in observations:
                    # Event/known timestamps can be repeated snapshot observation times;
                    # an identical value is still the same charge, not another operation.
                    compare = lambda x: {k: v for k, v in x.items() if k not in {"event_time", "known_time", "provenance"}}
                    need(compare(observations[key]) == compare(m), "conflicting-measurement-id", "Measurement identity has conflicting values")
                else:
                    observations[key] = m
            except (EvidenceError, TypeError) as exc:
                if series:
                    invalid.add(series)
                exclusions.append(exclusion(identifier, getattr(exc, "code", "invalid-measurement"), str(exc)))
    # A revised measurement ID supersedes its own previous observation exactly once.
    by_id = defaultdict(list)
    for m in observations.values():
        by_id[m["id"]].append(m)
    measurements = [max(rows, key=lambda m: m["revision"]) for rows in by_id.values()]
    series_rows = defaultdict(list)
    for m in measurements:
        series_rows[(m["metric"], m["unit"], m["basis"])].append(m)
    result = []
    for series, rows in sorted(series_rows.items()):
        bad, reason = series in invalid, None
        all_ids = {m["id"] for m in rows}
        covered, selected = set(), []
        for m in rows:
            if m["covers"]:
                if m["aggregation"] != "cumulative" or not set(m["covers"]) <= all_ids or m["id"] in m["covers"]:
                    bad, reason = True, "invalid-measurement-coverage"
                covered.update(m["covers"])
        cover_graph = {m["id"]: m["covers"] for m in rows}
        # Topological removal detects every cycle, including one beside valid rows.
        remaining = set(cover_graph)
        while remaining:
            leaves = {key for key in remaining if not (set(cover_graph[key]) & remaining)}
            if not leaves:
                bad, reason = True, "cyclic-measurement-coverage"
                break
            remaining -= leaves
        rows = [m for m in rows if m["id"] not in covered]
        scopes = defaultdict(list)
        for m in rows:
            scopes[m["scope"]].append(m)
        for scope, values in scopes.items():
            cumulative = [m for m in values if m["aggregation"] == "cumulative"]
            incremental = [m for m in values if m["aggregation"] == "incremental"]
            if cumulative:
                maximum = max(m["revision"] for m in cumulative)
                latest = [m for m in cumulative if m["revision"] == maximum]
                if len(latest) != 1 or incremental:
                    bad, reason = True, "ambiguous-cumulative-overlap"
                else:
                    selected.extend(latest)
            else:
                operations = {}
                for m in incremental:
                    key = (m["attempt_id"], m["operation_id"])
                    if key in operations and operations[key]["value"] != m["value"]:
                        bad, reason = True, "conflicting-charge-operation"
                    operations[key] = m
                selected.extend(operations.values())
        # Run/total totals must not silently be added to child/attempt counters.
        if len(selected) > 1 and any(m["aggregation"] == "cumulative" and m["scope"] in {"run", "total"} for m in selected):
            bad, reason = True, "ambiguous-parent-child-overlap"
        if not rows and measurements:
            bad, reason = True, "cyclic-measurement-coverage"
        if bad:
            exclusions.append(exclusion(record["record_id"], reason or "invalid-measurement-series", "/".join(series)))
        total = None if bad else float(sum((Decimal(str(m["value"])) for m in selected), Decimal(0)))
        scope_complete = len(selected) == 1 and selected[0]["aggregation"] == "cumulative" and selected[0]["scope"] == "run"
        coverage_basis = "cumulative-run-total" if scope_complete else "partial-observation-set"
        for assertion in record.get("measurement_coverage", []):
            try:
                object_value(assertion, "measurement coverage")
                if tuple(assertion.get(k) for k in ("metric", "unit", "basis")) != series:
                    continue
                need(assertion.get("complete") is True and isinstance(assertion.get("observation_ids"), list),
                     "invalid-coverage-assertion", "Coverage requires complete:true and exact observation_ids")
                need(set(assertion["observation_ids"]) == {m["id"] for m in selected} | covered,
                     "incomplete-coverage-binding", "Coverage IDs must exactly bind the effective and covered measurement observations")
                scope_complete, coverage_basis = True, "owner-asserted-complete-observation-set"
            except (EvidenceError, TypeError) as exc:
                exclusions.append(exclusion(record["record_id"], getattr(exc, "code", "invalid-coverage-assertion"), str(exc)))
        result.append({"metric": series[0], "unit": series[1], "basis": series[2], "value": total,
                       "valid": not bad, "complete": not bad and scope_complete, "coverage_basis": coverage_basis,
                       "observation_ids": sorted(m["id"] for m in selected),
                       "covered_observation_ids": sorted(covered)})
    return result


def is_exhausted(record):
    return record["status"] == "exhausted" or record.get("stop_reason") in EXHAUSTION_REASONS


def audit(eligible, context, exclusions):
    pairs, assessments, labels = [], [], {}
    for r in eligible:
        human, machine, run_pairs, run_assessments = judgment_view(r, context, exclusions)
        labels[r["record_id"]] = {"human": human, "machine": machine}
        pairs.extend(run_pairs)
        assessments.extend(run_assessments)
    cells = {"machine_positive_human_positive": [], "machine_positive_human_negative": [],
             "machine_negative_human_positive": [], "machine_negative_human_negative": []}
    for p in pairs:
        key = "machine_" + ("positive" if p["machine"] else "negative") + "_human_" + ("positive" if p["human"] else "negative")
        cells[key].append(p["pair_id"])
    disagreements = [p for p in pairs if p["machine"] != p["human"]]
    result = {"reference_policy": "one unique observation per exact target/rubric stratum; unresolved multiplicity excluded",
              "reference_reviewer": context.get("reference_reviewer"), "machine_reviewer": context.get("machine_reviewer"),
              "paired_denominator": len(pairs), "paired_run_coverage": ratio(len({p["record_id"] for p in pairs}), len(eligible)),
              "cells": cells, "cell_counts": {k: len(v) for k, v in cells.items()}, "pairs": pairs,
              "disagreements": disagreements, "disagreement_rate": ratio(len(disagreements), len(pairs)),
              "assessments": assessments, "unpaired_or_conflicted_strata": sum(bool(a["issues"]) for a in assessments),
              "interpretation": "Observed disagreements; neither human reference nor machine judgment is assumed infallible. Inspect the bound artifact and governing rubric before attributing a defect."}
    return result, labels


def cost_metrics(eligible, totals, labels):
    currencies = sorted({m["unit"] for items in totals.values() for m in items if m["metric"] == "cost"})
    accepted = [r for r in eligible if labels[r["record_id"]]["human"] is True]
    labeled = [r for r in eligible if labels[r["record_id"]]["human"] is not None]
    out = {}
    for currency in currencies:
        series = {}
        for basis in ("measured", "estimated", "reserved"):
            observed, complete_observed, missing = {}, {}, []
            for r in eligible:
                values = [m for m in totals[r["record_id"]] if m["metric"] == "cost" and m["basis"] == basis]
                selected = [m for m in values if m["unit"] == currency]
                # Preserve known currency spend even when it is partial or the run
                # also incurred another currency. Full-run ratios need more evidence.
                if len(selected) == 1 and selected[0]["value"] is not None:
                    observed[r["record_id"]] = selected[0]["value"]
                    if selected[0]["complete"] and len(values) == 1:
                        complete_observed[r["record_id"]] = selected[0]["value"]
                if r["record_id"] not in complete_observed:
                    missing.append(r["record_id"])
            # No valid observation is unknown spend, never zero; an observed measured zero stays 0.
            known = float(sum((Decimal(str(v)) for v in observed.values()), Decimal(0))) if observed else None
            accepted_values = [complete_observed[r["record_id"]] for r in accepted if r["record_id"] in complete_observed]
            complete = bool(eligible) and len(complete_observed) == len(eligible)
            accepted_complete = bool(accepted) and len(accepted_values) == len(accepted)
            series[basis] = {"known_spend": known, "run_coverage": ratio(len(complete_observed), len(eligible)),
                            "observed_run_coverage": ratio(len(observed), len(eligible)),
                            "missing_or_incompatible_run_ids": missing, "values_by_record": observed,
                            "accepted_run_cost_coverage": ratio(len(accepted_values), len(accepted)),
                            "mean_observed_cost_of_accepted_runs": float(sum(Decimal(str(v)) for v in accepted_values) / len(accepted_values)) if accepted_complete else None,
                            "spend_per_currently_evidenced_accepted_outcome": known / len(accepted) if complete and accepted else None,
                            "fully_adjudicated_cost_per_accepted_outcome": known / len(accepted) if complete and accepted and len(labeled) == len(eligible) else None,
                            "accepted_outcomes": len(accepted), "human_label_coverage": ratio(len(labeled), len(eligible))}
        out[currency] = {"currency": currency, "known_spend": series["measured"]["known_spend"],
                         "measured_run_coverage": series["measured"]["run_coverage"],
                         "mean_observed_cost_of_accepted_runs": series["measured"]["mean_observed_cost_of_accepted_runs"],
                         "spend_per_currently_evidenced_accepted_outcome": series["measured"]["spend_per_currently_evidenced_accepted_outcome"],
                         "fully_adjudicated_cost_per_accepted_outcome": series["measured"]["fully_adjudicated_cost_per_accepted_outcome"],
                         "series": series}
    return out


def scalar_summary(eligible, totals, metric):
    values = [m["value"] for r in eligible for m in totals[r["record_id"]]
              if m["metric"] == metric and m["basis"] == "measured" and m["value"] is not None]
    return {"unit": "seconds" if metric == "duration" else "tokens", "coverage": ratio(sum(any(m["metric"] == metric and m["basis"] == "measured" and m["complete"] for m in totals[r["record_id"]]) for r in eligible), len(eligible)),
            "observed_coverage": ratio(len(values), len(eligible)),
            "minimum": min(values) if values else None, "maximum": max(values) if values else None,
            "mean": statistics.mean(values) if values else None, "median": statistics.median(values) if values else None,
            "sum": float(sum(Decimal(str(v)) for v in values)) if values else None}


def metrics(eligible, totals, labels):
    labeled = sum(labels[r["record_id"]]["human"] is not None for r in eligible)
    accepted = sum(labels[r["record_id"]]["human"] is True for r in eligible)
    iterations = [r["iteration"] for r in eligible if r.get("iteration") is not None]
    def label_counts(values):
        return {"positive": sum(v is True for v in values), "negative": sum(v is False for v in values),
                "unknown": sum(v is None for v in values), "denominator": len(values)}
    return {"human_acceptance": ratio(accepted, labeled),
            "process_completion": label_counts([r.get("process_completion") for r in eligible]),
            "bound_machine_judgment": label_counts([labels[r["record_id"]]["machine"] for r in eligible]),
            "producer_machine_completion": label_counts([r.get("machine_completion") for r in eligible]),
            "iterations": {"coverage": ratio(len(iterations), len(eligible)), "minimum": min(iterations) if iterations else None,
                           "maximum": max(iterations) if iterations else None, "mean": statistics.mean(iterations) if iterations else None, "median": statistics.median(iterations) if iterations else None}, "label_coverage": ratio(labeled, len(eligible)),
            "human_acceptance_known": labeled, "accepted_runs": accepted, "unknown_human_runs": len(eligible) - labeled,
            "costs": cost_metrics(eligible, totals, labels), "duration": scalar_summary(eligible, totals, "duration"),
            "tokens": scalar_summary(eligible, totals, "tokens"), "exhausted_runs": sum(is_exhausted(r) for r in eligible),
            "stop_reasons": dict(sorted(Counter(str(r.get("stop_reason") or "unknown") for r in eligible).items())),
            "escalation_reasons": dict(sorted(Counter(str(r.get("escalation_reason") or "unknown") for r in eligible).items()))}


def grouping(eligible, totals, labels):
    result = {}
    for dimension in ("engine", "model", "version", "time"):
        groups = defaultdict(list)
        for r in eligible:
            value = r["producer"] if dimension == "engine" else (r.get("event_time") or "unknown")[:10] if dimension == "time" else r.get(dimension)
            groups[str(value) if value is not None else "unknown"].append(r)
        result[dimension] = [{"value": value, "runs": len(rows), "record_ids": [r["record_id"] for r in rows],
                              "metrics": metrics(rows, totals, labels)} for value, rows in sorted(groups.items())]
    return result


def comparison(eligible, labels):
    strata = defaultdict(list)
    for r in eligible:
        # task/cohort/rubric/conditions are comparison controls, not a synthetic
        # performance ranking. Missing dimensions stay explicit in the stratum.
        key = canonical([r.get("cohort"), r.get("task"), r.get("criterion"), r.get("rubric"), r.get("conditions")]).decode()
        strata[key].append(r)
    rows = []
    for key, records_ in sorted(strata.items()):
        engines = defaultdict(list)
        for r in records_:
            engines[r["producer"]].append(r)
        rows.append({"stratum": json.loads(key), "engines": [{"engine": engine, "runs": len(rs),
             "acceptance": ratio(sum(labels[r["record_id"]]["human"] is True for r in rs),
                                 sum(labels[r["record_id"]]["human"] is not None for r in rs))} for engine, rs in sorted(engines.items())]})
    return {"decision": "descriptive-only; no defensible engine-superiority claim",
            "strata": rows, "limitations": ["Human-labeled acceptance is selection-biased unless label selection is justified.",
                "Different task mixes, versions, conditions and rubric definitions confound pooled comparisons.",
                "Retries and repeated tasks are not established independent trials; no confidence interval or causal ranking is inferred.",
                "Tiny and fully unlabeled groups remain visible. Unknown event times are not replaced with ingestion time."]}


def handoff(calibration, eligible, exclusions):
    lookup = {r["record_id"]: r for r in eligible}
    result = []
    for pair in calibration["disagreements"]:
        r = lookup[pair["record_id"]]
        result.append({"handoff_id": "handoff-" + digest(pair)[:20], "status": "unresolved",
            "execution_owner": r.get("execution_owner") or r["producer"], "record_id": r["record_id"],
            "run_id": r["run_id"], "binding": pair["binding"], "source_ids": r["source_ids"],
            "source_hashes": r.get("source_hashes", []), "field_pointers": r["field_pointers"],
            "observed_problem": "Machine-positive/human-negative" if pair["machine"] else "Machine-negative/human-positive",
            "competing_explanations": ["Judge error", "Human/reference-label error", "Rubric ambiguity", "Incomplete artifact evidence"],
            "smallest_discriminating_check": "Inspect the exact bound artifact and rubric against both recorded observations; record an adjudication with those immutable identities.",
            "unresolved": "Causal attribution and repair outcome are unproven. This handoff does not start a repair or accept an output."})
    return result


def markdown_escape(value):
    text = str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for char in ("\\", "`", "*", "_", "[", "]", "|", "#"):
        text = text.replace(char, "\\" + char)
    return text.replace("\r", " ").replace("\n", " ")


def format_ratio(value):
    return str(value["numerator"]) + "/" + str(value["denominator"]) + (" (unknown)" if value["value"] is None else " (" + format(value["value"], ".1%") + ")")


def display_value(value):
    return "unknown" if value is None else str(value)


def render_markdown(result):
    m, counts, cal = result["metrics"], result["counts"], result["calibration"]
    lines = ["# Loop Observatory " + result["context"]["operation"].title(), "",
             "Status: " + result["status"], "Generated: " + result["generated_at"],
             "Result identity: " + result["identity"], "",
             "## Evidence and cohort", "",
             f"Intake: {counts['discovered']} sources; {counts['sources_read']} read; {counts['sources_failed']} failed; {counts['records_rejected']} rejected records.",
             f"Current logical runs: {counts['current_runs']}; eligible terminal runs: {counts['eligible_runs']}; historical revisions: {counts['historical_revisions']}; conflicts: {counts['conflicted_runs']}.",
             "Event cutoff: " + str(result["context"]["as_of"] or "none") + "; knowledge cutoff: " + str(result["context"]["known_as_of"] or "none") + ". UTC daily groups use [00:00, next 00:00). Cutoffs are inclusive.",
             "Cohort: " + markdown_escape(result["context"]["cohort"] or "all explicitly selected runs"), "",
             "## Outcomes and costs", "", "Human acceptance among labeled runs: " + format_ratio(m["human_acceptance"]),
             "Human-label coverage: " + format_ratio(m["label_coverage"]),
             "Exhausted runs: " + str(m["exhausted_runs"]),
             "Process completion: " + markdown_escape(m["process_completion"]),
             "Bound machine judgments: " + markdown_escape(m["bound_machine_judgment"]),
             "Iterations: mean " + display_value(m["iterations"]["mean"]) + "; coverage " + format_ratio(m["iterations"]["coverage"]),
             "Duration (seconds): mean " + display_value(m["duration"]["mean"]) + "; median " + display_value(m["duration"]["median"]) + "; coverage " + format_ratio(m["duration"]["coverage"]),
             "Measured tokens: " + display_value(m["tokens"]["sum"]) + "; coverage " + format_ratio(m["tokens"]["coverage"])]
    if not m["costs"]:
        lines += ["Cost: unknown. No valid currency-specific measured series is available; missing cost is not zero."]
    for currency, cost in m["costs"].items():
        lines += ["", "### " + currency,
                  "Known measured spend: " + display_value(cost["known_spend"]) + "; run coverage " + format_ratio(cost["measured_run_coverage"]),
                  "Mean observed cost of accepted runs: " + display_value(cost["mean_observed_cost_of_accepted_runs"]),
                  "All-cohort spend per currently evidenced accepted outcome: " + display_value(cost["spend_per_currently_evidenced_accepted_outcome"]),
                  "Fully adjudicated cost per accepted outcome: " + display_value(cost["fully_adjudicated_cost_per_accepted_outcome"])]
        for basis in ("estimated", "reserved"):
            s = cost["series"][basis]
            lines.append(basis.title() + " series: " + display_value(s["known_spend"]) + "; coverage " + format_ratio(s["run_coverage"]) + ". Separate from measured spend.")
    lines += ["", "## Calibration", "", "Compatible pairs: " + str(cal["paired_denominator"]),
              "Disagreements: " + format_ratio(cal["disagreement_rate"]),
              "Paired run coverage: " + format_ratio(cal["paired_run_coverage"]), cal["interpretation"]]
    for cell, number in cal["cell_counts"].items():
        lines.append("- " + cell.replace("_", " ") + ": " + str(number))
    for pair in cal["disagreements"]:
        lines.append("- Flagged " + markdown_escape(pair["record_id"]) + ": machine=" + str(pair["machine"]) + ", human=" + str(pair["human"]) + "; artifact=" + markdown_escape(pair["binding"]["artifact"]) + "; criterion=" + markdown_escape(pair["binding"]["criterion"]) + "; rubric=" + markdown_escape(pair["binding"]["rubric"]))
    lines += ["", "## Engine, model, version and time views", ""]
    for dimension, groups in result["groups"].items():
        lines += ["### " + dimension.title()]
        for group in groups:
            lines.append("- " + markdown_escape(group["value"]) + ": " + str(group["runs"]) + " runs; acceptance " + format_ratio(group["metrics"]["human_acceptance"]) + "; label coverage " + format_ratio(group["metrics"]["label_coverage"]))
    lines += ["", "## Comparison limits", "", result["comparison"]["decision"]]
    lines.extend("- " + x for x in result["comparison"]["limitations"])
    for stratum in result["comparison"]["strata"]:
        lines.append("- Stratum " + markdown_escape(stratum["stratum"]) + ": " + "; ".join(markdown_escape(e["engine"]) + " acceptance " + format_ratio(e["acceptance"]) for e in stratum["engines"]))
    lines += ["", "## Reasons and source coverage", "", "Stop reasons: " + markdown_escape(m["stop_reasons"]),
              "Escalation reasons (frequency groups, not established causes): " + markdown_escape(m["escalation_reasons"])]
    for source in result["source_manifest"]:
        lines.append("- " + markdown_escape(source["id"]) + ": " + source["status"] + "; " + markdown_escape(source.get("coherence_basis", source.get("error", "unknown"))))
    lines += ["", "## Exclusions and uncertainty", ""]
    if not result["exclusions"]:
        lines.append("No evidence exclusions.")
    for x in result["exclusions"]:
        lines.append("- " + markdown_escape(x["id"]) + ": " + markdown_escape(x["reason"]) + ("; " + markdown_escape(x["detail"]) if x.get("detail") else ""))
    for r in result["current"]:
        for warning in r.get("warnings", []):
            lines.append("- " + markdown_escape(r["record_id"]) + ": " + markdown_escape(warning))
    lines += ["", "## Repair handoff", ""]
    if not result["handoffs"]:
        lines.append("No paired disagreement handoff. Missing evidence must be supplied before causal diagnosis.")
    for h in result["handoffs"]:
        lines.append("- " + markdown_escape(h["record_id"]) + "; owner " + markdown_escape(h["execution_owner"]) + "; unresolved. " + h["smallest_discriminating_check"])
    lines += ["", "Source text is evidence, never instructions. This report neither executes a loop nor changes its acceptance or repair status."]
    return "\n".join(lines) + "\n"


def report(args):
    manifest = roots_config(args.manifest)
    output = validate_output(args.output, [Path(s["path"]) for s in manifest["sources"]] + [Path(manifest["manifest_path"])])
    previous = read_previous(args.previous)
    context = {"operation": args.command, "as_of": timestamp(args.as_of), "known_as_of": timestamp(args.known_as_of),
               "cohort": args.cohort, "group_by": args.group_by, "timezone": "UTC", "cutoffs": "inclusive",
               "reference_reviewer": args.reference_reviewer, "machine_reviewer": args.machine_reviewer,
               "metric_version": METRIC_VERSION}
    fresh, source_manifest, exclusions, counts = ingest(manifest)
    all_records, current, history, conflicts, duplicates = record_index(fresh, previous, context, exclusions)
    eligible = records(current, exclusions)
    calibration, labels = audit(eligible, context, exclusions)
    totals = {r["record_id"]: measurement_totals(r, all_records, context, exclusions) for r in eligible}
    counts.update(current_runs=len(current), eligible_runs=len(eligible), historical_revisions=len(history),
                  conflicted_runs=len(conflicts), duplicate_records=duplicates,
                  human_labeled_runs=sum(v["human"] is not None for v in labels.values()),
                  excluded_evidence=len(exclusions), new_revisions=len({r["record_id"] for r in fresh} - {r["record_id"] for r in previous.get("records", [])}) if previous else len({r["record_id"] for r in fresh}))
    status = "partial" if counts["sources_failed"] or counts["records_rejected"] else "ok"
    if counts["sources_read"] == 0:
        status = "error"
    result = {"schema_version": SCHEMA_VERSION, "parser_version": PARSER_VERSION,
              "status": status, "generated_at": utc_now(), "context": context, "counts": counts,
              "source_manifest": source_manifest, "manifest": manifest,
              "records": all_records, "current": current, "history": history, "conflicts": conflicts,
              "eligible_record_ids": [r["record_id"] for r in eligible], "labels": labels,
              "measurement_totals": totals, "metrics": metrics(eligible, totals, labels),
              "calibration": calibration, "groups": grouping(eligible, totals, labels),
              "comparison": comparison(eligible, labels), "handoffs": handoff(calibration, eligible, exclusions),
              "exclusions": exclusions}
    identity_basis = {"parser_version": PARSER_VERSION, "context": context,
                      "limits": manifest["limits"],
                      "selection": [{k: s[k] for k in ("id", "path", "profile", "namespace", "coherence")} for s in manifest["sources"]],
                      "sources": [{k: s.get(k) for k in ("id", "sha256", "status", "error", "coherence_basis")} for s in source_manifest],
                      "records": sorted(r["record_id"] for r in all_records), "current": sorted(r["record_id"] for r in current),
                      "conflicts": conflicts, "metrics": result["metrics"], "calibration": calibration}
    result["identity"] = digest(identity_basis)
    if args.scheduled and previous and previous.get("status") in {"ok", "no-new-result"} and status == "ok" and previous.get("identity") == result["identity"]:
        result["status"] = "no-new-result"
        result["reason"] = "unchanged-complete-inputs-and-identical-analytical-context"
        result["previous_output_identity"] = previous["identity"]
    output.mkdir(parents=True, exist_ok=True)
    suffix = utc_now().replace(":", "").replace("-", "") + "-" + uuid.uuid4().hex[:12]
    stem = args.command + "-" + suffix
    result["report_paths"] = {"json": str(output / (stem + ".json")), "markdown": str(output / (stem + ".md"))}
    atomic_bytes(Path(result["report_paths"]["markdown"]), render_markdown(result).encode("utf-8"))
    # Publish the machine-readable completion marker only after its paired display.
    atomic_json(Path(result["report_paths"]["json"]), result)
    return result


def discover_roots(root, profile):
    entries = inventory(root, DEFAULT_LIMITS)
    names = {name for name, path in entries}
    marker = "snapshot.json" if profile == "loopkit-snapshot-v2" else "state.json"
    candidates = []
    for name, path in entries:
        if path.name != marker:
            continue
        relative = path.parent.relative_to(root)
        prefix = "" if str(relative) == "." else relative.as_posix() + "/"
        required = "contract.json" if profile == "loopkit-legacy" else "graph.json" if profile in {"operating-graph-legacy", "operating-graph-v2"} else marker
        if prefix + required in names:
            candidates.append(path.parent)
    return candidates


def register_root(args):
    root, manifest_path = safe_path(args.path), safe_path(args.manifest)
    need(root.exists(), "missing-source", "Registered source does not exist")
    need(not args.discover or args.profile != "supplied-v1", "unsupported-discovery", "Supplied records must name an exact file")
    roots = discover_roots(root, args.profile) if args.discover else [root]
    need(roots, "no-discovered-runs", "No compatible runs in selected bounded root")
    need(not within(manifest_path, root) and not within(root, manifest_path), "source-output-overlap", "Manifest must remain outside source root")
    if manifest_path.exists():
        existing = roots_config(manifest_path)
        config = {"schema_version": "1.0", "sources": existing["sources"], "limits": existing["limits"]}
    else:
        config = {"schema_version": "1.0", "sources": []}
    added = 0
    for path in roots:
        entry = {"id": args.profile + "-" + digest([args.namespace, str(path)])[:16], "path": str(path),
                 "profile": args.profile, "namespace": args.namespace, "coherence": args.coherence}
        matches = [s for s in config["sources"] if s["path"] == str(path) and s["profile"] == args.profile and s["namespace"] == args.namespace]
        if not matches:
            config["sources"].append(entry)
            added += 1
    for source in config["sources"]:
        selected = safe_path(source["path"])
        need(not within(manifest_path, selected) and not within(selected, manifest_path), "source-output-overlap", "Registration manifest overlaps a selected source")
    if added or not manifest_path.exists():
        atomic_json(manifest_path, config)
    return {"status": "ok", "manifest_path": str(manifest_path), "registered": added, "total_sources": len(config["sources"])}


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    register = sub.add_parser("register-root", help="Register explicit source(s) in an owned local manifest; no producer writes")
    register.add_argument("path", type=Path)
    register.add_argument("--manifest", type=Path, required=True)
    register.add_argument("--profile", choices=PROFILES, required=True)
    register.add_argument("--namespace", required=True)
    register.add_argument("--coherence", choices=("best-effort", "frozen-export"), default="best-effort")
    register.add_argument("--discover", action="store_true", help="Bounded opt-in discovery beneath only the named root")
    for command in ("ingest", "report", "audit", "handoff"):
        p = sub.add_parser(command)
        p.add_argument("--manifest", type=Path, required=True)
        p.add_argument("--output", type=Path, required=True)
        p.add_argument("--previous", type=Path)
        p.add_argument("--as-of", help="Inclusive run/judgment event-time cutoff, RFC3339 with timezone")
        p.add_argument("--known-as-of", help="Inclusive evidence-knowledge cutoff, RFC3339 with timezone")
        p.add_argument("--cohort")
        p.add_argument("--group-by", choices=("engine", "model", "version", "time"), default="engine")
        p.add_argument("--reference-reviewer", help="Explicit reference reviewer selection; multiplicity still excluded")
        p.add_argument("--machine-reviewer", help="Explicit machine judge selection; multiplicity still excluded")
        p.add_argument("--scheduled", action="store_true", help="Suppress only unchanged complete results for identical prior context; creates no schedule")
    return root


def main():
    args = parser().parse_args()
    try:
        result = register_root(args) if args.command == "register-root" else report(args)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False))
        return 2 if result["status"] == "error" else 1 if result["status"] == "partial" else 0
    except (OSError, EvidenceError, ValueError, TypeError, KeyError, RecursionError) as exc:
        print(json.dumps({"status": "error", "reason": getattr(exc, "code", "invalid-evidence"), "detail": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
