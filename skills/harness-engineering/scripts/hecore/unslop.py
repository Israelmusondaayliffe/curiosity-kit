"""Unslop detection, voice profiling, and the audit-freeze-verify gates for harness repair.

Scripts detect and verify. They never rewrite prose; the approved repair is an
agent edit inside a frozen scope. Pattern families and their provenance are in
unslop_patterns.py and references/unslop-method.md.
"""
from __future__ import annotations

import json
import re
import statistics
from collections import Counter
from pathlib import Path
from typing import Any

from .common import HectlError, is_within, load_json, now_iso, sha256_bytes, sha256_file, write_json
from .unslop_patterns import CATALOG, structure_findings

TEXT_SUFFIXES = {".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".py", ".sh"}
FULLY_PROTECTED = {".json", ".jsonl", ".yaml", ".yml", ".toml", ".py", ".sh"}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules", ".venv"}
QUALITY = {"meaning_fidelity": 2.0, "protected_material": 2.0, "scope_authority": 1.5,
           "finding_reconciliation": 1.5, "language_quality": 2.0, "verification_evidence": 1.0}
HARD_GATES = ("fabrication_free", "protected_material_intact", "scope_intact", "terminal_findings",
              "p0_clear", "authored_em_dash_free", "method_self_contained")
FLOOR = 8.0
MAX_WORKERS = 3



FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"`[^`\n]+`")
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
URL = re.compile(r"https?://\S+")
COMMENT = re.compile(r"<!--.*?-->")
QUOTE = re.compile(r"“[^”]*”|\"[^\"\n]{3,}\"")


def prose_lines(text: str, keep_quotes: bool = False) -> list[tuple[int, str]]:
    """Lines of editable prose with protected spans blanked out, keeping line numbers."""
    lines = text.splitlines()
    out = []
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break
    fence = None
    for number in range(start, len(lines)):
        line = lines[number]
        marker = FENCE.match(line)
        if marker:
            token = marker.group(1)[0]
            fence = None if fence == token else (fence or token)
            continue
        if fence or line.lstrip().startswith("|") or line.lstrip().startswith(">"):
            continue
        cleaned = COMMENT.sub(" ", line)
        cleaned = INLINE_CODE.sub(" ", cleaned)
        cleaned = LINK.sub(lambda m: m.group(1), cleaned)
        cleaned = URL.sub(" ", cleaned)
        if not keep_quotes:
            cleaned = QUOTE.sub(" ", cleaned)
        out.append((number + 1, cleaned))
    return out


def scan_text(text: str, path: str = "") -> dict[str, Any]:
    findings = []
    words = 0
    for number, line in prose_lines(text):
        words += len(line.split())
        for pid, category, severity, pattern, guidance in CATALOG:
            for match in pattern.finditer(line):
                findings.append({"id": pid, "category": category, "severity": severity, "file": path,
                                 "line": number, "column": match.start() + 1, "match": match.group(0).strip()[:80],
                                 "guidance": guidance})
    findings += structure_findings(text, path, prose_lines(text), prose_lines(text, keep_quotes=True), words)
    counts = Counter(f["severity"] for f in findings)
    return {"file": path, "prose_words": words, "findings": findings,
            "counts": {k: counts.get(k, 0) for k in ("high", "medium", "low")},
            "per_100_words": round(len(findings) * 100 / words, 2) if words else 0.0,
            "note": "Raw evidence. Classify each match in context; a raw count is never the verdict."}


def voice_profile(text: str) -> dict[str, Any]:
    prose = " ".join(line for _, line in prose_lines(text))
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", prose) if len(s.split()) >= 2]
    lengths = [len(s.split()) for s in sentences]
    tokens = re.findall(r"[A-Za-z']+", prose.lower())
    total = max(len(tokens), 1)
    trigrams = Counter(" ".join(tokens[i:i + 3]) for i in range(len(tokens) - 2))
    signature = [{"phrase": p, "count": c} for p, c in trigrams.most_common(12) if c >= 2]
    return {
        "sentences": len(sentences),
        "sentence_length_mean": round(statistics.mean(lengths), 1) if lengths else 0,
        "sentence_length_stdev": round(statistics.pstdev(lengths), 1) if lengths else 0,
        "short_sentence_share": round(sum(1 for n in lengths if n <= 8) / len(lengths), 2) if lengths else 0,
        "first_person_rate": round(sum(tokens.count(w) for w in ("i", "me", "my", "we", "our")) / total, 4),
        "second_person_rate": round(sum(tokens.count(w) for w in ("you", "your")) / total, 4),
        "contraction_rate": round(sum(1 for t in tokens if "'" in t) / total, 4),
        "questions": prose.count("?"),
        "exclamations": prose.count("!"),
        "signature_phrases": signature,
        "note": "Signals to preserve during repair. Do not invent voice the source does not show.",
    }


