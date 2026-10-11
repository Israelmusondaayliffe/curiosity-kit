"""Local evaluation evidence and guarded promotion. No model/provider execution.

Contracts are independent of legacy HE schema1. Imported attestations are claims,
not authenticated execution or consent. See references/evaluation-contract.md.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import re
import shutil
import stat
import statistics
import tempfile
from pathlib import Path
from typing import Any, Optional

from .common import HectlError, now_iso, sha256_file, write_json

VERSION = 1
EXCLUSIONS = (".git", "__pycache__", ".pytest_cache", ".DS_Store")
MAX_JSON = 16 * 1024 * 1024
MAX_ARTIFACT = 64 * 1024 * 1024
ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
SHA = re.compile(r"^[0-9a-f]{64}$")
STATUSES = {"pass", "fail", "blocked", "invalid", "interrupted", "missing", "not-applicable"}
METRICS = {"duration_seconds", "tokens", "characters", "tool_calls", "cost_amount", "cost_currency"}


def require(condition: Any, message: str) -> None:
    if not condition:
        raise HectlError(message)


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def count(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def identifier(value: Any) -> str:
    require(isinstance(value, str) and bool(ID.fullmatch(value)), "unsafe or missing identifier")
    return value


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                                     allow_nan=False).encode("utf-8")).hexdigest()


def seal(record: dict, field: str) -> dict:
    out = copy.deepcopy(record)
    out.pop(field, None)
    out[field] = digest(out)
    return out


def check_seal(record: dict, field: str) -> None:
    require(isinstance(record, dict), "record must be an object")
    expected = record.get(field)
    body = {k: v for k, v in record.items() if k != field}
    require(isinstance(expected, str) and digest(body) == expected, field + " mismatch")


def safe_path(value: Any, exists: bool = False) -> Path:
    require(isinstance(value, (str, Path)), "path must be text")
    path = Path(value).expanduser()
    require(path.is_absolute(), "use an explicit absolute path")
    for ancestor in (path, *path.parents):
        require(not ancestor.is_symlink(), "symlink path refused: " + str(ancestor))
    path = path.resolve(strict=False)
    require(path != Path(path.anchor), "filesystem root is too broad")
    if exists:
        require(path.exists(), "path does not exist: " + str(path))
    return path


def relative(value: Any) -> str:
    require(isinstance(value, str) and value and "\\" not in value, "invalid relative path")
    p = Path(value)
    require(not p.is_absolute() and all(x not in ("", ".", "..") for x in value.split("/")),
            "unsafe relative path: " + str(value))
    require(not any(x in EXCLUSIONS for x in p.parts), "excluded path: " + value)
    return p.as_posix()


def disjoint(*paths: Path) -> None:
    for i, a in enumerate(paths):
        for b in paths[i + 1:]:
            require(a != b and a not in b.parents and b not in a.parents,
                    "paths must be disjoint: %s and %s" % (a, b))


def _pairs(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, "duplicate JSON key: " + key)
        obj[key] = value
    return obj


def read_record(value: Any) -> dict:
    path = safe_path(value, True)
    require(path.is_file() and path.stat().st_size <= MAX_JSON, "JSON must be a bounded regular file")
    try:
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_pairs,
                          parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    except (ValueError, UnicodeError) as exc:
        raise HectlError("invalid JSON: " + str(exc))
    require(isinstance(data, dict), "JSON record must be an object")
    return data


def save_new(value: Any, data: dict, protected=()) -> Path:
    path = safe_path(value)
    require(not path.exists(), "evidence already exists; choose a new output: " + str(path))
    for root in protected:
        disjoint(path, safe_path(root))
    path.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation prevents a concurrent run from overwriting evidence.
    payload = (json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode()
    require(len(payload) <= MAX_JSON, "record exceeds the bounded JSON size; reduce declared scope")
    fd, temporary = tempfile.mkstemp(prefix=".he-evidence-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, path)
    finally:
        os.unlink(temporary)
    return path


def header(data: dict, kind: str) -> None:
    require(isinstance(data, dict) and type(data.get("schema_version")) is int
            and data["schema_version"] == VERSION and data.get("kind") == kind,
            "expected %s schema_version %s" % (kind, VERSION))


def snapshot(target: Any, paths: Optional[list] = None) -> dict:
    root = safe_path(target, True)
    require(root.is_dir(), "target must be a directory")
    entries = []
    if paths is None:
        names = []
        for folder, directories, files in os.walk(root, followlinks=False):
            directories[:] = sorted(d for d in directories if d not in EXCLUSIONS)
            for name in directories + sorted(files):
                p = Path(folder) / name
                if name not in EXCLUSIONS:
                    names.append(p.relative_to(root).as_posix())
    else:
        require(isinstance(paths, list) and paths, "declare at least one target path")
        names = [relative(p) for p in paths]
        require(len(set(p.casefold() for p in names)) == len(names), "duplicate/aliased target paths")
    for name in sorted(names):
        p = safe_path(root / relative(name))
        if not p.exists():
            entries.append({"path": name, "type": "absent", "mode": None, "size": 0, "sha256": None})
            continue
        mode = stat.S_IMODE(p.stat().st_mode)
        require(not mode & 0o7000, "special mode bits refused: " + name)
        if p.is_dir():
            require(paths is None, "declared target paths must name files, not directories: " + name)
            entries.append({"path": name, "type": "directory", "mode": mode, "size": 0, "sha256": None})
        else:
            require(p.is_file(), "non-regular target: " + name)
            entries.append({"path": name, "type": "file", "mode": mode,
                            "size": p.stat().st_size, "sha256": sha256_file(p)})
    identity = {"kind": "he-framed-tree", "schema_version": VERSION,
                "exclusions": list(EXCLUSIONS), "entries": entries}
    return dict(identity, root=str(root), digest=digest(identity))


def stage(target: Any, output: Any, paths: list, manifest: Any) -> dict:
    root, out, report = safe_path(target, True), safe_path(output), safe_path(manifest)
    disjoint(root, out, report)
    require(not out.exists() and not report.exists(), "stage and manifest must be new")
    before = snapshot(root, paths)
    require(any(e["type"] == "file" for e in before["entries"]), "nothing to stage")
    out.mkdir(parents=True)
    for e in before["entries"]:
        if e["type"] == "file":
            dest = out / e["path"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / e["path"], dest)
    require(snapshot(root, paths)["digest"] == before["digest"], "source drifted during staging; stage is unqualified")
    result = {"kind": "he-stage", "schema_version": VERSION, "source": before,
              "candidate": snapshot(out, paths), "created_at": now_iso(), "status": "staged-unqualified"}
    save_new(report, result, (root, out))
    return result


def validate_suite(data: dict) -> dict:
    header(data, "he-eval-suite")
    require(set(data) == {"kind", "schema_version", "suite_id", "coverage_rationale", "target_paths", "adapter", "judge", "limits", "holdout", "cases"}, "unknown/missing suite fields")
    identifier(data.get("suite_id"))
    require(text(data.get("coverage_rationale")), "suite needs coverage_rationale")
    paths = data.get("target_paths")
    require(isinstance(paths, list) and paths, "suite needs declared target_paths")
    names = [relative(p) for p in paths]
    require(len(set(p.casefold() for p in names)) == len(names), "duplicate target paths")
    adapter = data.get("adapter")
    require(isinstance(adapter, dict) and set(adapter) == {"id", "revision", "model", "settings"}, "adapter fields must be id/revision/model/settings")
    identifier(adapter["id"])
    require(text(adapter["revision"]) and (adapter["model"] is None or text(adapter["model"]))
            and isinstance(adapter["settings"], dict), "invalid adapter identity")
    judge = data.get("judge")
    require(isinstance(judge, dict) and set(judge) == {"id", "revision", "model", "settings"}, "judge identity fields required")
    identifier(judge["id"])
    require(text(judge["revision"]) and (judge["model"] is None or text(judge["model"])) and isinstance(judge["settings"], dict), "judge identity invalid")
    limits = data.get("limits")
    required = {"max_runs", "max_launches", "max_repair_cycles", "max_low_yield_cycles"}
    require(isinstance(limits, dict) and set(limits) == required, "suite needs finite named limits")
    require(all(count(v) and v > 0 for v in limits.values()), "limits must be positive integers")
    holdout = data.get("holdout")
    require(isinstance(holdout, dict) and holdout.get("status") in ("untouched", "used-for-selection", "not-claimed")
            and text(holdout.get("evidence")), "holdout declaration required")
    cases = data.get("cases")
    require(isinstance(cases, list) and cases, "suite cases must be nonempty")
    ids = set()
    for case in cases:
        require(isinstance(case, dict), "case must be an object")
        require(set(case) == {"case_id", "kind", "split", "required", "prompt", "expectation", "criteria", "fixtures"}, "unknown/missing case fields")
        cid = identifier(case.get("case_id"))
        require(cid not in ids, "duplicate case_id")
        ids.add(cid)
        require(case.get("kind") in ("trigger", "functional", "qualitative"), "invalid case kind")
        require(case.get("split") in ("train", "validation", "test"), "case split required")
        require(type(case.get("required")) is bool, "case required must be boolean")
        require(text(case.get("prompt")) and text(case.get("expectation")), "case prompt/expectation required")
        criteria = case.get("criteria")
        require(isinstance(criteria, list) and criteria, "each case needs source-bound criteria")
        criterion_ids = set()
        for c in criteria:
            require(isinstance(c, dict), "criterion must be an object")
            require(set(c) == {"id", "description", "source"}, "unknown criterion fields")
            key = identifier(c.get("id"))
            require(key not in criterion_ids and text(c.get("description")) and text(c.get("source")), "invalid/duplicate criterion")
            criterion_ids.add(key)
        fixtures = case.get("fixtures")
        require(isinstance(fixtures, list), "fixtures must be a list (possibly empty)")
        for f in fixtures:
            require(isinstance(f, dict) and text(f.get("path")) and isinstance(f.get("sha256"), str)
                    and SHA.fullmatch(f["sha256"]), "fixture needs path and sha256")
    require(any(c["required"] for c in cases), "at least one case must be required")
    return {"valid": True, "suite_digest": digest(data), "adapter_digest": digest(adapter),
            "judge_digest": digest(judge), "case_digests": {c["case_id"]: digest(c) for c in cases}}


def metrics(data: Any) -> dict:
    require(isinstance(data, dict) and set(data) <= METRICS, "unknown/malformed metrics")
    out = {k: data.get(k) for k in METRICS}
    for key, value in out.items():
        if key == "cost_currency":
            require(value is None or bool(re.fullmatch(r"[A-Z]{3}", str(value))), "currency must be ISO-style uppercase code or null")
        elif value is not None:
            require(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0,
                    "metrics must be nonnegative finite numbers or null")
            if key in ("tokens", "characters", "tool_calls"):
                require(count(value), key + " must be integer or null")
    require(out["cost_amount"] is None or out["cost_currency"] is not None, "known cost needs currency")
    return out


def artifact(root: Path, item: dict) -> dict:
    require(isinstance(item, dict) and set(item) in ({"path", "sha256"}, {"path", "sha256", "size"}), "artifact must contain only path/hash and optional size")
    name = relative(item.get("path"))
    p = safe_path(root / name, True)
    require(p.is_file() and p.stat().st_size <= MAX_ARTIFACT, "artifact missing/nonregular/too large")
    actual = sha256_file(p)
    require(item.get("sha256") == actual, "artifact digest mismatch: " + name)
    return {"path": name, "sha256": actual, "size": p.stat().st_size}


def record_run(suite_path: Any, target: Any, results_path: Any, artifacts: Any, output: Any) -> dict:
    suite = read_record(suite_path)
    valid = validate_suite(suite)
    current = snapshot(target, suite["target_paths"])
    artroot = safe_path(artifacts, True)
    require(artroot.is_dir(), "artifacts must be a directory")
    disjoint(safe_path(target), artroot)
    for case in suite["cases"]:
        for fixture in case["fixtures"]:
            f = safe_path(fixture["path"], True)
            require(f.is_file() and sha256_file(f) == fixture["sha256"], "fixture drift: " + str(f))
    incoming = read_record(results_path)
    header(incoming, "he-eval-observations")
    require(set(incoming) == {"kind", "schema_version", "run_id", "suite_digest", "target_digest", "execution_tree_digest", "adapter_digest", "judge_digest", "execution", "cases"}, "unknown/missing observation record fields")
    identifier(incoming.get("run_id"))
    require(incoming.get("suite_digest") == valid["suite_digest"], "suite identity mismatch")
    require(incoming.get("target_digest") == current["digest"], "candidate/source identity mismatch")
    require(incoming.get("execution_tree_digest") == snapshot(target)["digest"], "complete execution tree identity mismatch")
    require(incoming.get("adapter_digest") == valid["adapter_digest"], "adapter identity mismatch")
    require(incoming.get("judge_digest") == valid["judge_digest"], "judge identity mismatch")
    execution = incoming.get("execution")
    require(isinstance(execution, dict) and execution.get("origin") in ("host-attested", "imported", "fixture")
            and type(execution.get("complete")) is bool and type(execution.get("adapter_available")) is bool
            and count(execution.get("launches")) and text(execution.get("evidence")), "explicit execution attestation required")
    require(set(execution) == {"origin", "complete", "adapter_available", "launches", "evidence", "assistance"}, "unknown/missing execution fields")
    assistance = execution.get("assistance")
    require(isinstance(assistance, dict) and set(assistance) == {"status", "details"} and assistance.get("status") in ("unaided", "assisted", "unknown")
            and text(assistance.get("details")), "explicit assistance provenance required")
    require(execution["launches"] <= suite["limits"]["max_launches"], "launch budget exceeded")
    rows = incoming.get("cases")
    require(isinstance(rows, list), "results cases must be an array")
    case_map = {c["case_id"]: c for c in suite["cases"]}
    supplied = {}
    for row in rows:
        require(isinstance(row, dict), "observation must be an object")
        require(set(row) == {"case_id", "case_digest", "status", "notes", "artifacts", "checks", "judgment", "metrics"}, "unknown/missing observation fields")
        cid = row.get("case_id")
        require(cid in case_map and cid not in supplied, "unknown/duplicate observation case")
        require(row.get("case_digest") == valid["case_digests"][cid], "case definition mismatch")
        status = row.get("status")
        require(status in STATUSES, "unknown observation status")
        require(text(row.get("notes")), "observation notes required")
        arts = row.get("artifacts")
        require(isinstance(arts, list), "artifacts must be an array")
        checked = [artifact(artroot, a) for a in arts]
        require(len({a["path"] for a in checked}) == len(checked), "duplicate artifact path")
        checks = row.get("checks")
        require(isinstance(checks, list), "checks must be an array")
        expected = {c["id"] for c in case_map[cid]["criteria"]}
        seen = set()
        for c in checks:
            require(isinstance(c, dict) and set(c) == {"criterion_id", "status", "evidence"} and c.get("criterion_id") in expected and c["criterion_id"] not in seen,
                    "unknown/duplicate criterion result")
            seen.add(c["criterion_id"])
            require(c.get("status") in STATUSES and text(c.get("evidence")), "criterion result needs status/evidence")
        judgment = row.get("judgment")
        require(isinstance(judgment, dict) and set(judgment) == {"reviewer", "mode", "evidence"} and text(judgment.get("reviewer"))
                and judgment.get("mode") in ("self", "identity-visible", "blind", "deterministic", "not-performed")
                and text(judgment.get("evidence")), "explicit judgment provenance required")
        if status in ("pass", "fail"):
            require(execution["adapter_available"] and execution["complete"] and checked and seen == expected,
                    "pass/fail needs complete execution, raw artifacts and all criteria")
            require(judgment["mode"] != "not-performed", "pass/fail needs performed judgment")
            require(all(c["status"] in ("pass", "fail", "not-applicable") for c in checks), "invalid/missing criterion cannot be a quality verdict")
            if status == "pass":
                require(all(c["status"] == "pass" for c in checks), "passing case must pass every declared criterion")
            else:
                require(any(c["status"] == "fail" for c in checks), "failed case needs a failed criterion")
        if status == "not-applicable":
            require(not case_map[cid]["required"], "required case cannot be not-applicable")
        supplied[cid] = {"case_id": cid, "case_digest": row["case_digest"], "kind": case_map[cid]["kind"],
                         "split": case_map[cid]["split"], "required": case_map[cid]["required"], "status": status,
                         "artifacts": checked, "checks": checks, "judgment": judgment,
                         "metrics": metrics(row.get("metrics", {})), "notes": row["notes"]}
    for cid, case in case_map.items():
        if cid not in supplied:
            supplied[cid] = {"case_id": cid, "case_digest": valid["case_digests"][cid], "kind": case["kind"],
                             "split": case["split"], "required": case["required"], "status": "missing", "artifacts": [],
                             "checks": [], "judgment": {"reviewer": "none", "mode": "not-performed", "evidence": "No observation supplied"},
                             "metrics": metrics({}), "notes": "No observation supplied"}
    ordered = [supplied[c["case_id"]] for c in suite["cases"]]
    required = [r for r in ordered if r["required"]]
    overall = ("pass" if all(r["status"] == "pass" for r in required) else
               "fail" if any(r["status"] == "fail" for r in required) else "incomplete")
    result = {"kind": "he-eval-run", "schema_version": VERSION, "run_id": incoming["run_id"],
              "created_at": now_iso(), "suite_digest": valid["suite_digest"], "suite": suite,
              "target_snapshot": current, "execution_tree": snapshot(target), "adapter": suite["adapter"], "adapter_digest": valid["adapter_digest"],
              "judge": suite["judge"], "judge_digest": valid["judge_digest"], "artifacts_root": str(artroot), "execution": execution, "evidence_origin": "declared-import",
              "cases": ordered, "status": overall, "summary": summarize(ordered),
              "limits": ["Imported claims are not authenticated execution, independence or consent."]}
    result = seal(result, "run_digest")
    save_new(output, result, (safe_path(target), artroot))
    return result


def summarize(rows: list) -> dict:
    counts = {s: sum(r["status"] == s for r in rows) for s in sorted(STATUSES)}
    valid = counts["pass"] + counts["fail"]
    costs = [r["metrics"]["cost_amount"] for r in rows]
    currencies = {r["metrics"]["cost_currency"] for r in rows if r["metrics"]["cost_amount"] is not None}
    return {"counts": counts, "valid_quality_observations": valid,
            "pass_rate": counts["pass"] / valid if valid else None,
            "required_total": sum(r["required"] for r in rows),
            "required_passed": sum(r["required"] and r["status"] == "pass" for r in rows),
            "cost_complete": bool(rows) and all(v is not None for v in costs) and len(currencies) == 1,
            "known_cost_total": sum(v for v in costs if v is not None) if len(currencies) == 1 else None,
            "cost_currency": next(iter(currencies)) if len(currencies) == 1 else None,
            "unknown_cost_observations": sum(v is None for v in costs)}


def load_run(value: Any, fresh: bool = False) -> dict:
    run = read_record(value)
    header(run, "he-eval-run")
    check_seal(run, "run_digest")
    valid = validate_suite(run.get("suite"))
    require(run.get("suite_digest") == valid["suite_digest"] and run.get("adapter_digest") == valid["adapter_digest"], "run suite/adapter drift")
    require(run.get("judge_digest") == valid["judge_digest"] and run.get("judge") == run["suite"]["judge"], "run judge mismatch")
    require(run.get("evidence_origin") == "declared-import" and run.get("adapter") == run["suite"]["adapter"], "run provenance/adapter mismatch")
    rows = run.get("cases")
    require(isinstance(rows, list) and len(rows) == len(run["suite"]["cases"]), "run coverage missing")
    execution = run.get("execution")
    require(isinstance(execution, dict) and execution.get("origin") in ("fixture", "imported", "host-attested")
            and count(execution.get("launches")) and type(execution.get("complete")) is bool
            and type(execution.get("adapter_available")) is bool and text(execution.get("evidence")), "run execution invalid")
    require(set(execution) == {"origin", "complete", "adapter_available", "launches", "evidence", "assistance"}, "unknown/missing execution fields")
    assistance = execution.get("assistance")
    require(isinstance(assistance, dict) and set(assistance) == {"status", "details"} and assistance.get("status") in ("unaided", "assisted", "unknown") and text(assistance.get("details")), "run assistance missing")
    require(execution["launches"] <= run["suite"]["limits"]["max_launches"], "launch budget exceeded")
    for row, definition in zip(rows, run["suite"]["cases"]):
        require(isinstance(row, dict) and row.get("case_id") == definition["case_id"]
                and row.get("case_digest") == digest(definition) and row.get("required") is definition["required"]
                and row.get("kind") == definition["kind"] and row.get("split") == definition["split"], "run case identity/coverage mismatch")
        require(row.get("status") in STATUSES, "run status invalid")
        metrics(row.get("metrics"))
        require(isinstance(row.get("artifacts"), list) and isinstance(row.get("checks"), list), "run artifacts/checks missing")
        for a in row["artifacts"]:
            relative(a.get("path"))
            require(isinstance(a.get("sha256"), str) and SHA.fullmatch(a["sha256"]) and count(a.get("size")), "run artifact identity invalid")
        if row["status"] in ("pass", "fail"):
            require(execution["complete"] and execution["adapter_available"] and row["artifacts"], "quality verdict lacks execution/artifacts")
            checks = row["checks"]
            require(len(checks) == len(definition["criteria"]) and {c.get("criterion_id") for c in checks} == {c["id"] for c in definition["criteria"]}, "criterion coverage missing")
            require(all(c.get("status") in ("pass", "fail", "not-applicable") and text(c.get("evidence")) for c in checks), "criterion validity missing")
            require(all(c["status"] == "pass" for c in checks) if row["status"] == "pass" else any(c["status"] == "fail" for c in checks), "case verdict contradicts checks")
            judgment = row.get("judgment", {})
            require(judgment.get("mode") in ("self", "identity-visible", "blind", "deterministic") and text(judgment.get("reviewer")) and text(judgment.get("evidence")), "judgment missing")
        require(not (row["required"] and row["status"] == "not-applicable"), "required case cannot be not-applicable")
    expected_status = "pass" if all(r["status"] == "pass" for r in rows if r["required"]) else "fail" if any(r["status"] == "fail" for r in rows if r["required"]) else "incomplete"
    require(run.get("status") == expected_status and run.get("summary") == summarize(rows), "summary/verdict does not match complete case evidence")
    if fresh:
        for case in run["suite"]["cases"]:
            for fixture in case["fixtures"]:
                require(sha256_file(safe_path(fixture["path"], True)) == fixture["sha256"], "fixture drift after evaluation")
        require(snapshot(run["target_snapshot"]["root"], run["suite"]["target_paths"])["digest"] == run["target_snapshot"]["digest"], "evaluated target drifted")
        require(snapshot(run["target_snapshot"]["root"])["digest"] == run["execution_tree"]["digest"], "execution tree drifted (including undeclared files)")
        for row in run["cases"]:
            for a in row["artifacts"]:
                artifact(safe_path(run["artifacts_root"], True), a)
    return run


def compare(baseline: Any, candidate: Any) -> dict:
    def selected(path):
        record = read_record(path)
        if record.get("kind") == "he-eval-baseline":
            header(record, "he-eval-baseline")
            check_seal(record, "baseline_digest")
            run = load_run(record["run_path"])
            require(run["run_digest"] == record["run_digest"], "pinned baseline run changed")
            return run
        return load_run(path)
    a, b = selected(baseline), selected(candidate)
    compatible = (a["suite_digest"] == b["suite_digest"] and a["adapter_digest"] == b["adapter_digest"]
                  and a["judge_digest"] == b["judge_digest"] and a["execution"]["assistance"]["status"] == b["execution"]["assistance"]["status"]
                  and a["execution"]["origin"] == b["execution"]["origin"])
    rows = []
    old = {r["case_id"]: r for r in a["cases"]}
    new = {r["case_id"]: r for r in b["cases"]}
    case_ids = list(old) + [cid for cid in new if cid not in old]
    for cid in case_ids:
        prior, row = old.get(cid), new.get(cid)
        matched = compatible and prior is not None and row is not None and prior["case_digest"] == row["case_digest"]
        quality = matched and prior["status"] in ("pass", "fail") and row["status"] in ("pass", "fail")
        verdict = ("regression" if prior["status"] == "pass" and row["status"] == "fail" else
                   "improvement" if prior["status"] == "fail" and row["status"] == "pass" else "tie") if quality else "inconclusive"
        rows.append({"case_id": cid, "matched": matched, "baseline": prior["status"] if prior else "missing",
                     "candidate": row["status"] if row else "missing", "verdict": verdict,
                     "baseline_required": prior["required"] if prior else None,
                     "candidate_required": row["required"] if row else None})
    removed = sorted(set(old) - set(new))
    added = sorted(set(new) - set(old))
    removed_required = [cid for cid in removed if old[cid]["required"]]
    added_required = [cid for cid in added if new[cid]["required"]]
    changed_requiredness = sorted(cid for cid in set(old) & set(new) if old[cid]["required"] != new[cid]["required"])
    weakened = [cid for cid in changed_requiredness if old[cid]["required"] and not new[cid]["required"]]
    observed_regression = any(r["verdict"] == "regression" for r in rows)
    return {"compatible": compatible, "baseline_run": a["run_digest"], "candidate_run": b["run_digest"],
            "cases": rows, "regression": observed_regression,
            "regression_assessment": "regression" if observed_regression else "inconclusive" if any(r["verdict"] == "inconclusive" for r in rows) else "no-observed-regression",
            "coverage_regression": bool(removed_required or weakened),
            "coverage": {"baseline_cases": len(old), "candidate_cases": len(new),
                         "removed_cases": removed, "added_cases": added,
                         "removed_required_cases": removed_required, "added_required_cases": added_required,
                         "changed_requiredness": changed_requiredness, "weakened_required_cases": weakened},
            "note": "Regression reports observed matched quality failures only. Coverage loss is separate; incompatible or missing cases remain inconclusive, never evidence of no regression."}



def _benchmark_stats(values: list) -> dict:
    known = [v for v in values if v is not None]
    return {"observations": len(values), "n": len(known), "unknown": len(values) - len(known),
            "mean": statistics.mean(known) if known else None,
            "sample_stddev": statistics.stdev(known) if len(known) >= 2 else None,
            "min": min(known) if known else None, "max": max(known) if known else None}


def aggregate(candidate_paths: list, baseline_paths: Optional[list] = None, output: Any = None) -> dict:
    """Descriptive repeated-run evidence. A repeat is an actual distinct validated run.

    Role means are case-observation means; deltas compare matched case conditions,
    not invented paired trials or significance. Invalid quality still consumes work.
    """
    require(isinstance(candidate_paths, list) and candidate_paths, "aggregate needs at least one candidate run")
    roles = {"candidate": [load_run(p) for p in candidate_paths]}
    if baseline_paths:
        roles["baseline"] = [load_run(p) for p in baseline_paths]
    all_runs = [r for runs in roles.values() for r in runs]
    require(len({r["run_digest"] for r in all_runs}) == len(all_runs), "duplicate run evidence cannot count as another repeat")
    def condition(run):
        return {"suite_digest": run["suite_digest"], "adapter_digest": run["adapter_digest"],
                "judge_digest": run["judge_digest"], "assistance": run["execution"]["assistance"],
                "execution_origin": run["execution"]["origin"]}
    frozen_condition = condition(all_runs[0])
    require(all(condition(r) == frozen_condition for r in all_runs),
            "incomparable suite, adapter, judge, assistance or evidence-origin groups; aggregate separately")
    currencies = {row["metrics"]["cost_currency"] for r in all_runs for row in r["cases"] if row["metrics"]["cost_amount"] is not None}
    require(len(currencies) <= 1, "mixed measured cost currencies; aggregate separately without currency conversion")
    currency = next(iter(currencies)) if currencies else None
    metric_names = ["quality_pass", "duration_seconds", "tokens", "characters", "tool_calls", "cost_amount"]
    def value(row, metric):
        if metric == "quality_pass":
            return 1.0 if row["status"] == "pass" else 0.0 if row["status"] == "fail" else None
        return row["metrics"][metric]
    def grouped(rows):
        return {"status_counts": {st: sum(r["status"] == st for r in rows) for st in sorted(STATUSES)},
                "metrics": {m: _benchmark_stats([value(r, m) for r in rows]) for m in metric_names}}
    summaries = {}
    for role, runs in roles.items():
        first = runs[0]
        target_identity = {"declared_digest": first["target_snapshot"]["digest"],
                           "execution_tree_digest": first["execution_tree"]["digest"]}
        require(all(r["target_snapshot"]["digest"] == target_identity["declared_digest"] and
                    r["execution_tree"]["digest"] == target_identity["execution_tree_digest"] for r in runs),
                "incomparable targets within " + role + "; freeze one target revision per role")
        require(len({r["run_id"] for r in runs}) == len(runs), "duplicate run_id within " + role)
        definitions = first["suite"]["cases"]
        rows = [row for r in runs for row in r["cases"]]
        by_case = {}
        for definition in definitions:
            cid = definition["case_id"]
            selected = [row for row in rows if row["case_id"] == cid]
            by_case[cid] = dict(grouped(selected), case_digest=digest(definition),
                               kind=definition["kind"], required=definition["required"])
        summaries[role] = {"target_identity": target_identity, "repeat_count": len(runs),
                           "case_observation_count": len(rows), "cases": by_case,
                           "pooled_case_observations": grouped(rows),
                           "launches_declared": sum(r["execution"]["launches"] for r in runs),
                           "repeats": [{"run_id": r["run_id"], "run_digest": r["run_digest"],
                                        "target_root": r["target_snapshot"]["root"], "status": r["status"],
                                        "cases": [{"case_id": row["case_id"], "status": row["status"],
                                                   "metrics": row["metrics"]} for row in r["cases"]]} for r in runs]}
    def delta(old, new):
        out = {}
        for metric in metric_names:
            a, b = old["metrics"][metric], new["metrics"][metric]
            out[metric] = {"candidate_minus_baseline_mean": b["mean"] - a["mean"] if a["mean"] is not None and b["mean"] is not None else None,
                           "baseline_n": a["n"], "candidate_n": b["n"],
                           "baseline_unknown": a["unknown"], "candidate_unknown": b["unknown"],
                           "complete_observations": a["unknown"] == b["unknown"] == 0}
        return out
    deltas = None
    if "baseline" in summaries:
        a, b = summaries["baseline"], summaries["candidate"]
        deltas = {"cases": {cid: delta(a["cases"][cid], b["cases"][cid]) for cid in a["cases"]},
                  "pooled_case_observations": delta(a["pooled_case_observations"], b["pooled_case_observations"]),
                  "method": "Candidate mean minus baseline mean under matched case conditions; no automatic repeat pairing."}
    report = {"kind": "he-eval-aggregate", "schema_version": VERSION, "condition": frozen_condition,
              "roles": summaries, "deltas": deltas,
              "units": {"quality_pass": "fraction of valid pass/fail case observations", "duration_seconds": "seconds per case observation",
                        "tokens": "recorded tokens", "characters": "characters", "tool_calls": "tool calls", "cost_amount": currency},
              "limits": ["Descriptive observations only; no causal, significance or general superiority claim.",
                         "Pooled means weight each observed case equally; they are not whole-run wall-clock totals.",
                         "Unknown metrics are excluded from numerical summaries and counted explicitly, never replaced with zero.",
                         "Sample standard deviation is undefined for fewer than two known observations.",
                         "Imported execution, metric and assistance claims remain unauthenticated."]}
    if output:
        roots = {r["target_snapshot"]["root"] for r in all_runs} | {r["artifacts_root"] for r in all_runs}
        save_new(output, report, tuple(safe_path(p) for p in roots))
    return report


def _reviewed(run: dict, review_path: Any, manifest_path: Any) -> dict:
    # Review's own route is lazy: core evaluation and legacy HE do not need it.
    from .review import validate_feedback
    review, manifest = read_record(review_path), read_record(manifest_path)
    validate_feedback(review, manifest)
    wanted = set()
    for row in run["cases"]:
        if row["required"]:
            require(row["artifacts"], "required case lacks reviewable artifact")
            for a in row["artifacts"]:
                wanted.add((row["case_id"], row["case_digest"], run["run_id"], run["run_digest"],
                            run["target_snapshot"]["digest"], "current", a["path"], a["sha256"]))
    accepted = set()
    for row in review["reviews"].values():
        i = row["identity"]
        if row["reviewed"] is True and row["accepted"] is True and text(row["reviewer"]) and text(row["evidence"]):
            accepted.add(tuple(i[k] for k in ("case_id", "case_digest", "run_id", "run_digest", "target_digest", "role", "artifact_path", "artifact_sha256")))
    require(wanted and wanted <= accepted, "every required current artifact needs explicit bound acceptance")
    return {"feedback_path": str(safe_path(review_path)), "feedback_digest": digest(review),
            "manifest_path": str(safe_path(manifest_path)), "manifest_digest": digest(manifest)}


def _legacy_plan(run_id: str, source: Path, operations: list, platform: str) -> dict:
    return {"schema_version": 1, "run_id": run_id, "platform": platform, "allowed_roots": [str(source)],
            "approval_groups": ["eval-promotion"],
            "outcome": {"primary_metric": "reviewed candidate applied", "before_state": "frozen source",
                        "target_state": "exact reviewed payload", "unresolved_before": len(operations),
                        "unresolved_target": 0, "expected_primary_outputs": max(1, len(operations))},
            "resource_budget": {"max_task_launches": 0, "max_support_artifacts": 0,
                                "max_verification_passes": 1, "max_low_yield_waves": 1,
                                "high_cost_approved": False, "cost_warning": None},
            "support_artifacts": [], "operations": operations}


def _plan_probe(plan: dict) -> dict:
    # The stored plan has no payload, so legacy apply refuses it; validate scope with an empty stand-in.
    probe = copy.deepcopy(plan)
    for op in probe["operations"]:
        op["content"] = ""
    return probe


def _promotion_body(source: Any, candidate: Any, suite_path: Any, run_path: Any, stage_path: Any,
                    review_path: Any, review_manifest: Any, platform: Any) -> tuple:
    """Derive the whole promotion from bound evidence. Apply rebuilds it, so no part can be substituted."""
    from .plans import validate_plan
    import base64
    src, dst = safe_path(source, True), safe_path(candidate, True)
    disjoint(src, dst)
    suite = read_record(suite_path)
    validate_suite(suite)
    run = load_run(run_path, True)
    require(run["suite_digest"] == digest(suite), "run does not qualify this suite")
    require(run["status"] == "pass" and all(r["status"] == "pass" for r in run["cases"] if r["required"]), "promotion requires all required cases passing")
    require(run["execution"]["origin"] != "fixture", "fixture-only evidence cannot authorize promotion")
    require(run["suite"]["holdout"]["status"] != "used-for-selection", "contaminated final test needs fresh qualification")
    stage_record = read_record(stage_path)
    header(stage_record, "he-stage")
    require(stage_record["source"]["root"] == str(src) and stage_record["candidate"]["root"] == str(dst), "stage roots mismatch")
    before = snapshot(src, suite["target_paths"])
    after = snapshot(dst, suite["target_paths"])
    declared = set(suite["target_paths"])
    require(all(e["path"] in declared for e in snapshot(dst)["entries"] if e["type"] == "file"), "candidate contains undeclared files; freeze the complete dependency set before qualification")
    require(before["digest"] == stage_record["source"]["digest"], "source changed since staging")
    require(run["target_snapshot"]["root"] == str(dst) and after["digest"] == run["target_snapshot"]["digest"], "candidate differs from reviewed run")
    reviewed = _reviewed(run, review_path, review_manifest)
    old = {e["path"]: e for e in before["entries"]}
    operations, payloads = [], []
    for e in after["entries"]:
        prior = old[e["path"]]
        require(e["type"] != "absent" or prior["type"] == "absent", "deletion requires a separate recovery contract")
        if e["type"] == "absent" or e == prior:
            continue
        require(prior["type"] == "absent" or e["mode"] == prior["mode"], "mode changes to existing files require separate approved operations")
        raw = (dst / e["path"]).read_bytes()
        require(len(raw) <= MAX_ARTIFACT and hashlib.sha256(raw).hexdigest() == e["sha256"], "payload drift/size limit")
        op = {"id": "file-%d" % (len(operations) + 1), "action": "create" if prior["type"] == "absent" else "update",
              "target": str(src / e["path"]), "approval_group": "eval-promotion",
              "reason": "Apply exact reviewed candidate " + run["run_id"]}
        if prior["type"] == "file":
            op["expected_sha256"] = prior["sha256"]
        operations.append(op)
        payloads.append({"id": op["id"], "path": e["path"], "sha256": e["sha256"], "mode": e["mode"],
                         "base64": base64.b64encode(raw).decode("ascii")})
    require(operations, "no file changes to promote")
    require(platform in ("codex", "claude-code", "cowork"), "explicit target platform required")
    plan = _legacy_plan(identifier(run["run_id"]), src, operations, platform)
    errors = validate_plan(_plan_probe(plan))
    require(not errors, "internal operation plan invalid: " + "; ".join(errors))
    body = {"kind": "he-eval-promotion", "schema_version": VERSION,
            "source": before, "candidate": after, "suite_digest": digest(suite),
            "suite_path": str(safe_path(suite_path)), "run_path": str(safe_path(run_path)),
            "run_digest": run["run_digest"], "stage_path": str(safe_path(stage_path)),
            "stage_digest": digest(stage_record), "review": reviewed, "operation_plan": plan,
            "payloads": payloads, "status": "prepared-not-approved"}
    return run, body


def prepare(source: Any, candidate: Any, suite_path: Any, run_path: Any, stage_path: Any,
            review_path: Any, review_manifest: Any, output: Any, platform: str) -> dict:
    from .plans import validate_plan
    run, body = _promotion_body(source, candidate, suite_path, run_path, stage_path, review_path, review_manifest, platform)
    promotion = seal(body, "promotion_digest")
    # Neither the envelope nor its nested plan is a runnable legacy plan: no weaker fallback route.
    require(bool(validate_plan(promotion)) and bool(validate_plan(promotion["operation_plan"])),
            "promotion must never be accepted as a legacy plan")
    save_new(output, promotion, (safe_path(source), safe_path(candidate), safe_path(run["artifacts_root"])))
    return promotion


def apply_promotion(promotion_path: Any, approval_path: Any, receipt: Any, backup_dir: Any, manifest: Any) -> dict:
    import base64
    from .plans import apply_plan, validate_plan
    envelope = read_record(promotion_path)
    header(envelope, "he-eval-promotion")
    check_seal(envelope, "promotion_digest")
    approval = read_record(approval_path)
    header(approval, "he-eval-approval")
    require(approval.get("status") == "approved" and approval.get("authority") == "user"
            and text(approval.get("evidence")) and approval.get("promotion_digest") == envelope["promotion_digest"],
            "exact promotion needs explicit user approval evidence")
    require(all(isinstance(envelope.get(k), dict) for k in ("source", "candidate", "review", "operation_plan")), "promotion envelope incomplete")
    # Rebuild from the bound run, stage, suite, review and current trees. A resealed envelope
    # cannot swap the candidate, payloads, roots or suite away from the reviewed passing run.
    run, rebuilt = _promotion_body(envelope["source"].get("root"), envelope["candidate"].get("root"),
                                   envelope.get("suite_path"), envelope.get("run_path"), envelope.get("stage_path"),
                                   envelope["review"].get("feedback_path"), envelope["review"].get("manifest_path"),
                                   envelope["operation_plan"].get("platform"))
    require(seal(rebuilt, "promotion_digest") == envelope, "promotion does not match its bound reviewed evidence; prepare again")
    src, dst = safe_path(rebuilt["source"]["root"], True), safe_path(rebuilt["candidate"]["root"], True)
    target_paths = run["suite"]["target_paths"]
    reviewed = rebuilt["review"]
    plan = copy.deepcopy(rebuilt["operation_plan"])
    targets = [op["target"] for op in plan["operations"]]
    require(isinstance(approval.get("approved_paths"), list) and sorted(approval["approved_paths"]) == sorted(targets), "approval target set differs")
    controls = [safe_path(x) for x in (receipt, backup_dir, manifest)]
    disjoint(*controls)
    for p in controls:
        for root in (src, dst, safe_path(run["artifacts_root"])):
            disjoint(p, root)
        require(not p.exists(), "apply output already exists: " + str(p))
    for control in controls:
        for evidence in (promotion_path, approval_path, envelope["run_path"], envelope["suite_path"], envelope["stage_path"], reviewed["feedback_path"], reviewed["manifest_path"]):
            disjoint(control, safe_path(evidence, True))
    # Durable payloads live in the new backup area. They never replace a target directory.
    payload_root = controls[1] / "reviewed-payloads"
    payload_root.mkdir(parents=True)
    for op, payload in zip(plan["operations"], rebuilt["payloads"]):
        require(op["id"] == payload["id"] and op["target"] == str(src / relative(payload["path"])), "payload target mismatch")
        try:
            raw = base64.b64decode(payload["base64"], validate=True)
        except (ValueError, TypeError) as exc:
            raise HectlError("invalid payload encoding: " + str(exc))
        require(len(raw) <= MAX_ARTIFACT and hashlib.sha256(raw).hexdigest() == payload["sha256"], "payload digest mismatch")
        frozen_file = payload_root / op["id"]
        fd = os.open(str(frozen_file), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "wb") as h:
            h.write(raw)
            h.flush()
            os.fsync(h.fileno())
        op["source"] = str(frozen_file)
    require(not validate_plan(plan), "promotion contains an invalid legacy operation plan")
    # Recheck after materializing inputs and immediately before legacy transactional writes.
    require(snapshot(src, target_paths)["digest"] == envelope["source"]["digest"], "source drift before writes")
    require(snapshot(dst, target_paths)["digest"] == envelope["candidate"]["digest"], "candidate drift before writes")
    require(load_run(envelope["run_path"], True)["run_digest"] == envelope["run_digest"], "run changed before writes")
    require(_reviewed(run, reviewed["feedback_path"], reviewed["manifest_path"]) == reviewed, "review changed before writes")
    require(read_record(approval_path) == approval, "approval changed before writes")
    result = apply_plan(plan, "apply", {"eval-promotion"}, controls[0], controls[1], controls[2])
    for op, payload in zip(plan["operations"], rebuilt["payloads"]):
        if op["action"] == "create":
            os.chmod(op["target"], payload["mode"])
    require(snapshot(src, target_paths)["digest"] == envelope["candidate"]["digest"], "post-apply content/mode mismatch; use rollback manifest")
    return dict(result, promotion_digest=envelope["promotion_digest"],
                note="Approval evidence is declared; this tool does not authenticate consent or enforce OS isolation.")


def cycle_init(state_path: Any, suite_path: Any, source: Any) -> dict:
    suite = read_record(suite_path)
    validate_suite(suite)
    snap = snapshot(source, suite["target_paths"])
    state = {"kind": "he-eval-cycle", "schema_version": VERSION, "suite_path": str(safe_path(suite_path)),
             "suite_digest": digest(suite), "source": snap, "limits": suite["limits"], "state": "running",
             "runs": [], "launches": 0, "repair_cycles": 0, "low_yield_cycles": 0, "failure_signatures": []}
    state = seal(state, "state_digest")
    save_new(state_path, state, (safe_path(source),))
    return state


def _cycle_step(state_path: Any, run_path: Any, repair: bool = False) -> dict:
    path = safe_path(state_path, True)
    state = read_record(path)
    original_digest = state.get("state_digest")
    header(state, "he-eval-cycle")
    check_seal(state, "state_digest")
    require(state["state"] == "running", "cycle is terminal; preserve it and explicitly replan")
    require(digest(read_record(state["suite_path"])) == state["suite_digest"], "cycle suite drift")
    run = load_run(run_path)
    require(run["suite_digest"] == state["suite_digest"], "cycle run suite mismatch")
    require(run["run_id"] not in [r["run_id"] for r in state["runs"]], "run already consumed; no budget refund/reuse")
    rows = [r for r in run["cases"] if r["required"]]
    unresolved = sum(r["status"] != "pass" for r in rows)
    signature = digest([(r["case_id"], r["status"]) for r in rows if r["status"] != "pass"])
    previous = state["runs"][-1]["unresolved"] if state["runs"] else None
    state["launches"] += run["execution"]["launches"]
    state["repair_cycles"] += int(repair)
    state["low_yield_cycles"] += int(previous is not None and unresolved >= previous)
    repeated = unresolved > 0 and signature in state["failure_signatures"]
    state["failure_signatures"].append(signature)
    state["runs"].append({"run_id": run["run_id"], "run_digest": run["run_digest"], "unresolved": unresolved,
                          "status": run["status"], "origin": run["execution"]["origin"]})
    limits = state["limits"]
    if not run["execution"]["adapter_available"]:
        state["state"], state["stop_reason"] = "blocked", "execution adapter unavailable"
    elif any((len(state["runs"]) > limits["max_runs"], state["launches"] > limits["max_launches"],
              state["repair_cycles"] > limits["max_repair_cycles"])):
        state["state"], state["stop_reason"] = "exhausted", "budget exceeded; consumed work remains counted"
    elif unresolved == 0:
        state["state"], state["stop_reason"] = "ready-for-review", "passing observations; not release acceptance"
    elif repeated or state["low_yield_cycles"] >= limits["max_low_yield_cycles"]:
        state["state"], state["stop_reason"] = "blocked", "repeated failure or low-yield cycle; replan"
    elif len(state["runs"]) >= limits["max_runs"] or state["launches"] >= limits["max_launches"] or state["repair_cycles"] >= limits["max_repair_cycles"]:
        state["state"], state["stop_reason"] = "exhausted", "finite budget reached"
    state = seal(state, "state_digest")
    # Refuse concurrent changes instead of overwriting another controller's state.
    require(read_record(path).get("state_digest") == original_digest, "state changed concurrently")
    write_json(path, state)
    return state


def cycle_step(state_path: Any, run_path: Any, repair: bool = False) -> dict:
    path = safe_path(state_path, True)
    lock = safe_path(path.with_name(path.name + ".lock"))
    try:
        fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise HectlError("cycle is locked; verify the owning process before recovering an interrupted lock")
    try:
        with os.fdopen(fd, "w") as handle:
            handle.write(str(os.getpid()))
        return _cycle_step(path, run_path, repair)
    finally:
        lock.unlink()


def cycle_stop(state_path: Any, status: str, reason: str) -> dict:
    require(status in ("cancelled", "blocked", "failed") and text(reason), "stop needs cancelled/blocked/failed and an explicit reason")
    path = safe_path(state_path, True)
    lock = safe_path(path.with_name(path.name + ".lock"))
    try:
        fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise HectlError("cycle is locked; verify the owning process before recovery")
    try:
        os.close(fd)
        state = read_record(path)
        header(state, "he-eval-cycle")
        check_seal(state, "state_digest")
        require(state["state"] == "running", "terminal cycle cannot be renamed")
        state.update(state=status, stop_reason=reason)
        state = seal(state, "state_digest")
        write_json(path, state)
        return state
    finally:
        lock.unlink()


def review_packet(run_path: Any, output: Any, prior_path: Any = None) -> dict:
    from .review import validate_manifest
    current = load_run(run_path, True)
    runs = [(current, "current")]
    if prior_path:
        prior = load_run(prior_path)
        for case in prior["cases"]:
            for a in case["artifacts"]:
                artifact(safe_path(prior["artifacts_root"], True), a)
        require(prior["artifacts_root"] == current["artifacts_root"], "combined packet needs an explicitly prepared common artifacts root; do not silently copy/export unrelated evidence")
        runs.append((prior, "prior"))
    manifest = {"schema": "he-review-v1", "mode": "artifacts", "title": "Review actual evaluation artifacts",
                "runs": [], "notes": "Declared results; review does not authenticate execution or authorize source application."}
    for run, role in runs:
        for case in run["cases"]:
            manifest["runs"].append({"run_id": run["run_id"], "run_digest": run["run_digest"],
                                    "case_id": case["case_id"], "case_digest": case["case_digest"],
                                    "target_digest": run["target_snapshot"]["digest"], "role": role,
                                    "artifacts": [{"path": a["path"], "sha256": a["sha256"]} for a in case["artifacts"]],
                                    "grading": case["checks"], "metrics": case["metrics"], "notes": case["notes"], "status": case["status"]})
    validate_manifest(manifest)
    save_new(output, manifest, (safe_path(current["target_snapshot"]["root"]), safe_path(current["artifacts_root"])))
    return {"manifest": str(safe_path(output)), "evidence_root": current["artifacts_root"], "packet_digest": digest(manifest), "status": "prepared-not-reviewed"}


def pin_baseline(run_path: Any, role: str, output: Any, review_path: Any = None, review_manifest: Any = None) -> dict:
    require(role in ("reference", "release"), "baseline role must be reference or release")
    run = load_run(run_path, role == "release")
    reviewed = None
    if role == "release":
        require(run["status"] == "pass" and run["execution"]["origin"] != "fixture", "release baseline needs current passing non-fixture evidence")
        require(review_path and review_manifest, "release baseline needs exact human review")
        require(run["suite"]["holdout"]["status"] != "used-for-selection", "used-for-selection holdout cannot qualify release")
        reviewed = _reviewed(run, review_path, review_manifest)
    result = seal({"kind": "he-eval-baseline", "schema_version": VERSION, "role": role,
                   "run_path": str(safe_path(run_path)), "run_digest": run["run_digest"], "run_status": run["status"],
                   "suite_digest": run["suite_digest"], "target_digest": run["target_snapshot"]["digest"],
                   "review": reviewed, "limits": "Pinned evidence, not installed proof or authenticated consent."}, "baseline_digest")
    save_new(output, result, (safe_path(run["target_snapshot"]["root"]), safe_path(run["artifacts_root"])))
    return result


def dispatch(argv=None) -> int:
    p = argparse.ArgumentParser(prog="hectl eval", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="command", required=True)
    q = sub.add_parser("snapshot"); q.add_argument("--target", required=True); q.add_argument("--path", action="append"); q.add_argument("--output", required=True)
    q = sub.add_parser("suite-check"); q.add_argument("suite")
    q = sub.add_parser("stage")
    for name in ("target", "output", "manifest"): q.add_argument("--" + name, required=True)
    q.add_argument("--path", action="append", required=True)
    q = sub.add_parser("record")
    for name in ("suite", "target", "results", "artifacts", "output"): q.add_argument("--" + name, required=True)
    q = sub.add_parser("compare"); q.add_argument("--baseline", required=True); q.add_argument("--candidate", required=True)
    q = sub.add_parser("aggregate"); q.add_argument("--candidate", action="append", required=True); q.add_argument("--baseline", action="append"); q.add_argument("--output")
    q = sub.add_parser("review-packet"); q.add_argument("--run", required=True); q.add_argument("--prior"); q.add_argument("--output", required=True)
    q = sub.add_parser("pin"); q.add_argument("--run", required=True); q.add_argument("--role", choices=("reference", "release"), required=True); q.add_argument("--output", required=True); q.add_argument("--review"); q.add_argument("--review-manifest")
    q = sub.add_parser("prepare")
    for name in ("source", "candidate", "suite", "run", "stage", "review", "review-manifest", "output", "platform"): q.add_argument("--" + name, required=True)
    q = sub.add_parser("apply")
    for name in ("promotion", "approval", "receipt", "backup-dir", "manifest"): q.add_argument("--" + name, required=True)
    q = sub.add_parser("cycle"); ss = q.add_subparsers(dest="cycle_command", required=True)
    z = ss.add_parser("init")
    for name in ("state", "suite", "source"): z.add_argument("--" + name, required=True)
    z = ss.add_parser("step"); z.add_argument("--state", required=True); z.add_argument("--run", required=True); z.add_argument("--repair", action="store_true")
    z = ss.add_parser("stop"); z.add_argument("--state", required=True); z.add_argument("--as", dest="stop_as", choices=("cancelled", "blocked", "failed"), required=True); z.add_argument("--reason", required=True)
    z = ss.add_parser("status"); z.add_argument("--state", required=True)
    args = p.parse_args(argv)
    try:
        if args.command == "snapshot":
            result = snapshot(args.target, args.path); save_new(args.output, result, (safe_path(args.target),))
        elif args.command == "suite-check": result = validate_suite(read_record(args.suite))
        elif args.command == "stage": result = stage(args.target, args.output, args.path, args.manifest)
        elif args.command == "record": result = record_run(args.suite, args.target, args.results, args.artifacts, args.output)
        elif args.command == "compare": result = compare(args.baseline, args.candidate)
        elif args.command == "aggregate": result = aggregate(args.candidate, args.baseline, args.output)
        elif args.command == "review-packet": result = review_packet(args.run, args.output, args.prior)
        elif args.command == "pin": result = pin_baseline(args.run, args.role, args.output, args.review, args.review_manifest)
        elif args.command == "prepare": result = prepare(args.source, args.candidate, args.suite, args.run, args.stage, args.review, args.review_manifest, args.output, args.platform)
        elif args.command == "apply": result = apply_promotion(args.promotion, args.approval, args.receipt, args.backup_dir, args.manifest)
        elif args.cycle_command == "init": result = cycle_init(args.state, args.suite, args.source)
        elif args.cycle_command == "step": result = cycle_step(args.state, args.run, args.repair)
        elif args.cycle_command == "stop": result = cycle_stop(args.state, args.stop_as, args.reason)
        else:
            result = read_record(args.state); header(result, "he-eval-cycle"); check_seal(result, "state_digest")
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0
    except (HectlError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(dispatch())
