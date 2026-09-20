# -*- coding: utf-8 -*-
"""Lot 32 — ménage des anciennes morts.

Constat (lecture du code publié, lot 31) : depuis le lot 25, la seule fin de partie est
`S.over='nav'` (encours sous 40 % du départ). `S.over` n'est jamais posé à 'dd', 'lp' ni 'rc',
mais :
  - `screenFinal` garde trois verdicts inatteignables (« Le fonds est liquidé », « Les rachats
    l'ont emporté », « Vous êtes remercié ») ;
  - la case « Comité » de la barre d'état est rendue avec `display:none` à chaque rafraîchissement,
    et sa pop-up (`showGauge('rc')`) n'est plus joignable ;
  - la barre de la jauge « Confiance » affiche `S.lp` alors que le chiffre affiché est `conf()` ;
  - six textes vus du joueur promettent encore les anciennes morts : règles (« jauge sous 8 /
    sous 4 / 28 % »), présentation (« la partie s'arrête »), pop-up Confiance (« sous 8, les
    rachats emportent le fonds »), pop-up Capital (« le fonds est liquidé »), et les deux profils
    (« liquidation à 40 % », « liquidation dès 16 % » — le seuil du flux est 13 % depuis le lot 6).
Une sauvegarde antérieure au lot 25 peut porter `S.over` à 'dd'/'lp'/'rc' : elle tombe
désormais sur le verdict d'encours, au lieu d'un verdict de réussite qui la contredirait.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
def between(a,b):
    assert e.s.count(a)==1,'debut ambigu %r'%a[:60]
    i=e.s.index(a); j=e.s.index(b,i); return e.s[i:j]

# 1. verdicts : une seule fin possible
old=between("if(S.over==='nav'){verdict=","else if(cagr>0.18")
nav=old.split("\n else if(S.over==='dd')")[0]
assert "S.over==='lp'" in old and "S.over==='rc'" in old
e.rep(old, nav.replace("if(S.over==='nav'){","if(S.over){   /* seule fin depuis le lot 25 ; couvre aussi les sauvegardes 'dd'/'lp'/'rc' */\n  ",1)+"\n ")

# 2. case Comité invisible supprimée ; barre de Confiance = conf()
old=between('<button class="tile gauge" data-gauge="rc" style="display:none">','<button class="tile gold" data-gauge="gain"')
e.rep(old,'')
e.rep('<span class="track"><i style="width:${S.lp}%;background:${gc(S.lp)}"></i></span></button>\n   <button class="tile gold"',
      '<span class="track"><i style="width:${conf()}%;background:${gc(conf())}"></i></span></button>\n   <button class="tile gold"')

# 3. pop-up Confiance : les deux composantes, les vrais seuils ; pop-up Comité (injoignable) fondue dedans
old=between("} else if(id==='lp'){","} else if(id[0]==='f'){")
new="""} else if(id==='lp'){
  const dl=S.lpD,dr=S.rcD,row=x=>[x[0],`<span class="${cls(x[1])}">${x[1]>=0?'+':'−'}${Math.abs(x[1]).toFixed(1)}</span>`];
  const pv=S.phase==='book'&&S._pv?(()=>{const nl=Math.max(0,Math.min(100,S.lp+(S._pv.lp||0))),nr=Math.max(0,Math.min(100,S.rc+(S._pv.rc||0)));
   return 0.6*Math.min(nl,nr)+0.4*(nl+nr)/2-conf()})():null;
  openModal('Confiance des investisseurs',`<p>Deux jugements en un chiffre : celui des investisseurs qui vous confient ${moneyB(S.aum0)}, et celui du comité des risques. La confiance vaut <em>0,6 × le plus sévère des deux + 0,4 × leur moyenne</em> : le plus mécontent pèse davantage.</p>
   ${tbl([['Investisseurs',Math.round(S.lp)],['Comité des risques',Math.round(S.rc)],['Confiance',`<b>${Math.round(conf())}</b>`]])}
   <p style="margin-top:10px"><b>Les investisseurs</b> suivent la performance nette, les plus hauts historiques et la surperformance face aux concurrents ; ils se détournent avec les pertes, les replis au-delà de 10 %, les incidents et une facture de frais trop lourde. Nervosité de votre profil : ×${PROF().lpMult.toFixed(2)}${S.flighty?' · passif fragile ×1,25':''}.</p>
   <p><b>Le comité</b> veut une volatilité ex-ante proche de la cible de ${(S.tgt*100).toFixed(0)} %, à ${(bandNow()*100).toFixed(0)} % près, et sanctionne les pertes au-delà de 2,2 σ ex-ante, la concentration sur un seul facteur, le book vide et les incidents. La performance achète de la patience.</p>
   <p><b>Seuils.</b> Sous <em>24</em>, l'un ou l'autre vous le fait savoir. Sous <em>20</em>, investisseurs ou comité, des rachats partent à la clôture, d'autant plus lourds que la confiance est basse. Comité sous <em>13</em> : mandat réduit à 3 unités par marché. Le fonds ne s'arrête que si l'encours tombe sous 40 % de son niveau de départ.</p>
   ${dl?tbl(dl.map(row),['Investisseurs · dernier trimestre','Δ']):'<p>Aucun trimestre bouclé pour l\\'instant.</p>'}
   ${dr?tbl(dr.map(row),['Comité · dernier trimestre','Δ']):''}
   ${pv!==null?`<p style="margin-top:10px">À la validation du book tel qu'il est : confiance <em class="${cls(pv)}">${sd1(pv)}</em> (investisseurs ${sd1(S._pv.lp||0)}, comité ${sd1(S._pv.rc||0)})${S._pv.why?' — '+S._pv.why:''}. Un book sous-investi inquiète les investisseurs autant qu'un book trop risqué inquiète le comité.</p>`:''}`);
 """
e.rep(old,new)

# 4. pop-up Capital
e.rep("""<p style="margin-top:10px">Au-delà de <em>${Math.round(ddMax()*100)} % de perte</em> depuis le pic, le fonds est liquidé.</p>""",
      """<p style="margin-top:10px">Au-delà de <em>${Math.round(ddMax()*100)} % de repli</em> depuis le pic, des investisseurs demandent leur sortie. Le fonds ne s'arrête que sous <em>${moneyB(0.4*S.aum0)}</em>, 40 % de l'encours de départ.</p>""")

# 5. présentation et règles
e.rep("""mais si les investisseurs retirent leur argent, si le comité des risques vous retire le mandat ou si le fonds perd plus de 28 %, la partie s'arrête et vous ne toucherez plus rien.""",
      """mais chaque faux pas — investisseurs ou comité à bout de patience, repli trop profond, appel de marge — fait partir de l'argent, et si l'encours tombe sous 40 % de son niveau de départ, la partie s'arrête et vous ne toucherez plus rien.""")
