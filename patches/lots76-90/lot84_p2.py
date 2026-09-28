import re
P='/home/claude/le-book/index.html';s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:100]);s=s.replace(old,new)
def rall(old,new):
    global s;n=s.count(old);assert n>=1,(0,old);s=s.replace(old,new);return n
# ---- risque trimestriel à l'affichage, comme la rentabilité (moteur inchangé, en annuel) ----
rep("function redOn(id){","/* lot 84 : le risque s'affiche en écart-type trimestriel, comme la rentabilité (le moteur reste annualisé) */\nfunction RQ(v){return v/2}\nfunction redOn(id){")
n1=rall("pct(sp)","pct(RQ(sp))");n2=rall("pct(te.sp)","pct(RQ(te.sp))");n3=rall("pct(0.7*S.tgt)","pct(RQ(0.7*S.tgt))")
n4=rall("pct(S.tgt)","pct(RQ(S.tgt))");n5=rall("pct(S.tgt,0)","pct(RQ(S.tgt),0)");n6=rall("pct(R.vol)","pct(RQ(R.vol))")
n7=rall("dec(TAIL.x0*100,0)","dec(TAIL.x0*50,0)");n8=rall("dec(sp*100,0)","dec(sp*50,0)")
rep("σ ${dec((sp0*100),1)} → <b>${dec((sp1*100),1)} %</b>","σ ${dec((sp0*50),1)} → <b>${dec((sp1*50),1)} %</b>")
rep("<td>${a.rk!==undefined?dec(a.rk*100,0)+' %':''}</td>","<td>${a.rk!==undefined?dec(a.rk*50,1)+' %':''}</td>")
rep("const rP=(R(kp)-r0)*100,rM=(R(km)-r0)*100,","const rP=(R(kp)-r0)*50,rM=(R(km)-r0)*50,")
s=s.replace("x.tgt)o.push(`cible de risque <em>${pct(x.tgt)}</em>`)","x.tgt)o.push(`cible de risque <em>${pct(RQ(x.tgt))}</em>`)")
s=s.replace("au-delà de 25 % de risque, la zone rouge","au-delà de 10 % de risque, la zone rouge")
# nuage : trimestriel, collatéral compris au point de départ
rep("const sv=`${dec(sp*100,1)} %`,   /* lot 83 : risque annualisé, comme partout ailleurs */","const sv=`${dec(sq*100,1)} %`,   /* lot 84 : trimestriel, comme la rentabilité */")
rep(" const sq=sp/2;"," const cs=colStdQ(),sq=Math.sqrt((sp/2)**2+cs*cs);   /* lot 84 : sans position, le risque est celui du collatéral */")
rep("function RQ(v){return v/2}","function RQ(v){return v/2}\nfunction colStdQ(){if(redOn('collat'))return 0;const o=colOpt();return o.l*Math.sqrt(o.p*(1-o.p))}")
rep('text-anchor="middle" fill="var(--dimmer)" font-family="var(--mono)">${Math.round(v*200)}</text>','text-anchor="middle" fill="var(--dimmer)" font-family="var(--mono)">${Math.round(v*100)}</text>')
rep("Risque : volatilité <b>annualisée</b> du book, comme partout dans le jeu, bruit d'estimation compris ; rentabilité : rendement attendu <b>du trimestre</b>. Graduations du risque tous les 10 points ;",
    "Valeurs <b>trimestrielles</b>, comme partout dans le jeu. Risque : écart-type du trimestre, book et collatéral compris, bruit d'estimation compris ;")
rep(" Rentabilité graduée tous les 5 points."," Traits tous les 5 points.")
# ---- mi-parcours : le ruban dit le trimestre à date ----
rep("""pre:`<div class="tape big" style="margin:4px 0 14px"><div class="tapehead"><span>DEPUIS LE LANCEMENT</span>""",
    """pre:`<div class="tape big" style="margin:4px 0 14px"><div class="tapehead"><span>T${S.q+1} À DATE <b class="${p[p.length-1]>=p[Math.min(p.length-1,S.tape.q0||0)]?'pos-g':'neg-g'}">${sgnp(p[p.length-1]/p[Math.min(p.length-1,S.tape.q0||0)]-1,1)}</b> · DEPUIS LE LANCEMENT</span>""")
