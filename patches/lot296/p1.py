p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# 1. le moteur
rep("""function bonD(){try{return BONWIN[bonEff()]||0}catch(e){return 0}}""",
"""/* lot 296 : le moral du desk, un stock de 0 à 100. Il ne dépend que de l'argent et des égards :
   cible = cran de bonus effectif (35, 45 … 75) + locaux (garage −5 … yacht +8) ; la moitié de l'écart se referme
   chaque trimestre. Une baisse de taux coûte 5 points par cran, les anecdotes déplacent le moral d'un coup.
   Les quatre effets du bonus (coûts, lecture, anecdotes, débauchage) se lisent sur le moral : à cran constant,
   le moral converge vers le niveau qui redonne exactement les effets de ce cran. */
const MORAL={t0:35,dt:10,k:0.5,cut:5,egard:30,lo:20,hi:80};
function motOff(){return Math.round(-25*(offFx('poach')-1))}
function motT(i){return MORAL.t0+MORAL.dt*i+motOff()}
function motV(){if(!S)return MORAL.t0;if(S.mot==null)S.mot=motT(bonEff());return S.mot}
function motX(m){return ((m==null?motV():m)-MORAL.t0)/MORAL.dt}
function motI(A,x){const n=A.length-1;if(x<=0)return A[0]+(A[1]-A[0])*x;if(x>=n)return A[n]+(A[n]-A[n-1])*(x-n);const i=Math.floor(x),f=x-i;return A[i]+(A[i+1]-A[i])*f}
const mclp=(v,a,b)=>Math.max(a,Math.min(b,v));
function motC(m){return mclp(motI(BONFX.map(f=>f.c),motX(m)),0.55,1.6)}
function motP(m){return mclp(motI(BONFX.map(f=>f.p),motX(m)),0.03,0.7)}
function motR(m){return mclp(motI(BONREAD,motX(m)),0.6,1.4)}
function motW(m){return mclp(motI(BONWIN,motX(m)),-0.14,0.14)}
function motAdd(d,why){if(!S||!d)return;const m0=motV();S.mot=mclp(m0+d,0,100);(S.motLog=S.motLog||[]).push({q:S.q,d:S.mot-m0,why})}
/* projection du moral au prochain trimestre pour un cran donné (page du bonus) */
function motNext(i,prev){const m=motV();return mclp(m+MORAL.k*(motT(i)-m)+(prev!=null&&i<prev?MORAL.cut*(i-prev):0),0,100)}
/* seuils : au-delà de 80, le desk peut refuser toutes les offres ; en deçà de 20, partir en groupe — probabilité qui tend vers 1 aux bords */
function motLo(m){m=m==null?motV():m;return m<MORAL.lo?Math.pow((MORAL.lo-m)/MORAL.lo,2):0}
function motHi(m){m=m==null?motV():m;return m>MORAL.hi?Math.pow((m-MORAL.hi)/(100-MORAL.hi),2):0}
function bonD(){try{return motW()}catch(e){return 0}}""")
rep("""function execMot(i){return EXECM[i==null?S.bud.exec:i]*BONFX[bonEff()].c}
function poachNow(){return Math.min(0.95,BONFX[bonEff()].p*(S.bonCutQ===S.q?BONCUT:1)*offFx('poach')*(boH(12)?0.5:1))}""",
"""function execMot(i){return EXECM[i==null?S.bud.exec:i]*motC()}
function poachNow(){return Math.min(0.95,motP()*(boH(12)?0.5:1))}   /* lot 296 : locaux et baisse de taux passent par le moral */""")
# 2. le bonus nourrit le moral
rep(""" S.bonEff=perf>0?i:0;
 if(d<0)S.bonCutQ=S.q;S.bonPrev=i}""",""" S.bonEff=perf>0?i:0;
 motV();motAdd(MORAL.k*(motT(S.bonEff)-S.mot),perf>0?'bonus':'pas de bonus');if(d<0)motAdd(MORAL.cut*d,'baisse du taux');   /* lot 296 */
 if(d<0)S.bonCutQ=S.q;S.bonPrev=i}""")
# 3. lecture des dépêches et veille
rep("""b=(1.25-(BONREAD[bonEff()]||1))/0.5;""","""b=(1.25-motR())/0.5;""")
rep("""*(BONREAD[bonEff()]||1)*(here(11)?0.7:1);   /* lot 223 */""","""*motR()*(here(11)?0.7:1);   /* lot 223 ; lot 296 */""")
# 4. les égards : les anecdotes déplacent le moral (un débauchage +10 % d'autrefois = −3 points)
rep("""  if(e.poach)S.poachBoost+=e.poach;""","""  if(e.poach)motAdd(-MORAL.egard*e.poach,'égards');""",2)
# 5. débauchage et seuils
rep(""" {const pP=Math.min(0.95,Math.max(0,poachNow()+0.5*(S.poachBoost||0))),cands=[];for(let p=1;p<=S.bud.fo;p++)if(here(p)&&FOP[p].cls)cands.push(p);   /* lot 96 : débauchage de base ; lot 99 : traders seulement */
 if(!S.over&&cands.length&&rng()<pP){const boss=(pick(S.rivals.filter(x=>x.poacher))||S.rivals[S.rivals.length-1]).boss;
  {const p=(S.huntP!=null&&cands.includes(S.huntP))?S.huntP:cands[Math.floor(rng()*cands.length)];S.huntP=null;gonesL().push({p,n:1,boss});""",
""" {const pP=Math.min(0.95,Math.max(0,poachNow())),cands=[];for(let p=1;p<=S.bud.fo;p++)if(here(p)&&FOP[p].cls)cands.push(p);   /* lot 96 : débauchage de base ; lot 99 : traders seulement ; lot 296 : lu sur le moral */
 const mu=prng32(hash32('mot'+S.q,S.seed)),mHi=!S.over&&mu()<motHi(),mLo=!S.over&&!mHi&&cands.length>1&&mu()<motLo();
 if(mHi){S.execPenalty=Math.max(0.7,S.execPenalty*0.92);S.poachMsg+=` Le moral est au plus haut : le desk refuse toutes les offres des concurrents, et redouble d'efforts (coûts d'exécution −8 %).`}
 if(mLo){const boss=(pick(S.rivals.filter(x=>x.poacher))||S.rivals[S.rivals.length-1]).boss,p=cands[Math.floor(mu()*cands.length)];cands.splice(cands.indexOf(p),1);gonesL().push({p,n:1,boss});
  S.poachMsg+=` Le moral est au plus bas : ${FOP[p].full} part en entraînant un collègue, chez ${boss}.`;motAdd(-3,'départ en groupe')}
 if(!S.over&&!mHi&&cands.length&&(mLo||rng()<pP)){const boss=(pick(S.rivals.filter(x=>x.poacher))||S.rivals[S.rivals.length-1]).boss;
  {const p=(S.huntP!=null&&cands.includes(S.huntP))?S.huntP:cands[Math.floor(rng()*cands.length)];S.huntP=null;gonesL().push({p,n:1,boss});""")
open(p,'w',encoding='utf-8').write(s)
