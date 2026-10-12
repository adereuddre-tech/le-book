p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)

# tickers : seulement pour les pré-annonces d'une dépêche qui touche des marchés ; les rumeurs de facteurs n'affichent que la macro
rep("""const tk=r=>{let L;if(r.hit)L=Object.keys(r.hit).filter(sy=>IDX[sy]!==undefined&&mktOpen(IDX[sy])).map(sy=>({sy,z:r.hit[sy]}));
   else L=INSTR.map((x,i)=>({sy:x.sym,i,z:x.b.reduce((a,b,k)=>a+b*(r.v[k]||0),0)})).filter(o=>mktOpen(o.i));""",
    """const tk=r=>{if(!r.hit)return '';let L=Object.keys(r.hit).filter(sy=>IDX[sy]!==undefined&&mktOpen(IDX[sy])).map(sy=>({sy,z:r.hit[sy]}));""")
open(p,'w',encoding='utf-8').write(s)
