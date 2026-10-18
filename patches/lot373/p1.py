p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# Fenêtres des jauges : textes justes (qui paie quoi depuis le lot 348, moral sur l'impact), plus courts, le technique replié
# Capital
rep("""<p class="note">Ce qu'un investisseur entré au premier jour a gagné ou perdu, après frais de gestion et commission de performance. Coûts de transaction et budget sont payés par votre société de gestion.</p>""",
    """<p class="note">Ce qu'un investisseur entré au premier jour a gagné ou perdu, après frais de gestion, commission de performance, fourchette et impact de vos ordres. Le courtage et le budget de l'équipe sont payés par votre société.</p>""")
rep("""<p style="margin-top:10px">Au-delà de <em>${Math.round(ddMax()*100)} % de repli</em> depuis le pic, le fonds continue : les investisseurs jugent sur leurs propres critères. Le fonds ne ferme plus sur un seuil d'encours : c'est votre société de gestion qui tient ou non. Une seule clôture en trésorerie négative, et c'est le dépôt de bilan.</p>""",
    """<p style="margin-top:10px">Un repli, même profond, ne ferme pas le fonds : ce sont vos investisseurs qui jugent, chacun sur son critère. La partie s'arrête à la première clôture en trésorerie négative, ou si les rachats vident le fonds.</p>""")
# Performance
rep("""<p>Ce qu'un investisseur entré au premier jour a gagné ou perdu, <em>après tout</em> : frais de gestion (${dec((VOL().mgmt*400),1)} % par an), commission de performance (${(perfFee()*100).toFixed(0)} % au-delà du plus haut historique relevé du taux des T-bills) et incidents. Les coûts de transaction et le budget d'exploitation sont payés par votre société de gestion : ils ne pèsent pas sur cette courbe. Le collatéral rapporte le taux au jour le jour (${dec((S.rate*100),1)} % actuellement), inclus.</p>""",
    """<p>Ce qu'un investisseur entré au premier jour a gagné ou perdu, <em>après tout</em> : frais de gestion (${dec((VOL().mgmt*400),1)} % par an), commission de performance (${(perfFee()*100).toFixed(0)} % au-delà du plus haut historique, relevé du taux des T-bills), fourchette et impact de vos ordres, incidents. Le collatéral rapporte le taux au jour le jour (${dec((S.rate*100),1)} % aujourd'hui). Le courtage et le budget de l'équipe sont payés par votre société : ils ne pèsent pas sur cette courbe.</p>""")
rep("""['Coûts d\\'exécution payés par vous','',`−${mm(S.totalTC)}`],['Budget d\\'exploitation payé par vous','',`−${mm(S.totalOps)}`]""",
    """['Fourchette et impact, payés par le fonds','',`−${mm(S.totalTC)}`],['Budget de l\\'équipe, payé par vous','',`−${mm(S.totalOps)}`]""")
# Moral
rep("""<p>Le moral de vos traders ne dépend que de l'argent et des égards. Chaque trimestre, il fait la moitié du chemin vers une cible fixée par votre cran de bonus — 30 au minimum ou sans bonus versé, puis 40, 50, 62, 75 et 95 au cran 🔥 — relevée par vos locaux (garage 0, yacht +13) ; un déménagement joue tout de suite, de l'écart entier, avant les signaux et les ordres du trimestre. À 50, tout est neutre ; en dessous, le desk coûte et lit mal ; au-dessus, il se surpasse, et à 100 il est déchaîné : coûts ×0,45, bruit de lecture ×0,35, anecdotes +25 pts, sang-froid ×0,7, débauchage 0 %, et il refuse toutes les offres. Une baisse de taux coûte 5 points par cran ; les petits gestes du quotidien (anecdotes) le déplacent d'un coup.</p>""",
    """<p>Le moral de vos traders ne dépend que de l'argent et des égards. Chaque trimestre, il fait la moitié du chemin vers sa cible : celle de votre cran de bonus (${MORAL.tg.join(', ')} ; ${MORAL.tg[0]} si aucun bonus n'est versé), plus vos locaux (garage 0 … yacht +13). À 50, tout est neutre ; en dessous, le desk coûte et lit mal ; au-dessus, il se surpasse.</p>""")
