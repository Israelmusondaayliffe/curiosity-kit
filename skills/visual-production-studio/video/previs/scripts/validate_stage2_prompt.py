#!/usr/bin/env python3
"""Check applicable Stage 2 structure, not visual quality or provider support.

Explicit format requires contiguous timing and one beat per panel unless a
complete ordered --panel-map JSON is supplied. Reference format accepts terse
board-led prompts; keyframes accepts transition prompts. Both may omit timing,
but any timing they contain is checked. --audio required is opt-in.
--handoff validates a recorded visual read and actual asset roles. A passing
receipt cannot prove that someone inspected an image: the operator must do so.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from timing import seconds, extract_timing_brackets, check_timeline

check_timing_sum = check_timeline

def count_beat_blocks(text):
    pairs = extract_timing_brackets(text)
    if pairs:
        return len(pairs)
    labels = re.findall(r"(?:\b(?:shot|panel|clip|beat|scene)\s+\d+|(?:分镜|镜)\s*\d+)\s*[:：.]", text, re.I)
    return len(labels)

def check_beat_count(text, panel_count, panel_map=None):
    count = count_beat_blocks(text)
    if panel_map is None:
        return (count == panel_count, f"{count} beats for {panel_count} panels; exact match required")
    if not isinstance(panel_map, list) or len(panel_map) != count:
        return False, "panel map must contain one panel-ID list per beat"
    if any(not isinstance(group, list) or not group or any(type(n) is not int for n in group) for group in panel_map):
        return False, "each beat must map to a nonempty list of integer panel IDs"
    flattened = [n for group in panel_map for n in group]
    if flattened != list(range(1, panel_count + 1)):
        return False, "panel map must cover every source panel exactly once in order"
    return True, f"explicit map preserves {panel_count} panels in {count} beats"

def check_character_locking(text):
    # Continuity may be for a product, place, or abstract subject, not a person.
    return bool(re.search(r"consisten|continuity|preserv|identity|一致|参考|reference|@(?:Image|Element)\d", text, re.I)), "continuity/reference instruction"

def check_sfx_cues(text):
    return bool(re.search(r"\bsfx\b|sound|audio|voice|music|音效|旁白|音频", text, re.I))

def check_handoff(handoff, text, panel_count):
    if not isinstance(handoff, dict):
        return False, "handoff must be an object"
    board = handoff.get("board_read", {})
    if not isinstance(board, dict) or not board.get("source") or not board.get("observation"):
        return False, "board_read needs the actual rendered source and visual observation"
    panels = board.get("panels", [])
    if not isinstance(panels, list) or any(not isinstance(p, dict) for p in panels):
        return False, "board_read panels must be records"
    if [p.get("id") for p in panels] != list(range(1, panel_count + 1)) or any(type(p.get("id")) is not int or not p.get("observation") for p in panels):
        return False, "visual read must describe every panel in observed order"
    assets = handoff.get("assets", [])
    if not isinstance(assets, list) or any(not isinstance(a, dict) for a in assets):
        return False, "assets must be records"
    allowed = {"storyboard", "start-frame", "identity", "wardrobe", "expression", "environment", "style", "end-frame", "motion", "audio"}
    tags = []
    for asset in assets:
        tag = asset.get("tag", "")
        if not isinstance(tag, str) or not tag.strip() or "\n" in tag or "\r" in tag or asset.get("role") not in allowed or not asset.get("source"):
            return False, "each asset needs a valid actual tag, source, and supported role"
        tags.append(tag.lower())
    if len(set(tags)) != len(tags):
        return False, "one uploaded tag cannot have conflicting roles"
    if not any(a["role"] == "storyboard" and a["source"] == board["source"] for a in assets):
        return False, "storyboard asset must identify the rendered board that was read"
    used = {t.lower() for t in re.findall(r"@(?:Image|Element)\d+", text, re.I)}
    if used - set(tags):
        return False, "prompt refers to unregistered uploaded tags: " + ", ".join(sorted(used - set(tags)))
    # Check explicit assignment sentences against the recorded roles.
    for asset in assets:
        tag = re.escape(asset["tag"])
        line = re.search(rf"(?:^|\n)[^\n]*{tag}\b[^\n]*", text, re.I)
        if line and asset["role"] in {"identity", "wardrobe", "expression", "storyboard"}:
            if re.search(r"start (?:frame|image)\s*:", line.group(0), re.I):
                return False, f"{asset['tag']} is {asset['role']}, not an actual start-frame asset"
    return True, "recorded board read and actual upload mapping are coherent; visual inspection still requires operator evidence"

def validate(text, duration, panel_count, format="explicit", audio="optional", panel_map=None, handoff=None):
    checks = []
    try:
        valid_input = seconds(duration) > 0 and type(panel_count) is int and panel_count > 0
        pairs = extract_timing_brackets(text)
    except (ValueError, ArithmeticError):
        valid_input, pairs = False, []
    if not valid_input:
        return [("valid_inputs", False, "positive finite duration and positive integer panel count required")]
    if format not in {"explicit", "reference", "keyframes"}:
        return [("format", False, "unknown format")]
    checks.append(("nonempty_prompt", bool(text.strip()), "prompt must contain content"))
    if format == "explicit" or pairs:
        ok, msg = check_timing_sum(text, duration)
        checks.append(("contiguous_timing", ok, msg))
        ok, msg = check_beat_count(text, panel_count, panel_map)
        checks.append(("panel_coverage", ok, msg))
    elif format == "reference":
        ok = bool(re.search(r"storyboard|panel|分镜|故事板", text, re.I))
        checks.append(("reference_sequence", ok, "terse form must identify the board sequence; exact timing is not statically established"))
    else:
        transitions = re.findall(r"^\s*(\d+)\s*(?:->|→)\s*(\d+)\s*:", text, re.M)
        ok = bool(transitions) and all(int(b) == int(a)+1 for a,b in transitions)
        ok = ok and [int(a) for a,b in transitions] == list(range(1, len(transitions)+1))
        checks.append(("keyframe_transitions", ok, "transition labels must be contiguous and ordered"))
    ok, msg = check_character_locking(text)
    checks.append(("continuity_or_reference", ok, msg))
    if audio == "required":
        checks.append(("audio_cues", check_sfx_cues(text), "requested audio requires a cue"))
    if handoff is not None:
        ok, msg = check_handoff(handoff, text, panel_count)
        checks.append(("rendered_board_handoff", ok, msg))
    return checks

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("duration")
    parser.add_argument("panel_count", type=int)
    parser.add_argument("--format", choices=["explicit", "reference", "keyframes"], default="explicit")
    parser.add_argument("--audio", choices=["optional", "required", "silent"], default="optional")
    parser.add_argument("--panel-map", help="JSON file: one ordered panel-ID list per beat")
    parser.add_argument("--handoff", help="JSON visual-read and actual-upload receipt")
    args = parser.parse_args()
    try:
        import sys
        text = sys.stdin.read() if args.source == "-" else Path(args.source).read_text()
        mapping = json.loads(Path(args.panel_map).read_text()) if args.panel_map else None
        handoff = json.loads(Path(args.handoff).read_text()) if args.handoff else None
        checks = validate(text, args.duration, args.panel_count, args.format, args.audio, mapping, handoff)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    for name, passed, message in checks:
        print(f"{'PASS' if passed else 'FAIL'} {name}: {message}")
    print("Structural checks only; not creative acceptance, native-control proof, or evidence of rendered fidelity.")
    raise SystemExit(0 if all(passed for _, passed, _ in checks) else 1)

if __name__ == "__main__":
    main()
