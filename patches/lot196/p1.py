# Lot 196 : concurrent fermé. Il était remplacé à la clôture même (rivReplace) : le tableau du résultat montrait déjà le
# remplaçant, sans trace du fonds tombé. Désormais il reste affiché au résultat (et au rapport final), classé dernier,
# performance en rouge avec « clôturé » ; il est exclu des rangs. Le remplaçant entre au début du trimestre suivant
# (planQuarter, avant le tirage de l'objectif), annoncé à l'ouverture.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
# clôture : marquer, ne plus remplacer
rep("S.qRivNew=[];S.rivals.forEach((rv,j)=>{if((rv.mgr||0)<-1e-9){const o={nm:rv.nm,boss:rv.boss},nv=rivReplace(j);S.qRivNew.push({o,nv})}});   /* lot 157 */",
    "S.qRivNew=[];S.rivals.forEach((rv,j)=>{if((rv.mgr||0)<-1e-9){rv.closed=S.q;S.qRivNew.push({o:{nm:rv.nm,boss:rv.boss}})}});   /* lot 157 ; lot 196 : remplacé au trimestre suivant */")
# planQuarter : remplacer les fermés
rep("function planQuarter(){\n reseed('mkt');",
    "function planQuarter(){\n S.qRivIn=[];(S.rivals||[]).forEach((rv,j)=>{if(rv.closed){const o={nm:rv.nm,boss:rv.boss},nv=rivReplace(j);delete nv.closed;S.qRivIn.push({o,nv:{nm:nv.nm,boss:nv.boss}})}});   /* lot 196 */\n reseed('mkt');")
# rangs : exclure les fermés
rep("S.rivals.filter(r=>r.cum>S.idx).length","S.rivals.filter(r=>!r.closed&&r.cum>S.idx).length",6)
rep("const rank=1+S.rivals.filter(x=>x.cum>tot).length;","const rank=1+S.rivals.filter(x=>!x.closed&&x.cum>tot).length;")
rep("const ahead=S.rivals.filter(r=>r.cum>me)","const ahead=S.rivals.filter(r=>!r.closed&&r.cum>me)")
rep("const behind=S.rivals.filter(r=>r.cum<=me)","const behind=S.rivals.filter(r=>!r.closed&&r.cum<=me)")
# tableau du résultat
rep("rk:r.vqLast||rivV(r),st:(RIVSTRAT[r.style]||{}).nm,th:r.tailHit,xr:(S.xRiv||[])[S.rivals.indexOf(r)]||0}))].sort((a,b)=>b.v-a.v);",
    "rk:r.vqLast||rivV(r),st:(RIVSTRAT[r.style]||{}).nm,th:r.tailHit,cl:!!r.closed,xr:(S.xRiv||[])[S.rivals.indexOf(r)]||0}))].sort((a,b)=>b.v-a.v);")
rep("${all.map(a=>({a,cv:a.cv})).sort((x,y)=>y.cv-x.cv).map(({a,cv})=>`<tr class=\"${a.me?'me':''}\"><td>${a.nm}",
    "${all.map(a=>({a,cv:a.cv})).sort((x,y)=>(x.a.cl?1:0)-(y.a.cl?1:0)||y.cv-x.cv).map(({a,cv})=>`<tr class=\"${a.me?'me':''}\"><td>${a.nm}${a.cl?'<br><b class=\"neg-g\" style=\"font-size:11px\">clôturé</b>':''}")
rep("<td class=\"${cls(a.v)}\">${sgn(a.v,1)}</td><td class=\"${cls(cv)}\">${sgn(cv,1)}</td></tr>`).join('')}",
    "<td class=\"${a.cl?'neg-g':cls(a.v)}\">${sgn(a.v,1)}</td><td class=\"${a.cl?'neg-g':cls(cv)}\">${sgn(cv,1)}${a.cl?' · clôturé':''}</td></tr>`).join('')}")
rep("const cums=[{nm:S.fundName,v:S.idx-1,me:1},...S.rivals.map(r=>({nm:r.nm,v:r.cum-1}))].sort((a,b)=>b.v-a.v);",
    "const cums=[{nm:S.fundName,v:S.idx-1,me:1},...S.rivals.map(r=>({nm:r.nm,v:r.cum-1,cl:!!r.closed}))].sort((a,b)=>(a.cl?1:0)-(b.cl?1:0)||b.v-a.v);")
rep("(S.qRivNew||[]).forEach(x=>warn.push(`🏚️ <b>${x.o.nm} ferme ses portes</b> : la société de gestion de ${x.o.boss} n'a plus de trésorerie. <b>${x.nv.nm}</b> prend sa place, lancé par ${x.nv.boss}, ancien bras droit de ${x.o.boss} ; il part de zéro et monte en charge.`));",
    "(S.qRivNew||[]).forEach(x=>warn.push(`🏚️ <b>${x.o.nm} ferme ses portes</b> : la société de gestion de ${x.o.boss} n'a plus de trésorerie. Un nouveau fonds du même style prendra sa place au prochain trimestre.`));")
# rapport final
rep("const lg=[{nm:S.fundName,v:S.idx-1,me:1},...S.rivals.map(x=>({nm:x.nm+'<span class=\"bossn\">'+x.boss+'</span>',v:x.cum-1}))].sort((a,b)=>b.v-a.v);",
    "const lg=[{nm:S.fundName,v:S.idx-1,me:1},...S.rivals.map(x=>({nm:x.nm+'<span class=\"bossn\">'+x.boss+'</span>'+(x.closed?' <b class=\"neg-g\" style=\"font-size:11px\">clôturé</b>':''),v:x.cum-1,cl:!!x.closed}))].sort((a,b)=>(a.cl?1:0)-(b.cl?1:0)||b.v-a.v);")
open('index.html','w',encoding='utf-8').write(s);print('lot196 ok')
s=open("index.html",encoding="utf-8").read()
rep("...(S.goal?[`🏅 <b>Objectif bonus : ${S.goal.nm}</b>",
    "...(S.qRivIn||[]).map(x=>`🏢 <b>${x.nv.nm}</b> prend la place de ${x.o.nm}, lancé par ${x.nv.boss}, ancien bras droit de ${x.o.boss} ; il part de zéro et monte en charge.`),...(S.goal?[`🏅 <b>Objectif bonus : ${S.goal.nm}</b>")
open('index.html','w',encoding='utf-8').write(s);print('lot196b ok')
