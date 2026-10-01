# Lot 122, p2 : en-têtes d'anecdotes — quand un trader ou quelqu'un du back office est cité, son icône à côté du portrait,
# et un portrait du bon genre.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function evHead(who,kind){return `<div class=\"evhead\">${avatar(who,kind)}",
    "const PGEN={'Ingrid':'f','Josiane':'f','Mireille':'f','Pare-Feu':'f','Solange':'f','Marie-Alpha':'f','Jean-Kevin':'m','Dwight':'m','Boris':'m','Tuco':'m','Winnie':'m','Gontran':'m','Report-à-Nouveau':'m','Tatillon':'m'};\n"
    "function personOf(who){const L=[...FOP,...BOP].filter(p=>p.ic&&p.who!=='Le loyer');for(const p of L){const keys=[p.full,p.who,...p.full.split(/[ «»]+/).filter(w=>w.length>3&&/^[A-ZÀ-Ý]/.test(w))];if(keys.some(k=>k&&who.includes(k)))return p}return null}\n"
    "function personGen(who){for(const k in PGEN)if(who.includes(k))return PGEN[k];return null}\n"
    "function evHead(who,kind){const P=personOf(who||'');return `<div class=\"evhead\">${avatar(who,kind,personGen(who||''))}${P?`<span class=\"pic\">${P.ic}</span>`:''}")
rep("function avatar(name,kind){","function avatar(name,kind,gen){")
rep(" const fem=Math.floor(h/117649)%2===0&&hs>=5;"," let fem=Math.floor(h/117649)%2===0&&hs>=5;\n if(gen==='f'){fem=true}else if(gen==='m'){fem=false}")
rep(".cardw.r{background:#3d1010;border-color:#E5483C}",".cardw.r{background:#3d1010;border-color:#E5483C}\n.evhead .pic{font-size:26px;margin:0 6px 0 -4px;align-self:center}")
open('index.html','w',encoding='utf-8').write(s);print('lot122 p2 ok')
s=open('index.html',encoding='utf-8').read()
rep(" const hs=Math.floor(h/49)%9, fb=Math.floor(h/343)%6, gl=Math.floor(h/2401)%4, ac=Math.floor(h/16807)%6;"," let hs=Math.floor(h/49)%9, fb=Math.floor(h/343)%6;const gl=Math.floor(h/2401)%4, ac=Math.floor(h/16807)%6;")
rep(" if(gen==='f'){fem=true}else if(gen==='m'){fem=false}"," if(gen==='f'){fem=true;if(hs<5)hs=5+h%4;fb=0}else if(gen==='m'){fem=false;if(hs>=5)hs=h%5}")
open('index.html','w',encoding='utf-8').write(s);print('lot122 p2b ok')
