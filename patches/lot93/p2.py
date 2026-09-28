# Lot 93b : libellés imbriqués (ch[].e.riskMsg, safeTxt) ; anecdotes de Sœur Marie-Alpha retirées en son absence
# (texte au féminin, « l'ancienne religieuse ») ; suffixe de rôle gardé pour le back office seulement.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function persoOk(e){const p=PERSO[e.t];return p===undefined||here(p)}","function persoOk(e){if(/Marie-Alpha/.test(e.who||'')&&!here(6))return false;const p=PERSO[e.t];return p===undefined||here(p)}\nfunction deepCast(x,c){if(typeof x==='string')return recast(x,c);if(Array.isArray(x))return x.map(y=>deepCast(y,c));if(x&&typeof x==='object'){const q={};for(const k in x)q[k]=deepCast(x[k],c);return q}return x}")
rep("if(Array.isArray(o.ch))o.ch=o.ch.map(ch=>{const q=Object.assign({},ch);for(const k in q)q[k]=recast(q[k],c);return q})});","if(Array.isArray(o.ch))o.ch=deepCast(o.ch,c)});")
rep("o.who=c.rx.test(pa[0])?(n=>n[0].toUpperCase()+n.slice(1))(c.sub())+(pa[1]?' · '+pa[1]:''):pa[0]}","o.who=c.rx.test(pa[0])?(n=>n[0].toUpperCase()+n.slice(1))(c.sub())+(pa[1]&&c.bo?' · '+pa[1]:''):pa[0]}")
rep("{re:'Mireille Cauchemar|Mireille',on:","{re:'Mireille Cauchemar|Mireille',bo:1,on:")
open('index.html','w',encoding='utf-8').write(s);print('ok')
