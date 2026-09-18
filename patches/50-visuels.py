# -*- coding: utf-8 -*-
"""Lot 5 — visuels : un seul dessin de courbe de NAV, réutilisé à l'accueil, à mi-parcours,
à la clôture de trimestre et au rapport final ; accueil refondu (bandeau, courbe, mur des
vingt-cinq marchés, concurrents).

Au passage, correction d'un défaut du tracé final : S.navs commençait à 100 alors que les
encours suivants sont en Md$ (0,1), ce qui dessinait une falaise dès le premier point.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ══ CSS ══
e.rep(""".spineart i{flex:1;display:block;border-radius:1px}""",
""".spineart i{flex:1;display:block;border-radius:1px}
/* courbe de NAV : même dessin à l'accueil, à mi-parcours, à la clôture et au rapport final */
.navc{display:block;width:100%;height:auto}
.navdraw{stroke-dasharray:1600;stroke-dashoffset:1600;animation:navdr 1.6s cubic-bezier(.35,0,.2,1) forwards}
@keyframes navdr{to{stroke-dashoffset:0}}
@media (prefers-reduced-motion:reduce){.navdraw{animation:none;stroke-dashoffset:0}}
.navbox{margin:14px 0 0;padding:10px 10px 7px;border:1px solid var(--line);border-radius:10px;background:linear-gradient(180deg,var(--panel),rgba(21,32,47,0))}
.navrow{display:flex;justify-content:space-between;gap:8px;font-family:var(--mono);font-size:10px;color:var(--dimmer);margin-top:3px}
.navcap{font-family:var(--mono);font-size:10px;color:var(--dimmer);letter-spacing:.05em;margin-bottom:5px}
/* mur des vingt-cinq marchés */
.mwall{display:grid;grid-template-columns:repeat(5,1fr);gap:4px;margin-top:10px}
.mw{font-style:normal;font-family:var(--mono);font-size:9.5px;text-align:center;padding:9px 1px 10px;border-radius:4px;background:var(--panel);border:1px solid var(--line);color:var(--dimmer);position:relative;overflow:hidden}
.mw::after{content:'';position:absolute;left:0;right:0;bottom:0;height:2px;background:var(--c);opacity:.6}
.mw.up{animation:mwp 7s ease-in-out infinite}
.mw.dn{animation:mwn 7s ease-in-out infinite}
@keyframes mwp{0%,70%,100%{color:var(--dimmer);background:var(--panel)}78%,90%{color:var(--long);background:rgba(79,169,140,.14)}}
@keyframes mwn{0%,62%,100%{color:var(--dimmer);background:var(--panel)}70%,86%{color:var(--short);background:rgba(196,87,111,.14)}}
@media (prefers-reduced-motion:reduce){.mw{animation:none}}
/* concurrents de l'accueil */
.rivs{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}
.riv{display:flex;gap:9px;align-items:center;padding:9px;border:1px solid var(--line);border-radius:8px;background:var(--panel)}
.riv .ava{width:38px;height:38px}
.riv b{display:block;font-size:12.5px;line-height:1.2}
.riv span{display:block;font-family:var(--mono);font-size:9px;color:var(--dimmer);margin-top:2px}
.isec{font-family:var(--mono);font-size:11px;color:var(--dimmer);letter-spacing:.06em;margin:26px 0 0;padding-top:16px;border-top:1px solid var(--line)}""")

# ══ helpers de dessin ══
e.rep("""function screenIntro(){""",
"""let NGID=0;
/* Courbe de NAV. Un seul dessin pour tout le jeu : aire dégradée, ligne qui se trace,
   repère au creux, point final. Le viewBox garde son rapport, donc pas de trait déformé. */
function navChart(vals,o){
 o=o||{};
 const v=(vals||[]).filter(x=>isFinite(x));
 if(v.length<2)return '';
 const W=o.w||320,H=o.h||110,pad=9;
 const base=o.base!==undefined?o.base:v[0];
 let lo=Math.min(base,...v),hi=Math.max(base,...v);
 const sp=(hi-lo)||Math.abs(base)*0.1||1;lo-=sp*0.14;hi+=sp*0.14;
 const px=i=>pad+i*(W-2*pad)/(v.length-1);
 const py=x=>H-pad-(x-lo)/(hi-lo)*(H-2*pad);
 const pts=v.map((x,i)=>px(i).toFixed(1)+','+py(x).toFixed(1));
 const col=o.col||(v[v.length-1]>=base?'#4FA98C':'#C4576F');
 const id='ng'+(NGID++);
 const area='M'+pts[0]+' L'+pts.join(' L')+' L'+px(v.length-1).toFixed(1)+','+(H-pad)+' L'+pad+','+(H-pad)+'Z';
 let mk='';
 const mn=Math.min(...v),li=v.indexOf(mn);
 if(o.trough&&mn<base*0.97&&li>0&&li<v.length-1)
  mk+=`<circle cx="${px(li).toFixed(1)}" cy="${py(mn).toFixed(1)}" r="3" fill="#C4576F"><animate attributeName="r" values="3;5.5;3" dur="2.6s" repeatCount="indefinite"/></circle>`;
 mk+=`<circle cx="${px(v.length-1).toFixed(1)}" cy="${py(v[v.length-1]).toFixed(1)}" r="3.2" fill="${col}"/>`;
 return `<svg class="navc" viewBox="0 0 ${W} ${H}" aria-hidden="true">
  <defs><linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${col}" stop-opacity=".32"/><stop offset="1" stop-color="${col}" stop-opacity="0"/></linearGradient></defs>
  <path d="${area}" fill="url(#${id})"/>
  <line x1="0" y1="${py(base).toFixed(1)}" x2="${W}" y2="${py(base).toFixed(1)}" stroke="#35496A" stroke-width="1" stroke-dasharray="3 4"/>
  <polyline class="${o.anim?'navdraw':''}" points="${pts.join(' ')}" fill="none" stroke="${col}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
  ${mk}</svg>`;
}
/* la performance nette cumulée, base 100 — exactement ce que lit la jauge « Perf. » */
function idxSeries(extra){
 const a=[1];(S.rets||[]).forEach(r=>a.push(a[a.length-1]*(1+r)));
 if(extra!==undefined&&isFinite(extra))a.push(a[a.length-1]*(1+extra));
 return a.map(x=>x*100);
}
function navBox(cap,vals,o){
 o=o||{};if(!vals||vals.length<2)return '';
 const last=vals[vals.length-1],base=vals[0];
 let pk=base,dd=0;vals.forEach(v=>{pk=Math.max(pk,v);dd=Math.max(dd,1-v/pk)});
 return `<div class="navbox"><div class="navcap">${cap}</div>${navChart(vals,o)}
  <div class="navrow"><span>DÉPART ${dec(base,0)}</span><span class="${dd>0.005?'neg-g':'dim-g'}">${dd>0.005?'REPLI MAX −'+dec(dd*100,1)+' %':'AUCUN REPLI'}</span><span class="${last>=base?'pos-g':'neg-g'}">${last>=base?'+':'−'}${dec(Math.abs(last/base-1)*100,1)} %${o.prov?' LATENT':''}</span></div></div>`;
}
/* la courbe de l'accueil : une partie imaginaire, toujours la même */
function heroNav(){
 const st=[1.9,2.6,-0.7,3.4,1.9,4.2,1.1,-2.6,-5.8,-4.4,-6.3,-2.1,1.5,3.2,2.1,4.6,3.0,5.2,2.4,3.9,4.7,6.4];
 const a=[100];st.forEach(x=>a.push(a[a.length-1]*(1+x/100)));return a;
}
function introTicker(){
 const T=["OUVERTURE DE MANDAT","BRENT \\u25B23,2\\u00a0%","RUMEUR : LA BANQUE CENTRALE AVANCERAIT SON CALENDRIER","YEN \\u25BC1,8\\u00a0%",
  "LE COMIT\\u00c9 DES RISQUES DEMANDE UN POINT DANS L'HEURE","M\\u00c9DAILLON D'OR \\u25B24,1\\u00a0% SUR LE TRIMESTRE","BITCOIN \\u25BC6,4\\u00a0%",
  "UN TRADER D\\u00c9MISSIONNE PAR MESSAGE VOCAL","OR \\u25B20,9\\u00a0%","APPEL DE MARGE CHEZ UN CONCURRENT","LE MARCH\\u00c9 VOUS ATTEND"];
 const line=T.join('   \\u00b7   ')+'   \\u00b7   ';
 return `<div class="tick" style="margin:0 -14px 18px"><span class="tlab">DIRECT</span><div class="twrap"><div class="tmove">${line}${line}</div></div></div>`;
}
function mktWall(){
 const ord=['Actions','Taux','Devises','Matières premières','Exotiques'];
 return `<div class="mwall">${INSTR_ALL.slice().sort((a,b)=>ord.indexOf(a.grp)-ord.indexOf(b.grp)||a.rk-b.rk)
  .map((x,i)=>`<i class="mw ${Math.sin(i*2.7)>0?'up':'dn'}" style="--c:${GRPC[x.grp]};animation-delay:${((i*3)%11)*0.6}s">${x.sym}</i>`).join('')}</div>`;
}
function introRivals(){
 return `<div class="rivs">${RIVALS.map(r=>`<div class="riv">${avatar(r.boss,'rival')}<div><b>${r.boss}</b><span>${r.nm.toUpperCase()}</span></div></div>`).join('')}</div>`;
}
function screenIntro(){""")

# ══ l'écran d'accueil ══
old=e.s[e.s.index("function screenIntro(){\n if(!fundName)"):e.s.index("function feeLine(){")]
e.rep(old,"""function screenIntro(){
 if(!fundName)fundName=randName();
 const nv=heroNav();let pk=nv[0],dd=0;nv.forEach(v=>{pk=Math.max(pk,v);dd=Math.max(dd,1-v/pk)});
 app.innerHTML=`<div class="splash fade">
  ${introTicker()}
  <div class="kicker" style="color:var(--gold)">BIENVENUE À BORD</div>
  <h1 class="splash-h1">Vous prenez les commandes<br>d'un <em>fonds global macro</em></h1>
  <div class="navbox">
   <div class="navcap">UNE PARTIE, HUIT TRIMESTRES</div>
   ${navChart(nv,{col:'#D9B06A',anim:1,trough:1,h:118})}
   <div class="navrow"><span>DÉPART ${dec(nv[0],0)}</span><span class="neg-g">REPLI −${dec(dd*100,0)} %</span><span class="pos-g">ARRIVÉE ${dec(nv[nv.length-1],0)}</span></div>
  </div>
  <p class="splash-p"><b style="color:var(--gold)">Le but : encaisser un maximum de commissions en deux ans sans vous faire débarquer.</b> Ce matin, le conseil vous a confié le book. Des marchés à tenir, quatre concurrents qui n'attendent que votre faux pas, des investisseurs qui vous adorent tant que ça monte, et un comité des risques qui vous surveille. À vous de choisir la taille du fonds — et donc la difficulté.</p>
  <div class="namebox">
   <div class="kicker">D'ABORD, UN NOM POUR VOTRE FONDS</div>
   <input id="fname" class="namein" value="${fundName}" maxlength="42" spellcheck="false" autocomplete="off">
   <div class="namerow"><button class="cta ghost" id="shuffle" style="margin:0">Proposez-m'en un</button></div>
  </div>
  <button class="cta gold" id="found">Fonder le fonds</button>
  ${hasSave()?`<button class="cta ghost" id="resume">Reprendre la partie en cours</button><button class="cta ghost" id="dropsave" style="margin-top:6px;font-size:12px;opacity:.6">Abandonner cette partie</button>`:''}
  <button class="cta ghost" id="hall">Palmarès et hauts faits</button>
  <div class="isec">LES VINGT-CINQ MARCHÉS</div>
  <p class="splash-p" style="margin-top:8px">Actions, taux, devises, matières premières, et quelques objets moins recommandables. La taille de votre fonds décide de ceux qui vous sont ouverts.</p>
  ${mktWall()}
  <div class="isec">CEUX D'EN FACE</div>
  <p class="splash-p" style="margin-top:8px">Quatre fonds jouent le même trimestre que vous. Vos investisseurs comparent — et c'est l'écart à la médiane qui décide des rachats, pas votre performance absolue.</p>
  ${introRivals()}
  <p class="splash-p" style="margin:18px 0 0">Le monde ne vous attendra pas : guerres, élections, sécheresses, faillites, rumeurs de couloir et traders à fort caractère. Vous allez adorer. Ou pas.</p>
 </div>`;
 const inp=document.getElementById('fname');
 inp.oninput=()=>{fundName=inp.value};
 document.getElementById('shuffle').onclick=()=>{fundName=randName();inp.value=fundName};
 document.getElementById('found').onclick=()=>{fundName=(inp.value||'').trim()||randName();screenSetup();window.scrollTo(0,0)};
 const rb=document.getElementById('resume');
 if(rb)rb.onclick=()=>{if(!loadGame())toast('Cette sauvegarde est inutilisable. Vous pouvez abandonner la partie et en lancer une nouvelle.')};
 const db=document.getElementById('dropsave');
 if(db)db.onclick=()=>{clearSave();toast('Partie abandonnée.');screenIntro()};
 document.getElementById('hall').onclick=()=>screenHall(screenIntro);
}
""")

# ══ la courbe en jeu ══
e.rep("""  <div class="rescard"><h3>${title}</h3><p>${head}</p>""",
      """  <div class="rescard"><h3>${title}</h3>${(extra&&extra.top)||''}<p>${head}</p>""")
e.rep("""  [['Jauges',`<span class="${cls(g.lp)}">${sd1(g.lp)}</span> · <span class="${cls(g.rc)}">${sd1(g.rc)}</span>`]],
  "Poursuivre le trimestre",stepEvents);""",
"""  [['Jauges',`<span class="${cls(g.lp)}">${sd1(g.lp)}</span> · <span class="${cls(g.rc)}">${sd1(g.rc)}</span>`]],
  "Poursuivre le trimestre",stepEvents,
  {top:navBox(`PERFORMANCE NETTE CUMULÉE · T1 À T${S.q+1} EN COURS`,idxSeries(p*0.5),{anim:1,trough:1,prov:1})});""")
e.rep("""  <div class="regime">${R.nm}</div><div class="sub">${R.d}</div></div>""",
"""  <div class="regime">${R.nm}</div><div class="sub">${R.d}</div></div>
  ${navBox(`PERFORMANCE NETTE CUMULÉE · ${S.q} TRIMESTRE${S.q>1?'S':''}`,idxSeries(),{anim:1,trough:1})}""")

# ══ rapport final : même courbe, et fin du tracé cassé ══
e.rep(""" const W=340,H=120,pad=5;
 const series=[S.navs.map(v=>v/100),...S.rivals.map(rv=>{let c=[1];S.rets.forEach((_,i)=>c.push(c[i]*(1+(rv.hist?rv.hist[i]:0))));return c})];
 const lo=Math.min(...S.navs)/100*0.99,hi=Math.max(...S.navs)/100*1.01;
 const px=i=>pad+i*(W-2*pad)/Math.max(1,S.navs.length-1),py=v=>H-pad-(v-lo)/(hi-lo||1)*(H-2*pad);
 const pts=S.navs.map((v,i)=>`${px(i).toFixed(1)},${py(v/100).toFixed(1)}`).join(' ');
""","")
e.rep("""  <svg class="curve" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none">
   <line x1="0" y1="${py(1)}" x2="${W}" y2="${py(1)}" stroke="#35496A" stroke-width="1" stroke-dasharray="3 3"/>
   <polyline points="${pts}" fill="none" stroke="${tot>=1?'#4FA98C':'#C4576F'}" stroke-width="2" stroke-linejoin="round"/></svg>""",
"""  ${navBox(`PERFORMANCE NETTE CUMULÉE · ${n} TRIMESTRE${n>1?'S':''}`,idxSeries(),{anim:1,trough:1,h:130})}""")

e.done("lot 5 — visuels")
