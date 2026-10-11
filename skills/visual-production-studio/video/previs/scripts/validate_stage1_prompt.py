#!/usr/bin/env python3
"""
validate_stage1_prompt.py

Deterministic validator for Stage 1 (image model) storyboard prompts.
Checks format-appropriate structural elements. Use --format grid for untimed grids or --format commercial for tables. Sound cues are required only with --audio required.

Usage:
    python validate_stage1_prompt.py path/to/prompt.txt
    python validate_stage1_prompt.py - < prompt_from_stdin.txt
    echo "prompt text" | python validate_stage1_prompt.py -

Exit code:
    0 = all checks passed
    1 = one or more checks failed

Prints a per-check pass/fail report and a final summary.
"""

import sys
import re
import argparse
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from timing import extract_timing_brackets, check_timeline


CHECKS = [
    "panel_count_declared",
    "aspect_ratio_declared",
    "duration_declared",
    "subject_named",
    "motion_register_named",
    "environment_described",
    "palette_stated",
    "arrow_legend_present",
    "sfx_present",
    "per_panel_timing_brackets",
]


def check_panel_count_declared(text):
    """Look for explicit panel count: '8 panel', '12-panel', '3x4 grid', '九宫格', '9镜', '16格'."""
    patterns = [
        r"\b\d{1,2}\s*[-\s]*panel",
        r"\bpanels?\s*:\s*\d{1,2}",
        r"\d+\s*个分镜",
        r"\b\d+[- ](?:shot|beat)\b",
        r"\b\d\s*[x×]\s*\d\s*(grid|panel|storyboard|分镜)",
        r"\b\d{1,2}\s*镜",
        r"\b\d{1,2}\s*格",
        r"九宫格",
        r"\bgrid\s*:\s*\d\s*[x×]\s*\d",
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def check_aspect_ratio_declared(text):
    """Look for aspect ratio: 16:9, 9:16, 1:1, 21:9, 4:3, 2.39:1."""
    return bool(re.search(r"\b\d{1,2}(\.\d+)?\s*:\s*\d{1,2}\b", text))


def check_duration_declared(text):
    """Look for duration in seconds: '15s', '15 seconds', '15秒', 'duration: 15'."""
    patterns = [
        r"\b\d{1,3}\s*s\b",
        r"\b\d{1,3}\s*sec",
        r"\b\d{1,3}\s*秒",
        r"duration\s*:?\s*\d{1,3}",
        r"\b\d{1,3}\s*-?\s*second",
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def check_subject_named(text):
    """Look for subject declaration keyword."""
    patterns = [
        r"\bsubject\s*:",
        r"主题\s*[:：]",
        r"\bcharacters?\s*:",
        r"\bcharacter\s*:",
        r"\bprotagonist\s*:",
        r"\bhero\s*:",
        r"\bhero\s+frame\b[^\n]*:",
        r"\bcharacter\s+design\b",
        r"主体\s*[:：]",
        r"主角\s*[:：]",
        r"角色\s*[:：]",
        r"\bof\s+a\s+[a-z]",
        r"\bfeaturing\s+a\s+[a-z]",
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def check_motion_register_named(text):
    """Look for motion type keyword."""
    keywords = [
        "dance", "dancing", "combat", "fight", "fighting", "running", "walking",
        "spinning", "leaping", "punch", "kick", "strike", "dodge", "block",
        "stillness", "static", "atmospheric", "slow", "rapid", "fast",
        "choreography", "movement", "motion", "action", "performance",
        "动作", "舞蹈", "战斗", "武打", "动态", "运动", "缓缓", "镜头",
    ]
    lower = text.lower()
    return any(k in lower for k in keywords)


def check_environment_described(text):
    """Look for environment/setting keyword."""
    patterns = [
        r"\benvironment\s*:",
        r"\bsetting\s*:",
        r"\blocation\s*:",
        r"\bbackground\s*:",
        r"\b(?:background|forest|alley|studio|ruins|blizzard)\b",
        r"\bscene\s*:",
        r"环境\s*[:：]",
        r"白色大理石|\binfinite white space\b",
        r"场景\s*[:：]",
        r"背景\s*[:：]",
        r"\bin\s+a\s+[a-z]+\s+(forest|city|room|street|studio|space|hall|alley|field|desert|mountain|ocean|sky)",
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def check_palette_stated(text):
    """Look for palette/color declaration."""
    patterns = [
        r"\bpalette\s*:",
        r"\bcolou?r\s+palette",
        r"\btone\s*:",
        r"\bcolou?r\s+scheme",
        r"调色板",
        r"画面风格\s*[:：]|色彩\s*[:：]",
        r"配色",
        r"色调",
        r"\b(monochrome|grayscale|neon|warm|cool|pastel|muted|vibrant)\s",
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def check_arrow_legend_present(text):
    """Look for arrow color logic / motion arrow legend."""
    patterns = [
        r"\barrow",
        r"\blegend",
        r"red\s*=\s*camera",
        r"blue\s*=\s*subject",
        r"camera\s+motion.{0,40}colou?r",
        r"colou?r[\s-]coded",
        r"箭头",
        r"图例",
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def check_sfx_present(text):
    """Look for SFX cues or audio notation."""
    patterns = [
        r"\bsfx\b",
        r"\bsound\s+effect",
        r"\baudio\s+cue",
        r"\bsound\s+design",
        r"音效",
        r"声效",
        r"sound\s*:",
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def check_per_panel_timing_brackets(text):
    """Concrete decimal or clock ranges only; labels alone are not timing."""
    return bool(extract_timing_brackets(text))


CHECK_FUNCS = {
    "panel_count_declared": check_panel_count_declared,
    "aspect_ratio_declared": check_aspect_ratio_declared,
    "duration_declared": check_duration_declared,
    "subject_named": check_subject_named,
    "motion_register_named": check_motion_register_named,
    "environment_described": check_environment_described,
    "palette_stated": check_palette_stated,
    "arrow_legend_present": check_arrow_legend_present,
    "sfx_present": check_sfx_present,
    "per_panel_timing_brackets": check_per_panel_timing_brackets,
}


def validate(text, format="annotated", audio="optional", duration=None, panel_count=None):
    """Return applicable checks; optional timed checks use the shared parser."""
    selected = [n for n in CHECKS if n not in {"sfx_present", "per_panel_timing_brackets", "arrow_legend_present"}]
    if format in {"annotated", "combat"}:
        selected += ["arrow_legend_present", "per_panel_timing_brackets"]
    if audio == "required":
        selected.append("sfx_present")
    results = [(name, CHECK_FUNCS[name](text)) for name in selected]
    try:
        pairs = extract_timing_brackets(text)
        if pairs and duration is not None:
            results.append(("contiguous_timing", check_timeline(text, duration)[0]))
        if pairs and panel_count is not None:
            results.append(("timing_count_matches_panels", len(pairs) == panel_count))
    except (ValueError, ArithmeticError):
        results.append(("valid_timing", False))
    return results, sum(p for _, p in results)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("--format", choices=["annotated", "combat", "grid", "commercial"], default="annotated")
    parser.add_argument("--audio", choices=["optional", "required", "silent"], default="optional")
    parser.add_argument("--duration")
    parser.add_argument("--panels", type=int)
    args = parser.parse_args()
    try:
        from pathlib import Path
        text = sys.stdin.read() if args.source == "-" else Path(args.source).read_text()
        results, count = validate(text, args.format, args.audio, args.duration, args.panels)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    for name, passed in results:
        print(f"{'PASS' if passed else 'FAIL'} {name}")
    print(f"{count}/{len(results)} structural checks passed. This does not establish image quality or user acceptance.")
    raise SystemExit(0 if count == len(results) else 1)

if __name__ == "__main__":
    main()