def protected_segments(text: str, suffix: str) -> list[str]:
    """Exact material an unslop repair may not change."""
    if suffix in FULLY_PROTECTED:
        return [text]
    segments: list[str] = []
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                segments.append("\n".join(lines[: i + 1]))
                break
    block: list[str] = []
    fence = None
    for line in lines:
        marker = FENCE.match(line)
        if marker:
            token = marker.group(1)[0]
            block.append(line)
            if fence == token:
                segments.append("\n".join(block))
                block, fence = [], None
            elif fence is None:
                fence = token
            continue
        if fence:
            block.append(line)
            continue
        if line.lstrip().startswith("|"):
            segments.append(line.strip())
        segments += INLINE_CODE.findall(line)
        segments += re.findall(r"\]\(([^)]+)\)", line)
        segments += URL.findall(line)
        segments += [q for q in QUOTE.findall(line)]
    return segments


def _inventory(roots: list[Path]) -> list[dict[str, Any]]:
    entries = []
    for root in roots:
        files = [root] if root.is_file() else sorted(root.rglob("*"))
        for path in files:
            if not path.is_file() or path.is_symlink() or SKIP_DIRS & set(path.parts) or path.suffix not in TEXT_SUFFIXES:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            protected = [sha256_bytes(s.encode()) for s in protected_segments(text, path.suffix)]
            entries.append({"path": str(path.resolve()), "sha256": sha256_file(path), "suffix": path.suffix,
                            "protected": sorted(protected)})
    return entries


def _digest(entries: list[dict[str, Any]]) -> str:
    return sha256_bytes(json.dumps([[e["path"], e["sha256"]] for e in sorted(entries, key=lambda e: e["path"])]).encode())


def _roots(values: list[str]) -> list[Path]:
    roots = []
    for value in values:
        path = Path(value).expanduser()
        if not path.is_absolute() or not path.exists() or path.is_symlink():
            raise HectlError(f"root must be an existing absolute non-symlink path: {value}")
        roots.append(path.resolve())
    return roots


def method_digest() -> str:
    skill = Path(__file__).resolve().parents[2]
    parts = [skill / "scripts" / "hecore" / "unslop.py", skill / "scripts" / "hecore" / "unslop_patterns.py",
             skill / "references" / "unslop-method.md",
             skill / "playbooks" / "unslop-repair.md"]
    missing = [str(p) for p in parts if not p.is_file()]
    if missing:
        raise HectlError("unslop method incomplete: " + ", ".join(missing))
    return sha256_bytes(b"".join(p.read_bytes() for p in parts))


def audit(run_id: str, roots: list[str], output: Path) -> dict[str, Any]:
    resolved = _roots(roots)
    if any(is_within(output, r) for r in resolved):
        raise HectlError("write audit output outside the audited roots")
    entries = _inventory(resolved)
    scans = [scan_text(Path(e["path"]).read_text(encoding="utf-8", errors="replace"), e["path"])
             for e in entries if e["suffix"] == ".md"]
    report = {"schema_version": 1, "run_id": run_id, "created_at": now_iso(), "roots": [str(r) for r in resolved],
              "method_sha256": method_digest(), "entries": entries, "inventory_sha256": _digest(entries),
              "raw_findings": sum(len(s["findings"]) for s in scans), "scans": scans}
    write_json(output, report)
    return report


def freeze(audit_path: Path, output: Path) -> dict[str, Any]:
    report = load_json(audit_path)
    roots = [Path(r) for r in report["roots"]]
    if any(is_within(output, r) for r in roots):
        raise HectlError("write freeze output outside the audited roots")
    current = _inventory(roots)
    if _digest(current) != report["inventory_sha256"]:
        before = {e["path"]: e["sha256"] for e in report["entries"]}
        drift = sorted(e["path"] for e in current if before.get(e["path"]) != e["sha256"])
        raise HectlError("source changed after audit; re-audit before freezing: " + ", ".join(drift[:10]))
    frozen = {"schema_version": 1, "run_id": report["run_id"], "frozen_at": now_iso(), "roots": report["roots"],
              "method_sha256": method_digest(), "entries": current, "inventory_sha256": report["inventory_sha256"]}
    write_json(output, frozen)
    return frozen


