"""Opt-in runtime readiness for `hectl audit --readiness`.

Static audit reports configuration; it cannot say whether hooks are trusted or whether a routine
actually produced its artifact. These checks add that, each with a status of pass, fail, unknown or
history. They read only what a supported surface exposes, keep output to an allowlist of fields,
bound every subprocess, and never change trust, permissions, schedules or files.
"""
from __future__ import annotations

import json
import math
import os
import re
import selectors
import subprocess
import time
from pathlib import Path
from typing import Any, Optional

from .common import HectlError

HOOK_FIELDS = ("key", "eventName", "pluginId", "sourcePath", "enabled", "isManaged", "currentHash", "trustStatus")
TRUSTED = {"trusted"}


def _check(name: str, status: str, detail: str, **data: Any) -> dict[str, Any]:
    return {"check": name, "status": status, "detail": detail, **data}


class ListingMalformed(Exception):
    """The native listing did not have the documented shape."""


def codex_native_hooks(cwd: Path, home: Path, codex_bin: str, timeout: float) -> tuple[list[dict[str, Any]], list[Any]]:
    """List hooks through the supported `codex app-server` JSON-lines interface (initialize, then
    hooks/list) for the selected home only (CODEX_HOME). Returns allowlisted rows and reported
    errors; raises ListingMalformed when the reply does not match the expected shape. The server
    is always stopped."""
    env = dict(os.environ, CODEX_HOME=str(home))
    proc = subprocess.Popen([codex_bin, "app-server"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, bufsize=0, env=env)
    selector = selectors.DefaultSelector()
    selector.register(proc.stdout, selectors.EVENT_READ)
    deadline = time.monotonic() + timeout
    buffer = b""

    def request(number: int, method: str, params: dict[str, Any]) -> Any:
        nonlocal buffer
        proc.stdin.write((json.dumps({"id": number, "method": method, "params": params}) + "\n").encode())
        proc.stdin.flush()
        while time.monotonic() < deadline:
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                if not line.strip():
                    continue
                reply = json.loads(line)
                if isinstance(reply, dict) and reply.get("id") == number:
                    if "error" in reply:
                        raise HectlError(f"{method} returned an error")
                    return reply.get("result")
            for key, _ in selector.select(max(0.01, min(1.0, deadline - time.monotonic()))):
                data = os.read(key.fileobj.fileno(), 65536)
                if not data:
                    raise HectlError("codex app-server ended before replying")
                buffer += data
        raise HectlError(f"codex app-server did not answer {method} within {timeout:g}s")

    try:
        request(1, "initialize", {"clientInfo": {"name": "hectl_readiness", "version": "1"}, "capabilities": {"experimentalApi": True}})
        proc.stdin.write(b'{"method":"initialized","params":{}}\n')
        proc.stdin.flush()
        result = request(2, "hooks/list", {"cwds": [str(cwd)]})
        if not isinstance(result, dict) or not isinstance(result.get("data"), list):
            raise ListingMalformed("hooks/list result has no data list")
        rows: list[dict[str, Any]] = []
        errors: list[Any] = []
        for entry in result["data"]:
            if not isinstance(entry, dict) or not isinstance(entry.get("hooks"), list) \
                    or not isinstance(entry.get("errors", []), list):
                raise ListingMalformed("hooks/list entry is not an object with a hooks list")
            errors.extend(entry.get("errors", []))
            for hook in entry["hooks"]:
                if not isinstance(hook, dict) or not isinstance(hook.get("enabled"), bool):
                    raise ListingMalformed("hook row is not an object with a boolean enabled flag")
                rows.append({k: hook.get(k) for k in HOOK_FIELDS})
        return rows, errors
    finally:
        selector.close()
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()


def hook_checks(platform: str, workspace: Optional[Path], home: Path, native: bool, codex_bin: str,
                timeout: float) -> list[dict[str, Any]]:
    if platform != "codex":
        return [_check("hooks-native-status", "unknown",
                       "no supported reader for native hook trust or enablement on this host; the configured hooks "
                       "listed in the audit are configuration, not trust or delivery evidence")]
    if not native:
        return [_check("hooks-native-status", "unknown", "not requested; pass --native-hooks to query codex app-server")]
    try:
        rows, errors = codex_native_hooks(workspace or home, home, codex_bin, timeout)
    except ListingMalformed as exc:
        return [_check("hooks-native-status", "unknown", f"native hook listing malformed: {exc}")]
    except (OSError, ValueError, HectlError) as exc:
        return [_check("hooks-native-status", "unknown", f"native hook listing unavailable: {type(exc).__name__}")]
    enabled = [r for r in rows if r.get("enabled") is True]
    # Managed hooks follow the host's managed trust policy, not per-user trust review.
    untrusted = [r for r in enabled if not r.get("isManaged") and r.get("trustStatus") not in TRUSTED]
    def source(row: dict[str, Any]) -> str:
        # One installed source: the full plugin id (name@marketplace), else the declaring file.
        return str(row.get("pluginId") or row.get("sourcePath") or row.get("key"))

    groups: dict[tuple[str, Any, Any], list[dict[str, Any]]] = {}
    by_event: dict[Any, list[dict[str, Any]]] = {}
    for row in enabled:
        by_event.setdefault(row.get("eventName"), []).append(row)
        if row.get("currentHash"):
            groups.setdefault(("same-content", row.get("eventName"), row.get("currentHash")), []).append(row)
        owner = str(row.get("pluginId") or "").partition("@")[0]
        if owner:
            groups.setdefault(("same-plugin", row.get("eventName"), owner), []).append(row)
    # A duplicate needs two distinct sources. Several handlers from one source are one owner's design.
    duplicates = [{"kind": kind, "event": event, "keys": [r.get("key") for r in g]}
                  for (kind, event, _), g in groups.items() if len({source(r) for r in g}) > 1]
    shared = {str(event): sorted({source(r) for r in g}) for event, g in by_event.items()
              if len({source(r) for r in g}) > 1}
    if duplicates:
        dup = _check("hooks-duplicate-owners", "fail",
                     f"{len(duplicates)} groups of enabled hooks are byte-identical or the same plugin from two sources",
                     duplicates=duplicates)
    elif shared:
        dup = _check("hooks-duplicate-owners", "unknown",
                     "no identical or same-plugin duplicates; several enabled hooks share an event and may overlap in purpose "
                     "(for example a legacy context bridge), which this check cannot rule out", shared_events=shared)
    else:
        dup = _check("hooks-duplicate-owners", "pass", "at most one enabled source per event")
    return [
        _check("hooks-native-listing", "fail" if errors else "pass",
               f"{len(rows)} hooks listed, {len(enabled)} enabled, {len(errors)} listing errors", hooks=rows),
        _check("hooks-trusted", "fail" if untrusted else "pass",
               f"{len(untrusted)} enabled, unmanaged hooks are not trusted", untrusted=[r.get("key") for r in untrusted]),
        dup,
    ]


def registry_checks(registry: Path, home: Path, platform: str) -> list[dict[str, Any]]:
    try:
        text = registry.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [_check("registry-structure", "unknown", f"registry unreadable: {type(exc).__name__}")]
    headings = [line.strip() for line in text.splitlines() if re.match(r"^#{2,3} ", line)]
    repeated = sorted({h for h in headings if headings.count(h) > 1})
    out = [_check("registry-structure", "fail" if repeated else "pass",
                  f"{len(headings)} section headings, {len(repeated)} repeated", repeated=repeated)]
    if platform in ("claude-code", "cowork"):
        folders = sorted(p.parent.name for p in (home / "scheduled-tasks").glob("*/SKILL.md"))
        missing = [name for name in folders if name not in text]
        # Without the host's own task state, an unnamed folder may be paused history or an orphan, not an active failure.
        out.append(_check("registry-task-parity", "unknown" if missing else "pass",
                          f"{len(folders)} scheduled-task folders, {len(missing)} not named in the registry; "
                          "inventory only, active versus paused is not known", unregistered=missing))
    else:
        out.append(_check("registry-task-parity", "unknown",
                          "no supported reader for this host's scheduled tasks; parity not checked"))
    out.append(_check("scheduled-task-native-state", "unknown",
                      "enabled, paused and permission-mode state come from the host app; no supported reader is used"))
    return out


def routine_receipt_check(state_path: Path, platform: str, home: Path) -> list[dict[str, Any]]:
    """A routine counts as working only if its last success left a dry-run receipt for this host
    and home that proves complete status, no stop or unverified checks, and an empty deletion list."""
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [_check("routine-receipt", "unknown", "routine state file not found")]
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        return [_check("routine-receipt", "fail", f"routine state unreadable: {type(exc).__name__}")]
    if not isinstance(state, dict):
        return [_check("routine-receipt", "fail", "routine state is not a JSON object")]
    fails = state.get("consecutive_failures")
    if isinstance(fails, bool) or not isinstance(fails, int) or fails < 0:
        return [_check("routine-receipt", "fail", "consecutive_failures is not a non-negative integer")]
    if state.get("last_result") != "complete" or fails != 0:
        return [_check("routine-receipt", "fail", f"last run did not complete cleanly; {fails} consecutive failures",
                       consecutive_failures=fails)]
    receipt_path = state.get("last_receipt")
    if not isinstance(receipt_path, str) or not Path(receipt_path).is_file():
        return [_check("routine-receipt", "fail", "last run reported success but its receipt is missing")]
    try:
        receipt = json.loads(Path(receipt_path).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        receipt = None
    if not isinstance(receipt, dict):
        return [_check("routine-receipt", "fail", "receipt unreadable", receipt=receipt_path)]
    host = "claude-code" if platform == "cowork" else platform
    try:
        same_home = Path(str(receipt.get("home"))).resolve() == home.resolve()
    except (OSError, RuntimeError):
        same_home = False
    proven = (receipt.get("host") == host and same_home and receipt.get("mode") == "dry-run"
              and receipt.get("status") == "complete" and not receipt.get("stop_reason")
              and receipt.get("unverified") == [] and receipt.get("deleted") == [])
    return [_check("routine-receipt", "pass" if proven else "fail",
                   "receipt proves a complete dry run for this host and home with zero deletion" if proven else
                   "receipt does not prove a complete dry run for this host and home with zero deletion",
                   receipt=receipt_path, mode=receipt.get("mode"), receipt_status=receipt.get("status"),
                   deleted=len(receipt.get("deleted") or []) if isinstance(receipt.get("deleted"), list) else None)]


def readiness(platform: str, home: Path, workspace: Optional[Path], registry: Optional[Path] = None,
              routine_state: Optional[Path] = None, native_hooks: bool = False, codex_bin: str = "codex",
              timeout: float = 30) -> dict[str, Any]:
    if not math.isfinite(timeout) or timeout <= 0:
        raise HectlError("--readiness-timeout must be a finite positive number", exit_code=2)
    checks = hook_checks(platform, workspace, home, native_hooks, codex_bin, timeout)
    checks += registry_checks(registry, home, platform) if registry else [
        _check("registry-structure", "unknown", "no registry selected; pass --registry")]
    checks += routine_receipt_check(routine_state, platform, home) if routine_state else [
        _check("routine-receipt", "unknown", "no routine selected; pass --routine-state")]
    counts = {s: sum(1 for c in checks if c["status"] == s) for s in ("pass", "fail", "unknown", "history")}
    return {"overall": "fail" if counts["fail"] else ("unknown" if counts["unknown"] else "pass"),
            "counts": counts, "checks": checks}
