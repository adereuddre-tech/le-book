/* Vérifie que la flèche de la barre d'état, sur l'écran de bilan d'une dépêche, raconte la
   MÊME chose que la ligne « Effets » de la carte. Avant correction, la flèche ne montrait
   que le dernier appel à gauge() et pouvait annoncer −2 quand la carte disait −9. */
const {playGame}=require('./bot.js');
const PROBE=`(function(){
 window.__E=[];
 const rc=resultCard;
 resultCard=function(kick,title,paras,rows,btn,next,extra){
  const r=rc.apply(this,arguments);
  if(/DÉPÊCHE/.test(kick)){
   const card=[...document.querySelectorAll('.rescard td,.rescard th')].map(x=>x.textContent).join(' ');
   const m=card.match(/investisseurs\\s*([+−-]?\\s*[\\d,]+)/i), n=card.match(/comité\\s*([+−-]?\\s*[\\d,]+)/i);
   const t=document.querySelector('[data-gauge=lp] span b');
   const a=t?t.textContent.match(/(\\d+)→(\\d+)/):null;
   if(m&&a){
    const dit=parseFloat(m[1].replace('−','-').replace(',','.').replace(/\\s/g,''));
    const fait=(+a[2])-(+a[1]);
    window.__E.push({dit:Math.round(dit),fait});
   }
  }
  return r};
})();`;
let ok=0,ko=0,ex=[];
for(let i=0;i<10;i++){
  const r=playGame({file:process.argv[2]||'index.html',seed:200+i,prof:['syst','fonda','flux'][i%3],dur:'normal',
    probe:PROBE,collect:'JSON.stringify(window.__E)'});
  (r.probe||[]).forEach(x=>{ if(Math.abs(x.dit-x.fait)<=1) ok++; else {ko++; if(ex.length<6)ex.push(x)} });
}
console.log('bilans de dépêche vérifiés : %d cohérents, %d incohérents', ok, ko);
if(ko)console.log('exemples (dit / fait) :',JSON.stringify(ex));
