P='/home/claude/le-book/index.html';s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:100]);s=s.replace(old,new)
# contexte : plafond courant et encours de départ du trimestre
rep("ops:S.budBp,regime:S.truth,goalQ:VOL().goal/4","ops:S.budBp,regime:S.truth,goalQ:VOL().goal/4,cap:S.maxk||3,navM:navB*1000")
# risque en trimestriel dans les libellés (prédicats inchangés, en annuel)
rep('{nm:"La main légère",d:"Garder la volatilité réalisée sous 15 %."','{nm:"La main légère",d:"Garder la volatilité réalisée sous 7,5 % par trimestre."')
rep('{nm:"Le gros calibre",d:"Terminer avec plus de 30 % de risque ex ante et un trimestre positif."','{nm:"Le gros calibre",d:"Terminer avec plus de 15 % de risque ex ante trimestriel et un trimestre positif."')
rep('{nm:"Le rendement propre",d:"Livrer l\'objectif du mandat avec une volatilité réalisée sous 15 %."','{nm:"Le rendement propre",d:"Livrer l\'objectif du mandat avec une volatilité réalisée sous 7,5 % par trimestre."')
rep('{nm:"Le ratio",d:"Livrer une performance trimestrielle supérieure à la moitié de la volatilité réalisée."','{nm:"Le ratio",d:"Livrer une performance trimestrielle supérieure à la volatilité réalisée trimestrielle."')
# comparaison en M$ de l'encours, pas d'un milliard fictif
rep("t:c=>c.pnlM>10*c.ops*1e-4*1000*(c.pnlM?1:1)&&c.q>0","t:c=>c.q>0&&c.pnlM>10*c.ops*1e-4*c.navM")
# plafonds de position : ±3 à ±5 selon les blocs — des objectifs qui ne soient pas acquis d'avance
rep('{nm:"Aucune unité extrême",d:"Terminer sans aucune position au-delà de ±3 unités.",t:c=>c.maxK<=3',
    '{nm:"Aucune unité extrême",d:"Terminer sans aucune position au-delà de ±2 unités.",t:c=>c.maxK<=2&&c.nPos>0')
rep('{nm:"Aucune position maximale",d:"Terminer sans aucune position à ±5 unités.",t:c=>c.maxK<5',
    '{nm:"Aucune position au plafond",d:"Terminer sans aucune position à votre plafond de position.",t:c=>c.maxK<c.cap&&c.nPos>0')
# régime qui n'existe pas
rep('{nm:"Surfer la tendance",d:"Terminer au-dessus de l\'objectif dans un régime de tendance.",t:c=>c.regime===\'trend\'',
    '{nm:"Surfer la reflation",d:"Terminer au-dessus de l\'objectif du mandat dans un régime de reflation.",t:c=>c.regime===\'reflation\'')
# marchés et classes : ne tirer que ce qui est ouvert
for sym in ['GC','CL','JPY','GBL']:
    rep("t:c=>c.has('%s')"%sym,"sym:'%s',t:c=>c.has('%s')"%(sym,sym))
for nm,t in [("Le taupier","Taux"),("Le cambiste","Devises"),("L'actionnaire","Actions"),("Le négociant","Matières premières"),("L'aventurier","Exotiques"),("Sans actions","Actions"),("Sans exotiques","Exotiques")]:
    rep("t:c=>c.inClass('%s')"%t, "cls:'%s',t:c=>c.inClass('%s')"%(t,t), s.count("t:c=>c.inClass('%s')"%t))
rep("preOk=g=>!g.pre||(g.pre==='never'?false:g.pre==='loss'?lastQ<0:lastQ>0);",
    "preOk=g=>(!g.sym||IDX[g.sym]!==undefined)&&(!g.cls||INSTR.some(x=>x.grp===g.cls))&&(!g.pre||(g.pre==='never'?false:g.pre==='loss'?lastQ<0:lastQ>0));   /* lot 89 : marchés et classes ouverts */")
# hauts faits
rep('nm:"Le mastodonte",d:"Terminer un mandat complet en mastodonte, univers étendu."','nm:"Le mastodonte",d:"Terminer un mandat complet en difficulté « difficile »."')
rep("tf:f=>!f.over&&f.size==='mega'&&f.univ==='ext'}","tf:f=>!f.over&&f.size==='mega'}")
rep("d:\"Terminer le cycle complet en mastodonte étendu, premier des quatre fonds, sans jamais être appelé en marge.\",tf:f=>!f.over&&f.dur==='saison'&&f.size==='mega'&&f.univ==='ext'&&f.rank===1&&!f.mc}",
    "d:\"Terminer le cycle complet de douze trimestres en difficile, premier des quatre fonds, sans jamais être appelé en marge.\",tf:f=>!f.over&&f.dur==='saison'&&f.size==='mega'&&f.rank===1&&!f.mc}")
open(P,'w',encoding='utf-8').write(s);print('ok')
