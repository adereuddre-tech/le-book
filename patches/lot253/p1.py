p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# mouvement d'une dépêche extrême : sans l'effet de foule, comme à l'écran de la dépêche
rep(" return v<0?v*crowd(riskShown(w).total):v}\nfunction xHintLoss"," return v}\nfunction xHintLoss")
# page : protection (chaque trimestre) + co-investissement (dès le 2e)
rep("""function screenCoinv(){
 if(S.q<1||S.coinvQ===S.q){screenComm();return}
 save('screenCoinv');
 const cash=Math.max(0,mgrCash()),pb=profitBook(S.k),sg=riskShown(weights(S.k)).total;
 const amt=p=>p*cash;
 app.innerHTML=statusBar()+`<div class="fade"><div class="pnlhead"><div class="q">TRIMESTRE ${S.q+1} · CO-INVESTISSEMENT</div>
  <div class="regime">Votre argent dans le fonds</div></div>
  <div class="block"><div class="attr">""","""/* lot 253 : protection contre les extrêmes, achetée en début de trimestre, ordres passés. Prime fixe payée par le fonds ;
   elle rend une part du choc immédiat de tout événement extrême du trimestre (STRESS et dépêches x:1), back office compris. */
const HEDGE={c:0.010,h:0.70};
function xImmEst(){const k=S.k,bo=0.5+0.5*(TAILM[S.bud.risk]||1),h=S.xHint;
 if(h&&h.t)return {nm:xHintName(),v:0.5*xEvLoss(k,h.t),sig:1};
 let sc=h&&h.id?STRESS.find(x=>x.id===h.id):null;const sig=!!sc;
 if(!sc){let bv=1e9;STRESS.forEach(x=>{const v=stressLoss(k,x);if(v<bv){bv=v;sc=x}})}
 return {nm:sc.nm.charAt(0).toLowerCase()+sc.nm.slice(1),v:0.5*bo*stressLoss(k,sc),sig}}
function hedgeBlock(){const e=xImmEst(),pX=1-(1-stressP())*(1-(S.q>=1?XPROB:0)),c=HEDGE.c*S.nav,on=S.hedgeQ===S.q||S.hedgePick===S.q;
 return `<div class="block"><div class="blockhead"><h2>Protection contre les extrêmes</h2><span class="hint">payée par le fonds</span></div>
  ${S.xHint?`<div class="flag xh" style="margin:0 0 8px"><span>${xHintTxt(S.k)}</span></div>`:''}
  <p class="note" style="margin:0 0 6px">Un événement extrême frappe ce trimestre avec une probabilité d'environ ${Math.round(pX*100)} %. ${xWatchTxt()}</p>
  <div class="attr"><span class="an">Prime, ${dec(HEDGE.c*100,0)} % de l'encours</span><span class="av"><b class="neg-g">−${mm(c)}</b></span></div>
  <div class="attr"><span class="an">${e.sig?'Extrême signalé':'Pire extrême pour votre book'} : ${e.nm} · choc immédiat</span><span class="av"><b class="${e.v<0?'neg-g':'pos-g'}">${sgnp(e.v,1)} · ${mm(Math.abs(e.v)*S.nav)}</b></span></div>
  <div class="attr"><span class="an">Rendu par la protection (${Math.round(HEDGE.h*100)} % du choc immédiat)</span><span class="av"><b class="pos-g">${e.v<0?'+'+mm(-e.v*HEDGE.h*S.nav):'—'}</b></span></div>
  <p class="note">La protection rend ${Math.round(HEDGE.h*100)} % du choc immédiat de tout événement extrême du trimestre ; la suite du mouvement reste à votre charge, comme pour une dépêche. Sans extrême, la prime est perdue.</p>
  <div class="cisel"><button class="hgp${on?'':' on'}" data-h="0">Sans protection</button><button class="hgp${on?' on':''}" data-h="1">Protéger · −${mm(c)}</button></div></div>`}
function screenCoinv(){
 const hAsk=S.hedgeAsk!==S.q,cAsk=S.q>=1&&S.coinvQ!==S.q;
 if(!hAsk&&!cAsk){screenComm();return}
 save('screenCoinv');
 const cash=Math.max(0,mgrCash()),pb=profitBook(S.k),sg=riskShown(weights(S.k)).total;
 const amt=p=>p*cash;
 app.innerHTML=statusBar()+`<div class="fade"><div class="pnlhead"><div class="q">TRIMESTRE ${S.q+1} · ${hAsk&&cAsk?'PROTECTION ET CO-INVESTISSEMENT':hAsk?'PROTECTION':'CO-INVESTISSEMENT'}</div>
  <div class="regime">${hAsk&&cAsk?'Couvrir le fonds, y placer votre argent':hAsk?'Couvrir le fonds':'Votre argent dans le fonds'}</div></div>
  ${hAsk?hedgeBlock():''}
  ${cAsk?`<div class="block"><div class="blockhead"><h2>Co-investissement</h2><span class="hint">votre trésorerie</span></div><div class="attr">""")
