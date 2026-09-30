# Lot 115 : demandes d'Antoine + équilibrage.
#  · book : le trader de chaque classe à côté du nom de la classe ;
#  · budget : descendre un cran ne parle de licenciement (bonus de départ) que pour qui était déjà là au trimestre précédent ;
#  · investisseurs : caisse de retraite sur 2 trimestres d'affilée (positifs → souscrit, négatifs → rachète) ; fonds souverain
#    chaque trimestre sur l'objectif annoncé (toujours présent : annonce standard par défaut) ;
#  · bonus : plus de motivation cachée ; effet direct et lisible par cran (part de la baisse des coûts que le desk livre,
#    débauchage), ×1,5 au débauchage le trimestre d'une baisse ; sans commission de performance, rien n'est versé et le desk
#    se comporte comme au cran minimal ;
#  · négociation de limite : sélecteurs stylés (le choix « Ne pas négocier » était invisible), clairement facultative ;
#  · équilibrage (60 parties par case, lot 114 : flux 77 %, quant 68 %, fondamental 67 %, difficile 66 %) : flux coûts ×1,00
#    (×0,90), quant investisseurs ×0,75 (×0,90), difficile équipe ×1,35 (×1,20).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
# book
rep("<span>${g.toUpperCase()}</span>${(g!=='Exotiques'||S.exoOpen)&&!covered(g)?",
    "<span>${g.toUpperCase()}</span>${TRD[g]!==undefined&&(g!=='Exotiques'||S.exoOpen)&&covered(g)?`<span class=\"trd\">${FOP[TRD[g]].ic} ${FOP[TRD[g]].who}</span>`:''}${(g!=='Exotiques'||S.exoOpen)&&!covered(g)?")
rep(".cisel{display:flex;gap:6px;margin-top:6px}",".cisel{display:flex;gap:6px;margin-top:6px}\n.sect .trd{margin-left:8px;font-size:12px;color:var(--gold);font-weight:600;letter-spacing:0}\n.cisel .lmp,.cisel .gtp{flex:1;padding:8px 4px;border-radius:6px;background:var(--panel2);border:1px solid var(--line2);color:var(--txt);font-size:12.5px}\n.cisel .lmp.on,.cisel .gtp.on{border:2px solid var(--gold);color:var(--gold);background:rgba(214,178,94,.12)}")
# budget : licenciement seulement pour qui était là
rep("<b class=\"neg-g\">Descendre, c'est licencier : chaque partant touche son bonus de départ, un trimestre de salaire.</b></p>",
    "${S.budPrev&&S.budPrev[b.id]>0?`<b class=\"neg-g\">Descendre sous le cran du trimestre dernier, c'est licencier : chaque partant touche son bonus de départ, un trimestre de salaire.</b>`:''}</p>")
rep("toast(`${i1>i0?'Recrutement':'Départ'} : <b>${who.map(l=>l.who).join(', ')}</b>${i1>i0&&who.length===1&&who[0].hi?` — « ${who[0].hi} »`:''}${i1<i0&&S.qSevM>0?` · versement du bonus ${mm(S.qSevM)}`:''} · ${bb.nm} ${b0.toFixed(0)} → <b>${b1.toFixed(0)} pb</b> (${(b1-b0)>=0?'+':'−'}${mm(Math.abs((b1-b0)*1e-4*S.nav))})`);",
    "const fired=i1<i0&&S.budPrev&&i1<S.budPrev[id];\n  toast(`${i1>i0?'Recrutement':fired?'Départ':'Sélection retirée'} : <b>${who.map(l=>l.who).join(', ')}</b>${i1>i0&&who.length===1&&who[0].hi?` — « ${who[0].hi} »`:''}${fired&&S.qSevM>0?` · versement du bonus de départ ${mm(S.qSevM)}`:''} · ${bb.nm} ${b0.toFixed(0)} → <b>${b1.toFixed(0)} pb</b> (${(b1-b0)>=0?'+':'−'}${mm(Math.abs((b1-b0)*1e-4*budNav()))})`);")
# investisseurs
rep("rule:\"rachète si 3 des 4 derniers trimestres sont négatifs ; souscrit après 4 trimestres positifs d'affilée. Clause de repli : au-delà du repli maximal de votre style, la moitié de sa part.\"",
    "rule:\"souscrit après 2 trimestres positifs d'affilée, rachète après 2 trimestres négatifs d'affilée. Clause de repli : au-delà du repli maximal de votre style, la moitié de sa part.\"")
