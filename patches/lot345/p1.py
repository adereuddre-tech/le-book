p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# rentabilité : le collatéral se lit sur le book envisagé (marge de k, pas du book courant) et à la probabilité de défaut du desk
rep("""function colExp(){const o=colOpt(),m=mgShare();return redOn('collat')?S.rate/4*0.6:m*Math.max(0,S.rate-0.001)/4+(1-m)*(S.rate/4+colY(o)-o.p*o.l)}""",
    """function colPD(o){if(!o.p)return 0;const Pd=typeof xDeskP==='function'&&S&&S.bud?xDeskP():null;if(Pd==null)return o.p;return Pd*Math.min(0.95,COLK*o.p)+(1-Pd)*colPx(o,false)}   /* lot 345 */
function colExp(k){const o=colOpt(),m=k?Math.min(1,marginPct(k)):mgShare();return redOn('collat')?S.rate/4*0.6:m*Math.max(0,S.rate-0.001)/4+(1-m)*(S.rate/4+colY(o)-colPD(o)*o.l)}""")
rep(""" k=k||S.k;const w=weights(k),k0=S.k0||S.k;let m=colExp();""",""" k=k||S.k;const w=weights(k),k0=S.k0||S.k;let m=colExp(k);   /* lot 345 : coût d'opportunité du collatéral selon la marge de ce book */""")
open(p,'w',encoding='utf-8').write(s)
