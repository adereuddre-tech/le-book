# Lot 111 : amplification de foule plafonnée à ×2,5 (événements extrêmes, pertes affichées au book). Sonde 24 parties :
# pertes immédiates jusqu'à 44 % du fonds (×4,75 d'amplification pour un book à 35 % de risque total).
# Campagne appariée (60 normal, 45 difficile) : score +4,1 ± 1,9 M$ en normal, −0,1 ± 0,7 en difficile ; survie inchangée
# (87 % / 73 %). Resserrer les déclencheurs des investisseurs (−2 %, ±2 pts, 2 trimestres négatifs sur 3) ne change
# rien non plus : les fins sont des faillites de la société de gestion, pas des fonds vidés.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function crowd(sp){return 1+2.5*Math.max(0,sp-0.20)/0.10}","function crowd(sp){return Math.min(2.5,1+2.5*Math.max(0,sp-0.20)/0.10)}")
open('index.html','w',encoding='utf-8').write(s);print('lot111 p1 ok')
