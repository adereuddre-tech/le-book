# -*- coding: utf-8 -*-
"""Lot 2 (fin) — les textes qui décrivaient l'ancienne comptabilité."""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# pop-up des coûts : l'exécution change de payeur
e.rep("""  openModal('Coûts du trimestre',`<p>La jauge additionne deux factures. Les <em>frais de gestion</em> et les <em>coûts de transaction</em> sont payés par le fonds et pèsent sur sa performance. Le <em>budget d'exploitation</em> est payé par votre société de gestion : il ne touche pas le fonds, il vient en déduction de vos gains. Un point de base vaut <em>${mm(S.nav*1e-4)}</em>.</p>
   ${tbl([['<b>Payé par le fonds</b>','',''],[`Frais de gestion (${(VOL().mgmt*400).toFixed(1).replace('.',',')} % par an)`,`${(VOL().mgmt*1e4).toFixed(0)} pb`,inU(-VOL().mgmt*S.nav,UC)],['Coûts de transaction'+(S.phase==='book'?' (en préparation)':' (engagés)'),c.tc.toFixed(0)+' pb',inU(-c.tc*1e-4*S.nav,UC)],['Sous-total fonds',`${tf.toFixed(0)} pb`,inU(-tf*1e-4*S.nav,UC)],
     ['<b>Payé par vous</b>','',''],...b.map(x=>[x[0],x[1],inU(-(x[3]||0),UC)]),['Sous-total société',`${c.ops.toFixed(0)} pb`,inU(-c.ops*1e-4*S.nav,UC)],
     ['<b>Total</b>',`<b>${tot.toFixed(0)} pb</b>`,inU(-tot*1e-4*S.nav,UC)]],['Poste','pb',UC.s.trim()])}`);""",
"""  openModal('Coûts du trimestre',`<p>La jauge additionne deux factures. Seuls les <em>frais de gestion</em> sont payés par le fonds et pèsent sur sa performance — et ils vous sont versés dès l'ouverture du trimestre. Le <em>budget d'exploitation</em> et les <em>coûts de transaction</em> sont payés par votre société de gestion : ils ne touchent pas le fonds, ils viennent en déduction de vos gains, et vous ne pouvez engager que ce que vous avez en caisse. Un point de base vaut <em>${mm(S.nav*1e-4)}</em>.</p>
   ${tbl([['<b>Payé par le fonds</b>','',''],[`Frais de gestion (${(VOL().mgmt*400).toFixed(1).replace('.',',')} % par an)`,`${(VOL().mgmt*1e4).toFixed(0)} pb`,inU(-VOL().mgmt*S.nav,UC)],
     ['<b>Payé par vous</b>','',''],['Coûts de transaction'+(S.phase==='book'?' (en préparation)':' (engagés)'),c.tc.toFixed(0)+' pb',inU(-c.tc*1e-4*S.nav,UC)],...b.map(x=>[x[0],x[1],inU(-(x[3]||0),UC)]),['Sous-total société',`${(c.ops+c.tc).toFixed(0)} pb`,inU(-(c.ops+c.tc)*1e-4*S.nav,UC)],
     ['<b>Total</b>',`<b>${tot.toFixed(0)} pb</b>`,inU(-tot*1e-4*S.nav,UC)],
     ['Trésorerie de votre société','',inU(mgrCash(),UC)]],['Poste','pb',UC.s.trim()])}`);""")

