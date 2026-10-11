import {openSync,writeSync,closeSync,renameSync,unlinkSync,copyFileSync,mkdirSync} from 'node:fs';
import {dirname} from 'node:path';
const LIMIT=256*1024*1024;
export async function freezeUrl(url,destPath,{maxBytes=LIMIT,timeoutMs=30000,fetchImpl=fetch,allowedHosts=null}={}) {
 if(!Number.isFinite(maxBytes)||maxBytes<=0||!Number.isFinite(timeoutMs)||timeoutMs<=0)throw Error('invalid download bounds');
 const check=v=>{const u=new URL(v);if(u.protocol!=='https:'||u.username||u.password)throw Error('freeze requires HTTPS without embedded credentials');if(allowedHosts&&!allowedHosts.includes(u.hostname))throw Error('unapproved download host');return u;};
 let current=check(url);const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),timeoutMs);let fd,tmp;
 try{
  let response;
  for(let i=0;i<5;i++){
   response=await fetchImpl(current.href,{signal:controller.signal,redirect:'manual'});
   if([301,302,303,307,308].includes(response.status)){if(!response.headers.get('location'))throw Error('redirect missing location');current=check(new URL(response.headers.get('location'),current).href);continue;}break;
  }
  if(!response?.ok)throw Error('freeze failed HTTP '+response?.status);
  const mime=(response.headers.get('content-type')||'').split(';')[0];
  if(!/^(image|audio|video)\//.test(mime)&&mime!=='application/octet-stream')throw Error('unexpected media type: '+mime);
  const length=Number(response.headers.get('content-length'));if(length>maxBytes)throw Error('download exceeds byte cap');
  if(!response.body)throw Error('empty response body');
  mkdirSync(dirname(destPath),{recursive:true});tmp=destPath+'.'+process.pid+'.partial';fd=openSync(tmp,'wx');let size=0;
  for await(const chunk of response.body){size+=chunk.length;if(size>maxBytes)throw Error('download exceeds byte cap');if(controller.signal.aborted)throw Error('download timeout');writeSync(fd,chunk);}
  if(!size)throw Error('empty response');closeSync(fd);fd=undefined;renameSync(tmp,destPath);tmp=undefined;return size;
 }finally{clearTimeout(timer);if(fd!==undefined)closeSync(fd);if(tmp)try{unlinkSync(tmp);}catch{}}
}
export function freezeLocalFile(srcPath,destPath){mkdirSync(dirname(destPath),{recursive:true});copyFileSync(srcPath,destPath);}
