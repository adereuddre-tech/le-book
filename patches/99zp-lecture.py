# -*- coding: utf-8 -*-
"""Lot 54 — lecture du book : attendu du book toujours visible, gain attendu par unité,
contribution au risque, signaux dans le même ordre pour tous, décomposition dans le détail.

  - Le rendement attendu du book passe dans la barre d'état, sous « Risque » : visible sur tous
    les écrans du trimestre (dosé par la difficulté). L'encadré du book, redondant, disparaît.
  - Par marché, la barre (qui n'apportait rien) est remplacée par une ligne :
      par unité  — le gain attendu pour le fonds d'une unité de position (w₁ × attendu du marché),
                   ± 2σ en facile ; sens et conviction en difficile ;
      risque     — en points de volatilité du portefeuille : la contribution du marché au risque
                   affiché (contributions d'Euler, remises à l'échelle du risque majoré pour que
                   leur somme égale le chiffre de la barre d'état). Positive, le marché ajoute du
                   risque ; négative, il diversifie. Sans position, l'effet d'une unité ajoutée.
  - Signaux : toujours dans l'ordre Tendance · Portage · Valeur ; celui du style en gras léger,
    les deux autres pleinement lisibles.
  - Le détail d'un marché agrège tout : chaque facteur (exposition × lecture des sources → effet),
    chaque signal (estimation → effet, catalyseur compris), la dérive, l'attendu, l'intervalle
    ± 2σ, le gain par unité et la contribution au risque. La densité tracée utilise désormais
    cet attendu et cette incertitude (elle ne comptait que les signaux).
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
def between(a,b):
    assert e.s.count(a)==1,'debut ambigu %r'%a[:60]
    i=e.s.index(a); j=e.s.index(b,i); return e.s[i:j]
# ── décomposition de l'attendu ────────────────────────────────────────────────
e.rep("function expBook(k){","""/* L'attendu d'un marché, morceau par morceau (mêmes termes que expRet). */
function expParts(i){
 const x=INSTR[i],f=S.factEst||[0,0,0,0],e=S.tcvEst||{t:[],c:[],v:[]},ed=UNIV().edge||1;
 const cv=(S.prof==='fonda'&&S.cat&&S.cat.includes(i))?2:1;
 return {fac:x.b.map((b,k)=>({b,f:f[k],v:x.sigQ*b*f[k]})),
  t:x.sigQ*SIGW.t*(e.t[i]||0)*ed,c:x.sigQ*SIGW.c*(e.c[i]||0)*ed,v:x.sigQ*SIGW.v*cv*(e.v[i]||0)*ed,cv,drift:x.drift||0};
}
/* Contribution de chaque marché au risque affiché, en points de volatilité (somme = risque affiché). */
function riskPts(k){
 const w=weights(k),sp=pvol(w);if(sp<1e-9)return w.map(()=>0);
 const sc=riskShown(w).total/sp,rc=riskContrib(w);
 return rc.map(v=>v*sc*100);
}
/* Sans position : ce qu'une unité ajouterait au risque affiché, en points. */
function riskAdd(i,k){const k1=[...k];k1[i]=(k1[i]||0)+1;return (riskShown(weights(k1)).total-riskShown(weights(k)).total)*100}
function expShort(o){const r=o.s>0?o.m/o.s:0;
 if((S.size||'mid')==='mega'){const n=Math.min(3,Math.floor(Math.abs(r)/0.35));return `<span class="${o.m>=0?'pos-g':'neg-g'}">${n?(o.m>=0?'▲':'▼').repeat(n):'·'}</span>`}
 return `<span class="${cls(o.m)}">${sgn(o.m,1)}</span>`}
