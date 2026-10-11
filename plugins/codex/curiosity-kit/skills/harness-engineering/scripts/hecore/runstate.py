"""Durable state for a bounded harness run: caps, receipts, stop states, resume.

The run never gains authority beyond its approved plan. A step that changes nothing
counts as a low-yield wave; one such wave stops the run for re-planning.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from .common import HectlError, load_json, now_iso, sha256_file, write_json
from .plans import validate_plan

TERMINAL = {"waiting-input", "blocked", "exhausted", "failed", "cancelled", "completed"}


def _count(value, label: str, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise HectlError(f"{label} must be an integer of at least {minimum}")
    return value


def init(state_path: Path, run_id: str, objective: str, plan: Path, max_steps: int, max_launches: int,
         unresolved: Optional[int]) -> dict[str, Any]:
    if state_path.exists():
        raise HectlError(f"state already exists; resume it instead: {state_path}")
    if not plan.is_file():
        raise HectlError(f"approved plan not found: {plan}")
    plan_data = load_json(plan)
    errors = validate_plan(plan_data)
    if errors:
        raise HectlError("the run needs a valid approved plan: " + "; ".join(errors[:5]))
    if not objective.strip() or not run_id.strip():
        raise HectlError("run id and objective are required")
    _count(max_steps, "max_steps", 1)
    _count(max_launches, "max_launches")
    budget_cap = plan_data["resource_budget"]["max_task_launches"]
    if max_launches > budget_cap:
        raise HectlError(f"max_launches {max_launches} exceeds the plan's max_task_launches {budget_cap}")
    planned = plan_data["outcome"]["unresolved_before"]
    unresolved = planned if unresolved is None else _count(unresolved, "unresolved")
    state = {"schema_version": 1, "run_id": run_id, "objective": objective, "plan": str(plan.resolve()),
             "plan_sha256": sha256_file(plan), "plan_run_id": plan_data["run_id"], "state": "running", "created_at": now_iso(),
             "caps": {"max_steps": max_steps, "max_task_launches": max_launches, "max_low_yield_waves": 1},
             "unresolved": unresolved, "launches": 0, "low_yield_waves": 0, "steps": []}
    write_json(state_path, state)
    return state


def _load(state_path: Path) -> dict[str, Any]:
    state = load_json(state_path)
    if state.get("schema_version") != 1 or "steps" not in state:
        raise HectlError("not a run state file")
    return state


def step(state_path: Path, action: str, delta: str, unresolved: int, checks: list[str], launches: int,
         group: Optional[str]) -> dict[str, Any]:
    state = _load(state_path)
    if state["state"] in TERMINAL:
        raise HectlError(f"run is {state['state']}; start a new run or re-plan")
    if not action.strip():
        raise HectlError("each step names its action")
    _count(unresolved, "unresolved")
    _count(launches, "launches")
    if sha256_file(Path(state["plan"])) != state["plan_sha256"]:
        state["state"] = "blocked"
        state["stop_reason"] = "approved plan changed during the run"
        write_json(state_path, state)
        return state
    progressed = bool(delta.strip()) and unresolved <= state["unresolved"]
    receipt = {"n": len(state["steps"]) + 1, "at": now_iso(), "action": action, "approval_group": group,
               "target_delta": delta, "unresolved_before": state["unresolved"], "unresolved_after": unresolved,
               "checks": checks, "launches": launches, "progressed": progressed}
    state["steps"].append(receipt)
    state["unresolved"] = unresolved
    state["launches"] += launches
    if not progressed:
        state["low_yield_waves"] += 1
    if state["launches"] > state["caps"]["max_task_launches"]:
        state["state"], state["stop_reason"] = "exhausted", "task launch cap exceeded"
    elif state["low_yield_waves"] >= state["caps"]["max_low_yield_waves"] and not progressed:
        state["state"], state["stop_reason"] = "exhausted", "a wave produced no target-state change; re-plan"
    elif len(state["steps"]) >= state["caps"]["max_steps"] and unresolved > 0:
        state["state"], state["stop_reason"] = "exhausted", "step cap reached with work unresolved"
    write_json(state_path, state)
    return state


def stop(state_path: Path, new_state: str, reason: str, verifier_receipt: Optional[Path]) -> dict[str, Any]:
    state = _load(state_path)
    if new_state not in TERMINAL:
        raise HectlError(f"state must be one of {sorted(TERMINAL)}")
    if state["state"] in TERMINAL and state["state"] != new_state:
        raise HectlError(f"run already ended as {state['state']}; a terminal state is not renamed")
    if new_state == "completed":
        if state["unresolved"] != 0:
            raise HectlError(f"cannot complete with {state['unresolved']} unresolved required items")
        if not verifier_receipt or not verifier_receipt.is_file():
            raise HectlError("completion needs a verifier receipt file")
        problems = check_receipt(load_json(verifier_receipt), state)
        if problems:
            raise HectlError("verifier receipt does not support completion: " + "; ".join(problems))
        state["verifier_receipt"] = str(verifier_receipt.resolve())
        state["verifier_receipt_sha256"] = sha256_file(verifier_receipt)
    state["state"], state["stop_reason"], state["ended_at"] = new_state, reason, now_iso()
    write_json(state_path, state)
    return state


def check_receipt(receipt: Any, state: dict[str, Any]) -> list[str]:
    """The receipt contract from assets/templates/verifier-receipt.json. Parsing cannot prove the
    evidence is true; it can refuse a receipt that records failure, gaps or staleness."""
    if not isinstance(receipt, dict):
        return ["receipt must be a JSON object"]
    problems = []
    if receipt.get("schema_version") != 1:
        problems.append("schema_version must be 1")
    if receipt.get("run_id") != state["run_id"]:
        problems.append("receipt run_id does not match this run")
    if receipt.get("functional_result") != "pass":
        problems.append(f"functional_result is {receipt.get('functional_result')!r}, not pass")
    if receipt.get("qualitative_result") not in ("pass", "not-required"):
        problems.append(f"qualitative_result is {receipt.get('qualitative_result')!r}, not pass or not-required")
    if receipt.get("unresolved_required") != 0:
        problems.append("unresolved_required must be 0")
    checks = receipt.get("checks")
    if not isinstance(checks, list) or not checks:
        problems.append("checks must list every required check")
    else:
        for i, check in enumerate(checks):
            if not isinstance(check, dict) or check.get("status") != "pass" or not check.get("evidence") or not check.get("check"):
                problems.append(f"checks[{i}] is not a passing check with evidence")
    verified = receipt.get("verified_at")
    last = state["steps"][-1]["at"] if state["steps"] else state["created_at"]
    if not isinstance(verified, str) or verified < last:
        problems.append("receipt is older than the last recorded step")
    return problems


def status(state_path: Path) -> dict[str, Any]:
    state = _load(state_path)
    last = state["steps"][-1] if state["steps"] else None
    plan_ok = Path(state["plan"]).is_file() and sha256_file(Path(state["plan"])) == state["plan_sha256"]
    nxt = ("resume: observe fresh state, choose one bounded action, record it with `run step`"
           if state["state"] == "running" and plan_ok else
           "re-plan: the approved plan changed" if not plan_ok else f"ended as {state['state']}")
    return {"run_id": state["run_id"], "state": state["state"], "unresolved": state["unresolved"],
            "steps": len(state["steps"]), "launches": state["launches"], "caps": state["caps"],
            "plan_unchanged": plan_ok, "last_step": last, "stop_reason": state.get("stop_reason"), "next": nxt}
