# Lot 200 : anecdotes — les chances de gagner en pourcentage. Chaque choix à issue aléatoire affiche une pastille
# « chances de gagner NN % », calculée sur ses effets (winP) : gain tiré avec la probabilité p (gamble2, gambleLp,
# risk positif) → p ; perte tirée avec la probabilité p (risk négatif, gamble de coûts) → 1 − p ; plusieurs tirages → produit.
# Les rares textes sans pourcentage (« une fois sur trois », « 50/50 », « risque divisé par deux », « risque réduit ») sont chiffrés.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("function fxTxt(s,x){",
"""/* lot 200 : probabilité de gagner un choix à issue aléatoire (null si rien n'est tiré au sort) */
function winP(e){if(!e)return null;let p=null;const mul=q=>{p=(p===null?1:p)*q};
 if(e.gamble2)mul(e.gamble2[1]>=0?e.gamble2[0]:1-e.gamble2[0]);
 if(e.gambleLp)mul(e.gambleLp[1]>=0?e.gambleLp[0]:1-e.gambleLp[0]);
 if(e.gamble)mul(1-e.gamble[0]);
 if(e.risk){const [q,v]=e.risk,good=v>0||(v===0&&((e.riskRc||0)+(e.riskLp||0))>0);mul(good?q:1-q)}
 return p}
function winChip(e){const p=winP(e);if(p===null)return '';const v=Math.round(p*100);
 return `<span class="stks"><span class="stk">chances de gagner <em class="${v>=50?'pos-g':'neg-g'}">${v} %</em></span></span>`}
function fxTxt(s,x){""")
# anecdote d'exécution
rep("${stake(c)}${bkPrev(c.e,'exec')}","${stake(c)}${winChip(c.e)}${bkPrev(c.e,'exec')}")
# anecdote de trader en cours de trimestre
rep("<span>${fxTxt(c.s,c.e)}${bkPrev(c.e,'mid')}","<span>${fxTxt(c.s,c.e)}${winChip(c.e)}${bkPrev(c.e,'mid')}")
# textes sans pourcentage
rep('s:"Coûts −10 %, risque divisé par deux.",e:{tcMult:0.9,risk:[0.1,-0.0015]','s:"Coûts −10 %. 10 % de risque : −0,15 %.",e:{tcMult:0.9,risk:[0.1,-0.0015]')
rep('s:"Coûts +5 %, risque divisé par deux.",e:{tcMultOn:[\'ESTX\',\'MXEF\'],tcMult:1.05,risk:[0.5,0.0015]','s:"Coûts +5 %. 50 % de ±0,15 %.",e:{tcMultOn:[\'ESTX\',\'MXEF\'],tcMult:1.05,risk:[0.5,0.0015]')
rep('s:"Coûts −18 %, risque réduit.",e:{tcMultOn:[\'MXEF\'],tcMult:0.82,risk:[0.15,-0.001]','s:"Coûts −18 %. 15 % de risque d\'écart de suivi : −0,1 %.",e:{tcMultOn:[\'MXEF\'],tcMult:0.82,risk:[0.15,-0.001]')
rep('Le conseil vous donne raison une fois sur trois."','33 % de chances que le conseil vous donne raison : comité +6."')
rep('1 unité. 50/50, ±0,54 % de l\'encours."','1 unité. 50 % de chances de +0,54 % de l\'encours, sinon −0,54 %."')
open('index.html','w',encoding='utf-8').write(s);print('lot200 ok')
