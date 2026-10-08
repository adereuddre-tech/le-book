import re
p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
a=s.index("const COLL=[\n");b=s.index("];\n",a)+3
s=s[:a]+"""const COLL=[   /* lot 247 : profils variés (fréquent et léger, rare et lourd), dispersion v du surcroît, net y−p·l relevé */
 {id:'tres',nm:'Bons du Trésor à 3 mois',ico:'🏛️',y:0,p:0,l:0,v:0,d:"Le taux sans risque, rien de plus, rien de moins."},
 {id:'mmf',nm:'Fonds monétaire « prime »',ico:'💧',y:0.0035,p:0.03,l:0.03,v:0.2,d:"Du papier commercial et des certificats de dépôt bien notés. Rarement un problème, mais un fonds de ce type a déjà « cassé le dollar »."},
 {id:'repo',nm:'Repo tripartite contre crédit',ico:'🔁',y:0.0075,p:0.12,l:0.025,v:0.3,d:"Vous prêtez du cash contre des obligations d'entreprises. Les décotes bougent souvent, rarement beaucoup."},
 {id:'clo',nm:'Tranches AAA de CLO',ico:'🧱',y:0.012,p:0.04,l:0.10,v:0.3,d:"Le haut de la pile d'une titrisation de prêts aux entreprises. Le défaut est quasi impossible ; la chute de prix en crise, non."},
 {id:'secl',nm:'Prêt de titres, cash réinvesti',ico:'⛓️',y:0.020,p:0.15,l:0.07,v:0.5,d:"Vos titres sont prêtés, le cash reçu en garantie est replacé en papier plus long et moins liquide. C'est ce qui a coulé la branche prêt de titres d'un assureur en 2008."},
 {id:'em',nm:'Dette émergente en devise locale',ico:'🌍',y:0.030,p:0.40,l:0.045,v:0.9,d:"Des emprunts d'État à haut rendement, non couverts en change. Le coupon est solide ; la devise décroche souvent, d'un coup."},
 {id:'hy',nm:'High yield court terme',ico:'☠️',y:0.040,p:0.18,l:0.14,v:0.5,d:"Des obligations sous la catégorie investissement, à moins de trois ans. Le coupon est superbe tant que personne ne fait défaut."},
 {id:'lev',nm:'Prêts à levier « cov-lite »',ico:'🏗️',y:0.048,p:0.12,l:0.27,v:0.4,d:"Des prêts syndiqués aux rachats d'entreprises, sans clauses de protection. Taux variable, liquidité de week-end."},
 {id:'at1',nm:'Dette bancaire AT1 (CoCos)',ico:'🏦',y:0.050,p:0.08,l:0.40,v:0.3,d:"Des obligations bancaires convertibles en actions ou effaçables par le régulateur. Calme pendant des années, puis remises à zéro en un week-end."},
 {id:'stab',nm:'Dollar synthétique crypto',ico:'🪙',y:0.085,p:0.25,l:0.272,v:1.0,d:"Un dollar numérique tenu par une position de base sur les dérivés crypto. Le rendement suit le financement des perpétuels ; stable, sauf le jour où il ne l'est pas."},
];
"""+s[b:]
rep("/* surcroît du trimestre : ±35 % autour de la moyenne, tirage pur par trimestre et par placement */\nfunction colY(o){if(!o.y)return 0;const u=prng32(hash32('coly'+o.id+'_'+S.q,S.seed))();return o.y*(1+0.7*(u-0.5))}",
"/* surcroît du trimestre : ±v/2 autour de la moyenne (lot 247 : v propre au placement), tirage pur par trimestre et par placement */\nfunction colY(o){if(!o.y)return 0;const u=prng32(hash32('coly'+o.id+'_'+S.q,S.seed))();return o.y*(1+(o.v??0.7)*(u-0.5))}")
open(p,'w',encoding='utf-8').write(s)
