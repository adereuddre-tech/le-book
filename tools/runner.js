// node runner.js plan.json out.jsonl  — plan = [{...opts}], reprend là où il s'est arrêté
const fs=require('fs');const {playGame}=require(require('path').join(__dirname,'bot.js'));
const plan=JSON.parse(fs.readFileSync(process.argv[2]));const out=process.argv[3];
const done=fs.existsSync(out)?fs.readFileSync(out,'utf8').trim().split('\n').filter(Boolean).length:0;
const lim=+(process.argv[4]||1e9);
for(let i=done;i<Math.min(plan.length,done+lim);i++){let r;try{r=playGame(plan[i])}catch(e){r={crash:String(e),cfg:plan[i]}}
 r.tag=plan[i].tag;fs.appendFileSync(out,JSON.stringify(r)+'\n');if(i%10===0&&global.gc)global.gc()}
if(done+lim>=plan.length)fs.appendFileSync(out+'.fin','ok\n');
