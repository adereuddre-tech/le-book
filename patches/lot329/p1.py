p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# moral jusqu'à 100 : un sixième cran hors de prix ; effets neutres à 50, pénalités en dessous, avantages croissants jusqu'à 100
rep("""const BONOFF=[0,0.025,0.05,0.10,0.15],""","""const BONOFF=[0,0.025,0.05,0.10,0.15,0.30],""")
rep("""const BONFX=[{c:1.35,p:0.50},{c:1.17,p:0.40},{c:1.00,p:0.30},{c:0.82,p:0.20},{c:0.70,p:0.12}],BONCUT=1.5;   /* lot 223 : coûts élargis */
const BONREAD=[1.25,1.12,1,0.87,0.75],BONWIN=[-0.08,-0.04,0,0.04,0.08];   /* lot 223 : lecture des dépêches, chances des anecdotes */""",
"""/* lot 329 : effets lus sur le moral, nœuds à 0, 25, 50, 75, 100 — neutres à 50, déchaînés à 100 */
const BONFX=[{c:1.60,p:0.70},{c:1.30,p:0.45},{c:1.00,p:0.30},{c:0.75,p:0.15},{c:0.45,p:0.03}],BONCUT=1.5;
const BONREAD=[1.40,1.20,1,0.75,0.45],BONWIN=[-0.14,-0.08,0,0.08,0.20];""")
rep("""const MORAL={t0:35,dt:10,k:0.5,cut:5,egard:20,lo:20,hi:80};""","""const MORAL={tg:[30,40,50,62,75,95],k:0.5,cut:5,egard:20,lo:20,hi:80};""")
rep("""function motT(i){return MORAL.t0+MORAL.dt*i+motOff()}
function motV(){if(!S)return MORAL.t0;""","""function motT(i){return MORAL.tg[Math.max(0,Math.min(MORAL.tg.length-1,i))]+motOff()}
function motV(){if(!S)return MORAL.tg[0];""")
rep("""function motX(m){return ((m==null?motV():m)-MORAL.t0)/MORAL.dt}""","""function motX(m){return mclp(m==null?motV():m,0,100)/25}""")
rep("""const mclp=(v,a,b)=>Math.max(a,Math.min(b,v));
""","")
rep("""const MORAL={tg""","""const mclp=(v,a,b)=>Math.max(a,Math.min(b,v));
const MORAL={tg""")
rep("""function motC(m){return mclp(motI(BONFX.map(f=>f.c),motX(m)),0.55,1.6)}
function motP(m){return mclp(motI(BONFX.map(f=>f.p),motX(m)),0.03,0.7)}
function motR(m){return mclp(motI(BONREAD,motX(m)),0.6,1.4)}
function motW(m){return mclp(motI(BONWIN,motX(m)),-0.14,0.14)}""","""function motC(m){return mclp(motI(BONFX.map(f=>f.c),motX(m)),0.45,1.6)}
function motP(m){return mclp(motI(BONFX.map(f=>f.p),motX(m)),0.03,0.7)}
function motR(m){return mclp(motI(BONREAD,motX(m)),0.45,1.4)}
function motW(m){return mclp(motI(BONWIN,motX(m)),-0.14,0.20)}""")
rep("""il fait la moitié du chemin vers la cible de votre taux de bonus — 35 au minimum, 75 au cran le plus haut, sans bonus s'il n'y a pas de commission de performance — relevée par vos locaux (garage 0, yacht +13).""",
    """il fait la moitié du chemin vers la cible de votre taux de bonus — 30 au minimum, 50 au troisième cran, 95 au cran maximal (hors de prix), le minimum sans commission de performance — relevée par vos locaux (garage 0, yacht +13). À 50, tout est neutre ; en dessous, le desk coûte et lit mal ; au-dessus, il se surpasse, et à 100 il est déchaîné : coûts ×0,45, bruit de lecture ×0,45, anecdotes +20 pts, débauchage 3 %, et il refuse toutes les offres.""")
rep("""chaque cran ajoute 2,5, 5, 10 ou 15 points. Le taux nourrit le moral du desk (${Math.round(motV())} aujourd'hui) : chaque trimestre, le moral fait la moitié du chemin vers la cible de votre taux (35 au minimum, 75 au cran le plus haut, plus selon vos locaux)""",
    """chaque cran ajoute 2,5, 5, 10, 15 ou 30 points — le dernier est hors de prix. Le taux nourrit le moral du desk (${Math.round(motV())} aujourd'hui) : chaque trimestre, le moral fait la moitié du chemin vers la cible de votre taux (${MORAL.tg.join(', ')} selon le cran, plus selon vos locaux). À 50, tout est neutre ; au-dessus, les avantages s'envolent jusqu'à 100""")
rep("""data-i="${i}">${dec(p*100,Number.isInteger(Math.round(p*1000)/10)?0:1)} %<br><small>""","""data-i="${i}">${i===BONOFF.length-1?'🔥 ':''}${dec(p*100,Number.isInteger(Math.round(p*1000)/10)?0:1)} %<br><small>""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep("""  <div class="cisel">${BONOFF.map((o,i)=>{const p=bonRate(i)""","""  <div class="cisel bn6">${BONOFF.map((o,i)=>{const p=bonRate(i)""")
rep(""".cisel .bnp,.cisel .bnw{""",""".cisel.bn6{flex-wrap:wrap}.cisel.bn6 .bnp{flex:1 1 30%}
.cisel .bnp,.cisel .bnw{""")
open(p,'w',encoding='utf-8').write(s)
