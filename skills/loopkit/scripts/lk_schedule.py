"""Records host observations; never creates, activates or impersonates a scheduler."""
import time
from lk_state import need, nonempty, edit, artifacts, scoped, file_hash
from lk_run import check_unit


def prepare(run, generation, draft):
    def op(s, root):
        need(s["status"] == "completed", "manual-run-required", "A verified successful manual run is required")
        for u in s["contract"]["units"]:
            check_unit(s, root, u)
        need(s["schedule"] is None or s["schedule"]["status"] in {"prepared", "stopped"},
             "schedule-active", "Reconcile the existing host schedule before replacing its record")
        need(isinstance(draft, dict), "schedule-invalid", "Expected schedule object")
        for key in ("cadence", "timezone", "task_prompt", "no_op", "stop_condition", "evidence_return", "authority"):
            need(nonempty(draft.get(key)), "schedule-invalid", "Missing " + key)
        need(draft.get("host") == s["contract"]["host"], "schedule-host", "Schedule host differs from run")
        s["schedule"] = {"status": "prepared", "draft": draft, "manual_run_id": s["run_id"],
                         "manual_artifacts": artifacts(s), "host_id": None, "history": [], "prepared_at": time.time()}
        s["next_action"] = "Use the actual supported host scheduler only with scheduling authority; then record its response"
    return edit(run, generation, "schedule-prepared", op)[0]


def observe(run, generation, observation):
    def op(s, root):
        record = s["schedule"]
        need(record is not None, "schedule-missing", "Prepare the schedule first")
        need(isinstance(observation, dict), "schedule-invalid", "Expected actual host observation")
        event = observation.get("event")
        need(event in {"activated", "execution", "no-op", "paused", "stopped", "failed"}, "schedule-invalid", "Unknown event")
        for key in ("host_id", "surface", "evidence_path", "summary"):
            need(nonempty(observation.get(key)), "schedule-invalid", "Missing " + key)
        need(observation.get("host") == s["contract"]["host"], "schedule-host", "Wrong host")
        evidence = scoped(s, observation["evidence_path"])
        need(evidence.is_file(), "schedule-evidence", "Actual host response/execution artifact is required")
        if event == "activated":
            need(record["status"] in {"prepared", "paused"}, "schedule-transition", "Invalid activation transition")
            need(nonempty(observation.get("authorization_reference")), "schedule-authority", "Name the actual separate activation authority")
            need(record["manual_artifacts"] == artifacts(s), "manual-run-stale", "Manual-run artifacts changed; requalify before activation")
            need(record["host_id"] in (None, observation["host_id"]), "schedule-id", "Cannot silently switch schedule id")
            record["host_id"] = observation["host_id"]
            record["status"] = "active-unobserved"
        else:
            need(record["host_id"] == observation["host_id"], "schedule-id", "Observation must identify the activated schedule")
            need(record["status"] not in {"prepared", "stopped"}, "schedule-transition", "No active schedule to observe")
            if event in {"execution", "no-op"}:
                need(record["status"] in {"active-unobserved", "observed"}, "schedule-transition", "Schedule is not active")
                need(nonempty(observation.get("execution_id")), "schedule-evidence", "Actual scheduled execution id required")
                need(observation.get("result") in {"success", "no-op", "failed", "blocked"}, "schedule-evidence", "Explicit execution result required")
                need(event != "no-op" or observation["result"] == "no-op", "schedule-evidence", "No-op result mismatch")
                if observation["result"] in {"success", "no-op"}:
                    need(nonempty(observation.get("verification_evidence")), "schedule-evidence", "Result inspection evidence required")
                    check = scoped(s, observation["verification_evidence"])
                    need(check.is_file(), "schedule-evidence", "Result inspection artifact missing")
                    observation["verification_sha256"] = file_hash(check)
                    record["status"] = "observed"
                else:
                    record["status"] = "attention-required"
            elif event == "paused":
                record["status"] = "paused"
            elif event == "stopped":
                record["status"] = "stopped"
            else:
                record["status"] = "attention-required"
        record["history"].append({**observation, "evidence_sha256": file_hash(evidence), "recorded_at": time.time()})
        s["next_action"] = "Report schedule status exactly as observed: " + record["status"]
    return edit(run, generation, "schedule-observed", op)[0]
