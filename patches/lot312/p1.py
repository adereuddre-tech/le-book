p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
CAT=open('patches/lot312/cat.js',encoding='utf-8').read()
a=s.index("const ATK={p0:0.55");b=s.index("function atkClose()",a)
NEW=CAT+r"""
/* lot 312 : la manœuvre de l'activiste se joue hors du book, chaque trimestre. Trois occasions du livre noir, mise de 1 à 5 %
   de l'encours, probabilité et multiple affichés ; verdict à la clôture. Trois réussites d'affilée à mises croissantes
   ouvrent le coup du siècle : mise de 5 à 15 %, gain jusqu'à huit fois la mise. */
const BK={stakes:[0.01,0.02,0.03,0.04,0.05],cds:[0.05,0.10,0.15],W:8,pCds:0.45,rec:12};
const ATK={};
function bkKind(f,d){return {fx:d>0?'short squeeze':'attaque contre la banque centrale',dt:d>0?'short squeeze':'attaque de la dette',ix:d>0?'short squeeze':'raid baissier',sk:d>0?'gamma squeeze':'raid baissier',cm:d>0?'corner':'long squeeze',od:d>0?'corner':'long squeeze'}[f]||'manœuvre'}
function atkReady(){return PROF().atk&&!(S.atk&&S.atk.q===S.q)}
function bkOffers(){if(S.bkOff&&S.bkOff.q===S.q)return S.bkOff.L;const u=prng32(hash32('bk'+S.q,S.seed)),rec=S.bkRec||[],C=BKCAT.filter(x=>!rec.includes(x[0])),L=[];
 while(L.length<3&&C.length){const x=C.splice(Math.floor(u()*C.length),1)[0];L.push({c:x[0],nm:x[1],f:x[2],ctx:x[3],d:u()<0.5?1:-1,p:Math.round((0.45+0.20*u())*20)/20,W:Math.round((1.6+0.6*u())*10)/10})}
 if((S.bkStreak||0)>=3){const x=BKCDS[Math.floor(u()*BKCDS.length)];L.unshift({c:x[0],nm:x[1],f:'cds',ctx:x[3],d:x[2],p:BK.pCds,W:BK.W,cds:1})}
 S.bkOff={q:S.q,L};return L}
function styDrawX(){const P=PROF();if(!P.atk)return '';const st=S.bkStreak||0,ser=st>=3?'<b class="gold-g">le coup du siècle est sur la table</b>':`série : ${st} réussite${st>1?'s':''} à mises croissantes — ${3-st} de plus pour le coup du siècle`;
 if(S.atk&&S.atk.q===S.q){const a=S.atk;return `<div class="blockhead"><h2>Le livre noir</h2><span class="hint">manœuvre lancée</span></div><p class="note" style="margin:0">${a.cds?`👑 <b>Coup du siècle</b> : ${a.nm}`:`🦅 ${a.kind} sur <b>${a.nm}</b>`}, ${Math.round(a.st*100)} % de l'encours en jeu. Réussite ${Math.round(a.p*100)} %, gain ${dec(a.W,1)} fois la mise ; verdict à la clôture. ${ser}.</p>`}
 const L=bkOffers();if(S.bkSel==null||S.bkSel>=L.length)S.bkSel=0;const o=L[S.bkSel],SK=o.cds?BK.cds:BK.stakes;if(!SK.includes(S.bkSt))S.bkSt=SK[o.cds?0:2];const sk=S.bkSt;
 return `<div class="blockhead"><h2>Le livre noir</h2><span class="hint">une manœuvre par trimestre · hors du book</span></div>
  <p class="note" style="margin:0 0 6px">Des marchés que votre book ne touche pas : votre desk y repère trois occasions. La manœuvre ne pèse ni sur le risque, ni sur la marge du book ; seul le résultat compte, à la clôture. ${ser}.</p>
  ${L.map((x,j)=>`<button class="pwb${j===S.bkSel?' on':''}" data-bk="${j}"><b>${x.cds?`👑 Coup du siècle · ${x.nm}`:`${x.d>0?'▲':'▼'} ${x.nm} · ${bkKind(x.f,x.d)}`}</b><small>${x.ctx} <i>· réussite ${Math.round(x.p*100)} % · gain ${dec(x.W,1)} × la mise</i></small></button>`).join('')}
  <div class="cisel" style="margin-top:6px">${SK.map(k=>`<button class="hgp${k===sk?' on':''}" data-bks="${k}">${Math.round(k*100)} %</button>`).join('')}</div>
  <div class="attr"><span class="an">Mise ${mm(sk*S.nav)} · réussite ${Math.round(o.p*100)} %</span><span class="av"><b class="pos-g">+${mm(o.W*sk*S.nav)}</b> / <b class="neg-g">−${mm(sk*S.nav)}</b></span></div>
  <button class="buy" id="atkgo" style="margin-top:6px"${S.phase==='book'?'':' disabled'}>${o.cds?'👑 Lancer le coup du siècle':`Lancer : ${bkKind(o.f,o.d)} sur ${o.nm}`}</button>`}
function styWire(el){el.querySelectorAll('[data-bk]').forEach(b=>b.onclick=()=>{S.bkSel=+b.dataset.bk;styDraw()});el.querySelectorAll('[data-bks]').forEach(b=>b.onclick=()=>{S.bkSt=+b.dataset.bks;styDraw()});
 const g=el.querySelector('#atkgo');if(g)g.onclick=()=>{if(!atkReady()||S.phase!=='book')return;const o=bkOffers()[S.bkSel||0],st=S.bkSt;
  S.atk={q:S.q,c:o.c,nm:o.nm,d:o.d,p:o.p,W:o.W,st,cds:!!o.cds,kind:o.cds?o.nm:bkKind(o.f,o.d)};(S.bkRec=S.bkRec||[]).push(o.c);S.bkRec=S.bkRec.slice(-BK.rec);
  gauge(0,o.cds?-3:-1,"Le comité apprend votre manœuvre");toast(`🦅 ${o.cds?'Coup du siècle lancé':'Manœuvre lancée'} : <b>${o.nm}</b>`);styDraw()}}
function atkResolve(){const a=S.atk;if(!a||a.q!==S.q||(S.atkRes&&S.atkRes.q===S.q))return;   /* un résultat par trimestre (le précédent restait affiché) */const ok=prng32(hash32('atk'+S.q,S.seed))()<a.p,x=ok?a.W*a.st:-a.st,nb=S.nav;
 S.nav*=(1+x);S.qEvM=(S.qEvM||0)+x*nb;S.evLog.push({t:`${a.cds?'Coup du siècle':'Manœuvre'} : ${a.nm}`,pnl:x,m:x*nb,lp:0,rc:0});
 if(a.cds)S.bkStreak=0;else if(ok){S.bkStreak=(S.bkStreak||0)>0&&a.st>(S.bkLast||0)?S.bkStreak+1:1;S.bkLast=a.st}else{S.bkStreak=0;S.bkLast=0}
 S.atkRes={q:S.q,ok,x,nm:a.nm,sym:a.c,kind:a.kind,cds:a.cds,st:a.st};if(ok)S.atkWins=(S.atkWins||0)+1}
function screenAtk(){S.atkRes=null;atkResolve();const R=S.atkRes,a=S.atk;
 app.innerHTML=statusBar()+`<div class="evwrap fade"><div class="evcard${R.ok?'':' bad'}">${evHead('Votre desk · clôture','news')}<h3>${R.cds?`👑 ${R.nm} : ${R.ok?'réussi !':'raté'}`:`🦅 Manœuvre sur ${R.nm} : ${R.ok?'réussie':'ratée'}`}</h3>
  <p class="note" style="margin:0 0 6px">${R.cds?'Le coup du siècle':R.kind[0].toUpperCase()+R.kind.slice(1)} · ${Math.round(R.st*100)} % de l'encours en jeu</p>
  <p>${R.ok?(R.cds?`On en parlera dans les manuels : les contreparties capitulent les unes après les autres, et le marché cède d'un coup. Le fonds encaisse ${dec(a.W,1)} fois la mise.`:`Les contreparties cèdent avant la clôture : le marché ${a.d>0?'s’envole':'décroche'} et vous sortez au meilleur moment.`):(R.cds?`Les autorités tiennent, et le marché vous broie. La mise est perdue ; la légende attendra.`:`Les contreparties ont tenu : le marché ${a.d>0?'retombe':'rebondit'}, et la mise est perdue.`)}</p>
  <div class="gzr"><span>effet sur le fonds</span><b class="${cls(R.x)}">${R.x>=0?'+':'−'}${mm(Math.abs(R.x)*S.nav/(1+R.x))} · ${sgnp(R.x,2)}</b></div>
  ${!R.cds&&R.ok&&(S.bkStreak||0)>=3?'<p class="note" style="margin:6px 0 0">👑 Trois réussites d’affilée à mises croissantes : le coup du siècle vous sera proposé au prochain trimestre.</p>':''}</div>
  <button class="cta" id="ok">Continuer</button></div>`;
 document.getElementById('ok').onclick=()=>{stepEvents();window.scrollTo(0,0)}}
function atkLocked(i){return false}   /* lot 312 : plus de ligne dans le book */
"""
s=s[:a]+NEW+s[b:]
rep("""function atkClose(){if(!(S.atk&&S.atk.q===S.q))S.atkRes=null;else atkResolve()}   /* lot 303 : la manœuvre se joue sur son écran ; filet si l'écran n'a pas été vu */""",
    """function atkClose(){if(!(S.atk&&S.atk.q===S.q))S.atkRes=null;else atkResolve()}   /* filet si l'écran n'a pas été vu */""")
