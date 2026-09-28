import sys
P=sys.argv[1];s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:80]);s=s.replace(old,new)
# cartons : la confiance nulle ne vaut un jaune qu'au moment où elle y tombe, pas à chaque clôture passée à zéro
rep("  else if(S.lp<=0)why.unshift('confiance des investisseurs à zéro');",
    "  else if(S.lp<=0&&!(S.lpClose<=0))why.unshift('confiance des investisseurs tombée à zéro');\n  S.lpClose=S.lp;")
# flux : l'intuition entre dans l'attendu affiché (rentabilité, nuage) comme une source très fiable
rep(" S.factEst=est.map(z=>z/Math.max(1,b.length)*2.2);\n}",
    " S.factEst=est.map(z=>z/Math.max(1,b.length)*2.2);\n if(S.hunch&&HUNCHW)S.factEst[S.hunch.k]+=(S.hunch.up?1:-1)*HUNCHW;   /* lot 77 */\n}\nvar HUNCHW=0.9;")
rep("lpMult:1.35,ddMax:0.22,","lpMult:1.20,ddMax:0.22,")
rep("confiance 35 % plus nerveuse","confiance 20 % plus nerveuse")
open(P,'w',encoding='utf-8').write(s);print('ok')