rep("${tapeSvg(p,S.tape.q0||0,{h:150,anim:1,draw:3,zero:1,rivals:rivalTapes()})}</div>`};","${tapeSvg(p,S.tape.q0||0,{h:150,anim:1,draw:3,zero:1,rivals:rivalTapes(),qs:S.tape.q0||0,ql:S.q+1})}</div>`};")
# ---- fin de trimestre : l'essentiel resserré ----
rep("  ${cz.length?`<p class=\"note\" style=\"margin:0 0 8px\">${cz.map(x=>`${x[0]} <b class=\"${x[1]>=0?'pos-g':'neg-g'}\">${sd1(x[1])}</b>`).join(' · ')}</p>`:''}\n","")
rep("""  ${S.comm&&S.comm.ret!==null?`<div class="attr"><span class="an">Engagement</span><span class="av">promis ≥ ${sgn(S.comm.ret,1)}, livré ${sgn(o.qTotal,1)} · <b class="${S.commRes&&S.commRes.ok?'pos-g':'neg-g'}">${S.commRes&&S.commRes.ok?'tenu':'manqué'}, confiance ${sd1(S.commRes&&S.commRes.ok?S.comm.win.lp:S.comm.lose.lp)}</b></span></div>`:''}""",
    """  ${S.comm&&S.comm.ret!==null?`<div class="attr"><span class="an">Engagement ≥ ${sgn(S.comm.ret,1)}</span><span class="av"><b class="${S.commRes&&S.commRes.ok?'pos-g':'neg-g'}">${S.commRes&&S.commRes.ok?'tenu':'manqué'}</b></span></div>`:''}""")
rep("""  <div class="attr"><span class="an">Confiance des investisseurs</span>""",
    """  ${Math.abs(o.P.flowM)>1e-9?`<div class="attr"><span class="an">${o.P.flowM>=0?'Souscriptions':'Rachats'}</span><span class="av">${inU(o.P.flowM,UQ)}</span></div>`:''}
  ${S.colRes&&S.colRes.show?`<div class="attr"><span class="an">Collatéral · ${S.colRes.nm.toLowerCase()}${S.colRes.hit?' · défaut':''}</span><span class="av">${inU(S.colRes.m,UQ)}</span></div>`:''}
  <div class="attr"><span class="an">Confiance des investisseurs</span>""")
rep("""  <div class="attr"><span class="an" style="color:var(--txt)">Trésorerie · votre gain net cumulé</span><span class="av"><b class="gold-g">${mm(mgrCash())}</b></span></div>
 </div>`;""","""  <div class="attr"><span class="an" style="color:var(--txt)">Trésorerie · votre gain net cumulé</span><span class="av"><b class="gold-g">${mm(mgrCash())}</b></span></div>
  <table class="qt" style="margin-top:12px"><thead><tr><th>Fonds</th><th>Risque</th><th>Trim.</th><th>Cumul</th></tr></thead><tbody>
  ${all.map(a=>({a,cv:a.cv})).sort((x,y)=>y.cv-x.cv).map(({a,cv})=>`<tr class="${a.me?'me':''}"><td>${a.nm}${a.th?`<br><span class="neg-g" style="font-size:11px">accident de levier</span>`:''}</td><td>${a.rk!==undefined?dec(a.rk*50,1)+' %':''}</td><td class="${cls(a.v)}">${sgn(a.v,1)}</td><td class="${cls(cv)}">${sgn(cv,1)}</td></tr>`).join('')}
  </tbody></table>
 </div>`;""")
