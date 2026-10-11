#!/usr/bin/env python3
"""hectl: the Harness Engineering command line. Standard library only, Python 3.9+.

Read-only unless a subcommand says otherwise: `apply --mode apply`, `rollback`,
`cleanup --apply` and `run` write, and each refuses without its own preconditions.
Run `python3 hectl.py <command> --help` for the arguments of one command.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hecore import audit as audit_mod  # noqa: E402
from hecore import cleanup as cleanup_mod  # noqa: E402
from hecore import packaging, plans, runstate, scan, unslop  # noqa: E402
from hecore.common import HectlError, load_json, write_json  # noqa: E402

SKILL_ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "playbooks/research.md", "playbooks/skill-evaluation.md", "playbooks/skill-repair.md", "playbooks/meta-audit.md",
    "references/skill-design.md", "references/review-methods.md", "references/evaluation-contract.md",
    "references/review-interface.md", "references/authoring-sources.md",
    "references/meta-audit/harness.md", "references/meta-audit/security.md", "references/meta-audit/work-system.md",
    "scripts/hecore/authoring.py", "scripts/hecore/evaluation.py", "scripts/hecore/review.py", "assets/review.html",
    "SKILL.md",
    "playbooks/interview.md", "playbooks/audit.md", "playbooks/plan.md", "playbooks/build.md", "playbooks/run.md",
    "playbooks/verification.md", "playbooks/maintenance.md", "playbooks/instruction-files.md",
    "playbooks/context-subtraction.md", "playbooks/skill-authoring.md", "playbooks/plugin-authoring.md",
    "playbooks/model-prompts.md", "playbooks/unslop-repair.md",
    "references/platforms.md", "references/architecture.md", "references/context-doctrine.md",
    "references/subtraction-protocol.md", "references/approvals.md", "references/proof.md",
    "references/interview-branches.md", "references/unslop-method.md",
    "assets/templates/operations-plan.json", "assets/templates/profile.json",
    "assets/templates/claude-global.md", "assets/templates/claude-project.md", "assets/templates/cowork-contract.md",
    "assets/templates/agents-global.md", "assets/templates/agents-workspace.md", "assets/templates/agents-project.md",
    "assets/templates/unslop-ledger.json", "assets/templates/verifier-receipt.json",
]


def emit(payload, output=None) -> None:
    if output:
        write_json(Path(output), payload)
    print(json.dumps(payload, indent=2))


def cmd_selfcheck(args) -> int:
    missing = [rel for rel in REQUIRED if not (SKILL_ROOT / rel).is_file()]
    result = packaging.check_skill(SKILL_ROOT)
    templates = []
    for name in ("operations-plan.json", "profile.json", "unslop-ledger.json", "verifier-receipt.json"):
        path = SKILL_ROOT / "assets" / "templates" / name
        if path.is_file():
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                templates.append(f"{name}: {exc}")
    ok = not missing and result["ok"] and not templates
    emit({"ok": ok, "skill_root": str(SKILL_ROOT), "missing_resources": missing,
          "link_errors": result["errors"], "template_errors": templates, "warnings": result["warnings"]})
    return 0 if ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hectl", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (("author", "materialize or check an authored skill"), ("eval", "record and compare evidence; guarded candidate application"), ("review", "offline query, history and artifact review")):
        sub.add_parser(name, help=help_text, add_help=False)

    p = sub.add_parser("detect", help="Detect the platform of this environment")
    p.set_defaults(func=lambda a: emit(audit_mod.detect_platform_details()) or 0)

    p = sub.add_parser("audit", help="Read-only inventory of a harness")
    p.add_argument("--platform", default="auto", choices=["auto", "claude-code", "cowork", "codex"])
    p.add_argument("--home", help="config home; defaults per platform")
    p.add_argument("--workspace", help="workspace, project or connected folder")
    p.add_argument("--output")

    def run_audit(a):
        platform = audit_mod.detect_platform() if a.platform == "auto" else a.platform
        home = Path(a.home) if a.home else audit_mod.default_home(platform)
        emit(audit_mod.audit(platform, home, Path(a.workspace) if a.workspace else None), a.output)
        return 0
    p.set_defaults(func=run_audit)

    for name, validator in (("profile", plans.validate_profile), ("plan", plans.validate_plan)):
        p = sub.add_parser(name, help=f"Validate a {name} JSON file")
        p.add_argument("path")
        if name == "profile":
            p.add_argument("--require-confirmed", action="store_true",
                           help="also require status confirmed; use before planning from a profile")

        def run_validate(a, validator=validator, name=name):
            data = load_json(Path(a.path))
            errors = validator(data)
            if name == "profile" and getattr(a, "require_confirmed", False) and isinstance(data, dict) and data.get("status") != "confirmed":
                errors.append("profile is a draft; a draft is never approval to plan or build")
            emit({"valid": not errors, "kind": name, "errors": errors})
            return 0 if not errors else 1
        p.set_defaults(func=run_validate)

    p = sub.add_parser("apply", help="Dry-run or apply approved plan groups")
    p.add_argument("plan")
    p.add_argument("--mode", choices=["dry-run", "apply"], default="dry-run")
    p.add_argument("--approved", action="append", required=True, help="approval group; repeat for several")
    p.add_argument("--receipt", required=True)
    p.add_argument("--backup-dir")
    p.add_argument("--manifest")
    p.set_defaults(func=lambda a: emit(plans.apply_plan(load_json(Path(a.plan)), a.mode, set(a.approved), Path(a.receipt),
                                                        Path(a.backup_dir) if a.backup_dir else None,
                                                        Path(a.manifest) if a.manifest else None)) or 0)

    p = sub.add_parser("rollback", help="Restore files from an apply manifest")
    p.add_argument("manifest")
    p.add_argument("--receipt", required=True)
    p.set_defaults(func=lambda a: emit(plans.rollback(Path(a.manifest), Path(a.receipt))) or 0)

    p = sub.add_parser("context-scan", help="Scan persistent context for over-constraint")
    p.add_argument("paths", nargs="+")
    p.add_argument("--long-run", action="store_true", help="the text drives a long unattended run")
    p.add_argument("--verification-policy", choices=["review-all", "keep-one"], default="review-all",
                   help="review-all flags every verification line; keep-one keeps the first test-your-work line")
    p.add_argument("--output")

    def run_scan(a):
        result = scan.scan_paths(a.paths, a.long_run, a.verification_policy)
        emit(result, a.output)
        return 1 if result["counts"]["FAIL"] else 0
    p.set_defaults(func=run_scan)

    p = sub.add_parser("skill-check", help="Validate one or more skill directories")
    p.add_argument("dirs", nargs="+")
    p.add_argument("--host", default="portable", choices=["portable", "claude-code", "codex"])

    def run_skill(a):
        results = [packaging.check_skill(Path(d), a.host) for d in a.dirs]
        emit({"ok": all(r["ok"] for r in results), "skills": results})
        return 0 if all(r["ok"] for r in results) else 1
    p.set_defaults(func=run_skill)

    p = sub.add_parser("plugin-check", help="Validate a plugin directory for one host")
    p.add_argument("dir")
    p.add_argument("--host", required=True, choices=["claude-code", "codex"])
    p.set_defaults(func=lambda a: (lambda r: emit(r) or (0 if r["ok"] else 1))(packaging.check_plugin(Path(a.dir), a.host)))

    p = sub.add_parser("parity", help="Compare a source tree with its installed copy")
    p.add_argument("source")
    p.add_argument("installed")
    p.set_defaults(func=lambda a: (lambda r: emit(r) or (0 if r["parity"] else 1))(packaging.parity(Path(a.source), Path(a.installed))))

    p = sub.add_parser("listing-budget", help="Estimate skill listing characters against a context size")
    p.add_argument("paths", nargs="+")
    p.add_argument("--context-tokens", type=int, default=200000)
    p.add_argument("--namespace", default="")
    p.set_defaults(func=lambda a: emit(packaging.listing_budget([Path(x) for x in a.paths], a.context_tokens, a.namespace)) or 0)

    p = sub.add_parser("selfcheck", help="Confirm this skill's own resources are present and linked")
    p.set_defaults(func=cmd_selfcheck)

    p = sub.add_parser("cleanup", help="Guarded stale-data cleanup; dry-run unless --apply")
    p.add_argument("--host", required=True, choices=["claude-code", "codex"])
    p.add_argument("--home")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--retain", action="append", default=[], metavar="CATEGORY=DAYS", help="raise a retention floor")
    p.add_argument("--max-candidates", type=int, default=cleanup_mod.MAX_CANDIDATES)
    p.add_argument("--max-bytes", type=int, default=cleanup_mod.MAX_BYTES)
    p.add_argument("--receipt-dir")
    p.add_argument("--reference-file", action="append", default=[], help="extra continuity file whose paths stay protected")
    p.add_argument("--installed-json", help="Codex installed-plugin JSON instead of calling `codex plugin list --json`")
    p.add_argument("--approved-receipt", help="with --apply: the dry-run receipt whose exact candidates the user approved; nothing else is deleted")

    def run_cleanup(a):
        overrides = {}
        for item in a.retain:
            key, _, value = item.partition("=")
            overrides[key] = int(value)
        code, receipt = cleanup_mod.run_cleanup(a.host, a.home, a.apply, overrides, a.max_candidates, a.max_bytes,
                                                Path(a.receipt_dir) if a.receipt_dir else None,
                                                [Path(x) for x in a.reference_file],
                                                Path(a.installed_json) if a.installed_json else None,
                                                approved_receipt=Path(a.approved_receipt) if a.approved_receipt else None)
        summary = {k: receipt.get(k) for k in ("mode", "home", "stop_reason", "receipt", "warnings")}
        summary["candidates"] = len(receipt.get("candidates", []))
        summary["candidate_bytes"] = receipt.get("candidate_bytes")
        summary["deleted"] = len(receipt.get("deleted", []))
        summary["status"] = receipt.get("status")
        summary["unverified"] = len(receipt.get("unverified", []))
        summary["skipped"] = len(receipt.get("skipped", []))
        summary["exit_code"] = code
        emit(summary)
        return code
    p.set_defaults(func=run_cleanup)

    p = sub.add_parser("unslop", help="Unslop detection and repair gates")
    usub = p.add_subparsers(dest="unslop_command", required=True)
    q = usub.add_parser("scan", help="Raw pattern evidence for one file; never edits")
    q.add_argument("path")
    q.add_argument("--output")
    q.set_defaults(func=lambda a: emit(unslop.scan_text(Path(a.path).read_text(encoding="utf-8", errors="replace"), a.path), a.output) or 0)
    q = usub.add_parser("voice", help="Voice signals to preserve during repair")
    q.add_argument("path")
    q.add_argument("--output")
    q.set_defaults(func=lambda a: emit(unslop.voice_profile(Path(a.path).read_text(encoding="utf-8", errors="replace")), a.output) or 0)
    q = usub.add_parser("audit", help="Inventory approved roots with hashes and protected fingerprints")
    q.add_argument("--run-id", required=True)
    q.add_argument("--root", action="append", required=True)
    q.add_argument("--output", required=True)
    q.set_defaults(func=lambda a: (lambda r: print(json.dumps({"status": "audited", "files": len(r["entries"]), "raw_findings": r["raw_findings"], "inventory_sha256": r["inventory_sha256"]})) or 0)(unslop.audit(a.run_id, a.root, Path(a.output))))
    q = usub.add_parser("freeze", help="Freeze an unchanged audit")
    q.add_argument("--audit", required=True)
    q.add_argument("--output", required=True)
    q.set_defaults(func=lambda a: (lambda r: print(json.dumps({"status": "frozen", "files": len(r["entries"]), "inventory_sha256": r["inventory_sha256"]})) or 0)(unslop.freeze(Path(a.audit), Path(a.output))))
    q = usub.add_parser("verify", help="Check a repair candidate against its freeze and ledger")
    q.add_argument("--freeze", required=True)
    q.add_argument("--ledger", required=True)
    q.add_argument("--output", required=True)
    q.set_defaults(func=lambda a: (lambda r: emit(r) or (0 if not r["failures"] else 1))(unslop.verify(Path(a.freeze), Path(a.ledger), Path(a.output))))

    p = sub.add_parser("run", help="Durable state for a bounded run")
    rsub = p.add_subparsers(dest="run_command", required=True)
    q = rsub.add_parser("init")
    q.add_argument("--state", required=True)
    q.add_argument("--run-id", required=True)
    q.add_argument("--objective", required=True)
    q.add_argument("--plan", required=True)
    q.add_argument("--max-steps", type=int, required=True)
    q.add_argument("--max-launches", type=int, default=0)
    q.add_argument("--unresolved", type=int, help="defaults to the plan's outcome.unresolved_before")
    q.set_defaults(func=lambda a: emit(runstate.init(Path(a.state), a.run_id, a.objective, Path(a.plan), a.max_steps, a.max_launches, a.unresolved)) or 0)
    q = rsub.add_parser("step")
    q.add_argument("--state", required=True)
    q.add_argument("--action", required=True)
    q.add_argument("--delta", default="", help="observable target-state change; empty means none")
    q.add_argument("--unresolved", type=int, required=True)
    q.add_argument("--check", action="append", default=[], help="command and result")
    q.add_argument("--launches", type=int, default=0)
    q.add_argument("--group")
    q.set_defaults(func=lambda a: (lambda s: emit(runstate.status(Path(a.state))) or (0 if s["state"] == "running" else 2))(runstate.step(Path(a.state), a.action, a.delta, a.unresolved, a.check, a.launches, a.group)))
    q = rsub.add_parser("stop")
    q.add_argument("--state", required=True)
    q.add_argument("--as", dest="new_state", required=True)
    q.add_argument("--reason", required=True)
    q.add_argument("--verifier-receipt")
    q.set_defaults(func=lambda a: emit(runstate.stop(Path(a.state), a.new_state, a.reason, Path(a.verifier_receipt) if a.verifier_receipt else None)) or 0)
    q = rsub.add_parser("status")
    q.add_argument("--state", required=True)
    q.set_defaults(func=lambda a: emit(runstate.status(Path(a.state))) or 0)
    return parser


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    # New optional routes must not change legacy imports or schema1 commands.
    if argv and argv[0] in {"author", "eval", "review"}:
        import importlib
        module = {"author": "authoring", "eval": "evaluation", "review": "review"}[argv[0]]
        return importlib.import_module("hecore." + module).dispatch(argv[1:])
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except HectlError as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
