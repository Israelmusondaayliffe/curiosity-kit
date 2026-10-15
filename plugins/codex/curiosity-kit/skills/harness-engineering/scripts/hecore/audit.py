"""Read-only harness audit. Records names and structure, never secret values."""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Optional

from .common import HectlError, is_within, now_iso, redact_keys, sha256_file

MANAGED_CLAUDE_MD = {
    "darwin": Path("/Library/Application Support/ClaudeCode/CLAUDE.md"),
    "linux": Path("/etc/claude-code/CLAUDE.md"),
}
IMPORT_RE = re.compile(r"(?<![\w`])@((?:~|\.{1,2}|/)?[\w./-]+\.\w+)")
PATH_RE = re.compile(r"`((?:~|/)[^`\s]+)`")
# Date or named placeholders mark a path template, not a literal file: YYYY-MM-DD, {name}.
TEMPLATE_RE = re.compile(r"YYYY|\bMM-DD\b|\{[^}/]+\}")
# A single absolute segment with no extension reads as a slash command (/contract-check, /plugin:skill).
COMMAND_RE = re.compile(r"/[A-Za-z][\w:-]*")
SECRET_VALUE = re.compile(r"(?i)(sk-|key|token|secret|bearer|password)")
PLACEHOLDER_RE = re.compile(r"\[fill:[^\]]*\]|\[(?:TODO|TBD|PLACEHOLDER)[^\]]*\]|\{\{[^}]+\}\}|<(?:REPLACE|FILL)[^>]*>", re.IGNORECASE)


def detect_platform_details() -> dict[str, Any]:
    """Platform signals. Installed CLIs alone do not identify the running host."""
    home = Path.home()
    signals = {
        "cowork_sandbox": Path("/mnt/user-data/uploads").is_dir() and (home / ".claude/plugins/synced").is_dir(),
        "inside_claude_code_session": os.environ.get("CLAUDECODE") == "1",
        "claude_installed": bool(shutil.which("claude")) or (home / ".claude/settings.json").is_file(),
        "codex_installed": bool(shutil.which("codex")) or Path(os.environ.get("CODEX_HOME", home / ".codex")).is_dir(),
    }
    if signals["cowork_sandbox"]:
        platform, reason = "cowork", "Cowork sandbox paths present"
    elif signals["inside_claude_code_session"]:
        platform, reason = "claude-code", "running inside a Claude Code session (CLAUDECODE=1)"
    elif signals["claude_installed"] and signals["codex_installed"]:
        platform, reason = "ambiguous", "both Claude Code and Codex are installed and no session signal says which host is running; pass --platform"
    elif signals["claude_installed"]:
        platform, reason = "claude-code", "only Claude Code is installed"
    elif signals["codex_installed"]:
        platform, reason = "codex", "only Codex is installed"
    else:
        platform, reason = "unknown", "no platform signal found"
    return {"platform": platform, "reason": reason, "signals": signals}


def detect_platform() -> str:
    return detect_platform_details()["platform"]


def default_home(platform: str) -> Path:
    if platform == "codex":
        return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude"))


def _expand(ref: str, base: Path) -> Path:
    if ref.startswith("~"):
        return Path(ref).expanduser()
    path = Path(ref)
    return path if path.is_absolute() else (base / path)


def _entry(scope: str, path: Path, selected: bool = True, note: str = "") -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    imports = []
    for ref in IMPORT_RE.findall(text):
        imports.append({"ref": ref, "exists": _expand(ref, path.parent).is_file()})
    entry = {"scope": scope, "path": str(path), "bytes": path.stat().st_size, "words": len(text.split()),
             "sha256": sha256_file(path), "imports": imports, "effective": selected and bool(text.strip())}
    if note:
        entry["note"] = note
    return entry


