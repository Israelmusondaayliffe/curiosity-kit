"""Skill and plugin validation for Claude Code and Codex, parity, listing budget."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .common import frontmatter, sha256_file

NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9]|-(?!-)){0,62}[a-z0-9]$|^[a-z0-9]$")
CODEX_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
DESC_MAX = 1024
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
CODEX_VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+codex\.\d+)?$")
LINK_RE = re.compile(r"\]\((?!https?:|mailto:|#)([^)\s]+?)(?:#[^)]*)?\)")
TICK_PATH_RE = re.compile(r"`((?:playbooks|references|scripts|assets)/[^`\s]+)`")
PLACEHOLDER_RE = re.compile(r"\[(?:TODO|TBD|PLACEHOLDER)[:\]]|\[fill:|\{\{[^}]+\}\}|__REPLACE_ME__|lorem ipsum", re.IGNORECASE)
DESC_CAP = 1536
EXCLUDE = {".DS_Store", "__pycache__", ".git", ".pytest_cache"}


def _yaml_scalars(path: Path) -> dict[str, str]:
    """Flatten a small YAML file into dotted keys. Enough for agents/openai.yaml."""
    out: dict[str, str] = {}
    stack: list[tuple[int, str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        match = re.match(r"^\s*([A-Za-z0-9_-]+):\s*(.*)$", raw)
        if not match:
            continue
        while stack and stack[-1][0] >= indent:
            stack.pop()
        key = ".".join([s[1] for s in stack] + [match.group(1)])
        value = match.group(2).strip()
        if value:
            out[key] = value.strip("\"'")
        else:
            stack.append((indent, match.group(1)))
    return out


def check_skill(skill_dir: Path, host: str = "portable") -> dict[str, Any]:
    """Validate a skill. portable applies the shared Agent Skills limits; codex adds the
    Codex validator's frontmatter allowlist; claude-code adds the listing cap for when_to_use."""
    skill_dir = Path(skill_dir).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    entry = skill_dir / "SKILL.md"
    if not entry.is_file():
        return {"skill": str(skill_dir), "ok": False, "errors": ["SKILL.md missing"], "warnings": []}
    text = entry.read_text(encoding="utf-8")
    meta, body_start = frontmatter(text)
    if not meta:
        errors.append("frontmatter missing or unterminated")
    name = meta.get("name", "")
    if not NAME_RE.match(name):
        errors.append(f"name must be hyphen-case, 1 to 64 characters, no leading, trailing or double hyphens, got {name!r}")
    elif name != skill_dir.name:
        errors.append(f"name {name!r} does not match directory {skill_dir.name!r}")
    description = meta.get("description", "")
    listing = description + (" - " + meta["when_to_use"] if meta.get("when_to_use") else "")
    if not description.strip():
        errors.append("description missing")
    else:
        if len(description) > DESC_MAX:
            errors.append(f"description is {len(description)} characters; the shared skill format and the Codex validator allow {DESC_MAX}")
        if "<" in description or ">" in description:
            errors.append("description cannot contain angle brackets (Codex validator)")
        if len(listing) > DESC_CAP:
            errors.append(f"description plus when_to_use is {len(listing)} characters; Claude Code truncates listing entries at {DESC_CAP}")
    if host == "codex":
        extra = sorted(set(meta) - CODEX_KEYS)
        if extra:
            errors.append(f"frontmatter keys not accepted by the Codex validator: {', '.join(extra)}; move host policy to agents/openai.yaml")
    dmi = meta.get("disable-model-invocation", "").lower() == "true"
    for md in sorted(skill_dir.rglob("*.md")):
        if EXCLUDE & set(md.parts):
            continue
        content = md.read_text(encoding="utf-8", errors="replace")
        in_fence = False
        for number, line in enumerate(content.splitlines(), 1):
            if line.lstrip().startswith(("```", "~~~")):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for ref in LINK_RE.findall(line):
                if not (md.parent / ref).exists():
                    errors.append(f"{md.relative_to(skill_dir)}:{number}: broken link {ref}")
            for ref in TICK_PATH_RE.findall(line):
                if "<" in ref or "*" in ref:
                    continue
                if not (skill_dir / ref).exists() and not (md.parent / ref).exists():
                    errors.append(f"{md.relative_to(skill_dir)}:{number}: missing resource {ref}")
            if PLACEHOLDER_RE.search(line) and "assets" not in md.relative_to(skill_dir).parts[:1]:
                errors.append(f"{md.relative_to(skill_dir)}:{number}: placeholder text")
    yaml_path = skill_dir / "agents" / "openai.yaml"
    if yaml_path.is_file():
        data = _yaml_scalars(yaml_path)
        implicit = data.get("policy.allow_implicit_invocation", "true").lower() == "true"
        if dmi and implicit:
            errors.append("disable-model-invocation is true but openai.yaml allows implicit invocation")
        if not dmi and not implicit:
            warnings.append("openai.yaml disables implicit invocation while Claude Code allows it")
    return {"skill": name or skill_dir.name, "ok": not errors, "errors": errors, "warnings": warnings,
            "listing_chars": len(listing), "model_invocable": not dmi}


