#!/usr/bin/env node
/* Container/media integrity gate. Does not claim visual, glyph or listening review. */
const fs=require('fs'),path=require('path'),cp=require('child_process'),g=require('./contracts.cjs');
const project=path.resolve(process.argv[2]||'.'),file=path.resolve(process.argv[3]||''),fps=g.rate(process.argv[4]||24);
function probe(f){return JSON.parse(cp.execFileSync('ffprobe',['-v','error','-count_frames','-show_streams','-show_format','-of','json',f],{encoding:'utf8'}));}
try{
 const d=probe(file),src=probe(g.source(project)),v=d.streams.find(s=>s.codec_type==='video'),sv=src.streams.find(s=>s.codec_type==='video');
 if(!v||!sv)throw Error('Missing video stream');const dur=g.positive(Number(d.format.duration),'output duration'),sd=g.positive(Number(src.format.duration),'source duration');
 if(Math.abs(dur-sd)>Math.max(.15,2/fps))throw Error(`Output/source duration mismatch: ${dur}/${sd}`);
 const plan=JSON.parse(fs.readFileSync(path.join(project,fs.existsSync(path.join(project,'theme.json'))?'theme.json':'plan.json'),'utf8'));
 if(v.width!==(plan.width??1280)||v.height!==(plan.height??720))throw Error('Output dimensions do not match current plan');
 if(Math.abs(g.rate(v.avg_frame_rate)-fps)>.01)throw Error('Output timebase differs from authoritative FPS');
 const frames=Number(v.nb_read_frames);if(!Number.isFinite(frames)||Math.abs(frames-dur*fps)>2)throw Error('Incomplete/unexpected frame count');
 if(src.streams.some(s=>s.codec_type==='audio')&&!d.streams.some(s=>s.codec_type==='audio'))throw Error('Source audio missing from output');
 const receipt={status:'PASS',scope:'container-duration-dimensions-fps-framecount-audio-presence',output:file,sha256:g.hash(file),source_sha256:g.hash(g.source(project)),duration:dur,width:v.width,height:v.height,fps:g.rate(v.avg_frame_rate),frames,motion_visual_audio_review:'UNRUN'};
 fs.writeFileSync(path.join(project,'_media-integrity.json'),JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt));
}catch(e){console.error('FAIL media integrity: '+e.message);process.exit(2)}
