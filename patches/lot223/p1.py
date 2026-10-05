# Lot 223 : bonus d'équipe plus marquants, trois effets selon le cran (du plus bas au plus haut) :
# 1. coûts d'exécution ×1,35 / ×1,17 / ×1,00 / ×0,82 / ×0,70 (avant ×1,20 … ×0,80) ;
# 2. lecture des dépêches : bruit sur la probabilité lue ×1,25 / ×1,12 / ×1 / ×0,87 / ×0,75 ;
# 3. anecdotes d'exécution et de traders : chances de gagner −8 / −4 / 0 / +4 / +8 points (tirage et pastille).
import re
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("const BONFX=[{c:1.20,p:0.50},{c:1.10,p:0.40},{c:1.00,p:0.30},{c:0.88,p:0.20},{c:0.80,p:0.12}],BONCUT=1.5;",
    "const BONFX=[{c:1.35,p:0.50},{c:1.17,p:0.40},{c:1.00,p:0.30},{c:0.82,p:0.20},{c:0.70,p:0.12}],BONCUT=1.5;   /* lot 223 : coûts élargis */\nconst BONREAD=[1.25,1.12,1,0.87,0.75],BONWIN=[-0.08,-0.04,0,0.04,0.08];   /* lot 223 : lecture des dépêches, chances des anecdotes */\nfunction bonD(){try{return BONWIN[bonEff()]||0}catch(e){return 0}}\nfunction riskGood(e){const v=e.risk[1];return v>0||(v===0&&((e.riskRc||0)+(e.riskLp||0))>0)}\nfunction pAdj(p,good){return Math.max(0.02,Math.min(0.98,p+(good?1:-1)*bonD()))}")
i=s.index("function winP(e){");j=s.index("\nfunction opxChip",i)
s=s[:i]+"""function winP(e){if(!e)return null;let p=null;const mul=q=>{p=(p===null?1:p)*q};   /* lot 223 : avec l'effet du bonus d'équipe */
 if(e.gamble2){const g=e.gamble2[1]>=0,q=pAdj(e.gamble2[0],g);mul(g?q:1-q)}
 if(e.gambleLp){const g=e.gambleLp[1]>=0,q=pAdj(e.gambleLp[0],g);mul(g?q:1-q)}
 if(e.gamble)mul(1-pAdj(e.gamble[0],false));
 if(e.risk){const g=riskGood(e),q=pAdj(e.risk[0],g);mul(g?q:1-q)}
 return p}"""+s[j:]
rep("if(e.gamble&&rng()<e.gamble[0]){g=-g/2;","if(e.gamble&&rng()<pAdj(e.gamble[0],false)){g=-g/2;")
rep("if(e.gamble&&rng()<e.gamble[0]){m=e.gamble[1];","if(e.gamble&&rng()<pAdj(e.gamble[0],false)){m=e.gamble[1];")
rep("if(e.risk){if(rng()<e.risk[0]){S.nav*=(1+e.risk[1]);","if(e.risk){if(rng()<pAdj(e.risk[0],riskGood(e))){S.nav*=(1+e.risk[1]);")
rep("if(e.risk){if(rng()<e.risk[0]){pnl+=e.risk[1];","if(e.risk){if(rng()<pAdj(e.risk[0],riskGood(e))){pnl+=e.risk[1];")
rep("const win=rng()<e.gamble2[0];const r=win?e.gamble2[1]:e.gamble2[2];","const win=rng()<pAdj(e.gamble2[0],e.gamble2[1]>=0);const r=win?e.gamble2[1]:e.gamble2[2];")
rep("if(e.gambleLp){const win=rng()<e.gambleLp[0];","if(e.gambleLp){const win=rng()<pAdj(e.gambleLp[0],e.gambleLp[1]>=0);")
rep("const pr=PROF(),sd=RESPH[S.bud.res]*(pr.id==='flux'?0.6:1);","const pr=PROF(),sd=RESPH[S.bud.res]*(pr.id==='flux'?0.6:1)*(BONREAD[bonEff()]||1);   /* lot 223 */")
rep("coûts d'exécution ×${dec(BONFX[bonEff()].c,2)} (effet du seul bonus)","coûts d'exécution ×${dec(BONFX[bonEff()].c,2)} · lecture des dépêches ×${dec(BONREAD[bonEff()],2)} · chances des anecdotes ${bonD()>=0?'+':'−'}${Math.round(Math.abs(bonD())*100)} pts (effets du seul bonus)")
open('index.html','w',encoding='utf-8').write(s);print('lot223 ok')
s=open("index.html",encoding="utf-8").read()
rep("Le taux fixe deux choses, directement : un multiplicateur sur tous vos coûts d'exécution, fourchette et impact de marché compris (×1,20 au minimum, ×0,80 au cran le plus haut) et le risque de débauchage.",
    "Le taux fixe quatre choses, directement : un multiplicateur sur tous vos coûts d'exécution, fourchette et impact de marché compris (×1,35 au minimum, ×0,70 au cran le plus haut), la précision de la lecture des dépêches (bruit ×1,25 à ×0,75), les chances de gagner des anecdotes du desk (−8 à +8 points) et le risque de débauchage.")
rep("${mm(p*pf)} · coûts ×${dec(c,2)} · débauche ${Math.round(Math.min(0.95,F.p*(i<prev?BONCUT:1))*100)} %</small>",
    "${mm(p*pf)} · coûts ×${dec(c,2)} · lecture ×${dec(BONREAD[pf>0?i:0],2)} · anecdotes ${BONWIN[pf>0?i:0]>=0?'+':'−'}${Math.round(Math.abs(BONWIN[pf>0?i:0])*100)} pts · débauche ${Math.round(Math.min(0.95,F.p*(i<prev?BONCUT:1))*100)} %</small>")
open('index.html','w',encoding='utf-8').write(s);print('lot223b ok')
