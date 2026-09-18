/* Le trait ne doit progresser que sur les données nouvelles : deux polylignes, l'ancienne
   posée d'emblée, la nouvelle animée. Et le ruban doit être dense. */
const {playGame}=require('./bot.js');
const PROBE=`(function(){
 window.__R={rend:0,deux:0,fige:0,pts:[],neuf:[],texte:0,texteVide:0};
 const sb=statusBar;
 statusBar=function(){const h=sb.apply(this,arguments);
  if(S.phase==='events'&&S.tape&&S.tape.pts.length>2){
   window.__R.rend++;
   const stat=(h.match(/<polyline points=/g)||[]).length;
   const anim=(h.match(/<polyline class="tapedraw"/g)||[]).length;
   if(stat&&anim)window.__R.deux++;
   if(stat&&!anim)window.__R.fige++;
   window.__R.pts.push(S.tape.pts.length);
   window.__R.neuf.push(S.tape.pts.length-(S.tape.from||0));
  }
  return h};
 const sm=screenMacroEvent;
 screenMacroEvent=function(){const r=sm.apply(this,arguments);
   const h=document.querySelector('.evcard h3');
   window.__R.texte++; if(!h||!h.textContent.trim())window.__R.texteVide++;
   return r};
})();`;
let A={rend:0,deux:0,fige:0,texte:0,texteVide:0},P=[],Nv=[];
for(let i=0;i<6;i++){const r=playGame({file:process.argv[2]||'index.html',seed:800+i,
  prof:['syst','fonda','flux'][i%3],dur:'normal',probe:PROBE,collect:'JSON.stringify(window.__R)'});
 const p=r.probe||{};['rend','deux','fige','texte','texteVide'].forEach(k=>A[k]+=p[k]||0);
 P=P.concat(p.pts||[]);Nv=Nv.concat(p.neuf||[])}
const med=a=>{a=a.slice().sort((x,y)=>x-y);return a[a.length>>1]};
console.log(A.rend+' rendus du ruban');
console.log('  deux traits (ancien pose + nouveau anime) : '+A.deux+' | un seul trait : '+A.fige);
console.log('  points du ruban : mediane '+med(P)+', max '+Math.max(...P));
console.log('  points nouveaux par rendu : mediane '+med(Nv));
console.log('  ecrans de depeche : '+A.texte+' | titre vide : '+A.texteVide);
