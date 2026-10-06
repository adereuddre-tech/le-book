# Lot 235 : frein à la croissance proportionnel à la taille du fonds (choix d'Antoine). Retour à la formule initiale
# d'impact (racine carrée du notionnel) : le lot 232 (puissance 0,8 calée sur l'encours de départ) pénalisait d'abord
# les marchés liquides, où une unité de risque pèse un gros notionnel. Désormais :
#  - impact ×1,5 dès le départ (IMPC) : un gros ordre coûte plus cher qu'avant, même à 100 M$ ;
#  - facture entière (fourchette + impact) × (encours / encours de départ)^0,35 au-dessus de l'encours de départ
#    (BRK, jamais en dessous) : ×1,76 à 500 M$, ×2,85 à 2 Md$, le même pour tous les marchés, donc l'ordre des coûts
#    entre marchés liquides et illiquides est conservé ;
#  - concurrents : même formule, freinés selon leur propre encours (rivTurn, facture d'ordres type).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("""/* lot 232 : exposant d'impact 0,8 au lieu de 0,5, calé sur l'encours de départ (S.aum0) */
const IMPEXP=0.8;
function impScale(A){const a0=(S&&S.aum0)||0.1;return Math.pow(Math.max(0.05,(A===undefined?S.nav:A)/a0),IMPEXP-0.5)}
/* lot 234 */
let BRK=0.25;""","""/* lot 235 : impact ×1,5 ; facture × (encours / encours de départ)^0,35 au-dessus de l'encours de départ */
const IMPC=1.5;
let BRK=0.35;""")
rep("*depthMult(x,bn)*impScale())*TCK*brake();   /* lot 232 ; lot 234 : frein sur la facture entière */",
    "*depthMult(x,bn)*IMPC)*TCK*brake();   /* lot 235 : impact ×1,5, frein sur la facture entière */")
rep("RIVBP[L]*1e-4*(S.aum0||A)+16e-4*A*impScale(A)}","RIVBP[L]*1e-4*(S.aum0||A)+16e-4*A*brake(A)}")
rep("function rivTurn(w,w0){let c=0;INSTR.forEach((x,i)=>{const d=Math.abs(w[i]-((w0&&w0[i])||0));if(d>1e-9){const bn=d*S.nav;c+=d*(x.s+x.c*Math.sqrt(bn)*impScale())*TCK*brake()*RIVB.exec*1e-4}});return c}",
    "function rivTurn(w,w0,A){let c=0;INSTR.forEach((x,i)=>{const d=Math.abs(w[i]-((w0&&w0[i])||0));if(d>1e-9){const bn=d*S.nav;c+=d*(x.s+x.c*Math.sqrt(bn)*IMPC)*TCK*brake(A)*RIVB.exec*1e-4}});return c}   /* lot 235 : selon l'encours du concurrent */")
rep("rv._bkc=rivTurn(rv._bk,rv.wPrev)}","rv._bkc=rivTurn(rv._bk,rv.wPrev,rv.mAum)}")
rep("if(r)v-=rivTurn(w1,w)*(ev.stress?5:2);","if(r)v-=rivTurn(w1,w,rv.mAum)*(ev.stress?5:2);")
open('index.html','w',encoding='utf-8').write(s);print('lot235 ok')
