const {playGame}=require('/home/claude/le-book/tools/bot.js');const fs=require('fs');
const probe=`(function(){window.__G={};window.__F={};window.__A={};window.__N=0;const G=goalCtx;goalCtx=function(o){const c=G.apply(this,arguments);
 if(o&&o.navBefore!==undefined&&!window.__busy){window.__busy=1;window.__N++;QGOALS.forEach(g=>{let v=0;try{v=g.t(c)?1:0}catch(e){v=-1}window.__G[g.nm]=(window.__G[g.nm]||0)+(v>0?1:0)+(v<0?1000:0)});
  FEATS.forEach(f=>{if(f.tq){let v=0;try{v=f.tq(c)?1:0}catch(e){v=1000}window.__F[f.id]=(window.__F[f.id]||0)+v}});window.__busy=0}return c};
 const A=award;award=function(id){window.__A[id]=1;return A.apply(this,arguments)}})()`;
const tot={G:{},F:{},A:{},N:0,games:0,err:0};
for(let sd=1;sd<=12;sd++)for(const pr of ['syst','fonda','flux']){const size=sd%3===0?'mega':sd%3===1?'small':'mid';
 const r=playGame({file:'/home/claude/lot89/final.html',seed:sd,prof:pr,size,dur:sd%4===0?'saison':'normal',probe,collect:'JSON.stringify({G:window.__G,F:window.__F,A:window.__A,N:window.__N})'});
 tot.games++;tot.err+=r.nerr||0;const p=typeof r.probe==='string'?JSON.parse(r.probe):r.probe;if(!p||!p.G)continue;tot.N+=p.N;
 for(const k in p.G)tot.G[k]=(tot.G[k]||0)+p.G[k];for(const k in p.F)tot.F[k]=(tot.F[k]||0)+p.F[k];for(const k in p.A)tot.A[k]=(tot.A[k]||0)+1;
 fs.writeFileSync('/home/claude/lot89/cov.json',JSON.stringify(tot))}
fs.writeFileSync('/home/claude/lot89/cov.json',JSON.stringify(tot));fs.writeFileSync('/home/claude/lot89/cov.fin','ok');
