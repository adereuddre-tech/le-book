# Lot 160 : moyen, équipe ×1,10 ; capacité du fonds lisible — un investisseur qui voudrait souscrire mais que la capacité
# bloque affiche « fonds plein » (souscriptions nulles au-delà de 2 fois la capacité souple : 300 M$ en moyen). La
# souscription d'office de la Couronne suit désormais la même capacité.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("goalMult:1,costM:1,seed:0.00015}","goalMult:1,costM:1.10,seed:0.00015}")
rep("const f=invInF(D);if(f>0.002)r.sub=invFlow(v,f*v.w*extNav())});","const f=invInF(D);if(f>0.002)r.sub=invFlow(v,f*v.w*extNav());else if(capStress()>0.5)r.full=1});")
rep("const f=INVP.royAuto[0]+(INVP.royAuto[1]-INVP.royAuto[0])*S.lp/100;r.sub+=invFlow(v,f*v.w*extNav());r.auto=1}",
    "const f=(INVP.royAuto[0]+(INVP.royAuto[1]-INVP.royAuto[0])*S.lp/100)*Math.max(0,1-capStress());if(f>0.002){r.sub+=invFlow(v,f*v.w*extNav());r.auto=1}else r.full=1}")
rep("v.ntc>0?`<span class=\"neg-g\">avis ${mm(v.ntc*h)}</span>`:''].filter(Boolean).join(' · ')||'—';\n  return `<tr${never",
    "v.ntc>0?`<span class=\"neg-g\">avis ${mm(v.ntc*h)}</span>`:'',r.full&&!(r.sub>0)?'<span style=\"color:var(--gold)\">fonds plein</span>':''].filter(Boolean).join(' · ')||'—';\n  return `<tr${never")
rep("Au-delà de 15 % de l'encours en avis, vous pouvez activer la gate.</p></details>",
    "Au-delà de 15 % de l'encours en avis, vous pouvez activer la gate. Capacité : au-delà de ${mm(capSoftNav())}, les souscriptions diminuent, et s'arrêtent à ${mm(2*capSoftNav())} (« fonds plein ») : un fonds trop gros ne peut plus placer l'argent sans faire bouger les marchés.</p></details>")
open('index.html','w',encoding='utf-8').write(s);print('lot160 ok')