rep("""['Moral',`<b>${Math.round(m)}</b>`],['Cible de votre bonus et de vos locaux',`${Math.round(motT(S.bonI==null?MOT.i0:S.bonI))}`],["Coûts d'exécution",'×'+dec(motC(),2)]""",
    """['Moral',`<b>${Math.round(m)}</b>`],['Cible de votre bonus et de vos locaux',`${Math.round(motT(S.bonI==null?MOT.i0:S.bonI))}`],["Coûts d'impact de vos ordres",'×'+dec(motC(),2)]""")
rep("""   <p class="note">Sous ${MORAL.lo}, le desk peut partir en groupe : ${Math.round(motLo(m)*100)} % aujourd'hui, de plus en plus probable vers 0. Au-dessus de ${MORAL.hi}, il peut refuser toutes les offres des concurrents et redoubler d'efforts : ${Math.round(motHi(m)*100)} % aujourd'hui, de plus en plus probable vers 100.</p>""",
    """   <details><summary>Les règles en détail</summary><p class="note">À 100, le desk est déchaîné : impact ×0,45, bruit de lecture ×0,35, anecdotes +25 pts, sang-froid ×0,7, débauchage 0 %. À 0 : impact ×1,6, bruit ×1,8, anecdotes −25 pts, sang-froid ×1,4, débauchage 85 %. Un déménagement joue tout de suite, de l'écart entier. Une baisse du cran de bonus coûte ${MORAL.cut} points par cran ; les anecdotes le déplacent d'un coup.</p>
   <p class="note">Sous ${MORAL.lo}, le desk peut partir en groupe : ${Math.round(motLo(m)*100)} % aujourd'hui. Au-dessus de ${MORAL.hi}, il peut refuser toutes les offres des concurrents et redoubler d'efforts : ${Math.round(motHi(m)*100)} % aujourd'hui.</p></details>""")
# Comité
rep("""   <p style="margin-top:10px">Le comité ne juge que trois limites, affichées sur la page du book. Le risque ex ante et la concentration se lisent sur le book de clôture ; le stop est vérifié après chaque événement du trimestre.</p>
   <ul class="rules2">""","""   <p style="margin-top:10px">Le comité ne juge que trois limites, affichées sur la page du book : le risque ex ante et la concentration, lus sur le book de clôture, et le stop, vérifié après chaque événement.</p>
   <details><summary>Cartons et contraintes</summary><ul class="rules2">""")
rep("""<li>Quatre trimestres propres d\\'affilée retirent un jaune.</li></ul>""","""<li>Quatre trimestres propres d\\'affilée retirent un jaune.</li></ul></details>""")
# Facteur
rep("""<p>Exposition nette de votre book à ce facteur, en points de volatilité annualisée : Σ<sub>i</sub> w<sub>i</sub>σ<sub>i</sub>b<sub>ik</sub>. Positif, vous gagnez si le facteur monte. La dernière colonne donne ce que vous rapporterait un mouvement de <em>+1 σ trimestriel</em> du facteur, marché par marché.</p>""",
    """<p>Ce que votre book gagne ou perd quand ce facteur bouge. Positif, vous gagnez s'il monte. La dernière colonne donne le gain d'un mouvement de <em>+1 σ trimestriel</em> du facteur, marché par marché.</p>
   <details><summary>Le calcul</summary><p class="note">Exposition nette en points de volatilité annualisée : Σ<sub>i</sub> w<sub>i</sub>σ<sub>i</sub>b<sub>ik</sub>, où b<sub>ik</sub> est la sensibilité du marché i au facteur.</p></details>""")
# Exposition
rep("""<p class="note">L'exposition n'est pas le risque : un book brut de 4× réparti sur des marchés qui s'annulent peut être moins volatil qu'un book de 1× concentré sur un seul facteur. La jauge Risque, elle, tient compte des corrélations. Les deux se lisent ensemble — un écart important entre elles signale un book qui repose sur des compensations, et les compensations se défont dans les crises.</p>""",
    """<p class="note">L'exposition n'est pas le risque : un book brut de 4× sur des marchés qui se compensent peut être moins volatil qu'un book de 1× sur un seul facteur. La jauge Risque tient compte des corrélations. Un grand écart entre les deux signale un book qui repose sur des compensations — et elles se défont dans les crises.</p>""")
