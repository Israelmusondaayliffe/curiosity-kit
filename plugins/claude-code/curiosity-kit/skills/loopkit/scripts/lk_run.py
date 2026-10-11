"""Bounded command capture and artifact-bound verification; no model/provider calls."""
import os
import shutil
import signal
import subprocess
import time
import uuid
from pathlib import Path
from lk_state import Fault, need, nonempty, scoped, artifacts, file_hash, digest, edit, load, clean_path, within

TERMINAL = {"completed", "exhausted", "failed", "cancelled"}


def unit(s):
    """Current unit: an explicitly reopened committed unit first, otherwise the next serial unit."""
    if s.get("reopened"):
        return lookup(s, "units", s["reopened"][0])
    need(s["unit_index"] < len(s["contract"]["units"]), "no-current-unit", "All units already committed")
    return s["contract"]["units"][s["unit_index"]]


def committed(s, unit_id):
    ids = [u["id"] for u in s["contract"]["units"]]
    need(unit_id in ids, "unit-unknown", "No such unit: " + str(unit_id))
    need(ids.index(unit_id) < s["unit_index"], "unit-not-committed", "Only an already committed unit can be rechecked or reopened")
    return lookup(s, "units", unit_id)


def remaining(s):
    return s["contract"]["limits"]["max_seconds"] - (time.time() - (s["started_epoch"] or time.time()))


def available(s):
    need(s["status"] not in TERMINAL, "terminal", "Run is terminal")
    need(s["status"] not in {"paused", "waiting_input", "blocked"}, "resume-required", "Resolve the prerequisite and resume explicitly")
    need(s["pending"] is None, "uncertain-action", "Reconcile the pending attempt before any execution")


def bound(s, spec):
    current = artifacts(s)
    return {name: current[name] for name in spec.get("artifacts", s["contract"]["artifacts"])}


def lookup(s, kind, name):
    return next(x for x in s["contract"][kind] if x["id"] == name)


def invocation(s, spec):
    cwd = scoped(s, spec["cwd"])
    need(cwd.is_dir(), "cwd-missing", "Invocation cwd is unavailable")
    argv = list(spec["argv"])
    exe = argv[0]
    if "/" in exe:
        exe = str((Path(exe) if Path(exe).is_absolute() else cwd / exe).resolve())
    else:
        exe = shutil.which(exe)
    need(exe and Path(exe).is_file() and os.access(exe, os.X_OK), "tool-missing", "Executable unavailable")
    argv[0] = exe
    # Explicit inputs bind check scripts/data as well as argv and executable.
    inputs = {name: file_hash(scoped(s, name)) for name in spec.get("inputs", [])}
    return {"argv": argv, "cwd": str(cwd), "executable_sha256": file_hash(exe),
            "inputs": inputs, "spec_sha256": digest(spec)}


def capture(root, token, call, timeout, ceiling):
    paths = [root / "evidence" / (token + suffix) for suffix in (".stdout", ".stderr")]
    handles = [open(p, "xb") for p in paths]
    for p in paths:
        os.chmod(p, 0o600)
    started = time.time()
    reason, code, pid = None, None, None
    try:
        proc = subprocess.Popen(call["argv"], cwd=call["cwd"], stdin=subprocess.DEVNULL,
                                stdout=handles[0], stderr=handles[1], shell=False, start_new_session=True)
        pid = proc.pid
        while proc.poll() is None:
            if time.time() - started >= timeout:
                reason = "timeout"
            elif sum(p.stat().st_size for p in paths) > ceiling:
                reason = "output-limit"
            if reason:
                os.killpg(proc.pid, signal.SIGKILL)
                break
            time.sleep(0.02)
        code = proc.wait()
        # A command may leave children holding capture files. Terminate only its own group.
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    except OSError as exc:
        reason = "spawn-error:" + type(exc).__name__
    finally:
        for handle in handles:
            handle.close()
    if sum(p.stat().st_size for p in paths) > ceiling:
        reason = "output-limit"
    return {"started_epoch": started, "finished_epoch": time.time(), "pid": pid,
            "exit_code": code, "failure": reason,
            "output": [{"path": str(p.relative_to(root)), "sha256": file_hash(p), "bytes": p.stat().st_size}
                       for p in paths]}


