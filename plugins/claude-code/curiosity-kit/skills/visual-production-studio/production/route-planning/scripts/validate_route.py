#!/usr/bin/env python3
"""Check an optional saved production route; never render or select a model."""
import json
import sys
from pathlib import Path

ROUTES = {
    'faceless-explainer', 'product-launch', 'pr-story', 'website-capture',
    'music-visualization', 'slideshow', 'motion-graphics', 'general-video',
    'previs', 'previs-to-sequence',
}
PROMPT_ONLY_ROUTES = {'previs', 'previs-to-sequence'}
PROMPT_ONLY_RUNTIMES = {'prompt-only', 'external'}
RUNTIMES = {'hyperframes', 'remotion', 'prompt-only', 'external'}


def validate(data):
    if not isinstance(data, dict):
        return ['route document must be a JSON object']
    errors = []
    route, runtime = data.get('route'), data.get('runtime')
    if not isinstance(route, str) or route not in ROUTES:
        errors.append('route is invalid')
    if not isinstance(runtime, str) or runtime not in RUNTIMES:
        errors.append('runtime is invalid')
    if isinstance(route, str) and route in PROMPT_ONLY_ROUTES:
        if not isinstance(runtime, str) or runtime not in PROMPT_ONLY_RUNTIMES:
            errors.append('previs routes produce prompts; runtime must be prompt-only or external')
    for field in ('duration_seconds', 'width', 'height'):
        if type(data.get(field)) is not int or data[field] <= 0:
            errors.append(f'{field} must be a positive integer')
    selected = data.get('skills')
    if not isinstance(selected, list) or not selected:
        errors.append('skills must be a non-empty list')
    elif any(not isinstance(item, str) or not item.strip() for item in selected):
        errors.append('skills must contain non-empty owner identifiers')
    for field in ('objective', 'rationale'):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f'{field} must be non-empty')
    return errors


def main():
    if len(sys.argv) != 2:
        print('usage: validate_route.py ROUTE.json', file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f'invalid input: {exc}', file=sys.stderr)
        return 2
    errors = validate(data)
    print(json.dumps({'valid': not errors, 'errors': errors}, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
