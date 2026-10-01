# Lot 138 : textes. Audit automatique des 88 rumeurs (règles par mots-clés) : une seule incohérence — le relèvement surprise
# de la BCE s'affichait « liquidité en hausse » ; sens imposé (liquidité en baisse). Six anecdotes d'exécution nouvelles,
# une ou deux par personnage peu servi (Tuco, Winnie, Sœur Marie-Alpha, Onésime), qui reprennent leurs micro-anecdotes.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("t:\"Le conseil des gouverneurs discuterait sérieusement d'un relèvement surprise\",v:[-1,1,-1,-1]","t:\"Le conseil des gouverneurs discuterait sérieusement d'un relèvement surprise\",v:[-1,1,1,-1]")
NEW=r'''
 {who:"Bartolomeo « Tuco » Ossobuco · énergie",t:"« Un cargo de café brésilien est bloqué à Santos. Le capitaine est mon cousin »",need:['KC'],p:"Tuco allume un cigare dans le bureau, malgré l'interdiction. « Un cigare par cargaison. Celle-là, j'en fume deux. »",
  ch:[{b:"Acheter avant le marché",s:"Coûts −30 % sur le café. 30 % de risque que le cousin exagère : −0,2 %.",e:{tcMultOn:['KC'],tcMult:0.7,risk:[0.3,-0.002],riskMsg:"Le cousin exagérait : le cargo est reparti le lendemain",safeTxt:"Le cargo est resté bloqué une semaine. Tuco offre des cigares à tout le desk."}},{b:"Attendre la dépêche officielle",s:"Plein tarif, Tuco éteint son cigare, vexé (débauchage +5 %).",e:{poach:0.05}}]},
 {who:"Bartolomeo « Tuco » Ossobuco · énergie",t:"« Le blé de Chicago, je le traite au fixing de Rotterdam. Ne me demandez pas comment »",need:['ZW'],p:"Il a un tableur qui s'appelle « NE PAS OUVRIR ». Il l'ouvre.",
  ch:[{b:"Faire confiance à Rotterdam",s:"Coûts −25 % sur le blé. 25 % de chances que le fixing dérape : coûts ×1,3 à la place.",e:{tcMultOn:['ZW'],tcMult:0.75,gamble:[0.25,1.3]}},{b:"Rester sur l'écran",s:"Plein tarif.",e:{}}]},
 {who:"Wing-Fat « Winnie » Leung · Asie",t:"« Hong Kong ouvre dans deux heures. Je peux placer le bitcoin avant que l'Europe se réveille »",need:['BTC'],p:"Winnie vit à l'heure de Hong Kong. Elle a trois montres, toutes réglées sur Central.",
  ch:[{b:"Laisser Winnie travailler la nuit",s:"Coûts −35 % sur le bitcoin. 30 % de risque d'une liquidation asiatique : −0,3 %.",e:{tcMultOn:['BTC'],tcMult:0.65,risk:[0.3,-0.003],riskMsg:"Une cascade de liquidations à Séoul a emporté le carnet",safeTxt:"Le carnet asiatique était profond. Winnie s'endort sur son clavier à 9 h."}},{b:"Attendre l'ouverture européenne",s:"Plein tarif. Winnie soupire en cantonais.",e:{}}]},
 {who:"Wing-Fat « Winnie » Leung · Asie",t:"« Un armateur de Singapour vend du fret au comptant. Je peux le contrer sur le Baltic Dry »",need:['BDI'],p:"« Il m'a appelée à 3 h du matin. Pour lui, il était 10 h. Pour moi aussi, d'ailleurs. »",
  ch:[{b:"Contrer l'armateur",s:"Coûts −30 % sur le Baltic Dry, comité −1 : le comité n'aime pas les ordres de nuit.",e:{tcMultOn:['BDI'],tcMult:0.7,rc:-1}},{b:"Passer par le courtier londonien",s:"Plein tarif.",e:{}}]},
 {who:"Sœur Marie-Alpha · exécution systématique",t:"« Le VIX est hors de sa loi normale depuis trois séances. Je recommande la prière, et un écart »",need:['VX'],p:"Elle prie pour la normalité des rendements. Elle prépare aussi un ordre d'arbitrage, au cas où.",
  ch:[{b:"Suivre la recommandation",s:"Coûts −20 % sur le VIX. 25 % de risque que la queue grossisse encore : −0,25 %.",e:{tcMultOn:['VX'],tcMult:0.8,risk:[0.25,-0.0025],riskMsg:"La distribution n'était pas normale : elle était pire",safeTxt:"Le VIX revient dans sa loi. Sœur Marie-Alpha se signe et range ses graphiques."}},{b:"Ne pas toucher à la volatilité",s:"Plein tarif.",e:{}}]},
 {who:"Le professeur Atterrissage · économiste en chef",t:"« Je passe sur un plateau à 7 h. Si je dis “atterrissage en douceur”, les taux longs détendent »",need:['TN','GBL'],p:"Une prévision par plateau télé. Il a déjà choisi sa cravate : celle de l'atterrissage.",
  ch:[{b:"Acheter les taux avant l'émission",s:"Coûts −25 % sur le T-Note et le Bund, comité −2 : le comité n'aime pas qu'on trade sur sa propre télé.",e:{tcMultOn:['TN','GBL'],tcMult:0.75,rc:-2}},{b:"Lui demander de rester vague",s:"Plein tarif. Le professeur est vexé (débauchage +5 %).",e:{poach:0.05}}]},'''
rep("const TRADER_EXEC=[","const TRADER_EXEC=["+NEW)
open('index.html','w',encoding='utf-8').write(s);print('lot138 p1 ok')
