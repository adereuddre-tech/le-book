const fs=require('fs'),{JSDOM}=require('jsdom');
const dom=new JSDOM(fs.readFileSync('index.html','utf8'),{runScripts:'dangerously',url:'https://x/',
 beforeParse(w){w.scrollTo=()=>{};w.setTimeout=f=>{try{f()}catch(e){}return 0}}});
setTimeout(()=>{console.log(dom.window.eval(`(()=>{
 const out=[];
 ['small','mid','mega'].forEach(sz=>{
  newGame(3,'fonda','std','inhouse','std',sz,'com','normal');S.fundName='T';
  /* newGame appelle deja planQuarter : la commission de gestion du T1 est deja versee */
  const purse=mgrCash()+(S.qOps||0);
  const maxbp=BUDGET.reduce((a,b)=>a+b.lv[b.lv.length-1].bp,0)+DESK().fixed*1e4;
  const minbp=BUDGET.reduce((a,b)=>a+b.lv[0].bp,0)+DESK().fixed*1e4;
  const ok=i=>budgetBpIf('exec',2)*1e-4*S.nav<=purse;
  out.push(sz.padEnd(6)+' encours '+(S.nav*1000).toFixed(0)+' M$ | caisse T1 '+(purse*1000).toFixed(2)+' M$ ('
   +(purse/S.nav*1e4).toFixed(0)+' pb) | tout au max '+maxbp.toFixed(0)+' pb = '+(maxbp*1e-4*S.nav*1000).toFixed(2)
   +' M$ → '+(maxbp*1e-4*S.nav<=purse?'POSSIBLE (probleme)':'impossible (voulu)')
   +' | minimum '+minbp.toFixed(0)+' pb toujours payable : '+(minbp*1e-4*S.nav<=purse));
 });
 return out.join('\\n')})()`));dom.window.close()},1200);
