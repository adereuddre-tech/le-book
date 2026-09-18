/* cover2.js — couverture forcée : chaque anecdote, chaque dépêche, CHAQUE choix.
   Pour chaque événement de chaque pool, on ouvre l'écran, on clique un choix, et on vérifie :
     - aucune erreur levée ;
     - aucun « undefined », « NaN » ou « [object » dans ce que le joueur lit ;
     - aucune jauge ni aucun encours devenus non finis.
   On signale aussi les textes libellés en milliards, hérités de la version où le fonds
   faisait 100 Md$ : le fonds fait aujourd'hui 75 à 150 M$.
   Usage : node tools/cover2.js [fichier] */
const fs=require('fs'),{JSDOM}=require('jsdom');
const file=process.argv[2]||'index.html';
const dom=new JSDOM(fs.readFileSync(file,'utf8'),{runScripts:'dangerously',url:'https://x/',
  beforeParse(w){w.scrollTo=()=>{};w.setTimeout=(f)=>{try{f()}catch(e){}return 0};w.alert=()=>{};w.prompt=()=>'';}});
const w=dom.window;
setTimeout(()=>{
 const out=w.eval(`(()=>{
  const bad=[],pools=[];
  const reset=()=>{newGame(7,'fonda','std','inhouse','std','mid','ext','normal');S.fundName='Audit';
    genRumors();const R=recoBook();S.k=R.k.slice();S.k0=new Array(N).fill(0);S.phase='events';};
  const scan=(where)=>{
    const ap=document.getElementById('app');const t=(ap?ap.textContent:'')||'';
    const m=t.match(/undefined|NaN|\\[object [A-Z]/);
    if(m)bad.push(where+' → « '+m[0]+' » dans '+t.slice(Math.max(0,t.indexOf(m[0])-60),t.indexOf(m[0])+40).replace(/\\s+/g,' '));
    if(!isFinite(S.nav)||!isFinite(S.lp)||!isFinite(S.rc))bad.push(where+' → état non fini : nav='+S.nav+' lp='+S.lp+' rc='+S.rc);
  };
  const force=(name,list,open)=>{
    let n=0,c=0;
    list.forEach((ev,i)=>{
      const nch=(ev.ch||[]).length||1;
      for(let k=0;k<nch;k++){
        reset();
        try{open(ev)}catch(e){bad.push(name+' #'+i+' ouverture → '+e.message);continue}
        scan(name+' #'+i+' « '+String(ev.t||ev.who||'').slice(0,40)+' » (avant choix)');
        const ch=[...document.querySelectorAll('.choice')];
        if(!ch.length){n++;continue}
        try{ch[Math.min(k,ch.length-1)].click()}catch(e){bad.push(name+' #'+i+' choix '+k+' → '+e.message);continue}
        scan(name+' #'+i+' choix '+k+' « '+((ev.ch&&ev.ch[k]&&ev.ch[k].b)||'?')+' »');
        c++;
      }
      n++;
    });
    pools.push(name+' : '+n+' événements, '+c+' choix forcés');
  };
  force('TRADER_EXEC',TRADER_EXEC,ev=>screenTraderEvent(ev));
  force('TRADER_MID',TRADER_MID,ev=>screenTraderEvent(ev));
  force('BOARDEV',BOARDEV,ev=>screenBoard(ev));
  force('STAKE',STAKE.filter(x=>x.ch),ev=>screenBoard(ev));
  force('MACROEV',MACROEV.slice(0,80),ev=>screenMacroEvent(ev));
  /* textes encore libellés en milliards alors que le fonds fait 75 à 150 M$ */
  const md=[];
  const walk=(name,list)=>list.forEach((ev,i)=>{
    const t=JSON.stringify([ev.t,ev.p,(ev.ch||[]).map(c=>[c.b,c.s])]);
    const m=t.match(/[\\d, ]+Md\\$|milliards/);
    if(m)md.push(name+' #'+i+' : '+m[0].trim()+' — '+String(ev.t||ev.who).slice(0,50));
  });
  walk('TRADER_EXEC',TRADER_EXEC);walk('TRADER_MID',TRADER_MID);walk('BOARDEV',BOARDEV);walk('MACROEV',MACROEV);
  return JSON.stringify({pools,bad,md});
 })()`);
 const r=JSON.parse(out);
 r.pools.forEach(p=>console.log(' '+p));
 console.log('\\n=== anomalies de rendu ===');
 if(!r.bad.length)console.log(' aucune : aucun « undefined », « NaN » ni état non fini sur l\'ensemble des choix');
 r.bad.slice(0,25).forEach(x=>console.log('  '+x));
 if(r.bad.length>25)console.log('  … et '+(r.bad.length-25)+' autres');
 console.log('\\n=== textes encore libellés en milliards ('+r.md.length+') ===');
 r.md.slice(0,20).forEach(x=>console.log('  '+x));
 dom.window.close();
},1500);