rep("""   <p class="note" id="cinote"></p></div>
  <button class="cta" id="ok">Placer et continuer</button></div>`;
 const note=()=>{""","""   <p class="note" id="cinote"></p></div>`:''}
  <button class="cta" id="ok">${cAsk?'Placer et continuer':'Continuer'}</button></div>`;
 app.querySelectorAll('.hgp').forEach(b=>b.onclick=()=>{S.hedgePick=+b.dataset.h?S.q:-1;app.querySelectorAll('.hgp').forEach(x=>x.classList.toggle('on',x===b))});
 if(!cAsk){document.getElementById('ok').onclick=()=>{hedgeApply();screenComm();window.scrollTo(0,0)};return}
 const note=()=>{""")
rep("""document.getElementById('ok').onclick=()=>{const tg=amt(coinvPct());S.nav+=tg;""","""document.getElementById('ok').onclick=()=>{if(hAsk)hedgeApply();const tg=amt(coinvPct());S.nav+=tg;""")
rep("""function screenComm(){""","""function hedgeApply(){if(S.hedgeAsk===S.q)return;S.hedgeAsk=S.q;if(S.hedgePick!==S.q)return;
 const c=HEDGE.c*S.nav;S.nav-=c;S.qEvM=(S.qEvM||0)-c;S.hedgeQ=S.q;S.evLog.push({t:'Protection contre les extrêmes',pnl:-HEDGE.c,m:-c,lp:0,rc:0});try{refreshGain()}catch(e){}}
function screenComm(){""")
# l'écran de la dépêche extrême : la protection rend sa part
rep("""(S.tails=S.tails||[]).push({q:S.q,t:ev.t,f:-imm,id:'stress'});xRivHit(ev.stress)}   /* lot 101 : le back office amortit le choc */""",
    """(S.tails=S.tails||[]).push({q:S.q,t:ev.t,f:-imm,id:'stress'});xRivHit(ev.stress)}   /* lot 101 : le back office amortit le choc */
 let hgB=0;if(ev.x&&S.hedgeQ===S.q&&imm<0){hgB=-imm*HEDGE.h;imm+=hgB}   /* lot 253 : protection */""")
rep("""aucun ordre possible jusqu'à la clôture, et fermés au fonds le trimestre prochain.</p>`:''}${evTimerHTML}</div>""",
    """aucun ordre possible jusqu'à la clôture, et fermés au fonds le trimestre prochain.</p>`:''}${hgB?`<p class="note" style="margin:8px 0 0">🛡 Votre protection rend <b class="pos-g">${mm(hgB*navB)}</b> sur le choc immédiat.</p>`:''}${evTimerHTML}</div>""")
# styles : bouton de protection comme les crans du co-investissement
rep(".cisel .lmp,.cisel .gtp{",".cisel .lmp,.cisel .gtp,.cisel .hgp{")
rep(".cisel .lmp.on,.cisel .gtp.on{",".cisel .lmp.on,.cisel .gtp.on,.cisel .hgp.on{")
open(p,'w',encoding='utf-8').write(s)
