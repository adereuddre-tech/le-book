import sys
P=sys.argv[1];s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:90]);s=s.replace(old,new)
# 1. financement du levier : coût convexe en risque, pour le fonds comme pour les concurrents
rep("function rivDrag(v){return 0.004*(v/0.2)*(v/0.2)}",
    "/* lot 80 : le prime broker finance le levier à un coût qui croît comme le carré du risque — même barème pour tous */\nconst FINK=0.006;\nfunction rivDrag(v){return FINK*(v/0.2)*(v/0.2)}\nfunction finDrag(k){const v=riskShown(weights(k||S.k)).total;return FINK*(v/0.2)*(v/0.2)}")
rep("const t=qElapsed(),w=weights(S.k);let g=0;for(let i=0;i<N;i++)g+=w[i]*S.rBase[i];if(!S.qColM)g+=colYield();return S.nav*(1+t*g)}",
    "const t=qElapsed(),w=weights(S.k);let g=-finDrag(S.k);for(let i=0;i<N;i++)g+=w[i]*S.rBase[i];if(!S.qColM)g+=colYield();return S.nav*(1+t*g)}")
rep(" let g=0;for(let i=0;i<N;i++)g+=w[i]*S.rBase[i];\n if(!S.qColM)g+=colYield();",
    " let g=-finDrag(S.k);for(let i=0;i<N;i++)g+=w[i]*S.rBase[i];\n if(!S.qColM)g+=colYield();")
rep(" let gross=0;for(let i=0;i<N;i++)gross+=w[i]*r[i];"," let gross=-finDrag(S.k);for(let i=0;i<N;i++)gross+=w[i]*r[i];")
rep(" const sg=riskShown(w).total;return m-0.5*sg*sg/4-tailExp(sg);"," const sg=riskShown(w).total;return m-0.5*sg*sg/4-tailExp(sg)-FINK*(sg/0.2)*(sg/0.2);")
# 2. accidents de levier dès 20 % de risque, pente plus raide
rep("const TAIL={x0:0.25,w:0.35,p:0.60},","const TAIL={x0:0.20,w:0.30,p:0.60},")
# 3. le comité note le risque ex ante à la clôture
rep("else if(S.marginCall)red='appel de marge';",
    "else if(S.marginCall)red='appel de marge';\n   else if(sp>=RISKCAP.r)red=`risque ex ante de ${dec(sp*100,0)} %`;")
rep("if(sp<0.02&&!(S.tails||[]).some(x=>x.q===S.q))why.push('book vide');",
    "if(sp<0.02&&!(S.tails||[]).some(x=>x.q===S.q))why.push('book vide');\n   if(sp>=RISKCAP.y&&sp<RISKCAP.r)why.push(`risque ex ante de ${dec(sp*100,0)} %`);")
rep("const MGC={","/* lot 80 : plafonds de risque du comité, jugés sur le book de clôture */\nconst RISKCAP={y:0.45,r:0.60};\nconst MGC={")
open(P,'w',encoding='utf-8').write(s);print('ok')
