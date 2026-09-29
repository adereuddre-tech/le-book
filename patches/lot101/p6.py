# Lot 101f : encore +13,9 ± 4,3 M$ face au lot 99 (vol du bot 25 % contre 20 %) : chocs ×0,4 au lieu de 0,25,
# amplification 1 + 2,5·max(0, sp − 0,20)/0,10.
s=open('index.html',encoding='utf-8').read()
for a,b in [("const STRESSK=0.25;","const STRESSK=0.4;"),("function crowd(sp){return 1+1.5*Math.max(0,sp-0.20)/0.10}","function crowd(sp){return 1+2.5*Math.max(0,sp-0.20)/0.10}")]:
    assert s.count(a)==1,a; s=s.replace(a,b)
open('index.html','w',encoding='utf-8').write(s);print('ok')
