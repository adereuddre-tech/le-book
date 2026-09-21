# -*- coding: utf-8 -*-
"""Lot 47 — une fin de partie plus douce, un bouton « Abandonner », les minuteurs en pause.

  - Fin de partie : l'encours doit tomber sous 5 % de son niveau de départ (−95 %), au lieu de
    40 %. Entre les deux, on survit, amaigri : les commissions fondent avec l'encours, et c'est
    déjà une punition suffisante. `NAVEND` porte le seuil ; les cinq textes qui disaient 40 % le
    lisent désormais.
  - « Abandonner » sous « Trimestre suivant » au débriefing, avec confirmation. La partie se
    termine par un verdict propre (« Vous avez rendu les clés ») et entre au palmarès.
  - Minuteurs : le compte à rebours des dépêches ne décompte pas tant qu'une fenêtre
    (tutoriel, info-bulle, pop-up de jauge) ou une carte dorée est ouverte. La fenêtre fermée
    reste dans le DOM (`display:none`) : c'est l'affichage qu'on teste, pas la présence.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep(" if(S.nav<0.40*S.aum0)S.over='nav';"," if(S.nav<NAVEND*S.aum0)S.over='nav';")
e.rep("function ddMax(){","/* Fin de partie : l'encours sous 5 % de son niveau de départ (−95 %). */\nconst NAVEND=0.05;\nfunction ddMax(){")
# textes
e.rep("et si l'encours tombe sous 40 % de son niveau de départ, la partie s'arrête","et si l'encours fond de 95 %, la partie s'arrête")
e.rep("Une seule façon : l'encours tombe sous <strong>40 %</strong> de son niveau de départ.",
      "Deux façons : l'encours tombe sous <strong>5 %</strong> de son niveau de départ, ou vous abandonnez.")
e.rep("Le fonds ne s'arrête que sous <em>${moneyB(0.4*S.aum0)}</em>, 40 % de l'encours de départ.",
      "Le fonds ne s'arrête que sous <em>${moneyB(NAVEND*S.aum0)}</em>, 5 % de l'encours de départ.")
e.rep("Le fonds ne s'arrête que si l'encours tombe sous 40 % de son niveau de départ.</p>",
      "Le fonds ne s'arrête que si l'encours tombe sous 5 % de son niveau de départ.</p>")
e.rep("La partie ne s'arrête que si l'encours tombe sous 40 % de son niveau de départ.</p>",
      "La partie ne s'arrête que si l'encours tombe sous 5 % de son niveau de départ.</p>")
e.rep("vtxt=`Le fonds est tombé sous 40 % de son encours de départ au trimestre ${S.q}",
      "vtxt=`Le fonds est tombé sous 5 % de son encours de départ au trimestre ${S.q}")
# abandon
e.rep(" if(S.over){   /* seule fin depuis le lot 25 ; couvre aussi les sauvegardes 'dd'/'lp'/'rc' */",
      " if(S.over==='quit'){verdict=\"Vous avez rendu les clés\";vtxt=`Au trimestre ${S.q}, vous avez préféré arrêter. Le conseil prend acte ; les commissions encaissées jusque-là restent les vôtres.`}\n"
      " else if(S.over){   /* encours sous NAVEND ; couvre aussi les sauvegardes 'dd'/'lp'/'rc' */")
e.rep("""  <button class="cta" id="nx">${S.over?'Voir le rapport final':(S.q>=QT()?`Clôturer les ${DUR().ans} an${DUR().ans>1?'s':''}`:'Trimestre suivant')}</""",
      """  <button class="cta" id="nx">${S.over?'Voir le rapport final':(S.q>=QT()?`Clôturer les ${DUR().ans} an${DUR().ans>1?'s':''}`:'Trimestre suivant')}</""")
e.rep(" document.getElementById('nx').onclick=()=>{\n  if(S.over||S.q>=QT()){screenFinal();window.scrollTo(0,0);return}",
""" if(!S.over&&S.q<QT()){const nx=document.getElementById('nx'),qb=document.createElement('button');
  qb.className='quitb';qb.id='quit';qb.textContent='Abandonner';nx.after(qb);
  qb.onclick=()=>{openModal('Abandonner la partie ?',`<p>Le mandat s'arrête ici. Vos commissions nettes, ${score(S.mgrFees-S.mgrCosts)}, restent les vôtres et la partie entre au palmarès avec un indice de ${Math.round(mgrIndex())}.</p>
   <p style="margin-top:14px;display:flex;gap:10px"><button class="buy" id="quitok">Rendre les clés</button><button class="buy" id="quitno">Continuer</button></p>`);
   document.getElementById('quitno').onclick=()=>{document.getElementById('modal').style.display='none'};
   document.getElementById('quitok').onclick=()=>{document.getElementById('modal').style.display='none';S.over='quit';save('screenDebrief');screenFinal();window.scrollTo(0,0)}}}
 document.getElementById('nx').onclick=()=>{
  if(S.over||S.q>=QT()){screenFinal();window.scrollTo(0,0);return}""")
e.rep(".lvls{display:grid;",".quitb{display:block;margin:12px auto 0;background:none;border:1px solid var(--line);color:var(--dim);font-family:var(--mono);font-size:12px;letter-spacing:.04em;padding:8px 16px;border-radius:8px;cursor:pointer}\n.lvls{display:grid;")
# minuteur en pause tant qu'une fenêtre est ouverte
e.rep(" TID=setInterval(()=>{t--;if(t<=0){",
      " /* en pause tant qu'une fenêtre ou une carte dorée est à l'écran : on lit sans être pressé */\n"
      " const busy=()=>{const m=document.getElementById('modal');return (m&&m.style.display!=='none')||!!document.getElementById('gold')};\n"
      " TID=setInterval(()=>{if(busy()){el.classList.add('paused');return}el.classList.remove('paused');t--;if(t<=0){")
e.rep(".lvls{display:grid;",".evtimer.paused{opacity:.45}\n.lvls{display:grid;")

# ── la spirale des rachats ──────────────────────────────────────────────────────
# Mesure (bot, full-floor, 15 parties) : même au seuil de −95 %, 8 fonds sur 15 disparaissaient,
# encours final 1,5 à 4,6 % du départ. Cause : le repli qui déclenche les rachats était
# `S.maxdd`, (1) un maximum sur toute la partie — une fois franchi, rachats à CHAQUE clôture,
# même après remontée — et (2) calculé sur l'encours (1 − nav/pic), donc les rachats creusaient
# eux-mêmes le repli qui les déclenchait. On mesure désormais le repli sur la performance
# (indice net contre son plus haut), et seul un nouveau plus bas au-delà du seuil (+2 pts par
# rapport au dernier déclenchement) fait partir de l'argent ; revenu à la moitié du seuil,
# le compteur se réarme.
e.rep(" if(S.maxdd>=ddMax())redeem('repli',0.10+0.35*(S.maxdd-ddMax()));",
      """ {const ddp=Math.max(0,1-S.idx/Math.max(S.hwmIdx||1,S.idx));
  if(ddp<ddMax()/2)S.ddHit=0;
  if(ddp>=ddMax()&&ddp>(S.ddHit||0)+0.02){S.ddHit=ddp;redeem('repli',0.10+0.35*(ddp-ddMax()))}}""")
# comptabilité des flux : le montant se mesure avant de réduire l'encours
e.rep(" S.nav*=(1-out);S.flows-=out*S.nav;S.qFlow=(S.qFlow||0)-out*S.nav;",
      " const amt=out*S.nav;S.nav-=amt;S.flows-=amt;S.qFlow=(S.qFlow||0)-amt;")
e.done("lot 47 — fin a -95 %, abandon, minuteurs en pause")
