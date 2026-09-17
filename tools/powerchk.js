// Vérifie les pouvoirs propres des trois styles
const fs=require('fs');const {JSDOM}=require('jsdom');
const html=fs.readFileSync(process.argv[2]||'index.html','utf8');
const mk=()=>new JSDOM(html,{runScripts:'dangerously',url:'https://x.test/',pretendToBeVisual:true,beforeParse(w){w.scrollTo=()=>{};w.setInterval=()=>0}}).window;
const out={};
for(const prof of ['syst','fonda','flux']){
 const w=mk();
 out[prof]=JSON.parse(w.eval(`(()=>{newGame(11,'${prof}','std','inhouse','std','mid','com','normal');
  const R={q:0,sure:0,sureWrong:0,hunch:0,hunchWrong:0,hunchTop2:0,nRum:[],phErr:[[],[],[]],ver:0};
  for(let t=0;t<300;t++){S.bud.res=t%3;planQuarter();genRumors();R.q++;
   R.nRum.push(S.rumors.filter(r=>!r.ev).length-RESN[S.bud.res]);
   S.rumors.filter(r=>r.sure).forEach(r=>{R.sure++;const d=r.v.reduce((a,z,k)=>a+z*S.f[k],0);if(d<-0.25)R.sureWrong++});
   if(S.hunch){R.hunch++;if(S.hunch.up!==(S.f[S.hunch.k]>0))R.hunchWrong++;
     const top=S.f.map((v,i)=>[Math.abs(v),i]).sort((a,b)=>b[0]-a[0]).slice(0,2).map(x=>x[1]);if(top.includes(S.hunch.k))R.hunchTop2++}
   /* précision des probabilités de dépêche */
   S.sc=null;const n0=S.evVerified;
   for(let e=0;e<3;e++){S.sc=null;const ev=POOLS.MACROEV.live[(t*7+e)%POOLS.MACROEV.live.length];
    /* reproduit le tirage de screenMacroEvent sans l'écran */
    S.sc={p:0.25+0.50*rng(),m:[0.6,-0.5]};const pr=PROF(),sd=[0.16,0.10,0.05][S.bud.res]*(pr.id==='flux'?0.6:1);
    const ver=pr.id==='fonda'&&!S.evVerified;if(ver){S.evVerified=true;R.ver++}
    const sh=pr.id==='syst'?0.04:0;const ph=ver?S.sc.p:Math.max(0.1,Math.min(0.9,S.sc.p+sh+sd*gauss()));
    R.phErr[S.bud.res].push(ph-S.sc.p)}
  }
  const ms=a=>{const m=a.reduce((x,y)=>x+y,0)/a.length;return [+m.toFixed(3),+Math.sqrt(a.reduce((x,y)=>x+(y-m)**2,0)/a.length).toFixed(3)]};
  R.phErr=R.phErr.map(ms);R.nRum=ms(R.nRum);
  /* capture, coûts, ajustement offert */
  S.k=new Array(N).fill(0);const ev=POOLS.MACROEV.live.find(e=>Object.keys(e.hit).length>=1);const touched=Object.keys(ev.hit).map(s=>IDX[s]);
  S.freeAdjUsed=false;S.sc={p:0.5,ph:0.5,m:[0.6,-0.5]};const P=evPlans(ev,touched);
  const i0=P[0].trades[0].i;R.capture=+(P[0].kE[i0]/(P[0].t[i0])).toFixed(2);R.free=P[0].free;R.fixRc=P[0].fixRc.map(x=>x[1]);
  R.labels=P.map(o=>o.b);R.tcMult=PROF().tcMult;R.lpMult=+(pnlGz(-0.01).lp/(${'(()=>{const s0=S.prof;S.prof="fonda";const v=pnlGz(-0.01).lp;S.prof=s0;return v})()'})).toFixed(2);
  R.incMult=PROF().incMult;
  return JSON.stringify(R)})()`));
 // bouton du modèle : présent pour le seul quant, et il applique bien le book
 const w2=mk();const d=w2.document;w2.eval(`newGame(5,'${prof}','std','inhouse','std','mid','com','normal');S.tuto=99;S.fundName='Test Capital'`);
 w2.eval(`TUTO=false;phaseOpen()`);
 let guard=0;while(!d.querySelector('#send')&&guard++<40){const b=d.querySelector('#tutooff')||d.querySelector('#ok')||d.querySelector('#pgo')||d.querySelector('#rgo');if(!b)break;b.click()}
 const am=d.querySelector('#applymodel');out[prof].modelBtn=!!am;
 if(am){am.click();out[prof].modelApplied=w2.eval('S.k.join()===S.modelK.join()&&S.k.some(v=>v!==0)')}
 out[prof].hunchState=w2.eval('JSON.stringify(S.hunch)+S.prof');out[prof].hunchShown=d.querySelector('#app').innerHTML.includes('🫀');
}
console.log(JSON.stringify(out,null,1));
