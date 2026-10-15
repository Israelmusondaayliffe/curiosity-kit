"""Guarded stale-data cleanup for a Claude Code or Codex home.

Dry-run unless --apply. Only allowlisted categories past their retention floor are
candidates. Every safety check runs before the first deletion, and every run writes
an atomic receipt. Exit codes: 0 ok, 2 safety stop, 3 locked, 4 bad home, 5 receipt failure.
"""
from __future__ import annotations

import json
import math
import os
import shutil
import signal
import subprocess
import time
from pathlib import Path
from typing import Any, Optional

from .common import TOOL_VERSION, HectlError, is_within, now_iso, write_json

EXIT_OK, EXIT_SAFETY, EXIT_LOCKED, EXIT_BAD_HOME, EXIT_RECEIPT = 0, 2, 3, 4, 5
MAX_CANDIDATES = 10_000
MAX_BYTES = 2 * 1024 ** 3
LOCK = ".hectl-cleanup.lock"
STALE_LOCK_SECONDS = 6 * 3600

PROFILES: dict[str, dict[str, Any]] = {
    "claude-code": {
        "retention": {"transcripts": 90, "cache": 14, "shell_snapshots": 30, "plugin_versions": 30},
        "deny_names": {"CLAUDE.md", "MEMORY.md", "settings.json", "settings.local.json", ".credentials.json",
                       "installed_plugins.json", "known_marketplaces.json", "config.json"},
        "deny_parts": {"memory", "scheduled-tasks", "hooks", "agents", "commands", "skills", "backups",
                       "marketplaces", "data", "cleanup-receipts"},
    },
    "codex": {
        "retention": {"archived_sessions": 90, "cache": 14, "temp": 14, "shell_snapshots": 30, "plugin_versions": 30},
        "deny_names": {"config.toml", "auth.json", "AGENTS.md", "MEMORY.md", "history.jsonl"},
        "deny_parts": {"sessions", "memories", "backups", "attachments", "generated_images", "skills", "rules",
                       ".tmp", "sqlite", "state", "cleanup-receipts"},
    },
}


def resolve_home(host: str, override: Optional[str]) -> Path:
    env = "CLAUDE_CONFIG_DIR" if host == "claude-code" else "CODEX_HOME"
    default = Path.home() / (".claude" if host == "claude-code" else ".codex")
    raw = override or os.environ.get(env) or str(default)
    if "$" in raw:
        raise HectlError(f"refusing unexpanded home path {raw!r}", EXIT_BAD_HOME)
    home = Path(raw).expanduser()
    if not home.is_absolute():
        raise HectlError(f"refusing relative home path {raw!r}", EXIT_BAD_HOME)
    if home.is_symlink():
        raise HectlError(f"refusing symlinked home {home}", EXIT_BAD_HOME)
    resolved = home.resolve()
    if not resolved.is_dir():
        raise HectlError(f"home does not exist: {resolved}", EXIT_BAD_HOME)
    if resolved == Path("/") or len(resolved.parts) < 3 or resolved == Path.home().resolve():
        raise HectlError(f"refusing broad root as home: {resolved}", EXIT_BAD_HOME)
    if (resolved / ".git").exists():
        raise HectlError(f"refusing a repository root as home: {resolved}", EXIT_BAD_HOME)
    if host == "claude-code":
        if not (resolved / "settings.json").is_file() or not ((resolved / "plugins").is_dir() or (resolved / "projects").is_dir()):
            raise HectlError(f"{resolved} does not look like a Claude Code home", EXIT_BAD_HOME)
    elif not ((resolved / "config.toml").is_file() or (resolved / "plugins").is_dir()):
        raise HectlError(f"{resolved} does not look like a Codex home", EXIT_BAD_HOME)
    return resolved


def _newest_mtime(path: Path) -> float:
    newest = path.lstat().st_mtime
    if path.is_dir():
        for child in path.rglob("*"):
            newest = max(newest, child.lstat().st_mtime)
    return newest


def _bytes(path: Path) -> int:
    if path.is_file():
        return path.lstat().st_size
    return sum(c.lstat().st_size for c in path.rglob("*") if c.is_file() and not c.is_symlink())