rep("rule:\"rachète si l'objectif annoncé est manqué deux trimestres de suite ; souscrit s'il est tenu deux fois de suite (sans annonce : l'objectif du mandat).\"",
    "rule:\"chaque trimestre : souscrit si l'objectif annoncé est tenu, rachète s'il est manqué.\"")
rep(" if(id==='fs'){if(n<2)return 0;const a=H[n-2];return !a.ok&&!L.ok?-1:a.ok&&L.ok?1:0}\n const T=H.slice(-4);if(T.length<2)return 0;const neg=T.filter(x=>x.r<0).length;\n return (T.length===4?neg>=3:neg===T.length)?-1:(T.length===4&&neg===0)?1:0}",
    " if(id==='fs')return L.ok?1:-1;\n if(n<2)return 0;const a=H[n-2];return a.r<0&&L.r<0?-1:a.r>0&&L.r>0?1:0}")
rep("const tg=S.comm&&S.comm.ret!=null?S.comm.ret:VOL().goal/4;","const tg=S.comm&&S.comm.ret!=null?S.comm.ret:VOL().goal/4;   /* l'annonce standard (objectif entier) est choisie par défaut */")
rep("Le fonds souverain juge sur cet objectif, la caisse de retraite sur la régularité, le family office sur le signe, le fonds de fonds sur la moyenne des concurrents.",
    "Le fonds souverain juge sur cet objectif chaque trimestre, la caisse de retraite sur deux trimestres d'affilée, le family office sur la performance absolue, le fonds de fonds sur la moyenne des concurrents.")
rep("(mandat : ${sgnp(VOL().goal,1)} par an)","(annonce standard)")
# bonus : effet direct
rep("const BONUS=[0.05,0.075,0.10,0.15,0.20],POACHP=0.5,MOT={m0:0.30,k:0.7,up:0.10,dn:0.18,poach:0.8,cut:1.6,i0:2,lo:1.15,hi:0.85};\nfunction motTg(i){return Math.sqrt(BONUS[i]/0.20)}\nfunction motNow(){return S&&S.mot!=null?S.mot:MOT.m0}\n",
    "const BONUS=[0.05,0.075,0.10,0.15,0.20],POACHP=0.5,MOT={i0:2};\n/* lot 115 : effet direct du cran de bonus versé — g : part de la baisse des coûts du budget salle de marché que le desk livre ;\n   p : risque de débauchage par trimestre ; ×1,5 le trimestre d'une baisse de taux */\nconst BONFX=[{g:0.50,p:0.50},{g:0.65,p:0.40},{g:0.80,p:0.30},{g:0.95,p:0.20},{g:1.10,p:0.12}],BONCUT=1.5;\nfunction bonEff(){return S&&S.bonEff!=null?S.bonEff:MOT.i0}\n")
rep("function execMot(i){const e=EXECM[i==null?S.bud.exec:i],m=motNow();return (e<1?1-(1-e)*(0.5+0.5*m):e)*(MOT.lo+(MOT.hi-MOT.lo)*m)}   /* lot 108 : la motivation donne la moitié du gain */",
    "function execMot(i){const e=EXECM[i==null?S.bud.exec:i];return e<1?1-(1-e)*BONFX[bonEff()].g:e}")
rep("function poachNow(){return Math.min(0.95,POACHP*(1-MOT.poach*motNow())*(S.bonCutQ===S.q?MOT.cut:1))}",
    "function poachNow(){return Math.min(0.95,BONFX[bonEff()].p*(S.bonCutQ===S.q?BONCUT:1))}")
rep("function bonTxt(){return `<br>Motivation du desk : <b>${Math.round(motNow()*100)} %</b> · coûts ×${dec(execMot(),2)} au lieu de ×${dec(EXECM[S.bud.exec],2)}",
    "function bonTxt(){return `<br>Bonus au cran ${dec(BONUS[bonEff()]*100,1)} % : le desk livre ${Math.round(BONFX[bonEff()].g*100)} % de la baisse des coûts de votre budget · coûts ×${dec(execMot(),2)} au lieu de ×${dec(EXECM[S.bud.exec],2)}")