def _toml_list(config: Path, key: str) -> Optional[list[str]]:
    if not config.is_file():
        return None
    match = re.search(rf"(?m)^\s*{key}\s*=\s*\[(.*?)\]", config.read_text(encoding="utf-8", errors="replace"), re.S)
    if not match:
        return None
    return re.findall(r'"([^"]*)"', match.group(1))


def instruction_chain(platform: str, home: Path, workspace: Optional[Path]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Instruction files in load order and a note on how far the inspection reached.

    Each entry says whether it is effective. Codex picks one file per directory
    (AGENTS.override.md before AGENTS.md before configured fallbacks); Claude Code loads
    every CLAUDE.md and CLAUDE.local.md from the filesystem root down to the workspace.
    """
    chain: list[dict[str, Any]] = []
    scope: dict[str, Any] = {}
    if platform == "codex":
        selected = None
        for name in ("AGENTS.override.md", "AGENTS.md"):
            path = home / name
            if path.is_file():
                nonempty = bool(path.read_text(encoding="utf-8", errors="replace").strip())
                is_sel = selected is None and nonempty
                chain.append(_entry("global", path, is_sel, "" if is_sel else "present but not used: an earlier file in the override order wins or it is empty"))
                if is_sel:
                    selected = path
        if workspace:
            markers = _toml_list(home / "config.toml", "project_root_markers")
            markers = [".git"] if markers is None else markers
            fallbacks = [f for f in (_toml_list(home / "config.toml", "project_doc_fallback_filenames") or [])
                         if f and f not in (".", "..") and "/" not in f]
            root = None
            if markers:
                for candidate in [workspace, *workspace.parents]:
                    if any((candidate / m).exists() for m in markers):
                        root = candidate
                        break
            dirs = [workspace] if root is None else [d for d in reversed([workspace, *workspace.parents]) if is_within(d, root)]
            names = ["AGENTS.override.md", "AGENTS.md", *[f for f in fallbacks if f not in ("AGENTS.override.md", "AGENTS.md")]]
            for directory in dirs:
                found = [directory / n for n in names if (directory / n).is_file()]
                for i, path in enumerate(found):
                    chain.append(_entry("project", path, i == 0, "" if i == 0 else f"shadowed by {found[0].name} in the same directory"))
            scope = {"project_root": str(root) if root else None, "root_markers": markers, "directories_inspected": [str(d) for d in dirs],
                     "not_inspected": "directories below the workspace, which Codex reads only when the working directory is inside them"}
    elif platform == "cowork":
        if workspace and (workspace / "CLAUDE.md").is_file():
            chain.append(_entry("folder-contract", workspace / "CLAUDE.md"))
            text = (workspace / "CLAUDE.md").read_text(encoding="utf-8", errors="replace")
            for item in sorted(workspace.glob("*.md")):
                if item.name != "CLAUDE.md" and item.name in text:
                    chain.append(_entry("folder-companion", item))
        scope = {"not_inspected": "app-level global instructions live in the Cowork app settings, not on disk"}
    else:
        managed = MANAGED_CLAUDE_MD.get(sys.platform)
        if managed and managed.is_file():
            chain.append(_entry("managed", managed))
        if (home / "CLAUDE.md").is_file():
            chain.append(_entry("user", home / "CLAUDE.md"))
        if workspace:
            dirs = list(reversed([workspace, *workspace.parents]))[1:]  # filesystem root excluded
            for directory in dirs:
                label = "project" if directory == workspace else "ancestor"
                for name in ("CLAUDE.md", ".claude/CLAUDE.md", "CLAUDE.local.md"):
                    path = directory / name
                    if name == ".claude/CLAUDE.md" and directory != workspace:
                        continue
                    if path.is_file() and path.resolve() != (home / "CLAUDE.md").resolve():
                        chain.append(_entry(label if name != "CLAUDE.local.md" else "local", path))
            scope = {"directories_inspected": [str(d) for d in dirs],
                     "not_inspected": "nested CLAUDE.md files below the workspace, which load only when files there are read"}
    return chain, scope


MODEL_FIELDS = {"claude-code": ("model", "effortLevel"),
                "codex": ("model", "model_reasoning_effort", "model_provider", "model_verbosity")}


def model_settings(platform: str, path: Path) -> dict[str, Any]:
    """Configured model and effort only, from an explicit allowlist of non-sensitive top-level fields.

    Short plain strings only; env, auth, provider credentials and every other value stay unread.
    """
    fields = MODEL_FIELDS.get("codex" if platform == "codex" else "claude-code")
    found: dict[str, str] = {}
    if not path.is_file():
        return {"source": str(path), "exists": False, "values": found}
    if platform == "codex":
        for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = raw.split("#", 1)[0].strip()
            if line.startswith("["):
                break  # top-level keys only; profiles and tables are not read
            match = re.match(r'^([A-Za-z_]+)\s*=\s*"([^"]{1,80})"\s*$', line)
            if match and match.group(1) in fields:
                found[match.group(1)] = match.group(2)
    else:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"source": str(path), "exists": True, "parse_error": True, "values": found}
        for key in fields:
            value = data.get(key) if isinstance(data, dict) else None
            if isinstance(value, str) and 0 < len(value) <= 80:
                found[key] = value
    safe = {k: v for k, v in found.items() if re.match(r"^[A-Za-z0-9._:/\[\]-]+$", v) and not SECRET_VALUE.search(v)}
    return {"source": str(path), "exists": True, "values": safe, "allowlist": list(fields)}


def json_keys(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"exists": False}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"exists": True, "parse_error": True}
    keys = list(data) if isinstance(data, dict) else []
    return {"exists": True, "keys": redact_keys(keys)}


def toml_keys(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"exists": False}
    sections: list[str] = []
    keys: list[str] = []
    section = ""
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        header = re.match(r"^\[\[?([^\]]+)\]\]?$", line)
        if header:
            section = header.group(1).strip()
            sections.append(section)
            continue
        key = re.match(r"^([A-Za-z0-9_.\"-]+)\s*=", line)
        if key:
            name = key.group(1).strip('"')
            keys.append(f"{section}.{name}" if section else name)
    return {"exists": True, "sections": redact_keys(sorted(set(sections))), "keys": redact_keys(keys)}


def hooks_summary(settings: Path) -> list[dict[str, Any]]:
    """Event, matcher and program name of each configured hook. Arguments are not recorded."""
    if not settings.is_file():
        return []
    try:
        data = json.loads(settings.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [{"error": f"unparseable {settings.name}"}]
    out = []
    for event, groups in (data.get("hooks") or {}).items():
        for group in groups if isinstance(groups, list) else []:
            for hook in group.get("hooks", []) if isinstance(group, dict) else []:
                command = str(hook.get("command", ""))
                program = Path(command.split()[0]).name if command.split() else hook.get("type", "")
                out.append({"event": event, "matcher": group.get("matcher", ""), "program": program})
    return out


def skills_in(root: Path) -> list[str]:
    if not root.is_dir():
        return []
    return sorted(p.parent.name for p in root.glob("*/SKILL.md")) + sorted(
        f".system/{p.parent.name}" for p in root.glob(".system/*/SKILL.md"))


def claude_plugins(home: Path) -> list[dict[str, Any]]:
    registry = home / "plugins" / "installed_plugins.json"
    enabled: dict[str, Any] = {}
    settings = home / "settings.json"
    if settings.is_file():
        try:
            enabled = json.loads(settings.read_text(encoding="utf-8")).get("enabledPlugins") or {}
        except (OSError, json.JSONDecodeError):
            enabled = {}
    plugins: list[dict[str, Any]] = []
    if registry.is_file():
        try:
            payload = json.loads(registry.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            payload = {}
        for key, installs in (payload.get("plugins") or {}).items():
            for install in installs if isinstance(installs, list) else []:
                name, _, market = key.partition("@")
                plugins.append({"name": name, "marketplace": market or None, "version": install.get("version"),
                                "scope": install.get("scope"), "enabled": enabled.get(key),
                                "path": install.get("installPath")})
    else:
        for root in (home / "plugins" / "cache", home / "plugins" / "synced"):
            for manifest in sorted(root.glob("*/*/*/.claude-plugin/plugin.json")) + sorted(root.glob("*/.claude-plugin/plugin.json")):
                try:
                    data = json.loads(manifest.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    continue
                plugins.append({"name": data.get("name"), "version": data.get("version"), "path": str(manifest.parents[1])})
    return sorted(plugins, key=lambda p: (str(p["name"]), str(p.get("version"))))


def codex_plugins(home: Path) -> list[dict[str, Any]]:
    plugins = []
    cache = home / "plugins" / "cache"
    for version_dir in sorted(cache.glob("*/*/*")):
        if version_dir.is_dir():
            plugins.append({"marketplace": version_dir.parent.parent.name, "name": version_dir.parent.name,
                            "version": version_dir.name, "path": str(version_dir)})
    return plugins


def codex_surfaces(home: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """Hook and MCP names Codex declares in config.toml. Values are never read into the report."""
    config = home / "config.toml"
    sections = toml_keys(config).get("sections", []) if config.is_file() else []
    keys = toml_keys(config).get("keys", []) if config.is_file() else []
    servers = sorted({s.split(".")[1] for s in sections if s.startswith("mcp_servers.") and len(s.split(".")) >= 2})
    hook_items = sorted({x for x in sections + keys if x == "hooks" or x.startswith("hooks.")})
    extra = [str(p) for p in (home / "hooks.json", home / "hooks") if p.exists()]
    hooks = {"inspected": [str(config)] if config.is_file() else [], "found": hook_items,
             "present_not_parsed": extra,
             "not_inspected": "project .codex/config.toml files and any host-managed hook trust store"}
    mcp = {"inspected": [str(config)] if config.is_file() else [], "found": servers,
           "not_inspected": "project .codex/config.toml files and plugin-provided servers"}
    return hooks, mcp


def mcp_names(*paths: Path) -> list[dict[str, str]]:
    out = []
    for path in paths:
        if path.is_file():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            servers = data.get("mcpServers", data) if isinstance(data, dict) else {}
            for name in servers if isinstance(servers, dict) else []:
                out.append({"name": name, "source": str(path)})
    return out


def chain_findings(chain: list[dict[str, Any]], commands: Optional[set[str]] = None) -> list[dict[str, Any]]:
    """Instruction-chain findings. `commands` holds names the host can invoke as `/name`;
    None means the registry was not inspected, so command references stay unverified."""
    findings = []
    for entry in chain:
        path = Path(entry["path"])
        text = path.read_text(encoding="utf-8", errors="replace")
        for imp in entry["imports"]:
            if not imp["exists"]:
                findings.append({"type": "dead-import", "file": str(path), "ref": imp["ref"]})
        for ref in PATH_RE.findall(text):
            if "*" in ref or "<" in ref or "$" in ref or TEMPLATE_RE.search(ref):
                continue
            target = Path(ref).expanduser()
            if target.exists():
                continue
            if COMMAND_RE.fullmatch(ref):
                if commands is None or ref[1:] not in commands:
                    findings.append({"type": "unverified-command-reference", "file": str(path), "ref": ref})
                continue
            findings.append({"type": "dead-path-reference", "file": str(path), "ref": ref})
        for line_no, line in enumerate(text.splitlines(), 1):
            if PLACEHOLDER_RE.search(line):
                findings.append({"type": "placeholder", "file": str(path), "line": line_no})
    return findings


def audit(platform: str, home: Path, workspace: Optional[Path]) -> dict[str, Any]:
    if platform in ("auto", "ambiguous", "unknown"):
        details = detect_platform_details()
        platform = details["platform"]
        if platform not in ("claude-code", "cowork", "codex"):
            raise HectlError(f"platform is {platform}: {details['reason']}")
    home = home.expanduser().resolve(strict=False)
    ws = workspace.expanduser().resolve(strict=False) if workspace else None
    chain, chain_scope = instruction_chain(platform, home, ws)
    report: dict[str, Any] = {
        "schema_version": 1,
        "generated_at": now_iso(),
        "platform": platform,
        "home": str(home),
        "workspace": str(ws) if ws else None,
        "instruction_chain": chain,
        "instruction_chain_scope": chain_scope,
        "instruction_words_total": sum(e["words"] for e in chain if e["effective"]),
    }
    if platform == "codex":
        report["config"] = toml_keys(home / "config.toml")
        report["model_settings"] = model_settings("codex", home / "config.toml")
        report["skills"] = {"home": skills_in(home / "skills"), "workspace": skills_in(ws / ".codex" / "skills") if ws else []}
        report["plugins"] = codex_plugins(home)
        report["hooks"], report["mcp_servers"] = codex_surfaces(home)
        report["rules_present"] = (home / "rules").is_dir()
        report["memory_present"] = (home / "memories").is_dir()
    else:
        report["model_settings"] = model_settings("claude-code", home / "settings.json")
        report["config"] = {"user": json_keys(home / "settings.json"),
                            "project": json_keys(ws / ".claude" / "settings.json") if ws else {"exists": False},
                            "local": json_keys(ws / ".claude" / "settings.local.json") if ws else {"exists": False}}
        report["skills"] = {"user": skills_in(home / "skills"), "project": skills_in(ws / ".claude" / "skills") if ws else []}
        report["plugins"] = claude_plugins(home)
        hook_sources = [home / "settings.json"] + ([ws / ".claude" / "settings.json", ws / ".claude" / "settings.local.json"] if ws else [])
        report["hooks"] = {"inspected": [str(p) for p in hook_sources if p.is_file()],
                           "found": [h for p in hook_sources for h in hooks_summary(p)],
                           "not_inspected": "managed policy settings and hooks shipped inside installed plugins"}
        mcp_sources = [ws / ".mcp.json"] if ws else []
        report["mcp_servers"] = {"inspected": [str(p) for p in mcp_sources if p.is_file()],
                                 "found": mcp_names(*mcp_sources),
                                 "not_inspected": "user and local MCP scopes in ~/.claude.json (holds credentials, not read) and plugin-provided servers"}
        report["agents"] = sorted(p.stem for p in (home / "agents").glob("*.md"))
        report["commands"] = sorted(p.stem for p in (home / "commands").glob("*.md"))
        report["scheduled_tasks"] = sorted(p.parent.name for p in (home / "scheduled-tasks").glob("*/SKILL.md"))
        report["memory_present"] = any((home / "projects").glob("*/memory/MEMORY.md")) if (home / "projects").is_dir() else False
    names: dict[str, int] = {}
    for group in report["skills"].values():
        for name in group:
            names[name] = names.get(name, 0) + 1
    commands = set(report.get("commands", [])) | set(names)
    if platform == "codex":
        commands |= {p.stem for p in (home / "prompts").glob("*.md")}
    for plugin in report.get("plugins", []):
        if plugin.get("enabled") is not False and plugin.get("name") and plugin.get("path"):
            commands |= {f"{plugin['name']}:{n}" for n in skills_in(Path(plugin["path"]) / "skills")}
            commands |= {f"{plugin['name']}:{c.stem}" for c in (Path(plugin["path"]) / "commands").glob("*.md")}
    findings = chain_findings(chain, commands)
    findings += [{"type": "duplicate-skill-name", "name": n} for n, c in sorted(names.items()) if c > 1]
    if platform == "cowork" and ws and not (ws / "CLAUDE.md").is_file():
        findings.append({"type": "missing-folder-contract", "file": str(ws / "CLAUDE.md")})
    if not chain:
        findings.append({"type": "empty-instruction-chain"})
    report["verified_findings"] = findings
    return report
