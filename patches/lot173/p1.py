# Lot 173 : budget du back office — avec un carton rouge, le comité interdit de descendre sous Tatillon ; les crans du bas
# s'affichaient « hors trésorerie ». Le libellé dit désormais la vraie raison, et le paragraphe d'en-tête l'explique.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("${o?mm(l.bp*1e-4*budNav()):'<span class=\"hx\">hors trésorerie</span>'}","${o?mm(l.bp*1e-4*budNav()):(b.id==='bo'&&redOn('budget')&&i<3?'<span class=\"hx\">interdit : carton rouge</span>':'<span class=\"hx\">hors trésorerie</span>')}")
rep("un demi-trimestre de salaire.</b>`:''}","un demi-trimestre de salaire.</b>`:''}${b.id==='bo'&&redOn('budget')?` <b class=\"neg-g\">Carton rouge : le comité vous interdit de descendre le back office sous ${BOP[3].who}.</b>`:''}")
open('index.html','w',encoding='utf-8').write(s);print('lot173 ok')
