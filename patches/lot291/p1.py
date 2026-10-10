p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# 1. prime du chasseur de queue : prix d'une protection à 100 % du choc, le surplus de 20 % est offert
rep("function hedgeCost(){return Math.max(HEDGE.min,hL()*hedgeEV())*(boH(9)?0.7:1)}",
    "function hedgeCost(){return Math.max(HEDGE.min,hL()*hedgeEV()*Math.min(1,hH())/hH())*(boH(9)?0.7:1)}   /* lot 291 : la part rendue au-delà du choc n'est pas facturée */")
rep("""<span class="an">Prime : ${cr>HEDGE.min+1e-9?`${dec(hL(),0)} × ce montant`:`plancher de ${dec(HEDGE.min*100,1)} %`}</span>""",
    """<span class="an">Prime : ${cr>HEDGE.min+1e-9?(hH()>1?`ce que rendrait une protection à 100 % du choc · le surplus de ${Math.round(hH()*100-100)} % est offert`:`${dec(hL(),0)} × ce montant`):`plancher de ${dec(HEDGE.min*100,1)} %`}</span>""")
rep("""Vous l'achetez à son juste prix : elle ne coûte que ce qu'elle rend en moyenne, et rend plus que le choc.""",
    """Vous la payez au prix d'une protection qui rendrait exactement le choc : les 20 % de plus sont offerts, elle rapporte en moyenne.""")
# 2. Solange : la protection rend sur le choc brut, l'exercice de crise réduit la perte — les deux s'additionnent
rep("""let hgB=0;if(ev.x&&S.hedgeQ===S.q&&imm<0){hgB=-imm*hH();imm+=hgB}   /* lot 253 : protection */
 if(ev.stress&&pwOn('so')&&imm<0)imm*=ev.stress==='cyber'?0:0.65;   /* lot 268 : Solange */""",
"""let hgB=0;if(ev.x&&S.hedgeQ===S.q&&imm<0)hgB=-imm*hH();   /* lot 253 : protection, sur le choc brut du marché */
 if(ev.stress&&pwOn('so')&&imm<0)imm*=ev.stress==='cyber'?0:0.65;   /* lot 268 : Solange ; lot 291 : avant la protection, qui rend quand même sur le choc brut */
 imm+=hgB;""")
rep("""d:"Ce trimestre, le choc immédiat d'un événement extrême est réduit de 35 %, et une cyberattaque ne vous touche pas."}""",
    """d:"Ce trimestre, le choc immédiat d'un événement extrême est réduit de 35 %, et une cyberattaque ne vous touche pas. S'ajoute à la protection, qui rend sur le choc du marché."}""")
open(p,'w',encoding='utf-8').write(s)
# 3. textes du style
s=open(p,encoding='utf-8').read()
rep("""pw:"la protection au juste prix, et qui rend 120 % du choc : vous gagnez quand tout s'effondre\"""",
    """pw:"la protection au prix du choc, et qui en rend 120 % : vous gagnez quand tout s'effondre\"""")
rep("""votre protection contre les extrêmes coûte son juste prix (1 × ce qu'elle rend en moyenne, au lieu de 2 ×) et rend 120 % du choc immédiat au lieu de 70 % : un extrême vous enrichit""",
    """votre protection contre les extrêmes rend 120 % du choc immédiat au lieu de 70 %, et vous ne la payez qu'au prix d'une protection à 100 % (sans la marge de 2 × des autres styles) : le surplus est offert, un extrême vous enrichit""")
rep("""tail:"la protection au juste prix, et qui rend plus que le choc\"""","""tail:"la protection au prix du choc, et qui rend plus que le choc\"""")
rep("""la protection contre les extrêmes vous est vendue à son juste prix (aujourd'hui""","""la protection contre les extrêmes vous est vendue au prix du choc moyen, sans marge (aujourd'hui""")
rep("""et rend 120 % du choc immédiat. ${xWatchTxt()}""","""et rend 120 % du choc immédiat : les 20 % de plus sont offerts. ${xWatchTxt()}""")
open(p,'w',encoding='utf-8').write(s)
