/* Vérifie l'écran de mi-parcours : plus de courbe, et la décomposition annoncée est juste. */
const {playGame}=require('./bot.js');
const PROBE=`(function(){
 window.__M=[];
 const mm=screenMidMark;
 screenMidMark=function(){
  const r=mm.apply(this,arguments);
  const t=document.querySelector('.rescard p').textContent.replace(/\\s+/g,' ');
  const y=ytdIdx();
  window.__M.push({courbes:document.querySelectorAll('.rescard svg.navc').length,
                   ruban:document.querySelectorAll('.tape svg.navc').length,
                   hold:document.querySelectorAll('.evhold').length,
                   ytd:+(y.now-100).toFixed(2), txt:t.slice(0,150)});
  return r};
})();`;
let M=[];
for(let i=0;i<6;i++){const r=playGame({file:process.argv[2]||'index.html',seed:600+i,
  prof:['syst','fonda','flux'][i%3],dur:'normal',probe:PROBE,collect:'JSON.stringify(window.__M)'});
  M=M.concat(r.probe||[])}
console.log(M.length+' ecrans de mi-parcours');
console.log('  courbes dans la carte : '+M.reduce((a,x)=>a+x.courbes,0)+' (0 attendu)');
console.log('  ruban present         : '+M.filter(x=>x.ruban>0).length+' / '+M.length);
M.slice(0,3).forEach(x=>console.log('  ytd calcule '+x.ytd.toFixed(2)+' % | texte : '+x.txt));
