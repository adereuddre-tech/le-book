# Lot 101c : calibrage — à 1,6 le choc immédiat allait de 6 à 53 % de l'encours (tous les marchés touchés à la fois).
s=open('index.html',encoding='utf-8').read()
for a,b in [("const STRESSK=1.6;","const STRESSK=0.25;"),("if(Math.abs(v)>=0.15)h[x.sym]=+v.toFixed(2)","if(Math.abs(v)>=0.03)h[x.sym]=+v.toFixed(3)")]:
    assert s.count(a)==1,a; s=s.replace(a,b)
open('index.html','w',encoding='utf-8').write(s);print('ok')
