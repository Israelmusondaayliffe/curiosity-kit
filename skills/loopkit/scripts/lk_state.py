"""LoopKit's single authoritative snapshot. Python 3.9+, local POSIX filesystems."""
import contextlib
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import time
import uuid


class Fault(Exception):
    def __init__(self, code, detail):
        super().__init__(detail)
        self.code = code


def need(condition, code, detail):
    if not condition:
        raise Fault(code, detail)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path):
    try:
        with open(path, encoding="utf-8") as stream:
            def unique(pairs):
                out = {}
                for key, value in pairs:
                    need(key not in out, "duplicate-key", "Duplicate JSON key: " + key)
                    out[key] = value
                return out
            return json.load(stream, object_pairs_hook=unique,
                             parse_constant=lambda x: (_ for _ in ()).throw(Fault("invalid-json", x)))
    except (OSError, ValueError) as exc:
        raise Fault("unreadable-json", str(exc)) from exc


def clean_path(path):
    """Canonical real path. The named path itself must not be a symlink. Ancestors may be system aliases
    (macOS /tmp and /var resolve to /private/...); paths inside a workspace are checked strictly by scoped()."""
    p = Path(os.path.abspath(os.path.expanduser(str(path))))
    need(not p.is_symlink(), "symlink", "Symlink path refused: " + str(p))
    return Path(os.path.realpath(str(p)))


