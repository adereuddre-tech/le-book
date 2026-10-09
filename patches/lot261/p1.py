p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("""   le contrer (la fournir) ×1,5 ; extrême (les deux familles) : ×4 et ×2. Un trader sur la classe réduit le surcoût d'un tiers. */
const URG={ev:{f:2.5,c:1.5},x:{f:4,c:2},tail:3};
function urgM(m,i){return covered(INSTR[i].grp)?1+(m-1)*2/3:m}""","""   le contrer (la fournir) ×1,5 ; extrême (les deux familles) : ×4 et ×2. Un trader sur la classe réduit le surcoût d'un tiers.
   lot 261 : contrer ×1 (dépêche) et ×1,5 (extrême) ; le trader multiplie le coût par 2/3 (contrer une dépêche : ×0,67). */
const URG={ev:{f:2.5,c:1},x:{f:4,c:1.5},tail:3};
function urgM(m,i){return covered(INSTR[i].grp)?m*2/3:m}""")
rep("le contrer, c'est fournir la liquidité dont les autres ont besoin (×1,5, ×2 sur un extrême) ; un trader sur la classe retire un tiers de ce surcoût ;",
    "le contrer, c'est fournir la liquidité dont les autres ont besoin (×1, ×1,5 sur un extrême) ; un trader sur la classe retire un tiers du coût (contrer une dépêche : ×0,67) ;")
open(p,'w',encoding='utf-8').write(s)
