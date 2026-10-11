#!/usr/bin/env python3
"""Check saved prompt structure, not creative meaning or native provider support.

CLI accepts plain text or fenced prompt(s). Optional Seedance mode labels select
review hints, never a model upgrade or a live capability assertion. Exit 0 means
only structural checks passed; 1 malformed structure; 2 input/argument failure.
"""
from __future__ import annotations
import argparse
import pathlib
import re
import sys

MODES=('auto','text-to-video','continuous-one-take','beat-cut-music-video','omni-reference','first-last-frame','extension','visual-edit','audio-edit','ultra-long','storyboard','blockout','green-screen','clip-join')

def code_blocks(text):
    return re.findall(r'^```[^\n]*\n(.*?)^```\s*$',text,re.M|re.S)

def infer_mode(text):
    """Conservative routing hint; explicit mode is preferable to prose guessing."""
    match=re.search(r'^\s*Mode:\s*([^\n]+)',text,re.I|re.M)
    if match:
        value=match.group(1).strip().lower().replace(' ','-')
        if value in MODES and value!='auto':return value
    t=text.lower()
    if re.search(r'\baudio[- ]edit\b',t):return 'audio-edit'
    if re.search(r'\bedit\s+@video\d+',t):return 'visual-edit'
    if re.search(r'\bextend\s+@video\d+',t):return 'extension'
    if re.search(r'\b(single continuous|continuous unbroken|one-take)\b',t):return 'continuous-one-take'
    if re.search(r'\bfirst and last frame\b',t):return 'first-last-frame'
    if re.search(r'\bhard cuts?\b',t) and re.search(r'\bon (?:the )?beat\b',t):return 'beat-cut-music-video'
    return 'text-to-video'

def parse_timestamp(value):
    value=value.strip().rstrip('sS').strip()
    if ':' in value:
        minute,second=value.split(':',1)
        if not 0<=float(second)<60:raise ValueError('seconds component must be below 60')
        return int(minute)*60+float(second)
    return float(value)

def timeline_intervals(prompt):
    stamp=r'\d+(?::\d{2}(?:\.\d+)?|\.\d+)?\s*[sS]?'
    pattern=rf'\[\s*({stamp})\s*[-–]\s*({stamp})(?:\s*\|[^\]]*)?\s*\]'
    return [(parse_timestamp(a),parse_timestamp(b)) for a,b in re.findall(pattern,prompt)]

def declared_duration(prompt):
    patterns=(r'\b(?:full video|duration|total duration)\s*:\s*(\d+(?:\.\d+)?)\s*(?:s\b|seconds?\b)',r'\b(?:create|generate|make|produce)\b.{0,40}?\b(\d+(?:\.\d+)?)[ -]second\b')
    for pattern in patterns:
        m=re.search(pattern,prompt,re.I)
        if m:return float(m.group(1))
    return None

def check_timeline(prompt,errors):
    try:intervals=timeline_intervals(prompt)
    except ValueError as e:errors.append(str(e));return
    duration=declared_duration(prompt)
    if not intervals:return  # Untimed prose and sparse keyframes are legitimate.
    if abs(intervals[0][0])>0.001:errors.append('timeline must begin at 0')
    if any(a>=b for a,b in intervals):errors.append('timeline contains a non-positive interval')
    if any(abs(a[1]-b[0])>0.001 for a,b in zip(intervals,intervals[1:])):errors.append('timeline has a gap or overlap')
    if duration is not None and abs(intervals[-1][1]-duration)>0.001:errors.append(f'timeline must end at declared duration {duration:g}')

def check_references(prompt,errors):
    """Retained public helper. Prose roles require human review, not keyword gates."""
    return None

def validate_generic(text):
    errors=[]
    if not text.strip():return ['empty prompt']
    fences=re.findall(r'^```[^\n]*$',text,re.M)
    if len(fences)%2:errors.append('unclosed prompt fence')
    blocks=code_blocks(text)
    if fences and not blocks and not errors:errors.append('malformed prompt fences')
    if any(not block.strip() for block in blocks):errors.append('empty prompt block')
    for block in blocks or [text]:check_timeline(block,errors)
    return errors

def validate_seedance(text,selected_mode):
    if selected_mode not in MODES:return ['unknown mode'],selected_mode
    mode=infer_mode(text) if selected_mode=='auto' else selected_mode
    return validate_generic(text),mode

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('file');p.add_argument('--profile',choices=('generic','seedance-2.5'),default='generic');p.add_argument('--mode',choices=MODES,default='auto')
    a=p.parse_args()
    try:text=pathlib.Path(a.file).read_text(encoding='utf-8')
    except (OSError,UnicodeError) as e:print(f'INPUT_ERROR: {e}',file=sys.stderr);return 2
    errors,mode=validate_seedance(text,a.mode) if a.profile=='seedance-2.5' else (validate_generic(text),'generic')
    if errors:print('STRUCTURE_FAIL: '+'; '.join(errors));return 1
    print(f'STRUCTURE_OK [{a.profile}/{mode}]; provider support, reference roles, creative fidelity and rendered quality NOT VERIFIED')
    return 0
if __name__=='__main__':raise SystemExit(main())
