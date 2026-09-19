/* Le ruban doit finir sur le chiffre NET affiche en haut de l'ecran. */
const {playGame}=require('./bot.js');
const PROBE=`(function(){window.__F=[];const sd=screenDebrief;
 screenDebrief=function(o){const r=sd.apply(this,arguments);
  if(S.tape&&S.tape.pts.length>2){
   const y0=Math.floor(S.q/4)*4;let base=1;for(let i=0;i<y0;i++)base*=(1+S.rets[i]);
   window.__F.push({ruban:+(S.tape.pts[S.tape.pts.length-1]-100).toFixed(1),
                    tuile:+((S.idx/base-1)*100).toFixed(1)});}
  return r};})();`;
let F=[];
for(let i=0;i<6;i++){const r=playGame({file:process.argv[2]||'index.html',seed:1100+i,prof:['syst','fonda','flux'][i%3],dur:'normal',probe:PROBE,collect:'JSON.stringify(window.__F)'});F=F.concat(r.probe||[])}
const d=F.map(x=>Math.abs(x.ruban-x.tuile));
console.log(F.length+' cloturés | ecart max ruban/tuile : '+Math.max(0,...d).toFixed(2)+' pts | exemples '+JSON.stringify(F.slice(0,3)));
