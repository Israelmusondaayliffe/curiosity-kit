#!/usr/bin/env python3
"""Render a categorical dot plot from checked CSV values, without recalculating metrics."""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal, InvalidOperation, localcontext, ROUND_CEILING
import hashlib
import io
import json
import math
import os
from pathlib import Path
import stat
import sys
import textwrap
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

MAX_BYTES = 1024 * 1024
MAX_ROWS = 30


def clean(text: str, name: str, limit: int) -> str:
    if not text.strip() or len(text) > limit:
        raise ValueError(f"{name} must contain 1 to {limit} characters")
    if any(ord(c) < 32 and c not in '\t\n\r' for c in text):
        raise ValueError(f"{name} contains unsupported control characters")
    return ' '.join(text.split())


def number(text: str, label: str) -> Decimal:
    try:
        n = Decimal(text)
    except InvalidOperation:
        raise ValueError(f"{label}: expected a plain finite number") from None
    if not n.is_finite() or len(text) > 40 or not math.isfinite(float(n)):
        raise ValueError(f"{label}: unsupported nonfinite or oversized number")
    return n


def load(args: argparse.Namespace):
    # An explicit file only. No home/config/catalog inspection or network calls.
    fd = os.open(args.csv, os.O_RDONLY | os.O_NONBLOCK | getattr(os, 'O_NOFOLLOW', 0))
    with os.fdopen(fd, 'rb') as f:
        if not stat.S_ISREG(os.fstat(f.fileno()).st_mode):
            raise ValueError('CSV must be a regular file')
        raw = f.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError('CSV exceeds 1 MiB')
    digest = hashlib.sha256(raw).hexdigest()
    if args.expect_sha256 and args.expect_sha256.lower() != digest:
        raise ValueError('CSV identity differs from --expect-sha256; reconcile the source before plotting')
    reader = csv.reader(io.StringIO(raw.decode('utf-8-sig')), strict=True)
    try:
        headers = next(reader)
    except StopIteration:
        raise ValueError('CSV is empty') from None
    if not headers or any(not h.strip() for h in headers) or len(set(headers)) != len(headers):
        raise ValueError('CSV headers must be nonempty and unique')
    names = [args.label, args.value] + ([args.lower, args.upper] if args.lower else [])
    if len(set(names)) != len(names) or any(name not in headers for name in names):
        raise ValueError('selected columns must be present and distinct')
    columns = [headers.index(name) for name in names]
    rows, seen = [], set()
    for line, values in enumerate(reader, 2):
        if len(values) != len(headers):
            raise ValueError(f'CSV row {line}: wrong number of fields; blank rows are not silently dropped')
        label = clean(values[columns[0]], f'row {line} label', 160)
        if label in seen:
            raise ValueError(f'duplicate displayed label: {label}')
        seen.add(label)
        value_text = values[columns[1]].strip()
        value = number(value_text, f'row {line} value')
        lo = number(values[columns[2]].strip(), f'row {line} lower') if args.lower else value
        hi = number(values[columns[3]].strip(), f'row {line} upper') if args.upper else value
        if not lo <= value <= hi:
            raise ValueError(f'row {line}: supplied interval must contain its value')
        rows.append((label, value, lo, hi, value_text))
        if len(rows) > MAX_ROWS:
            raise ValueError('More than 30 rows: choose a purposeful view or another chart tool, without hiding excluded rows')
    if not rows:
        raise ValueError('CSV has no data rows')
    return digest, rows


