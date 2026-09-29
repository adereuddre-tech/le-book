# Lot 102, C · investisseurs nommés. Quatre investisseurs (caisse de retraite, fonds souverain, family office,
# fonds de fonds), chacun avec sa satisfaction = confiance + écart propre, ses rachats sur préavis d'un trimestre,
# ses souscriptions et une gate. Remplacent les flux par concurrent, le rachat à confiance basse, le retrait pour
# risque, les deux redeem() de clôture, les 5 % du carton rouge et les retraits après dépêche (midFlows).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)

# 1. moteur
rep("function flowInB(frac){",r'''/* ══════════ lot 102 : investisseurs nommés ══════════ */
const INVR=[
 {id:'cr',nm:'Caisse de retraite des Cheminots',ic:'🚂',w0:0.35,off0:3,thr:25,sub:0.06,wt:{perf:0.7,dd:1.8,risk:1.6,med:0.3,mg:1.5},
  d:"Patiente, mais tenue par une clause de repli : au-delà du repli maximal de votre style, elle demande la moitié de sa part."},
 {id:'fs',nm:'Fonds souverain de Nordhavn',ic:'🏛️',w0:0.30,off0:6,thr:20,sub:0.10,wt:{perf:1,med:0.7,comm:1.6,leak:1.8},
  d:"Le plus gros ticket et le plus lent à bouger ; il tient à la parole donnée et déteste lire vos positions dans la presse."},
 {id:'fam',nm:'Family office Vandermeer',ic:'🎩',w0:0.15,off0:-8,thr:35,sub:0.15,wt:{perf:1.6,neg:1.5,dd:1.2,risk:0.5,med:0.7},
  d:"Nerveux : un trimestre négatif lui pèse double, un bon trimestre le rend généreux."},
 {id:'ff',nm:'Fonds de fonds Albatros',ic:'🐦',w0:0.20,off0:-4,thr:30,sub:0.12,wt:{perf:0.8,med:2.2,risk:1.1},
  d:"Il vous compare aux trois concurrents, trimestre après trimestre."}];
const INVP={n0:0.20,nk:0.60,subAt:65,back:0.05,gate:0.15,gateLp:-6,cancel:8,offMax:25,offK:0.85,dStep:8};
function invs(){if(!S.inv)S.inv=INVR.map(d=>({id:d.id,w:d.w0,off:d.off0,ntc:0}));return S.inv}
function invD(id){return INVR.find(d=>d.id===id)}
function invSat(v){return Math.max(0,Math.min(100,Math.round(S.lp+(v.off||0))))}
function extNav(){return Math.max(0,S.nav-(S.coinvLock?coinvLocked():0))}
function invFlow(v,amt){const I=invs(),E=extNav(),h=I.map(x=>x.w*E),j=I.indexOf(v);amt=Math.max(-h[j],amt);h[j]+=amt;const E2=E+amt;
 I.forEach((x,q)=>x.w=E2>1e-12?Math.max(0,h[q])/E2:0);S.nav+=amt;S.flows=(S.flows||0)+amt;S.qFlow=(S.qFlow||0)+amt;return amt}
function invDue(){const E=extNav();return invs().reduce((a,v)=>a+(v.ntc>0?v.ntc*v.w*E:0),0)}
function gateOk(){return S.gateUsed!==S.q-1&&invDue()>INVP.gate*extNav()}
function invCat(l){return /^Performance|^Objectif|plus haut/.test(l)?'perf':/négatif/.test(l)?'neg':/communication|^Engagement/.test(l)?'comm':/^Repli/.test(l)?'dd':/médiane/.test(l)?'med':/^Risque ex ante/.test(l)?'risk':/circulé/.test(l)?'leak':/marge/.test(l)?'mg':''}
/* clôture : écarts propres, avis échus (gate), nouveaux avis, souscriptions. Rend le flux net en fraction d'encours. */
function invClose(o){const I=invs(),E0=Math.max(1e-9,extNav());
 const lines=(S.lpD||[]).filter(x=>!/^Multiplicateur|^Plafonnement/.test(x[0]));
 I.forEach(v=>{const D=invD(v.id);let d=0;lines.forEach(x=>{const c=invCat(x[0]);if(c&&D.wt[c]!==undefined)d+=(D.wt[c]-1)*x[1]});
  d*=o.lpMult*(d<0?SIZE().lpNeg:1);v.off=Math.max(-INVP.offMax,Math.min(INVP.offMax,D.off0+(v.off+Math.max(-INVP.dStep,Math.min(INVP.dStep,d))-D.off0)*INVP.offK))});
 let due=0;const R=I.map(v=>{const D=invD(v.id),r={id:v.id,sat:invSat(v),h0:v.w*E0,pay:0,ntc:0,sub:0,cancel:false,gated:0};
  if(v.ntc>0){if(r.sat>=D.thr+INVP.cancel){r.cancel=true;v.ntc=0}else{r.pay=v.ntc*v.w*E0;due+=r.pay}}return r});
 let gf=1;S.qGate=false;
 if(S.gateNext&&due>INVP.gate*E0){gf=INVP.gate*E0/due;S.gateUsed=S.q;S.qGate=true;S.gates=(S.gates||0)+1;S.lp=Math.max(0,S.lp+INVP.gateLp);S.lpD.push(['Gate activée : rachats limités à '+Math.round(INVP.gate*100)+' % de l\'encours',INVP.gateLp])}
 S.gateNext=false;
 R.forEach((r,j)=>{const v=I[j];if(r.pay>0){const p=r.pay*gf;r.gated=r.pay-p;r.pay=-invFlow(v,-p);
  v.ntc=r.gated>1e-12&&v.w*extNav()>1e-12?Math.min(1,r.gated/(v.w*extNav())):0}});
 R.forEach((r,j)=>{const v=I[j],D=invD(v.id);if(v.ntc>0||v.w<1e-6)return;const sat=invSat(v);let f=0;
  if(sat<D.thr)f=Math.min(1,(INVP.n0+INVP.nk*(D.thr-sat)/D.thr)*(SIZE().flowMult||1));
  if(v.id==='cr'&&o.ddp>=ddMax()){f=Math.max(f,0.5);r.clause=true}
  if(f>0){v.ntc=f;v.ntcQ=S.q;r.ntc=f*v.w*extNav()}});
 R.forEach((r,j)=>{const v=I[j],D=invD(v.id);if(v.ntc>0)return;const sat=invSat(v);
  if(v.w<0.01){if(sat>=70&&!r.pay){r.sub=invFlow(v,INVP.back*S.aum0);r.back=true}return}
  if(sat>INVP.subAt){const f=D.sub*(sat-INVP.subAt)/(100-INVP.subAt)*(SIZE().flowIn||1)*Math.max(0,1-capStress());if(f>0.002)r.sub=invFlow(v,f*v.w*extNav())}});
 R.forEach((r,j)=>{r.h1=I[j].w*extNav();r.sat=invSat(I[j])});
 S.invQ=R;const net=R.reduce((a,r)=>a+r.sub-r.pay,0);
 const nm=r=>invD(r.id).nm,P=R.filter(r=>r.pay>0),N=R.filter(r=>r.ntc>0),U=R.filter(r=>r.sub>0),C=R.filter(r=>r.cancel);
 S.poachMsg=[P.length?`Rachats payés : ${P.map(r=>`${nm(r)} −${mm(r.pay)}${r.gated>0?` (gate : ${mm(r.gated)} reportés)`:''}`).join(' · ')}.`:'',
  C.length?`Avis retirés : ${C.map(nm).join(', ')}.`:'',
  N.length?`Avis de rachat déposés, payables à la prochaine clôture : ${N.map(r=>`${nm(r)} ${mm(r.ntc)}${r.clause?' (clause de repli)':''}`).join(' · ')}.`:'',
  U.length?`Souscriptions : ${U.map(r=>`${nm(r)} +${mm(r.sub)}${r.back?' (retour)':''}`).join(' · ')}.`:''].filter(Boolean).join(' ')||'Aucun mouvement d\'investisseur.';
 return net/E0}
/* tableau des investisseurs (débriefing, pop-up d'encours) */
function invTable(){const I=invs(),E=extNav(),R=S.invQ||[];
 return `<table class="qt" style="margin-top:12px"><thead><tr><th style="text-align:left">Investisseur</th><th>Part</th><th>Satisf.</th><th>Mouvement</th></tr></thead><tbody>
 ${I.map(v=>{const D=invD(v.id),r=R.find(x=>x.id===v.id)||{},sat=invSat(v),h=v.w*E;
  const mv=[r.pay>0?`<span class="neg-g">−${mm(r.pay)}</span>`:'',r.sub>0?`<span class="pos-g">+${mm(r.sub)}</span>`:'',r.cancel?'avis retiré':'',v.ntc>0?`<span class="neg-g">avis ${mm(v.ntc*h)}</span>`:''].filter(Boolean).join(' · ')||'—';
  return `<tr><td style="text-align:left">${D.ic} ${D.nm}</td><td>${h>1e-9?mm(h)+' · '+Math.round(v.w*100)+' %':'parti'}</td><td class="${sat<D.thr?'neg-g':sat>INVP.subAt?'pos-g':''}">${sat}<small style="color:var(--dimmer)"> / ${D.thr}</small></td><td>${mv}</td></tr>`}).join('')}</tbody></table>
 <p class="note" style="margin-top:6px">Satisfaction = confiance ± l'humeur propre de chacun. Sous son seuil, un investisseur dépose un avis de rachat, payé à la clôture suivante ; l'avis tombe s'il remonte à son seuil + ${INVP.cancel}. Au-dessus de ${INVP.subAt}, il souscrit.</p>`}
function flowInB(frac){''')
# 2. clôture : les flux par concurrent et les rachats de confiance / risque cèdent la place aux investisseurs
rep(''' const CLI={syst:0.6,fonda:1.0,flux:1.6};
 const fl=S.rivals.map(rv=>{const d=qTotal-(rv.last||0),s=CLI[rv.style]||1;
   let f=Math.max(-0.06,Math.min(0.06,0.5*s*d));if(f<0)f*=SIZE().flowMult;else f*=(SIZE().flowIn||1);return {rv,d,f}});
 let tot=fl.reduce((a,x)=>a+x.f,0);
 if(S.lp<40)tot-=RDM.low*(40-S.lp)/40*SIZE().flowMult;
 const riskOut=(RISKLP.fk*Math.max(0,sp-RISKLP.fl)+RISKQ.fl*Math.max(0,sp-RISKLP.fl)**2)*SIZE().flowMult;tot-=riskOut;
 tot=Math.max(-0.25,Math.min(0.20,tot+(rng()-0.5)*0.01));
 S.qFlowBy=fl.map(x=>({nm:x.rv.nm,d:x.d,f:x.f}));
 const amt=tot*S.nav;S.nav+=amt;S.flows+=amt;S.qFlow=(S.qFlow||0)+amt;
 const lines=fl.filter(x=>Math.abs(x.f)>=0.002).map(x=>`${x.rv.nm} ${x.f>0?'+':'−'}${dec(Math.abs(x.f)*100,1)} % (${x.d>0?'battu':'devant vous'} de ${dec(Math.abs(x.d)*100,1)} pt${Math.abs(x.d)>=0.015?'s':''})`);
 S.poachMsg=`${tot>=0?'Collecte':'Rachats'} : ${tot>=0?'+':'−'}${dec(Math.abs(tot)*100,1)} % d'encours (${mm(Math.abs(amt))}).${lines.length?' Clients par concurrent — '+lines.join(' · ')+'.':''}${riskOut>=0.001?` Dont −${dec(riskOut*100,1)} % retirés pour un risque jugé trop élevé.`:''}`;
''',''' const tot=invClose({lpMult,ddp:Math.max(0,1-S.idx/Math.max(S.hwmIdx||1,S.idx))});   /* lot 102 : investisseurs nommés */
''')
rep('''  if(ddp>=ddMax()&&ddp>(S.ddHit||0)+0.02){S.ddHit=ddp;redeem('repli',RDM.dd0+RDM.ddk*(ddp-ddMax()))}}
 if(S.lp<=20)redeem('investisseurs',RDM.lp0+RDM.lpk*(20-S.lp));
''','''  }   /* lot 102 : repli et confiance passent par les investisseurs nommés */
''')
rep("S.redNext=rn;const out=0.05*S.nav;S.nav-=out;S.flows-=out;S.qFlow=(S.qFlow||0)-out;S.lp=Math.max(0,S.lp-6);","S.redNext=rn;S.lp=Math.max(0,S.lp-6);")
# retraits après dépêche : supprimés
rep("function midFlows(total,lines){\n","function midFlows(total,lines){return;   /* lot 102 : plus de retrait anonyme après dépêche */\n")
# trophée du fonds souverain : c'est Nordhavn qui relève son mandat
rep("B('souv',g>=1.6&&conf0>=78,()=>{const m=flowInB(0.20);","B('souv',g>=1.6&&conf0>=78,()=>{const v=invs().find(x=>x.id==='fs'),m=invFlow(v,0.20*extNav());")
# 3. débriefing
rep("<li>5 % de l'encours retiré par les investisseurs.</li>","")
rep("5 % de l'encours retiré, confiance −6","confiance −6")
rep(''' if(S.lp<24&&!S.over)warn.push("Le principal investisseur a demandé un point mensuel. C'est le signe qui précède les rachats.");''',
''' {const I=invs().filter(v=>v.ntc>0);if(I.length&&!S.over){const E=extNav(),t=I.reduce((a,v)=>a+v.ntc*v.w*E,0);
  warn.push(`📨 <b>Avis de rachat pour la prochaine clôture</b> : ${I.map(v=>`${invD(v.id).nm} ${mm(v.ntc*v.w*E)}`).join(' · ')}, soit ${dec(t/Math.max(1e-9,E)*100,1)} % de l'encours. Un avis tombe si l'investisseur remonte à son seuil + ${INVP.cancel}.`)}}''')
