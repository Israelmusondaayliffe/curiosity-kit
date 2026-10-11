"""Small local committed-operation store. Process-crash recovery, not a database service.

A commit file is the sole authority. JSON projections are disposable and verified on
ordinary reads. Immutable content objects are staged before a commit. No filesystem
lock is held while a controller calls a worker or external service. Hashes establish
local integrity, not authentication, OS isolation or distributed exactly-once work.
"""
from __future__ import annotations

import base64
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import tempfile
import time
from typing import Any

RECORD_VERSION = 2


class RuntimeErrorBase(ValueError):
    code = 2


class CorruptionError(RuntimeErrorBase):
    code = 3


class ApprovalError(RuntimeErrorBase):
    code = 4


class ConversionNeeded(RuntimeErrorBase):
    code = 5


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                       allow_nan=False) + "\n").encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def byte_digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def identifier(value: Any, label: str = "identifier") -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", value) or value in {".", ".."}:
        raise RuntimeErrorBase(f"{label}: unsafe identifier")
    return value


def safe_root(root: Path) -> Path:
    root = Path(os.path.abspath(str(root)))
    for part in [root, *root.parents]:
        if part.is_symlink():
            raise RuntimeErrorBase("run root or ancestor is a symlink")
    return root


def safe_path(root: Path, relative: str) -> Path:
    root = safe_root(root)
    if not isinstance(relative, str) or not relative or "\\" in relative or any(ord(c) < 32 for c in relative):
        raise RuntimeErrorBase("unsafe relative path")
    p = PurePosixPath(relative)
    if p.is_absolute() or ".." in p.parts or relative != p.as_posix():
        raise RuntimeErrorBase("unsafe relative path")
    result = root
    for component in p.parts:
        result = result / component
        if result.is_symlink():
            raise RuntimeErrorBase("symlink in an owned path")
    return result


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=str(path.parent), prefix=".stage-", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(str(temporary), str(path))
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def fault(phase: str) -> None:
    """Explicit isolated-test hook. Never configured by graph or worker content."""
    if os.environ.get("OG_FAULT_PHASE") == phase:
        os._exit(91)


