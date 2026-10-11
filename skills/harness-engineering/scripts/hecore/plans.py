"""Profile and operations-plan validation, guarded apply, and rollback.

Apply checks every approved operation before writing anything, then records each
write in the manifest as it happens, so an interrupted run can still be rolled back.
"""
from __future__ import annotations

import hashlib
import os
import re
import shutil
from pathlib import Path
from typing import Any, Optional

from .common import (PLATFORMS, SCHEMA_VERSION, HectlError, atomic_write, is_within, load_json,
                     now_iso, sha256_bytes, sha256_file, write_json)

SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
RECORD_TYPES = {"fact", "constraint", "preference", "assumption", "decision"}
OUTCOME_FIELDS = {"primary_metric", "before_state", "target_state", "unresolved_before",
                  "unresolved_target", "expected_primary_outputs"}
BUDGET_FIELDS = {"max_task_launches", "max_support_artifacts", "max_verification_passes",
                 "max_low_yield_waves", "high_cost_approved", "cost_warning"}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _count(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def validate_profile(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["profile must be an object"]
    for key in ("schema_version", "status", "platform", "user", "scope", "decisions"):
        if key not in data:
            errors.append(f"missing {key}")
    if errors:
        return errors
    if data["schema_version"] != SCHEMA_VERSION:
        errors.append("unsupported schema_version")
    if data["status"] not in ("draft", "confirmed"):
        errors.append("status must be draft or confirmed")
    platform = data["platform"]
    if not isinstance(platform, dict) or platform.get("primary") not in PLATFORMS:
        errors.append(f"platform.primary must be one of {', '.join(PLATFORMS)}")
    elif any(p not in PLATFORMS for p in platform.get("others", [])):
        errors.append("platform.others contains an unknown platform")
    for key in ("user", "scope"):
        if not isinstance(data[key], dict):
            errors.append(f"{key} must be an object")
    decisions = data["decisions"]
    if not isinstance(decisions, list):
        errors.append("decisions must be a list")
    else:
        for i, record in enumerate(decisions):
            if not isinstance(record, dict) or record.get("type") not in RECORD_TYPES or not _nonempty(record.get("text")):
                errors.append(f"decisions[{i}] needs type in {sorted(RECORD_TYPES)} and text")
    for i, item in enumerate(data.get("deferred", [])):
        if not isinstance(item, dict) or not _nonempty(item.get("item")) or not (_nonempty(item.get("owner")) or _nonempty(item.get("revisit_trigger"))):
            errors.append(f"deferred[{i}] needs item plus owner or revisit_trigger")
    if data.get("status") == "confirmed" and not _nonempty(data.get("confirmed_by")):
        errors.append("a confirmed profile records confirmed_by")
    return errors


def check_target(target: Path, roots: list[Path]) -> Path:
    if target.is_symlink():
        raise HectlError(f"target is a symlink: {target}")
    resolved = target.expanduser().resolve(strict=False)
    if not any(is_within(resolved, root) for root in roots):
        raise HectlError(f"target outside allowed roots: {target}")
    return resolved


def validate_plan(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["plan must be an object"]
    for key in ("schema_version", "run_id", "platform", "allowed_roots", "approval_groups", "outcome",
                "resource_budget", "support_artifacts", "operations"):
        if key not in data:
            errors.append(f"missing {key}")
    if errors:
        return errors
    if data["schema_version"] != SCHEMA_VERSION:
        errors.append("unsupported schema_version")
    if not isinstance(data["run_id"], str) or not SAFE_ID.match(data["run_id"]) or data["run_id"] in (".", ".."):
        errors.append("run_id must be 1-64 characters of letters, digits, dot, dash or underscore, starting with a letter or digit")
    if data["platform"] not in PLATFORMS:
        errors.append(f"platform must be one of {', '.join(PLATFORMS)}")
    roots = data["allowed_roots"]
    if not isinstance(roots, list) or not roots or not all(_nonempty(r) for r in roots):
        errors.append("allowed_roots must be a non-empty list of paths")
        roots = []
    groups = data["approval_groups"]
    if not isinstance(groups, list) or not groups or len(groups) != len(set(groups)):
        errors.append("approval_groups must be a non-empty unique list")
        groups = []
    outcome = data["outcome"]
    if not isinstance(outcome, dict) or set(outcome) != OUTCOME_FIELDS:
        errors.append(f"outcome must have exactly {sorted(OUTCOME_FIELDS)}")
    else:
        for key in ("primary_metric", "before_state", "target_state"):
            if not _nonempty(outcome[key]):
                errors.append(f"outcome.{key} must be a non-empty string")
        if not (_count(outcome["unresolved_before"]) and _count(outcome["unresolved_target"])):
            errors.append("outcome unresolved counts must be non-negative integers")
        elif outcome["unresolved_target"] > outcome["unresolved_before"]:
            errors.append("outcome.unresolved_target cannot exceed unresolved_before")
        if not (_count(outcome["expected_primary_outputs"]) and outcome["expected_primary_outputs"] >= 1):
            errors.append("outcome.expected_primary_outputs must be at least 1")
    budget = data["resource_budget"]
    if not isinstance(budget, dict) or set(budget) != BUDGET_FIELDS:
        errors.append(f"resource_budget must have exactly {sorted(BUDGET_FIELDS)}")
    else:
        launches = budget["max_task_launches"]
        if not (_count(launches) and launches <= 24):
            errors.append("max_task_launches must be 0 to 24")
        elif launches > 6 and not (budget["high_cost_approved"] is True and _nonempty(budget["cost_warning"])):
            errors.append("a launch cap above 6 needs high_cost_approved=true and a cost_warning")
        if budget["max_verification_passes"] != 1:
            errors.append("max_verification_passes must be 1: one final verification pass, reruns only for changes")
        if budget["max_low_yield_waves"] != 1:
            errors.append("max_low_yield_waves must be 1: one wave without target-state change stops the run")
        if not (_count(budget["max_support_artifacts"]) and budget["max_support_artifacts"] <= 12):
            errors.append("max_support_artifacts must be 0 to 12")
        elif isinstance(data["support_artifacts"], list) and len(data["support_artifacts"]) > budget["max_support_artifacts"]:
            errors.append("support_artifacts exceeds max_support_artifacts")
    if not isinstance(data["support_artifacts"], list) or len(set(map(str, data["support_artifacts"]))) != len(data["support_artifacts"]):
        errors.append("support_artifacts must be a list without duplicates")
    ops = data["operations"]
    if not isinstance(ops, list):
        return errors + ["operations must be a list"]
    seen: set[str] = set()
    canonical: dict[str, str] = {}
    root_paths = [Path(r).expanduser() for r in roots]
    for i, op in enumerate(ops):
        label = f"operations[{i}]"
        if not isinstance(op, dict):
            errors.append(f"{label} must be an object")
            continue
        for key in ("id", "action", "target", "approval_group"):
            if key not in op:
                errors.append(f"{label} missing {key}")
        if any(key not in op for key in ("id", "action", "target", "approval_group")):
            continue
        if not isinstance(op["id"], str) or not SAFE_ID.match(op["id"]):
            errors.append(f"operation id {op['id']!r} must be 1-64 characters of letters, digits, dot, dash or underscore")
            continue
        if op["id"] in seen:
            errors.append(f"duplicate operation id {op['id']}")
        seen.add(op["id"])
        if op["action"] not in ("create", "update"):
            errors.append(f"{op['id']}: action must be create or update")
        if op["approval_group"] not in groups:
            errors.append(f"{op['id']}: unknown approval group {op['approval_group']}")
        if ("content" in op) == ("source" in op):
            errors.append(f"{op['id']}: needs exactly one of content or source")
        if op["action"] == "update" and not _nonempty(op.get("expected_sha256")):
            errors.append(f"{op['id']}: update requires expected_sha256")
        if not _nonempty(op.get("reason")):
            errors.append(f"{op['id']}: every operation states its reason")
        if root_paths:
            try:
                check_target(Path(op["target"]).expanduser(), root_paths)
            except HectlError as exc:
                errors.append(f"{op['id']}: {exc}")
        for key in target_keys(Path(op["target"])):
            if key in canonical:
                errors.append(f"{op['id']}: same target as {canonical[key]} (one operation per file)")
                break
        for key in target_keys(Path(op["target"])):
            canonical.setdefault(key, op["id"])
    return errors


def target_keys(path: Path) -> list[str]:
    """Identity keys for a target: resolved path folded for case-insensitive volumes, plus inode when it exists."""
    resolved = Path(path).expanduser().resolve(strict=False)
    keys = ["path:" + str(resolved).casefold()]
    try:
        stat = resolved.stat()
        keys.append(f"inode:{stat.st_dev}:{stat.st_ino}")
    except OSError:
        pass
    return keys


def _payload(op: dict[str, Any]) -> bytes:
    if "content" in op:
        return str(op["content"]).encode("utf-8")
    source = Path(op["source"]).expanduser()
    if not source.is_file() or source.is_symlink():
        raise HectlError(f"{op['id']}: source is not a regular file: {source}")
    return source.read_bytes()


def _control_checks(targets: list[Path], receipt: Path, manifest: Optional[Path], backup_dir: Optional[Path]) -> None:
    """Receipts, manifests and backups must not collide with targets or pass through symlinks."""
    target_keys_all = {k for t in targets for k in target_keys(t)}
    for label, path in (("receipt", receipt), ("manifest", manifest), ("backup directory", backup_dir)):
        if path is None:
            continue
        path = Path(path).expanduser()
        for parent in [path, *path.parents]:
            if parent.is_symlink():
                raise HectlError(f"{label} path passes through a symlink: {parent}")
        if set(target_keys(path)) & target_keys_all:
            raise HectlError(f"{label} path is also an operation target: {path}")
        for target in targets:
            if label == "backup directory" and is_within(target, path):
                raise HectlError(f"operation target lies inside the backup directory: {target}")
    if manifest is not None and Path(manifest).exists():
        raise HectlError(f"manifest already exists; keep it and choose a new path: {manifest}")
    if receipt is not None and manifest is not None and set(target_keys(receipt)) & set(target_keys(manifest)):
        raise HectlError("receipt and manifest must be different files")


def _crash_point(op_id: str) -> None:
    """Test hook: simulate a process kill after the target write and before the manifest update."""
    if os.environ.get("HECTL_TEST_CRASH_AFTER_WRITE") == op_id:
        os._exit(70)


def apply_plan(plan: dict[str, Any], mode: str, approved: set[str], receipt: Path,
               backup_dir: Optional[Path] = None, manifest: Optional[Path] = None) -> dict[str, Any]:
    errors = validate_plan(plan)
    if errors:
        raise HectlError("plan invalid: " + "; ".join(errors))
    unknown = approved - set(plan["approval_groups"])
    if unknown:
        raise HectlError(f"unknown approved groups: {', '.join(sorted(unknown))}")
    if mode == "apply" and (backup_dir is None or manifest is None):
        raise HectlError("apply needs --backup-dir and --manifest")
    roots = [Path(r).expanduser() for r in plan["allowed_roots"]]
    # Bookkeeping files may not collide with any declared target, approved or not, current or not.
    _control_checks([Path(op["target"]).expanduser() for op in plan["operations"]], receipt,
                    manifest if mode == "apply" else None, backup_dir if mode == "apply" else None)
    # Preflight: every approved operation must be safe before the first write.
    staged = []
    results: list[dict[str, Any]] = []
    for op in plan["operations"]:
        if op["approval_group"] not in approved:
            results.append({"id": op["id"], "status": "not-approved"})
            continue
        target = check_target(Path(op["target"]).expanduser(), roots)
        payload = _payload(op)
        desired = sha256_bytes(payload)
        if op["action"] == "create":
            if target.exists() or target.is_symlink():
                raise HectlError(f"{op['id']}: create target already exists: {target}")
        else:
            if not target.is_file() or target.is_symlink():
                raise HectlError(f"{op['id']}: update target is not a regular file: {target}")
            current = sha256_file(target)
            if current != op["expected_sha256"]:
                raise HectlError(f"{op['id']}: hash changed since audit: {target}")
            if current == desired:
                results.append({"id": op["id"], "status": "already-current", "sha256": current})
                continue
        staged.append((op, target, payload, desired))
    if mode == "dry-run":
        for op, target, _payload_bytes, desired in staged:
            results.append({"id": op["id"], "status": "would-change", "action": op["action"],
                            "target": str(target), "sha256": desired})
        out = {"schema_version": SCHEMA_VERSION, "run_id": plan["run_id"], "mode": mode,
               "approved_groups": sorted(approved), "generated_at": now_iso(), "results": results}
        write_json(receipt, out)
        return out
    assert backup_dir is not None and manifest is not None
    run_backups = backup_dir / plan["run_id"]
    if not is_within(run_backups, backup_dir) or run_backups.resolve(strict=False) == backup_dir.resolve(strict=False):
        raise HectlError(f"run_id does not give a folder inside the backup directory: {plan['run_id']!r}")
    if run_backups.exists():
        raise HectlError(f"backups for run {plan['run_id']} already exist; keep them and use a new run id or directory: {run_backups}")
    run_backups.mkdir(parents=True)
    record = {"schema_version": SCHEMA_VERSION, "run_id": plan["run_id"], "status": "in-progress",
              "started_at": now_iso(), "backup_root": str(run_backups), "entries": []}
    write_json(manifest, record)
    try:
        for op, target, payload, desired in staged:
            entry: dict[str, Any] = {"id": op["id"], "action": op["action"], "target": str(target),
                                     "applied_sha256": desired, "state": "pending", "created_dirs": []}
            if op["action"] == "update":
                backup = run_backups / f"{op['id']}-{hashlib.sha256(str(target).encode()).hexdigest()[:12]}-{target.name}"
                if not is_within(backup, run_backups) or backup.exists() or backup.is_symlink():
                    raise HectlError(f"{op['id']}: unsafe or existing backup path {backup}")
                shutil.copy2(target, backup)
                entry["backup"] = str(backup)
                entry["original_sha256"] = sha256_file(backup)
            else:
                missing = []
                parent = target.parent
                while not parent.exists():
                    missing.append(str(parent))
                    parent = parent.parent
                entry["created_dirs"] = missing
            # Write-ahead: the entry is durable before the target changes.
            record["entries"].append(entry)
            write_json(manifest, record)
            atomic_write(target, payload)
            _crash_point(op["id"])
            entry["state"] = "applied"
            write_json(manifest, record)
            results.append({"id": op["id"], "status": "changed", "target": str(target), "sha256": sha256_file(target)})
    except BaseException as exc:
        record["status"] = "interrupted"
        record["error"] = str(exc)
        write_json(manifest, record)
        raise HectlError(f"apply interrupted; roll back with the manifest {manifest}: {exc}")
    record["status"] = "complete"
    record["finished_at"] = now_iso()
    write_json(manifest, record)
    out = {"schema_version": SCHEMA_VERSION, "run_id": plan["run_id"], "mode": mode,
           "approved_groups": sorted(approved), "generated_at": now_iso(), "results": results,
           "manifest": str(manifest)}
    write_json(receipt, out)
    return out


def rollback(manifest_path: Path, receipt: Path) -> dict[str, Any]:
    """Undo an apply, including an interrupted one. Pending entries are resolved by hash:
    a target still at its original state needs nothing, one at the applied state is restored,
    anything else blocks the whole rollback before any file changes."""
    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict) or manifest.get("schema_version") != SCHEMA_VERSION or not isinstance(manifest.get("entries"), list):
        raise HectlError("invalid rollback manifest")
    _control_checks([Path(e["target"]) for e in manifest["entries"]], receipt, None, None)
    plan_actions = []
    for entry in reversed(manifest["entries"]):
        target = Path(entry["target"])
        if target.is_symlink():
            raise HectlError(f"rollback target is a symlink: {target}")
        current = sha256_file(target) if target.is_file() else None
        if entry["action"] == "create":
            if current is None and entry.get("state") == "pending":
                plan_actions.append(("nothing", entry))
            elif current == entry["applied_sha256"]:
                plan_actions.append(("remove", entry))
            else:
                raise HectlError(f"rollback refused, file changed after apply: {target}")
        else:
            backup = Path(entry["backup"])
            if not backup.is_file() or sha256_file(backup) != entry["original_sha256"]:
                raise HectlError(f"rollback backup missing or changed: {backup}")
            if current == entry["original_sha256"] and entry.get("state") == "pending":
                plan_actions.append(("nothing", entry))
            elif current == entry["applied_sha256"]:
                plan_actions.append(("restore", entry))
            else:
                raise HectlError(f"rollback refused, file changed after apply: {target}")
    results = []
    for action, entry in plan_actions:
        target = Path(entry["target"])
        if action == "remove":
            target.unlink()
            for directory in entry.get("created_dirs", []):
                try:
                    Path(directory).rmdir()
                except OSError:
                    break
            results.append({"id": entry["id"], "status": "removed-created-file", "target": str(target)})
        elif action == "restore":
            atomic_write(target, Path(entry["backup"]).read_bytes())
            results.append({"id": entry["id"], "status": "restored", "target": str(target), "sha256": sha256_file(target)})
        else:
            results.append({"id": entry["id"], "status": "never-written", "target": str(target)})
    out = {"schema_version": SCHEMA_VERSION, "run_id": manifest.get("run_id"), "generated_at": now_iso(), "results": results}
    write_json(receipt, out)
    return out
