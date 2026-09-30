# Lot 118 : classer les styles par leurs pouvoirs. Flux : intuition juste 80 % du temps (75 % au lot 116, 85 % avant).
# Quant : son modèle lit tendance, portage et valeur avec un bruit ×0,6 (les autres styles : ×0,3 sur leur signal, ×1,3 ailleurs).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("S.hunch={k,up:(rng()<0.75)===(S.f[k]>0)};","S.hunch={k,up:(rng()<0.80)===(S.f[k]>0)};")
rep("const mine=STYLESIG[S.prof],ne=kk=>e*(kk===mine?0.3:1.3);","const mine=STYLESIG[S.prof],ne=kk=>e*(S.prof==='syst'?0.6:(kk===mine?0.3:1.3));")
rep("return e*((typeof STYLESIG!=='undefined'&&STYLESIG[S.prof]===key)?0.3:(typeof STYLESIG!=='undefined'?1.3:1))}","return e*(S.prof==='syst'?0.6:(typeof STYLESIG!=='undefined'&&STYLESIG[S.prof]===key)?0.3:(typeof STYLESIG!=='undefined'?1.3:1))}")
open('index.html','w',encoding='utf-8').write(s);print('lot118 p1 ok')
