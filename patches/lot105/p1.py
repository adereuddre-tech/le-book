# Lot 105 : investisseurs simplifiés. Plus de satisfaction ni d'humeur par investisseur : la confiance suffit.
# Chaque investisseur déclenche sur SON critère de performance ; la confiance fixe le montant.
#   caisse de retraite : régularité (4 derniers trimestres) ; fonds souverain : engagement tenu ou manqué deux fois de suite ;
#   family office : performance absolue du trimestre ; fonds de fonds : écart à la médiane des concurrents.
# Rachat = part × taux propre × 2 × (1 − confiance/100) ; souscription = part × taux propre × confiance/50.
# Préavis d'un trimestre (l'avis tombe si le critère repasse au vert), gate et clause de repli inchangés.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
i=s.index("/* ══════════ lot 102 : investisseurs nommés ══════════ */");j=s.index("function flowInB(frac){",i)
s=s[:i]+r'''/* ══════════ lot 102/105 : investisseurs nommés — déclencheur = performance, montant = confiance ══════════ */
const INVR=[
 {id:'cr',nm:'Caisse de retraite des Cheminots',ic:'🚂',w0:0.35,out:0.30,inn:0.05,crit:'Régularité',
  rule:"rachète si 3 des 4 derniers trimestres sont négatifs ; souscrit après 4 trimestres positifs d'affilée. Clause de repli : au-delà du repli maximal de votre style, la moitié de sa part."},
 {id:'fs',nm:'Fonds souverain de Nordhavn',ic:'🏛️',w0:0.30,out:0.25,inn:0.08,crit:'Engagement',
  rule:"rachète si l'objectif annoncé est manqué deux trimestres de suite ; souscrit s'il est tenu deux fois de suite (sans annonce : l'objectif du mandat)."},
 {id:'fam',nm:'Family office Vandermeer',ic:'🎩',w0:0.15,out:0.40,inn:0.12,crit:'Absolue',
  rule:"rachète après un trimestre sous −3 % ; souscrit après un trimestre au-dessus de +4 %."},
 {id:'ff',nm:'Fonds de fonds Albatros',ic:'🐦',w0:0.20,out:0.35,inn:0.10,crit:'Relative',
  rule:"rachète si vous finissez 3 points sous la médiane des concurrents ; souscrit 3 points au-dessus."}];
const INVP={abs:[-0.03,0.04],rel:0.03,back:0.05,backLp:60,gate:0.15,gateLp:-6};
function invs(){if(!S.inv)S.inv=INVR.map(d=>({id:d.id,w:d.w0,ntc:0}));return S.inv}
function invD(id){return INVR.find(d=>d.id===id)}
function extNav(){return Math.max(0,S.nav-(S.coinvLock?coinvLocked():0))}
function invFlow(v,amt){const I=invs(),E=extNav(),h=I.map(x=>x.w*E),j=I.indexOf(v);amt=Math.max(-h[j],amt);h[j]+=amt;const E2=E+amt;
 I.forEach((x,q)=>x.w=E2>1e-12?Math.max(0,h[q])/E2:0);S.nav+=amt;S.flows=(S.flows||0)+amt;S.qFlow=(S.qFlow||0)+amt;return amt}
function invDue(){const E=extNav();return invs().reduce((a,v)=>a+(v.ntc>0?v.ntc*v.w*E:0),0)}
function gateOk(){return S.gateUsed!==S.q-1&&invDue()>INVP.gate*extNav()}
/* verdict de chaque investisseur sur l'historique H (du plus ancien au plus récent) : −1 rachat, +1 souscription, 0 rien */
function invVerdict(id,H){const n=H.length,L=H[n-1];if(!n)return 0;
 if(id==='fam')return L.r<INVP.abs[0]?-1:L.r>INVP.abs[1]?1:0;
 if(id==='ff')return L.rel<-INVP.rel?-1:L.rel>INVP.rel?1:0;
 if(id==='fs'){if(n<2)return 0;const a=H[n-2];return !a.ok&&!L.ok?-1:a.ok&&L.ok?1:0}
 const T=H.slice(-4);if(T.length<2)return 0;const neg=T.filter(x=>x.r<0).length;
 return (T.length===4?neg>=3:neg===T.length)?-1:(T.length===4&&neg===0)?1:0}
function invOutF(D){return Math.min(1,D.out*2*(1-S.lp/100)*(SIZE().flowMult||1))}
function invInF(D){return D.inn*S.lp/50*(SIZE().flowIn||1)*Math.max(0,1-capStress())}
function invClose(o){const I=invs(),E0=Math.max(1e-9,extNav());
 const tg=S.comm&&S.comm.ret!=null?S.comm.ret:VOL().goal/4;
 (S.invH=S.invH||[]).push({r:o.r,rel:o.r-o.med,ok:o.r>=tg});if(S.invH.length>8)S.invH.shift();
 let due=0;const R=I.map(v=>{const r={id:v.id,vd:invVerdict(v.id,S.invH),h0:v.w*E0,pay:0,ntc:0,sub:0,cancel:false,gated:0};
  if(v.ntc>0){if(r.vd>0){r.cancel=true;v.ntc=0}else{r.pay=v.ntc*v.w*E0;due+=r.pay}}return r});
 let gf=1;S.qGate=false;
 if(S.gateNext&&due>INVP.gate*E0){gf=INVP.gate*E0/due;S.gateUsed=S.q;S.qGate=true;S.gates=(S.gates||0)+1;S.lp=Math.max(0,S.lp+INVP.gateLp);S.lpD.push(['Gate activée : rachats limités à '+Math.round(INVP.gate*100)+' % de l\'encours',INVP.gateLp])}
 S.gateNext=false;
 R.forEach((r,j)=>{const v=I[j];if(r.pay>0){const p=r.pay*gf;r.gated=r.pay-p;r.pay=-invFlow(v,-p);
  v.ntc=r.gated>1e-12&&v.w*extNav()>1e-12?Math.min(1,r.gated/(v.w*extNav())):0}});
 R.forEach((r,j)=>{const v=I[j],D=invD(v.id);if(v.ntc>0||v.w<1e-6)return;let f=r.vd<0?invOutF(D):0;
  if(v.id==='cr'&&o.ddp>=ddMax()){f=Math.max(f,0.5);r.clause=true}
  if(f>0.002){v.ntc=f;v.ntcQ=S.q;r.ntc=f*v.w*extNav()}});
 R.forEach((r,j)=>{const v=I[j],D=invD(v.id);if(v.ntc>0||r.vd<=0)return;
  if(v.w<0.01){if(!r.pay&&S.lp>=INVP.backLp){r.sub=invFlow(v,INVP.back*S.aum0);r.back=true}return}
  const f=invInF(D);if(f>0.002)r.sub=invFlow(v,f*v.w*extNav())});
 S.invQ=R;const net=R.reduce((a,r)=>a+r.sub-r.pay,0);
 const nm=r=>invD(r.id).nm,P=R.filter(r=>r.pay>0),N=R.filter(r=>r.ntc>0),U=R.filter(r=>r.sub>0),C=R.filter(r=>r.cancel);
 S.poachMsg=[P.length?`Rachats payés : ${P.map(r=>`${nm(r)} −${mm(r.pay)}${r.gated>0?` (gate : ${mm(r.gated)} reportés)`:''}`).join(' · ')}.`:'',
  C.length?`Avis retirés : ${C.map(nm).join(', ')}.`:'',
  N.length?`Avis de rachat déposés, payables à la prochaine clôture : ${N.map(r=>`${nm(r)} ${mm(r.ntc)}${r.clause?' (clause de repli)':''}`).join(' · ')}.`:'',
  U.length?`Souscriptions : ${U.map(r=>`${nm(r)} +${mm(r.sub)}${r.back?' (retour)':''}`).join(' · ')}.`:''].filter(Boolean).join(' ')||'Aucun mouvement d\'investisseur.';
 return net/E0}
function invTable(){const I=invs(),E=extNav(),R=S.invQ||[];
 return `<table class="qt" style="margin-top:12px"><thead><tr><th style="text-align:left">Investisseur</th><th>Part</th><th>Critère</th><th>Mouvement</th></tr></thead><tbody>
 ${I.map(v=>{const D=invD(v.id),r=R.find(x=>x.id===v.id)||{},h=v.w*E;
  const mv=[r.pay>0?`<span class="neg-g">−${mm(r.pay)}</span>`:'',r.sub>0?`<span class="pos-g">+${mm(r.sub)}</span>`:'',r.cancel?'avis retiré':'',v.ntc>0?`<span class="neg-g">avis ${mm(v.ntc*h)}</span>`:''].filter(Boolean).join(' · ')||'—';
  const vd=r.vd<0?'neg-g':r.vd>0?'pos-g':'';
  return `<tr><td style="text-align:left" title="${D.rule}">${D.ic} ${D.nm}</td><td>${h>1e-9?mm(h)+' · '+Math.round(v.w*100)+' %':'parti'}</td><td class="${vd}">${D.crit}</td><td>${mv}</td></tr>`}).join('')}</tbody></table>
 <p class="note" style="margin-top:6px">${INVR.map(D=>`<b>${D.nm}</b> ${D.rule}`).join('<br>')}<br>Le montant dépend de la confiance : un rachat vaut ${Math.round(INVR[0].out*100)} à ${Math.round(INVR[2].out*100)} % de la part à confiance 50, le double à confiance nulle ; une souscription grossit avec la confiance. Un avis est payé à la clôture suivante et tombe si le critère repasse au vert.</p>`}
'''+s[j:]
rep("const tot=invClose({lpMult,ddp:","const tot=invClose({r:qTotal,med,ddp:")
rep("Un avis tombe si l'investisseur remonte à son seuil + ${INVP.cancel}.","Un avis tombe si le critère de l'investisseur repasse au vert d'ici là.")
rep("Chaque investisseur y ajoute son humeur propre ; sous son seuil, il dépose un avis de rachat payé à la clôture suivante.","Chaque investisseur juge sur son critère (régularité, engagement, performance absolue ou relative) ; la confiance fixe le montant de ses rachats et de ses souscriptions.")
open('index.html','w',encoding='utf-8').write(s);print('lot105 p1 ok')
