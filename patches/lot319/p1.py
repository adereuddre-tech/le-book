p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# Jean-Kevin tracé à l'exécution : sa part dans la facture des ordres
rep("""   <div class="kv"><span>Impact de marché, pour le fonds</span>${mn(execImpactAmt(tot,1,S.leakQ))}</div>`""",
    """   <div class="kv"><span>Impact de marché, pour le fonds</span>${mn(execImpactAmt(tot,1,S.leakQ))}</div>${pwOn('jk')&&S.pwJK?`<div class="kv"><span>🐣 Tableur de Jean-Kevin : ${S.pwJK<1?'il marche':'il plante'} (${S.pwJK<1?'−':'+'}20 %), compris dans la facture</span>${mn(tot/S.pwJK-tot)}</div>`:''}`""")
open(p,'w',encoding='utf-8').write(s)
