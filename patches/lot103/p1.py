# Lot 103, D · comité à limites affichées : risque ex ante, stop trimestriel (contrôlé dans stepEvents),
# concentration par classe ; une limite négociable un trimestre. Plus de cartons sur repli, médiane, book vide,
# appel de marge ni confiance nulle ; plus de pénalité de confiance en double (risque, cartons, marge à la clôture).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)

# 1. limites
rep("/* lot 102 : investisseurs nommés */".join(["","x"])[:0]+"/* ══════════ lot 102 : investisseurs nommés ══════════ */",r'''/* ══════════ lot 103 : limites du comité ══════════ */
const LIM={vol:0.30,red:1.5,stop:0.10,conc:0.70,negLp:-3,neg:{vol:1.25,stop:0.03,conc:0.15}};
function limBO(){return Math.sqrt(BANDB[(S&&S.bud)?S.bud.risk:3]/BANDB[3])}
function limNegOn(id,raw){return !raw&&!!(S&&S.limNeg&&S.limNeg.q===S.q&&S.limNeg.id===id)}
function limVol(raw){return LIM.vol*limBO()*((S&&S.bandTight)||1)*(limNegOn('vol',raw)?LIM.neg.vol:1)}
function limStop(raw){return (LIM.stop*limBO()+(limNegOn('stop',raw)?LIM.neg.stop:0))*((S&&S.bandTight)||1)}
function limConc(raw){return Math.min(1,LIM.conc+(limNegOn('conc',raw)?LIM.neg.conc:0))}
function clsConc(w){const sp=pvol(w);if(sp<1e-6)return {v:0,g:''};const rc=riskContrib(w),m={};INSTR.forEach((x,i)=>m[x.grp]=(m[x.grp]||0)+rc[i]);
 let g='',v=0;for(const k in m){const f=m[k]/sp;if(f>v){v=f;g=k}}return {v,g}}
function limRows(k){const w=weights(k),sp=pvol(w),cc=clsConc(w),lv=limVol(),lc=limConc(),ng=S.limNeg&&S.limNeg.q===S.q?S.limNeg.id:'';
 return `<div class="kv"><span>Limite du comité · risque ex ante${ng==='vol'?' (négociée)':''}</span><b class="${sp>lv*LIM.red?'neg-g':sp>lv?'gold-g':''}">${dec(sp*50,1)} % / ${dec(lv*50,1)} %</b></div>
  <div class="kv"><span>Limite · concentration${cc.g?' ('+cc.g.toLowerCase()+')':''}${ng==='conc'?' (négociée)':''}</span><b class="${cc.v>lc?'gold-g':''}">${Math.round(cc.v*100)} % / ${Math.round(lc*100)} %</b></div>
  <div class="kv"><span>Limite · stop trimestriel${ng==='stop'?' (négocié)':''}</span><b>−${dec(limStop()*100,1)} %</b></div>`}
/* ══════════ lot 102 : investisseurs nommés ══════════ */''')
# 2. clôture : cartons sur les seules limites
rep('''  const tt=S.bandTight||1,ddp=Math.max(0,1-S.idx/Math.max(S.hwmIdx||1,S.idx));
  if(ddp<0.10){C.ddR=0;C.ddY=0}
  if(qTotal<=-0.20*tt)red=`trimestre à ${sgnp(qTotal,1)}`;
  else if(ddp>=0.30*tt&&ddp>(C.ddR||0)+0.05){red=`repli de ${dec(ddp*100,0)} % depuis le plus haut`;C.ddR=ddp}
  else if(S.marginCall)red='appel de marge';
   else if(sp>=RISKCAP.r)red=`risque ex ante de ${dec(sp*50,0)} %`;
  if(sp<0.02&&!(S.tails||[]).some(x=>x.q===S.q))why.push('book vide');
   if(sp>=RISKCAP.y&&sp<RISKCAP.r)why.push(`risque ex ante de ${dec(sp*50,0)} %`);
  if(qTotal<=-0.10*tt)why.push(`trimestre à ${sgnp(qTotal,1)}`);
  if(ddp>=0.18*tt&&ddp>(C.ddY||0)+0.04){why.push(`repli de ${dec(ddp*100,0)} % depuis le plus haut`);C.ddY=ddp}
  if(qTotal-med<=-0.20)why.push(`${dec((med-qTotal)*100,0)} pts sous la médiane des concurrents`);
  if(S.midY===S.q-1){why.unshift('confiance tombée à zéro en cours de trimestre');C.y=Math.max(0,C.y-1)}
  else if(S.lp<=0&&!(S.lpClose<=0))why.unshift('confiance des investisseurs tombée à zéro');
  S.lpClose=S.lp;
''','''  /* lot 103 : le comité ne juge que ses limites affichées (celles du trimestre qui se clôt : S.q est déjà incrémenté) */
  S.q--;const lv=limVol(),ls=limStop(),lc=limConc();S.q++;const cc=clsConc(wFin);
  if(sp>=lv*LIM.red)red=`risque ex ante de ${dec(sp*50,1)} %, limite ${dec(lv*50,1)} %`;
  else if(qTotal<=-2*ls)red=`trimestre à ${sgnp(qTotal,1)}, deux fois le stop`;
  if(sp>lv+1e-9&&sp<lv*LIM.red)why.push(`risque ex ante de ${dec(sp*50,1)} % au-dessus de la limite de ${dec(lv*50,1)} %`);
  if(S.stopY===S.q-1)why.push(`stop trimestriel de −${dec(ls*100,1)} % franchi, book maintenu`);
  else if(S.stopQn!==S.q-1&&qTotal<=-ls)why.push(`stop trimestriel de −${dec(ls*100,1)} % franchi à la clôture`);
  if(cc.v>lc+1e-9)why.push(`${Math.round(cc.v*100)} % du risque en ${cc.g.toLowerCase()}, limite ${Math.round(lc*100)} %`);
''')
rep("  else if(S.qCard)S.lp=Math.max(0,S.lp-2);\n","")
rep("S.redNext=rn;S.lp=Math.max(0,S.lp-6);","S.redNext=rn;")
# pénalités en double
rep("if(sp>RISKLP.x0+0.005)lpD.push(","if(false)lpD.push(")   # lot 103 : le risque ex ante relève du comité seul
rep(" if(S.marginCall)lpD.push(['Liquidation forcée sur appel de marge',-7]);\n","")
rep(" if(S.marginCall)rcD.push([`Appel de marge : ${(S.marginCall.f*100).toFixed(0)} % du book liquidé d'office`,-12]);\n","")
rep("if(lp0>0&&S.lp<=0&&['budget','book','events'].includes(S.phase)&&S.midY!==S.q)midYellow();","/* lot 103 : plus de jaune à confiance nulle */")
# 3. stop trimestriel, vérifié après chaque événement
rep(" if(S.live&&marginPct(S.k)>MGC.thr+1e-9){screenMarginCall();window.scrollTo(0,0);return}   /* lot 100 */\n",
''' if(S.live&&marginPct(S.k)>MGC.thr+1e-9){screenMarginCall();window.scrollTo(0,0);return}   /* lot 100 */
 if(S.live&&S.stopQn!==S.q&&S.k.some(v=>v)&&liveRet()<=-limStop()){screenStopQ();window.scrollTo(0,0);return}   /* lot 103 */
''')
rep("function screenMarginCall(){",r'''function screenStopQ(){S.stopQn=S.q;const r=liveRet(),ls=limStop(),k1=S.k.map(v=>Math.trunc(v/2));let c=0;for(let i=0;i<N;i++){const d=k1[i]-S.k[i];if(d)c+=tcost(d,i).cost*1.3}
 const O=[{id:'cut',b:"Couper le book de moitié",s:`Ordres au tarif d'urgence : ${mm(c)} à votre charge. Pas de carton.`},
  {id:'keep',b:"Passer outre",s:"Le book reste en place ; le comité consigne un carton jaune à la clôture."}];
 app.innerHTML=statusBar()+`<div class="evwrap fade"><div class="evcard bad">${evHead('Comité des risques · stop trimestriel','risk')}<h3>Trimestre à ${sgnp(r,1)} : le stop de −${dec(ls*100,1)} % est franchi</h3>
  <p>La limite est écrite dans votre mandat. Le comité demande de réduire le book de moitié avant la prochaine séance ; dans les deux cas, plus aucun renforcement sur les dépêches ce trimestre.</p>${evTimerHTML}</div>
  <div class="choices" style="margin-top:12px">${O.map((o,i)=>`<button class="choice" data-m="${i}"><b>${o.b}</b><span>${o.s}${i===0?bkD(k1,0,false):''}</span></button>`).join('')}</div></div>`;
 const go=i=>{clearTimer();const o=O[i];
  if(o.id==='cut'){const r0=liveRet();S.k=k1;const r1=liveRet();S.qEvM=(S.qEvM||0)+(r0-r1)*S.navQ0;S.pendingTC+=c/S.nav;S.totalTC+=c;S.stopCut=S.q}else S.stopY=S.q;
  S.noAddQ=true;S.stops=(S.stops||0)+1;S.evLog.push({t:'Stop trimestriel du comité',pnl:0,m:0,lp:0,rc:0});refreshGain();stepEvents()};
 app.querySelectorAll('.choice[data-m]').forEach(b=>b.onclick=()=>go(+b.dataset.m));
 armTimer(()=>go(0),'sans réponse : le desk coupe la moitié')}
function screenMarginCall(){''')
# 4. négociation : coût à l'ouverture
rep(" S.stopQ=false;S.noAddQ=false;\n"," S.stopQ=false;S.noAddQ=false;\n if(S.limNeg&&S.limNeg.q===S.q&&!S.limNeg.paid){S.limNeg.paid=1;S.lp=Math.max(0,S.lp+LIM.negLp)}   /* lot 103 */\n")
# 5. affichage : book, débriefing, pop-ups
rep("  <div class=\"kv\"><span>Perte à −2 σ trimestriels</span>","  ${limRows(S.k)}\n  <div class=\"kv\"><span>Perte à −2 σ trimestriels</span>")
rep(" const coSel=(S.over||S.q>=QT())?'':`",r''' const lmSel=(S.over||S.q>=QT()||S.qCard||(S.limNeg&&S.limNeg.q===S.q-1))?'':(()=>{const cur=S.limNeg&&S.limNeg.q===S.q?S.limNeg.id:'';
  const O=[['','Aucune'],['vol',`Risque ${dec(limVol(1)*50,1)} → ${dec(limVol(1)*LIM.neg.vol*50,1)} %`],['stop',`Stop −${dec(limStop(1)*100,1)} → −${dec((limStop(1)/((S.bandTight)||1)+LIM.neg.stop)*((S.bandTight)||1)*100,1)} %`],['conc',`Concentration ${Math.round(limConc(1)*100)} → ${Math.round(Math.min(1,limConc(1)+LIM.neg.conc)*100)} %`]];
  return `<div class="block"><div class="blockhead"><h2>Négocier une limite</h2><span class="hint">trimestre prochain</span></div>
  <p class="note" style="margin-top:0">Sans carton ce trimestre, le comité accepte de relever une limite pendant un trimestre. Les investisseurs l'apprennent : confiance ${LIM.negLp} à l'ouverture. Pas deux trimestres de suite.</p>
  <div class="cisel">${O.map(([id,t])=>`<button class="lmp${cur===id?' on':''}" data-l="${id}">${t}</button>`).join('')}</div></div>`})();
 const coSel=(S.over||S.q>=QT())?'':`''')
