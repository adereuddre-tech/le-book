const fs=require('fs');const {JSDOM,VirtualConsole}=require('jsdom');
const html=fs.readFileSync(process.argv[2],'utf8');const errs=[];
const vc=new VirtualConsole();vc.on('jsdomError',e=>errs.push(String(e.message||e)));
const dom=new JSDOM(html,{runScripts:'dangerously',url:'https://x.test/',pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){w.scrollTo=()=>{};w.setInterval=()=>0;w.setTimeout=f=>{try{f()}catch(e){}return 0}}});
const w=dom.window,d=w.document,$=s=>d.querySelector(s);w.onerror=m=>errs.push(m);
for(let i=0;i<200;i++){if($('#send'))break;const t=$('#tutooff');if(t){t.click();continue}if($('#found')){$('#found').click();continue}
 let hit=false;for(const id of ['#ok','#go2','#rgo','#pgo','#nx','#go']){const b=$(id);if(b&&!b.disabled){b.click();hit=true;break}}if(hit)continue;
 const ch=d.querySelectorAll('.choice:not([disabled])');if(ch.length){ch[0].click();continue}
 const any=[...d.querySelectorAll('button.cta')].filter(b=>!b.disabled);if(any.length){any[0].click();continue}break}
console.log(w.eval(`(()=>{const R=recoBook();S.k=R.k.map(v=>Math.max(-S.maxk,Math.min(S.maxk,Math.round(v))));S.lastR=S.lastR||S.k.map(()=>0.01);
let n=0,nul=0,shown=0,bad=[];const k0=[...S.k];
const pools={mid:[...TRADER_MID,...STAKE,...BOARDEV],exec:[...TRADER_EXEC]};
for(const m in pools)for(const ev of pools[m])for(const c of (ev.ch||[])){n++;const p=kPrev(c.e||{},m);if(!p){nul++;bad.push(ev.t);continue}
 const h=bkD(p.k,p.cost,p.hid);if(h)shown++;if(h.includes('NaN')||h.includes('undefined'))bad.push('NaN '+ev.t)}
const same=S.k.every((v,i)=>v===k0[i]);
return JSON.stringify({n,nul,shown,same,bad:bad.slice(0,5),map:riskMap(riskShown(weights(S.k)).total,true).includes('NaN'),mapS:riskMap(riskShown(weights(S.k)).total,false).includes('NaN')})})()`));
console.log('errs',errs.slice(0,3));
