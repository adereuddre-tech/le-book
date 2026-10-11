p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# 1. la mécanique : une position de ±3 à ±5 sur l'un des trois marchés au signal le plus net ; à la clôture, un événement spécial
#    pousse le marché dans votre sens — il renforce le mouvement, ou le retourne s'il partait contre vous
a=s.index("/* lot 272 : l'attaque du macro activiste */");b=s.index("function pwHere(o)",a)
s=s[:a]+r"""/* lot 303 : la manœuvre de l'activiste — n'importe quel marché, à la hausse (corner, short squeeze) ou à la baisse
   (long squeeze, attaque contre une banque centrale). Une fois par an, dès le premier trimestre : position de ±3, ±4 ou ±5
   sur l'un des trois marchés au signal le plus net. À la clôture, un événement spécial : réussi, le marché finit dans votre sens
   (mouvement renforcé de 1,2 σ, ou retourné s'il partait contre vous) ; raté, il vous résiste d'une demi-σ. */
const ATK={p0:0.55,pm:0.05,read:0.10,A:1.2,back:0.5};
function atkReady(){return PROF().atk&&!(S.atk&&S.atk.q===S.q)&&(S.atkLast==null||S.q-S.atkLast>=4)}
function atkCands(){return INSTR.map((x,i)=>i).filter(i=>mktOpen(i)).sort((a,b)=>Math.abs(expRet(b).m)/INSTR[b].sigQ-Math.abs(expRet(a).m)/INSTR[a].sigQ).slice(0,3)}
function atkP(i,d,m){return Math.min(0.9,ATK.p0+ATK.pm*(m-3)+(Math.sign(expRet(i).m)===d?ATK.read:0))}
function atkKind(i,d){const g=INSTR[i].grp;return d>0?(g==='Matières premières'?'corner':'short squeeze'):(g==='Devises'||g==='Taux'?'attaque contre la banque centrale':'long squeeze')}
function atkGain(i,d,m){return m*U/INSTR[i].sig*ATK.A*INSTR[i].sigQ}   /* ordre de grandeur du gain de la manœuvre seule, en part de l'encours */
function styDrawX(){const P=PROF();if(!P.atk)return '';
 if(S.atk&&S.atk.q===S.q){const a=S.atk;return `<div class="blockhead"><h2>La manœuvre</h2><span class="hint">lancée</span></div><p class="note" style="margin:0">🦅 ${atkKind(a.i,a.d)[0].toUpperCase()+atkKind(a.i,a.d).slice(1)} sur <b>${INSTR[a.i].nm}</b> : position ${a.d>0?'+':'−'}${a.m}. Réussite ${Math.round(a.p*100)} % ; verdict à la clôture, lors d'un événement spécial.</p>`}
 if(!atkReady())return `<div class="blockhead"><h2>La manœuvre</h2><span class="hint">une par an</span></div><p class="note" style="margin:0">Prochaine manœuvre possible au trimestre ${(S.atkLast||0)+5}.</p>`;
 const C=atkCands();if(!C.length)return '';if(!C.includes(S.atkSel))S.atkSel=C[0];const i=S.atkSel;
 if(S.atkD==null||S.atkSelD!==i){S.atkD=Math.sign(expRet(i).m)||1;S.atkSelD=i}S.atkM=S.atkM||4;const d=S.atkD,m=S.atkM,p=atkP(i,d,m),g=atkGain(i,d,m);
 return `<div class="blockhead"><h2>La manœuvre</h2><span class="hint">une par an · votre pouvoir</span></div>
  <p class="note" style="margin:0 0 6px">Les trois marchés où votre desk lit le signal le plus net. Prenez position : à la clôture, vous pesez sur le marché pour qu'il finisse dans votre sens. Plus la position est grosse, plus la manœuvre a de chances de réussir ; dans le sens du signal, +10 pts.</p>
  <div class="cisel">${C.map(j=>{const e=expRet(j).m;return `<button class="hgp${j===i?' on':''}" data-atk="${j}">${INSTR[j].sym} ${e>=0?'▲':'▼'}</button>`}).join('')}</div>
  <div class="cisel" style="margin-top:6px"><button class="hgp${d>0?' on':''}" data-atd="1">▲ ${atkKind(i,1)}</button><button class="hgp${d<0?' on':''}" data-atd="-1">▼ ${atkKind(i,-1)}</button></div>
  <div class="cisel" style="margin-top:6px">${[3,4,5].map(k=>`<button class="hgp${k===m?' on':''}" data-atm="${k}">${d>0?'+':'−'}${k}</button>`).join('')}</div>
  <div class="attr"><span class="an">Position ${d>0?'+':'−'}${m} sur ${INSTR[i].nm} · réussite ${Math.round(p*100)} %</span><span class="av"><b class="pos-g">≈ +${mm(g*S.nav)}</b> / <b class="neg-g">≈ −${mm(g*ATK.back/ATK.A*S.nav)}</b></span></div>
  <p class="note" style="margin:2px 0 0">En plus du mouvement propre du marché. La ligne remplace votre position actuelle sur ${INSTR[i].sym} ; le comité apprend la manœuvre (contrôle −2).</p>
  <button class="buy" id="atkgo" style="margin-top:6px"${S.phase==='book'?'':' disabled'}>Lancer : ${atkKind(i,d)} sur ${INSTR[i].sym}</button>`}
function styWire(el){el.querySelectorAll('[data-atk]').forEach(b=>b.onclick=()=>{S.atkSel=+b.dataset.atk;styDraw()});el.querySelectorAll('[data-atd]').forEach(b=>b.onclick=()=>{S.atkD=+b.dataset.atd;styDraw()});el.querySelectorAll('[data-atm]').forEach(b=>b.onclick=()=>{S.atkM=+b.dataset.atm;styDraw()});
 const g=el.querySelector('#atkgo');if(g)g.onclick=()=>{if(!atkReady()||S.phase!=='book')return;const i=S.atkSel,d=S.atkD,m=S.atkM;S.atk={q:S.q,i,d,m,p:atkP(i,d,m)};S.atkLast=S.q;S.k[i]=d*m;
  gauge(0,-2,"Le comité apprend votre manœuvre");toast(`🦅 Manœuvre lancée : ${atkKind(i,d)} sur <b>${INSTR[i].nm}</b>`);
  try{drawRows();renderRisk();refreshSend();refreshGain();renderTC&&renderTC()}catch(e){}styDraw()}}
/* l'événement spécial, à la clôture, après les dépêches */
function atkResolve(){const a=S.atk;if(!a||a.q!==S.q||S.atkRes)return;const ok=prng32(hash32('atk'+S.q,S.seed))()<a.p,i=a.i,d=a.d,o=S.rBase[i],sq=INSTR[i].sigQ;
 const n=ok?d*(Math.max(0,d*o)+ATK.A*sq):o-d*ATK.back*sq;S.rBase[i]=n;const x=weights(S.k)[i]*(n-o);
 S.atkRes={ok,x,nm:INSTR[i].nm,sym:INSTR[i].sym,kind:atkKind(i,d),o,n,rev:ok&&d*o<0};if(ok)S.atkWins=(S.atkWins||0)+1}
function screenAtk(){atkResolve();const R=S.atkRes,K=R.kind[0].toUpperCase()+R.kind.slice(1);
 app.innerHTML=statusBar()+`<div class="evwrap fade"><div class="evcard${R.ok?'':' bad'}">${evHead('Votre desk · clôture','news')}<h3>🦅 Manœuvre sur ${R.nm} : ${R.ok?'réussie':'ratée'}</h3><p class="note" style="margin:0 0 6px">${K}</p>
  <p>${R.ok?(R.rev?`Le marché partait contre vous (${sgn(R.o,1)}) : votre manœuvre le retourne, il finit à ${sgn(R.n,1)}.`:`Le marché allait déjà dans votre sens : votre manœuvre l'emballe, il finit à ${sgn(R.n,1)} au lieu de ${sgn(R.o,1)}.`):`Les contreparties ont tenu, et elles vous font payer l'audace : ${R.sym} finit à ${sgn(R.n,1)} au lieu de ${sgn(R.o,1)}.`}</p>
  <div class="gzr"><span>effet de la manœuvre sur le fonds</span><b class="${cls(R.x)}">${R.x>=0?'+':'−'}${mm(Math.abs(R.x)*S.nav)} · ${sgnp(R.x,2)}</b></div></div>
  <button class="cta" id="ok">Continuer</button></div>`;
 document.getElementById('ok').onclick=()=>{stepEvents();window.scrollTo(0,0)}}
function atkClose(){if(!(S.atk&&S.atk.q===S.q))S.atkRes=null;else atkResolve()}   /* lot 303 : la manœuvre se joue sur son écran ; filet si l'écran n'a pas été vu */
"""+s[b:]
# 2. la ligne de la manœuvre peut dépasser votre plafond de position
rep("function kCap(i){return mktOpen(i)?((S&&S.maxk)||5):0}","function kCap(i){return mktOpen(i)?Math.max((S&&S.maxk)||5,(S&&S.atk&&S.atk.q===S.q&&S.atk.i===i)?S.atk.m:0):0}   /* lot 303 */")
# 3. l'écran de la manœuvre, après les dépêches
rep(""" if(!S.tailDone){if(S.tailEv===null||S.tailEv===undefined)S.tailEv=tailDraw()||0;""",""" if(S.atk&&S.atk.q===S.q&&S.atkShown!==S.q){S.atkShown=S.q;screenAtk();window.scrollTo(0,0);return}   /* lot 303 */
 if(!S.tailDone){if(S.tailEv===null||S.tailEv===undefined)S.tailEv=tailDraw()||0;""")