function expBook(k){""")
# ── barre d'état : attendu du book sous « Risque » ─────────────────────────────
e.rep("""<span class="fl">Risque</span><span class="tri none">&nbsp;</span><span class="ft2 lin"><span class="mand" style="left:50%"></span><i style="left:0;width:${Math.min(100,rk*50)}%;background:${rcol}"></i></span><b>${Math.round(sp*100)}/${Math.round(S.tgt*100)}</b></button>""",
      """${(()=>{const ex=S.tcvEst&&S.k.some(v=>v)&&S.phase!=='debrief';const rv=`${Math.round(sp*100)}/${Math.round(S.tgt*100)}`;
       return `<span class="fl">${ex?`Risque ${rv}`:'Risque'}</span><span class="tri none">&nbsp;</span><span class="ft2 lin"><span class="mand" style="left:50%"></span><i style="left:0;width:${Math.min(100,rk*50)}%;background:${rcol}"></i></span><b>${ex?`<span class="fxa">attendu</span> ${expShort(expBook(S.k))}`:rv}</b>`})()}</button>""")
e.rep(".lvls{display:grid;",".fxa{font-size:11px;font-weight:400}\n.tcvb>span{display:contents}\n.xline{display:flex;gap:14px;flex-wrap:wrap;font-family:var(--mono);font-size:11.5px;color:var(--dim);margin:6px 0 2px}\n.xline .xk{color:var(--dimmer);margin-right:4px}\n.lvls{display:grid;")
e.rep("""   <div class="xbook" id="xbook"></div>\n""","")
old=between(" {const xb=document.getElementById('xbook');","\n const gr=")
e.rep(old,"")
# ── ligne par marché : gain par unité et risque ────────────────────────────────
e.rep("""     ${mktOpen(i)&&S.tcvEst?`<div class="xrow">${expView(expRet(i))}</div>`:''}""",
      """     ${mktOpen(i)&&S.tcvEst?(()=>{const o=expRet(i),w1=U/x.sig,g={m:w1*o.m,s:w1*o.s},rp=S.k[i]?RP[i]:riskAdd(i,S.k),lv=S.size||'mid';
       return `<div class="xline"><span><span class="xk">par unité</span>${expShort(g)}${lv==='small'?` <span class="dim-g">± ${dec(2*g.s*100,1)}</span>`:''}</span><span><span class="xk">${S.k[i]?'risque':'+1 unité'}</span><span class="${rp>0.05?'neg-g':rp<-0.05?'pos-g':'dim-g'}">${rp>=0?'+':'−'}${dec(Math.abs(rp),1)} pt${Math.abs(rp)>=2?'s':''}</span></span></div>`})():''}""")
e.rep(" GRP.forEach(g=>{\n  h+=`<div class=\"sect\">"," const RP=riskPts(S.k);\n GRP.forEach(g=>{\n  h+=`<div class=\"sect\">")
# ── signaux : même ordre pour tous, le sien en gras léger ──────────────────────
e.rep("""${(()=>{const m=STYLESIG[S.prof]||'t',o=['t','c','v'].filter(z=>z!==m);
       return `<span class="mine">${tcvChip(SIGNM[m],S.tcvEst[m][i])}</span>`+o.map(z=>`<span class="oth">${tcvChip(SIGNM[z],S.tcvEst[z][i])}</span>`).join('')})()}""",
      """${(()=>{const m=STYLESIG[S.prof]||'t';
       return ['t','c','v'].map(z=>`<span class="${z===m?'mine':'oth'}">${tcvChip(SIGNM[z],S.tcvEst[z][i])}</span>`).join('')})()}""")
e.rep(".tcvb .mine i{font-weight:700;font-size:12.5px;border:1px solid currentColor}\n.tcvb .oth i{opacity:.55}",".tcvb .mine i{font-weight:600}\n.tcvb .oth i{opacity:.9}")
# ── le détail d'un marché : tout l'attendu, agrégé ─────────────────────────────
e.rep(" const drift=x.sigQ*(0.12*e.t[i]+0.10*e.c[i]+0.08*e.v[i]);",
      " const XR=expRet(i),XP=expParts(i),drift=XR.m;   /* l'attendu complet : facteurs, signaux, dérive */")
e.rep(" const sg=x.sigQ,mu=Math.log(1+drift)-sg*sg/2;"," const sg=Math.max(0.005,XR.s),mu=Math.log(1+Math.max(-0.9,drift))-sg*sg/2;")
old=between("  <p style=\"margin:12px 0 4px\">Signaux du desk</p>","  <p style=\"margin-top:10px\">Position actuelle :")
e.rep(old,"""  <p style="margin:12px 0 4px">Rendement attendu du trimestre, morceau par morceau</p>
  ${(()=>{const pc=v=>`<span class="${cls(v)}">${sgn(v,1)}</span>`,sig=(nm,z,v,x2)=>[`${nm}${x2?' <i class="cat">⚡ ×2</i>':''}`,`<span class="${z>0?'pos-g':z<0?'neg-g':'dim-g'}">${chip(z)} ${lab(z)}</span>`,pc(v)];
    const w1=U/x.sig,rp=S.k[i]?riskPts(S.k)[i]:riskAdd(i,S.k);
    return tbl([...XP.fac.map((o,k)=>[FACT[k].nm,`exposition ${o.b>=0?'+':'−'}${dec(Math.abs(o.b),2)} × lecture ${o.f>=0?'+':'−'}${dec(Math.abs(o.f),2)}`,pc(o.v)]),
      sig('Tendance',e.t[i],XP.t),sig('Portage',e.c[i],XP.c),sig('Valeur',e.v[i],XP.v,XP.cv>1),
      ...(Math.abs(XP.drift)>1e-6?[['Dérive propre au marché','',pc(XP.drift)]]:[]),
      ['<b>Attendu du marché</b>',`± 2σ : ${sgn(XR.m-2*XR.s,1)} à ${sgn(XR.m+2*XR.s,1)}`,`<b>${pc(XR.m)}</b>`],
      ['<b>Par unité, pour le fonds</b>',`± ${dec(2*w1*XR.s*100,1)} %`,`<b>${pc(w1*XR.m)}</b>`],
      [S.k[i]?'<b>Contribution au risque</b>':'<b>Une unité ajouterait</b>',`sur ${Math.round(riskShown(weights(S.k)).total*100)} points de risque affiché`,`<b class="${rp>0?'neg-g':'pos-g'}">${rp>=0?'+':'−'}${dec(Math.abs(rp),1)} pt</b>`]],['','Lecture','Effet'])})()}
  <p class="note">Facteurs : l'exposition du marché multipliée par ce que vos sources disent du facteur. Signaux : ce que tendance, portage et valeur ajoutent. L'intervalle couvre environ 95 trimestres sur 100 : il mesure ce que vous ne savez pas, pas une erreur de calcul.</p>
  <details style="margin-top:8px"><summary>Comprendre les signaux</summary>
  <p style="margin-top:8px"><em>Tendance</em> — ${TCVTXT.t.d}</p><p><em>Portage</em> — ${TCVTXT.c.d[x.grp]}</p><p><em>Valeur</em> — ${TCVTXT.v.d}</p>
  <p>Ces estimations sont bruitées ; votre style lit la sienne trois fois plus nettement que les deux autres, et la salle de marché règle le bruit (±${dec(TCVQ[S.bud.exec],2)} cran).</p></details>
""")
# le message de clic du book parle désormais de confiance et de comité en cartons
e.rep("<br><span class=\"${cls(pv.lp)}\">investisseurs ${sd1(pv.lp)}</span> · <span class=\"${cls(pv.rc)}\">comité ${sd1(pv.rc)}</span> à la validation",
      "<br>${gz(pv.lp,pv.rc,'always')} à la validation")
e.rep("""'<i class="cat">⚡ catalyseur</i>'""","""'<i class="cat" title="Catalyseur : l&#39;écart de valeur se referme ce trimestre">⚡</i>'""")

# ── la fenêtre d'un marché, réordonnée : la décision d'abord, les définitions repliées ──
old=between(" openModal(`${x.sym} — ${x.nm}`,`${dens}","\napp.addEventListener('click',e=>{const m=e.target.closest('[data-mkt]')")
e.rep(old,""" const pc=v=>`<span class="${cls(v)}">${sgn(v,1)}</span>`,w1=U/x.sig,rp=S.k[i]?riskPts(S.k)[i]:riskAdd(i,S.k);
 const L=(z)=>`<span class="${z>0?'pos-g':z<0?'neg-g':'dim-g'}">${chip(z)}</span>`;
 openModal(`${MFLAG[x.sym]||''} ${x.sym} — ${x.nm}`,`${dens}
  <p class="note" style="margin-top:0">Attendu du trimestre <em class="${cls(XR.m)}">${sgn(XR.m,1)}</em>, de ${sgn(XR.m-2*XR.s,1)} à ${sgn(XR.m+2*XR.s,1)} à 95 %. Trait doré : l'attendu ; pointillé : le zéro.</p>
  ${tbl([...XP.fac.map((o,k)=>[FACT[k].nm,`${o.b>=0?'+':'−'}${dec(Math.abs(o.b),2)} × ${o.f>=0?'+':'−'}${dec(Math.abs(o.f),2)}`,pc(o.v)]),
    ['Tendance',L(e.t[i]),pc(XP.t)],['Portage',L(e.c[i]),pc(XP.c)],[`Valeur${XP.cv>1?' ⚡':''}`,L(e.v[i]),pc(XP.v)],
    ...(Math.abs(XP.drift)>1e-6?[['Dérive propre','',pc(XP.drift)]]:[]),
    ['<b>Attendu</b>','',`<b>${pc(XR.m)}</b>`]],['','Exposition × lecture','Effet'])}
  ${tbl([['Par unité, pour le fonds',`<b>${pc(w1*XR.m)}</b> ± ${dec(2*w1*XR.s*100,1)} %`],
    [S.k[i]?'Contribution au risque':'Une unité ajouterait',`<b class="${rp>0?'neg-g':'pos-g'}">${rp>=0?'+':'−'}${dec(Math.abs(rp),1)} pt</b> sur ${Math.round(riskShown(weights(S.k)).total*100)}`],
    ['Position',S.k[i]===0?'à plat':`${S.k[i]>0?'+':''}${S.k[i]} · ${bn(notionalBn(S.k[i],i),1)}`],
    ['Autres fonds',Math.abs(S.crowd[i])<0.25?'neutres':(S.crowd[i]>0?'majoritairement longs':'majoritairement courts')]])}
  <details style="margin-top:10px"><summary>Comment lire ce tableau</summary>
   <p style="margin-top:8px">Facteurs : l'exposition du marché (de −1 à +1) multipliée par ce que vos sources disent du facteur. Signaux : ce que tendance, portage et valeur ajoutent${XP.cv>1?' — la valeur compte double sur un catalyseur':''}. L'intervalle couvre environ 95 trimestres sur 100 : il mesure ce que vous ne savez pas.</p>
   <p><em>Tendance</em> — ${TCVTXT.t.d}</p><p><em>Portage</em> — ${TCVTXT.c.d[x.grp]}</p><p><em>Valeur</em> — ${TCVTXT.v.d}</p>
   <p>Votre style lit son signal trois fois plus nettement que les deux autres ; la salle de marché règle le bruit (±${dec(TCVQ[S.bud.exec],2)} cran).</p></details>
  <details><summary>Le marché</summary>
   <p style="margin-top:8px">${x.sub}. Volatilité annualisée ${dec((x.sig*100),1)} %. Une unité vaut <em>${moneyB(Math.abs(notionalBn(1,i)))}</em> de notionnel ; une unité de plus coûterait ${dec(t1.bp,1)} pb, soit ${mm(t1.cost)}.</p></details>`);
}""")
e.done("lot 54 — lecture du book : attendu visible, par unite, risque, detail agrege")
