p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# affichage : niveau facile (petit fonds), tous styles ; plus en moyen ni difficile
rep("${PROF().numeric?`<div class=\"wire\" style=\"margin:10px 0 8px\"><div class=\"kv\" style=\"padding-bottom:6px\"><span><b>Le book que le modèle construirait</b></span>",
    "${S.size==='small'?`<div class=\"wire\" style=\"margin:10px 0 8px\"><div class=\"kv\" style=\"padding-bottom:6px\"><span><b>Le book que ${PROF().numeric?'le modèle':'le desk'} construirait</b></span>")
rep("if(fe&&PROF().id==='syst'){   /* le book du modèle est le pouvoir propre du quant */",
    "if(fe&&S.size==='small'){   /* lot 251 : le book du desk, offert à tous les styles en niveau facile, retiré en moyen et difficile */")
rep("et vous propose un book d'un bouton.","et, en niveau facile, vous propose un book d'un bouton.")
rep("<b>Pouvoir propre — le book du modèle</b> : un portefeuille optimisé sur toutes les sources et tous les signaux, appliqué d'un bouton ; le modèle de risque annonce parfois l'événement extrême et chiffre sa perte",
    "<b>Pouvoir propre — le modèle de risque</b> : il annonce parfois l'événement extrême et chiffre sa perte ; en niveau facile, le book du modèle, optimisé sur toutes les sources et tous les signaux, s'applique d'un bouton (comme pour tous les styles)")
rep('syst:"book du modèle, en un bouton ; signaux lus plus nettement"','syst:"modèle de risque : l\'événement extrême annoncé et chiffré ; signaux lus plus nettement"')
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep('ef:[["g","capital de départ : 1 M$, plus celui de votre style"],["g","équipe 15 % moins chère"],',
    'ef:[["g","capital de départ : 1 M$, plus celui de votre style"],["g","le book que votre desk construirait, proposé chaque trimestre et applicable d\'un bouton, quel que soit votre style"],["g","équipe 15 % moins chère"],')
open(p,'w',encoding='utf-8').write(s)