# Risque
rep("""<p>Le chiffre affiché n'est pas le σ du modèle : c'est le σ du modèle <em>majoré</em> de ce que le modèle ne voit pas encore — des corrélations réalisées qui dépassent les corrélations estimées, et la variance des dépêches qui tomberont ce trimestre.</p>""",
    """<p>Le risque affiché est la volatilité du modèle, <em>majorée</em> de ce qu'il ne voit pas encore : des corrélations qui se tendent, et les dépêches qui tomberont ce trimestre.</p>""")
rep("""   <p style="margin:12px 0 4px">D'où vient la majoration</p>
   <p class="note">La majoration""","""   <details><summary>D'où vient la majoration</summary>
   <p class="note">La majoration""")
rep("""ce chiffre ne vous dit rien de ce qui va arriver.</p>
""","""ce chiffre ne vous dit rien de ce qui va arriver.</p></details>
""")
rep("""   ${tbl([['Marge utilisée · seuil d\\'appel',`${(marginPct(S.k)*100).toFixed(0)} % · ${(MGC.thr*100).toFixed(0)} %`],['Accident de levier ce trimestre',""","""   ${tbl([['Accident de levier ce trimestre',""")
rep("""   <p style="margin:12px 0 4px">Part de la variance par facteur</p>
   ${tbl([...FACT.map((f,k)=>[f.nm,(vd.fv[k]/vd.tot*100).toFixed(0)+' %']),['Propre aux marchés',(vd.idio/vd.tot*100).toFixed(0)+' %']])}
   ${top.length?`<p style="margin:12px 0 4px">Contributeurs au risque</p>${tbl(top.map(o=>[INSTR[o.i].sym+' '+INSTR[o.i].nm,(o.v/sp*100).toFixed(0)+' %']))}`:''}`);""",
    """   ${top.length?`<p style="margin:12px 0 4px">Principaux contributeurs au risque</p>${tbl(top.map(o=>[INSTR[o.i].sym+' '+INSTR[o.i].nm,(o.v/sp*100).toFixed(0)+' %']))}`:''}
   <details><summary>Part de la variance par facteur</summary>${tbl([...FACT.map((f,k)=>[f.nm,(vd.fv[k]/vd.tot*100).toFixed(0)+' %']),['Propre aux marchés',(vd.idio/vd.tot*100).toFixed(0)+' %']])}</details>`);""")
# Trésorerie
rep("""<p>Votre société de gestion part avec un petit capital, selon la difficulté et votre style ; ensuite, sa trésorerie, ce sont vos gains nets — votre score — moins la part que vous avez placée dans le fonds, bloquée jusqu'à la clôture.</p>""",
    """<p>Votre société part avec un petit capital, selon la difficulté et votre style. Ensuite, sa trésorerie, ce sont vos gains nets — votre score — moins la part placée dans le fonds, bloquée jusqu'à la clôture.</p>""")
rep("""   <p class="note" style="margin-top:6px">À l'ouverture de chaque trimestre, après la commission de gestion, ${pc} % de votre trésorerie entre dans le fonds""","""   <details><summary>Comment marche le co-investissement</summary><p class="note" style="margin-top:6px">À l'ouverture de chaque trimestre, après la commission de gestion, ${pc} % de votre trésorerie entre dans le fonds""")
rep("""La part se choisit au débriefing, 25 % au moins.</p>""","""La part se choisit au débriefing, 25 % au moins.</p></details>""")
# Abandon
rep("""<p>Le mandat s'arrête ici. Vos commissions nettes, ${score(S.mgrFees-S.mgrCosts)}, restent les vôtres et la partie entre au palmarès.</p>""",
    """<p>Le mandat s'arrête ici. Vos gains nets, ${score(S.mgrFees-S.mgrCosts)}, restent les vôtres et la partie entre au palmarès.</p>""")
open(p,"w",encoding="utf-8").write(s)
