# Lot 210 : objectifs bonus — un coup de pouce de début de partie. Deux objectifs par partie, aux trimestres 1 et 2
# seulement (plus rien ensuite). La centaine d'objectifs d'avant est remplacée par 13 objectifs choisis : liés aux
# vrais choix du joueur (réactions graduées, promesse, budget, construction du book, classement), atteignables par
# tous les styles et dans tous les univers (plus de « position sur tel marché » ni de classe d'actifs fermée).
# Nouveaux compteurs : S.qReactW (réactions à une dépêche qui ont payé), S.qContraW (dont contres).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
i=s.index('const QGOALS=[');j=s.index('\n];\n',i)+4
s=s[:i]+r'''/* lot 210 : qn = trimestre (1 : faire ses preuves, 2 : confirmer) ; pre : condition de tirage */
const QGOALS=[
 /* — trimestre 1 : faire ses preuves — */
 {qn:1,nm:"Premier coup de sonde",d:"Gagner plus de 1,5 % de l'encours sur une seule dépêche.",t:c=>c.bestEv>0.015,b:0.10},
 {qn:1,nm:"Le contre-pied gagnant",d:"Contrer une dépêche — à moitié ou au maximum — et que le retournement vous donne raison.",t:c=>(S.qContraW||0)>=1,b:0.12},
 {qn:1,nm:"Parole d'entrée",d:"Faire une annonce aux investisseurs, quelle qu'elle soit, et la tenir.",t:c=>c.comm&&c.comm!=='none'&&c.commOK,b:0.08},
 {qn:1,nm:"Le book d'architecte",d:"Finir le trimestre positif sans qu'un seul facteur porte plus du tiers du risque du book.",t:c=>c.q>0&&c.nPos>0&&c.fmax<0.34,b:0.10},
 {qn:1,nm:"Premier de la classe",d:"Faire mieux que les trois concurrents ce trimestre.",t:c=>c.beatAll,b:0.12},
 {qn:1,nm:"Le desk qui rapporte",d:"Gagner au moins trois fois ce que coûte votre équipe ce trimestre.",t:c=>c.q>0&&c.pnlM>3*c.ops*1e-4*c.navM,b:0.10},
 /* — trimestre 2 : confirmer — */
 {qn:2,nm:"La confirmation",d:"Deuxième trimestre positif d'affilée, et mieux que la médiane des concurrents.",t:c=>c.q>0&&c.prevQ>0&&c.rel>0,b:0.10,pre:'gain'},
 {qn:2,nm:"Effacer l'ardoise",d:"Après un premier trimestre négatif, ramener le fonds au-dessus de son point de départ.",t:c=>c.q>0&&S.idx>1,b:0.12,pre:'loss'},
 {qn:2,nm:"Le flair",d:"Réagir à au moins deux dépêches avec profit dans le trimestre (renforcer ou contrer, à moitié ou au maximum).",t:c=>(S.qReactW||0)>=2,b:0.10},
 {qn:2,nm:"Le relais de confiance",d:"Finir avec la confiance en hausse et une collecte nette positive.",t:c=>c.dLp>0&&c.flow>0,b:0.10},
 {qn:2,nm:"Le sniper",d:"Battre la médiane des concurrents avec six lignes ouvertes au plus.",t:c=>c.nPos>0&&c.nPos<=6&&c.rel>0,b:0.11},
 {qn:2,nm:"Main de fer",d:"Livrer l'objectif du mandat sans jamais reculer de plus de 5 % depuis le plus haut du trimestre.",t:c=>c.q>=c.goalQ&&c.dd<0.05,b:0.12},
 {qn:2,nm:"Le chasseur",d:"Gagner au moins une place au classement cumulé.",t:c=>c.rankUp>=1,b:0.10,pre:'rank2'}
];
'''+s[j:]
rep("""const gav=QGOALS.filter(g=>!S.usedGoals.includes(g.id||g.nm)&&preOk(g));
 S.goal=pick(gav.length?gav:QGOALS.filter(preOk));S.usedGoals.push(S.goal.id||S.goal.nm);""",
"""const gav=QGOALS.filter(g=>g.qn===S.q+1&&preOk(g));   /* lot 210 : trimestres 1 et 2 seulement */
 S.goal=S.q<2&&gav.length?pick(gav):null;if(S.goal)S.usedGoals.push(S.goal.id||S.goal.nm);
 S.qReactW=0;S.qContraW=0;""")
rep(" const react=resid;\n"," const react=resid;\n if(acted&&react>0){S.qReactW=(S.qReactW||0)+1;if(o.n<0)S.qContraW=(S.qContraW||0)+1}   /* lot 210 */\n")
open('index.html','w',encoding='utf-8').write(s);print('lot210 ok')
