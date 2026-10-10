p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("""function visP(k){return 1-visList(k).reduce((a,v)=>a*(1-v.p),1)}""",
    """function visP(k){const L=visList(k);return Math.min(0.6,Math.sqrt(L.reduce((a,v)=>a+v.p*v.p,0)))}   /* lot 277 : en racine — quatre lignes visibles pèsent deux fois une seule */""")
rep(""" {const V=visList(S.k),u=prng32(hash32('vis'+S.q,S.seed));for(const v of V){if(u()<v.p){const w=weights(S.k),i=v.i,H=v.kind==='short'?VIS.Hs:VIS.Hl,""",
    """ {const V=visList(S.k),u=prng32(hash32('vis'+S.q,S.seed)),PT=visP(S.k);if(V.length&&u()<PT){let r=u()*V.reduce((a,v)=>a+v.p,0),v=V[0];for(const x of V){if(r<x.p){v=x;break}r-=x.p}{const w=weights(S.k),i=v.i,H=v.kind==='short'?VIS.Hs:VIS.Hl,""")
open(p,'w',encoding='utf-8').write(s)
