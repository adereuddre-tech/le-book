const fs=require('fs'),{JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',url:'https://x/',
 beforeParse(w){w.scrollTo=()=>{};w.setTimeout=f=>{try{f()}catch(e){}return 0}}});
setTimeout(()=>{console.log(dom.window.eval(`(()=>{
 newGame(4,'fonda','std','inhouse','std','mid','com','normal');S.fundName='T';
 const h=gz(-2,-1);
 const d=document.createElement('div');d.innerHTML=h;
 return 'sortie : '+h+'\\n  elements de premier niveau : '+d.children.length+' (1 attendu)'
  +'\\n  texte : « '+d.textContent+' » ('+d.textContent.length+' caracteres)';
})()`));dom.window.close()},1200);