rep(" if(S.atk&&S.atk.q===S.q)S.k[S.atk.i]=S.atk.d*S.atk.m;   /* lot 308 : la manœuvre impose sa ligne, quoi qu'aient fait les boutons du book */\n","")
rep("function kCap(i){return mktOpen(i)?Math.max((S&&S.maxk)||5,(S&&S.atk&&S.atk.q===S.q&&S.atk.i===i)?S.atk.m:0):0}   /* lot 303 */","function kCap(i){return mktOpen(i)?((S&&S.maxk)||5):0}")
# confiance et comité : petits effets chaque trimestre, gros pour le coup du siècle
rep("""S.atkRes.ok?15:-10]);""","""S.atkRes.ok?(S.atkRes.cds?15:3):(S.atkRes.cds?-10:-3)]);""")
rep("""if(S.atkRes&&!S.atkRes.ok)rcD.push(['Manœuvre ratée : le comité demande des comptes',-5]);""","""if(S.atkRes&&!S.atkRes.ok)rcD.push(['Manœuvre ratée : le comité demande des comptes',S.atkRes.cds?-5:-2]);""")
# textes du style
rep("""pw:"la manœuvre : une fois par an, un corner ou un squeeze qui force le marché dans votre sens\"""","""pw:"le livre noir : chaque trimestre, un corner ou un squeeze hors du book — et, après trois réussites, le coup du siècle\"""")
a2=s.index("<b>Pouvoir propre — la manœuvre</b>");b2=s.index('"]',a2)
s=s[:a2]+"""<b>Pouvoir propre — le livre noir</b> : chaque trimestre, trois occasions sur des marchés que le book ne touche pas (roupie, bonos argentins, cacao, Volkswagen, GameStop…). Mise de 1 à 5 % de l'encours, réussite de 45 à 65 %, gain de 1,6 à 2,2 fois la mise, sans peser sur le risque ni la marge. Trois réussites d'affilée à mises croissantes : le coup du siècle, jusqu'à 15 % de l'encours pour huit fois la mise"""+s[b2:]
rep("""act:"une manœuvre par an : corner ou squeeze sur n'importe quel marché\"""","""act:"le livre noir : un corner ou un squeeze par trimestre, hors du book\"""")
open(p,'w',encoding='utf-8').write(s)
