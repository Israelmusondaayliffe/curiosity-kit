"""Shared helpers for hectl. Standard library only; Python 3.9 or newer."""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
TOOL_VERSION = "1.0.0"
SECRET_KEY = re.compile(r"(?i)(token|secret|password|passwd|cookie|credential|authorization|api[_-]?key|private[_-]?key|bearer)")
PLATFORMS = ("claude-code", "cowork", "codex")


class HectlError(RuntimeError):
    """A refusal or failed precondition. exit_code lets callers map safety stops."""

    def __init__(self, message: str, exit_code: int = 1):
        super().__init__(message)
        self.exit_code = exit_code


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise HectlError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise HectlError(f"invalid JSON in {path}: {exc}") from exc


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    """Write through a temp file in the same directory, then rename."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if path.exists():
            os.chmod(tmp, path.stat().st_mode & 0o777)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def write_json(path: Path, payload: Any) -> None:
    atomic_write(Path(path), (json.dumps(payload, indent=2, sort_keys=False) + "\n").encode("utf-8"))


def is_within(path: Path, root: Path) -> bool:
    try:
        Path(path).resolve(strict=False).relative_to(Path(root).resolve(strict=False))
        return True
    except ValueError:
        return False


def redact_keys(keys: list[str]) -> list[str]:
    return sorted("redacted-sensitive-key" if SECRET_KEY.search(k) else k for k in keys)


def frontmatter(text: str) -> tuple[dict[str, str], int]:
    """Parse simple YAML frontmatter (scalar keys, folded or quoted values).

    Returns the mapping and the line index where the body starts. An absent or
    unterminated block returns ({}, 0).
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, 0
    data: dict[str, str] = {}
    current = None
    for index in range(1, len(lines)):
        line = lines[index]
        if line.strip() == "---":
            for key, value in data.items():
                value = value.strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                    value = value[1:-1]
                data[key] = value
            return data, index + 1
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match and not line.startswith(" "):
            current = match.group(1)
            value = match.group(2)
            data[current] = "" if value in (">", ">-", "|", "|-") else value
        elif current is not None and line.startswith((" ", "\t")):
            data[current] = (data[current] + " " + line.strip()).strip()
    return {}, 0