def execute(run, generation, action, execute_allowed, unit_id=None):
    """run-unit / check on the current unit; with unit_id, a check-only recheck of a committed unit (never its actions)."""
    need(execute_allowed, "execution-opt-in", "Review exact contract commands and authority; supply --execute to run")
    need(not (action and unit_id), "recheck-only", "A committed unit is rechecked with check --unit; its actions are never replayed")
    def begin(s, root):
        available(s)
        target = committed(s, unit_id) if unit_id else unit(s)
        if unit_id:
            # A recheck only re-reads evidence: it spends wall-clock time, never a work iteration or no-progress count.
            need(remaining(s) > 0, "budget-exhausted", "Run time budget exhausted; a recheck needs remaining time")
            s["rechecks"] = s.get("rechecks", 0) + 1
        elif (remaining(s) <= 0 or s["iterations"] >= s["contract"]["limits"]["max_iterations"]
                or s["no_progress"] >= s["contract"]["limits"]["no_progress_limit"]):
            s["status"] = "exhausted"
            s["next_action"] = "Budget exhausted; report unfinished work"
            return False
        s["started_epoch"] = s["started_epoch"] or time.time()
        s["iterations"] += 0 if unit_id else 1
        s["status"] = "running"
        s["pending"] = {"batch": uuid.uuid4().hex, "unit": target["id"], "kind": "run" if action else ("recheck" if unit_id else "check"),
                        "attempt": None, "started_epoch": time.time()}
        return True
    s, began = edit(run, generation, "iteration-start", begin)
    if not began:
        return s
    u = lookup(s, "units", s["pending"]["unit"])
    jobs = [("actions", x) for x in u["actions"]] if action else []
    jobs += [("checks", x) for x in u["checks"]]
    batch = s["pending"]["batch"]
    for kind, name in jobs:
        spec = lookup(s, kind, name)
        call = invocation(s, spec)
        token = uuid.uuid4().hex
        def intent(v, root):
            need(v["pending"] and v["pending"]["batch"] == batch, "attempt-changed", "Attempt changed")
            need(remaining(v) > 0, "budget-exhausted", "Run time budget exhausted")
            v["pending"]["attempt"] = {"id": token, "kind": kind, "name": name,
                                        "invocation": call, "before": artifacts(v)}
        s, _ = edit(run, s["generation"], "command-intent", intent)
        before = s["pending"]["attempt"]["before"]
        observed = capture(clean_path(run), token, call, min(spec["timeout"], remaining(s)),
                           s["contract"]["limits"]["max_output_bytes"])
        after = artifacts(s)
        result = {"id": token, "batch": batch, "unit": u["id"], "kind": kind, "name": name,
                  "contract_sha256": s["contract_sha256"], "invocation": call, "before": before,
                  "after": bound(s, spec), **observed}
        # Machine pass is derived from captured process output, never from a supplied boolean.
        result["passed"] = (observed["exit_code"] == 0 and observed["failure"] is None
                            and (kind != "checks" or (before == after and all(x is not None for x in result["after"].values()))))
        if kind == "checks" and before != after:
            result["failure"] = "check-mutated-artifact"
        def record(v, root):
            need(v["pending"] and v["pending"]["attempt"] and v["pending"]["attempt"]["id"] == token,
                 "attempt-changed", "Pending identity changed; result not committed")
            v["results"].append(result)
            v["pending"]["attempt"] = None
        s, _ = edit(run, s["generation"], "command-result", record)
        if kind == "actions" and not result["passed"]:
            break
    def end(v, root):
        v["pending"] = None
        current = [r for r in v["results"] if r["batch"] == batch and r["kind"] == "checks" and r["passed"]]
        passed = sorted(r["name"] for r in current)
        v["last_artifacts"] = artifacts(v)
        if unit_id:  # a recheck refreshes evidence only; it does not move the current unit's progress accounting
            ok = set(u["checks"]) <= set(passed)
            v["next_action"] = ("Committed unit " + u["id"] + " rechecked: " + ("current evidence passes" if ok else
                                "checks fail; reopen it with a reason to redo it"))
            v["status"] = "running"
            return
        progress = bool(set(passed) - set(v["progress_checks"]))
        v["no_progress"] = 0 if progress else v["no_progress"] + 1
        v["progress_checks"] = passed
        v["last_artifacts"] = artifacts(v)
        v["next_action"] = "Inspect captured checks, satisfy judgments, and finish the unit; otherwise diagnose"
        v["status"] = "running"
        # Budget exhaustion blocks another attempt, but a just-verified final unit may still be committed.
        v["budget_reached"] = (v["iterations"] >= v["contract"]["limits"]["max_iterations"]
                               or v["no_progress"] >= v["contract"]["limits"]["no_progress_limit"]
                               or remaining(v) <= 0)
        if v["budget_reached"] and not set(u["checks"]) <= set(passed):
            v["status"] = "exhausted"
            v["next_action"] = "Budget exhausted with required checks unfinished"
    s, _ = edit(run, s["generation"], "iteration-end", end)
    return s