rep("  </tbody></table>\n  ${(()=>{const T0=S.tresQ0","  </tbody></table>\n  ${invTable()}\n  ${(()=>{const T0=S.tresQ0")
rep(" const coSel=(S.over||S.q>=QT())?'':`",''' const gtSel=(S.over||S.q>=QT()||!gateOk())?'':`<div class="block"><div class="blockhead"><h2>Gate</h2><span class="hint">prochaine clôture</span></div>
  <p class="note" style="margin-top:0">${mm(invDue())} d'avis de rachat tombent à la prochaine clôture, ${dec(invDue()/Math.max(1e-9,extNav())*100,1)} % de l'encours. La gate limite les paiements à ${Math.round(INVP.gate*100)} % de l'encours, au prorata ; le reste est reporté d'un trimestre. Prix : confiance ${INVP.gateLp}, et pas deux trimestres de suite.</p>
  <div class="cisel"><button class="gtp${S.gateNext?'':' on'}" data-g="0">Payer à l'échéance</button><button class="gtp${S.gateNext?' on':''}" data-g="1">Activer la gate</button></div></div>`;
 const coSel=(S.over||S.q>=QT())?'':`''')
rep("${bnSel}${coSel}","${bnSel}${gtSel}${coSel}")
rep(" app.querySelectorAll('.cip').forEach(b=>b.onclick=",''' app.querySelectorAll('.gtp').forEach(b=>b.onclick=()=>{S.gateNext=b.dataset.g==='1';app.querySelectorAll('.gtp').forEach(x=>x.classList.toggle('on',x===b))});
 app.querySelectorAll('.cip').forEach(b=>b.onclick=''')
# 4. pop-up d'encours
rep("   <p style=\"margin-top:10px\">Au-delà de <em>${Math.round(ddMax()*100)} % de repli</em> depuis le pic, des investisseurs demandent leur sortie.",
    "   <p style=\"margin:12px 0 4px\">Vos investisseurs</p>${invTable()}\n   <p style=\"margin-top:10px\">Au-delà de <em>${Math.round(ddMax()*100)} % de repli</em> depuis le pic, la caisse de retraite demande la moitié de sa part.")
open('index.html','w',encoding='utf-8').write(s);print('lot102 p1 ok')
