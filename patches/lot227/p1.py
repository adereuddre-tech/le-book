# Lot 227 : tableau des investisseurs — leurs règles (qui rachète, qui souscrit, quand) passent dans le détail repliable
# « Montants, préavis et confiance », juste en dessous, au lieu d'occuper l'écran. La règle de la Couronne ne commence
# plus par « la holding de la famille royale » (texte de l'ancien filtre, désormais « régnante »).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep(""" <p class="note" style="margin-top:6px">${INVR.map(D=>`${D.ic} <b>${D.nm.split(' (')[0]}</b> ${D.rule.replace(/^la holding de la famille royale /,'')}`).join('<br>')}</p>
 <details style="margin-top:4px"><summary class="note">Montants, préavis et confiance</summary><p class="note">""",
""" <details style="margin-top:6px"><summary class="note">Montants, préavis et confiance</summary>
 <p class="note">${INVR.map(D=>`${D.ic} <b>${D.nm.split(' (')[0]}</b> ${D.rule.replace(/^la holding de la famille (royale|régnante) /,'')}`).join('<br>')}</p><p class="note">""")
open('index.html','w',encoding='utf-8').write(s);print('lot227 ok')
