/* Lot 39 : une sauvegarde d'avant les onze crans porte des budgets 0/1/2 ; loadGame doit les
   remonter sur l'échelle (0→0, 1→4, 2→8). Sinon le joueur se réveille au tiers de son budget. */
const fs=require('fs');const {JSDOM,VirtualConsole}=require('jsdom');
const html=fs.readFileSync(process.argv[2]||'index.html','utf8');
const vc=new VirtualConsole();const errs=[];vc.on('jsdomError',e=>errs.push(String(e.message||e)));
const dom=new JSDOM(html,{runScripts:'dangerously',url:'https://x.test/',pretendToBeVisual:true,virtualConsole:vc,
 beforeParse(w){w.scrollTo=()=>{};w.setInterval=()=>0;w.setTimeout=f=>{try{f()}catch(e){errs.push('t:'+e.message)}return 0}}});
const w=dom.window,d=w.document,$=s=>d.querySelector(s);
setTimeout(()=>{
 /* une partie normale jusqu'au premier point de sauvegarde */
 if($('#tutooff'))$('#tutooff').click();
 if($('#found'))$('#found').click();
 if($('#go'))$('#go').click();
 let n=0;while(n++<60&&!w.eval('typeof S!=="undefined"&&S&&S.bud')){const b=[...d.querySelectorAll('button.cta')].filter(x=>!x.disabled)[0];if(b)b.click();else break}
 const raw=w.localStorage.getItem('lebook_save_v2');
 if(!raw){console.log('pas de sauvegarde');return}
 const o=JSON.parse(raw);const s=o.S||o.d||o.state||o;
 const st=s.bud?s:(s.S||{});
 st.bud={exec:2,risk:0,res:1,ret:1};delete st.budN;
 w.localStorage.setItem('lebook_save_v2',JSON.stringify(o));
 w.eval('loadGame()');
 console.log('après reprise :',w.eval('JSON.stringify(S.bud)'),'budN',w.eval('S.budN'),
   'bp',w.eval('budgetBp().toFixed(0)'),'erreurs',errs.length);
},900);
