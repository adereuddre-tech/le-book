p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# 1. le mouvement du marché vu par le joueur = tendance du trimestre + dépêches qui l'ont touché
rep("gonesL().forEach(g=>g.n=0);S.cntBp=0;S.qSevM=0;","gonesL().forEach(g=>g.n=0);S.cntBp=0;S.qSevM=0;S.qMv={};")
rep(""" for(const sym in ev.hit){const i=IDX[sym];const r=0.5*ev.hit[sym]*INSTR[i].sigQ;imm+=w[i]*r;touched.push(i)}""",
    """ for(const sym in ev.hit){const i=IDX[sym];const r=0.5*ev.hit[sym]*INSTR[i].sigQ;imm+=w[i]*r;touched.push(i);(S.qMv=S.qMv||{})[i]=(S.qMv[i]||0)+ev.hit[sym]*INSTR[i].sigQ}   /* lot 308 : ce que les dépêches ont fait au marché */""")
# 2. résolution cohérente : réussie, le marché finit dans votre sens ; ratée, il finit contre vous ; position retournée ou soldée : sans effet
rep("""function atkResolve(){const a=S.atk;if(!a||a.q!==S.q||S.atkRes)return;const ok=prng32(hash32('atk'+S.q,S.seed))()<a.p,i=a.i,d=a.d,o=S.rBase[i],sq=INSTR[i].sigQ;
 const n=ok?d*(Math.max(0,d*o)+ATK.A*sq):o-d*ATK.back*sq;S.rBase[i]=n;const x=weights(S.k)[i]*(n-o);
 S.atkRes={ok,x,nm:INSTR[i].nm,sym:INSTR[i].sym,kind:atkKind(i,d),o,n,rev:ok&&d*o<0};if(ok)S.atkWins=(S.atkWins||0)+1}""",
"""function atkResolve(){const a=S.atk;if(!a||a.q!==S.q||S.atkRes)return;const i=a.i,d=a.d,sq=INSTR[i].sigQ,mv=(S.qMv&&S.qMv[i])||0,o=S.rBase[i],P=o+mv;
 if(d*S.k[i]<=0){S.atkRes={ok:false,vd:true,x:0,nm:INSTR[i].nm,sym:INSTR[i].sym,kind:atkKind(i,d),o:P,n:P};return}   /* lot 308 : plus de position dans le sens de la manœuvre */
 const ok=prng32(hash32('atk'+S.q,S.seed))()<a.p,P2=ok?d*(Math.max(0,d*P)+ATK.A*sq):d*Math.min(d*P-ATK.back*sq,-ATK.back*sq),n=P2-mv;   /* lot 308 : ratée, le marché finit contre vous */
 S.rBase[i]=n;const x=weights(S.k)[i]*(n-o);
 S.atkRes={ok,x,nm:INSTR[i].nm,sym:INSTR[i].sym,kind:atkKind(i,d),o:P,n:P2,rev:(ok?d*P<0:d*P>0)};if(ok)S.atkWins=(S.atkWins||0)+1}""")
rep("""  <p>${R.ok?(R.rev?`Le marché partait contre vous (${sgn(R.o,1)}) : votre manœuvre le retourne, il finit à ${sgn(R.n,1)}.`:`Le marché allait déjà dans votre sens : votre manœuvre l'emballe, il finit à ${sgn(R.n,1)} au lieu de ${sgn(R.o,1)}.`):`Les contreparties ont tenu, et elles vous font payer l'audace : ${R.sym} finit à ${sgn(R.n,1)} au lieu de ${sgn(R.o,1)}.`}</p>""",
"""  <p>${R.vd?`Votre position sur ${R.sym} n'est plus dans le sens de la manœuvre : elle tombe à plat, le marché finit à ${sgn(R.n,1)}.`:R.ok?(R.rev?`Le marché partait contre vous (${sgn(R.o,1)} sur le trimestre, dépêches comprises) : votre manœuvre le retourne, il finit à ${sgn(R.n,1)}.`:`Le marché allait déjà dans votre sens : votre manœuvre l'emballe, il finit à ${sgn(R.n,1)} au lieu de ${sgn(R.o,1)} (dépêches comprises).`):(R.rev?`Les contreparties ont tenu et retournent le marché contre vous : ${R.sym} finit à ${sgn(R.n,1)} au lieu de ${sgn(R.o,1)} (dépêches comprises).`:`Les contreparties ont tenu et enfoncent le clou : ${R.sym} finit à ${sgn(R.n,1)} au lieu de ${sgn(R.o,1)} (dépêches comprises).`)}</p>""")
rep(""" document.getElementById('ok').onclick=()=>{stepEvents();window.scrollTo(0,0)}}
function atkClose()""",""" document.getElementById('ok').onclick=()=>{stepEvents();window.scrollTo(0,0)}}
function atkLocked(i){return !!(S&&S.atk&&S.atk.q===S.q&&S.atk.i===i)}
function atkClose()""")
# 3. la ligne de la manœuvre est verrouillée jusqu'aux ordres
rep("""   const i=+b.dataset.i,v=+b.dataset.v;
   const k1=S.k[i],sp0=pvol(weights(S.k)),c0=liveTC();""","""   const i=+b.dataset.i,v=+b.dataset.v;
   if(atkLocked(i)){toast('🦅 Ligne de la manœuvre : verrouillée ce trimestre.');return}   /* lot 308 */
   const k1=S.k[i],sp0=pvol(weights(S.k)),c0=liveTC();""")
rep("""function commitOrders(){
 S.kVal=[...S.k];""","""function commitOrders(){
 if(S.atk&&S.atk.q===S.q)S.k[S.atk.i]=S.atk.d*S.atk.m;   /* lot 308 : la manœuvre impose sa ligne, quoi qu'aient fait les boutons du book */
 S.kVal=[...S.k];""")
rep("""La ligne remplace votre position actuelle sur ${INSTR[i].sym} ; le comité apprend la manœuvre (contrôle −2).""","""La ligne remplace votre position actuelle sur ${INSTR[i].sym} et reste verrouillée jusqu'à la clôture ; réussie, le marché finit dans votre sens, ratée, il finit contre vous. Le comité apprend la manœuvre (contrôle −2).""")
open(p,'w',encoding='utf-8').write(s)