def render(args, digest, rows):
    title = clean(args.title, 'title', 160)
    caption = clean(args.caption, 'caption', 600)
    unit = clean(args.unit, 'unit', 80)
    source = clean(args.source, 'source', 300)
    alt = clean(args.alt, 'alt', 800)
    minimum = min(Decimal(0), *(r[2] for r in rows))
    maximum = max(Decimal(0), *(r[3] for r in rows))
    if minimum == maximum:
        minimum, maximum = Decimal(-1), Decimal(1)
    # Positions only; exact input strings remain the displayed point labels.
    with localcontext() as ctx:
        ctx.prec = 50
        span = maximum - minimum
        def x(v):
            return 335 + float((v - minimum) / span) * 485
        title_lines = textwrap.wrap(title, 85)
        top = 45 + 25 * len(title_lines)
        y = top + 42
        placements = []
        for row in rows:
            label_lines = textwrap.wrap(row[0], 34)
            placements.append((row, y, label_lines))
            y += max(40, len(label_lines) * 20 + 12)
        axis_y = y
        caption_lines = textwrap.wrap(caption, 112)
        source_lines = textwrap.wrap('Source: ' + source, 112)
        height = axis_y + 75 + 20 * (len(caption_lines) + len(source_lines))
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title description">',
                 f'<title id="title">{escape(title)}</title>',
                 f'<desc id="description">{escape(alt)} Values in {escape(unit)}. ' + escape('; '.join(f'{r[0]}: {r[4]}' + (f', interval {r[2]} to {r[3]}' if args.lower else '') for r in rows)) + '</desc>',
                 '<metadata>' + escape(json.dumps({'source_file': Path(args.csv).name, 'source_sha256': digest, 'label_column': args.label, 'value_column': args.value, 'lower_column': args.lower, 'upper_column': args.upper, 'rows': len(rows), 'scope': 'rendered supplied values; not statistical or semantic verification'}, ensure_ascii=False)) + '</metadata>',
                 '<rect width="100%" height="100%" fill="white"/>',
                 '<g font-family="DejaVu Sans, sans-serif" fill="#172b3a">']
        def text(px, py, content, size=15, extra=''):
            return f'<text x="{px}" y="{py}" font-size="{size}" {extra}>{escape(str(content))}</text>'
        for i, line in enumerate(title_lines):
            parts.append(text(28, 32 + i * 25, line, 21, 'font-weight="bold"'))
        parts.append(text(335, top, unit, 14))
        # Round tick values (1, 2, 2.5 or 5 x 10^n) inside the unchanged plotting domain, so labels stay readable.
        raw = span / Decimal(5)
        mag = Decimal(10) ** raw.adjusted()
        step = next(m * mag for m in (Decimal(1), Decimal(2), Decimal('2.5'), Decimal(5), Decimal(10)) if m * mag >= raw)
        tick = (minimum / step).to_integral_value(rounding=ROUND_CEILING) * step
        while tick <= maximum:
            px = x(tick)
            parts.append(f'<line x1="{px:.3f}" y1="{top+16}" x2="{px:.3f}" y2="{axis_y-14}" stroke="#d7dfe5"/>')
            parts.append(text(f'{px:.3f}', axis_y+8, format(tick.normalize(), 'f'), 12, 'text-anchor="middle"'))
            tick += step
        for (label, value, lo, hi, value_text), py, label_lines in placements:
            for j, line in enumerate(label_lines):
                parts.append(text(28, py + j * 20, line))
            if args.lower:
                parts.append(f'<line x1="{x(lo):.3f}" y1="{py-5}" x2="{x(hi):.3f}" y2="{py-5}" stroke="#126b74" stroke-width="3"/>')
            parts.append(f'<circle cx="{x(value):.3f}" cy="{py-5}" r="5" fill="#126b74"/>')
            parts.append(text(845, py, value_text))
        py = axis_y + 42
        for line in caption_lines + source_lines:
            parts.append(text(28, py, line, 13)); py += 20
        parts.extend(['</g>', '</svg>'])
        return '\n'.join(parts) + '\n'


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('csv', help='checked UTF-8 CSV; explicit file only')
    for field in ['label', 'value', 'unit', 'title', 'caption', 'source', 'alt', 'out']:
        p.add_argument('--'+field, required=True)
    p.add_argument('--lower'); p.add_argument('--upper')
    p.add_argument('--expect-sha256', help='optional exact source hash for frozen or resumed work')
    a = p.parse_args(argv)
    try:
        if bool(a.lower) != bool(a.upper):
            raise ValueError('--lower and --upper must be supplied together')
        if a.expect_sha256 and (len(a.expect_sha256) != 64 or any(c not in '0123456789abcdefABCDEF' for c in a.expect_sha256)):
            raise ValueError('--expect-sha256 must be a 64-character hex SHA256')
        digest, rows = load(a)
        svg = render(a, digest, rows)
        ET.fromstring(svg)  # Reject XML-forbidden text before creating any output.
        # Build everything before writing; an existing file or link is never replaced.
        with open(a.out, 'x', encoding='utf-8') as f:
            f.write(svg)
        print(json.dumps({'status': 'rendered', 'output': a.out, 'source_sha256': digest, 'rows': len(rows), 'verified': 'CSV shape, numeric/interval consistency and requested identity only', 'unverified': ['source truth', 'statistical validity', 'caption support', 'visual inspection', 'publication authority']}))
        return 0
    except (OSError, ValueError, UnicodeError, csv.Error, ArithmeticError, ET.ParseError) as exc:
        print(json.dumps({'status': 'error', 'error': str(exc)}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
