# Lot 101b : le back office amortit le choc immédiat des scénarios (TAILM : ×0,75 à Pare-Feu, ×1,75 au loyer seul) ;
# textes : plus d'« accidents de levier » pour le joueur ; zone rouge du nuage retirée ; hauts faits et objectifs
# qui les citaient portent sur les scénarios de stress (S.tails les enregistre).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep(" const navB=S.nav;S.nav*=(1+imm);S.qEvM+=imm*navB;"," if(ev.stress){imm*=0.5+0.5*(TAILM[S.bud.risk]||1);(S.tails=S.tails||[]).push({q:S.q,t:ev.t,f:-imm,id:'stress'})}   /* lot 101 : le back office amortit le choc */\n const navB=S.nav;S.nav*=(1+imm);S.qEvM+=imm*navB;")
rep("Le loyer seul, c'est la catastrophe : incidents en série, accidents de levier. Au-dessus, chaque poste réduit nettement la fréquence et la gravité des incidents et les accidents de levier, jusqu'à les diviser par deux au dernier cran, et rassure le comité.",
    "Le loyer seul, c'est la catastrophe : incidents en série, chocs de stress encaissés de plein fouet. Au-dessus, chaque poste réduit nettement la fréquence et la gravité des incidents et amortit le choc immédiat des scénarios de stress, et rassure le comité.")
rep(" · accidents de levier ×${dec(TAILM[i],2)}"," · choc de stress ×${dec(0.5+0.5*TAILM[i],2)}")
rep("<b>Accidents de levier</b> et appels de marge ×${dec(TAILM[i],2)}.","<b>Choc immédiat des scénarios de stress</b> ×${dec(0.5+0.5*TAILM[i],2)}.")
rep("Traverser le trimestre sans appel de marge ni accident de levier,","Traverser le trimestre sans appel de marge ni scénario de stress,")
rep("Finir positif sans incident opérationnel ni accident de levier.","Finir positif sans incident opérationnel ni scénario de stress.")
rep('nm:"Dompter le levier",d:"Finir un trimestre positif malgré un accident de levier."','nm:"Dompter la tempête",d:"Finir un trimestre positif malgré un scénario de stress."')
rep("Au-delà de <strong>25 %</strong> de risque ex ante, des <strong>accidents de levier</strong> deviennent possibles — krach éclair, trader non autorisé, erreur système, marges relevées — et d'autant plus graves que le book est gros. S'en sortir coûte très cher.",
    "Le prime broker vérifie la <strong>marge</strong> après chaque événement : au-delà de 50 % de l'encours, appel de marge. Des <strong>scénarios de stress</strong> — krach, choc de taux, flambée du dollar, choc pétrolier, assèchement de liquidité, rallye de soulagement — peuvent frapper chaque trimestre ; le book affiche ce que chacun vous coûterait.")
rep("['Accidents de levier et appels de marge',`au-delà de ${dec(TAIL.x0*50,0)} % de risque ex ante`]","['Appel de marge',`au-delà de ${Math.round(MGC.thr*100)} % de marge utilisée, vérifiée après chaque événement`]")
rep("Le risque se paie autrement, par les accidents de levier.","Le risque se paie autrement : appels de marge et scénarios de stress.")
rep("; au-delà de 10 % de risque, la zone rouge est celle des accidents de levier.",".")
rep("sa jauge passe à l'ambre à la cible de votre mandat et au rouge là où commencent les accidents de levier.","sa jauge passe à l'ambre puis au rouge à mesure qu'il monte.")
rep("ni le drain de volatilité ni les accidents de levier, qui dépendent du risque et se lisent sur l'axe horizon","ni le drain de volatilité ni les scénarios de stress, qui dépendent du risque et se lisent sur l'axe horizon")
i=s.find("if(TAIL.x0/2<xm)g+=`<rect");j=s.find("accidents de levier</text>`;",i);assert i>0 and j>i
s=s[:i]+s[j+len("accidents de levier</text>`;"):]
open('index.html','w',encoding='utf-8').write(s);print('ok')