rep("${S.bonCutQ===S.q?' · <span class=\"neg-g\">baisse du taux mal vécue</span>':''}.`}","${S.bonCutQ===S.q?' · <span class=\"neg-g\">baisse du taux : débauchage ×1,5 ce trimestre</span>':''}.`}")
rep(" const tg=perf>0?motTg(i):0;let m=motNow();m+=MOT.k*(tg-m)+(d>0?MOT.up*d:MOT.dn*d);S.mot=Math.max(0,Math.min(1,m));\n",
    " S.bonEff=perf>0?i:0;\n")
rep("(motivation ${Math.round(motNow()*100)} %)","(bonus ${dec(BONUS[bonEff()]*100,1)} %)")
i=s.index(" const bnSel=");j=s.index(" const gtSel=",i)
s=s[:i]+''' const bnSel=(S.over||S.q>=QT())?'':(()=>{const pf=Math.max(0,(S.mgrQ&&S.mgrQ.perf)||0),cur=S.bonI==null?MOT.i0:S.bonI,prev=S.bonPrev==null?MOT.i0:S.bonPrev,e=EXECM[S.bud.exec];
  return `<div class="block"><div class="blockhead"><h2>Taux de bonus d'équipe</h2><span class="hint">versé à l'ouverture</span></div>
  <p class="note" style="margin-top:0">Une part de votre commission de performance${pf>0?` (${mm(pf)} ce trimestre)`:' — aucune ce trimestre : rien ne sera versé, et le desk se comporte comme au cran minimal'}. Le taux fixe deux choses, directement : la part de la baisse des coûts d'exécution de votre budget salle de marché que le desk livre, et le risque de débauchage. Baisser le taux multiplie le débauchage par 1,5 le trimestre de la baisse.</p>
  <div class="cisel">${BONUS.map((p,i)=>{const F=BONFX[pf>0?i:0],c=e<1?1-(1-e)*F.g:e;return `<button class="bnp${i===cur?' on':''}" data-i="${i}">${dec(p*100,Number.isInteger(Math.round(p*1000)/10)?0:1)} %<br><small>${mm(p*pf)} · coûts ×${dec(c,2)} · débauche ${Math.round(Math.min(0.95,F.p*(i<prev?BONCUT:1))*100)} %</small></button>`}).join('')}</div></div>`})();
'''+s[j:]
assert 'motNow' not in s and 'motTg' not in s and 'S.mot' not in s
# négociation facultative
rep("const O=[['','Aucune'],['vol',","const O=[['','Ne pas négocier'],['vol',")
rep("<h2>Négocier une limite</h2><span class=\"hint\">trimestre prochain</span>","<h2>Négocier une limite</h2><span class=\"hint\">facultatif · trimestre prochain</span>")
rep("Sans carton ce trimestre, le comité accepte de relever une limite pendant un trimestre. Les investisseurs l'apprennent : confiance ${LIM.negLp} à l'ouverture.",
    "Facultatif. Sans carton ce trimestre, vous pouvez demander au comité de relever une limite pendant un trimestre. Seulement si vous le demandez, les investisseurs l'apprennent : confiance ${LIM.negLp} à l'ouverture.")
# équilibrage
rep("sigBonus:0,capture:0.85,tcMult:0.90,","sigBonus:0,capture:0.85,tcMult:1.00,")
rep("rumBonus:0.05,lpMult:0.90,modelScale:0.80","rumBonus:0.05,lpMult:0.75,modelScale:0.80")
rep("goalMult:1,costM:1.20,seed:0}","goalMult:1,costM:1.35,seed:0}")
rep("aucun capital de départ ; équipe 20 % plus chère","aucun capital de départ ; équipe 35 % plus chère")
open('index.html','w',encoding='utf-8').write(s);print('lot115 p1 ok')
s=open('index.html',encoding='utf-8').read()
rep("jauge investisseurs 10 % moins nerveuse","jauge investisseurs 25 % moins nerveuse",1) if s.count("jauge investisseurs 25 % moins nerveuse")==1 and False else None
rep("rapports réguliers : jauge investisseurs 10 % moins nerveuse","rapports réguliers : jauge investisseurs 25 % moins nerveuse")
rep("coûts de transaction −10 %, un ajustement gratuit par trimestre","un ajustement gratuit par trimestre")
open('index.html','w',encoding='utf-8').write(s);print('lot115 p1b ok')
