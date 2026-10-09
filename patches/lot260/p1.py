p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# barème d'urgence + amortissement par le trader de la classe
rep("""function tcost(dk,i){""","""/* lot 260 : surcoût d'urgence en cours de trimestre. Dépêche : suivre le mouvement (prendre la liquidité) ×2,5,
   le contrer (la fournir) ×1,5 ; extrême (les deux familles) : ×4 et ×2. Un trader sur la classe réduit le surcoût d'un tiers. */
const URG={ev:{f:2.5,c:1.5},x:{f:4,c:2},tail:3};
function urgM(m,i){return covered(INSTR[i].grp)?1+(m-1)*2/3:m}
function tcost(dk,i){""")
rep("""  const tc=tcost(d,i);const c=tc.cost*(ev.stress?5:2)*S.tcMultQ*(S.leakQ?1.45:1);""",
    """  const tc=tcost(d,i);const c=tc.cost*urgM((ev.x?URG.x:URG.ev)[a>0?'f':'c'],i)*S.tcMultQ*(S.leakQ?1.45:1);   /* lot 260 */""")
rep("""if(d)imp+=tcost(d,m).cost*5}""","""if(d)imp+=tcost(d,m).cost*urgM(URG.tail,m)}   /* lot 260 : ×3 (×5 avant) */""")
# rivalité ×1,5, stop ×1,3, appel de marge ×1,3 / ×1,8 : le trader amortit aussi
s=s.replace("tcost(nk-S.k[i],i).cost*1.5*S.tcMultQ","tcost(nk-S.k[i],i).cost*urgM(1.5,i)*S.tcMultQ")
s=s.replace("tcost(hF-S.k[i],i).cost*1.5*S.tcMultQ","tcost(hF-S.k[i],i).cost*urgM(1.5,i)*S.tcMultQ")
s=s.replace("tcost(hD-S.k[i],i).cost*1.5*S.tcMultQ","tcost(hD-S.k[i],i).cost*urgM(1.5,i)*S.tcMultQ")
s=s.replace("tcost(-nk-S.k[i],i).cost*1.5*S.tcMultQ","tcost(-nk-S.k[i],i).cost*urgM(1.5,i)*S.tcMultQ")
rep("const tt=tcost(target-S.k[i],i);cost=tt.cost*1.5*S.tcMultQ;","const tt=tcost(target-S.k[i],i);cost=tt.cost*urgM(1.5,i)*S.tcMultQ;")
rep("const d=-Math.sign(k[bi]);c1+=tcost(d,bi).cost*1.3;k[bi]+=d}","const d=-Math.sign(k[bi]);c1+=tcost(d,bi).cost*urgM(1.3,bi);k[bi]+=d}")
rep("let c2=0;for(let i=0;i<N;i++){const d=k2[i]-S.k[i];if(d)c2+=tcost(d,i).cost*MGC.crisis}","let c2=0;for(let i=0;i<N;i++){const d=k2[i]-S.k[i];if(d)c2+=tcost(d,i).cost*urgM(MGC.crisis,i)}")
rep("let c=0;for(let i=0;i<N;i++){const d=k1[i]-S.k[i];if(d)c+=tcost(d,i).cost*1.3}","let c=0;for(let i=0;i<N;i++){const d=k1[i]-S.k[i];if(d)c+=tcost(d,i).cost*urgM(1.3,i)}")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep("Les montants portent sur votre book entier, hors coûts d'ajustement, que paie votre société de gestion ;",
    "Les montants portent sur votre book entier, hors coûts d'ajustement, que paie votre société de gestion. Ces ordres d'urgence coûtent plus cher que ceux du début de trimestre : suivre le mouvement, c'est acheter ce que tout le monde achète (×2,5, ×4 sur un extrême) ; le contrer, c'est fournir la liquidité dont les autres ont besoin (×1,5, ×2 sur un extrême) ; un trader sur la classe retire un tiers de ce surcoût ;")
open(p,'w',encoding='utf-8').write(s)