rep("${bnSel}${gtSel}${coSel}","${bnSel}${gtSel}${lmSel}${coSel}")
rep(" app.querySelectorAll('.gtp').forEach(",''' app.querySelectorAll('.lmp').forEach(b=>b.onclick=()=>{const id=b.dataset.l;S.limNeg=id?{id,q:S.q}:null;app.querySelectorAll('.lmp').forEach(x=>x.classList.toggle('on',x===b))});
 app.querySelectorAll('.gtp').forEach(''')
rep("confiance −6.`:`🟨 <b>Carton jaune du comité</b> — ${S.qCard.why}. Confiance −2 ; au deuxième, c'est le rouge.`","`:`🟨 <b>Carton jaune du comité</b> — ${S.qCard.why}. Au deuxième, c'est le rouge.`")
rep(". Au prochain trimestre : <b>${S.qCard.cn.nm}</b> — ${S.qCard.cn.t}. `",". Au prochain trimestre : <b>${S.qCard.cn.nm}</b> — ${S.qCard.cn.t}.`")
rep("<li>Confiance −6.</li>","")
rep("Ce que le comité des risques reproche à votre book s'y ajoute pour moitié, et chaque carton coûte à la clôture (jaune −2, rouge −6). Sous <em>20</em>, des rachats partent à chaque clôture.",
    "Chaque investisseur y ajoute son humeur propre ; sous son seuil, il dépose un avis de rachat payé à la clôture suivante. Les cartons du comité ne coûtent pas de confiance : ils imposent des contraintes.")