class Store:
    def __init__(self, root: Path):
        self.root = safe_root(root)

    @contextmanager
    def lock(self, timeout: float = 2.0, *, create: bool = False):
        try:
            import fcntl
        except ImportError as exc:
            raise RuntimeErrorBase("local writer lock unsupported on this platform") from exc
        if create:
            self.root.mkdir(parents=True, exist_ok=True)
        elif not self.root.is_dir():
            raise RuntimeErrorBase("run is not initialized; read-only access creates no directory")
        path = safe_path(self.root, ".writer.lock")
        if not create and not path.is_file():
            if (self.root / "state.json").exists() and not (self.root / "commits").exists():
                raise ConversionNeeded("conversion-needed: legacy records have no protocol-2 writer lock")
            raise CorruptionError("initialized run writer lock is missing; no lock was created or stolen")
        with path.open("a+b" if create else "r+b") as handle:
            limit = time.monotonic() + timeout
            while True:
                try:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= limit:
                        raise RuntimeErrorBase("run writer is busy; no lock was stolen")
                    time.sleep(0.02)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def commits(self):
        folder = safe_path(self.root, "commits")
        paths = sorted(folder.glob("*.json")) if folder.exists() else []
        if not paths:
            if (self.root / "state.json").exists() or (self.root / "events.jsonl").exists():
                raise ConversionNeeded("conversion-needed: v1/live records are not migrated; create an isolated v2 run")
            raise RuntimeErrorBase("run is not initialized")
        records = []
        previous = None
        run_id = None
        operations = set()
        for seq, path in enumerate(paths, 1):
            safe_path(self.root, path.relative_to(self.root).as_posix())
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
                expected = record["sha256"]
                unsigned = {k: v for k, v in record.items() if k != "sha256"}
                if record["recordVersion"] != RECORD_VERSION:
                    raise ConversionNeeded("conversion-needed: unsupported committed record version")
                if digest(unsigned) != expected or record["sequence"] != seq or record["previousSha256"] != previous:
                    raise CorruptionError("committed operation chain mismatch")
                if path.name != f"{seq:08d}.json":
                    raise CorruptionError("committed operation sequence filename mismatch")
                if record["operationId"] in operations:
                    raise CorruptionError("duplicate committed operation identity")
                if run_id is not None and record["data"]["runId"] != run_id:
                    raise CorruptionError("committed run identity changed")
                if record["data"]["generation"] != seq:
                    raise CorruptionError("committed generation mismatch")
                run_id = record["data"]["runId"]
                operations.add(record["operationId"])
            except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
                raise CorruptionError(f"invalid committed record: {path.name}") from exc
            records.append(record)
            previous = expected
        return records

    def projections(self, records):
        data = records[-1]["data"]
        files = {
            "state.json": canonical(data),
            "graph.json": canonical(data["graph"]),
            "contract.json": canonical(data["contract"]),
            "policies.json": canonical(data["graph"]["rewritePolicy"]),
            "artifacts.jsonl": b"".join(canonical(data["artifacts"][key]) for key in sorted(data["artifacts"])),
            "approvals.jsonl": b"".join(canonical(a) for a in data["approvals"]),
            "events.jsonl": b"".join(canonical({k:r[k] for k in ("sequence", "operationId", "operation", "intentSha256", "timestamp", "previousSha256", "sha256")}) for r in records),
            "graph-versions/hashes.json": canonical({v: digest(g) for v,g in data["versions"].items()}),
        }
        for version, graph in data["versions"].items():
            files[f"graph-versions/v{int(version):04d}.json"] = canonical(graph)
        for invocation in data["invocations"].values():
            prefix = invocation["directory"]
            files[prefix + "/task-packet.json"] = canonical(invocation["task"])
            files[prefix + "/dispatch-receipt.json"] = canonical(invocation["dispatchReceipt"])
            if invocation.get("launch") is not None:
                files[prefix + "/thread-launch.json"] = canonical(invocation["launch"])
            if invocation.get("launchReceipt") is not None:
                files[prefix + "/launch-receipt.json"] = canonical(invocation["launchReceipt"])
            if invocation.get("returned") is not None:
                files[prefix + "/return-receipt.json"] = canonical(invocation["returned"])
            for index, late in enumerate(invocation.get("lateReturns", [])):
                files[prefix + f"/late-return-{index+1}.json"] = canonical(late)
        for key, proposal in data["proposals"].items():
            files[f"rewrites/proposals/{key}.json"] = canonical(proposal)
        for change in data["rewrites"]:
            files[f"rewrites/applied/{change['proposalId']}.json"] = canonical(change)
        if data.get("verification"):
            files["verification.json"] = canonical(data["verification"])
        return files

    def load(self, *, check_projections: bool = True, check_objects: bool = True):
        records = self.commits()
        if check_projections:
            for relative, content in self.projections(records).items():
                path = safe_path(self.root, relative)
                if not path.is_file() or path.read_bytes() != content:
                    raise CorruptionError(f"projection mismatch: {relative}; use recover from committed authority")
        data = deepcopy(records[-1]["data"])
        for sha in data["objects"] if check_objects else []:
            path = safe_path(self.root, f"objects/{sha}")
            if not path.is_file() or byte_digest(path.read_bytes()) != sha:
                raise CorruptionError(f"committed content object missing or altered: {sha}")
        return data, records

    def stage_object(self, content: bytes) -> str:
        sha = byte_digest(content)
        path = safe_path(self.root, f"objects/{sha}")
        if path.exists():
            if path.read_bytes() != content:
                raise CorruptionError("immutable content address collision")
        else:
            atomic_write(path, content)
        return sha

    def publish(self, records):
        for relative, content in self.projections(records).items():
            path = safe_path(self.root, relative)
            atomic_write(path, content)
            fault("during-projections")
        fault("after-projection")

    def commit(self, data, records, operation_id, operation, intent, result):
        identifier(operation_id, "operationId")
        sequence = len(records) + 1
        data["generation"] = sequence
        record = {"recordVersion": RECORD_VERSION, "sequence": sequence,
                  "operationId": operation_id, "operation": operation,
                  "intentSha256": digest(intent), "timestamp": now(),
                  "previousSha256": records[-1]["sha256"] if records else None,
                  "data": deepcopy(data), "result": deepcopy(result)}
        record["sha256"] = digest(record)
        fault("before-commit")
        path = safe_path(self.root, f"commits/{sequence:08d}.json")
        if path.exists():
            raise CorruptionError("commit generation already exists")
        atomic_write(path, canonical(record))
        fault("after-commit")
        records = records + [record]
        self.publish(records)
        return deepcopy(result)

    def recover(self):
        with self.lock():
            data, records = self.load(check_projections=False, check_objects=False)
            self.publish(records)
            return {"recovered": True, "generation": data["generation"],
                    "runId": data["runId"], "guarantee": "local process-crash recovery only"}
