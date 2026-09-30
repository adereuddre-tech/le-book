# Lot 114 : difficile à 30 % de commission de performance ; coûts d'exécution du quant ×0,72.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
i=s.index("{id:'mega',lvl:'Expert'");j=s.index("rivSkill",i)
seg=s[i:j];assert seg.count("perf:0.25")==1 and seg.count("25 %")>=2,seg.count("25 %")
s=s[:i]+seg.replace("perf:0.25","perf:0.30").replace("25 %","30 %")+s[j:]
rep("sigBonus:0,capture:0.50,tcMult:0.80,","sigBonus:0,capture:0.50,tcMult:0.72,")
rep("coûts de transaction −20 % : le modèle","coûts de transaction −28 % : le modèle")
open('index.html','w',encoding='utf-8').write(s);print('lot114 p1 ok')
