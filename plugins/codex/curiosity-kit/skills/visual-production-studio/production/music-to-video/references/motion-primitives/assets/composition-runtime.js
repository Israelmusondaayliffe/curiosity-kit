/* Visual Production composition lifecycle. Standalone document/iframe scope.
 * GSAP remains separately licensed. No autonomous playback or network loading. */
(function(global){
  'use strict';
  const hooks=new Set(), cleanups=new Set(); let timeline=null, disposed=false, resolveReady, rejectReady;
  const ready=new Promise((resolve,reject)=>{resolveReady=resolve;rejectReady=reject});
  const api={ready,status:'preparing',hooks,addRender(fn){hooks.add(fn);return ()=>hooks.delete(fn)},addCleanup(fn){cleanups.add(fn)},
    repaint(){ if(!timeline||disposed)return; for(const child of timeline.getChildren(true,true,true)){const cb=child.eventCallback('onUpdate');if(cb)cb.apply(child,child.vars.onUpdateParams||[])}const own=timeline.eventCallback('onUpdate');if(own)own.call(timeline);for(const fn of hooks)fn(timeline.time());},
    seek(t){if(!timeline||disposed)throw Error('Composition is not ready');if(!Number.isFinite(t)||t<0||t>api.duration+1e-7)throw RangeError('Seek outside composition');timeline.totalTime(Math.min(t,api.duration),true);api.repaint();return api;},
    async register(id,tl){if(timeline)throw Error('One timeline per isolated composition');timeline=tl;global.__timelines=global.__timelines||{};global.__timelines[id]=tl;
      try{if(document.fonts)await document.fonts.ready;
      const urls=new Set();for(const node of document.querySelectorAll('[style]'))for(const match of node.style.cssText.matchAll(/url\(["']?([^"')]+)["']?\)/g))if(!match[1].startsWith('#'))urls.add(match[1]);
      await Promise.all([...urls].map(url=>new Promise((ok,fail)=>{const im=new Image();im.onload=ok;im.onerror=()=>fail(Error('Missing recipe texture: '+url));im.src=url})));
      const root=document.querySelector('[data-composition-id]');let declared=Number(root?.dataset.duration);if(!Number.isFinite(declared)||declared<=0)throw Error('Invalid declared duration');
      const duration=Math.max(declared,tl.totalDuration());if(!Number.isFinite(duration))throw Error('Infinite composition');api.duration=duration;api.id=id;api.timeline=tl;
      // Pin intended readable holds and extend metadata for genuine animated tails.
      if(tl.totalDuration()<duration)tl.to({hold:0},{hold:1,duration,ease:'none'},0);
      if(root){root.dataset.duration=String(duration);root.dataset.compositionId=id;for(const clip of root.querySelectorAll('[data-duration]'))if(Number(clip.dataset.start||0)===0&&Number(clip.dataset.duration)===declared)clip.dataset.duration=String(duration);}
      api.status='ready';api.seek(0);resolveReady(api);}catch(e){api.status='failed';rejectReady(e);throw e;}
    },
    dispose(){disposed=true;timeline?.kill();for(const fn of cleanups)fn();hooks.clear();cleanups.clear();api.status='disposed';},
    number(value,min,max,name){const n=Number(value);if(typeof value==='boolean'||!Number.isFinite(n)||n<min||n>max)throw RangeError(name+' outside ['+min+','+max+']');return n;},
    color(value){if(!/^#[0-9a-f]{3}([0-9a-f]{3})?$/i.test(value))throw TypeError('Expected hex color');return value;},
    svg(value){const d=new DOMParser().parseFromString(value,'image/svg+xml');if(d.querySelector('parsererror')||d.documentElement.localName!=='svg')throw Error('Invalid SVG');const allowed=new Set('svg g path circle rect ellipse polygon polyline line defs linearGradient radialGradient stop clipPath mask title desc'.split(' '));for(const el of d.querySelectorAll('*')){if(!allowed.has(el.localName))throw Error('Unsupported active SVG element: '+el.localName);for(const a of el.attributes){if(/^on/i.test(a.name)||/href/i.test(a.name)||/url\((?!#[\w-]+\))/i.test(a.value)||a.name==='style')throw Error('SVG must contain inert local geometry');}}return new XMLSerializer().serializeToString(d.documentElement);},
    inputs(){const v={...(global.__musicVariables||(global.__hyperframes?.getVariables?.()||{}))};for(const [k,x]of Object.entries(v)){if(x!==''&&/Color$|^color(Low|Mid|High)$|^idleInk$/.test(k))api.color(x);if(['leftMark','rightMark'].includes(k)&&x)v[k]=api.svg(x);if(k==='icon'&&typeof x==='string'&&x.trim().startsWith('<'))v[k]=api.svg(x);if(['program','cards','landings','frames','strobePlan','phrases','climax'].includes(k)&&typeof x==='string'&&x.trim()){try{JSON.parse(x)}catch{throw Error('Invalid JSON input: '+k)}}if(typeof x==='string'&&x.length>100000)throw Error('Input exceeds recipe budget: '+k);}
      if(v.tiles!=null){api.number(v.tiles,2,200,'tiles');if(!Number.isInteger(v.tiles))throw Error('tiles must be an integer');}if(v.bands!=null){api.number(v.bands,1,200,'bands');if(!Number.isInteger(v.bands))throw Error('bands must be an integer');}if(v.gap!=null)api.number(v.gap,0,200,'gap');if(v.flowSpeed!=null)api.number(v.flowSpeed,0.05,10,'flowSpeed');if(v.sweepSpeed!=null)api.number(v.sweepSpeed,0.2,3,'sweepSpeed');return v;},
    program(steps,{allowed,duration,count}){if(!Array.isArray(steps)||steps.length>200)throw Error('Program must contain at most 200 steps');
      const needs={staggerInOut:'enter',holdRecolor:'on',snakeFillOverlay:'fill',lockup:'enter',slot:'enter',bg:'at',shake:'beats',expand:'at'};
      for(const step of steps){if(!step||!allowed.includes(step.op))throw Error('Unknown program operator');const required=step[needs[step.op]];if(required==null||Array.isArray(required)&&!required.length)throw Error('Missing operator timing: '+step.op);
        for(const [key,value]of Object.entries(step)){if(['enter','exit','fill','overlay','recolor','beats'].includes(key)){if(!Array.isArray(value)||value.length>10000||value.some((t,i)=>typeof t!=='number'||!Number.isFinite(t)||t<0||t>duration||(i&&t<value[i-1])))throw Error('Invalid program anchors: '+key);}if(['on','off','at','swap','box','fade','to'].includes(key))api.number(value,0,duration,key);}
        if(step.op==='expand'&&step.to!=null&&step.to<=step.at)throw Error('Expansion must end after it starts');
        if(step.settle!=null)api.number(step.settle,0.001,duration,'settle');if(Array.isArray(step.order)&&(!Number.isInteger(count)||step.order.length!==count||new Set(step.order).size!==count||step.order.some(i=>!Number.isInteger(i)||i<0||i>=count)))throw Error('Custom order must permute tile indices');
      }return steps;
    },
    rawField(canvas,uniforms,fragment,colors){let gl=null,program,buffer,shaders=[];const W=canvas.width=1920,H=canvas.height=1080;
      const fallback=()=>{if(canvas.dataset.fallback)return;canvas.dataset.fallback='true';const plate=document.createElement('div');plate.className=canvas.className;plate.style.cssText='position:absolute;inset:0;width:100%;height:100%;background:radial-gradient(ellipse at 48% 46%, '+colors[2]+', '+colors[1]+' 45%, '+colors[0]+' 90%)';canvas.after(plate);canvas.style.display='none';api.addCleanup(()=>plate.remove());canvas.dataset.renderMode='css-fallback';};
      try{gl=canvas.getContext('webgl',{alpha:false,preserveDrawingBuffer:true});if(!gl){fallback();return {render:()=>{},dispose:()=>{}};}
        function compile(type,source){const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(s));shaders.push(s);return s;}
        program=gl.createProgram();gl.attachShader(program,compile(gl.VERTEX_SHADER,'attribute vec2 position;varying vec2 vUv;void main(){vUv=position*0.5+0.5;gl_Position=vec4(position,0.,1.);}'));gl.attachShader(program,compile(gl.FRAGMENT_SHADER,fragment));gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(program));
        buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);const pos=gl.getAttribLocation(program,'position');const locations=Object.fromEntries(Object.keys(uniforms).map(k=>[k,gl.getUniformLocation(program,k)]));
        const render=()=>{if(gl.isContextLost()){fallback();return;}gl.useProgram(program);gl.viewport(0,0,W,H);gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.enableVertexAttribArray(pos);gl.vertexAttribPointer(pos,2,gl.FLOAT,false,0,0);for(const [k,u]of Object.entries(uniforms)){let v=u.value;if(Array.isArray(v))gl[v.length===2?'uniform2fv':'uniform3fv'](locations[k],v);else gl.uniform1f(locations[k],v)}gl.drawArrays(gl.TRIANGLES,0,3)};
        const dispose=()=>{gl.deleteBuffer(buffer);gl.deleteProgram(program);shaders.forEach(s=>gl.deleteShader(s))};api.addCleanup(dispose);canvas.addEventListener('webglcontextlost',fallback,{once:true});canvas.dataset.renderMode='webgl';return {render,dispose};
      }catch(e){fallback();api.warning='WebGL fallback: '+e.message;return {render:()=>{},dispose:()=>{if(gl){if(buffer)gl.deleteBuffer(buffer);if(program)gl.deleteProgram(program);shaders.forEach(s=>gl.deleteShader(s));}}};}
    }
  };
  global.MusicRuntime=api;global.__musicComposition=api;global.addEventListener?.('error',event=>{api.status='failed';rejectReady(event.error||Error(event.message));});global.addEventListener?.('unhandledrejection',event=>{api.status='failed';rejectReady(event.reason);});
})(window);
