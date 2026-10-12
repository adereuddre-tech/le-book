p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
rep("""const KAPPA={ES:[0.012,0],NQ:[0.012,0],ESTX:[0.012,0],TOPX:[0.012,0],MXEF:[0.012,0],TN:[0.004,0],GBL:[0.004,0],R:[0.004,0],OAT:[0.004,0],JGB:[0.004,0],VX:[-0.085,0.085/1.5]};""",
"""/* lot 317 : tableau complet. Devises : écart de taux ; χ = κ0/1,5 — le portage s'annule à −1,5 σ d'appétit et s'inverse au-delà
   (débouclage des carry trades, rachat des devises de financement). Matières et crypto : coût de stockage ou de financement. */
const KAPPA={ES:[0.012,0],NQ:[0.012,0],ESTX:[0.012,0],TOPX:[0.012,0],MXEF:[0.015,0],
 TN:[0.004,0],GBL:[0.004,0],R:[0.004,0],OAT:[0.004,0],JGB:[0.004,0],
 AUD:[0.005,0.005/1.5],MXP:[0.010,0.010/1.5],GBP:[0.002,0.002/1.5],EUR:[-0.002,-0.002/1.5],JPY:[-0.005,-0.005/1.5],
 GC:[-0.002,0],KC:[-0.005,0],ZW:[-0.005,0],BTC:[-0.005,0],
 VX:[-0.085,0.085/1.5]};""")
open(p,'w',encoding='utf-8').write(s)
