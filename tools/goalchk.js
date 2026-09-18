/* goalchk.js — rejoue les 108 prédicats d'objectif (QGOALS) et les 36 prédicats de haut fait
   (FEATS) sur des contextes RÉELS, produits par de vraies clôtures de trimestre et de vraies
   fins de partie, et non sur des objets fabriqués.

   Motivation : dans le jeu, les prédicats sont appelés dans un try/catch muet
   (`FEATS.forEach(f=>{if(f.tq){try{...}catch(e){}}})`). Un prédicat cassé n'est jamais
   attribué et ne dit rien. Ici on les rejoue tous sur chaque contexte et on remonte tout.

   Usage : node tools/goalchk.js [fichier] [nb de parties]
   Signale : prédicat qui lève, prédicat qui ne rend pas un booléen, prédicat jamais vrai
   (inatteignable) et prédicat toujours vrai (gratuit). */
const {playGame}=require('./bot.js');
const file=process.argv[2]||'index.html', NG=+(process.argv[3]||18);

const PROBE=`
(function(){
 window.__P={n:0,nf:0,tcbp:[],g:QGOALS.map(()=>({ok:0,err:0,bad:0,msg:'',got:''})),
             fq:FEATS.map(()=>({ok:0,err:0,bad:0,msg:'',got:'',absent:0})),
             ff:FEATS.map(()=>({ok:0,err:0,bad:0,msg:'',got:'',absent:0}))};
 const run=(list,slot,c)=>list.forEach((G,i)=>{
   const t=slot===window.__P.ff?G.tf:(slot===window.__P.fq?G.tq:G.t);
   if(!t){slot[i].absent=1;return}
   let v;try{v=t(c)}catch(e){slot[i].err++;slot[i].msg=String(e.message).slice(0,70);return}
   if(typeof v!=='boolean'){slot[i].bad++;slot[i].got=String(v).slice(0,24)}
   else if(v)slot[i].ok++;
 });
 const g=goalCtx;
 goalCtx=function(o){
   const c=g(o);
   window.__P.n++;
   c.streak=S.streak;window.__P.tcbp.push(+c.tcBp.toFixed(2));
   if(!window.__P.miss){                      /* un prédicat qui lit un champ absent rend
                                                 false en silence : on le détecte une fois */
     const keys=new Set(Object.keys(c));window.__P.miss=[];
     const scan=(list,kind)=>list.forEach(G=>{const t=kind==='t'?G.t:(kind==='tq'?G.tq:G.tf);if(!t)return;
       const src=String(t);const bad=[...new Set([...src.matchAll(/\bc\.(\w+)/g)].map(m=>m[1]))].filter(k=>!keys.has(k));
       if(bad.length)window.__P.miss.push((G.nm||G.id)+' ['+kind+'] lit '+bad.join(', '))});
     scan(QGOALS,'t');scan(FEATS,'tq');
   }                       /* le jeu ajoute streak avant d'évaluer les tq */
   run(QGOALS,window.__P.g,c);
   run(FEATS,window.__P.fq,c);
   return c;
 };
 /* les prédicats de fin de partie s'évaluent sur S.finalCtx, écrit au rapport final */
 const rf=screenFinal;
 screenFinal=function(){const r=rf.apply(this,arguments);
   if(S.finalCtx){window.__P.nf++;run(FEATS,window.__P.ff,S.finalCtx)}
   return r};
})();`;

const COLLECT=`JSON.stringify(window.__P)`;

const agg={n:0,nf:0,g:null,fq:null,ff:null};
const merge=(a,b)=>{if(!a)return b.map(x=>Object.assign({},x));
  b.forEach((x,i)=>{a[i].ok+=x.ok;a[i].err+=x.err;a[i].bad+=x.bad;
    if(x.msg)a[i].msg=x.msg; if(x.got)a[i].got=x.got});return a};

const profs=['syst','fonda','flux'], sizes=['small','mid','mega'], univs=['fin','com','ext'];
for(let i=0;i<NG;i++){
  const r=playGame({file,seed:100+i,prof:profs[i%3],size:sizes[(i/3|0)%3],univ:univs[i%3],dur:'normal',probe:PROBE,collect:COLLECT});
  const p=r.probe;
  if(!p||p.err){console.log('partie',i,'sonde muette',p&&p.err);continue}
  agg.n+=p.n;agg.nf+=p.nf;global.__tcbp=(global.__tcbp||[]).concat(p.tcbp||[]);global.__miss=(global.__miss||[]).concat(p.miss||[]);
  agg.g=merge(agg.g,p.g);agg.fq=merge(agg.fq,p.fq);agg.ff=merge(agg.ff,p.ff);
}

const NAMES=require('fs').readFileSync(file,'utf8');
const names=(re)=>[...NAMES.matchAll(re)].map(m=>m[1]);
const gn=names(/\{nm:"((?:[^"\\]|\\.)*)",d:"(?:[^"\\]|\\.)*",t:c=>/g);
const fn=names(/\{id:'[^']*',\s*tier:\d+,ic:'[^']*',nm:"((?:[^"\\]|\\.)*)"/g);

function report(title,slot,names,n){
  if(!slot){console.log(title,': aucun contexte');return}
  const err=[],bad=[],never=[],always=[];
  slot.forEach((x,i)=>{const nm=names[i]||('#'+i);
    if(x.absent)return;                       /* ce haut fait n'a pas ce type de prédicat */
    if(x.err)err.push(`${nm} — ${x.msg} (${x.err}×)`);
    if(x.bad)bad.push(`${nm} — rend ${x.got} (${x.bad}×)`);
    if(!x.err&&!x.bad&&x.ok===0)never.push(nm);
    if(!x.err&&!x.bad&&x.ok===n&&n>0)always.push(nm);
  });
  const actifs=slot.filter(x=>x.ok>0).length, presents=slot.filter(x=>!x.absent).length;
  console.log(`\n=== ${title} — ${presents} prédicats sur ${n} contextes, ${actifs} déclenchés au moins une fois`);
  const show=(t,a)=>{if(a.length)console.log(` ${t} (${a.length}) :\n   `+a.join('\n   '))};
  show('LÈVENT',err);show('NON BOOLÉENS',bad);show('jamais vrais',never);show('toujours vrais',always);
  if(!err.length&&!bad.length)console.log(' aucun prédicat cassé');
}
if(global.__tcbp&&global.__tcbp.length){const v=global.__tcbp.slice().sort((a,b)=>a-b),q=f=>v[Math.min(v.length-1,Math.floor(v.length*f))];
 console.log('\ncoût d\'exécution du trimestre, en pb de l\'encours : mediane %s, quartiles %s / %s, deciles %s / %s, max %s (n=%d)',
  q(.5),q(.25),q(.75),q(.1),q(.9),v[v.length-1],v.length)}
if(global.__miss&&global.__miss.length){
  console.log('\n!! prédicats qui lisent un champ absent du contexte (ils rendent false en silence) :');
  [...new Set(global.__miss)].forEach(x=>console.log('   '+x));
} else console.log('\naucun prédicat ne lit de champ absent du contexte');
report('Objectifs de trimestre (QGOALS)',agg.g,gn,agg.n);
report('Hauts faits de trimestre (tq)',agg.fq,fn,agg.n);
report('Hauts faits de fin de partie (tf)',agg.ff,fn,agg.nf);
