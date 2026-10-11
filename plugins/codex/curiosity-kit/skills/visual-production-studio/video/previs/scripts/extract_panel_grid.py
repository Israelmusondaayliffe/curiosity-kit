#!/usr/bin/env python3
"""
extract_panel_grid.py

Vision helper that attempts to detect panel boundaries in a storyboard composite
image using basic edge detection and aspect-ratio heuristics. Reports detected
panel count, detected grid shape (e.g., 3x4), and a confidence score.

Falls back to "vision inference required" when confidence is low. Used by
Mode 3 (VIDEO-FROM-STORYBOARD) and Mode 5 (DECONSTRUCT) agents.

Usage:
    python extract_panel_grid.py path/to/storyboard.png

Output (stdout, key=value lines):
    panel_count=12
    grid_rows=3
    grid_cols=4
    confidence=0.78
    method=edge_projection
    aspect_ratio=1.77
    fallback=false

When confidence is below threshold, fallback=true and the agent should fall back
to direct vision inference.

Dependencies: PIL (Pillow), numpy. Both available in the default container.
"""

import sys
import os


THRESHOLD = 0.55  # Below this, advise fallback to vision inference
DARK_VAL = 60     # Pixel value below this counts as a "dark" pixel (gridline)


def import_deps():
    try:
        from PIL import Image
        import numpy as np
        return Image, np
    except ImportError as e:
        print(f"panel_count=0", )
        print(f"grid_rows=0")
        print(f"grid_cols=0")
        print(f"confidence=0.0")
        print(f"method=missing_dependencies")
        print(f"fallback=true")
        print(f"error={e}", file=sys.stderr)
        sys.exit(0)


def load_grayscale(path, Image, np):
    img = Image.open(path).convert("L")
    arr = np.asarray(img, dtype=np.uint8)
    return arr


def find_gridlines(profile, min_gap_ratio=0.05):
    """
    Given a 1D darkness profile (sum of darkness per row or column), return
    indices of detected gridlines. A gridline is a peak in the profile that is
    well-separated from other peaks.
    """
    import numpy as np
    n = len(profile)
    if n == 0:
        return []
    # Normalize
    p = profile.astype(float)
    p = (p - p.min()) / (p.max() - p.min() + 1e-9)
    # Threshold at 0.6 of range
    above = p > 0.6
    # Find runs of True
    peaks = []
    i = 0
    min_gap = int(n * min_gap_ratio)
    while i < n:
        if above[i]:
            j = i
            while j < n and above[j]:
                j += 1
            center = (i + j - 1) // 2
            if not peaks or center - peaks[-1] >= min_gap:
                peaks.append(center)
            i = j
        else:
            i += 1
    return peaks


def detect_grid(arr, np):
    """
    Detect grid by projecting darkness onto row and column axes.
    Returns (rows, cols, confidence, method).
    """
    h, w = arr.shape
    # Darkness profile: count dark pixels per row and per column
    dark = arr < DARK_VAL
    row_profile = dark.sum(axis=1).astype(float)
    col_profile = dark.sum(axis=0).astype(float)

    # Find peaks (horizontal lines = rows of gridline, vertical lines = cols of gridline)
    h_lines = find_gridlines(row_profile)
    v_lines = find_gridlines(col_profile)

    # Trim outermost lines (image edges)
    def trim_edges(lines, dim):
        if not lines:
            return []
        edge_zone = int(dim * 0.03)
        return [x for x in lines if edge_zone < x < dim - edge_zone]

    h_inner = trim_edges(h_lines, h)
    v_inner = trim_edges(v_lines, w)

    # Number of panel rows = number of inner horizontal lines + 1
    rows = len(h_inner) + 1
    cols = len(v_inner) + 1

    # Sanity bounds: panels are 1x1 to 5x6
    if rows < 1 or rows > 6 or cols < 1 or cols > 6:
        return 0, 0, 0.0, "out_of_bounds"
    if rows * cols < 2 or rows * cols > 20:
        return 0, 0, 0.0, "panel_count_out_of_bounds"

    # Confidence heuristic: more uniform spacing = higher confidence
    confidence = compute_confidence(h_inner, v_inner, h, w, np)
    return rows, cols, confidence, "edge_projection"


def compute_confidence(h_inner, v_inner, h, w, np):
    """
    Confidence = how uniformly the detected gridlines are spaced.
    Uniform spacing implies a real grid. Returns 0.0 to 1.0.
    """
    def uniformity(lines, dim):
        if len(lines) < 1:
            return 0.0
        # Include implicit edges
        positions = [0] + sorted(lines) + [dim]
        gaps = [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]
        if not gaps or len(gaps) < 2:
            return 0.0
        mean_gap = sum(gaps) / len(gaps)
        if mean_gap == 0:
            return 0.0
        variance = sum((g - mean_gap) ** 2 for g in gaps) / len(gaps)
        std = variance ** 0.5
        cv = std / mean_gap  # coefficient of variation
        # Lower CV = more uniform = higher confidence
        return max(0.0, 1.0 - cv * 1.5)

    u_h = uniformity(h_inner, h)
    u_v = uniformity(v_inner, w)
    # Both axes must be uniform for a real grid
    return round((u_h * u_v) ** 0.5, 3)


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_panel_grid.py <path_to_image>", file=sys.stderr)
        sys.exit(2)
    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(2)

    Image, np = import_deps()
    try:
        arr = load_grayscale(path, Image, np)
    except Exception as e:
        print(f"panel_count=0")
        print(f"grid_rows=0")
        print(f"grid_cols=0")
        print(f"confidence=0.0")
        print(f"method=load_failure")
        print(f"fallback=true")
        print(f"error={e}", file=sys.stderr)
        sys.exit(0)

    h, w = arr.shape
    aspect = round(w / h, 2) if h else 0
    rows, cols, conf, method = detect_grid(arr, np)
    panel_count = rows * cols
    fallback = conf < THRESHOLD or panel_count == 0

    print(f"panel_count={panel_count}")
    print(f"grid_rows={rows}")
    print(f"grid_cols={cols}")
    print(f"confidence={conf}")
    print(f"method={method}")
    print(f"aspect_ratio={aspect}")
    print(f"fallback={'true' if fallback else 'false'}")

    if fallback:
        print(f"hint=confidence_below_{THRESHOLD}_use_vision_inference", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
