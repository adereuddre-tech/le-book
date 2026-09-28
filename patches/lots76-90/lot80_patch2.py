import sys
P=sys.argv[1];s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:90]);s=s.replace(old,new)
rep("const RISKCAP={y:0.45,r:0.60};","""const RISKCAP={y:0.35,r:0.50};
/* lot 80 : les investisseurs lisent le risque ex ante à chaque clôture — confiance −k par tranche de 5 pts
   au-delà de x0, et retraits au-delà de fl (fraction de l'encours par point de risque), vous comme les concurrents */
const RISKLP={x0:0.20,k:1.5,fl:0.25,fk:0.08};""")
rep("if(S.marginCall)lpD.push(['Liquidation forcée sur appel de marge',-7]);",
    "if(S.marginCall)lpD.push(['Liquidation forcée sur appel de marge',-7]);\n if(sp>RISKLP.x0+0.005)lpD.push([`Risque ex ante de ${dec(sp*100,0)} % : jugé trop élevé`,-Math.round(RISKLP.k*(sp-RISKLP.x0)/0.05)]);")
rep("if(S.lp<40)tot-=0.04*(40-S.lp)/40*SIZE().flowMult;",
    "if(S.lp<40)tot-=0.04*(40-S.lp)/40*SIZE().flowMult;\n const riskOut=RISKLP.fk*Math.max(0,sp-RISKLP.fl)*SIZE().flowMult;tot-=riskOut;")
rep("S.poachMsg=`${tot>=0?'Collecte':'Rachats'} : ${tot>=0?'+':'−'}${dec(Math.abs(tot)*100,1)} % d'encours (${mm(Math.abs(amt))}).${lines.length?' Clients par concurrent — '+lines.join(' · ')+'.':''}`;",
    "S.poachMsg=`${tot>=0?'Collecte':'Rachats'} : ${tot>=0?'+':'−'}${dec(Math.abs(tot)*100,1)} % d'encours (${mm(Math.abs(amt))}).${lines.length?' Clients par concurrent — '+lines.join(' · ')+'.':''}${riskOut>=0.001?` Dont −${dec(riskOut*100,1)} % retirés pour un risque jugé trop élevé.`:''}`;")
rep(" rv.mAum*=(1+r);"," rv.mAum*=(1+r);\n {const o=1-RISKLP.fk*Math.max(0,rivV(rv)-RISKLP.fl)*((SIZE()&&SIZE().flowMult)||1);rv.mAum*=o;rv.mHwm*=o}   /* lot 80 : leurs clients aussi */")
open(P,'w',encoding='utf-8').write(s);print('ok')