def verify(freeze_path: Path, ledger_path: Path, output: Path) -> dict[str, Any]:
    frozen = load_json(freeze_path)
    ledger = load_json(ledger_path)
    failures: list[str] = []
    roots = [Path(r) for r in frozen["roots"]]
    if ledger.get("run_id") != frozen["run_id"]:
        failures.append("ledger run_id does not match the freeze")
    if method_digest() != frozen.get("method_sha256"):
        failures.append("unslop method files changed since the freeze")
    approval = ledger.get("approval") or {}
    if approval.get("status") != "approved" or approval.get("authority") != "user" or not approval.get("evidence"):
        failures.append("approval must be status approved, authority user, with evidence")
    approved = {str(Path(p).resolve()) for p in approval.get("approved_paths", [])}
    created_ok = {str(Path(p).resolve()) for p in approval.get("created_paths", [])}
    for p in approved | created_ok:
        if not any(is_within(Path(p), r) for r in roots):
            failures.append(f"approved path outside frozen roots: {p}")
    before = {e["path"]: e for e in frozen["entries"]}
    current = {e["path"]: e for e in _inventory(roots)}
    changed = sorted(p for p in current if p in before and current[p]["sha256"] != before[p]["sha256"])
    created = sorted(p for p in current if p not in before)
    deleted = sorted(p for p in before if p not in current)
    for p in changed:
        if p not in approved:
            failures.append(f"out-of-scope change: {p}")
    for p in created:
        if p not in created_ok:
            failures.append(f"unapproved new file: {p}")
    for p in deleted:
        failures.append(f"file deleted during repair: {p}")
    for p in changed:
        old, new = before[p], current[p]
        if old["suffix"] in FULLY_PROTECTED:
            failures.append(f"structured file changed inside an unslop repair: {p}")
            continue
        missing = Counter(old["protected"]) - Counter(new["protected"])
        if missing:
            failures.append(f"protected material changed in {p} ({sum(missing.values())} segments)")
        text = Path(p).read_text(encoding="utf-8", errors="replace")
        if any("—" in line for _, line in prose_lines(text)):
            failures.append(f"authored em dash remains in {p}")
        if text.count("```") % 2 or re.search(r"\[(?:TODO|TBD)[:\]]|__REPLACE_ME__", text):
            failures.append(f"placeholder or fence corruption in {p}")
    workers = ledger.get("workers", [])
    if len(workers) > MAX_WORKERS:
        failures.append(f"more than {MAX_WORKERS} workers")
    owned_by: dict[str, str] = {}
    for w in workers:
        wid = w.get("worker_id", "?")
        if w.get("recursive_launches", 0):
            failures.append(f"{wid} launched another worker")
        owned = {str(Path(p).resolve()) for p in w.get("owned_paths", [])}
        for p in owned:
            if p in owned_by:
                failures.append(f"{wid} and {owned_by[p]} both own {p}")
            owned_by[p] = wid
        for p in w.get("changed_paths", []):
            if str(Path(p).resolve()) not in owned:
                failures.append(f"{wid} changed a path it does not own: {p}")
        for claim in ("approved", "integrated", "installed", "complete_run"):
            if w.get(claim):
                failures.append(f"{wid} claims parent authority: {claim}")
    findings = ledger.get("findings", [])
    unresolved = 0
    for f in findings:
        state = f.get("state")
        if state not in ("repaired", "protected") or not f.get("evidence"):
            unresolved += 1
        elif state == "protected" and not all(f.get(k) for k in ("category", "reason", "source_owner")):
            unresolved += 1
    if unresolved:
        failures.append(f"{unresolved} accepted findings are not terminal with evidence")
    for r in ledger.get("residuals", []):
        if r.get("class") not in ("legitimate-technical", "protected-source") or not r.get("evidence"):
            failures.append(f"residual without a valid class and evidence: {r.get('match', r)}")
    quality = ledger.get("quality") or {}
    cats = quality.get("category_scores") or {}
    score = 0.0
    if set(cats) != set(QUALITY):
        failures.append(f"quality categories must be exactly {sorted(QUALITY)}")
    else:
        for name, cap in QUALITY.items():
            value = cats[name].get("score") if isinstance(cats[name], dict) else None
            if not isinstance(value, (int, float)) or value < 0 or value > cap or not cats[name].get("evidence"):
                failures.append(f"quality.{name} needs a score from 0 to {cap} with evidence")
            else:
                score += value
    if round(score, 2) < FLOOR:
        failures.append(f"contextual score {score:.1f} below the {FLOOR} floor")
    gates = quality.get("hard_gates") or {}
    for gate in HARD_GATES:
        if gates.get(gate) is not True:
            failures.append(f"hard gate failed or missing: {gate}")
    for wave in ledger.get("repair_waves", []):
        if wave.get("unresolved_after", 0) >= wave.get("unresolved_before", 0) and wave.get("unresolved_before", 0) > 0:
            failures.append(f"repair wave {wave.get('wave')} did not reduce unresolved work; stop and re-plan")
    review = ledger.get("integrated_review") or {}
    current_digest = _digest(list(current.values()))
    if review.get("status") != "clear" or review.get("fresh") is not True:
        failures.append("integrated review must be fresh and clear")
    if review.get("inventory_sha256") != current_digest:
        failures.append("integrated review does not match the current candidate inventory")
    result = {"schema_version": 1, "run_id": frozen["run_id"], "verified_at": now_iso(),
              "changed": changed, "created": created, "score": round(score, 2), "floor": FLOOR,
              "current_inventory_sha256": current_digest, "failures": failures,
              "functional_result": "pass" if not failures else "fail",
              "note": "Qualitative judgement belongs to the integrated review; this gate checks scope, evidence and invariants."}
    write_json(output, result)
    return result
