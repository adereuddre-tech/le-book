# Lot 237 : confiance de fin de trimestre cohérente avec la performance. La clôture jugeait la performance des positions
# HORS dépêches (« déjà comptées »), alors qu'en séance une dépêche ne peut retirer que 9 points au plus (pnlGz) : un
# trimestre à −60 % dont −89 M$ de dépêches et +17 M$ de positions finissait en hausse de confiance (91 → 100).
# Désormais : performance du trimestre tout compris (qTotal) au même barème (260 × gain, 200 × perte), moins ce que les
# dépêches ont déjà fait bouger en séance (S.qEvLp, la part « marché » de chaque dépêche) ; écart à la médiane des
# concurrents calculé sur le trimestre tout compris.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep(" S.evImmG={lp:g.lp+gn.lp,rc:g.rc+gn.rc};"," S.evImmG={lp:g.lp+gn.lp,rc:g.rc+gn.rc};S.evImmP=g.lp;   /* lot 237 : part P&L seule (sans la nervosité) */")
rep(" S.evLog.push({t:ev.t,pnl:total,m:total*navB,lp:ev0.lp+g.lp+gr.lp,rc:ev0.rc+g.rc+gr.rc});",
    " S.evLog.push({t:ev.t,pnl:total,m:total*navB,lp:ev0.lp+g.lp+gr.lp,rc:ev0.rc+g.rc+gr.rc});\n S.qEvLp=(S.qEvLp||0)+(S.evImmP||0)+g.lp+(o.gz[si].fl||0);S.evImmP=0;   /* lot 237 : part P&L de la dépêche (immédiat + suite), déjà répercutée en séance */")
rep(" const lpD=[['Performance des positions sur le trimestre (hors dépêches déjà comptées)',net>0?260*net:200*net]];",
    " const lpD=[['Performance du trimestre, tout compris',qTotal>0?260*qTotal:200*qTotal]];   /* lot 237 */\n if(Math.abs(S.qEvLp||0)>=0.05)lpD.push(['Dépêches : déjà répercutées en séance',-(S.qEvLp||0)]);")
rep(" lpD.push(['Écart à la médiane des concurrents',(net-med)*85]);"," lpD.push(['Écart à la médiane des concurrents',(qTotal-med)*85]);   /* lot 237 : tout compris */")
# remise à zéro au début du trimestre
rep("S.qReactW=0;S.qContraW=0;","S.qReactW=0;S.qContraW=0;S.qEvLp=0;")
open('index.html','w',encoding='utf-8').write(s);print('lot237 ok')
