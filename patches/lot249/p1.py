import math
p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
SH=0.35
def pr(l,sg):  # probabilité (< 1/2) donnant l'écart-type sg pour une perte l
    q=(sg/l)**2;return (1-math.sqrt(1-4*q))/2
D=[ # id, nom, ico, p, perte (None = déduite de σ), σ (%/trim), description
 ('mmf','Commercial paper (A-1/P-1)','💧',.03,None,.5,"Des billets de trésorerie d'entreprises de premier rang, à quelques semaines. Rarement un problème, mais un émetteur a déjà fait défaut du jour au lendemain."),
 ('repo','Tri-party repo (credit collateral)','🔁',.12,None,1,"Vous prêtez du cash contre des obligations d'entreprises. Les décotes bougent souvent, rarement beaucoup."),
 ('clo','AAA CLO tranches','🧱',.04,None,1.5,"Le haut de la pile d'une titrisation de prêts aux entreprises. Le défaut est quasi impossible ; la chute de prix en crise, non."),
 ('em','Local-currency EM debt','🌍',.40,None,2,"Des emprunts d'État à haut rendement, non couverts en change. Le coupon est solide ; la devise décroche souvent, d'un coup."),
 ('secl','Sec-lending cash reinvestment','⛓️',.15,None,2.5,"Vos titres sont prêtés, le cash reçu en garantie est replacé en papier plus long et moins liquide. C'est ce qui a coulé la branche prêt de titres d'un assureur en 2008."),
 ('hy','Short-duration high yield','☠️',.18,None,3,"Des obligations sous la catégorie investissement, à moins de trois ans. Le coupon est superbe tant que personne ne fait défaut."),
 ('lev','Cov-lite leveraged loans','🏗️',None,.08,3.5,"Des prêts syndiqués aux rachats d'entreprises, sans clauses de protection. Taux variable, liquidité de week-end."),
 ('at1','Bank AT1 CoCos','🏦',None,.09,4,"Des obligations bancaires que le régulateur peut convertir ou effacer. Le marché les solde à la moindre rumeur sur une banque."),
 ('stab','Synthetic dollar (crypto basis)','🪙',None,.10,4.5,"Un dollar numérique tenu par une position de base sur les dérivés crypto. Le rendement suit le financement des perpétuels ; stable, sauf le jour où il ne l'est pas."),
]
rows=[" {id:'tres',nm:'3-month T-bills',ico:'🏛️',y:0,p:0,l:0,d:\"Le taux sans risque, rien de plus, rien de moins.\"},"]
for i,n,ic,pp,l,sg,d in D:
    if l is None: l=sg/100/math.sqrt(pp*(1-pp))
    else: pp=round(pr(l,sg/100),4)
    y=SH*sg/100+pp*l
    rows.append(f" {{id:'{i}',nm:'{n}',ico:'{ic}',y:{y:.5f},p:{pp},l:{l:.4f},d:\"{d}\"}},")
a=s.index("/* lot 248 : écarts-types");b=s.index("];\n",a)+3
s=s[:a]+"""/* lot 249 : écarts-types l·√(p(1−p)) de 0 à 4,5 % par trimestre, pas de 0,5, classés ; pertes des trois
   derniers entre 8 et 10 %, probabilités déduites ; Sharpe constant : surcroît net y − p·l = 0,35 × écart-type */
const COLL=[
"""+"\n".join(rows)+"\n];\n"+s[b:]
rep("/* lot 248 : surcroît du trimestre = moyenne ± 10 % du net attendu (y − p·l), tirage pur par trimestre et par placement :\n   le net reste positif et croît avec le risque dans 99 % des trimestres */\nfunction colY(o){if(!o.y)return 0;const u=prng32(hash32('coly'+o.id+'_'+S.q,S.seed))();return o.y+0.2*(u-0.5)*(o.y-o.p*o.l)}",
"/* lot 249 : surcroît du trimestre = moyenne ± 8 % du net attendu (y − p·l), tirage pur par trimestre et par placement :\n   le net reste positif et croît avec le risque sur toute l'échelle dans 95 % des trimestres */\nfunction colY(o){if(!o.y)return 0;const u=prng32(hash32('coly'+o.id+'_'+S.q,S.seed))();return o.y+0.16*(u-0.5)*(o.y-o.p*o.l)}")
open(p,'w',encoding='utf-8').write(s)
