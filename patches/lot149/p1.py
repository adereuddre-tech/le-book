# Lot 149 : « L'inspecteur » et « La commandante » retirés (Firmin Tatillon, Solange Pare-Feu) ; prêts à effet de levier :
# 20 % de risque de perdre 21 % (au lieu de 30 % / 14 %).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
for a,b in [("L'inspecteur Firmin Tatillon","Firmin Tatillon"),("L'inspecteur Tatillon","Firmin Tatillon"),("La commandante Solange Pare-Feu","Solange Pare-Feu"),("La commandante Pare-Feu","Solange Pare-Feu")]:
    n=s.count(a);assert n>=1,a;s=s.replace(a,b)
assert "inspecteur Tatillon" not in s and "commandante Pare-Feu" not in s
rep("{id:'lev',nm:'Prêts à effet de levier',ico:'🏗️',y:0.055,p:0.30,l:0.14,","{id:'lev',nm:'Prêts à effet de levier',ico:'🏗️',y:0.055,p:0.20,l:0.21,")
open('index.html','w',encoding='utf-8').write(s);print('lot149 ok')
