const fs=require('fs');const {JSDOM,VirtualConsole}=require('jsdom');
const dom=new JSDOM(fs.readFileSync(process.argv[2],'utf8'),{runScripts:'dangerously',url:'https://x.test/',pretendToBeVisual:true,virtualConsole:new VirtualConsole(),beforeParse(w){w.scrollTo=()=>{};w.setInterval=()=>0;w.setTimeout=f=>{try{f()}catch(e){}return 0}}});
const w=dom.window,d=w.document,$=s=>d.querySelector(s);
for(let i=0;i<200;i++){if($('#send'))break;const t=$('#tutooff');if(t){t.click();continue}if($('#found')){$('#found').click();continue}
 let hit=false;for(const id of ['#ok','#go2','#rgo','#pgo','#nx','#go']){const b=$(id);if(b&&!b.disabled){b.click();hit=true;break}}if(hit)continue;
 const ch=d.querySelectorAll('.choice:not([disabled])');if(ch.length){ch[0].click();continue}
 const any=[...d.querySelectorAll('button.cta')].filter(b=>!b.disabled);if(any.length){any[0].click();continue}break}
console.log(w.eval(`(()=>{const i=IDX.ES,j=IDX.TN;const a=tcost(1,i).cost,b=tcost(1,j).cost;S.stars=["Actions"];const a2=tcost(1,i).cost,b2=tcost(1,j).cost;return [a2/a,b2/b].map(x=>x.toFixed(2)).join(" ")})()`));
