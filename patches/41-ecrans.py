# -*- coding: utf-8 -*-
"""Lot 4 (suite) — écrans : une étape d'exécution au lieu de deux, annonce en un clic,
pré-annonces vides, pastille « vérifiée » qui débordait, nowcast durable, ancien du desk."""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ══ 1. exécution : la fenêtre de phase disparaît, l'écran porte l'information ══
old=e.s[e.s.index("function phaseExec(){"):e.s.index("function phaseLive(){")]
e.rep(old,"")
e.rep("""screenComm:()=>screenComm(),phaseExec:()=>phaseExec(),screenExec:()=>screenExec(),""",
      """screenComm:()=>screenComm(),phaseExec:()=>screenExec(),screenExec:()=>screenExec(),""")
e.rep(""" app.innerHTML=statusBar()+`<div class="fade">
  <div class="block"><details open><summary style="font-size:15px;color:var(--txt);font-weight:600">Récapitulatif des ordres · ${orders.length} marché${orders.length>1?'s':''}</summary>
   <div class="wire">${orders.length?orders.map(o=>`<div class="attr"><span class="an"><span class="num" style="color:${GRPC[INSTR[o.i].grp]}">${INSTR[o.i].sym}</span> <span class="recap" style="color:var(--dimmer)">${S.k0[o.i]>0?'+':''}${S.k0[o.i]} → ${S.k[o.i]>0?'+':''}${S.k[o.i]} · ${moneyB(o.t.bn)}</span></span><span class="av neg-g">${o.t.bp.toFixed(1)} pb · ${mm(o.t.cost)}</span></div>`).join('')
    +`<div class="kv" style="margin-top:8px"><span>Total au tarif standard</span><b class="neg-g">${mm(tot)} · ${sgn(-tot/S.nav,3)}</b></div>`
    :`<p class="note" style="margin:0">Aucun ordre. Le book est reconduit.</p>`}
   <p class="note">Multiplicateur du trimestre ×${mult.toFixed(2)} : budget desk ×${EXECM[S.bud.exec].toFixed(2)}, liquidité ×${S.liq.toFixed(2)}, taux ×${(1+(S.rate-0.03)*4).toFixed(2)}, profil ×${PROF().tcMult.toFixed(2)}${S.execPenalty!==1?`, débauchage ×${S.execPenalty.toFixed(2)}`:''}. Organisation « ${DESK().nm.toLowerCase()} » appliquée marché par marché.${S.star>=0?` Recrue du trimestre sur ${INSTR[S.star].sym} : ÷3.`:''}</p>
  </div>""",
""" const lqNm=S.liq>1.5?'très dégradée':S.liq>1.2?'dégradée':S.liq>1.05?'un peu tendue':S.liq<0.92?'excellente':'normale';
 app.innerHTML=statusBar()+`<div class="fade">
  <div class="block"><div class="blockhead"><h2>${orders.length?'Les traders passent vos ordres':'Aucun ordre à passer'}</h2><span class="hint">T${S.q+1} · exécution</span></div>
   ${orders.length?`<div class="kv"><span>Coût total des ordres, à votre charge</span><b class="neg-g">${mm(tot)} · ${(tot/S.nav*1e4).toFixed(0)} pb de l'encours</b></div>
   <div class="kv"><span>Trésorerie de votre société après paiement</span><b class="${(mgrCash())>=0?'':'neg-g'}">${mm(mgrCash())}</b></div>
   <p class="note" style="margin:8px 0 0">${orders.length} marché${orders.length>1?'s':''} à travailler, liquidité ${lqNm} (×${S.liq.toFixed(2)}), taux au jour le jour ${(S.rate*100).toFixed(1)} %. Le desk a son mot à dire sur la manière de faire.</p>`
   :`<p class="note" style="margin:0">Le book est reconduit tel quel : vous ne payez rien. Le desk en profite pour vous parler d'autre chose.</p>`}
   ${orders.length?`<details style="margin-top:10px"><summary>Détail des ordres et des coûts, marché par marché</summary>
    <div class="wire" style="margin-top:8px">${orders.map(o=>`<div class="attr"><span class="an"><span class="num" style="color:${GRPC[INSTR[o.i].grp]}">${INSTR[o.i].sym}</span> <span class="recap" style="color:var(--dimmer)">${S.k0[o.i]>0?'+':''}${S.k0[o.i]} → ${S.k[o.i]>0?'+':''}${S.k[o.i]} · ${moneyB(o.t.bn)}</span></span><span class="av neg-g">${o.t.bp.toFixed(1)} pb · ${mm(o.t.cost)}</span></div>`).join('')}
    <p class="note">Multiplicateur du trimestre ×${mult.toFixed(2)} : budget desk ×${EXECM[S.bud.exec].toFixed(2)}, liquidité ×${S.liq.toFixed(2)}, taux ×${(1+(S.rate-0.03)*4).toFixed(2)}, profil ×${PROF().tcMult.toFixed(2)}${S.execPenalty!==1?`, débauchage ×${S.execPenalty.toFixed(2)}`:''}.${S.star>=0?` Recrue du trimestre sur ${INSTR[S.star].sym} : ÷3.`:''}</p></div></details>`:''}
  </div>""")

# ══ 2. annonce : toucher la promesse vaut validation ══
e.rep("""  ${opts.map((o,i)=>`<div class="cardwrap ${S.commPick===o.id?'sel':''}"><button class="card" data-i="${i}">""",
      """  ${opts.map((o,i)=>`<div class="cardwrap"><button class="card commgo" data-i="${i}">""")
