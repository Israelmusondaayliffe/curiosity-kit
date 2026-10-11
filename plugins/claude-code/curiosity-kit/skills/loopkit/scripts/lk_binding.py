"""Explicit workspace-to-run hook selection; no discovery scans or host settings."""
import hashlib
import os
from pathlib import Path
from lk_state import Fault, need, load, locked, read_json, atomic, encoded, digest, clean_path

OWNER = "loopkit.workspace-binding"
TERMINAL = {"completed", "exhausted", "failed", "cancelled"}


def canonical(path):
    return Path(path).expanduser().resolve()


def state_root(host, supplied=None):
    need(host in {"codex", "claude-code"}, "binding-host", "Unknown host")
    selected = supplied if supplied is not None else os.environ.get("LOOPKIT_STATE_ROOT")
    if selected is not None:
        need(bool(str(selected).strip()), "binding-root", "State root cannot be empty")
        return canonical(selected)
    if host == "codex":
        return canonical(Path(os.environ.get("CODEX_HOME") or (Path.home() / ".codex")) / "loopkit")
    return canonical(Path(os.environ.get("CLAUDE_CONFIG_DIR") or (Path.home() / ".claude")) / "loopkit")


def pointer_path(host, workspace, supplied=None):
    work = canonical(workspace)
    key = hashlib.sha256(str(work).encode("utf-8")).hexdigest()
    path = state_root(host, supplied) / "bindings" / host / (key + ".json")
    # Explicit root aliases are canonicalized. Never follow a substituted pointer/directory.
    clean_path(path)
    return path, work


def pointer_read(path, host, workspace):
    need(not path.is_symlink(), "binding-symlink", "Binding pointer is a symlink")
    value = read_json(path)
    need(isinstance(value, dict) and isinstance(value.get("binding"), dict), "binding-invalid", "Malformed binding")
    b = value["binding"]
    need(value.get("sha256") == digest(b), "binding-integrity", "Binding digest mismatch")
    need(b.get("schema") == 1 and b.get("owner") == OWNER, "binding-owner", "Not a LoopKit-owned binding")
    need(b.get("host") == host and b.get("workspace") == str(workspace),
         "binding-mismatch", "Pointer host/workspace does not match")
    need(isinstance(b.get("run"), str) and isinstance(b.get("run_id"), str), "binding-invalid", "Missing run identity")
    need(str(canonical(b["run"])) == b["run"], "binding-invalid", "Run pointer must be canonical")
    return b


def validate_run(run, host, workspace, expected_id=None):
    s = load(canonical(run))
    need(s["contract"]["host"] == host and s["workspace"] == str(workspace),
         "binding-run-mismatch", "Run snapshot belongs to a different host or workspace")
    need(expected_id is None or s["run_id"] == expected_id, "binding-run-replaced", "Selected run identity changed")
    return s


def bind(run, workspace, host, supplied=None, replace_run=None):
    path, work = pointer_path(host, workspace, supplied)
    selected = canonical(run)
    s = validate_run(selected, host, work)
    need(s["status"] not in TERMINAL, "binding-terminal", "Choose a nonterminal run")
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with locked(path.parent):
        # Re-read under the pointer lock; no snapshot mutation or run-directory search.
        s = validate_run(selected, host, work)
        need(s["status"] not in TERMINAL, "binding-terminal", "Run became terminal")
        if path.exists():
            previous = pointer_read(path, host, work)
            same = previous["run"] == str(selected) and previous["run_id"] == s["run_id"]
            need(same or (replace_run is not None and previous["run"] == str(canonical(replace_run))),
                 "binding-conflict", "A different run is selected; name it explicitly with --replace-run")
        else:
            need(replace_run is None, "binding-changed", "Expected prior binding is absent")
        b = {"schema": 1, "owner": OWNER, "host": host, "workspace": str(work),
             "run": str(selected), "run_id": s["run_id"]}
        atomic(path, encoded({"binding": b, "sha256": digest(b)}) + b"\n")
    return {"bound": True, "pointer": str(path), "run": str(selected), "run_id": s["run_id"],
            "workspace": str(work), "host": host}


def resolve(workspace, host, supplied=None):
    path, work = pointer_path(host, workspace, supplied)
    if not path.exists():
        return None
    b = pointer_read(path, host, work)
    s = validate_run(b["run"], host, work, b["run_id"])
    if s["status"] in TERMINAL:
        return None
    return Path(b["run"])


def unbind(run, workspace, host, supplied=None):
    path, work = pointer_path(host, workspace, supplied)
    if not path.exists():
        return {"unbound": False, "reason": "no-selected-pointer"}
    with locked(path.parent):
        need(path.exists(), "binding-changed", "Binding changed before cleanup")
        b = pointer_read(path, host, work)
        need(b["run"] == str(canonical(run)), "binding-conflict", "Selected pointer names a different run")
        # Validate pointer ownership/identity, but permit cleanup of a now-missing or corrupt run.
        # We remove only the named owned pointer, never its run, evidence, root or other bindings.
        path.unlink()
        fd = os.open(str(path.parent), os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    return {"unbound": True, "pointer": str(path), "run": b["run"]}
