# Lot 101h : un scénario ciblé sans cible (pas de vente à découvert, book vide) est sauté.
s=open('index.html',encoding='utf-8').read()
a=" if(ev&&ev.stress){const e2=stressEv(ev.stress);if(e2)ev=e2}   /* lot 101 : choc calculé sur le book du moment */"
assert s.count(a)==1
s=s.replace(a," if(ev&&ev.stress){const e2=stressEv(ev.stress);if(e2)ev=e2;if(!Object.keys(ev.hit).length){stepEvents();return}}   /* lot 101 : choc calculé sur le book du moment */")
open('index.html','w',encoding='utf-8').write(s)