def _component_paths(manifest: dict[str, Any], key: str) -> list[str]:
    value = manifest.get(key)
    if value is None:
        return []
    return [value] if isinstance(value, str) else [v for v in value if isinstance(v, str)]


def check_plugin(plugin_dir: Path, host: str) -> dict[str, Any]:
    plugin_dir = Path(plugin_dir)
    errors: list[str] = []
    folder = ".claude-plugin" if host == "claude-code" else ".codex-plugin"
    manifest_path = plugin_dir / folder / "plugin.json"
    if not manifest_path.is_file():
        return {"plugin": str(plugin_dir), "host": host, "ok": False, "errors": [f"{folder}/plugin.json missing"], "skills": []}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"plugin": str(plugin_dir), "host": host, "ok": False, "errors": [f"manifest JSON: {exc}"], "skills": []}
    name = manifest.get("name", "")
    if not NAME_RE.match(str(name)):
        errors.append(f"plugin name must be kebab case, got {name!r}")
    version = str(manifest.get("version", ""))
    pattern = CODEX_VERSION_RE if host == "codex" else SEMVER_RE
    if not pattern.match(version):
        errors.append(f"version {version!r} is not valid for {host}")
    for key in ("skills", "agents", "commands", "hooks"):
        for rel in _component_paths(manifest, key):
            if not (plugin_dir / rel).exists():
                errors.append(f"{key} path {rel} has no files")
    skill_roots = _component_paths(manifest, "skills") or ["skills"]
    skills = []
    for root in skill_roots:
        base = plugin_dir / root
        dirs = [base] if (base / "SKILL.md").is_file() else sorted(p.parent for p in base.glob("*/SKILL.md"))
        for skill_dir in dirs:
            result = check_skill(skill_dir, host)
            if host == "codex" and not (skill_dir / "agents" / "openai.yaml").is_file():
                result["errors"].append("Codex skill lacks agents/openai.yaml")
                result["ok"] = False
            skills.append(result)
            errors.extend(f"{result['skill']}: {e}" for e in result["errors"])
    if not skills:
        errors.append("plugin contains no skills")
    hooks_file = plugin_dir / "hooks" / "hooks.json"
    if hooks_file.is_file():
        try:
            json.loads(hooks_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"hooks/hooks.json: {exc}")
    return {"plugin": name, "version": version, "host": host, "ok": not errors, "errors": errors, "skills": skills}


def file_map(root: Path) -> dict[str, str]:
    out = {}
    for path in sorted(Path(root).rglob("*")):
        if path.is_file() and not (EXCLUDE & set(path.parts)):
            out[path.relative_to(root).as_posix()] = sha256_file(path)
    return out


def parity(source: Path, installed: Path) -> dict[str, Any]:
    a, b = file_map(source), file_map(installed)
    missing = sorted(set(a) - set(b))
    extra = sorted(set(b) - set(a))
    changed = sorted(k for k in set(a) & set(b) if a[k] != b[k])
    return {"source": str(source), "installed": str(installed), "files": len(a),
            "parity": not (missing or extra or changed), "missing": missing, "extra": extra, "changed": changed}


def listing_budget(paths: list[Path], context_tokens: int, namespace: str = "") -> dict[str, Any]:
    entries = []
    for path in paths:
        path = Path(path)
        skill_dirs = [path] if (path / "SKILL.md").is_file() else sorted(p.parent for p in path.rglob("SKILL.md") if not (EXCLUDE & set(p.parts)))
        for skill_dir in skill_dirs:
            meta, _ = frontmatter((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
            if meta.get("disable-model-invocation", "").lower() == "true":
                entries.append({"skill": meta.get("name", skill_dir.name), "listed": False, "chars": 0})
                continue
            name = (namespace + ":" if namespace else "") + meta.get("name", skill_dir.name)
            text = meta.get("description", "") + (" - " + meta["when_to_use"] if meta.get("when_to_use") else "")
            entries.append({"skill": name, "listed": True, "description_chars": len(text),
                            "truncated": len(text) > DESC_CAP, "chars": len(name) + 4 + min(len(text), DESC_CAP)})
    total = sum(e["chars"] for e in entries)
    budget = int(context_tokens * 4 * 0.01)
    return {"context_tokens": context_tokens, "budget_chars": budget, "total_chars": total,
            "share_of_budget": round(total / budget, 4) if budget else None, "entries": entries,
            "note": "Estimate from the documented rule: 1% of context at 4 characters per token, 1,536 characters per entry. Other installed skills share the same budget."}
