# Lot 109 : les « tuyaux » du prime broker. Avant l'exécution, 35 % des trimestres, le prime broker propose une affaire
# hors book : coût certain, gain possible, espérance positive. Le fonds paie et encaisse tout de suite (P&L du trimestre).
# Refusée, un concurrent la prend : son trimestre en porte le résultat.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("function screenExec(){\n hint('exec');",r'''/* lot 109 : tuyaux du prime broker — c coût, g gain, p chance ; espérance p·g − c > 0 */
const TIPS=[
 {id:'spec',nm:"Special situations",ic:'🎯',c:0.010,g:0.050,p:1/3,d:"Une scission de conglomérat que le marché n'a pas encore lue. Le desk du prime broker a fait le travail ; il vous ouvre l'allocation."},
 {id:'dist',nm:"Dette en détresse",ic:'🏚️',c:0.015,g:0.060,p:0.35,d:"Des obligations d'un distributeur en restructuration, à 22 centimes. Si le plan passe, elles repartent vers 60."},
 {id:'ma',nm:"Arbitrage de fusion",ic:'🤝',c:0.005,g:0.015,p:0.60,d:"Une OPA amicale, l'écart de prix reste large : le marché doute de l'autorisation de la concurrence."},
 {id:'dual',nm:"Double cotation",ic:'🔀',c:0.004,g:0.012,p:0.55,d:"La même action cote à deux places avec un écart anormal ; le prime broker prête les titres pour le jouer."},
 {id:'ipo',nm:"Introduction en bourse",ic:'🔔',c:0.008,g:0.040,p:0.30,d:"Une allocation dans une introduction très demandée. Premier jour glorieux, ou retrait du dossier."},
 {id:'adj',nm:"Adjudication souveraine",ic:'🏦',c:0.003,g:0.009,p:0.50,d:"Une adjudication du Trésor s'annonce mal couverte ; le prime broker vous propose d'y soumissionner sous le marché."},
 {id:'adjc',nm:"Adjudication de crédit souverain",ic:'🧾',c:0.006,g:0.022,p:0.40,d:"Une émission d'un souverain émergent, prime d'émission généreuse si la demande suit."}];
const TIPP=0.35;
function tipDraw(){const u=prng32(hash32('tip'+S.q,S.seed));if(u()>=TIPP)return null;const t=TIPS[Math.floor(u()*TIPS.length)];const win=u()<t.p,rj=Math.floor(u()*S.rivals.length);return {t,win,rj}}
function screenTip(){S.tipQ=S.q;const D=tipDraw();if(!D){screenExec();return}const {t,win,rj}=D,rv=S.rivals[rj];
 const ev=t.p*t.g-t.c;
 app.innerHTML=statusBar()+`<div class="evwrap fade"><div class="evcard">${evHead('Prime broker · proposition hors book','trade')}<h3>${t.ic} ${t.nm}</h3><p>${t.d}</p>
  ${tbl([['Coût certain',`<b class="neg-g">−${dec(t.c*100,1)} % · ${mm(t.c*S.nav)}</b>`],['Gain si ça passe',`<b class="pos-g">+${dec(t.g*100,1)} % · ${mm(t.g*S.nav)}</b>`],['Chance',`${Math.round(t.p*100)} %`],['Espérance',`<b class="pos-g">+${dec(ev*100,2)} % · ${mm(ev*S.nav)}</b>`]])}
  <p class="note" style="margin-top:6px">Le fonds paie et encaisse tout de suite ; le résultat compte dans le trimestre. Si vous passez, ${rv.nm} prend l'affaire.</p></div>
  <div class="choices" style="margin-top:12px"><button class="choice" data-t="1"><b>Prendre l'affaire</b><span>−${dec(t.c*100,1)} % tout de suite, +${dec(t.g*100,1)} % une fois sur ${dec(1/t.p,1)}.</span></button>
  <button class="choice" data-t="0"><b>Passer</b><span>${rv.nm} la prend à votre place.</span></button></div></div>`;
 const go=k=>{clearTimer();const imm=win?t.g-t.c:-t.c;
  if(k){const navB=S.nav;S.nav*=(1+imm);S.qEvM=(S.qEvM||0)+imm*navB;(S.tipLog=S.tipLog||[]).push({q:S.q,id:t.id,win,m:imm*navB});
   toast(win?`${t.nm} : l'affaire passe, ${sgnp(imm,1)} pour le fonds (${mm(imm*navB)}).`:`${t.nm} : l'affaire ne passe pas, ${sgnp(imm,1)} pour le fonds.`)}
  else{S.xRiv=S.rivals.map((r,j)=>((S.xRiv||[])[j]||0)+(j===rj?imm:0));toast(`${rv.nm} a pris l'affaire : ${win?'elle est passée':'elle a échoué'} (${sgnp(imm,1)} pour lui).`)}
  screenExec();window.scrollTo(0,0)};
 app.querySelectorAll('.choice[data-t]').forEach(b=>b.onclick=()=>go(+b.dataset.t));
 armTimer(()=>go(0),"sans réponse : l'affaire part ailleurs")}
function screenExec(){
 if(S.tipQ!==S.q){screenTip();return}   /* lot 109 */
 hint('exec');''')
open('index.html','w',encoding='utf-8').write(s);print('lot109 p1 ok')
