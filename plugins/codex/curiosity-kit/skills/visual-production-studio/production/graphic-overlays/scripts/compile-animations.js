/* Graphic-overlay declarative animations. Requires caller-provided local GSAP and DOM. */
(function(global){
 'use strict';
 const kinds=['fade-in','fade-out','slide-in','kinetic-chars','typewriter','count-up','draw-path','grow-y','grow-x','scale-pop','blur-in','mask-reveal','morph-to','blink'];
 const num=(value,fallback,name)=>{const n=value===undefined?fallback:Number(value);if(!Number.isFinite(n))throw new TypeError(`${name} must be finite`);return n;};
 function compileCard(tl,host,{startSec,endSec,fps,transition='fade'}){
  if(!Number.isFinite(fps)||fps<=0||!Number.isFinite(startSec)||startSec<0||!Number.isFinite(endSec)||endSec<=startSec)throw new RangeError('Invalid card interval or fps');
  const q=t=>Math.round(t*fps)/fps,start=q(startSec),end=Math.floor(endSec*fps)/fps;
  if(end<=start)throw new RangeError('Card has no complete output frame');
  if(!['cut','fade','slide','wipe'].includes(transition))throw new RangeError('Unknown card transition');
  const enter=Math.min(q(.4),(end-start)/3),exit=Math.min(q(.35),(end-start)/3);
  tl.set(host,{visibility:'hidden',opacity:0},0);
  tl.set(host,{visibility:'visible'},start);
  const hostFrom={opacity:transition==='cut'?1:0},hostTo={opacity:1,duration:transition==='cut'?0:enter,ease:'power2.out',immediateRender:false};
  if(transition==='slide'){hostFrom.y=24;hostTo.y=0;}
  if(transition==='wipe'){hostFrom.clipPath='inset(0 100% 0 0)';hostTo.clipPath='inset(0 0% 0 0)';}
  tl.fromTo(host,hostFrom,hostTo,start);
  for(const el of host.querySelectorAll('[data-anim]')){
   const a=el.dataset,kind=a.anim;if(!kinds.includes(kind))throw new RangeError(`Unknown data-anim: ${kind}`);
   const at=num(a.animAt,0,'at');if(at<0)throw new RangeError('Animation offset must not be negative');
   const t=q(startSec+at);if(t>=end)throw new RangeError(`Animation ${kind} starts outside card`);
   const requested=num(a.animDuration,.45,'duration');if(requested<0)throw new RangeError('Duration must not be negative');
   const d=Math.min(Math.max(0,q(requested)),end-t),ease=a.animEase||'power2.out';
   const fromTo=(target,from,to)=>{tl.set(target,from,0);tl.fromTo(target,from,{...to,duration:d,ease:to.ease||ease,immediateRender:false},t);};
   if(kind==='fade-in')fromTo(el,{opacity:0},{opacity:1});
   else if(kind==='fade-out')fromTo(el,{opacity:1},{opacity:0});
   else if(kind==='slide-in'){
    const direction=a.animFrom||'left',dist=num(a.animDistance,80,'distance');
    if(!['left','right','top','bottom'].includes(direction))throw new RangeError('Unknown slide direction');
    const axis=['left','right'].includes(direction)?'x':'y';fromTo(el,{opacity:0,[axis]:['left','top'].includes(direction)?-dist:dist},{opacity:1,[axis]:0});
   }else if(kind==='kinetic-chars'||kind==='typewriter'){
    const chars=Array.from(el.querySelectorAll('.char'));if(!chars.length)throw new Error(`${kind} requires .char children`);
    const stagger=num(a.animStagger,kind==='typewriter'?.08:.04,'stagger');if(stagger<0)throw new RangeError('Stagger must not be negative');
    const pattern=a.animPattern||(kind==='typewriter'?'fade':'pop');if(!['fade','pop'].includes(pattern))throw new RangeError('Unknown character pattern');
    chars.forEach((char,i)=>{const ct=q(t+i*stagger);if(ct>=end)throw new RangeError('Character reveal extends beyond card');const from=pattern==='pop'?{opacity:0,y:8,scale:.8}:{opacity:0};tl.set(char,from,0);tl.fromTo(char,from,{opacity:1,...(pattern==='pop'?{y:0,scale:1}:{}),duration:Math.min(d,end-ct),ease,immediateRender:false},ct);});
   }else if(kind==='count-up'){
    const from=num(a.animFrom,0,'from'),to=num(a.animTo,100,'to'),fmt=a.animFormat||',d';
    if(!/^\.[0-6]f$/.test(fmt)&&fmt!==',d')throw new RangeError('Unsupported number format');
    const format=v=>fmt===',d'?Math.round(Number(v)).toLocaleString('en-US'):Number(v).toFixed(Number(fmt[1]));
    tl.set(el,{textContent:format(from)},0);
    tl.fromTo(el,{textContent:from},{textContent:to,duration:d,ease,immediateRender:false,modifiers:{textContent:format}},t);
   }else if(kind==='draw-path'){
    if(typeof el.getTotalLength!=='function')throw new TypeError('draw-path requires an SVG geometry element');
    const length=el.getTotalLength();fromTo(el,{strokeDasharray:length,strokeDashoffset:length},{strokeDashoffset:0});
   }else if(kind==='grow-x'||kind==='grow-y'){
    const prop=kind==='grow-x'?'width':'height',n=num(kind==='grow-x'?a.animTargetW:a.animTargetH,undefined,'grow target');if(n<0)throw new RangeError('Grow target must not be negative');fromTo(el,{[prop]:0},{[prop]:n});
   }else if(kind==='scale-pop')fromTo(el,{opacity:0,scale:.6},{opacity:1,scale:1,ease:a.animEase||'back.out(1.6)'});
   else if(kind==='blur-in')fromTo(el,{opacity:0,filter:'blur(16px)'},{opacity:1,filter:'blur(0px)'});
   else if(kind==='mask-reveal'){
    const masks={left:'inset(0 100% 0 0)',right:'inset(0 0 0 100%)',top:'inset(0 0 100% 0)',bottom:'inset(100% 0 0 0)'};
    const mask=masks[a.animDirection||'left'];if(!mask)throw new RangeError('Unknown mask direction');fromTo(el,{clipPath:mask},{clipPath:'inset(0% 0% 0% 0%)'});
   }else if(kind==='morph-to'){
    const props=JSON.parse(a.animProps||'{}'),allowed=new Set(['x','y','scale','scaleX','scaleY','rotation','opacity','width','height','color','backgroundColor','borderRadius','filter','clipPath','backgroundPosition','backgroundSize','borderColor','borderWidth','boxShadow','textShadow','letterSpacing','lineHeight','fontSize','padding','margin','left','top','right','bottom','transformOrigin','stroke','fill','strokeWidth']);
    const supportedProperty=(k,v)=>allowed.has(k)||(typeof global.CSS?.supports==='function'&&!/^(animation|transition|on[A-Z]|__proto__|constructor|prototype)/.test(k)&&global.CSS.supports(k.startsWith('--')?k:k.replace(/[A-Z]/g,c=>'-'+c.toLowerCase()),String(v)));
    if(!props||Array.isArray(props)||typeof props!=='object'||!Object.keys(props).length||Object.entries(props).some(([k,v])=>!supportedProperty(k,v)))throw new TypeError('morph-to accepts visual CSS supported by this browser, excluding autonomous animation, transition and executable GSAP controls');
    if(Object.values(props).some(v=>(typeof v==='string'&&/url\s*\(|expression\s*\(|@import/i.test(v))||(typeof v!=='string'&&!(typeof v==='number'&&Number.isFinite(v)))))throw new TypeError('Invalid morph value');
    tl.to(el,{...props,duration:d,ease},t);
   }else if(kind==='blink'){
    const period=num(a.animPeriod,1,'blink period');if(period<2/fps)throw new RangeError('Blink period needs at least two output frames');
    tl.set(el,{opacity:1},0);const halfFrames=Math.max(1,Math.round(period*fps/2)),firstFrame=Math.round(t*fps),endFrame=Math.floor(end*fps);
    for(let frame=firstFrame+halfFrames,n=1;frame<endFrame;frame+=halfFrames,n++)tl.set(el,{opacity:n%2?0:1},frame/fps);
   }
  }
  if(transition!=='cut')tl.to(host,{opacity:0,duration:exit,ease:'power2.in'},end-exit);
  tl.set(host,{visibility:'hidden',opacity:0},end);
  return tl;
 }
 const api={compileCard,kinds};if(typeof module!=='undefined'&&module.exports)module.exports=api;global.GraphicOverlayAnimations=api;
})(typeof globalThis!=='undefined'?globalThis:window);
