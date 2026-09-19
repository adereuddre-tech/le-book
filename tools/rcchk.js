/* La note du comite doit decroitre des qu'on s'ecarte du mandat, dans les deux sens,
   et etre calculee sur la volatilite AFFICHEE. */
const fs=require('fs'),{JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync(process.argv[2]||'index.html','utf8'),{runScripts:'dangerously',url:'https://x/',
 beforeParse(w){w.scrollTo=()=>{};w.setTimeout=f=>{try{f()}catch(e){}return 0}}});
setTimeout(()=>{console.log(dom.window.eval(`(()=>{
 newGame(4,'fonda','std','inhouse','std','mid','com','normal');S.fundName='T';genRumors();
 const R=recoBook(),out=[];let prev=null,mono=true;
 for(let a=0.2;a<=2.2001;a+=0.2){
  const k=R.k.map(v=>Math.max(-S.maxk,Math.min(S.maxk,Math.round(v*a))));
  const w=weights(k),shown=riskShown(w).total,plain=pvol(w),rc=riskRc(k);
  out.push('x'+a.toFixed(1)+'  affiche '+(shown*100).toFixed(1)+' %  brut '+(plain*100).toFixed(1)
   +' %  cible '+(S.tgt*100).toFixed(0)+' %  comite '+rc.toFixed(1));
 }
 return out.join('\\n')})()`));dom.window.close()},1400);
