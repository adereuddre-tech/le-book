const {playGame}=require('./bot.js');
const PROBE=`(function(){
 window.__L={deb:0,debTape:0,debOld:0,seg:0,segOff:0,gain:0,gainOk:0,texte:0,texteVide:0};
 const sd=screenDebrief;
 screenDebrief=function(o){const r=sd.apply(this,arguments);
   window.__L.deb++;
   if(/LE TRIMESTRE, HEURE PAR HEURE/.test((document.getElementById('app')||{}).textContent||''))window.__L.debTape++;
   if(/PERFORMANCE NETTE CUMUL/.test((document.getElementById('app')||{}).textContent||''))window.__L.debOld++;
   return r};
 const sp=screenPlay;
 screenPlay=function(){const r=sp.apply(this,arguments);
   const b=[...document.querySelectorAll('.seg button')];
   window.__L.seg+=b.length;window.__L.segOff+=b.filter(x=>x.disabled).length;
   const t=document.getElementById('gaintile');
   if(t){window.__L.gain++;
     const v=parseFloat(String(t.textContent).replace(/[^0-9,.\\-−]/g,'').replace('−','-').replace(',','.'));
     const c=mgrCash()*1000;
     if(Math.abs(Math.abs(v)-Math.abs(c))<0.06||Math.abs(v-c)<0.06)window.__L.gainOk++;}
   return r};
 const sm=screenMacroEvent;
 screenMacroEvent=function(){const r=sm.apply(this,arguments);
   const h=document.querySelector('.evcard h3');const w=document.querySelector('.evwrap');
   window.__L.texte++;
   if(!h||!h.textContent.trim()||(w&&w.classList.contains('evhold')))window.__L.texteVide++;
   return r};
})();`;
const A={};
for(let i=0;i<6;i++){const r=playGame({file:process.argv[2]||'index.html',seed:900+i,
 prof:['syst','fonda','flux'][i%3],dur:'normal',probe:PROBE,collect:'JSON.stringify(window.__L)'});
 Object.entries(r.probe||{}).forEach(([k,v])=>A[k]=(A[k]||0)+v)}
console.log('debriefings : '+A.deb+' | avec le ruban du trimestre : '+A.debTape+' | avec l ancienne courbe : '+A.debOld);
console.log('ecrans du book : '+A.gain+' | tuile = tresorerie : '+A.gainOk);
console.log('cases de position rendues : '+A.seg+' | grisees (hors portee ou hors caisse) : '+A.segOff);
console.log('depeches : '+A.texte+' | texte absent ou retarde : '+A.texteVide);
