// Preserve nested identities; reject ambiguous legacy basename references.
import {copyFileSync,existsSync,mkdirSync,readFileSync,writeFileSync} from 'node:fs';
import {basename,dirname,join} from 'node:path';
import {inside,hashFile} from './safety.mjs';
export function basenamesFromCandidates(value) {
 return typeof value==='string'?value.split(';').map(s=>s.split(/\s+[—–-]\s+/)[0].trim()).filter(Boolean):[];
}
export function stageAssets({hyperframesDir,frames}) {
 const wanted=new Set(frames.flatMap(f=>basenamesFromCandidates(f.extra?.asset_candidates)));
 const anomalies=[], mappings=[]; let staged=0;
 const statePath=inside(hyperframesDir,'.hyperframes/staged-assets.json');
 const old=existsSync(statePath)?JSON.parse(readFileSync(statePath,'utf8')):{};
 for(const ref of wanted){
  try{
   const relative=ref.replace(/^assets\//,''); if(!relative||relative.startsWith('/')||relative.split('/').includes('..'))throw Error('unsafe asset reference '+ref);
   const dest=inside(hyperframesDir,'assets/'+relative);
   const choices=['capture/assets','capture/assets/videos','capture/screenshots'].map(d=>inside(hyperframesDir,d+'/'+relative)).filter(existsSync);
   const unique=[...new Map(choices.map(p=>[hashFile(p),p])).values()];
   if(unique.length>1)throw Error('ambiguous same-basename asset '+ref+'; use explicit nested capture paths');
   if(!unique.length){if(existsSync(dest)&&!old[ref]){staged++;continue;}throw Error('required asset missing: '+ref);}
   const src=unique[0],sha=hashFile(src);
   if(existsSync(dest)&&!old[ref]&&hashFile(dest)!==sha)throw Error('destination is an unowned different asset: '+ref);
   mkdirSync(dirname(dest),{recursive:true});if(!existsSync(dest)||hashFile(dest)!==sha)copyFileSync(src,dest);
   old[ref]={source:src,path:'assets/'+relative,sha256:sha};mappings.push(old[ref]);staged++;
  }catch(e){anomalies.push(e.message);}
 }
 mkdirSync(dirname(statePath),{recursive:true});writeFileSync(statePath,JSON.stringify(old,null,2)+'\n');
 return {staged,wanted,anomalies,mappings};
}
