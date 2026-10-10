p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# co-investissement : la part choisie sort de la trésorerie affichée dès l'écran, et suit chaque choix
rep("""function coPend(){return 0;   /* lot 240 */""",
    """function coPend(){if(S&&S.coinvScr===S.q&&S.coinvQ!==S.q)return coinvPct()*Math.max(0,mgrCash());return 0;   /* lot 240 ; lot 293 : en temps réel sur l'écran du co-investissement */""")
rep(""" const cash=Math.max(0,mgrCash()),pb=profitBook(S.k),sg=riskShown(weights(S.k)).total;""",
    """ const cash=Math.max(0,mgrCash()),pb=profitBook(S.k),sg=riskShown(weights(S.k)).total;S.coinvScr=cAsk?S.q:-1;""")
open(p,'w',encoding='utf-8').write(s)
