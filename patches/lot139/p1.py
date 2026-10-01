# Lot 139 : textes. Débriefing « ce qu'on en dit » démultiplié (investisseurs : ton ×5 paliers et performance ×5 paliers ;
# comité ×5 paliers) : deux variantes de plus par palier. Six anecdotes d'exécution nouvelles (Dwight, Ingrid, Boris ×2,
# Jean-Kevin ×2).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
def pre(anchor,new):   # insère des variantes juste avant une phrase existante d'un tableau
    rep(anchor,new+anchor)
# investisseurs : ton
pre('"On vous appelle par votre prénom et on vous propose des tickets sans les demander."','"Un fonds de pension canadien demande à visiter vos bureaux. Il n\'y a rien à visiter ; il insiste.","Votre lettre trimestrielle est transférée à des gens qui ne sont pas vos investisseurs, avec un mot gentil.",')
pre('"Le ton reste cordial, avec la réserve de gens qui vous prêtent beaucoup."','"On vous pose des questions par curiosité, plus par inquiétude.","Le déjeuner annuel est maintenu, le dessert aussi.",')
pre('"Les questions deviennent précises et les réponses sont relues."','"Le déjeuner annuel est devenu une visioconférence de trente minutes.","On vous demande votre « plan de continuité ». Personne n\'en parlait il y a un an.",')
pre('"Deux allocataires ont demandé les formulaires de rachat « pour information »."','"Votre interlocuteur habituel a été remplacé par quelqu\'un du service juridique.","On vous demande deux fois la date exacte de la prochaine fenêtre de liquidité.",')
pre('"Les lettres recommandées ont commencé à arriver."','"Vos investisseurs ont ouvert un groupe de discussion. Sans vous.","Le mot « transition » revient dans tous les courriels, en objet.",')
# investisseurs : performance
pre('`Un trimestre à ${sgnp(q,1)} : ils le prendront volontiers deux fois, sans y croire.`','`${sgnp(q,1)} : on vous demande, mi-sérieux, si vous acceptez encore de l\'argent.`,`${sgnp(q,1)}. Le chiffre est encadré dans le bureau d\'un allocataire. Pas le vôtre.`,')
pre("`${sgnp(q,1)} : exactement ce qu'ils ont acheté, ni plus ni moins.`","`${sgnp(q,1)} : la courbe monte au bon rythme, et personne ne vous appelle. C'est le but.`,`${sgnp(q,1)}, comme prévu. Un comité d'investissement passe à autre chose en trente secondes.`,")
pre("`${sgnp(q,1)} : positif, mais sous le mandat. Ils remarquent l'écart.`","`${sgnp(q,1)} : ils auraient fait mieux avec un fonds obligataire, et ils le savent.`,`${sgnp(q,1)}. On vous félicite d'avoir été positif, ce qui n'est jamais bon signe.`,")
pre("`${sgnp(q,1)} : une perte modérée, qu'ils acceptent si elle est expliquée.`","`${sgnp(q,1)} : ils demandent l'attribution de performance, ligne par ligne.`,`${sgnp(q,1)}. « Pas grave », disent-ils. Ils le notent quand même.`,")
pre("`${sgnp(q,1)} : le chiffre a circulé avant la lettre, sans commentaire.`","`${sgnp(q,1)} : le directeur des investissements de la caisse a appelé lui-même. Il n'appelle jamais.`,`${sgnp(q,1)}. Un journaliste vous demande un commentaire ; vos investisseurs l'ont lu avant vous.`,")
# comité
pre('"Le dossier a été expédié en dix minutes, et c\'est un compliment."','"Le comité a fini en avance et parlé de ses vacances.",')
pre('"Validé avec deux remarques de forme."','"Le rapport est validé, avec un « RAS » manuscrit en marge.",')
pre('"Un point intermédiaire est demandé le mois prochain."','"L\'inspecteur Tatillon a demandé la liste des ordres passés après 18 h.",')
pre('"Le comité a saisi le conseil d\'un « point d\'attention »."','"On vous demande de justifier chaque position supérieure à 2 % du risque. Par écrit, et signées.",')
pre('"La réduction du mandat a été mise au vote. Il manquait une voix."','"Le comité a demandé une copie de votre contrat de travail. Pour « vérifier une clause ».",')
NEW=r'''
 {who:"Dwight Tannenbaum · actions, à la voix",t:"« Un vendeur pressé sur le TOPIX. Je l'ai au téléphone, il pleure presque »",need:['TOPX'],p:"Dwight met le haut-parleur. On entend un homme expliquer que sa femme l'attend à Kyoto.",
  ch:[{b:"Le soulager de son block",s:"Coûts −35 % sur le TOPIX. 30 % de risque qu'il pleure pour une raison : −0,25 %.",e:{tcMultOn:['TOPX'],tcMult:0.65,risk:[0.3,-0.0025],riskMsg:"Il pleurait parce qu'il savait",safeTxt:"Il pleurait de soulagement. Dwight raccroche, ému."}},{b:"Lui souhaiter bon voyage",s:"Plein tarif.",e:{}}]},
 {who:"Ingrid Bergström · taux",t:"« L'adjudication du Gilt est mal couverte. Je soumissionne trois ticks sous le marché »",need:['R'],p:"Ingrid ne lève pas les yeux. « La courbe ne ment pas. Les primary dealers, si. »",
  ch:[{b:"Soumissionner",s:"Coûts −30 % sur le Gilt. 25 % de chances d'être servie au mauvais moment : coûts ×1,3 à la place.",e:{tcMultOn:['R'],tcMult:0.7,gamble:[0.25,1.3]}},{b:"Acheter sur le marché secondaire",s:"Plein tarif.",e:{}}]},
 {who:"Boris Rasoumovsky · devises",t:"« Le peso mexicain se traite mieux à Londres à 8 h qu'à New York à 9 h. Je vous montre »",need:['MXP'],p:"Boris a imprimé un graphique. Il l'a plastifié.",
  ch:[{b:"Traiter à Londres",s:"Coûts −25 % sur le peso.",e:{tcMultOn:['MXP'],tcMult:0.75}},{b:"Attendre New York",s:"Plein tarif, Boris range son graphique (débauchage +5 %).",e:{poach:0.05}}]},
 {who:"Boris Rasoumovsky · devises",t:"« Le yen fait un aller-retour de 2 % chaque fois que Tokyo déjeune. Je déjeune avec eux »",need:['JPY'],p:"Il a réglé une alarme sur 12 h 30, heure de Tokyo. Il dîne à 4 h 30 du matin.",
  ch:[{b:"Le laisser déjeuner",s:"Coûts −30 % sur le yen. 30 % de risque d'une intervention : −0,2 %.",e:{tcMultOn:['JPY'],tcMult:0.7,risk:[0.3,-0.002],riskMsg:"Le ministère des Finances est intervenu pendant le dessert",safeTxt:"Tokyo a déjeuné, le yen a fait son aller-retour, Boris aussi."}},{b:"Traiter à l'ouverture européenne",s:"Plein tarif.",e:{}}]},
 {who:"Jean-Kevin Lévêque-Charbonnier · stagiaire",t:"« J'ai codé un algorithme d'exécution ce week-end. Il s'appelle Kévin 2.0 »",need:['ESTX','GBL'],p:"Le tableur a des couleurs. Il a aussi, désormais, un bouton rouge.",
  ch:[{b:"Essayer Kévin 2.0",s:"Coûts −20 % sur l'Euro Stoxx et le Bund. 35 % de risque d'un bug : coûts ×1,4 à la place.",e:{tcMultOn:['ESTX','GBL'],tcMult:0.8,gamble:[0.35,1.4]}},{b:"Le féliciter et ne pas y toucher",s:"Plein tarif. Jean-Kevin est fier quand même.",e:{}}]},
 {who:"Jean-Kevin Lévêque-Charbonnier · stagiaire",t:"« Le courtier m'a invité à un dîner. Il m'a dit que j'avais l'étoffe d'un gérant »",need:['ES'],p:"Il porte une cravate. Il ne sait pas la nouer : c'est un clip.",
  ch:[{b:"Le laisser négocier les frais au dîner",s:"Coûts −15 % sur le S&P, comité −1 : le comité n'aime pas les dîners de courtiers.",e:{tcMultOn:['ES'],tcMult:0.85,rc:-1}},{b:"Lui rappeler la politique des cadeaux",s:"Plein tarif. Jean-Kevin rend la cravate.",e:{}}]},'''
rep("const TRADER_EXEC=[","const TRADER_EXEC=["+NEW)
open('index.html','w',encoding='utf-8').write(s);print('lot139 p1 ok')
