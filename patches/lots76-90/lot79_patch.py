import re
P='/home/claude/le-book/index.html';s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:90]);s=s.replace(old,new)
# 1. budgets élevés : coûts ×4/3, ×5/3, ×2 aux crans 4, 5, 6 ; bénéfices ramenés à 70 % de leur écart au standard
CM={4:4/3,5:5/3,6:2.0}
def lvfix(line):
    bps=[int(x) for x in re.findall(r'bp:(\d+)',line)]
    new=[round(b*CM.get(i,1)) for i,b in enumerate(bps)]
    it=iter(new);return re.sub(r'bp:\d+',lambda m:'bp:%d'%next(it),line)
for old in re.findall(r'lv:\[\{nm:"Minimal".*?\]\}',s):
    rep(old,lvfix(old))
K=0.70
def shrink(name,txt,rnd=2):
    m=re.search(re.escape(name)+r'\s*=\s*\[([^\]]*)\]',txt)
    a=[float(x) for x in m.group(1).split(',')];b=a[:]
    for i in (4,5,6):b[i]=a[3]+K*(a[i]-a[3])
    f=(lambda v:str(int(round(v)))) if rnd==0 else (lambda v:('%.3f'%v).rstrip('0').rstrip('.') if v!=int(v) else ('%.2f'%v))
    return m.group(0),m.group(0).replace(m.group(1),','.join(f(v) for v in b))
for nm,r in [('EXECM',2),('RISKM',2),('RISKS',2),('RETM ',2),('RESN',0),('RESREL',2),('RESR  ',2),('RESPH ',3),('TCVQ',2),('BANDB',2),('RISKRC',2),('STARP',2),('TAILM',2)]:
    o,n=shrink(nm,s,r);rep(o,n)
rep("const BUDMAX=5;","/* lot 79 : crans hauts deux fois plus chers au plus (×4/3, ×5/3, ×2) ; leurs effets ramenés à 70 % de leur\n   écart au standard */\nconst BUDMAX=5;")
# 2. concurrents : budget choisi au début de chaque trimestre en difficile, si la trésorerie le permet et si c'est utile
rep("rivSkill:0.120,rivVol:1.10,","rivSkill:0.150,rivVol:1.10,rivBud:1,")
rep("function rivalCostQ(){return (BUDGET.reduce((a,b)=>a+b.lv[3].bp,0)+DESK().fixed*1e4+16)*1e-4}",
"""function rivalCostQ(rv){const L=(rv&&rv.bl)||3;return (BUDGET.reduce((a,b)=>a+b.lv[L].bp,0)+DESK().fixed*1e4+16)*1e-4}
/* lot 79 : surcroît de rendement trimestriel d'un concurrent selon son cran de budget (les trois postes au même cran) */
const RIVBRET=[0,0,0,0,0.008,0.014,0.018];
function rivBudget(rv){
 rv.bl=3;rv.bRet=0;if(!(SIZE()&&SIZE().rivBud))return;
 const A=rv.mAum||S.aum0,cash=rv.mgr||0,c3=rivalCostQ({bl:3});
 /* l'argent pèse moins quand la caisse est pleine : λ = 1 à 3 % de l'encours en trésorerie */
 const lam=Math.max(0.5,Math.min(1.5,0.03*A/Math.max(1e-9,cash)));let best=0;
 for(let L=4;L<=6;L++){const dc=rivalCostQ({bl:L})-c3;
  if(cash<2*dc*A)break;                      /* deux trimestres de surcoût d'avance, sinon on ne monte pas */
  const u=RIVBRET[L]-lam*dc;if(u>best){best=u;rv.bl=L;rv.bRet=RIVBRET[L]}}
}""")
rep("const mg=v.mgmt*rv.mAum,cost=rivalCostQ()*rv.mAum;","const mg=v.mgmt*rv.mAum,cost=rivalCostQ(rv)*rv.mAum;")
rep("(S.rivals||[]).forEach(rv=>{rv.vq=rivVolQ(rv)});","(S.rivals||[]).forEach(rv=>{rv.vq=rivVolQ(rv);rivBudget(rv)});")
rep("return t*((v/2)*((RIVKS[r.style]||RIVK)*e+(RIVNOISE[r.style]||0.78)*rivNz(j,q))-0.008-rivDrag(v))-(t>=tt?tl:0);",
    "return t*((v/2)*((RIVKS[r.style]||RIVK)*e+(RIVNOISE[r.style]||0.78)*rivNz(j,q))-0.008-rivDrag(v)+(r.bRet||0))-(t>=tt?tl:0);")
# 3. nuage : les concurrents bougent pendant le trimestre
rep("function rivPt(rv){\n const s=rv.skill,K4=4,v=rivV(rv);let E;","function rivPt(rv,vv){\n const s=rv.skill,K4=4,v=vv||rivV(rv);let E;")
rep("return {x:v,y:S.rate/4+(v/2)*(RIVKS[rv.style]||RIVK)*E-0.008-rivDrag(v)-0.5*v*v/4-tailExp(v,1),",
    "return {x:v,y:S.rate/4+(v/2)*(RIVKS[rv.style]||RIVK)*E-0.008-rivDrag(v)+(rv.bRet||0)-0.5*v*v/4-tailExp(v,1),")
rep("R=(S.rivals||[]).map((rv,j)=>{const p=rivPt(rv);p.x/=2;",
    "R=(S.rivals||[]).map((rv,j)=>{const p=rivPtLive(rv,j);p.x/=2;")
rep("function rivCol(j){","""/* lot 79 : en séance, chaque concurrent ajuste son book à chaque nouvelle : il charge quand il gagne, allège
   quand il perd, et son attendu intègre ce que le trimestre a déjà montré. Affichage seulement. */
function rivPtLive(rv,j){
 if(S.phase!=='events'||!S.live)return rivPt(rv);
 const t=qElapsed(),rt=rivRet(j,t,S.q),v0=rivV(rv),step=S.evIdx||0;
 const jit=1+0.10*(prng32(hash32('rlive'+j+'_'+S.q+'_'+step,S.seed))()-0.5);
 const v=Math.max(0.6*v0,Math.min(1.3*v0,v0*Math.exp(1.6*rt)*jit)),p=rivPt(rv,v);
 p.y+=0.35*rt;return p}
function rivCol(j){""")
open(P,'w',encoding='utf-8').write(s);print('ok')