def _has_symlink(path: Path) -> bool:
    return path.is_symlink() or (path.is_dir() and any(c.is_symlink() for c in path.rglob("*")))


def _reference_texts(host: str, home: Path, extra: list[Path]) -> tuple[list[str], bool]:
    sources: list[Path] = []
    if host == "claude-code":
        sources += sorted((home / "projects").glob("*/memory/**/*.md")) if (home / "projects").is_dir() else []
        sources += [home / "CLAUDE.md"] + sorted((home / "scheduled-tasks").glob("*/SKILL.md"))
    else:
        sources += [home / "memories" / "MEMORY.md"] + sorted((home / "memories" / "rollout_summaries").glob("*.md"))
    sources += extra
    texts = []
    try:
        for source in sources:
            if source.is_file() and not source.is_symlink():
                texts.append(source.read_text(encoding="utf-8", errors="replace"))
    except OSError:
        return texts, False
    return texts, True


def _installed_claude(home: Path) -> tuple[set[tuple[str, str, str]], set[tuple[str, str]], set[Path], Optional[str]]:
    """Installed plugin versions from installed_plugins.json. Any schema surprise disables plugin cleanup."""
    unavailable = (set(), set(), set())
    try:
        data = json.loads((home / "plugins" / "installed_plugins.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return (*unavailable, f"installed_plugins.json unreadable ({exc}); plugin versions not considered")
    plugins = data.get("plugins") if isinstance(data, dict) else None
    if not isinstance(plugins, dict) or not plugins:
        return (*unavailable, "installed_plugins.json has no recognizable plugins map; plugin versions not considered")
    triples, pairs, paths = set(), set(), set()
    for key, installs in plugins.items():
        if "@" not in key or not isinstance(installs, list) or not installs:
            return (*unavailable, f"installed_plugins.json entry {key!r} is malformed; plugin versions not considered")
        plugin, market = key.rsplit("@", 1)
        pairs.add((market, plugin))
        for install in installs:
            if not isinstance(install, dict) or not isinstance(install.get("version"), str) or not install["version"]:
                return (*unavailable, f"installed_plugins.json entry {key!r} has a malformed install row; plugin versions not considered")
            triples.add((market, plugin, install["version"]))
            if install.get("installPath"):
                paths.add(Path(install["installPath"]).resolve())
    return triples, pairs, paths, None


def _installed_codex(home: Path, installed_json: Optional[Path]) -> tuple[Optional[set[Path]], Optional[str]]:
    """Active plugin versions from `codex plugin list --json` (or a saved copy). Any schema surprise disables plugin cleanup."""
    try:
        if installed_json:
            payload = json.loads(installed_json.read_text(encoding="utf-8"))
        else:
            if not shutil.which("codex"):
                return None, "codex CLI not found; plugin versions not considered"
            run = subprocess.run(["codex", "plugin", "list", "--json"], capture_output=True, text=True, timeout=60, check=True)
            payload = json.loads(run.stdout)
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        return None, f"installed plugin inventory failed ({exc}); plugin versions not considered"
    rows = payload.get("installed") if isinstance(payload, dict) else None
    if not isinstance(rows, list) or not rows:
        return None, "installed plugin inventory has no recognizable installed list; plugin versions not considered"
    active = set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("installed"), bool):
            return None, f"malformed installed row {row!r}; plugin versions not considered"
        parts = [row.get("marketplaceName"), row.get("name"), row.get("version")]
        if not all(isinstance(p, str) and p for p in parts):
            return None, f"installed row lacks marketplace, name or version {row!r}; plugin versions not considered"
        if row["installed"]:
            active.add((home / "plugins" / "cache" / parts[0] / parts[1] / parts[2]).resolve())
    if not active:
        return None, "inventory lists no installed plugin; plugin versions not considered"
    return active, None


def _referenced(path: Path, home: Path, texts: list[str]) -> bool:
    rel = path.relative_to(home).as_posix()
    return any(str(path) in t or rel in t or path.name in t for t in texts)


def _plugin_active(host: str, home: Path, path: Path, installed_json: Optional[Path]) -> Optional[bool]:
    """Fresh inventory read for one plugin version directory. None means the inventory is unavailable."""
    if host == "claude-code":
        triples, pairs, install_paths, warning = _installed_claude(home)
        if warning:
            return None
        market, plugin, version = path.relative_to(home / "plugins" / "cache").parts[:3]
        return (market, plugin) not in pairs or (market, plugin, version) in triples or path.resolve() in install_paths
    active, warning = _installed_codex(home, installed_json)
    if warning or active is None:
        return None
    return path.resolve() in active


def _recheck(host: str, home: Path, candidate: dict[str, Any], retention: dict[str, int], clock: float,
             texts: list[str], installed_json: Optional[Path]) -> Optional[str]:
    """Return a reason to keep the candidate, re-checked immediately before deletion."""
    path = Path(candidate["path"])
    category = candidate["category"]
    profile = PROFILES[host]
    if not path.exists() and not path.is_symlink():
        return "disappeared-before-action"
    if path.is_symlink() or _has_symlink(path) or not is_within(path.resolve(), home):
        return "symlink-or-escape-before-action"
    rel = path.relative_to(home)
    if path.name in profile["deny_names"] or set(rel.parts[:-1] if path.is_file() else rel.parts) & profile["deny_parts"]:
        return "denied-location"
    if (clock - _newest_mtime(path)) / 86400 <= retention[category]:
        return "became-recent-before-action"
    if path.is_dir() and ((path / ".in_use").exists() or (path / ".lock").exists()):
        return "in-use-marker-before-action"
    if _referenced(path, home, texts):
        return "referenced-by-memory-before-action"
    if category == "plugin_versions":
        active = _plugin_active(host, home, path, installed_json)
        if active is None:
            return "plugin-inventory-unavailable-before-action"
        if active:
            return "plugin-became-active-before-action"
    open_found, open_unknown = _open_paths([path])
    owned, owned_unknown = _process_owned([path])
    if open_unknown or owned_unknown:
        raise HectlError("open-file or process check became unavailable during deletion", EXIT_SAFETY)
    if str(path) in open_found:
        return "open-file-before-action"
    if str(path) in owned:
        return "process-owned-before-action"
    return None


def discover(host: str, home: Path, retention: dict[str, int], now: float, extra_refs: list[Path],
             installed_json: Optional[Path] = None) -> dict[str, Any]:
    profile = PROFILES[host]
    candidates: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    warnings: list[str] = []
    texts, refs_ok = _reference_texts(host, home, extra_refs)

    def consider(path: Path, category: str, mtime: Optional[float] = None) -> None:
        rel = path.relative_to(home)
        if path.is_symlink() or _has_symlink(path):
            skipped.append({"path": str(path), "category": category, "reason": "symlink"})
            return
        if not is_within(path.resolve(), home):
            skipped.append({"path": str(path), "category": category, "reason": "escapes-home"})
            return
        if path.name in profile["deny_names"] or set(rel.parts[:-1] if path.is_file() else rel.parts) & profile["deny_parts"]:
            skipped.append({"path": str(path), "category": category, "reason": "denied-location"})
            return
        if path.is_dir() and ((path / ".in_use").exists() or (path / ".lock").exists()):
            skipped.append({"path": str(path), "category": category, "reason": "in-use-marker"})
            return
        age = (now - (mtime if mtime is not None else _newest_mtime(path))) / 86400
        if age <= retention[category]:
            return
        if category in ("transcripts", "archived_sessions") and not refs_ok:
            skipped.append({"path": str(path), "category": category, "reason": "memory-check-unavailable"})
            return
        if _referenced(path, home, texts):
            skipped.append({"path": str(path), "category": category, "reason": "referenced-by-memory"})
            return
        candidates.append({"path": str(path), "category": category, "is_dir": path.is_dir(),
                           "bytes": _bytes(path), "age_days": round(age, 1)})

    def files_under(root: Path, category: str) -> None:
        if root.is_dir() and not root.is_symlink():
            for item in sorted(root.rglob("*")):
                if item.is_file() or item.is_symlink():
                    consider(item, category, item.lstat().st_mtime)

    if host == "claude-code":
        projects = home / "projects"
        if projects.is_dir():
            for transcript in sorted(projects.glob("*/*.jsonl")):
                consider(transcript, "transcripts", transcript.lstat().st_mtime)
        files_under(home / "cache", "cache")
        files_under(home / "shell-snapshots", "shell_snapshots")
        triples, pairs, install_paths, warning = _installed_claude(home)
        cache = home / "plugins" / "cache"
        if warning:
            warnings.append(warning)
        elif cache.is_dir():
            for version_dir in sorted(cache.glob("*/*/*")):
                if not version_dir.is_dir():
                    continue
                market, plugin, version = version_dir.relative_to(cache).parts
                if (market, plugin) not in pairs:
                    skipped.append({"path": str(version_dir), "category": "plugin_versions", "reason": "plugin-not-installed"})
                elif (market, plugin, version) in triples or version_dir.resolve() in install_paths:
                    continue
                else:
                    consider(version_dir, "plugin_versions")
    else:
        files_under(home / "archived_sessions", "archived_sessions")
        files_under(home / "cache", "cache")
        files_under(home / "tmp", "temp")
        files_under(home / "shell_snapshots", "shell_snapshots")
        active, warning = _installed_codex(home, installed_json)
        cache = home / "plugins" / "cache"
        if warning:
            warnings.append(warning)
        elif cache.is_dir() and active is not None:
            for version_dir in sorted(cache.glob("*/*/*")):
                if version_dir.is_dir() and version_dir.resolve() not in active:
                    consider(version_dir, "plugin_versions")
    return {"candidates": candidates, "skipped": skipped, "warnings": warnings}


def _open_paths(paths: list[Path]) -> tuple[set[str], set[str]]:
    """(open, unknown): paths open in any process, and paths the check could not verify."""
    if not paths:
        return set(), set()
    lsof = shutil.which("lsof")
    if not lsof:
        return set(), {str(p) for p in paths}
    found: set[str] = set()
    unknown: set[str] = set()
    files = [p for p in paths if not p.is_dir()]
    for start in range(0, len(files), 150):
        chunk = files[start:start + 150]
        try:
            run = subprocess.run([lsof, "-Fn", "--"] + [str(p) for p in chunk], capture_output=True, text=True, timeout=120)
        except (OSError, subprocess.SubprocessError):
            unknown.update(str(p) for p in chunk)
            continue
        if run.returncode not in (0, 1):
            unknown.update(str(p) for p in chunk)
            continue
        found.update(line[1:] for line in run.stdout.splitlines() if line.startswith("n"))
    for directory in (p for p in paths if p.is_dir()):
        try:
            run = subprocess.run([lsof, "-Fn", "+D", str(directory)], capture_output=True, text=True, timeout=300)
        except (OSError, subprocess.SubprocessError):
            unknown.add(str(directory))
            continue
        if run.returncode not in (0, 1):
            unknown.add(str(directory))
        elif any(line.startswith("n") for line in run.stdout.splitlines()):
            found.add(str(directory))
    return found, unknown


def _process_owned(paths: list[Path]) -> tuple[set[str], set[str]]:
    """(owned, unknown): paths named on a live process command line, and paths ps could not verify."""
    try:
        run = subprocess.run(["ps", "-axo", "args"], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return set(), {str(p) for p in paths}
    table = run.stdout
    if run.returncode != 0 or not table.strip():
        return set(), {str(p) for p in paths}
    return {str(p) for p in paths if str(p) in table}, set()


def _lock(home: Path) -> Path:
    lock = home / LOCK
    try:
        fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        try:
            pid = int(lock.read_text().strip() or "0")
        except (OSError, ValueError):
            pid = 0
        alive = False
        if pid:
            try:
                os.kill(pid, 0)
                alive = True
            except OSError:
                alive = False
        if alive or time.time() - lock.stat().st_mtime < STALE_LOCK_SECONDS:
            raise HectlError(f"another cleanup holds {lock}", EXIT_LOCKED)
        lock.unlink()
        fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    with os.fdopen(fd, "w") as handle:
        handle.write(str(os.getpid()))
    return lock


def _delete(path: Path, home: Path) -> None:
    if path.is_symlink() or not is_within(path.resolve(), home):
        raise HectlError(f"unsafe at deletion time: {path}", EXIT_SAFETY)
    if path.is_dir():
        for child in sorted(path.rglob("*"), key=lambda p: len(p.parts), reverse=True):
            if child.is_symlink():
                raise HectlError(f"symlink appeared during deletion: {child}", EXIT_SAFETY)
            child.unlink() if child.is_file() else child.rmdir()
        path.rmdir()
    else:
        path.unlink()
        parent = path.parent
        while parent != home and is_within(parent, home) and parent.name not in ("projects", "cache", "plugins", "tmp", "archived_sessions", "shell_snapshots", "shell-snapshots"):
            try:
                parent.rmdir()
            except OSError:
                break
            parent = parent.parent


def run_cleanup(host: str, home_override: Optional[str], apply: bool, retention_overrides: dict[str, int],
                max_candidates: int, max_bytes: int, receipt_dir: Optional[Path], extra_refs: list[Path],
                installed_json: Optional[Path] = None, now: Optional[float] = None,
                approved_receipt: Optional[Path] = None) -> tuple[int, dict[str, Any]]:
    profile = PROFILES[host]
    retention = dict(profile["retention"])
    for key, value in retention_overrides.items():
        if key not in retention:
            raise HectlError(f"unknown retention category {key} for {host}")
        if value < retention[key]:
            raise HectlError(f"retention for {key} can only be raised (floor {retention[key]} days)")
        retention[key] = value
    if max_candidates > MAX_CANDIDATES or max_bytes > MAX_BYTES or max_candidates < 1 or max_bytes < 1:
        raise HectlError("ceilings can only be lowered from 10000 candidates and 2 GiB")
    home = resolve_home(host, home_override)
    approved: Optional[set] = None
    if apply:
        if approved_receipt is None:
            raise HectlError("--apply needs --approved-receipt: the dry-run receipt whose candidates the user approved")
        try:
            prior = json.loads(Path(approved_receipt).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise HectlError(f"approved receipt unreadable: {exc}")
        if prior.get("mode") != "dry-run" or prior.get("host") != host or Path(prior.get("home", "")).resolve() != home:
            raise HectlError("approved receipt must be a dry run for this host and home")
        if prior.get("status") != "complete" or prior.get("stop_reason") or prior.get("unverified"):
            raise HectlError("approved receipt is blocked or incomplete; rerun the dry run once every check can run")
        approved = {c["path"] for c in prior.get("candidates", []) if isinstance(c, dict) and "path" in c}
    receipt_root = receipt_dir or home / "cleanup-receipts"
    receipt: dict[str, Any] = {"tool": "hectl cleanup", "tool_version": TOOL_VERSION, "host": host, "home": str(home),
                               "mode": "apply" if apply else "dry-run", "started_at": now_iso(),
                               "retention_days": retention, "ceilings": {"max_candidates": max_candidates, "max_bytes": max_bytes},
                               "safety_checks": [], "deleted": [], "unverified": [], "stop_reason": None}
    code = EXIT_OK
    lock = _lock(home)
    receipt["disk_free_before"] = shutil.disk_usage(home).free
    try:
        found = discover(host, home, retention, now or time.time(), extra_refs, installed_json)
        receipt.update(found)
        total = sum(c["bytes"] for c in found["candidates"])
        receipt["candidate_bytes"] = total
        if len(found["candidates"]) > max_candidates or total > max_bytes:
            receipt["stop_reason"] = "ceiling exceeded; nothing deleted"
            code = EXIT_SAFETY
        else:
            receipt["safety_checks"].append("ceilings")
            paths = [Path(c["path"]) for c in found["candidates"]]
            open_found, open_unknown = _open_paths(paths)
            owned, owned_unknown = _process_owned(paths)
            receipt["safety_checks"] += ["open-files" if not open_unknown else "open-files-unavailable",
                                         "process-ownership" if not owned_unknown else "process-ownership-unavailable"]
            keep = []
            for candidate in found["candidates"]:
                path_text = candidate["path"]
                if path_text in open_unknown or path_text in owned_unknown:
                    reasons = [r for r, bucket in (("open-file-check-unavailable", open_unknown),
                                                   ("process-check-unavailable", owned_unknown)) if path_text in bucket]
                    receipt["unverified"].append({**candidate, "reasons": reasons})
                elif path_text in open_found:
                    receipt["skipped"].append({"path": path_text, "category": candidate["category"], "reason": "open-file"})
                elif path_text in owned:
                    receipt["skipped"].append({"path": path_text, "category": candidate["category"], "reason": "process-owned"})
                else:
                    keep.append(candidate)
            receipt["candidates"] = keep
            if receipt["unverified"]:
                receipt["stop_reason"] = (f"{len(receipt['unverified'])} items could not be checked for open files or owning processes; "
                                          "status blocked, nothing is approval-eligible or deleted until the checks run")
                code = EXIT_SAFETY
            else:
                if apply:
                    clock = now or time.time()
                    texts, refs_ok = _reference_texts(host, home, extra_refs)
                    for candidate in keep:
                        if approved is not None and candidate["path"] not in approved:
                            receipt["skipped"].append({"path": candidate["path"], "category": candidate["category"], "reason": "not-in-approved-set"})
                            continue
                        if candidate["category"] in ("transcripts", "archived_sessions") and not refs_ok:
                            receipt["skipped"].append({"path": candidate["path"], "category": candidate["category"], "reason": "memory-check-unavailable-before-action"})
                            continue
                        reason = _recheck(host, home, candidate, retention, clock, texts, installed_json)
                        if reason:
                            receipt["skipped"].append({"path": candidate["path"], "category": candidate["category"], "reason": reason})
                            continue
                        _delete(Path(candidate["path"]), home)
                        receipt["deleted"].append(candidate["path"])
                    receipt["safety_checks"].append("pre-action-recheck")
    except HectlError as exc:
        receipt["stop_reason"] = str(exc)
        code = exc.exit_code if exc.exit_code in (EXIT_SAFETY, EXIT_LOCKED, EXIT_BAD_HOME) else EXIT_SAFETY
    finally:
        if lock.exists():
            lock.unlink()
    receipt["status"] = ("complete" if code == EXIT_OK and not receipt["stop_reason"] else
                         "blocked" if receipt["unverified"] else "safety-stop")
    receipt["disk_free_after"] = shutil.disk_usage(home).free
    receipt["finished_at"] = now_iso()
    try:
        stamp = receipt["finished_at"].replace("+00:00", "Z").replace(":", "")
        path = receipt_root / f"{stamp}-{host}-{receipt['mode']}.json"
        write_json(path, receipt)
        receipt["receipt"] = str(path)
    except OSError as exc:
        receipt["stop_reason"] = f"receipt write failed: {exc}"
        return EXIT_RECEIPT, receipt
    return code, receipt


ROUTINE_COMPLETE, ROUTINE_FAILED, ROUTINE_STOPPED, ROUTINE_STATE_INVALID, ROUTINE_BUSY = 0, 1, 3, 4, 5


def _routine_state(path: Path) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    """Read routine state. Absent is a fresh start; anything unreadable or malformed fails closed."""
    if not os.path.lexists(path):
        return {"consecutive_failures": 0}, None
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, f"unreadable or invalid JSON: {type(exc).__name__}"
    if not isinstance(state, dict):
        return None, "state is not a JSON object"
    fails = state.get("consecutive_failures")
    if isinstance(fails, bool) or not isinstance(fails, int) or fails < 0:
        return None, f"consecutive_failures must be a non-negative integer, found {type(fails).__name__}"
    return state, None


def _replace_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def _release_owned_lock(lock: Optional[Path], pid: int) -> bool:
    """Remove the cleanup lock only when it records exactly this child's pid."""
    if lock is None or not lock.is_file() or lock.is_symlink():
        return False
    try:
        owner = lock.read_text(encoding="utf-8").strip()
    except OSError:
        return False
    if owner != str(pid):
        return False
    lock.unlink()
    return True


def _run_bounded(argv: list[str], timeout: float, owned_lock: Optional[Path]) -> tuple[Optional[int], str, str, bool]:
    """Run the dry run in its own process group. On timeout, kill that group (including any
    inventory helpers it started) and release only the lock the killed child owned."""
    proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        out, err = proc.communicate(timeout=timeout)
        return proc.returncode, out, err, False
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except OSError:
            pass
        proc.communicate()
        _release_owned_lock(owned_lock, proc.pid)
        return None, "", "", True


def _receipt_status(stdout: str) -> tuple[Optional[str], str]:
    try:
        summary = json.loads(stdout)
    except ValueError:
        summary = None
    reported = summary.get("receipt") if isinstance(summary, dict) else None
    if reported is not None and not isinstance(reported, str):
        return None, "receipt-path-invalid"
    if not reported:
        return None, "no-receipt-in-output"
    if not Path(reported).is_file():
        return reported, "receipt-missing"
    try:
        receipt = json.loads(Path(reported).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        receipt = None
    if not isinstance(receipt, dict):
        return reported, "receipt-unreadable"
    if receipt.get("mode") != "dry-run":
        return reported, "wrong-mode"
    if receipt.get("deleted") != []:
        return reported, "deleted-in-dry-run" if receipt.get("deleted") else "deletion-list-missing"
    status = receipt.get("status")
    return reported, status if isinstance(status, str) else "receipt-status-invalid"


def run_routine(state_path: Path, child_argv: list[str], max_failures: int, timeout: float,
                owned_lock: Optional[Path] = None) -> tuple[int, dict[str, Any]]:
    """Opt-in unattended wrapper around a dry-run cleanup. It owns a consecutive-failure counter:
    invalid state fails closed without running or writing; at the limit it stops without running;
    an overlapping invocation is refused (exit 5) without touching the counter; otherwise it runs
    the dry run as a bounded child process group, reads the exact receipt the child reports, and
    replaces the state atomically. It never applies."""
    if max_failures < 1 or not math.isfinite(timeout) or timeout <= 0:
        raise HectlError("--routine-max-failures must be at least 1 and --routine-timeout a finite positive number",
                         exit_code=2)
    try:
        import fcntl
    except ImportError:
        raise HectlError("routine mode needs POSIX file locking (fcntl)", exit_code=2)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    guard = os.open(str(state_path.with_name(f".{state_path.name}.lock")), os.O_CREAT | os.O_RDWR, 0o600)
    try:
        try:
            fcntl.flock(guard, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            return ROUTINE_BUSY, {"result": "BUSY", "state": str(state_path),
                                  "reason": "another routine invocation holds this state; nothing ran and the counter is unchanged"}
        return _routine_locked(state_path, child_argv, max_failures, timeout, owned_lock)
    finally:
        os.close(guard)


def _routine_locked(state_path: Path, child_argv: list[str], max_failures: int, timeout: float,
                    owned_lock: Optional[Path]) -> tuple[int, dict[str, Any]]:
    state, problem = _routine_state(state_path)
    if state is None:
        return ROUTINE_STATE_INVALID, {"result": "STATE_INVALID", "state": str(state_path), "reason": problem,
                                       "action": "nothing ran and the state file was not changed; inspect or restore it"}
    fails = state["consecutive_failures"]
    if fails >= max_failures:
        return ROUTINE_STOPPED, {"result": "STOPPED", "state": str(state_path), "consecutive_failures": fails,
                                 "reason": f"{fails} consecutive failed runs; review the receipts, then reset consecutive_failures to 0"}
    receipt_path: Optional[str] = None
    child_exit: Optional[int] = None
    detail = ""
    try:
        child_exit, out, err, timed_out = _run_bounded(child_argv, timeout, owned_lock)
        if timed_out:
            status, detail = "timeout", f"dry run exceeded {timeout:g}s; its process group was stopped"
        else:
            receipt_path, status = _receipt_status(out)
            if child_exit != 0 or status != "complete":
                detail = (err or "")[-600:]
    except OSError as exc:
        status, detail = "launch-failed", type(exc).__name__
    ok = child_exit == 0 and status == "complete"
    fails = 0 if ok else fails + 1
    _replace_state(state_path, {"consecutive_failures": fails, "last_run": now_iso(),
                                "last_result": "complete" if ok else "failed", "last_status": status,
                                "last_receipt": receipt_path})
    return (ROUTINE_COMPLETE if ok else ROUTINE_FAILED), {
        "result": "COMPLETE" if ok else "FAILED", "state": str(state_path), "receipt": receipt_path,
        "receipt_status": status, "dry_run_exit": child_exit, "consecutive_failures": fails, "detail": detail}
