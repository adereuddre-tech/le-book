/* Mesure du poids des anecdotes d'exécution : par choix, ce que le fonds gagne ou perd,
   ce que la facture d'ordres bouge, et ce que les deux jauges prennent.
   Usage : node tools/execmeas.js <fichier> [nbGraines] */
const {playGame}=require('./execprobe.js');
const file=process.argv[2]||'index.html',NS=+(process.argv[3]||6);
const PROBE=`window.__tx=[];window.__rq=0;(function(){
 /* deux familles distinctes : l'anecdote d'exécution (écran des ordres, carte « EXÉCUTION · »)
    et l'anecdote de desk pendant le trimestre (carte « LE DESK · »). */
 const RQ=resolveQuarter;resolveQuarter=function(){window.__rq++;return RQ.apply(this,arguments)};
 const snap=(fam,t)=>window.__tx.push({fam,t,q:S.q,rq:window.__rq,nav0:S.nav,lp0:S.lp,rc0:S.rc,tc0:S.pendingTC*S.nav,sl0:S.execSlipQ||0});
 const SX=screenExec;screenExec=function(){snap('exec','');return SX.apply(this,arguments)};
 const SE=screenTraderEvent;screenTraderEvent=function(ev){snap('desk',ev&&ev.t);return SE.apply(this,arguments)};
 const RC=resultCard;resultCard=function(k){k=String(k);
  const fam=k.indexOf('EX')===0?'exec':(k.indexOf('LE DESK')===0?'desk':null);
  if(fam){for(let i=window.__tx.length-1;i>=0;i--){const e=window.__tx[i];
   if(e.fam!==fam)continue;
   if(!e.done&&e.rq===window.__rq&&e.q===S.q){e.done=1;e.nav=S.nav;e.lp=S.lp;e.rc=S.rc;e.tc=S.pendingTC*S.nav;e.sl=S.execSlipQ||0}
   break}}
  return RC.apply(this,arguments)};
})()`;

const q=(a,p)=>{const b=[...a].sort((x,y)=>x-y);return b.length?b[Math.min(b.length-1,Math.floor(p*b.length))]:0};
const st=a=>({n:a.length,moy:a.reduce((x,y)=>x+y,0)/Math.max(1,a.length),med:q(a,0.5),p10:q(a,0.10),p90:q(a,0.90)});
const f=(x,d=2)=>Number(x).toFixed(d);
const rows=[],games=[];
for(let s=1;s<=NS;s++)for(const prof of ['fonda','syst','flux']){
 const r=playGame({file,seed:s*13+1,prof,dur:'normal',collect:'JSON.stringify(window.__tx)',probe:PROBE});
 games.push(r);(r.probe||[]).filter(e=>e.done).forEach(e=>rows.push({fam:e.fam,
  fondBp:(e.nav-e.nav0)/e.nav0*1e4,          /* effet sur le fonds, en pb de l'encours */
  slipBp:(e.sl-e.sl0)/e.nav0*1e4,            /* dont dégradation du prix moyen */
  billBp:(e.tc-e.tc0)/e.nav0*1e4,            /* facture d'ordres, à la charge du gérant */
  lp:e.lp-e.lp0, rc:e.rc-e.rc0}));
}
const FAM=f=>rows.filter(r=>r.fam===f);
const P=(nm,a)=>{const x=st(a);console.log(nm.padEnd(30),'n',x.n,'moy',f(x.moy),'méd',f(x.med),'p10',f(x.p10),'p90',f(x.p90))};
console.log('parties',games.length,'erreurs',games.reduce((a,g)=>a+g.nerr,0),'anecdotes',rows.length,
 '· par partie',f(rows.length/games.length,1));
for(const f of ['exec','desk']){
 const a=FAM(f);console.log('\n— '+(f==='exec'?"anecdotes d'exécution (écran des ordres)":'anecdotes de desk')+' —',a.length,'choix ·',(a.length/games.length).toFixed(1),'par partie');
 P('fonds (pb encours)',a.map(r=>r.fondBp));
 P('  dont prix moyen (pb)',a.map(r=>r.slipBp));
 P('facture ordres (pb)',a.map(r=>r.billBp));
 P('investisseurs',a.map(r=>r.lp));
 P('comité',a.map(r=>r.rc));
 console.log('  touchent les investisseurs',a.filter(r=>Math.abs(r.lp)>=0.5).length,'/',a.length,
  '· le comité',a.filter(r=>Math.abs(r.rc)>=0.5).length,'· le fonds (>5 pb)',a.filter(r=>Math.abs(r.fondBp)>5).length);
}
console.log('score moyen',f(games.reduce((a,g)=>a+g.score,0)/games.length,1),'M$ · survie',
 games.filter(g=>!g.over).length,'/',games.length);
