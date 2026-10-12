p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
rep("""function kap(i,a){const k=KAPPA[INSTR[i].sym];if(!k)return 0;const aa=Math.max(-3,Math.min(1.5,a||0));return k[0]+k[1]*aa}""",
    """function kap(i,a){const k=KAPPA[INSTR[i].sym];if(!k)return 0;const aa=Math.max(-4,Math.min(1.5,a||0));return k[0]+k[1]*aa}   /* lot 318 : panique jusqu'à −4 σ (VIX ≈ +14 %) */""")
rep("""κ = κ0 + χ·a, a = appétit pour le risque (en σ, borné à [−3 ; +1,5]).""","""κ = κ0 + χ·a, a = appétit pour le risque (en σ, borné à [−4 ; +1,5]).""")
open(p,'w',encoding='utf-8').write(s)