def result_fresh(s, root, r):
    spec = lookup(s, r["kind"], r["name"])
    need(r["contract_sha256"] == s["contract_sha256"] and r["after"] == bound(s, spec),
         "stale-evidence", "Artifacts or contract differ from captured check")
    need(r["invocation"] == invocation(s, spec), "check-changed", "Command, executable or declared inputs changed")
    for item in r["output"]:
        p = clean_path(root / item["path"])
        need(within(p, root / "evidence") and p.is_file() and file_hash(p) == item["sha256"],
             "capture-integrity", "Captured output is missing or changed")


def check_unit(s, root, u):
    for check in u["checks"]:
        matches = [r for r in s["results"] if r["kind"] == "checks" and r["name"] == check and r["unit"] == u["id"]]
        need(matches, "missing-check", "No captured check: " + check)
        r = matches[-1]
        need(r["passed"] and r["exit_code"] == 0 and r["failure"] is None,
             "check-failed", "Latest captured check failed: " + check)
        result_fresh(s, root, r)
    for name in u["judgments"]:
        matches = [j for j in s["reviews"] if j["criterion_id"] == name and j["unit"] == u["id"]]
        need(matches and matches[-1]["verdict"] == "pass", "judgment-missing-or-failed", "Judgment not satisfied: " + name)
        j = matches[-1]
        need(j["artifacts"] == judged(s, name) and j["contract_sha256"] == s["contract_sha256"],
             "stale-judgment", "Judged artifacts changed since the review; record a fresh review with review --unit")
        p = scoped(s, j["evidence_path"])
        need(p.is_file() and file_hash(p) == j["evidence_sha256"], "review-integrity", "Review evidence changed")
        spec = lookup(s, "judgments", name)
        need(not spec["independent"] or j["independent"] is True,
             "review-unavailable", "Required independent review unavailable")


def judged(s, name):
    current = artifacts(s)
    return {n: current[n] for n in lookup(s, "judgments", name).get("artifacts", s["contract"]["artifacts"])}


def finish(run, generation):
    def op(s, root):
        available(s)
        u = unit(s)
        check_unit(s, root, u)
        redo = bool(s.get("reopened")) and s["reopened"][0] == u["id"]
        s["verified_units"].append({"id": u["id"], "at": time.time(), "artifacts": artifacts(s),
                                    "generation": s["generation"] + 1, "reverified": redo})
        if redo:
            s["reopened"].pop(0)  # later committed units keep their own evidence; final completion rechecks them all
        else:
            s["unit_index"] += 1
        s["no_progress"] = 0
        s["progress_checks"] = []
        if s["unit_index"] == len(s["contract"]["units"]) and not s.get("reopened"):
            # All essential criteria must remain satisfied at final delivery.
            for prior in s["contract"]["units"]:
                check_unit(s, root, prior)
            s["status"] = "completed"
            s["next_action"] = "Return verified artifacts and material limits"
        elif s.get("budget_reached"):
            s["status"] = "exhausted"
            s["next_action"] = "Report verified units and unfinished remainder"
        else:
            s["next_action"] = "Execute next serial unit"
    return edit(run, generation, "unit-verified", op)[0]


def review(run, generation, note, unit_id=None):
    """Record a judgment for the current unit, or refresh one for a committed unit (truthful re-review of current files)."""
    def op(s, root):
        available(s)
        u = committed(s, unit_id) if unit_id else unit(s)
        need(isinstance(note, dict) and note.get("criterion_id") in u["judgments"], "review-invalid", "Unknown judgment criterion")
        need(note.get("verdict") in ("pass", "fail", "unavailable") and type(note.get("independent")) is bool,
             "review-invalid", "Explicit verdict and independence required")
        for key in ("reviewer", "evidence_path", "reason"):
            need(nonempty(note.get(key)), "review-invalid", "Missing review " + key)
        p = scoped(s, note["evidence_path"])
        need(p.is_file(), "review-missing", "Actual review artifact required")
        s["reviews"].append({**note, "unit": u["id"], "contract_sha256": s["contract_sha256"],
                             "artifacts": judged(s, note["criterion_id"]), "evidence_sha256": file_hash(p), "at": time.time()})
    return edit(run, generation, "judgment-recorded", op)[0]


