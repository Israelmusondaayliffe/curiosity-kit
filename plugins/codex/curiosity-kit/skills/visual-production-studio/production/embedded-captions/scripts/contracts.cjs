/* Local input/evidence boundaries. No downloads, source adoption, or global cache writes. */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const cp = require('child_process');
function positive(v, name) { if (typeof v !== 'number' || !Number.isFinite(v) || v <= 0) throw Error(`${name} must be a finite positive number`); return v; }
function rate(v) {
  const s = String(v).trim();
  if (!/^\d+(?:\.\d+)?(?:\/\d+(?:\.\d+)?)?$/.test(s)) throw Error(`Invalid frame rate: ${s}`);
  const [n,d='1'] = s.split('/').map(Number); return positive(n/d, 'frame rate');
}
function fps(project, fallback=24) { const f=path.join(project,'matte.fps'); return rate(fs.existsSync(f)?fs.readFileSync(f,'utf8'):fallback); }
function scriptJSON(v,...rest) { return JSON.stringify(v,...rest).replace(/</g,'\\u003c').replace(/>/g,'\\u003e').replace(/&/g,'\\u0026').replace(/\u2028/g,'\\u2028').replace(/\u2029/g,'\\u2029'); }
function hash(f) { return crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex'); }
function source(project) {
 const f=path.join(project,'source.mp4');
 if (!fs.existsSync(f) || !fs.statSync(f).isFile()) throw Error('BLOCKED: designate one authoritative source.mp4 before parallel preparation; generated videos are never adopted');
 return f;
}
function duration(project) { return positive(Number(cp.execFileSync('ffprobe',['-v','error','-show_entries','format=duration','-of','csv=p=0',source(project)],{encoding:'utf8'}).trim()),'source duration'); }
function transcript(d, dur=Infinity) {
 if (!d || !Array.isArray(d.words) || !d.words.length) throw Error('transcript.words must be nonempty');
 let prev=-1;
 for (const [i,w] of d.words.entries()) {
  if (!w || typeof (w.text??w.word)!=='string' || !(w.text??w.word).trim() || !Number.isFinite(w.start) || !Number.isFinite(w.end) || w.start<0 || w.end<=w.start || w.start<prev || w.end>dur+0.05) throw Error(`invalid transcript word ${i}: ordered nonempty text and finite in-bounds timing required`);
  prev=w.end;
 }
 return d;
}
function id(s) { if (typeof s!=='string' || !/^[a-z][a-z0-9_-]*$/i.test(s)) throw Error(`invalid identifier: ${s}`); return s; }
function lines(x) { if (!Array.isArray(x)||!x.length||x.some(a=>!Array.isArray(a)||!a.length||a.some(w=>typeof w!=='string'||!w.trim()))) throw Error('lines must contain nonempty arrays of nonempty words; all-hero/no-body themes require a separately qualified branch'); }
function cache(project,stage,options,artifacts) {
 const key={source_sha256:hash(source(project)),options,node:process.version,contract:1}; const f=path.join(project,`_cache-${id(stage)}.json`);let prior=null;try{prior=JSON.parse(fs.readFileSync(f,'utf8'))}catch{}
 const exists=artifacts.some(a=>fs.existsSync(path.join(project,a)));
 if (exists && (!prior||JSON.stringify(prior.key)!==JSON.stringify(key)||!prior.complete)) throw Error(`BLOCKED: ${stage} cache is stale/unbound/incomplete. Preserve old artifacts and use a fresh isolated project.`);
 return {key,complete(){fs.writeFileSync(f,JSON.stringify({key,complete:true,artifacts},null,2)+'\n')},hit:exists};
}
function requireSuccess(r,label) { if (r.error || r.signal || r.status!==0) throw Error(`BLOCKED: ${label} did not complete (status=${r.status}, signal=${r.signal||'none'}): ${r.error?.message||r.stderr||''}`); return r; }
function measured(cpModule,command,args,options) {
 const i=args.findIndex(a=>/measure-layout\.cjs$/.test(a));
 if(i<0) return requireSuccess(cpModule.spawnSync(command,args,options),'compiler child');
 const project=args[i+1], f=path.join(project,'_layout.json'), before=Date.now();
 if(fs.existsSync(f)) fs.renameSync(f,path.join(project,`_layout.previous-${process.pid}-${before}.json`));
 const result=requireSuccess(cpModule.spawnSync(command,args,options),'layout measurement');
 if(!fs.existsSync(f)||fs.statSync(f).mtimeMs<before-1000) throw Error('BLOCKED: layout measurement is absent/stale');
 const d=JSON.parse(fs.readFileSync(f,'utf8'));if(!Array.isArray(d.samples)||!d.samples.length)throw Error('BLOCKED: layout has zero samples');return result;
}
function manifest(project,mode,names,details={}) {
 const inputs={};for(const n of ['source.mp4','transcript.json','theme.json','plan.json','cinematic.json','matte.fps'])if(fs.existsSync(path.join(project,n)))inputs[n]=hash(path.join(project,n));
 const outputs={};for(const n of names)outputs[n]=hash(path.join(project,n));
 fs.writeFileSync(path.join(project,'_caption-output.json'),JSON.stringify({schema:1,mode,inputs,outputs,...details,render_status:'UNRUN',glyph_review:'UNRUN'},null,2)+'\n');
}
function boundArtifact(project,name,d) {
 const f=path.join(project,name),src=path.join(project,'source.mp4');
 if(fs.existsSync(f) && !d)throw Error(`BLOCKED: invalid ${name}`);
 if(d && fs.existsSync(src) && d.source_sha256!==hash(src))throw Error(`BLOCKED: stale/unbound ${name}; regenerate from current source`);
 return d;
}
function checkManifest(project) {
 const m=JSON.parse(fs.readFileSync(path.join(project,'_caption-output.json'),'utf8'));
 for(const [n,h] of Object.entries({...m.inputs,...m.outputs}))if(!fs.existsSync(path.join(project,n))||hash(path.join(project,n))!==h)throw Error(`BLOCKED: changed/missing declared artifact ${n}; recompile`);
 for(const n of ['index.html','rail.html','index_fg.html'])if(fs.existsSync(path.join(project,n))&&!m.outputs[n])throw Error(`BLOCKED: orphan layer ${n}; preserve it outside the active project before rendering`);
 return m;
}
module.exports={positive,rate,fps,scriptJSON,hash,source,duration,transcript,id,lines,cache,requireSuccess,measured,manifest,checkManifest,boundArtifact};
if(require.main===module){const [cmd,p,arg]=process.argv.slice(2);try{if(cmd==='fps')console.log(fps(p,arg||24));else if(cmd==='source')console.log(source(p));else if(cmd==='manifest')checkManifest(p);else if(cmd==='rail-applicability')console.log(checkManifest(p).rail_handoff===false?'not_applicable':'required');else throw Error('usage: contracts.cjs fps|source|manifest PROJECT')}catch(e){console.error(e.message);process.exit(3)}}
