"""Deterministic over-constraint scan of persistent context. Read-only.

It finds the line-level patterns the context doctrine treats as model compensation
and the file-level shapes that suggest progressive disclosure. Judgement about
user policy versus compensation stays with the agent; the scanner only supplies evidence.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

FAIL, WARN, INFO = "FAIL", "WARN", "INFO"
CATALOGUE = "context-scan: catalogue"
IGNORE = "context-scan: ignore"


def _rx(*parts: str) -> list[re.Pattern]:
    return [re.compile(p, re.IGNORECASE) for p in parts]


# category -> (severity, action, reason, patterns)
RULES: dict[str, tuple[str, str, str, list[re.Pattern]]] = {
    "reasoning-echo": (FAIL, "remove", "Asking a model to expose its reasoning can trigger refusals and leaks working notes. Use the host's thinking or progress channel.", _rx(
        r"\bshow (?:your|its|the) (?:thinking|reasoning|thought process|work)\b",
        r"\b(?:explain|describe|walk through) (?:your|its) (?:internal )?reasoning\b",
        r"\b(?:echo|transcribe|reproduce|narrate|output|print) (?:your|its|the) (?:thinking|reasoning|thought process|chain of thought)\b",
        r"\bchain[- ]of[- ]thought\b",
        r"\breflect on (?:your|its) (?:reasoning|thinking)\b",
        r"\breason(?:ing)? (?:step by step )?(?:first|before) (?:you )?answer",
        r"\bthink (?:out loud|aloud)\b",
        r"<(?:reflection|thinking|scratchpad)>",
    )),
    "verification-instruction": (WARN, "review", "Explicit verify or double-check lines can cause over-verification on capable models. A signal to test with the target model, not proof the line is unneeded.", _rx(
        r"\bdouble[- ]check\b",
        r"\bre-?verify\b",
        r"\bverify (?:your|its|the) (?:own )?(?:work|answer|output|response|result)s?\b",
        r"\bfinal (?:verification|check) step\b",
        r"\bcheck (?:your|its) (?:own )?work\b",
        r"\bsubagent (?:to|that) (?:verify|check|double[- ]check)\b",
        r"\bscore (?:it |yourself )?(?:from )?0 ?(?:to|-) ?10\b",
    )),
    "anti-laziness": (WARN, "review", "Early-stopping compensation can drive over-elaboration. Test before removing.", _rx(
        r"\bbe (?:thorough|exhaustive|comprehensive)\b",
        r"\bdo ?n[o']t stop (?:early|until)\b",
        r"\bleave nothing out\b",
        r"\bcomplete (?:ALL|every single)\b",
        r"\bdo not be lazy\b",
        r"\bexhaustive(?:ly)?\b",
    )),
    "capitalised-emphasis": (WARN, "rewrite", "Shouted rules can read as conflicts; a plain statement is usually enough.", [
        re.compile(r"\b(?:CRITICAL|MANDATORY|YOU MUST|ALWAYS|NEVER|MUST NOT)\b|\bIMPORTANT:"),
    ]),
    "forced-summary": (WARN, "review", "Fixed-cadence summaries and restatements add noise unless the run needs them.", _rx(
        r"\bsummari[sz]e (?:after )?every \d+\b",
        r"\bafter every \d+ (?:tool calls|steps|turns)\b",
        r"\brestate (?:the )?(?:task|contract|plan|goal) (?:each|every|before)\b",
    )),
    "narration-suppression": (WARN, "review", "Suppressing progress updates can silence useful behavior. Check whether the reader needs them.", _rx(
        r"\bhold (?:all )?(?:findings|updates|results) (?:for|until) the (?:final|end)\b",
        r"\bdo not (?:send|give|write) (?:progress|interim) updates\b",
        r"\bno (?:interim|progress) (?:updates|messages)\b",
    )),
    "anti-formatting": (WARN, "rewrite", "Blanket formatting bans can remove structure the content needs. State when structure is wanted instead.", _rx(
        r"\b(?:use )?minimal formatting\b",
        r"\bno (?:bullet points|bullets|headers|headings|lists)\b",
        r"\bnever use (?:bullet points|bullets|headers|headings|lists|markdown)\b",
        r"\bavoid (?:bullet points|bullets|headers|headings|markdown)\b",
    )),
    "think-prompting": (WARN, "review", "Where the host offers reasoning or effort settings, prefer them over prompt pressure. Test with the target model.", _rx(
        r"\bthink (?:carefully|hard|deeply|step[- ]by[- ]step)\b",
        r"\btake a deep breath\b",
        r"\bultrathink\b",
    )),
    "subagent-pressure": (WARN, "rewrite", "Blanket spawning pressure over-delegates. Say when delegation helps instead.", _rx(
        r"\b(?:always|aggressively) (?:use|spawn|launch) (?:a |many |multiple )?(?:sub-?agents?|parallel agents)\b",
        r"\bspawn (?:multiple|several|many|as many) (?:sub-?agents|agents)\b",
    )),
    "tool-pressure": (WARN, "move", "Tool guidance belongs once, in the tool's own description.", _rx(
        r"\byou must (?:call|use) the \w+ tool\b",
        r"\bremember to (?:call|use) the \w+ tool\b",
        r"\balways (?:call|use) the \w+ tool (?:first|before)\b",
    )),
}

DESCRIPTIVE = re.compile(
    r"\b(?:not|never write|never add|avoid|remove[sd]?|removing|removal|delete[sd]?|cut|strip|ban(?:ned)?|"
    r"forbid(?:den)?|instead of|rather than|no need|legacy|obsolete|stale|used to|previously|anti-pattern|"
    r"compensat\w*|deprune|don't|do not (?:use|add|write|instruct))\b", re.IGNORECASE)
PROHIBITION = re.compile(r"^\s*(?:[-*]|\d+[.)])?\s*(?:Do not|Don't|Never|Avoid|No)\b", re.IGNORECASE)
EXAMPLE_HEAD = re.compile(r"^\s{0,3}#{1,6}\s.*\bexamples?\b", re.IGNORECASE)
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")

PROHIBITION_LIMIT = 8
WORD_LIMIT = 800
EXAMPLE_LIMIT = 3


VERIFICATION_POLICIES = ("review-all", "keep-one")
REPEAT_CHECK = re.compile(r"double[- ]check|re-?verify", re.IGNORECASE)


def scan_text(path: str, text: str, long_run: bool = False, verification_policy: str = "review-all") -> list[dict[str, Any]]:
    """Signals for judgement and testing, not proof. `verification_policy`: review-all flags every
    verification line; keep-one keeps the first test-your-work line and flags the rest."""
    kept_one = False
    lines = text.splitlines()
    head = "\n".join(lines[:20])
    findings: list[dict[str, Any]] = []
    fence = None
    prohibitions = 0
    examples = 0
    body_words = 0
    catalogue = CATALOGUE in head
    for number, line in enumerate(lines, 1):
        marker = FENCE.match(line)
        if marker:
            token = marker.group(1)[0]
            fence = None if fence == token else (fence or token)
            continue
        if fence:
            continue
        body_words += len(line.split())
        if PROHIBITION.match(line):
            prohibitions += 1
        if EXAMPLE_HEAD.match(line):
            examples += 1
        if catalogue or IGNORE in line:
            continue
        for category, (severity, action, reason, patterns) in RULES.items():
            if not any(p.search(line) for p in patterns):
                continue
            level = severity
            note = reason
            if (severity == FAIL or category == "verification-instruction") and DESCRIPTIVE.search(line):
                level, note = INFO, "Names the pattern to forbid or describe it. Confirm by hand. " + reason
            elif category == "verification-instruction" and long_run:
                level, note = INFO, "Often kept in a long unattended run where no person reviews intermediate work. " + reason
            elif (category == "verification-instruction" and verification_policy == "keep-one"
                  and not kept_one and not REPEAT_CHECK.search(line)):
                kept_one = True
                level, note = INFO, "Kept as the one test-your-work line under --verification-policy keep-one. " + reason
            findings.append({"file": path, "line": number, "category": category, "severity": level,
                             "text": line.strip()[:240], "reason": note, "action": action})
    if not catalogue:
        if prohibitions >= PROHIBITION_LIMIT:
            findings.append({"file": path, "line": 0, "category": "prohibition-density", "severity": WARN,
                             "text": f"{prohibitions} prohibition lines",
                             "reason": "Long prohibition lists conflict. Describe the wanted shape once.", "action": "rewrite"})
        if body_words >= WORD_LIMIT:
            findings.append({"file": path, "line": 0, "category": "progressive-disclosure", "severity": INFO,
                             "text": f"{body_words} words outside code",
                             "reason": "Detail only some tasks need can load on demand from a linked file.", "action": "move"})
        if examples >= EXAMPLE_LIMIT:
            findings.append({"file": path, "line": 0, "category": "example-weight", "severity": INFO,
                             "text": f"{examples} example sections",
                             "reason": "Examples narrow exploration. Prefer interface design or a test fixture.", "action": "rewrite"})
    return findings


def collect(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = Path(raw).expanduser()
        if path.is_dir():
            files.extend(sorted(p for p in path.rglob("*.md") if ".git" not in p.parts))
        elif path.is_file():
            files.append(path)
    return files


def scan_paths(paths: list[str], long_run: bool = False, verification_policy: str = "review-all") -> dict[str, Any]:
    files = collect(paths)
    rows: list[dict[str, Any]] = []
    for path in files:
        found = scan_text(str(path), path.read_text(encoding="utf-8", errors="replace"), long_run, verification_policy)
        rows.extend(found or [{"file": str(path), "line": 0, "category": "clean", "severity": INFO,
                               "text": "", "reason": "No scanner findings.", "action": "keep"}])
    order = {"reasoning-echo": 0, "verification-instruction": 1}
    rank = {FAIL: 0, WARN: 1, INFO: 2}
    rows.sort(key=lambda r: (rank[r["severity"]], order.get(r["category"], 2), r["file"], r["line"]))
    counts = {level: sum(1 for r in rows if r["severity"] == level and r["category"] != "clean") for level in (FAIL, WARN, INFO)}
    return {"files": len(files), "counts": counts, "findings": rows}
