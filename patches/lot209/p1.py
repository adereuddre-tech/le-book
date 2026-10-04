# Lot 209 (lot C) : accidents de levier et appels de marge à 5 crans + couverture (voir new_tail.js).
# Corrige aussi l'affichage : « tenir » montrait −0,3 L / −1,5 L et confiance −1 / −8, « couper » confiance −3,
# « couvrir » confiance −2, alors que le jeu appliquait −0,5 L / −1,8 L, −2 / −10, −4 et −3.
import os
s=open("index.html",encoding="utf-8").read()
i=s.index('function tailOpts');j=s.index('/* lot 100 : appel de marge',i)
new=open(os.path.join(os.path.dirname(__file__),'new_tail.js'),encoding='utf-8').read()
s=s[:i]+new+s[j:]
open('index.html','w',encoding='utf-8').write(s);print('lot209 ok')
