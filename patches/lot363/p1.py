p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# bonus : minimum = (salaires FO courants ÷ 2,5 + salaires BO courants ÷ 10) % de la commission ; crans = multiplicateurs ; total ≤ 90 %
# moral : la cible suit ce que le bonus représente pour l'équipe (bonus versé / salaires du trimestre)
rep("""const BONOFF=[0,0.025,0.05,0.10,0.15,0.30],POACHP=0.5,MOT={i0:0};
function bonBase(){if(!S||!S.bud)return 0;return 5*massBp('fo')*1e-4}   /* lot 304 : masse salariale du front office */   /* lot 282 : 5 fois le coût du front office en pb, sans plafond */
function bonRate(i){return bonBase()+BONOFF[i]}""",
"""const BONOFF=[1,1.25,1.5,2,2.5,4],POACHP=0.5,MOT={i0:0};   /* lot 363 : les crans multiplient le minimum */
const BONK={fo:2.5,bo:10,max:0.9,floor:0.01,r0:0.8};
function salQ(){return (S&&S.bud)?teamBp(Math.max(5,massBp('fo')+massBp('bo')))*1e-4*budNav():0}   /* au moins 5 pb : Jean-Kevin seul a aussi un moral */   /* salaires du trimestre, inflation et locaux compris */
function bonBase(){if(!S||!S.bud)return 0;return Math.min(BONK.max,Math.max(BONK.floor,(teamBp(massBp('fo'))/BONK.fo+teamBp(massBp('bo'))/BONK.bo)/100))}   /* lot 363 */
function bonRate(i){return Math.min(BONK.max,bonBase()*BONOFF[i])}
function bonRho(i,perf){const sq=salQ();return sq>0&&perf>0?Math.min(bonRate(i)*perf,Math.max(0,mgrCash()))/sq:0}   /* bonus versé / salaires du trimestre */
function motTrho(r){return 30+65*(1-Math.exp(-Math.max(0,r)/BONK.r0))+motOff()}""")
rep("""function motT(i){return MORAL.tg[Math.max(0,Math.min(MORAL.tg.length-1,i))]+motOff()}""","""function motT(i){return motTrho(bonRho(i,(S&&S.mgrQ&&S.mgrQ.perf)||0))}   /* lot 363 : cible lue sur le bonus rapporté aux salaires */""")
rep(""" motV();motAdd(MORAL.k*(motT(S.bonEff)-S.mot),perf>0?'bonus':'pas de bonus');""",""" motV();motAdd(MORAL.k*(motTrho(perf>0&&salQ()>0?amt/salQ():0)-S.mot),perf>0?'bonus':'pas de bonus');""")
rep("""Le minimum vaut 5 fois la masse salariale de votre front office sur 100 M$ (${dec(bonBase()*100,1)} % aujourd'hui) ; chaque cran ajoute 2,5, 5, 10, 15 ou 30 points — le dernier est hors de prix. Le taux nourrit le moral du desk (${Math.round(motV())} aujourd'hui) : chaque trimestre, le moral fait la moitié du chemin vers la cible de votre taux (${MORAL.tg.join(', ')} selon le cran, plus selon vos locaux).""",
    """Le minimum suit les salaires : leurs points de base du trimestre, ÷ 2,5 pour le front office et ÷ 10 pour le back office, en % de la commission (${dec(bonBase()*100,1)} % avec votre équipe, soit ${mm(bonBase()*pf)}) ; chaque cran le multiplie par 1,25, 1,5, 2, 2,5 ou 4 — le dernier est hors de prix — sans jamais dépasser 90 % de la commission. Le moral du desk (${Math.round(motV())} aujourd'hui) fait chaque trimestre la moitié du chemin vers une cible qui dépend de ce que le bonus représente pour l'équipe : 30 sans bonus, ≈ 52 à un tiers des salaires du trimestre, ≈ 76 à un trimestre de salaire, ≈ 90 à deux, ≈ 95 à quatre, plus selon vos locaux.""")
rep("""data-i="${i}">${i===BONOFF.length-1?'🔥 ':''}${dec(p*100,Number.isInteger(Math.round(p*1000)/10)?0:1)} %<br><small>${mm(p*pf)} · moral → ${Math.round(m)} ·""",
    """data-i="${i}">${i===BONOFF.length-1?'🔥 ':''}${dec(p*100,1)} %<br><small>×${dec(BONOFF[i],2).replace(/,00$/,'')} · ${mm(p*pf)} · ${Math.round(bonRho(i,pf)*100)} % des salaires · moral → ${Math.round(m)} ·""")
rep("""il fait la moitié du chemin vers la cible de votre taux de bonus — 30 au minimum, 50 au troisième cran, 95 au cran maximal (hors de prix), le minimum sans commission de performance — relevée par vos locaux""",
    """il fait la moitié du chemin vers une cible fixée par ce que le bonus représente pour l'équipe — 30 sans bonus, ≈ 52 à un tiers des salaires du trimestre, ≈ 76 à un trimestre de salaire, ≈ 90 à deux, ≈ 95 à quatre — relevée par vos locaux""")
rep("""['Cible de votre taux et de vos locaux',""","""['Cible de votre bonus et de vos locaux',""")
open(p,'w',encoding='utf-8').write(s)
