# Lot 163 : page du book — l'objectif du trimestre (et l'objectif bonus) en haut de page ; « le book est reconduit » corrigé
# (le book repart à plat chaque trimestre) ; « dollar » → « liquidité » dans l'aide des sources.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep(" app.innerHTML=statusBar()+`<div class=\"fade\">\n  <div class=\"block\"><div class=\"blockhead\"><h2>Bruits de salle et rumeurs</h2>",
    " app.innerHTML=statusBar()+`<div class=\"fade\">\n  ${objRows()}\n  <div class=\"block\"><div class=\"blockhead\"><h2>Bruits de salle et rumeurs</h2>")
rep("  ${objRows()}\n  ${S.xHint?`<div class=\"flag xh\">","  ${S.xHint?`<div class=\"flag xh\">")
rep("<p class=\"note\" style=\"text-align:center\">Le book est reconduit tel quel au trimestre suivant tant que vous ne le modifiez pas — seuls les changements coûtent, et c'est vous qui les payez.</p>",
    "<p class=\"note\" style=\"text-align:center\">Le book repart à plat à chaque trimestre : chaque position se rachète, et c'est vous qui payez les ordres.</p>")
rep("<p class=\"note\" style=\"margin:0\">Le book est reconduit tel quel : vous ne payez rien. Le desk en profite pour vous parler d'autre chose.</p>",
    "<p class=\"note\" style=\"margin:0\">Aucune position ce trimestre : vous ne payez aucun ordre. Le desk en profite pour vous parler d'autre chose.</p>")
rep("effet sur les quatre facteurs — croissance, inflation, dollar, appétit pour le risque","effet sur les quatre facteurs — croissance, inflation, liquidité, appétit pour le risque")
open('index.html','w',encoding='utf-8').write(s);print('lot163 ok')