rep("Le comité ne tient pas de jauge : il juge vos résultats à chaque clôture et sort des cartons. Ce qu'il note entre-temps pèse sur la confiance ; une seule exception : si la confiance tombe à zéro, le jaune tombe sur-le-champ.",
    "Le comité ne juge que trois limites, affichées sur la page du book. Le risque ex ante et la concentration se lisent sur le book de clôture ; le stop est vérifié après chaque événement du trimestre.")
rep("<li>🟥 <b>Rouge</b> : trimestre à −20 % ou pire, repli de 30 % depuis le plus haut (puis chaque 5 points de plus), appel de marge, ou deuxième jaune.</li><li>🟨 <b>Jaune</b> : trimestre à −10 % ou pire, repli de 18 % (puis chaque 4 points de plus), 20 points sous la médiane des concurrents, book vide, confiance à zéro (même en cours de trimestre).</li><li>Le comité ne juge plus le risque ex ante : il n'y a pas de mandat de volatilité. Le risque se paie autrement : appels de marge et scénarios de stress.</li><li>Un rouge coûte 5 % de l\\'encours, 6 points de confiance, et une contrainte forte",
    "<li>🟥 <b>Rouge</b> : risque ex ante à ${dec(LIM.red,1)} fois la limite, trimestre à deux fois le stop, ou deuxième jaune.</li><li>🟨 <b>Jaune</b> : risque ex ante au-dessus de la limite, stop franchi sans couper, concentration au-dessus de la limite.</li><li>Limites du trimestre : risque ${dec(limVol()*50,1)} %, stop −${dec(limStop()*100,1)} %, concentration ${Math.round(limConc()*100)} % du risque dans une classe. Le back office les élargit ou les resserre ; une limite se négocie au débriefing.</li><li>Un rouge impose deux contraintes fortes")
rep("${tbl([['Plafond de position',","${limRows(S.k)}${tbl([['Plafond de position',")
open('index.html','w',encoding='utf-8').write(s);print('lot103 p1 ok')
