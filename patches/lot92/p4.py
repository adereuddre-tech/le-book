# Lot 92d : capture 380 px — le rôle passait sous « hors caisse » (texte non replié dans le bouton).
s=open('index.html',encoding='utf-8').read()
o=".tm .tnm{flex:1;display:flex;flex-direction:column;min-width:0}"
assert s.count(o)==1
s=s.replace(o,o+".tm .tnm b,.tm .tnm i{white-space:normal;overflow-wrap:anywhere}")
open('index.html','w',encoding='utf-8').write(s);print('ok')
