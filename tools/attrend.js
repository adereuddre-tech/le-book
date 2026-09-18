/* Vérifie que la cascade affichée au débriefing boucle : quatre facteurs + part propre = brut. */
const {playGame}=require('./bot.js');
const PROBE=`(function(){window.__A=[];const sd=screenDebrief;
 screenDebrief=function(o){const r=sd.apply(this,arguments);
  const t=document.body.textContent||'';
  const has=/Part propre des marchés/.test(t);
  const sum=o.attr.reduce((a,b)=>a+b,0)+(o.gross-o.attr.reduce((a,b)=>a+b,0));
  window.__A.push({has,ecart:+((sum-o.gross)*1e4).toFixed(3)});
  return r};})();`;
let R=[];
for(let i=0;i<6;i++){const r=playGame({file:process.argv[2]||'index.html',seed:400+i,prof:['syst','fonda','flux'][i%3],dur:'normal',probe:PROBE,collect:'JSON.stringify(window.__A)'});R=R.concat(r.probe||[])}
console.log(R.length+' clotures | ligne « part propre » presente : '+R.filter(x=>x.has).length
  +' | ecart max du total au brut : '+Math.max(0,...R.map(x=>Math.abs(x.ecart))).toFixed(4)+' pb');