# 4. textes
rep("""pw:"l'attaque : une fois par an, un pari géant contre une banque centrale\"""","""pw:"la manœuvre : une fois par an, un corner ou un squeeze qui force le marché dans votre sens\"""")
rep("""<b>Pouvoir propre — l'attaque</b> : une fois par an, vous misez 5, 10 ou 15 % de l'encours contre une monnaie. Plus la mise est grosse, plus la banque centrale risque de céder (30 à 50 %, +10 pts si votre desk lit déjà la monnaie faible). Réussie : 1,2 fois la mise, et la légende. Ratée : la mise perdue, et le comité furieux""",
    """<b>Pouvoir propre — la manœuvre</b> : une fois par an, dès le premier trimestre, une position de ±3, ±4 ou ±5 sur l'un des trois marchés au signal le plus net, à la hausse (corner, short squeeze) ou à la baisse (long squeeze, attaque contre une banque centrale). À la clôture, un événement spécial : réussie (55 à 75 %, +10 pts dans le sens du signal), le marché finit dans votre sens, renforcé de 1,2 σ ou retourné ; ratée, il vous résiste d'une demi-σ, et le comité est furieux""")
rep("""act:"une attaque de monnaie par an\"""","""act:"une manœuvre par an : corner ou squeeze sur n'importe quel marché\"""")
rep("""lpD.push([S.atkRes.ok?`L'attaque sur ${S.atkRes.nm} a réussi : la banque centrale a cédé`:`L'attaque sur ${S.atkRes.nm} a échoué : la banque centrale a tenu`,S.atkRes.ok?15:-10]);""",
    """lpD.push([S.atkRes.ok?`Manœuvre réussie sur ${S.atkRes.nm} (${S.atkRes.kind})`:`Manœuvre ratée sur ${S.atkRes.nm} (${S.atkRes.kind})`,S.atkRes.ok?15:-10]);""")
