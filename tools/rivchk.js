/* Les concurrents bougent-ils vraiment, et en lien avec le marche ? */
const {playGame}=require('./bot.js');
const PROBE=`(function(){window.__V=[];const sb=statusBar;
 statusBar=function(){const h=sb.apply(this,arguments);
  if(S.phase==='events'&&S.tape&&S.tape.pts.length>60){
   const rt=rivalTapes();
   if(rt.length===4)window.__V.push({me:+(S.tape.pts[S.tape.pts.length-1]-100).toFixed(2),
     riv:rt.map(r=>+(r.pts[r.pts.length-1]-100).toFixed(2))});}
  return h};})();`;
let V=[];
for(let i=0;i<5;i++){const r=playGame({file:process.argv[2]||'index.html',seed:1000+i,prof:'fonda',dur:'normal',
  probe:PROBE,collect:'JSON.stringify(window.__V)'});V=V.concat(r.probe||[])}
const flat=V.filter(x=>x.riv.every(v=>Math.abs(v)<0.05)).length;
const sd=a=>{const m=a.reduce((x,y)=>x+y,0)/a.length;return Math.sqrt(a.map(x=>(x-m)**2).reduce((x,y)=>x+y,0)/a.length)};
const disp=V.map(x=>sd(x.riv));
const me=V.map(x=>x.me),r0=V.map(x=>x.riv[0]);
const mm=a=>a.reduce((x,y)=>x+y,0)/a.length;
const cov=mm(V.map(x=>(x.me-mm(me))*(x.riv[0]-mm(r0))));
console.log(V.length+' releves | concurrents tous plats : '+flat);
console.log('dispersion entre les 4 concurrents : mediane '+disp.sort((a,b)=>a-b)[disp.length>>1].toFixed(2)+' pts');
console.log('correlation vous / concurrent 1 : '+(cov/(sd(me)*sd(r0)||1)).toFixed(2));
console.log('exemple :',JSON.stringify(V[Math.floor(V.length/2)]));
