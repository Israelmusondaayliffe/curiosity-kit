/** Graphic-overlay stage geometry. No I/O, cropping, dependency installation or implicit layout selection. */
const rect=(x,y,width,height)=>({x,y,width,height});
const positive=(v,name)=>{if(!Number.isFinite(v)||v<=0)throw new RangeError(`${name} must be positive and finite`);return v;};
export function zoneBounds(zone,width,height){
 positive(width,'width');positive(height,'height');const portrait=height>width;
 switch(zone){
  case 'fullscreen':case 'video-overlay':return rect(0,0,width,height);
  case 'lower-third':{const y=Math.round(height*.7);return rect(0,y,width,height-y);}
  case 'side-panel':{if(portrait){const y=Math.round(height*.6);return rect(0,y,width,height-y);}const x=Math.round(width*.58);return rect(x,0,width-x,height);}
  case 'whiteboard-area':{if(portrait){const y=Math.round(height*.55);return rect(0,y,width,height-y);}const m=Math.min(40,width/10,height/10);return rect(m,m,width-2*m,height-2*m);}
  default:throw new RangeError(`Unknown zone: ${zone}`);
 }
}
export function layoutBounds(layout,width,height,sourceWidth=width,sourceHeight=height,corner='top-right'){
 [width,height,sourceWidth,sourceHeight].forEach((v,i)=>positive(v,['width','height','sourceWidth','sourceHeight'][i]));
 const portrait=height>width,full=rect(0,0,width,height);
 if(layout==='split'){
  if(portrait){const half=Math.floor(height/2);return {zone:'side-panel',card:rect(0,0,width,half),video:rect(0,half,width,height-half),videoZ:1,cardZ:2};}
  const half=Math.floor(width/2);return {zone:'side-panel',card:rect(0,0,half,height),video:rect(half,0,width-half,height),videoZ:1,cardZ:2};
 }
 if(layout==='stack'){
  const m=portrait?0:Math.round(14*width/1920),gap=Math.max(1,Math.round(14*height/1080));
  const vh=Math.round(height*(portrait?844/1920:548/1080)),y=m+vh+gap;
  return {zone:'lower-third',video:rect(m,m,width-2*m,vh),card:rect(m,y,width-2*m,height-y-m),videoZ:1,cardZ:2};
 }
 if(layout==='pip'){
  if(!['top-left','top-right','bottom-left','bottom-right'].includes(corner))throw new RangeError('Unknown PiP corner');
  const aspect=sourceWidth/sourceHeight,sourcePortrait=aspect<1,scale=width/(portrait?1080:1920);
  const margin=Math.min(28*scale,width/10,height/10);
  const preferredWidth=(portrait?(sourcePortrait?312:360):(sourcePortrait?248:460))*scale;
  const w=Math.min(preferredWidth,width-2*margin,(height-2*margin)*aspect),h=w/aspect;
  return {zone:'fullscreen',card:full,video:rect(corner.endsWith('right')?width-w-margin:margin,corner.startsWith('bottom')?height-h-margin:margin,w,h),videoZ:4,cardZ:2};
 }
 if(layout==='overlay'){
  const glass=portrait?rect(24*width/1080,1280*height/1920,1032*width/1080,564*height/1920):rect(48*width/1920,460*height/1080,660*width/1920,540*height/1080);
  return {zone:'video-overlay',video:full,card:full,glass,videoZ:1,gradientZ:2,cardZ:3};
 }
 throw new RangeError(`Unknown layout: ${layout}`);
}
export function frameInsets(frame,width,height){
 positive(width,'width');positive(height,'height');
 if(frame==='clean'||frame==='hairline')return rect(0,0,width,height);
 if(frame!=='polaroid')throw new RangeError(`Unknown frame: ${frame}`);
 // All values are local to one outer #video-wrap; shrink chrome proportionally for small frames.
 const s=Math.min(1,width/480,height/360),edge=24*s,photoPad=14*s,caption=64*s;
 return rect(edge+photoPad,edge+photoPad,width-2*(edge+photoPad),height-2*edge-photoPad-caption);
}
export function cssBounds({x,y,width,height}){return {left:x,top:y,width,height};}
