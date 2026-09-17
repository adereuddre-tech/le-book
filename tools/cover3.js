// couverture : evPlans sur toutes les dépêches ouvertes, 3 styles, avec et sans interdiction du comité
const fs=require('fs');const {JSDOM}=require('jsdom');
const html=fs.readFileSync(process.argv[2]||'index.html','utf8');let bad=0,n=0,neg=0,pos=0,evd=[];
for(const prof of ['syst','fonda','flux'])for(const [size,univ] of [['small','fin'],['mega','ext']]){
 const dom=new JSDOM(html,{runScripts:'dangerously',url:'https://x.test/',pretendToBeVisual:true,beforeParse(w){w.scrollTo=()=>{};w.setInterval=()=>0}});
 const w=dom.window;
 const r=w.eval(`(()=>{newGame(7,'${prof}','std','inhouse','std','${size}','${univ}','normal');
  const out={n:0,bad:0,neg:0,pos:0,evd:[]};
  const P=POOLS.MACROEV.live;
  S.k=recoBook().k.map(v=>Math.max(-S.maxk,Math.min(S.maxk,Math.round(v))));
  for(const nA of [false,true])for(const ev of P){S.noAddQ=nA;S.sc={p:0.5,m:[0.6,-0.5]};
   try{const touched=Object.keys(ev.hit).map(s=>IDX[s]);if(touched.some(i=>i===undefined))throw 'marché fermé';
    const pl=evPlans(ev,touched);out.n++;
    if(pl.length!==2||pl[1].a!=='none')throw 'forme';
    const f=pl[0];if(f.trades.length){if(!(f.pay[0]>pl[1].pay[0]))throw 'poursuite ne paie pas plus';
     if(!(f.pay[1]<pl[1].pay[1]))throw 'retournement ne coûte pas plus';
     if(nA&&!f.fixRc.some(x=>x[0]===-6))throw 'interdiction ignorée';
     out.evd.push(0.5*(f.pay[0]-pl[1].pay[0])+0.5*(f.pay[1]-pl[1].pay[1]));}
    for(const o of pl)for(const z of o.gz)if(!isFinite(z.lp)||!isFinite(z.rc))throw 'NaN';
   }catch(e){out.bad++;if(out.bad<3)out.err=String(e)+' '+ev.t}}
  return JSON.stringify(out)})()`);
 const o=JSON.parse(r);n+=o.n;bad+=o.bad;evd.push(...o.evd);if(o.err)console.log(prof,size,univ,o.err);
}
evd.sort((a,b)=>a-b);
console.log('plans',n,'anomalies',bad,'gain moyen suivre-vs-rien à p=0,5 (pb)',(evd.reduce((a,b)=>a+b,0)/evd.length*1e4).toFixed(1),'médiane',(evd[evd.length>>1]*1e4).toFixed(1));
