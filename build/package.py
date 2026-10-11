#!/usr/bin/env python3
"""Build host packages of Curiosity Kit from one source revision.

Outputs (default build/out/):
  claude-code/curiosity-kit/                    full plugin for Claude Code (--plugin-dir or a marketplace)
  codex/curiosity-kit/                          full plugin for Codex, with per-skill agents/openai.yaml
  test/<host>/<skill>/                  one-skill plugin per skill and host, for isolation tests
  build-manifest.json                   sha256 of every emitted file and the validation results

The build only copies and generates metadata. It never installs anything.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "skills" / "harness-engineering" / "scripts"))
from hecore.common import sha256_file, write_json  # noqa: E402
from hecore.packaging import check_plugin  # noqa: E402

IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", ".pytest_cache")
HOSTS = {"claude-code": ".claude-plugin", "codex": ".codex-plugin"}


def source_provenance(repo: Path) -> tuple[str | None, bool | None]:
    """Read Git identity without refreshing the index or running fsmonitor."""
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    git = ["git", "-c", "core.fsmonitor=false", "-c", "core.untrackedCache=false", "-C", str(repo)]
    try:
        rev = subprocess.run([*git, "rev-parse", "--verify", "-q", "HEAD"],
                             capture_output=True, text=True, env=env)
        state = subprocess.run([*git, "status", "--porcelain"],
                               capture_output=True, text=True, env=env)
    except OSError:
        return None, None
    revision = rev.stdout.strip() if rev.returncode == 0 else None
    dirty = bool(state.stdout.strip()) if state.returncode == 0 else None
    return revision, dirty


def yaml_quote(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def openai_yaml(meta: dict) -> str:
    return (
        "interface:\n"
        f"  display_name: {yaml_quote(meta['display_name'])}\n"
        f"  short_description: {yaml_quote(meta['short_description'])}\n"
        f"  default_prompt: {yaml_quote(meta['default_prompt'])}\n"
        "\npolicy:\n"
        f"  allow_implicit_invocation: {'true' if meta['allow_implicit_invocation'] else 'false'}\n"
    )


def emit(host: str, target: Path, skills: list[str], name: str | None = None) -> None:
    if target.exists():
        shutil.rmtree(target)
    manifest = json.loads((REPO / "adapters" / host / "plugin.json").read_text(encoding="utf-8"))
    if name:
        manifest["name"] = name
        manifest["description"] = f"Isolation test package containing only {skills[0]}."
    write_json(target / HOSTS[host] / "plugin.json", manifest)
    shutil.copyfile(REPO / "LICENSE", target / "LICENSE")
    metadata = json.loads((REPO / "adapters" / "codex" / "skill-metadata.json").read_text(encoding="utf-8"))
    for skill in skills:
        shutil.copytree(REPO / "skills" / skill, target / "skills" / skill, ignore=IGNORE)
        if host == "codex":
            # Claude's explicit-only flag is kept in the shared source. Codex
            # carries that policy in agents/openai.yaml instead of frontmatter.
            entry = target / "skills" / skill / "SKILL.md"
            lines = entry.read_bytes().decode("utf-8").splitlines(keepends=True)
            if lines and lines[0].strip() == "---":
                end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), 0)
                if end and any(line.startswith("disable-model-invocation:") for line in lines[1:end]):
                    header = [line for line in lines[1:end] if not line.startswith("disable-model-invocation:")]
                    entry.write_bytes("".join([lines[0], *header, *lines[end:]]).encode("utf-8"))
            if skill not in metadata:
                raise SystemExit(f"adapters/codex/skill-metadata.json has no entry for {skill}")
            out = target / "skills" / skill / "agents" / "openai.yaml"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(openai_yaml(metadata[skill]), encoding="utf-8")
    # Domain logic travels with the owning skill. Register the default hook file
    # once; an extra manifest hooks path would double-load it in Claude Code.
    hook_metadata = REPO / "adapters" / host / "hooks.json"
    if hook_metadata.is_file():
        declarations = json.loads(hook_metadata.read_text(encoding="utf-8"))
        events = {}
        for skill in skills:
            for event, handlers in declarations.get(skill, {}).items():
                script = target / "skills" / skill / "scripts" / "loopkit_hook.py"
                if not script.is_file():
                    raise SystemExit(f"{skill}: declared hook script is missing")
                events.setdefault(event, []).extend(handlers)
        if events:
            if "hooks" in manifest:
                raise SystemExit("Default hooks/hooks.json and explicit manifest hooks cannot both be emitted")
            write_json(target / "hooks" / "hooks.json", {"hooks": events})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=str(REPO / "build" / "out"))
    parser.add_argument("--skill", action="append", help="limit to these skills (default: every skill in skills/)")
    args = parser.parse_args()
    revision, dirty = source_provenance(REPO)
    out = Path(args.out).resolve()
    skills = args.skill or sorted(p.parent.name for p in (REPO / "skills").glob("*/SKILL.md"))
    results = []
    targets = []
    for host in HOSTS:
        full = out / host / "curiosity-kit"
        emit(host, full, skills)
        targets.append((host, full))
        for skill in skills:
            test = out / "test" / host / skill
            emit(host, test, [skill], name=f"curiosity-kit-{skill}-test")
            targets.append((host, test))
    files = {}
    for host, target in targets:
        result = check_plugin(target, host)
        results.append({"host": host, "path": str(target.relative_to(out)), "ok": result["ok"], "errors": result["errors"]})
        for path in sorted(target.rglob("*")):
            if path.is_file():
                files[str(path.relative_to(out))] = sha256_file(path)
    report = {"schema_version": 1, "source_revision": revision, "source_dirty": dirty, "skills": skills,
              "packages": results, "files": files}
    write_json(out / "build-manifest.json", report)
    print(json.dumps({"out": str(out), "packages": results, "files": len(files), "source_revision": revision,
                      "source_dirty": dirty}, indent=2))
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
