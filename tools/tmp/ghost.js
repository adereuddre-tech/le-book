const fs=require('fs');const {JSDOM,VirtualConsole}=require('jsdom');
const dom=new JSDOM(fs.readFileSync(process.argv[2],'utf8'),{runScripts:'dangerously',url:'https://x.test/',pretendToBeVisual:true,virtualConsole:new VirtualConsole(),beforeParse(w){w.scrollTo=()=>{};w.setInterval=()=>0;w.setTimeout=f=>{try{f()}catch(e){}return 0}}});
const w=dom.window,d=w.document,$=s=>d.querySelector(s);
for(let i=0;i<200;i++){if($('#send'))break;const t=$('#tutooff');if(t){t.click();continue}if($('#found')){$('#found').click();continue}
 let hit=false;for(const id of ['#ok','#go2','#rgo','#pgo','#nx','#go']){const b=$(id);if(b&&!b.disabled){b.click();hit=true;break}}if(hit)continue;
 const ch=d.querySelectorAll('.choice:not([disabled])');if(ch.length){ch[0].click();continue}
 const any=[...d.querySelectorAll('button.cta')].filter(b=>!b.disabled);if(any.length){any[0].click();continue}break}
console.log(w.eval(`(()=>{const o=[];const sp=()=>riskShown(weights(S.k)).total;
riskMap(sp(),false);S.k[0]=2;S.k[1]=-1;riskMap(sp(),false);o.push(JSON.stringify(S._kGhost.slice(0,3)));
S.k[2]=1;riskMap(sp(),false);o.push(JSON.stringify(S._kGhost.slice(0,3)));riskMap(sp(),true);o.push(JSON.stringify(S._kGhost.slice(0,3)));
return o.join(' | ')})()`));
