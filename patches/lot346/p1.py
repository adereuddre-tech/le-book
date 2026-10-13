p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# portage structurel des actions et des obligations proportionnel au risque : κ = 0,066 × vol (même prime par unité de risque)
rep("""const KAPPA={ES:[0.012,0],NQ:[0.012,0],ESTX:[0.012,0],TOPX:[0.012,0],MXEF:[0.015,0],
 TN:[0.004,0],GBL:[0.004,0],R:[0.004,0],OAT:[0.004,0],JGB:[0.004,0],""","""const KRP=0.066;   /* lot 346 : prime de risque trimestrielle par point de vol annualisée, actions et obligations (κ = KRP·σ, lu à la volatilité courante) */
const KAPPA={ES:['rp',0],NQ:['rp',0],ESTX:['rp',0],TOPX:['rp',0],MXEF:['rp',0],
 TN:['rp',0],GBL:['rp',0],R:['rp',0],OAT:['rp',0],JGB:['rp',0],""")
rep("""function kap(i,a){const k=KAPPA[INSTR[i].sym];if(!k)return 0;const aa=Math.max(-4,Math.min(1.5,a||0));return k[0]+k[1]*aa}""",
    """function kap(i,a){const k=KAPPA[INSTR[i].sym];if(!k)return 0;const aa=Math.max(-4,Math.min(1.5,a||0));return (k[0]==='rp'?KRP*INSTR[i].sig:k[0])+k[1]*aa}""")
open(p,'w',encoding='utf-8').write(s)
