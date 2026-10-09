p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("""function urgM(m,i){return covered(INSTR[i].grp)?m*2/3:m}""","""function urgM(m,i){return covered(INSTR[i].grp)?m*2/3:m}
/* lot 262 : à contre-sens, on fournit la liquidité et le marché cède une décote, croissante avec la taille de l'ordre :
   k × √(unités) pb du notionnel, plafonnée — dépêche 2,5 pb (6 pb au plus), extrême 15 pb (40 pb au plus). Les coûts
   normaux sont de 2 à 4 pb du notionnel : un gros ordre à contre-sens dans un extrême coûte moins que rien. */
const REB={ev:{k:2.5,cap:6},x:{k:15,cap:40}};
function urgF(m,i){return Math.max(1,urgM(m,i))}   /* coupes forcées (stop, appel de marge) : jamais sous le tarif normal */""")
rep("""  const tc=tcost(d,i);const c=tc.cost*urgM((ev.x?URG.x:URG.ev)[a>0?'f':'c'],i)*S.tcMultQ*(S.leakQ?1.45:1);   /* lot 260 */""",
    """  const tc=tcost(d,i),um=urgM((ev.x?URG.x:URG.ev)[a>0?'f':'c'],i)*S.tcMultQ*(S.leakQ?1.45:1),RB=ev.x?REB.x:REB.ev;   /* lot 260 */
  const c=tc.cost*um-(a<0?Math.min(RB.cap,RB.k*Math.sqrt(Math.abs(d)))*1e-4*tc.bn:0);   /* lot 262 : à contre-sens, décote cédée par le marché */""")
rep("""'ordres −'+mm(o.cost)""","""(o.cost<0?'rabais +'+mm(-o.cost):'ordres −'+mm(o.cost))""")
rep("""<span class="${o.cost>0?'neg-g':'dim-g'}">${o.n===0""","""<span class="${o.cost>0?'neg-g':o.cost<0?'pos-g':'dim-g'}">${o.n===0""")
rep("""${free?`Coût ${nb(mm(cost))} offert par le desk`:`Coût ${nb(mm(cost))} à votre charge`}""",
    """${free?`Coût ${nb(mm(cost))} offert par le desk`:cost<0?`Rabais de ${nb(mm(-cost))} pour votre société de gestion : vous fournissez la liquidité que les autres cherchent`:`Coût ${nb(mm(cost))} à votre charge`}""")
rep("const d=-Math.sign(k[bi]);c1+=tcost(d,bi).cost*urgM(1.3,bi);k[bi]+=d}","const d=-Math.sign(k[bi]);c1+=tcost(d,bi).cost*urgF(1.3,bi);k[bi]+=d}")
rep("let c=0;for(let i=0;i<N;i++){const d=k1[i]-S.k[i];if(d)c+=tcost(d,i).cost*urgM(1.3,i)}","let c=0;for(let i=0;i<N;i++){const d=k1[i]-S.k[i];if(d)c+=tcost(d,i).cost*urgF(1.3,i)}")
rep("c2+=tcost(d,i).cost*urgM(MGC.crisis,i)}","c2+=tcost(d,i).cost*urgF(MGC.crisis,i)}")
rep("le contrer, c'est fournir la liquidité dont les autres ont besoin (×1, ×1,5 sur un extrême) ; un trader sur la classe retire un tiers du coût (contrer une dépêche : ×0,67) ;",
    "le contrer, c'est fournir la liquidité dont les autres ont besoin : coût ×1 (×1,5 sur un extrême), moins une décote que le marché vous cède, d'autant plus forte que l'ordre est gros (jusqu'à 6 pb du notionnel sur une dépêche, 40 pb sur un extrême) — un gros ordre à contre-sens dans un extrême vous rapporte ; un trader sur la classe retire un tiers des surcoûts ;")
open(p,'w',encoding='utf-8').write(s)
