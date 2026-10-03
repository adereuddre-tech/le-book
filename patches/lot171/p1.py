# Lot 171 : tableau des concurrents — votre fonds a toujours ses deux lignes : événements extrêmes et accidents de levier du
# trimestre (« aucun » sinon le total).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("${(a.mt||[]).map(x=>`<br><span class=\"${cls(-x.f)}\" style=\"font-size:11px\">${x.id==='stress'?'événement extrême':'accident de levier'} ${sgnp(-x.f,1)}</span>`).join('')}",
    "${a.me?[['stress','événements extrêmes'],['lev','accidents de levier']].map(([id,l])=>{const v=(a.mt||[]).filter(x=>id==='stress'?x.id==='stress':x.id!=='stress').reduce((s,x)=>s-x.f,0);return `<br><span class=\"${Math.abs(v)<5e-5?'dim-g':cls(v)}\" style=\"font-size:11px\">${l} : ${Math.abs(v)<5e-5?'aucun':sgnp(v,1)}</span>`}).join(''):''}")
open('index.html','w',encoding='utf-8').write(s);print('lot171 ok')