e.rep("""Avant l'exécution, vous rencontrez les investisseurs et le comité des risques. Que promettez-vous pour ce trimestre ?</p>""",
      """Avant l'exécution, vous rencontrez les investisseurs et le comité des risques. Que promettez-vous pour ce trimestre ? Touchez votre réponse, elle est validée aussitôt.</p>""")
e.rep("""  <p class="note">L'annonce ne change rien tout de suite : elle se solde à la fin du trimestre, sur le résultat tout compris, commissions et coûts déduits.</p>
  <button class="cta gold" id="commok" ${S.commPick?'':'disabled'}>${S.commPick?'Annoncer : '+opts.find(o=>o.id===S.commPick).nm.toLowerCase():'Choisissez votre annonce'}</button></div>`;
 app.querySelectorAll('.card[data-i]').forEach(b=>b.onclick=()=>{S.commPick=opts[+b.dataset.i].id;screenComm()});
 document.getElementById('commok').onclick=()=>{
  const o=opts.find(x=>x.id===S.commPick);S.comm={id:o.id,nm:o.nm,ret:o.ret,win:o.win,lose:o.lose};
  S.commPick=null;phaseExec();
 };""",
"""  <p class="note">L'annonce ne change rien tout de suite : elle se solde à la fin du trimestre, sur le résultat tout compris, commissions et coûts déduits.</p></div>`;
 app.querySelectorAll('.card[data-i]').forEach(b=>b.onclick=()=>{
  const o=opts[+b.dataset.i];S.comm={id:o.id,nm:o.nm,ret:o.ret,win:o.win,lose:o.lose};
  S.commPick=null;screenExec();window.scrollTo(0,0);
 });""")

# ══ 3. pré-annonces « undefined » : la file contient aussi des dépêches de rivalité, sans texte ══
e.rep(""" S.evQueue.filter(ev=>!ev.trader).slice(0,3).forEach(ev=>{if(rng()<pr){""",
      """ S.evQueue.filter(ev=>!ev.trader&&!ev.rivalEv&&!ev.stake&&ev.t&&ev.hit).slice(0,3).forEach(ev=>{if(rng()<pr){""")

# ══ 4. source vérifiée : une pastille, plus un préfixe qui déborde du gabarit ══
e.rep("""   if(cand.length){const r=pick(cand);r.truth=true;r.p=0.97;r.rel='forte';r.sure=true;
     r.src='Source vérifiée · '+r.src}""",
      """   if(cand.length){const r=pick(cand);r.truth=true;r.p=0.97;r.rel='forte';r.sure=true}""")
e.rep("""<i class="rel ${r.rel}">fiabilité ${r.rel}</i>""",
      """${r.sure?'<i class="sure">✓ vérifiée</i>':''}<i class="rel ${r.rel}">fiabilité ${r.rel}</i>""")
e.rep(""".chips i.rel.faible{color:var(--dimmer)}""",
""".chips i.rel.faible{color:var(--dimmer)}
.chips i.sure{color:var(--gold);background:rgba(217,176,106,.16)}
.news .src{overflow-wrap:anywhere}""")

# ══ 5. le modèle de nowcast sert tout le mandat, et il est payé par le gérant ══
e.rep("""  ch:[{b:"Acheter",s:"−30 pb, précision des signaux marché améliorée ce trimestre.",e:{cash:-0.003,tcvBoost:true}},{b:"Refuser",s:"Rien.",e:{}},""",
      """  ch:[{b:"Acheter le modèle",s:"−1,5 M$ de votre poche ; le bruit de vos indicateurs de tendance, portage et valeur est divisé par trois, pour tout le reste du mandat.",e:{mgrM:-1.5,tcvPerm:true}},{b:"Refuser",s:"Rien.",e:{}},""")
e.rep("""  if(e.tcvBoost){const t=S.tcv;S.tcvEst={t:t.t.map(quant),c:t.c.map(quant),v:t.v.map(quant)};msg.push("Le desk dispose maintenant de signaux marché exacts pour le trimestre.")}""",
"""  if(e.tcvBoost){const t=S.tcv;S.tcvEst={t:t.t.map(quant),c:t.c.map(quant),v:t.v.map(quant)};msg.push("Le desk dispose maintenant de signaux marché exacts pour le trimestre.")}
  if(e.tcvPerm){S.tcvPerm=true;const t=S.tcv;S.tcvEst={t:t.t.map(quant),c:t.c.map(quant),v:t.v.map(quant)};msg.push("Vos indicateurs sont recalés dès maintenant, et le resteront jusqu'à la fin du mandat.")}
  if(e.mgrM){S.mgrCosts-=e.mgrM/1000;refreshGain();msg.push(`${e.mgrM<0?'−':'+'}${mm(Math.abs(e.mgrM)/1000)} sur vos gains de gérant.`)}""")
e.rep(""" const e=TCVQ[S.bud.exec];""",
      """ const e=TCVQ[S.bud.exec]*(S.tcvPerm?0.33:1);   /* le modèle de nowcast acheté sert tout le mandat */""")

# ══ 6. « Un ancien du desk » : des montants qui veulent dire quelque chose ══
e.rep("""{b:"Investir 50 M$",s:"−5 pb, 35 % de récupérer +15 pb dans un an... enfin ce trimestre.",e:{cash:-0.0005,risk:[0.35,0.0015],riskMsg:"Son fonds a bien démarré",safeTxt:"Son fonds ne décolle pas."}}""",
      """{b:"Placer 1 % de l'encours chez lui",s:"−100 pb tout de suite ; 35 % de chances que sa première année rende +260 pb, sinon l'argent y dort.",e:{cash:-0.010,risk:[0.35,0.026],riskMsg:"Son fonds a très bien démarré",safeTxt:"Son fonds ne décolle pas : votre argent y dort."}}""")

e.done("lot 4 — écrans et événements")
