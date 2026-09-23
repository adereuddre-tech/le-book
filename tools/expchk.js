/* Lot 51 : l'intervalle ± 2σ du rendement attendu contient-il le mouvement réel ~95 fois sur 100 ?
   Par marché : z = (rBase − attendu)/σ au moment du desk. Pour le book : sur le book validé. */
const {playGame}=require('./bot.js');
const F=process.argv[2]||'index.html';
const hook="window.__xz=[];window.__xb=[];(function(){const SP=screenPlay;window.screenPlay=function(){const r=SP.apply(this,arguments);try{for(let i=0;i<N;i++){if(!mktOpen(i))continue;const o=expRet(i);window.__xz.push((S.rBase[i]-o.m)/o.s)}}catch(e){}return r};const CO=commitOrders;window.commitOrders=function(){const r=CO.apply(this,arguments);try{const o=expBook(S.k);const w=weights(S.k);let g=S.rate/4;for(let i=0;i<N;i++)g+=w[i]*S.rBase[i];if(o.s>0)window.__xb.push((g-o.m)/o.s)}catch(e){}return r}})()";
let Z=[],B=[];
for(const prof of ['syst','fonda','flux'])for(let s=1;s<=4;s++){const g=playGame({file:F,seed:s,prof,dur:'normal',pre:hook,collect:"JSON.stringify({z:window.__xz,b:window.__xb})"});if(g.probe&&g.probe.z){Z=Z.concat(g.probe.z);B=B.concat(g.probe.b)}}
const st=a=>{const m=a.reduce((x,y)=>x+y,0)/a.length,sd=Math.sqrt(a.reduce((x,y)=>x+(y-m)**2,0)/a.length);return {n:a.length,moy:m.toFixed(2),ecart:sd.toFixed(2),dans2s:(a.filter(z=>Math.abs(z)<=2).length/a.length*100).toFixed(1)+'%'}};
console.log('marchés',JSON.stringify(st(Z)));console.log('book',JSON.stringify(st(B)));
