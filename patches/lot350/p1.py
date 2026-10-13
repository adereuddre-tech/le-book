p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# locaux : afficher ce que le déménagement change vraiment au budget (loyer + fin de la remise du garage sur l'équipe) et ce qui manque
rep("""function drawOffs(){""","""function offDelta(i){const sv=S.office,c0=opsT();S.office=i;const c1=opsT();S.office=sv;return c1-c0}   /* lot 350 */
function drawOffs(){""")
rep("""Déménager ne coûte rien de plus que le nouveau loyer.</p>""","""Déménager ne coûte rien de plus que le nouveau loyer ; le chiffre « budget » compte aussi l'effet des locaux sur le coût de l'équipe (le garage la fait 5 % moins chère).</p>""")
rep("""<span>${mm(o.bp*1e-4*budNav())} par trimestre${ok?'':' · hors trésorerie'}</span>""","""<span>${mm(o.bp*1e-4*budNav())} par trimestre${i!==cur?(d=>` · budget ${d>=0?'+':'−'}${mm(Math.abs(d))}`)(offDelta(i)):''}${ok?'':` · hors trésorerie : il manque ${mm(Math.max(0,offDelta(i)-mgrCash()))}`}</span>""")
open(p,'w',encoding='utf-8').write(s)