rep("""rcD.push(['Attaque ratée : le comité demande des comptes',-5]);""","""rcD.push(['Manœuvre ratée : le comité demande des comptes',-5]);""")
rep("""S.atkRes.ok?pk([`${F} a fait plier la banque centrale : ${S.atkRes.nm} décroche, le fonds encaisse ${sgnp(S.atkRes.x,1)}. On parle déjà de « l'homme qui a cassé » la monnaie`,`Coup de maître de ${F} contre ${S.atkRes.nm} : la banque centrale abandonne la défense de sa monnaie`],56):pk([`La banque centrale a tenu : ${F} perd ${sgnp(S.atkRes.x,1)} sur son attaque contre ${S.atkRes.nm}. Le gouverneur savoure`,`${F} se casse les dents sur ${S.atkRes.nm} : les réserves étaient plus profondes que prévu`],57));""",
    """S.atkRes.ok?pk([`${F} réussit sa manœuvre sur ${S.atkRes.nm} (${S.atkRes.kind}) : le fonds encaisse ${sgnp(S.atkRes.x,1)}. On parle déjà de « l'homme qui a fait plier » le marché`,`Coup de maître de ${F} sur ${S.atkRes.nm} : les contreparties ont dû céder`],56):pk([`Les contreparties ont tenu : ${F} perd ${sgnp(S.atkRes.x,1)} sur sa manœuvre ratée sur ${S.atkRes.nm} (${S.atkRes.kind})`,`${F} se casse les dents sur ${S.atkRes.nm} : le marché était plus profond que prévu`],57));""")
open(p,'w',encoding='utf-8').write(s)