# pop-up des gains
e.rep("""   ${tbl([['Commissions de gestion et de performance encaissées',`<b class="pos-g">+${mm(S.mgrFees)}</b>`],
     ['Budget d\\'exploitation payé',`<b class="neg-g">−${mm(S.mgrCosts)}</b>`],
     ['<b>Gains nets</b>',`<b class="${(S.mgrFees-S.mgrCosts)>=0?'pos-g':'neg-g'}">${score(S.mgrFees-S.mgrCosts)}</b>`]])}""",
"""   ${tbl([['Commissions encaissées, bonus d\\'objectif compris',`<b class="pos-g">+${mm(S.mgrFees)}</b>`],
     ['Budget d\\'exploitation et coûts d\\'exécution',`<b class="neg-g">−${mm(S.mgrCosts)}</b>`],
     ...(S.totalTC?[['&nbsp;&nbsp;dont exécution depuis le début',`<span class="dim-g">−${mm(S.totalTC)}</span>`]]:[]),
     ['<b>Gains nets</b>',`<b class="${mgrNet()>=0?'pos-g':'neg-g'}">${score(mgrNet())}</b>`],
     ['Capital de départ de la société',`<span class="dim-g">+${mm(S.mgrCap0||0)}</span>`],
     ['<b>Trésorerie disponible</b>',`<b class="${mgrCash()>=0?'':'neg-g'}">${mm(mgrCash())}</b>`]])}""")
e.rep("""<p class="note">La commission de gestion est prélevée chaque trimestre sur l'encours ; la commission de performance ne se déclenche qu'au-dessus du plus haut historique du fonds. Le budget d'exploitation est à votre charge, pas à celle des investisseurs : chaque point de base dépensé sort de votre poche.""",
"""<p class="note">La commission de gestion vous est versée <em>à l'ouverture</em> de chaque trimestre, sur l'encours du moment : c'est votre seul revenu certain. La commission de performance et le bonus d'objectif tombent <em>à la clôture</em>, et la performance ne se déclenche qu'au-dessus du plus haut historique du fonds. En face, le budget d'exploitation et les coûts d'exécution sont à votre charge, pas à celle des investisseurs, et vous ne pouvez engager que ce que vous avez en caisse : à sec, les niveaux de budget renforcés se verrouillent et vous ne pouvez plus passer d'ordres coûteux.""")

# pop-up performance : le fonds ne paie plus les transactions
e.rep("""frais de gestion (${(VOL().mgmt*400).toFixed(1)} % par an), commission de performance (${(VOL().perf*100).toFixed(0)} % au-dessus du plus haut historique), coûts de transaction, budget d'exploitation refacturé et incidents.""",
"""frais de gestion (${(VOL().mgmt*400).toFixed(1)} % par an), commission de performance (${(VOL().perf*100).toFixed(0)} % au-dessus du plus haut historique) et incidents. Les coûts de transaction et le budget d'exploitation sont payés par votre société de gestion : ils ne pèsent pas sur cette courbe.""")
e.rep("""['Coûts de transaction cumulés','',`−${mm(S.totalTC)}`],['Budget d\\'exploitation cumulé','',`−${mm(S.totalOps)}`]""",
      """['Coûts d\\'exécution payés par vous','',`−${mm(S.totalTC)}`],['Budget d\\'exploitation payé par vous','',`−${mm(S.totalOps)}`]""")

# débriefing : la facture d'exécution quitte la cascade du fonds
e.rep("""   <div class="attr"><span class="an">Coûts de transaction</span><span class="av">${inU(o.P.tcM,UQ)}</span></div>
   <div class="attr"><span class="an">Frais de gestion et de performance</span><span class="av">${inU(o.P.feeM,UQ)}</span></div>""",
"""   <div class="attr"><span class="an">Frais de gestion et de performance</span><span class="av">${inU(o.P.feeM,UQ)}</span></div>""")
e.rep("""<summary>Détails</summary><p class="note">Encours de début de trimestre : ${moneyB(o.q0)}.""",
      """<summary>Détails</summary><p class="note">Les coûts d'exécution du trimestre (${mm(-o.P.tcM)}) n'apparaissent pas ici : ils sont à votre charge, pas à celle du fonds. Encours de début de trimestre : ${moneyB(o.q0)}.""")
