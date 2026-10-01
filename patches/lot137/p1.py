# Lot 137 : rubans des concurrents — l'événement extrême (et le tuyau pris par un concurrent) apparaît au moment où il frappe,
# pas seulement à la clôture ; micro-anecdotes dans les rôles de Tuco, Winnie, Sœur Marie-Alpha et Onésime ; budget total
# dans le bouton de validation ; coût des ordres en blanc gras sur l'écran du desk.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function xRivHit(id){const sc=STRESS.find(x=>x.id===id);if(!sc)return;\n","function xRivHit(id){const sc=STRESS.find(x=>x.id===id);if(!sc)return;if(S.xRivT==null||S.xRivQ!==S.q){S.xRivT=typeof qElapsed==='function'?qElapsed():0;S.xRivQ=S.q}\n")
rep("  ts.forEach((t,k)=>{const nv=v*(1+rivRet(j,t,tq))*100;","  ts.forEach((t,k)=>{const xr=(S.xRiv&&S.xRivQ===tq&&t>=(S.xRivT||0))?(S.xRiv[j]||0):0,nv=v*(1+rivRet(j,t,tq)+xr)*100;")
rep("S.rumors=[];S.xRiv=null;","S.rumors=[];S.xRiv=null;S.xRivT=null;S.xRivQ=null;")
rep("role:\"trader matières premières\"","role:\"trader matières premières, un cigare par cargaison\"")
rep("role:\"trader exotiques\"","role:\"trader exotiques, vit à l'heure de Hong Kong\"")
rep("role:\"stratégiste quantitative, recherche\"","role:\"stratégiste quantitative, prie pour la normalité des rendements\"")
rep("role:\"économiste en chef : un coup de pouce par trimestre\"","role:\"économiste en chef, une prévision par plateau télé : un coup de pouce par trimestre\"")
rep(" });\n}\n\n/* ---------- positionnement ---------- */",
    " });\n {const ok=document.getElementById('ok');if(ok){const t=budgetBp()*1e-4*budNav();ok.innerHTML=`Valider le budget · <b>${mm(t)}</b> ce trimestre — passer au book`}}   /* lot 137 */\n}\n\n/* ---------- positionnement ---------- */")
rep("<div class=\"kv\"><span>Ordres, à votre charge</span><b class=\"neg-g\">${mm(tot)}</b></div>","<div class=\"kv\"><span><b style=\"color:#fff\">Ordres, à votre charge</b></span><b style=\"color:#fff;font-size:17px\">−${mm(tot)}</b></div>")
open('index.html','w',encoding='utf-8').write(s);print('lot137 p1 ok')
