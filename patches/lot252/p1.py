p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# 1. le tirage de la veille après celui de l'extrême macro (x:1)
rep("  xHintDraw();   /* lot 106 */\n","")
rep("""   if(av.length){const e=av[Math.floor(u()*av.length)];S.usedX.push(e.t);S.evQueue.splice(Math.floor(u()*(S.evQueue.length+1)),0,e)}}}
""","""   if(av.length){const e=av[Math.floor(u()*av.length)];S.usedX.push(e.t);S.evQueue.splice(Math.floor(u()*(S.evQueue.length+1)),0,e)}}}
 xHintDraw();   /* lot 106 ; lot 252 : après les deux tirages d'extrêmes */
""")
# 2. veille graduée
a=s.index("/* lot 106 : l'événement extrême s'annonce parfois.");b=s.index("function stressP(){")
s=s[:a]+r"""/* lot 252 : veille des extrêmes, graduée de 10 à 95 %. Elle couvre les deux familles d'extrêmes (STRESS, calculés sur le book,
   et dépêches x:1). Trois probabilités : sentir l'extrême qui vient (s), l'identifier une fois senti (i), fausse alerte
   un trimestre sans extrême (fa = 15 % × (1 − s)). Facteurs repris : fiabilité des sources selon la recherche (RESREL, front office),
   contrôle des risques (cran du back office), lecture des dépêches selon le bonus (BONREAD). Bases par style :
   le flux sent le mieux et identifie le moins, le fondamental l'inverse, le quant entre les deux. */
const XSB={syst:{s:0.27,i:0.50},fonda:{s:0.175,i:0.65},flux:{s:0.40,i:0.10}};
function xWatch(){const P=PROF(),B=XSB[P.id]||XSB.fonda,bd=S.bud||{},f=((RESREL[bd.res]??0)+0.08)/0.19,r=Math.min(1,(bd.bo||0)/5),b=(1.25-(BONREAD[bonEff()]||1))/0.5;
 const sv=Math.max(0.10,Math.min(0.95,B.s+0.30*f+0.20*r+0.15*(b-0.5))),iv=Math.max(0.05,Math.min(0.95,B.i+0.30*f+0.10*(b-0.5)));
 return {s:sv,i:iv,fa:0.15*(1-sv)}}
function xHintDraw(){const u=prng32(hash32('xhint'+S.q,S.seed)),W=xWatch(),src=PROF().id,a=u(),b=u(),c=u(),d=u();S.xHint=null;
 const sc=S.stressQ?STRESS.find(x=>x.id===S.stressQ):null,mx=sc?null:(S.evQueue||[]).find(e=>e.x&&!e.stress);
 if(sc||mx){if(a<W.s)S.xHint=b<W.i?(sc?{src,id:sc.id}:{src,t:mx.t}):{src}}
 else if(c<W.fa)S.xHint=b<W.i?{src,id:STRESS[Math.floor(d*STRESS.length)].id,fake:1}:{src,fake:1}}
/* mouvement complet d'une dépêche extrême sur le book k (lecture, comme stressLoss) */
function xEvLoss(k,t){const e=MACROEV.find(x=>x.t===t);if(!e)return 0;const w=weights(k);let v=0;for(const sy in e.hit){const i=IDX[sy];if(i!==undefined)v+=w[i]*e.hit[sy]*INSTR[i].sigQ}
 return v<0?v*crowd(riskShown(w).total):v}
function xHintLoss(k){const h=S&&S.xHint;if(!h||!k)return null;if(h.id){const sc=STRESS.find(x=>x.id===h.id);return sc?stressLoss(k,sc):null}if(h.t)return xEvLoss(k,h.t);return null}
function xHintName(){const h=S&&S.xHint;if(!h)return '';if(h.id){const sc=STRESS.find(x=>x.id===h.id);return sc?sc.nm.charAt(0).toLowerCase()+sc.nm.slice(1):''}
 return h.t?h.t.charAt(0).toLowerCase()+h.t.slice(1):''}
function xHintTxt(k){const h=S&&S.xHint;if(!h)return '';const nm=xHintName(),L=xHintLoss(k);
 const who={syst:'<b>Le modèle de risque</b> signale',fonda:'<b>Votre réseau</b> annonce',flux:'<b>Votre intuition</b> :'}[h.src]||'<b>Rumeur</b> :';
 const what=nm?`un événement extrême ce trimestre : ${nm}.`:`un choc extrême se prépare ce trimestre. ${h.src==='flux'?'Vous ne sauriez pas dire lequel.':'Lequel, personne ne le sait.'}`;
 const ch=h.src==='syst'&&nm&&L!=null?` Perte du book sur le mouvement complet : ${sgnp(L,1)} · ${moneyB(Math.abs(L)*S.nav)}.`:'';
 return `🔴 ${who} ${what}${ch}`}
function xWatchTxt(){const W=xWatch();return `Votre veille sent venir <b>${Math.round(W.s*100)} %</b> des extrêmes et en identifie <b>${Math.round(W.i*100)} %</b> ; fausse alerte ${Math.round(W.fa*100)} % des trimestres calmes.`}
"""+s[b:]
# 3. page du book : la veille sous la ligne des extrêmes
rep("""l'un d'eux frappe ce trimestre avec une probabilité de ${Math.round(stressP()*100)} %</span><b></b></div>""",
    """l'un d'eux frappe ce trimestre avec une probabilité de ${Math.round(stressP()*100)} %</span><b></b></div><p class="note" style="margin:2px 0 4px">${xWatchTxt()}</p>""")
rep("Des événements extrêmes peuvent frapper chaque trimestre ; une rumeur, ou le pouvoir de votre style, les annonce parfois.",
    "Des événements extrêmes peuvent frapper chaque trimestre ; votre veille les sent venir de 10 à 95 % des fois, selon votre style, vos équipes et leur bonus, et une protection s'achète en début de trimestre.")
open(p,'w',encoding='utf-8').write(s)
