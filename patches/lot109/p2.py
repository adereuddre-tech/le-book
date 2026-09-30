# Lot 109, p2 : boutons du tuyau en data-tip (data-t est l'attribut des accidents de levier, lu par le bot).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep('<button class="choice" data-t="1"><b>Prendre l\'affaire</b>','<button class="choice" data-tip="1"><b>Prendre l\'affaire</b>')
rep('<button class="choice" data-t="0"><b>Passer</b>','<button class="choice" data-tip="0"><b>Passer</b>')
rep("app.querySelectorAll('.choice[data-t]').forEach(b=>b.onclick=()=>go(+b.dataset.t));\n armTimer(()=>go(0),\"sans réponse : l'affaire part ailleurs\")}",
    "app.querySelectorAll('.choice[data-tip]').forEach(b=>b.onclick=()=>go(+b.dataset.tip));\n armTimer(()=>go(0),\"sans réponse : l'affaire part ailleurs\")}")
open('index.html','w',encoding='utf-8').write(s);print('lot109 p2 ok')
