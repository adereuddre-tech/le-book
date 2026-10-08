import math
p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
SH=0.30
D=[ # id, nom, ico, p, sigma(%/trim), description
 ('mmf','Fonds monétaire « prime »','💧',.03,.5,"Du papier commercial et des certificats de dépôt bien notés. Rarement un problème, mais un fonds de ce type a déjà « cassé le dollar »."),
 ('repo','Repo tripartite contre crédit','🔁',.12,1,"Vous prêtez du cash contre des obligations d'entreprises. Les décotes bougent souvent, rarement beaucoup."),
 ('clo','Tranches AAA de CLO','🧱',.04,1.5,"Le haut de la pile d'une titrisation de prêts aux entreprises. Le défaut est quasi impossible ; la chute de prix en crise, non."),
 ('em','Dette émergente en devise locale','🌍',.40,2,"Des emprunts d'État à haut rendement, non couverts en change. Le coupon est solide ; la devise décroche souvent, d'un coup."),
 ('secl','Prêt de titres, cash réinvesti','⛓️',.15,2.5,"Vos titres sont prêtés, le cash reçu en garantie est replacé en papier plus long et moins liquide. C'est ce qui a coulé la branche prêt de titres d'un assureur en 2008."),
 ('hy','High yield court terme','☠️',.18,3,"Des obligations sous la catégorie investissement, à moins de trois ans. Le coupon est superbe tant que personne ne fait défaut."),
 ('lev','Prêts à levier « cov-lite »','🏗️',.12,4,"Des prêts syndiqués aux rachats d'entreprises, sans clauses de protection. Taux variable, liquidité de week-end."),
 ('at1','Dette bancaire AT1 (CoCos)','🏦',.08,5,"Des obligations bancaires que le régulateur peut convertir ou effacer. Calmes pendant des années, puis une émission rayée en un week-end."),
 ('stab','Dollar synthétique crypto','🪙',.25,6,"Un dollar numérique tenu par une position de base sur les dérivés crypto. Le rendement suit le financement des perpétuels ; stable, sauf le jour où il ne l'est pas."),
]
rows=[" {id:'tres',nm:'Bons du Trésor à 3 mois',ico:'🏛️',y:0,p:0,l:0,d:\"Le taux sans risque, rien de plus, rien de moins.\"},"]
for i,n,ic,pp,sg,d in D:
    l=sg/100/math.sqrt(pp*(1-pp)); y=SH*sg/100+pp*l
    rows.append(f" {{id:'{i}',nm:'{n}',ico:'{ic}',y:{y:.5f},p:{pp},l:{l:.4f},d:\"{d}\"}},")
a=s.index("const COLL=[");b=s.index("];\n",a)+3
s=s[:a]+"""/* lot 248 : écarts-types l·√(p(1−p)) échelonnés 0 · 0,5 · 1 · 1,5 · 2 · 2,5 · 3 · 4 · 5 · 6 % par trimestre, classés ;
   Sharpe constant : surcroît net y − p·l = 0,30 × écart-type */
const COLL=[
"""+"\n".join(rows)+"\n];\n"+s[b:]
rep("/* surcroît du trimestre : ±v/2 autour de la moyenne (lot 247 : v propre au placement), tirage pur par trimestre et par placement */\nfunction colY(o){if(!o.y)return 0;const u=prng32(hash32('coly'+o.id+'_'+S.q,S.seed))();return o.y*(1+(o.v??0.7)*(u-0.5))}",
"/* lot 248 : surcroît du trimestre = moyenne ± 10 % du net attendu (y − p·l), tirage pur par trimestre et par placement :\n   le net reste positif et croît avec le risque dans 99 % des trimestres */\nfunction colY(o){if(!o.y)return 0;const u=prng32(hash32('coly'+o.id+'_'+S.q,S.seed))();return o.y+0.2*(u-0.5)*(o.y-o.p*o.l)}")
open(p,'w',encoding='utf-8').write(s)
