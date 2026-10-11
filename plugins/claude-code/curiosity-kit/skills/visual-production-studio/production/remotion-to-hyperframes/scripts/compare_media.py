#!/usr/bin/env python3
"""Local paired-video diagnostics. No rescale/retime/installation/network actions."""
import argparse
from fractions import Fraction
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


def call(args, **kwargs):
    return subprocess.run(list(map(str, args)), check=True, **kwargs)


def probe(path):
    p = Path(path).resolve(strict=True)
    raw = call(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames',
                '-show_streams', '-show_format', '-of', 'json', p], capture_output=True, text=True)
    obj = json.loads(raw.stdout)
    if not obj.get('streams'):
        raise ValueError(f'No video stream: {p}')
    stream = obj['streams'][0]
    fps = Fraction(stream.get('avg_frame_rate', '0/1'))
    rate = Fraction(stream.get('r_frame_rate', '0/1'))
    if fps <= 0 or rate != fps:
        raise ValueError(f'Unsupported unknown or variable frame rate: {p}')
    count = int(stream.get('nb_read_frames', 0))
    duration = float(stream.get('duration') or obj.get('format', {}).get('duration', 0))
    if count < 1 or not math.isfinite(duration) or duration <= 0:
        raise ValueError(f'Invalid video duration/frame count: {p}')
    # Decode timestamps as a second CFR check; matching nominal rates alone are not proof.
    times_raw = call(['ffprobe','-v','error','-select_streams','v:0','-show_frames',
                      '-show_entries','frame=best_effort_timestamp_time','-of','json',p],
                     capture_output=True,text=True)
    frames = json.loads(times_raw.stdout).get('frames', [])
    times = [float(f['best_effort_timestamp_time']) for f in frames
             if 'best_effort_timestamp_time' in f]
    if len(times) != count or not all(math.isfinite(t) for t in times):
        raise ValueError(f'Incomplete decoded frame timestamps: {p}')
    step = 1 / float(fps)
    if any(abs((b-a)-step) > max(0.00001,step*0.005) for a,b in zip(times,times[1:])):
        raise ValueError(f'Variable decoded timestamp spacing unsupported: {p}')
    if abs(duration-count/float(fps)) > max(0.002, step/2):
        raise ValueError(f'Duration inconsistent with decoded frames: {p}')
    return {'path':str(p),'width':int(stream['width']),'height':int(stream['height']),
            'fps':str(fps),'frame_count':count,'duration':duration,
            'start_time':times[0], 'pix_fmt':stream.get('pix_fmt','unknown'),
            'color_space':stream.get('color_space','unknown'),
            'color_range':stream.get('color_range','unknown'),
            'color_transfer':stream.get('color_transfer','unknown'),
            'color_primaries':stream.get('color_primaries','unknown')}


def preflight(a,b):
    left,right = probe(a),probe(b)
    mismatch = {k:[left[k],right[k]] for k in ('width','height','fps','frame_count','pix_fmt',
                'color_space','color_range','color_transfer','color_primaries') if left[k]!=right[k]}
    tol=max(0.002,0.5/float(Fraction(left['fps'])))
    if abs(left['duration']-right['duration']) > tol:
        mismatch['duration']=[left['duration'],right['duration']]
    if abs(left['start_time']-right['start_time']) > 0.00001:
        mismatch['start_time']=[left['start_time'],right['start_time']]
    meta={'baseline':left,'translated':right,'mismatches':mismatch,
          'color_metadata_complete':all(left[k]!='unknown' for k in
             ('color_space','color_range','color_transfer','color_primaries'))}
    return meta


def diff(meta,out,threshold):
    if not math.isfinite(threshold) or not 0<=threshold<=1:
        raise ValueError('SSIM threshold must be a finite number from 0 to 1')
    # Run in output directory so FFmpeg's filter filename parser sees a safe fixed name.
    # Use argument arrays throughout; filenames never enter shell or filter expressions.
    args=['ffmpeg','-y','-hide_banner','-nostats','-loglevel','info',
          '-i',meta['baseline']['path'],'-i',meta['translated']['path'],
          '-filter_complex','[0:v][1:v]ssim=stats_file=ssim.log',
          '-an','-f','null','-']
    with (out/'ffmpeg.stderr').open('w') as log:
        call(args,cwd=out,stderr=log,stdout=subprocess.DEVNULL)
    values=[]
    for line in (out/'ssim.log').read_text().splitlines():
        hit=re.search(r'\bn:(\d+).*?All:([-\d.]+)',line)
        if hit:
            value=float(hit[2])
            if not math.isfinite(value):raise ValueError('Nonfinite SSIM sample')
            values.append({'frame':int(hit[1])-1,'ssim':value})
    expected=meta['baseline']['frame_count']
    if len(values)!=expected or [v['frame'] for v in values]!=list(range(expected)):
        raise ValueError('SSIM samples do not cover every decoded frame exactly once')
    ordered=sorted(v['ssim'] for v in values);n=len(ordered);mean=sum(ordered)/n
    result={'status':'PASS' if mean>=threshold else 'FAIL','scope':'video SSIM only',
            'pass':mean>=threshold,'frame_count':n,'mean':round(mean,6),'min':ordered[0],
            'max':ordered[-1],'p05':ordered[min(n-1,int(.05*n))],
            'p95':ordered[min(n-1,int(.95*n))],'threshold':threshold,'metadata':meta,
            'worst_frames':sorted(values,key=lambda v:v['ssim'])[:min(10,n)]}
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return 0 if result['pass'] else 1


