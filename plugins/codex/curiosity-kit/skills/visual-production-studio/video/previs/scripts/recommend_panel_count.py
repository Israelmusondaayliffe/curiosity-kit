#!/usr/bin/env python3
"""Editorial starting counts, not provider limits. User counts and actual boards win.
Examples: 15 medium -> 12; 15 combat -> 16; 25 fast -> 16; 6 slow -> 4.
"""
import argparse
import math

VALID_REGISTERS = {"slow", "medium", "fast", "combat"}
ANCHORS = {
    5: {"slow": 4, "medium": 5, "fast": 6, "combat": 6},
    10: {"slow": 6, "medium": 8, "fast": 9, "combat": 10},
    15: {"slow": 8, "medium": 12, "fast": 12, "combat": 16},
    20: {"slow": 9, "medium": 12, "fast": 14, "combat": 16},
    25: {"slow": 12, "medium": 14, "fast": 16, "combat": 16},
}

def recommend(duration, register):
    register = register.lower()
    if register not in VALID_REGISTERS:
        return None, f"unknown register: {register}", []
    try:
        duration = float(duration)
    except (ValueError, TypeError):
        return None, "duration must be a finite positive number", []
    if not math.isfinite(duration) or duration <= 0:
        return None, "duration must be a finite positive number", []
    warnings = []
    if duration > 25:
        warnings.append("Long board: consider multiple sheets or editorial segments. Check the selected surface's actual clip limit; 25 seconds is not a model ceiling.")
        return 16, "single-sheet readability starting point; user may choose more", warnings
    if duration < 5:
        return 4, "short-board starting point", ["A single image plus motion may be sufficient; fewer panels are valid."]
    if duration in ANCHORS:
        count = ANCHORS[duration][register]
    else:
        lower = max(t for t in ANCHORS if t < duration)
        upper = min(t for t in ANCHORS if t > duration)
        ratio = (duration - lower) / (upper - lower)
        count = round(ANCHORS[lower][register] + ratio * (ANCHORS[upper][register] - ANCHORS[lower][register]))
    return count, f"{duration:g}s {register} editorial starting point; preserve an explicit count or observed board", warnings

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("duration", type=float)
    parser.add_argument("register", choices=sorted(VALID_REGISTERS))
    args = parser.parse_args()
    count, rationale, warnings = recommend(args.duration, args.register)
    if count is None:
        parser.error(rationale)
    print(f"Recommended panel count: {count}\nRationale: {rationale}\nBeat duration: ~{args.duration/count:.2f}s per panel")
    for warning in warnings:
        print(f"Note: {warning}")

if __name__ == "__main__":
    main()
