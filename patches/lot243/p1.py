# Lot 243 : commentaire du résultat trimestriel varié. qVerb tirait une phrase fixe par tranche de résultat (« Votre book
# en a tiré le meilleur. » presque à chaque bon trimestre). Désormais 6 à 8 formulations par situation (vent contraire
# battu, vent favorable manqué, très bon, bon, à peine positif, légère perte, perte nette, lourde perte), tirées par
# trimestre (pk : déterministe, change d'un trimestre à l'autre), et jamais la même que le trimestre précédent.
s=open("index.html",encoding="utf-8").read()
i=s.index("function qVerb(R,q){");j=s.index("\nfunction qRegime()",i)
s=s[:i]+r'''function qVerb(R,q){
 const V={
  contre:["Votre book était du bon côté : il gagne contre le vent.","Le marché soufflait contre vous ; votre book a tenu le cap, et mieux.","À contre-courant, et c'est vous qui aviez raison ce trimestre.","Les autres ont subi le vent ; votre book l'a pris de face, et l'a battu.","Le régime ne vous était pas favorable : le résultat n'en est que plus parlant.","Mauvais temps pour tout le monde, sauf pour votre book."],
  manque:["Votre book n'en a pas profité.","Le vent était favorable ; votre book a regardé passer le train.","Un trimestre porteur, et vous étiez mal placé pour en profiter.","Les autres ont surfé la vague ; vous l'avez prise à l'envers.","Le marché offrait ce trimestre ; votre book l'a refusé.","Beau temps sur les marchés, nuages sur votre book."],
  tresbon:["Votre book en a tiré le meilleur.","Un trimestre de ceux qu'on raconte aux investisseurs.","Les paris ont payé, presque tous en même temps.","Le genre de trimestre qui justifie la commission de performance.","Vos convictions ont fait le travail ; le desk n'a plus qu'à ne rien casser.","Un trimestre propre, large, sans discussion possible.","Les chiffres parlent d'eux-mêmes : le comité n'a pas de question.","Votre book a pris ce que le marché donnait, et un peu plus."],
  bon:["Votre book termine en hausse, proprement.","Un trimestre solide, sans coup d'éclat ni frayeur.","Le travail est fait : positif, et sans drame.","Une progression régulière, de celles qui rassurent les allocataires.","Rien de spectaculaire, mais tout est allé dans le bon sens.","Le book a avancé à petits pas, mais il a avancé."],
  maigre:["Votre book termine dans le vert, sans éclat.","Positif, de justesse : le trimestre ne fera pas les gros titres.","Un trimestre à l'équilibre, qu'on retiendra surtout pour ce qu'il n'a pas coûté.","Dans le vert, à peine. Les frais ont mangé l'essentiel.","Le book a fait du surplace, du bon côté de la ligne.","Ni gain ni perte qui vaille d'être commenté."],
  leger:["Votre book y laisse un peu.","Un léger recul, rien qui change la trajectoire.","Quelques points rendus au marché, sans gravité.","Le book a reculé d'un pas ; le comité le note sans s'alarmer.","Une petite perte, du genre qu'on efface en un trimestre.","Un trimestre gris : un peu de perte, beaucoup d'attente."],
  perte:["Votre book en a fait les frais.","Le trimestre a coûté, et le comité voudra comprendre pourquoi.","Plusieurs paris ont tourné au même moment.","Une perte nette : les investisseurs liront la lettre deux fois.","Le book a encaissé ; il faudra le reconstruire.","Les convictions n'ont pas tenu face au marché."],
  lourd:["Un trimestre lourd : le book a pris la tempête de plein fouet.","La perte est sévère ; elle pèsera sur la confiance.","Tout ce qui pouvait mal tourner a mal tourné en même temps.","Un trimestre à oublier, si les investisseurs vous le permettent.","Le book a plié ; reste à savoir s'il est cassé.","Une perte qui se lit en gros caractères dans la lettre trimestrielle."]};
 const k=R&&R.wind<0&&q>0?'contre':R&&R.wind>0&&q<0?'manque':q>=0.06?'tresbon':q>=0.02?'bon':q>=0?'maigre':q>-0.02?'leger':q>-0.08?'perte':'lourd';
 const a=V[k];let t=pk(a,17);if(t===S.qVerbPrev&&a.length>1)t=a[(a.indexOf(t)+1)%a.length];
 S.qVerbPrev=t;return t}'''+s[j:]
open('index.html','w',encoding='utf-8').write(s);print('lot243 ok')
