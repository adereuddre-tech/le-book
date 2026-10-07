# Lot 240 : co-investissement sur une page dédiée, juste après la validation du book : la rentabilité estimée du book
# est connue et la facture des ordres est déjà déduite de la trésorerie. La part choisie (25 à 100 %) de la trésorerie
# disponible entre dans le fonds pour le trimestre ; elle n'est plus fixée à la fin du trimestre précédent ni placée à
# l'ouverture. Pas de co-investissement au premier trimestre (règle du lot 94), comme avant.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
# 1) ouverture : plus de placement automatique
rep("  const tg=S.q>=1?coinvPct()*cashCo:0;   /* lot 94 : rien au premier trimestre */",
    "  const tg=0;   /* lot 240 : placement choisi après le book (screenCoinv) */")
# 2) validation du book → page de co-investissement
rep("   commitOrders();screenComm();window.scrollTo(0,0);","   commitOrders();screenCoinv();window.scrollTo(0,0);")
rep("function screenComm(){","""/* lot 240 : co-investissement, après le book */
function screenCoinv(){
 if(S.q<1||S.coinvQ===S.q){screenComm();return}
 save('screenCoinv');
 const cash=Math.max(0,mgrCash()),pb=profitBook(S.k),sg=riskShown(weights(S.k)).total;
 const amt=p=>p*cash;
 app.innerHTML=statusBar()+`<div class="fade"><div class="pnlhead"><div class="q">TRIMESTRE ${S.q+1} · CO-INVESTISSEMENT</div>
  <div class="regime">Votre argent dans le fonds</div></div>
  <div class="block"><div class="attr"><span class="an">Rentabilité estimée du book</span><span class="av">${pc2(pb)}</span></div>
   <div class="attr"><span class="an">Risque du book (annualisé)</span><span class="av">${dec(sg*100,1)} %</span></div>
   <div class="attr"><span class="an">Trésorerie disponible, ordres payés</span><span class="av"><b class="gold-g">${mm(cash)}</b></span></div>
   <p class="note">Part de votre trésorerie placée dans le fonds pour ce trimestre : elle suit son résultat net, gains comme pertes, et vous revient à la clôture. Bloquée tout le trimestre, elle ne paie ni budget, ni imprévus. 25 % au moins.</p>
   <div class="cisel">${COINVS.map(p=>`<button class="cip${Math.abs(p-coinvPct())<1e-9?' on':''}" data-p="${p}">${Math.round(p*100)} %</button>`).join('')}</div>
   <p class="note" id="cinote"></p></div>
  <button class="cta" id="ok">Placer et continuer</button></div>`;
 const note=()=>{const p=coinvPct(),r=amt(p);document.getElementById('cinote').innerHTML=`${mm(r)} placés · à rentabilité estimée, ${pb>=0?'+':'−'}${mm(Math.abs(r*pb))} pour vous ce trimestre ; reste en trésorerie ${mm(cash-r)}.`};note();
 app.querySelectorAll('.cip').forEach(b=>b.onclick=()=>{S.coinvPct=+b.dataset.p;app.querySelectorAll('.cip').forEach(x=>x.classList.toggle('on',x===b));note();refreshGain()});
 document.getElementById('ok').onclick=()=>{const tg=amt(coinvPct());S.nav+=tg;S.navQ0+=tg;S.coinvBase=tg;S.coinvIn=tg;S.coinvLock=tg;S.coinvQ=S.q;refreshGain();screenComm();window.scrollTo(0,0)};
}
function screenComm(){""")
# 3) reprise
rep("   screenComm:()=>screenComm(),","   screenComm:()=>screenComm(),screenCoinv:()=>screenCoinv(),")
# 4) fin de trimestre : plus de choix de co-investissement, plus de montant en attente
i0=s.index('function screenDebrief(o){')
a=s.index(" const coSel=(S.over||S.q>=QT())",i0);b=s.index("</p></div>`;\n",a)+len("</p></div>`;\n")
s=s[:a]+" const coSel='';   /* lot 240 : le co-investissement se choisit après le book */\n"+s[b:]
rep("function coPend(){if(!S||S.phase!=='debrief'||S.over||S.q>=QT())return 0;","function coPend(){return 0;   /* lot 240 */\n if(!S||S.phase!=='debrief'||S.over||S.q>=QT())return 0;")
open('index.html','w',encoding='utf-8').write(s);print('lot240 ok')
