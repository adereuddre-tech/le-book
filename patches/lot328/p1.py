p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# activiste : trois profils (sûr / équilibré / audacieux), réussite qui monte avec la mise et la légende, coup du siècle gradué
rep("""const BK={stakes:[0.01,0.02,0.03,0.04,0.05],cds:[0.05,0.10,0.15],W:8,pCds:0.45,rec:12};""",
"""const BK={stakes:[0.01,0.02,0.03,0.04,0.05],cds:[0.05,0.10,0.15],W:8,pCds:[0.40,0.50,0.60],rec:12,perPt:0.03,leg:0.05,legMax:0.15,pMax:0.95,
 P:[{id:'sur',nm:'coup sûr',p:0.75,W:0.8},{id:'eq',nm:'équilibré',p:0.60,W:1.6},{id:'aud',nm:'audacieux',p:0.45,W:2.6}]};   /* lot 328 : espérance croissante avec le risque */
function bkLeg(){return Math.min(BK.legMax,BK.leg*(S.atkWins||0))}
function bkP(o,st){if(o.cds)return BK.pCds[Math.max(0,BK.cds.indexOf(st))];return Math.min(BK.pMax,o.p+BK.perPt*(Math.round(st*100)-1)+bkLeg())}""")
rep("""while(L.length<3&&C.length){const x=C.splice(Math.floor(u()*C.length),1)[0];L.push({c:x[0],nm:x[1],f:x[2],ctx:x[3],d:u()<0.5?1:-1,p:Math.round((0.45+0.20*u())*20)/20,W:Math.round((1.6+0.6*u())*10)/10})}
 if((S.bkStreak||0)>=3){const x=BKCDS[Math.floor(u()*BKCDS.length)];L.unshift({c:x[0],nm:x[1],f:'cds',ctx:x[3],d:x[2],p:BK.pCds,W:BK.W,cds:1})}""",
"""BK.P.forEach(P=>{if(!C.length)return;const x=C.splice(Math.floor(u()*C.length),1)[0];L.push({c:x[0],nm:x[1],f:x[2],ctx:x[3],d:u()<0.5?1:-1,pr:P.id,prn:P.nm,p:Math.round((P.p+0.04*(u()-0.5))*100)/100,W:Math.round((P.W*(0.97+0.06*u()))*10)/10})});
 if((S.bkStreak||0)>=3){const x=BKCDS[Math.floor(u()*BKCDS.length)];L.unshift({c:x[0],nm:x[1],f:'cds',ctx:x[3],d:x[2],p:BK.pCds[0],W:BK.W,cds:1})}""")
rep("""Réussite ${Math.round(a.p*100)} %, gain ${dec(a.W,1)} fois la mise ; verdict à la clôture.""","""Réussite ${Math.round(a.p*100)} %, gain ${dec(a.W,1)} fois la mise, espérance ${sgn(a.p*a.W-(1-a.p),0).replace(' %','')}${' '}% de la mise ; verdict à la clôture.""")
rep("""  <p class="note" style="margin:0 0 6px">Des marchés que votre book ne touche pas : votre desk y repère trois occasions. La manœuvre ne pèse ni sur le risque, ni sur la marge du book ; seul le résultat compte, à la clôture. ${ser}.</p>
  ${L.map((x,j)=>`<button class="pwb${j===S.bkSel?' on':''}" data-bk="${j}"><b>${x.cds?`👑 Coup du siècle · ${x.nm}`:`${x.d>0?'▲':'▼'} ${x.nm} · ${bkKind(x.f,x.d)}`}</b><small>${x.ctx} <i>· réussite ${Math.round(x.p*100)} % · gain ${dec(x.W,1)} × la mise</i></small></button>`).join('')}""",
"""  <p class="note" style="margin:0 0 6px">Des marchés que votre book ne touche pas : votre desk y repère trois occasions, du coup sûr à l'audacieux. Plus le coup est risqué, plus il rapporte en moyenne. La réussite monte de ${Math.round(BK.perPt*100)} points par point de mise (le desk y met les moyens) et de ${Math.round(BK.leg*100)} points par manœuvre réussie dans le mandat (votre légende : +${Math.round(bkLeg()*100)} sur ${Math.round(BK.legMax*100)}), jusqu'à ${Math.round(BK.pMax*100)} %. La manœuvre ne pèse ni sur le risque, ni sur la marge du book ; seul le résultat compte, à la clôture. ${ser}.</p>
  ${L.map((x,j)=>{const pp=bkP(x,x.cds?(BK.cds.includes(sk)?sk:BK.cds[0]):(BK.stakes.includes(sk)?sk:0.03));return `<button class="pwb${j===S.bkSel?' on':''}" data-bk="${j}"><b>${x.cds?`👑 Coup du siècle · ${x.nm}`:`${x.d>0?'▲':'▼'} ${x.nm} · ${bkKind(x.f,x.d)} · <i>${x.prn}</i>`}</b><small>${x.ctx} <i>· réussite ${Math.round(pp*100)} % · gain ${dec(x.W,1)} × la mise · espérance ${pp*x.W-(1-pp)>=0?'+':'−'}${Math.round(Math.abs(pp*x.W-(1-pp))*100)} % de la mise</i></small></button>`}).join('')}""")
rep("""  <div class="attr"><span class="an">Mise ${mm(sk*S.nav)} · réussite ${Math.round(o.p*100)} %</span><span class="av"><b class="pos-g">+${mm(o.W*sk*S.nav)}</b> / <b class="neg-g">−${mm(sk*S.nav)}</b></span></div>""",
"""  ${(()=>{const pp=bkP(o,sk),ev=(pp*o.W-(1-pp))*sk*S.nav;return `<div class="attr"><span class="an">Mise ${mm(sk*S.nav)} · réussite ${Math.round(pp*100)} %</span><span class="av"><b class="pos-g">+${mm(o.W*sk*S.nav)}</b> / <b class="neg-g">−${mm(sk*S.nav)}</b></span></div><div class="attr"><span class="an">Espérance</span><span class="av"><b class="${cls(ev)}">${ev>=0?'+':'−'}${mm(Math.abs(ev))}</b></span></div>`})()}""")
# l'ordre d'affichage du sélecteur doit précéder l'usage de sk dans les offres : sk est déjà défini avant le return
rep("""S.atk={q:S.q,c:o.c,nm:o.nm,d:o.d,p:o.p,W:o.W,st,cds:!!o.cds,kind:o.cds?o.nm:bkKind(o.f,o.d)};""",
    """S.atk={q:S.q,c:o.c,nm:o.nm,d:o.d,p:bkP(o,st),W:o.W,st,cds:!!o.cds,pr:o.prn,kind:o.cds?o.nm:bkKind(o.f,o.d)};""")
rep("""ouvrent le coup du siècle : mise de 5 à 15 %, gain jusqu'à huit fois la mise. */""","""ouvrent le coup du siècle : mise de 5 à 15 %, gain jusqu'à huit fois la mise.
   lot 328 : trois profils (sûr, équilibré, audacieux) à espérance croissante ; réussite +3 pts par point de mise, +5 pts par réussite du mandat (≤ +15), plafond 95 % ;
   coup du siècle 40 / 50 / 60 % à 5 / 10 / 15 %. */""")
open(p,'w',encoding='utf-8').write(s)
