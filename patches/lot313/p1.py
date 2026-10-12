p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
a=s.index("const TIPS=[");b=s.index("const TIPP=0.35;",a)
NEW=r"""const TIPS=[   /* lot 313 : chaque type garde son coût, son gain et sa chance ; v = variantes de présentation */
 {id:'spec',nm:"Special situations",ic:'🎯',c:0.010,g:0.050,p:1/3,d:"Une scission de conglomérat que le marché n'a pas encore lue. Le desk du prime broker a fait le travail ; il vous ouvre l'allocation.",v:[
  ["Scission d'un conglomérat coréen","La filiale de batteries sort de la maison mère ; les fonds indiciels devront vendre la mère et acheter la fille le même jour."],
  ["Sortie d'indice forcée","Un groupe chinois quitte l'indice mondial : 4 milliards de ventes mécaniques à la clôture, puis plus personne."],
  ["Holding décotée","Porsche SE cote 50 % sous la valeur de ce qu'elle détient. Un activiste vient d'entrer au capital."],
  ["Rachat d'actions géant","Un fabricant de puces annonce 20 milliards de rachats. Le prime broker a une allocation sur le bloc d'exécution."],
  ["Restructuration d'une foncière","Une foncière allemande vend ses immeubles un par un ; chaque vente se fait au-dessus de la valeur affichée."]]},
 {id:'dist',nm:"Dette en détresse",ic:'🏚️',c:0.015,g:0.060,p:0.35,d:"Des obligations d'un distributeur en restructuration, à 22 centimes. Si le plan passe, elles repartent vers 60.",v:[
  ["Bonos argentins","Ils cotent 28 centimes avant l'élection. Un candidat promet de payer ; l'autre de tout renégocier."],
  ["Obligations d'un promoteur chinois","À 3 centimes. Le tribunal de Hong Kong statue sur la liquidation dans six semaines."],
  ["Dette zambienne","L'accord avec les créanciers chinois est « imminent » depuis dix-huit mois. Cette fois, le cuivre aide."],
  ["Eurobonds libanais","À 6 centimes, en défaut depuis 2020. Un plan du FMI circule ; le prime broker en a vu une copie."],
  ["Obligations d'un loueur de voitures","En faillite, mais les voitures d'occasion se vendent plus cher que neuves. Les créanciers pourraient être remboursés à 100."],
  ["Dette vénézuélienne","À 10 centimes. Une rumeur de levée des sanctions pétrolières, une de plus."]]},
 {id:'ma',nm:"Arbitrage de fusion",ic:'🤝',c:0.005,g:0.015,p:0.60,d:"Une OPA amicale, l'écart de prix reste large : le marché doute de l'autorisation de la concurrence.",v:[
  ["Fusion de deux sidérurgistes","Bruxelles a ouvert une enquête approfondie ; l'écart est à 12 %. Les remèdes proposés suffiront-ils ?"],
  ["OPA sur un éditeur de jeux vidéo","Le régulateur britannique a déjà dit non une fois. L'acheteur revient avec un remède sur le cloud."],
  ["Rachat d'un laboratoire par un géant pharmaceutique","Autorisation américaine en attente ; l'écart rémunère 20 % l'an si tout passe."],
  ["Offre sur un fabricant de puces","Pékin doit donner son accord. Il ne l'a jamais refusé ouvertement — il l'a laissé expirer."],
  ["Fusion de deux banques régionales","Les syndicats menacent, le gouvernement a une action de préférence. L'écart reste à 9 %."]]},
 {id:'dual',nm:"Double cotation",ic:'🔀',c:0.004,g:0.012,p:0.55,d:"La même action cote à deux places avec un écart anormal ; le prime broker prête les titres pour le jouer.",v:[
  ["Actions A et H d'une banque chinoise","Les actions de Shanghai cotent 40 % au-dessus de celles de Hong Kong. La passerelle de Stock Connect rouvre lundi."],
  ["Unilever, Londres contre Amsterdam","L'unification des deux lignes est annoncée ; l'écart doit se fermer à la date de conversion."],
  ["Certificats de dépôt d'un fondeur taïwanais","Le certificat new-yorkais vaut 18 % de plus que l'action de Taipei. Les quotas de conversion s'ouvrent."],
  ["Action ordinaire et préférentielle","La préférentielle sans droit de vote cote 25 % sous l'ordinaire ; la famille veut fusionner les deux."]]},
 {id:'ipo',nm:"Introduction en bourse",ic:'🔔',c:0.008,g:0.040,p:0.30,d:"Une allocation dans une introduction très demandée. Premier jour glorieux, ou retrait du dossier.",v:[
  ["Une licorne de l'intelligence artificielle","Le carnet est sursouscrit 30 fois ; la banque vous réserve une ligne parce que vous ne revendez pas le premier jour."],
  ["Le géant saoudien du pétrole","1 % du capital mis en vente, le fonds souverain soutient le cours. Les étrangers boudent."],
  ["Un fabricant de puces britannique","Retour en bourse après six ans en mains japonaises ; 10 % de flottant seulement."],
  ["Une plateforme de paiement chinoise","La plus grosse introduction de l'histoire, si Pékin ne la suspend pas la veille — c'est déjà arrivé."],
  ["Un champion indien du commerce en ligne","Les particuliers indiens ont réservé 60 fois l'offre. Le premier jour sera une fête, ou une émeute."]]},
 {id:'adj',nm:"Adjudication souveraine",ic:'🏦',c:0.003,g:0.009,p:0.50,d:"Une adjudication du Trésor s'annonce mal couverte ; le prime broker vous propose d'y soumissionner sous le marché.",v:[
  ["Adjudication de BTP italiens à 30 ans","Rome émet 8 milliards la semaine du budget ; les primary dealers sont pleins."],
  ["JGB à 30 ans","La Banque du Japon réduit ses achats ; la dernière adjudication à 30 ans a été la plus mal couverte depuis 1987."],
  ["Gilts indexés","Les fonds de pension britanniques reviennent ; le Trésor double la taille de l'émission."],
  ["Bons du Trésor américain à 20 ans","La maturité que personne n'aime : la dernière adjudication s'est faite 4 points de base au-dessus du marché."]]},
 {id:'adjc',nm:"Adjudication de crédit souverain",ic:'🧾',c:0.006,g:0.022,p:0.40,d:"Une émission d'un souverain émergent, prime d'émission généreuse si la demande suit.",v:[
  ["Eurobond égyptien","Le Caire sort 2 milliards à 10 ans, trois semaines après un accord avec le FMI."],
  ["Retour du Ghana sur les marchés","Première émission depuis le défaut ; la prime d'émission est de 150 points de base."],
  ["Obligations turques en dollars","Ankara profite d'une fenêtre ; les réserves nettes sont redevenues positives, disent-ils."],
  ["Émission verte du Nigeria","Le premier « green bond » du pays, sursouscrit si les fonds ESG suivent."],
  ["Panda bond hongrois","Budapest emprunte en yuans à Pékin ; Bruxelles fronce les sourcils, le carnet se remplit."]]},
 {id:'phys',nm:"Cargaison physique",ic:'🚢',c:0.008,g:0.030,p:0.35,d:"Un négociant vous propose une cargaison physique à livrer en fin de trimestre.",v:[
  ["Fèves de cacao ivoiriennes","Un cargo de 20 000 tonnes, livrable à Anvers. Les stocks certifiés de Londres sont au plus bas depuis vingt ans."],
  ["Nickel au LME","Un lot de cathodes dans un entrepôt de Rotterdam. Les sacs, cette fois, ne contiennent pas de pierres."],
  ["Jus d'orange concentré","Des fûts congelés en Floride, juste avant la saison des ouragans."],
  ["Uranium","Un fonds physique vend une partie de son stock ; une centrale japonaise redémarre le mois prochain."],
  ["Vanille de Madagascar","Une récolte entière, avant le cyclone annoncé."]]},
 {id:'bloc',nm:"Bloc d'actions",ic:'📦',c:0.006,g:0.020,p:0.45,d:"Un vendeur pressé cède un bloc avec décote, après la clôture.",v:[
  ["Bloc d'une banque, vendu par l'État","L'État cède 5 % du capital avec 4 % de décote. Il en reste 20 % à vendre d'ici l'été."],
  ["Bloc d'un fondateur","Le fondateur d'un groupe de luxe vend pour payer ses impôts. Décote de 6 %."],
  ["Ligne d'un family office en liquidation","Un family office à crédit total doit tout vendre avant l'ouverture. Les banques se disputent les blocs."],
  ["Participation d'un fonds de capital-investissement","Sortie d'un fonds de LBO, troisième placement de l'année ; le marché commence à le savoir."]]},
 {id:'conv',nm:"Obligation convertible",ic:'🔁',c:0.005,g:0.016,p:0.50,d:"Une convertible cotée sous sa valeur théorique ; le prime broker prête l'action pour la couvrir.",v:[
  ["Convertible d'un producteur de bitcoin","Elle cote sous son plancher obligataire. La société lève pour acheter encore du bitcoin."],
  ["Convertible d'un constructeur de voitures électriques","Volatilité implicite à 35 %, réalisée à 60 %. Le desk dit que c'est de l'argent gratuit."],
  ["Convertible d'une compagnie de croisières","Remboursable dans dix-huit mois, les réservations reviennent. Les vendeurs sont des fonds en rachat."],
  ["CoCo d'une banque européenne","9 % de coupon ; le souvenir d'une banque suisse dont les CoCos avaient été effacées pèse encore."]]},
 {id:'cat',nm:"Obligation catastrophe",ic:'🌀',c:0.007,g:0.025,p:0.40,d:"Une obligation catastrophe proposée avant la saison à risque.",v:[
  ["Ouragans en Floride","Le capital disparaît si un ouragan de catégorie 5 frappe Miami. Sinon, 14 % de coupon."],
  ["Séisme au Japon","Un tremblement de terre de magnitude 8 à Tokyo efface l'émission. Le coupon est à 9 %."],
  ["Tempêtes en Europe","La réassurance a doublé ses prix ; l'émission est à moitié vide à deux jours de la clôture."],
  ["Pandémie","La Banque mondiale émet de nouveau ; la dernière fois, le déclencheur avait fait débat."]]},
 {id:'curio',nm:"Actif de collection",ic:'🏺',c:0.006,g:0.022,p:0.40,d:"Un actif réel, hors des marchés cotés, que le prime broker finance à crédit.",v:[
  ["Cave de grands crus de Bordeaux","Un négociant en difficulté solde ses millésimes 2010 ; l'indice Liv-ex cherche un plancher."],
  ["Montres de collection","Une collection d'acier vendue en un lot ; les listes d'attente fondent, les enchères reprennent."],
  ["Meules de parmesan","Une banque d'Émilie vend des meules gagées ; affinage de 36 mois garanti."],
  ["Art contemporain","Une succession new-yorkaise vend avant la grande vente de mai ; l'estimation est prudente."],
  ["Cartes à collectionner","Une collection de cartes de 1999, notées 10/10. Un fonds spécialisé veut entrer."]]}];
"""
s=s[:a]+NEW+s[b:]
rep("""function tipDraw(){const u=prng32(hash32('tip'+S.q,S.seed));if(u()>=TIPP)return null;const t=TIPS[Math.floor(u()*TIPS.length)];const win=u()<t.p,rj=Math.floor(u()*S.rivals.length);return {t,win,rj}}""",
    """function tipDraw(){const u=prng32(hash32('tip'+S.q,S.seed));if(u()>=TIPP)return null;const t=TIPS[Math.floor(u()*TIPS.length)];const win=u()<t.p,rj=Math.floor(u()*S.rivals.length),vv=t.v&&t.v.length?t.v[Math.floor(prng32(hash32('tipv'+S.q,S.seed))()*t.v.length)]:null;return {t,win,rj,vv}}""")
rep("""function screenTip(){S.tipQ=S.q;const D=tipDraw();if(!D){screenExec();return}const {t,win,rj}=D,rv=S.rivals[rj];""",
    """function screenTip(){S.tipQ=S.q;const D=tipDraw();if(!D){screenExec();return}const {t,win,rj,vv}=D,rv=S.rivals[rj];""")
rep("""<h3>${t.ic} ${t.nm}</h3><p>${t.d}</p>""","""<h3>${t.ic} ${vv?vv[0]:t.nm}</h3>${vv?`<p class="note" style="margin:0 0 6px">${t.nm}</p>`:''}<p>${vv?vv[1]:t.d}</p>""")
open(p,'w',encoding='utf-8').write(s)
