// Local project boundaries and owned generated-artifact state.
import {existsSync, realpathSync, readFileSync, writeFileSync, mkdirSync, renameSync} from 'node:fs';
import {resolve, relative, dirname, isAbsolute, join} from 'node:path';
import {createHash} from 'node:crypto';
export const scriptJSON = value => JSON.stringify(value).replace(/[<>&\u2028\u2029]/g, c => '\\u'+c.charCodeAt(0).toString(16).padStart(4,'0'));
export const htmlAttr = value => String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function inside(root,path) {
 const base=resolve(root), dest=resolve(base,path); const rel=relative(base,dest);
 if(rel==='..'||rel.startsWith('../')||isAbsolute(rel)) throw Error('path escapes project: '+path);
 let ancestor=dest; while(!existsSync(ancestor)&&ancestor!==dirname(ancestor)) ancestor=dirname(ancestor);
 const realBase=existsSync(base)?realpathSync(base):base, real=realpathSync(ancestor), rr=relative(realBase,real);
 if(rr==='..'||rr.startsWith('../')||isAbsolute(rr)) throw Error('symlink escapes project: '+path);
 return dest;
}
export function artifactState(root) {const p=join(root,'.hyperframes/native-artifacts.json'); return existsSync(p)?JSON.parse(readFileSync(p,'utf8')):{};}
export function setArtifact(root,key,value) {const p=inside(root,'.hyperframes/native-artifacts.json'); mkdirSync(dirname(p),{recursive:true}); const s=artifactState(root); s[key]=value; const tmp=p+'.'+process.pid+'.tmp';writeFileSync(tmp,JSON.stringify(s,null,2)+'\n');renameSync(tmp,p);}
export const hashFile = p => createHash('sha256').update(readFileSync(p)).digest('hex');