def atomic(path, data):
    path = clean_path(path)
    fd, name = tempfile.mkstemp(prefix=".lk-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, str(path))
        directory = os.open(str(path.parent), os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def save(run, state):
    atomic(run / "snapshot.json", encoded({"sha256": digest(state), "state": state}) + b"\n")


def load(run):
    run = clean_path(run)
    envelope = read_json(run / "snapshot.json")
    need(isinstance(envelope, dict) and isinstance(envelope.get("state"), dict),
         "snapshot-shape", "Snapshot envelope is malformed")
    s = envelope["state"]
    need(envelope.get("sha256") == digest(s), "snapshot-integrity", "Snapshot digest mismatch")
    need(s.get("schema") == 1 and s.get("contract_sha256") == digest(s.get("contract")),
         "contract-integrity", "Contract identity changed")
    need(type(s.get("generation")) is int and s["generation"] >= 0,
         "generation-invalid", "Invalid generation")
    need(s.get("run_path") == str(run), "run-moved", "Run path changed; do not silently relocate state")
    return s


@contextlib.contextmanager
def locked(run):
    try:
        import fcntl
    except ImportError as exc:
        raise Fault("locking-unavailable", "This implementation requires POSIX flock") from exc
    run = clean_path(run)
    path = clean_path(run / ".lock")
    fd = os.open(str(path), os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise Fault("writer-active", "Another writer holds this run; retry from a fresh read") from exc
        yield run
    finally:
        os.close(fd)


def edit(run, expected, event, operation):
    with locked(run) as root:
        s = load(root)
        need(s["generation"] == expected, "stale-writer", "Read current generation before retrying")
        result = operation(s, root)
        s["generation"] += 1
        s["updated_epoch"] = time.time()
        s["events"].append({"generation": s["generation"], "event": event, "at": s["updated_epoch"]})
        save(root, s)
        return s, result


def nonempty(value):
    return isinstance(value, str) and bool(value.strip()) and "__REPLACE_ME__" not in value


def names(items, label):
    need(isinstance(items, list), "contract-invalid", label + " must be a list")
    result = set()
    for item in items:
        need(isinstance(item, dict) and nonempty(item.get("id")), "contract-invalid", label + " needs ids")
        need(item["id"] not in result, "contract-invalid", "Duplicate " + label + " id")
        result.add(item["id"])
    return result


def validate(c):
    need(isinstance(c, dict) and c.get("schema") == 1, "contract-invalid", "Expected schema 1 object")
    for key in ("title", "outcome", "authority"):
        need(nonempty(c.get(key)), "contract-invalid", key + " is required")
    need(c.get("host") in ("codex", "claude-code"), "contract-invalid", "Choose the actual target host")
    for key in ("allowed_paths", "forbidden_paths", "external_actions", "artifacts"):
        need(isinstance(c.get(key), list) and all(nonempty(x) for x in c[key]),
             "contract-invalid", key + " must be a string list")
    need(c["allowed_paths"] and c["artifacts"], "contract-invalid", "Declare scope and observable artifacts")
    limits = c.get("limits", {})
    for key in ("max_iterations", "no_progress_limit", "max_seconds", "max_output_bytes"):
        need(type(limits.get(key)) is int and limits[key] > 0, "contract-invalid", "Positive " + key + " required")
    for key in ("success", "failure", "blocked", "exhausted"):
        need(nonempty(c.get("stops", {}).get(key)), "contract-invalid", "Missing stop: " + key)
    action_ids = names(c.get("actions"), "actions")
    check_ids = names(c.get("checks"), "checks")
    judgment_ids = names(c.get("judgments"), "judgments")
    unit_ids = names(c.get("units"), "units")
    need(check_ids and unit_ids, "contract-invalid", "At least one check and one unit required")
    for spec in c["actions"] + c["checks"]:
        argv = spec.get("argv")
        need(isinstance(argv, list) and argv and all(nonempty(x) and "\x00" not in x for x in argv),
             "contract-invalid", "Use a nonempty argv list, never a shell command string")
        need(nonempty(spec.get("cwd")) and nonempty(spec.get("authority")),
             "contract-invalid", "Each invocation needs cwd and its scoped authority reference")
        need(type(spec.get("timeout")) is int and 0 < spec["timeout"] <= limits["max_seconds"],
             "contract-invalid", "Invocation timeout exceeds run budget or is invalid")
        need(isinstance(spec.get("inputs", []), list) and all(nonempty(x) for x in spec.get("inputs", [])),
             "contract-invalid", "Invocation inputs must be relative file paths")
        need(isinstance(spec.get("artifacts", c["artifacts"]), list)
             and set(spec.get("artifacts", c["artifacts"])) <= set(c["artifacts"])
             and spec.get("artifacts", c["artifacts"]), "contract-invalid", "Invalid bound artifacts")
    for j in c["judgments"]:
        need(nonempty(j.get("criterion")) and type(j.get("independent")) is bool,
             "contract-invalid", "Judgment needs criterion and explicit independence requirement")
        # Optional scope: a review binds only the artifacts it judges, so later units' files do not invalidate it.
        need(isinstance(j.get("artifacts", c["artifacts"]), list) and j.get("artifacts", c["artifacts"])
             and set(j.get("artifacts", c["artifacts"])) <= set(c["artifacts"]), "contract-invalid", "Invalid judged artifacts")
    used_checks, used_judgments = set(), set()
    for unit in c["units"]:
        need(nonempty(unit.get("outcome")), "contract-invalid", "Unit needs observable outcome")
        for key, available in (("actions", action_ids), ("checks", check_ids), ("judgments", judgment_ids)):
            values = unit.get(key)
            need(isinstance(values, list) and all(isinstance(x, str) for x in values)
                 and len(set(values)) == len(values) and set(values) <= available,
                 "contract-invalid", "Invalid unit " + key)
        need(unit["checks"], "contract-invalid", "Every unit needs a real check")
        used_checks.update(unit["checks"])
        used_judgments.update(unit["judgments"])
    need(used_checks == check_ids and used_judgments == judgment_ids,
         "contract-invalid", "All declared checks and judgments must belong to a unit")
    return c


def within(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def inside(workspace, value):
    """Workspace-relative path with no symlink component inside the workspace, so a planted link cannot redirect access."""
    need(not Path(value).is_absolute(), "path-scope", "Contract paths must be workspace-relative")
    relative = Path(os.path.normpath(value))
    need(not relative.parts or relative.parts[0] != "..", "path-scope", "Path escapes workspace")
    p = workspace
    for part in ([] if str(relative) == "." else relative.parts):
        p = p / part
        need(not p.is_symlink(), "symlink", "Symlink inside workspace refused: " + str(p))
    need(within(p, workspace), "path-scope", "Path escapes workspace")
    return p


def scoped(s, value):
    workspace = clean_path(s["workspace"])
    p = inside(workspace, value)
    c = s["contract"]
    allowed = [inside(workspace, x) for x in c["allowed_paths"]]
    forbidden = [inside(workspace, x) for x in c["forbidden_paths"]]
    need(any(within(p, x) for x in allowed) and not any(within(p, x) for x in forbidden),
         "path-scope", "Path outside approved contract scope: " + value)
    return p


def artifacts(s):
    out = {}
    for name in s["contract"]["artifacts"]:
        p = scoped(s, name)
        need(not p.exists() or p.is_file(), "artifact-shape", "Declare exact files, not directories")
        out[name] = file_hash(p) if p.exists() else None
    return out


def initialize(contract, run, workspace):
    c = copy.deepcopy(validate(contract))
    root, workspace = clean_path(run), clean_path(workspace)
    need(workspace.is_dir(), "workspace-missing", "Workspace must exist")
    s = {"schema": 1, "run_id": uuid.uuid4().hex, "run_path": str(root), "workspace": str(workspace),
         "contract": c, "contract_sha256": digest(c), "generation": 0, "status": "ready",
         "unit_index": 0, "iterations": 0, "no_progress": 0, "started_epoch": None,
         "updated_epoch": time.time(), "pending": None, "results": [], "reviews": [],
         "verified_units": [], "reopened": [], "events": [], "schedule": None, "next_action": "Execute the first bounded unit"}
    for value in c["allowed_paths"] + c["forbidden_paths"] + c["artifacts"]:
        inside(workspace, value)
    for spec in c["actions"] + c["checks"]:
        need(scoped(s, spec["cwd"]).is_dir(), "cwd-missing", "Declared cwd must exist")
    s["last_artifacts"] = artifacts(s)
    s["progress_checks"] = []
    need(not root.exists(), "run-exists", "Choose a new run directory; existing runs are never overwritten")
    root.mkdir(parents=True, mode=0o700)
    (root / "evidence").mkdir(mode=0o700)
    save(root, s)
    return s
