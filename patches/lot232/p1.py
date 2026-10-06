# Lot 232 : impact de marché plus raide avec l'encours — frein à la progression au-delà de quelques centaines de M$.
# L'impact d'un ordre croissait en racine carrée du notionnel (p = 0,5). Il croît désormais en notionnel^0,8, calé sur
# l'encours de départ : le terme d'impact est multiplié par (encours / encours de départ)^0,3. À l'encours de départ rien
# ne change ; à 1 Md$ (départ 100 M$) l'impact pèse 2,0 fois plus, à 2 Md$ 2,5 fois plus. S'applique à tout ce qui passe
# par tcost : book, renforts et contres des dépêches, rivalité, accidents, affichage compris. Les concurrents suivent la
# même loi (rotation du book, 16 pb d'ordres sur leur encours). Plafond d'impact par exécution (1,5 % de l'encours) retiré.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("const TCK=3;\nfunction tcost(dk,i){",
"""const TCK=3;
/* lot 232 : exposant d'impact 0,8 au lieu de 0,5, calé sur l'encours de départ (S.aum0) */
const IMPEXP=0.8;
function impScale(A){const a0=(S&&S.aum0)||0.1;return Math.pow(Math.max(0.05,(A===undefined?S.nav:A)/a0),IMPEXP-0.5)}
function tcost(dk,i){""")
rep("bp=(x.s+x.c*Math.pow(bnE,pw)*(pw===0.5?1:1.9)*depthMult(x,bn))*TCK;","bp=(x.s+x.c*Math.pow(bnE,pw)*(pw===0.5?1:1.9)*depthMult(x,bn)*impScale())*TCK;   /* lot 232 */")
rep("return -Math.min(IMPK*bill*execImpactF(m,leak),IMPMAX*S.nav);","return -IMPK*bill*execImpactF(m,leak);   /* lot 232 : plafond de 1,5 % de l'encours retiré */")
rep("c+=d*(x.s+x.c*Math.sqrt(bn))*TCK*RIVB.exec*1e-4}});return c}","c+=d*(x.s+x.c*Math.sqrt(bn)*impScale())*TCK*RIVB.exec*1e-4}});return c}   /* lot 232 */")
rep("function rivalCostAmt(rv,A){const L=(rv&&rv.bl)||3;return RIVBP[L]*1e-4*(S.aum0||A)+16e-4*A}","function rivalCostAmt(rv,A){const L=(rv&&rv.bl)||3;return RIVBP[L]*1e-4*(S.aum0||A)+16e-4*A*impScale(A)}   /* lot 232 : ordres au même frein que le joueur */")
rep("c = impact en pb par √(Md$) — loi en racine carrée","c = impact en pb par √(Md$) à l'encours de départ ; au-delà, l'impact croît en notionnel^0,8 (lot 232)")
rep("Chaque changement de position paie une demi-fourchette plus un impact en racine carrée du notionnel, multiplié","Chaque changement de position paie une demi-fourchette plus un impact qui croît en racine carrée du notionnel, puis de plus en plus vite quand l'encours dépasse celui du départ (puissance 0,8), multiplié")
open('index.html','w',encoding='utf-8').write(s);print('lot232 ok')
