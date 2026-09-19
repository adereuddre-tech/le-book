/* Le book proposé par le desk remplit-il le mandat de risque ? */
const fs=require('fs'),{JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync(process.argv[2]||'index.html','utf8'),{runScripts:'dangerously',url:'https://x/',
 beforeParse(w){w.scrollTo=()=>{};w.setTimeout=f=>{try{f()}catch(e){}return 0}}});
setTimeout(()=>{console.log(dom.window.eval(`(()=>{
 const R={};['syst','fonda','flux'].forEach(pr=>{
  const rr=[];
  for(let s=1;s<=40;s++){
   newGame(s,pr,'std','inhouse','std','mid','com','normal');S.fundName='T';genRumors();
   const b=recoBook();const tg=S.tgt*(PROF().modelScale||1);
   rr.push(tg>0?b.vol/tg:0);
  }
  rr.sort((a,b)=>a-b);
  R[pr]={min:+rr[0].toFixed(2),d1:+rr[4].toFixed(2),med:+rr[20].toFixed(2),max:+rr[39].toFixed(2),
         vides:rr.filter(x=>x<0.5).length};
 });
 return JSON.stringify(R,null,1)})()`));dom.window.close()},1400);
