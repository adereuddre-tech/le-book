/* Verrou a la case : quand la tresorerie fond, les positions trop cheres doivent griser. */
const fs=require('fs'),{JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',url:'https://x/',
 beforeParse(w){w.scrollTo=()=>{};w.setTimeout=f=>{try{f()}catch(e){}return 0}}});
setTimeout(()=>{console.log(dom.window.eval(`(()=>{
 const out=[];TUTO=false;SHOWHINTS=false;
 newGame(3,'fonda','std','inhouse','std','mid','com','normal');S.fundName='T';S.tuto=99;
 genRumors();
 [999,0.40,0.12,0.02,0].forEach(cap=>{
  S.mgrCosts=0;S.mgrFees=0;S.mgrCap0=cap/1000;S.k=new Array(N).fill(0);S.k0=new Array(N).fill(0);
  screenPlay();
  const b=[...document.querySelectorAll('.seg button')].filter(x=>Math.abs(+x.dataset.v)<=S.maxk);
  const off=b.filter(x=>x.disabled).length;
  const send=document.getElementById('send');
  out.push('tresorerie '+(cap===999?'illimitee':(cap*1000).toFixed(0)+' k$').padEnd(12)
    +' cases utiles '+b.length+', grisees '+String(off).padStart(3)+' ('+(100*off/b.length).toFixed(0)+' %)'
    +' | bouton : '+(send?send.textContent.trim():'?'));
 });
 return out.join('\\n')})()`));dom.window.close()},1400);
