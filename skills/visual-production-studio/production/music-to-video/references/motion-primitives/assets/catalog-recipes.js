/* Nine parameterized authoring recipes. GSAP and an instance-owned render registry
   are supplied by the caller. These are not standalone HTML compositions. */
(function(global){
 const finite=(n)=>{if(typeof n!=='number'||!Number.isFinite(n))throw Error('Finite time/value required');return n;};
 const ordered=(xs)=>{if(!Array.isArray(xs)||!xs.length||xs.some((x,i)=>finite(x)<0||(i&&x<=xs[i-1])))throw Error('Nonempty strictly ordered anchor array required');return xs;};
 function add(kind,{tl,gsap,nodes=[],at=0,end,anchors,palette,value=100,format=n=>Math.floor(n).toLocaleString('en-US'),render,sourceTimeline,holdAt,from=0,oldSystem,newSystem,mark,layers=nodes}){
  finite(at);if(at<0)throw Error('Negative anchor');if(!tl||!gsap)throw Error('Timeline and GSAP required');const span=()=>{finite(end);if(end<=at)throw Error('Positive active span required');return end-at;};
  switch(kind){
   case 'chromatic-pressure':{const d=span();if(nodes.length!==3)throw Error('Provide aligned R/G/B glyph layers');tl.set(nodes,{opacity:1},at);nodes.forEach((n,i)=>{tl.fromTo(n,{x:0,y:0},{x:[-18,0,18][i],y:[3,-2,1][i],duration:d*.35,ease:'steps(2)'},at);tl.to(n,{x:0,y:0,duration:d*.65,ease:'steps(3)'},at+d*.35)});break;}
   case 'color-grid-shuffle':{ordered(anchors);if(!nodes.length||!palette?.length)throw Error('Grid and palette required');anchors.forEach((t,k)=>nodes.forEach((n,i)=>tl.set(n,{backgroundColor:palette[(i*7+k*3)%palette.length]},t)));break;}
   case 'content-swap':{ordered(anchors);if(!nodes.length)throw Error('Prebuilt content nodes required');tl.set(nodes,{autoAlpha:0},0);anchors.forEach((t,k)=>{tl.set(nodes,{autoAlpha:0},t);tl.set(nodes[k%nodes.length],{autoAlpha:1},t)});break;}
   case 'freeze-hold':{const d=span();finite(holdAt);if(!sourceTimeline||sourceTimeline===tl||!render)throw Error('Separate source timeline and frame render registry required');render(t=>sourceTimeline.totalTime(t<at?t:t<=end?holdAt:Math.max(0,t-d),true));break;}
   case 'negative-space-hold':{span();if(!mark||layers.includes(mark))throw Error('Separate mark from busy layers');tl.set(layers,{autoAlpha:0},at);tl.set(mark,{autoAlpha:1},at);break;}
   case 'overlay-pop':{const d=span();if(!nodes.length)throw Error('Overlay nodes required');tl.fromTo(nodes,{autoAlpha:0,y:20,scale:.86},{autoAlpha:1,y:0,scale:1,duration:d,ease:'back.out(1.7)'},at);break;}
   case 'staggered-reveal':{ordered(anchors);if(nodes.length!==anchors.length)throw Error('One anchor per accumulating item');nodes.forEach((n,i)=>tl.fromTo(n,{autoAlpha:0,y:30},{autoAlpha:1,y:0,duration:.24,ease:'power3.out'},anchors[i]));break;}
   case 'system-replace':{if(!oldSystem||!newSystem||oldSystem===newSystem)throw Error('Distinct system containers required');tl.set(newSystem,{autoAlpha:0},0);tl.set(oldSystem,{autoAlpha:0},at);tl.set(newSystem,{autoAlpha:1},at);break;}
   case 'value-counter':{const d=span();finite(value);finite(from);if(nodes.length!==1||!render)throw Error('One text node and render registry required');const state={value:from};tl.fromTo(state,{value:from},{value,duration:d,ease:'power2.out'},at);render(t=>{nodes[0].textContent=format(t>=end?value:state.value)});break;}
   default:throw Error('Unknown recipe: '+kind);
  }
  return tl;
 }
 const api={add};if(typeof module!=='undefined')module.exports=api;else global.MusicRecipes=api;
})(typeof window==='undefined'?globalThis:window);