def reopen(run, generation, unit_id, reason):
    """Return one committed unit to work because its evidence is stale or failing. Never for terminal runs, never with
    pending work, never when its evidence is still valid; other verified units are untouched."""
    need(nonempty(reason), "reason-required", "Name the observed change that invalidated the unit")
    def op(s, root):
        available(s)
        u = committed(s, unit_id)
        need(unit_id not in s["reopened"], "already-reopened", "Unit is already reopened")
        try:
            check_unit(s, root, u)
        except Fault as exc:
            s["reopened"].append(unit_id)
            s["events"].append({"event": "reopen-cause", "unit": unit_id, "cause": exc.code, "detail": str(exc), "reason": reason})
            s["status"] = "running"
            s["next_action"] = "Redo reopened unit " + unit_id + " with run-unit, verify, then finish it"
            return
        raise Fault("evidence-current", "Unit " + unit_id + " still has current passing evidence; nothing to reopen")
    return edit(run, generation, "unit-reopened", op)[0]


def pause(run, generation, status, reason):
    need(status in {"paused", "blocked", "waiting_input", "cancelled", "failed", "exhausted"}, "status-invalid", "Invalid stop")
    need(nonempty(reason), "reason-required", "Name the actual reason")
    def op(s, root):
        need(s["status"] not in TERMINAL, "terminal", "Terminal state cannot be silently reopened")
        need(s["pending"] is None, "uncertain-action", "Reconcile in-flight work before a clean stop")
        s["status"], s["next_action"] = status, reason
    return edit(run, generation, "stopped", op)[0]


def resume(run, generation, reason, acknowledge_drift=False):
    """With acknowledge_drift, an inspected artifact change is recorded and becomes the drift baseline only. Captured
    results and reviews keep their original hashes, so affected units stay stale until rechecked or reopened."""
    need(nonempty(reason), "reason-required", "State which prerequisite cleared")
    def op(s, root):
        need(s["status"] not in TERMINAL, "terminal", "Terminal runs stay terminal")
        need(s["pending"] is None, "uncertain-action", "Inspect in-flight effects and explicitly reconcile first")
        current, next_step = artifacts(s), reason
        if acknowledge_drift:
            need(current != s["last_artifacts"], "no-drift", "No artifact drift to acknowledge; resume without the flag")
            stale = []
            for u in s["contract"]["units"][:s["unit_index"]]:
                try:
                    check_unit(s, root, u)
                except (Fault, OSError) as exc:
                    stale.append({"unit": u["id"], "cause": getattr(exc, "code", "evidence-unavailable")})
            s["events"].append({"event": "drift-acknowledged", "reason": reason, "previous": s["last_artifacts"], "current": current,
                                "changed": sorted(k for k in current if current[k] != s["last_artifacts"].get(k)),
                                "stale_committed_units": stale})
            s["last_artifacts"] = current
            if stale:
                ids = ", ".join(x["unit"] for x in stale)
                next_step = ("Drift acknowledged; committed units with stale evidence: " + ids +
                          ". Run check --unit ID --execute for each; reopen any that fail. Then continue")
        need(current == s["last_artifacts"], "workspace-drift",
             "Artifacts changed; inspect them, then resume --acknowledge-drift to record the change (evidence stays stale)")
        if remaining(s) <= 0 or s.get("budget_reached"):
            s["status"], s["next_action"] = "exhausted", "Budget remains exhausted after restart"
        else:
            s["status"], s["next_action"] = "running", next_step
    return edit(run, generation, "resumed", op)[0]


def reconcile(run, generation, note):
    def op(s, root):
        need(s["pending"] is not None, "no-pending-action", "There is no pending attempt")
        need(isinstance(note, dict) and note.get("batch") == s["pending"]["batch"], "reconcile-invalid", "Name exact pending batch")
        need(note.get("resolution") in {"observed-complete", "observed-not-applied", "unknown"}, "reconcile-invalid", "Invalid resolution")
        for key in ("reason", "evidence_path"):
            need(nonempty(note.get(key)), "reconcile-invalid", "Missing " + key)
        p = scoped(s, note["evidence_path"])
        need(p.is_file(), "reconcile-invalid", "Fresh inspection evidence required")
        need(note.get("process_stopped") is True, "process-unconfirmed", "Confirm the original executor and owned children are stopped")
        s["events"].append({"event": "reconciliation-evidence", "note": note,
                             "evidence_sha256": file_hash(p), "pending": s["pending"]})
        if note["resolution"] != "unknown":
            s["pending"] = None
        s["status"] = "blocked"
        s["last_artifacts"] = artifacts(s)
        s["next_action"] = "Recheck artifacts; resume explicitly. Reconciliation is not verification or permission to replay"
    return edit(run, generation, "reconciled", op)[0]
