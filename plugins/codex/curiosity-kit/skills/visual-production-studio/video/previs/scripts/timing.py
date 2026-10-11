"""Shared decimal-second and clock-range parsing, without guessing missing beats."""
import re
from decimal import Decimal, InvalidOperation

NUMBER = r"\d+(?:\.\d+)?"
TIME = rf"(?:\d+:\d{{2}}(?:\.\d+)?|{NUMBER})"
RANGE = re.compile(rf"(?<![\d.:])(?P<a>{TIME})\s*(?:s\b)?\s*(?:-|–|—|\bto\b)\s*(?P<b>{TIME})\s*(?:s(?:ec(?:ond)?s?)?\b)?", re.I)

def seconds(value):
    raw = str(value).strip()
    if ":" in raw:
        minutes, secs = raw.split(":")
        if Decimal(secs) >= 60:
            raise ValueError("clock seconds must be below 60")
        result = Decimal(minutes) * 60 + Decimal(secs)
    else:
        result = Decimal(raw)
    if not result.is_finite():
        raise ValueError("time must be finite")
    return result

def extract_timing_brackets(text):
    """Read ranges in document order. Ignore prose counts such as 'panels 3-4'."""
    pairs = []
    for line in text.splitlines():
        for match in RANGE.finditer(line):
            before, after = line[:match.start()], line[match.end():]
            token = match.group(0)
            # A timing range is bracketed, clock-based, or has a seconds suffix.
            if not (before.rstrip().endswith(("[", "(", "（")) or ":" in token or re.search(r"s(?:ec(?:ond)?s?)?$", token.strip(), re.I)):
                continue
            pairs.append((seconds(match.group("a")), seconds(match.group("b"))))
    return pairs

def check_timeline(text, duration):
    try:
        target = seconds(duration)
        pairs = extract_timing_brackets(text)
    except (ValueError, InvalidOperation) as exc:
        return False, str(exc)
    if target <= 0:
        return False, "duration must be positive"
    if not pairs:
        return False, "no explicit timing ranges found"
    cursor = Decimal(0)
    for index, (start, end) in enumerate(pairs, 1):
        if end <= start:
            return False, f"beat {index} has zero or reversed duration"
        if start != cursor:
            kind = "gap" if start > cursor else "overlap or out-of-order beat"
            return False, f"{kind} before beat {index}: expected {cursor}s, got {start}s"
        cursor = end
    if cursor != target:
        return False, f"timeline ends at {cursor}s, expected {target}s"
    return True, f"{len(pairs)} contiguous beats cover 0 to {target}s"