e.rep(""" const UG=pickU([S.mgrQ.mgmt,S.mgrQ.perf,S.mgrQ.ops,S.mgrQ.fees-S.mgrQ.ops]);""",
      """ const UG=pickU([S.mgrQ.mgmt,S.mgrQ.perf,S.mgrQ.ops,S.mgrQ.tc||0,S.mgrQ.fees-S.mgrQ.ops]);""")
e.rep("""   <div class="attr"><span class="an">Net du trimestre</span><span class="av">${inU(S.mgrQ.fees-S.mgrQ.ops,UG)}</span></div>""",
      """   <div class="attr"><span class="an">Net du trimestre</span><span class="av">${inU(S.mgrQ.fees-S.mgrQ.ops-(S.mgrQ.tc||0),UG)}</span></div>""")
e.rep("""    ${tbl([['Commission de gestion',inU(S.mgrQ.mgmt,UG)],['Commission de performance',inU(S.mgrQ.perf,UG)],[`Budget d'exploitation (${S.budBp} pb)`,inU(-S.mgrQ.ops,UG)]])}</details>""",
"""    ${tbl([['Commission de gestion (versée à l\\'ouverture)',inU(S.mgrQ.mgmt,UG)],['Commission de performance',inU(S.mgrQ.perf,UG)],...(S.qGoal&&S.qGoal.ok?[['Bonus d\\'objectif',inU(S.qGoal.bonus,UG)]]:[]),[`Budget d'exploitation (${S.budBp} pb)`,inU(-S.mgrQ.ops,UG)],['Coûts d\\'exécution',inU(-(S.mgrQ.tc||0),UG)],['<b>Trésorerie disponible</b>',`<b>${mm(mgrCash())}</b>`]])}</details>""")

# rapport final
e.rep("""   <div class="cell"><div class="cl">Coûts de transaction payés</div><div class="cv">${moneyB(S.totalTC)}</div></div>""",
      """   <div class="cell"><div class="cl">Exécution payée de votre poche</div><div class="cv">${moneyB(S.totalTC)}</div></div>""")

# tutoriel : les sources ne s'achètent plus depuis le lot S
e.rep(""" {id:1,t:"Acheter des sources, ou s'en passer",
  h:`<p>Les rumeurs sont à vendre, et elles sont payées <em>par vous</em>, pas par le fonds : chaque achat sort de votre score. Une rumeur porte une orientation par facteur et une classe de fiabilité — faible, moyenne, forte — qui est la probabilité qu'elle soit vraie.</p>
  <p>Acheter plusieurs sources qui pointent dans le même sens vaut mieux qu'en acheter une chère : c'est l'accumulation d'indices indépendants qui déplace l'estimation, pas le prix payé. Ne rien acheter est une stratégie viable, le desk n'aura que les signaux de marché.</p>`},""",
""" {id:1,t:"Les sources, et ce qu'elles valent",
  h:`<p>Chaque trimestre un certain nombre de sources arrivent sur votre bureau : leur nombre et leur fiabilité dépendent du budget de recherche macro que vous avez fixé et de votre style. Une source porte une orientation par facteur et une classe de fiabilité — faible, moyenne, forte — qui est la probabilité qu'elle dise vrai.</p>
  <p>Plusieurs sources qui pointent dans le même sens valent mieux qu'une seule très fiable : c'est l'accumulation d'indices indépendants qui déplace l'estimation. Une <em>pré-annonce</em> concerne une dépêche qui peut tomber en cours de trimestre — ou pas.</p>`},""")
e.rep("""Les prix dépendent de la qualité de la source et de votre budget de recherche (×${[1.3,1.0,0.6][S.bud.res].toFixed(1)}). Les achats sont à votre charge de gérant.</p></details>""",
      """Le nombre de sources et leur fiabilité dépendent de votre budget de recherche macro et de votre style ; elles ne s'achètent pas à l'unité.</p></details>""")

e.done("lot 2 — textes de la nouvelle comptabilité")
