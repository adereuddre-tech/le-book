# Lot 174 : quant, capital de départ 1 M$ (0,4 M$) — pour qu'il survive le plus, devant le fondamental et le flux.
# Mesure (90 parties de quant, graines 10001–10030) : 0,4 M$ → 74 % ; 0,7 M$ → 76 % ; 1,0 M$ → 83 % (facile 90, moyen 83,
# difficile 77). Ensemble : 77 % · 45,6 M$ ; quant 83, fondamental 77, flux 71 ; facile 88, moyen 77, difficile 67.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const STYSEED={syst:0.0004,fonda:0,flux:0};","const STYSEED={syst:0.0010,fonda:0,flux:0};")
rep("capital de départ +0,40 M$","capital de départ +1 M$")
open('index.html','w',encoding='utf-8').write(s);print('lot174 ok')
