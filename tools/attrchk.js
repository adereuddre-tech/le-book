/* attrchk.js — l'attribution factorielle affichée au débriefing explique-t-elle vraiment le
   brut du trimestre ? On compare la somme des quatre barres à la performance réelle des
   positions, sur des clôtures réelles. */
const {playGame}=require('./bot.js');
const PROBE=`(function(){
 window.__A=[];
 const sd=screenDebrief;
 screenDebrief=function(o){
   const sum=o.attr.reduce((a,b)=>a+b,0);
   window.__A.push({gross:+(o.gross*1e4).toFixed(1),attr:+(sum*1e4).toFixed(1),
                    resid:+((o.gross-sum)*1e4).toFixed(1)});
   return sd.apply(this,arguments)};
})();`;
let R=[];
for(let i=0;i<12;i++){
  const r=playGame({file:process.argv[2]||'index.html',seed:300+i,prof:['syst','fonda','flux'][i%3],dur:'normal',
    probe:PROBE,collect:'JSON.stringify(window.__A)'});
  R=R.concat(r.probe||[]);
}
const n=R.length;
const mean=a=>a.reduce((x,y)=>x+y,0)/a.length;
const sd=a=>{const m=mean(a);return Math.sqrt(mean(a.map(x=>(x-m)**2)))};
const g=R.map(x=>x.gross),a=R.map(x=>x.attr),d=R.map(x=>x.resid);
/* part de la variance du brut expliquée par la somme des facteurs */
const cov=mean(R.map(x=>(x.gross-mean(g))*(x.attr-mean(a))));
const beta=cov/ (sd(a)**2||1e-9), r2=(cov/(sd(g)*sd(a)||1e-9))**2;
console.log(n+' clotures');
console.log('brut du trimestre        : moyenne '+mean(g).toFixed(1)+' pb, ecart-type '+sd(g).toFixed(1));
console.log('somme des 4 facteurs     : moyenne '+mean(a).toFixed(1)+' pb, ecart-type '+sd(a).toFixed(1));
console.log('residu (brut - facteurs) : moyenne '+mean(d).toFixed(1)+' pb, ecart-type '+sd(d).toFixed(1));
console.log('pente brut~facteurs '+beta.toFixed(2)+' (1,00 si l echelle est bonne), R2 '+r2.toFixed(2));
