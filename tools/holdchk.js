/* Les quatre écrans d'événement du trimestre attendent-ils le tracé du ruban ? */
const {playGame}=require('./bot.js');
const PROBE=`(function(){
 window.__H={};
 const wrap=(nm,fn)=>function(){const r=fn.apply(this,arguments);
   const w=document.querySelector('.evwrap');
   const k=nm+(S.phase==='events'?'':' (hors trimestre)');
   window.__H[k]=window.__H[k]||{n:0,hold:0};
   window.__H[k].n++; if(w&&w.classList.contains('evhold'))window.__H[k].hold++;
   return r};
 screenMacroEvent=wrap('depeche',screenMacroEvent);
 screenTraderEvent=wrap('desk',screenTraderEvent);
 screenRivalEvent=wrap('rivalite',screenRivalEvent);
 screenIncident=wrap('incident',screenIncident);
 const rc=resultCard;resultCard=function(){const r=rc.apply(this,arguments);
   const w=document.querySelector('.evwrap');
   window.__H['bilan']=window.__H['bilan']||{n:0,hold:0};
   window.__H['bilan'].n++; if(w&&w.classList.contains('evhold'))window.__H['bilan'].hold++;
   return r};
})();`;
const T={};
for(let i=0;i<8;i++){const r=playGame({file:process.argv[2]||'index.html',seed:700+i,
  prof:['syst','fonda','flux'][i%3],dur:'normal',probe:PROBE,collect:'JSON.stringify(window.__H)'});
  Object.entries(r.probe||{}).forEach(([k,v])=>{T[k]=T[k]||{n:0,hold:0};T[k].n+=v.n;T[k].hold+=v.hold})}
Object.entries(T).forEach(([k,v])=>console.log('  '+k.padEnd(24)+v.hold+' / '+v.n+' avec attente du trace'));