e.rep("""<b>Perdre</b><span>Trois façons : les investisseurs retirent tout (jauge sous <strong>8</strong>), le comité vous remercie (jauge sous <strong>4</strong>), ou le fonds perd plus de <strong>28 %</strong> depuis son plus haut (40 % pour le gérant quantitatif, 16 % pour le gérant de flux).</span>""",
      """<b>Perdre</b><span>Une seule façon : l'encours tombe sous <strong>40 %</strong> de son niveau de départ. On y arrive par les rachats, qui partent quand les investisseurs ou le comité passent sous <strong>20</strong>, ou quand le repli dépasse <strong>${Math.round(PROFILES.find(p=>p.id==='fonda').ddMax?PROFILES.find(p=>p.id==='fonda').ddMax*100:28)} %</strong> depuis le plus haut (${Math.round(PROFILES.find(p=>p.id==='syst').ddMax*100)} % pour le gérant quantitatif, ${Math.round(PROFILES.find(p=>p.id==='flux').ddMax*100)} % pour le gérant de flux). Plus la confiance est basse, plus ils sont lourds.</span>""")

# 6. profils
e.rep("""des investisseurs qui connaissent la stratégie : liquidation à 40 % de perte au lieu de 28 %""",
      """des investisseurs qui connaissent la stratégie : rachats pour repli à partir de 40 % de perte au lieu de 28 %""")
e.rep("""de l'argent rapide : liquidation dès 16 % de perte au lieu de 28 %""",
      """de l'argent rapide : rachats pour repli dès 13 % de perte au lieu de 28 %""")
# 7. multiplicateurs affichés : virgule décimale (le lot S l'avait promis, 12 affichages y échappaient)
import re
R=re.compile(r"×\$\{([^{}`]+?)\.toFixed\((\d)\)\}")
n=len(R.findall(e.s)); assert n==12,'multiplicateurs : %d'%n
e.s=R.sub(lambda m:"×${dec(%s,%s)}"%(m.group(1),m.group(2)),e.s)
e.done("lot 32 — menage des anciennes morts")
