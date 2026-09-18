/* tapechk.js — le ruban dit-il la vérité ?
   1. le dernier point du ruban = le P&L du fonds à cet instant (exigence 2) ;
   2. en fin de trimestre, ce chiffre = celui que le débriefing affiche (grQ).  */
const {playGame}=require('./bot.js');
const PROBE=`(function(){
 window.__T={pts:0,ecartRuban:0,ecartCloture:[],n:0};
 const sb=statusBar;
 statusBar=function(){const h=sb.apply(this,arguments);
   if(S.phase==='events'&&S.tape&&S.tape.pts.length>2){
     const last=S.tape.pts[S.tape.pts.length-1], cible=ytdIdx().now;
     window.__T.pts++;
     window.__T.ecartRuban=Math.max(window.__T.ecartRuban,Math.abs(last-cible));
   }
   return h};
 const rq=resolveQuarter;
 resolveQuarter=function(){
   const avant=liveRet(), t=qElapsed();
   const r=rq.apply(this,arguments);
   const grQ=S.qPnl?(S.qPnl.grossM+S.qPnl.collM+S.qPnl.evM+S.qPnl.incM+(S.qMgmtM?-S.qMgmtM:0))/Math.max(1e-9,S.navQ0):null;
   window.__T.n++;
   if(grQ!==null)window.__T.ecartCloture.push({t:+t.toFixed(2),ruban:+(avant*1e4).toFixed(1),cloture:+(grQ*1e4).toFixed(1)});
   return r};
})();`;
let P=0,E=0,C=[];
for(let i=0;i<8;i++){
  const r=playGame({file:process.argv[2]||'index.html',seed:500+i,prof:['syst','fonda','flux'][i%3],dur:'normal',
    probe:PROBE,collect:'JSON.stringify(window.__T)'});
  const t=r.probe||{};P+=t.pts||0;E=Math.max(E,t.ecartRuban||0);C=C.concat(t.ecartCloture||[]);
}
console.log(P+' rendus du ruban | ecart max entre le dernier point et le P&L du fonds : '+E.toFixed(6)+' point d\'indice');
const fin=C.filter(x=>x.t>0.99);
console.log(C.length+' clotures, dont '+fin.length+' avec le trimestre entierement ecoule');
const d=fin.map(x=>Math.abs(x.ruban-x.cloture));
if(d.length)console.log('  ecart max ruban / debriefing sur celles-la : '+Math.max(...d).toFixed(2)+' pb');
const ecarts=fin.map(x=>Math.abs(x.ruban-x.cloture)).sort((a,b)=>a-b);
console.log('  clotures ou le ruban tombe pile (<0,5 pb) : '+ecarts.filter(x=>x<0.5).length+' / '+ecarts.length);
console.log('  les autres : '+JSON.stringify(ecarts.filter(x=>x>=0.5).map(x=>+x.toFixed(0))));
console.log('  (le stop, l appel de marge et le portage s appliquent DANS la cloture, apres le dernier evenement :')
console.log('   le ruban ne peut pas les connaitre, et c est normal qu il s arrete avant.)');