def strip(meta,out,samples):
    count=meta['baseline']['frame_count']
    if not 1<=samples<=count:
        raise ValueError(f'samples must be an integer from 1 to frame count {count}')
    frames=[0] if samples==1 else [round(i*(count-1)/(samples-1)) for i in range(samples)]
    if len(set(frames))!=samples:raise ValueError('Sample indices must be distinct')
    fps=float(Fraction(meta['baseline']['fps']))
    pairs=[{'row':i,'frame':f,'seconds':f/fps} for i,f in enumerate(frames)]
    (out/'samples.json').write_text(json.dumps(pairs,indent=2)+'\n')
    (out/'timestamps.txt').write_text(''.join(f"{f/fps:.9f}\n" for f in frames))
    n=len(frames);parts=[]
    # Split first, then select ONE different frame for EACH branch. Selecting before
    # splitting duplicates the same stream and yields identical first-frame rows.
    for stream,prefix in [(0,'b'),(1,'t')]:
        if n==1:parts.append(f'[{stream}:v]select=eq(n\\,{frames[0]}),setpts=PTS-STARTPTS[{prefix}0]')
        else:
            parts.append(f'[{stream}:v]split={n}'+''.join(f'[{prefix}s{i}]' for i in range(n)))
            for i,f in enumerate(frames):
                parts.append(f'[{prefix}s{i}]select=eq(n\\,{f}),setpts=PTS-STARTPTS[{prefix}{i}]')
    for i in range(n):parts.append(f'[b{i}][t{i}]hstack=inputs=2[row{i}]')
    if n==1:parts.append('[row0]null[out]')
    else:parts.append(''.join(f'[row{i}]' for i in range(n))+f'vstack=inputs={n}[out]')
    with (out/'ffmpeg.stderr').open('w') as log:
        call(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',meta['baseline']['path'],
              '-i',meta['translated']['path'],'-filter_complex',';'.join(parts),
              '-map','[out]','-frames:v','1',out/'strip.png'],stderr=log,stdout=subprocess.DEVNULL)
    if not (out/'strip.png').is_file() or not (out/'strip.png').stat().st_size:
        raise ValueError('Strip output missing')
    print(f'wrote {out/"strip.png"} ({n} distinct sampled frame indices)')
    return 0


def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['diff','strip']);ap.add_argument('baseline')
    ap.add_argument('translated');ap.add_argument('output');ap.add_argument('--samples',type=int,default=8)
    args=ap.parse_args();out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
    may_write_error=True
    try:
        for binary in ['ffmpeg','ffprobe']:
            if not shutil.which(binary):raise ValueError(f'Missing dependency: {binary}')
        # Never overwrite a source through a colliding generated-output path.
        for source in (Path(args.baseline).resolve(),Path(args.translated).resolve()):
            if source in [out/name for name in ('summary.json','metadata.json','ssim.log','ffmpeg.stderr','strip.png','samples.json','timestamps.txt')]:
                may_write_error=False
                raise ValueError('Source path collides with diagnostic output')
        meta=preflight(args.baseline,args.translated)
        (out/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
        if meta['mismatches']:raise ValueError('Paired video metadata mismatch: '+json.dumps(meta['mismatches']))
        if args.mode=='diff':return diff(meta,out,float(os.environ.get('R2HF_SSIM_THRESHOLD','.85')))
        return strip(meta,out,args.samples)
    except (ValueError,KeyError,OSError,ZeroDivisionError,subprocess.CalledProcessError) as exc:
        result={'status':'ERROR','pass':False,'error':str(exc),'scope':'comparison setup'}
        if may_write_error:
            (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result),file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
