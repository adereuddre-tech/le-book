import sys
P=sys.argv[1];s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:100]);s=s.replace(old,new)
rep("const sg=riskShown(w).total;return m-0.5*sg*sg/4-tailExp(sg)-FINK*(sg/0.2)*(sg/0.2);",
    "const sg=riskShown(w).total;return m-FINK*(sg/0.2)*(sg/0.2);   /* lot 85 : lecture des marchés, moins le financement facturé ; ni accidents ni drain */")
rep("function rivPt(rv,vv){","/* lot 85 : full = avec drain et coût moyen des accidents (pour leurs décisions) ; sans = même lecture que la vôtre */\nfunction rivPt(rv,vv,full){")
rep("+(rv.bRet||0)-0.5*v*v/4-tailExp(v,1),l:","+(rv.bRet||0)-(full?0.5*v*v/4+tailExp(v,1):0),l:")
rep("const y=rivPt(rv,t).y;if(y>by){by=y;bv=t}","const y=rivPt(rv,t,1).y;if(y>by){by=y;bv=t}")
rep("drain de volatilité et coût moyen des accidents de levier compris","financement du levier compris ; ni le drain de volatilité ni les accidents de levier, qui dépendent du risque et se lisent sur l'axe horizontal")
rep("lpNeg:1.60,rcNeg:1.35,lp0:-8,flowMult:1.15,","lpNeg:1.40,rcNeg:1.35,lp0:-8,flowMult:1.15,")
open(P,'w',encoding='utf-8').write(s);print('ok')