m=re.search(r'\n  <div class="block"><details><summary style="font-size:15px;color:var\(--txt\);font-weight:600">La concurrence.*?</tbody></table></details></div>',s,re.S);assert m;s=s[:m.start()]+s[m.end():]
rep("if(S.poachMsg)warn.push(S.poachMsg);","const detl=[];if(S.poachMsg)detl.push(S.poachMsg);")
rep("{const c=S.colRes;if(c&&c.show)warn.push(c.lock?","{const c=S.colRes;if(c&&c.show)detl.push(c.lock?")
rep("""  <button class="cta" id="nx">""","""  ${detl.length?`<div class="block"><details><summary style="font-size:15px;color:var(--txt);font-weight:600">Rachats et collatéral · le détail</summary>${detl.map(t=>`<p class="note">${t}</p>`).join('')}</details></div>`:''}
  <button class="cta" id="nx">""")
# ---- carton rouge : cadre de carte, plus vif ----
rep(".mbox.redbox{border:2px solid #D2463C;box-shadow:0 0 0 3px rgba(210,70,60,.25)}",
    ".mbox.redbox{max-width:340px;margin-left:auto;margin-right:auto;border:2px solid #E5483C;background:linear-gradient(165deg,#4a1512 0%,#1c0d10 70%);box-shadow:0 0 0 3px rgba(229,72,60,.30),0 0 28px rgba(229,72,60,.45);animation:redglow 1.6s ease-in-out infinite alternate}\n@keyframes redglow{from{box-shadow:0 0 0 3px rgba(229,72,60,.30),0 0 16px rgba(229,72,60,.35)}to{box-shadow:0 0 0 3px rgba(229,72,60,.55),0 0 34px rgba(229,72,60,.70)}}")
# ---- rapport final : durée juste, ton qui claque ----
rep("""else if(cagr>0.18&&S.maxdd<0.15&&rank===1){verdict="Deux années de référence";vtxt="Performance, discipline de risque, et vous avez battu les trois. Reste à savoir ce qui, là-dedans, se reproduira."}
 else if(cagr>0.12&&S.maxdd<0.20){verdict="Mandat renouvelé";vtxt="Vous tenez l'objectif dans les limites. Les investisseurs resignent pour trois ans."}
 else if(cagr>0.03){verdict="Vous survivez";vtxt="Assez pour continuer, pas assez pour lever. Le fonds reste sous-dimensionné pour ses ambitions."}
 else if(cagr>-0.05){verdict="Deux ans pour rien";vtxt="Frais payés, risque pris, rien produit. Les allocataires appellent ça un coût d'option."}""",
"""else if(cagr>0.25&&rank===1){verdict="Une signature sur la place";vtxt=`${ANS} de mandat, et vous finissez devant les trois. Les allocataires font la queue, le fonds ferme aux souscriptions : désormais, c'est vous qui choisissez vos clients.`}
 else if(cagr>0.18&&S.maxdd<0.20){verdict=`${ANSC} de référence`;vtxt="Performance et discipline de risque : le genre de courbe qu'on imprime dans les présentations. Le conseil vous propose d'ouvrir un second fonds."}
 else if(cagr>0.12){verdict="Mandat renouvelé, avec les honneurs";vtxt=`Vous tenez l'objectif, et plus. Les investisseurs resignent pour ${ANS} de plus et augmentent leurs tickets.`}
 else if(cagr>0.03){verdict="Vous survivez";vtxt="Assez pour continuer, pas assez pour lever. Le fonds reste sous-dimensionné pour ses ambitions."}
 else if(cagr>-0.05){verdict=`${ANSC} pour rien`;vtxt="Frais payés, risque pris, rien produit. Les allocataires appellent ça un coût d'option."}""")
rep(" let verdict,vtxt;"," let verdict,vtxt;const ANS=`${DUR().ans} an${DUR().ans>1?'s':''}`,ANSC=ANS.charAt(0).toUpperCase()+ANS.slice(1);")
open(P,'w',encoding='utf-8').write(s);print('ok',n1,n2,n3,n4,n5,n6,n7,n8)
