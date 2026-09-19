# -*- coding: utf-8 -*-
"""Lot 19 — barre d'état, formats monétaires, mi-parcours, comité et risque."""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ── D. choix « normal » par défaut ──
e.rep("""let setup={prof:'flux',arch:'std',desk:'inhouse',vol:'std',size:'mid',univ:'com',dur:'normal'}""",
      """let setup={prof:'fonda',arch:'std',desk:'inhouse',vol:'std',size:'mid',univ:'com',dur:'normal'}""")
e.rep("""setup={prof:'syst',arch:'std',desk:'inhouse',vol:'std',size:'mid'};""",
      """setup={prof:'fonda',arch:'std',desk:'inhouse',vol:'std',size:'mid',univ:'com',dur:'normal'};""")

# ── E. en k$ jusqu'à dix millions, en M$ au-delà ──
e.rep("""const score=x=>{const a=Math.abs(x);
 if(a>=1)return sig3(x,'Md$');
 if(a>=0.00005)return sig3(x*1000,'M$');
 return (x<0?'−':'')+Math.abs(x*1e6).toFixed(0)+' k$'};""",
"""/* Trésorerie et gains : en milliers de dollars tant qu'on est sous dix millions, ce qui est
   la plage où se joue la partie, puis en millions. 9 999 k$, puis 13,23 M$. */
const score=x=>{const a=Math.abs(x),sg=x<0?'−':'';
 if(a>=1)return sig3(x,'Md$');
 if(a>=0.01)return sg+(a*1000).toFixed(2).replace('.',',')+' M$';
 return sg+Math.round(a*1e6).toLocaleString('fr-FR').replace(/\\u202f|\\u00a0/g,' ')+' k$'};""")

# ── F. valeur du fonds : ancienne → nouvelle, dans la couleur du mouvement ──
e.rep("""<b>${moneyB(S.nav)}</b></button>""",
"""<b>${(()=>{const q0=S.navQ0||0,d=q0?S.nav/q0-1:0;
     return (S.phase!=='budget'&&Math.abs(d)>0.002)
      ?`<span class="dim-g" style="font-weight:400">${moneyB(q0)}</span> <span class="${cls(d)}">→${moneyB(S.nav)}</span>`
      :moneyB(S.nav)})()}</b></button>""")

# ── G. la valeur d'un point de base, en k$ (elle s'affichait « 0 M$ ») ──
e.rep("""Un point de base vaut <em>${(S.nav*0.1).toFixed(0)} M$</em>.""",
      """Un point de base vaut <em>${(S.nav*100).toFixed(0)} k$</em>.""")

# ── H. texte du mi-parcours ──
e.rep("""  [`Le fonds est à <em class="${cls(tot)}">${sgn(tot/100,1)}</em> depuis le début de l'année. Sur ce total, <em class="${cls(dir)}">${dir>=0?'+':'−'}${dec(Math.abs(dir),1)} point${Math.abs(dir)>=2?'s':''}</em> viennent des positions directionnelles que vous portez en ce moment — <em class="${cls(p)}">${sgn(p,1)} · ${mn(p*navB)}</em> de gains latents, rien n'est encaissé. Le reste est déjà acquis : dépêches soldées, collatéral, incidents. Les investisseurs et le comité reçoivent le rapport hebdomadaire et réagissent : ${gz(g.lp,g.rc,'always')}.`,""",
"""  [`Le fonds est à <em class="${cls(tot)}">${sgn(tot/100,1)}</em> depuis le début de l'année. Sur ce total, <em class="${cls(dir)}">${dir>=0?'+':'−'}${dec(Math.abs(dir),1)} point${Math.abs(dir)>=2?'s':''}</em> viennent des positions directionnelles que vous portez depuis le début du trimestre — <em class="${cls(p)}">${sgn(p,1)} · ${mn(p*navB)}</em>. Les investisseurs et le comité reçoivent le rapport hebdomadaire et réagissent : ${gz(g.lp,g.rc,'always')}.`,""")

# ── I + J. la jauge des coûts disparaît, celle du risque prend la place ──
e.rep("""   <button class="fg" data-gauge="cost"><span class="fl">Coûts T</span><span class="tri none">&nbsp;</span><span class="ft2"><i style="left:0;width:${Math.min(100,ctot/1.6)}%;background:${ctot>90?'var(--short)':ctot>65?'var(--warn)':'var(--dim)'}"></i></span><b>${ctot.toFixed(0)} pb</b></button>\n""","")
e.rep("""   <button class="fg" data-gauge="risk"><span class="fl">Risque</span>""",
      """   <button class="fg" data-gauge="risk" style="flex:2.2">${''}<span class="fl">Risque</span>""")
e.rep(""" const rcol=Math.abs(rk-1)<=band?'var(--long)':(rk>1+band?'var(--short)':'var(--warn)');""",
""" /* couleur continue : vert dans la bande, puis jaune, orange, rouge à mesure que l'écart
    au mandat grandit. Un dégradé se lit mieux que trois paliers. */
 const rdev=Math.max(0,(Math.abs(rk-1)-band)/0.95);
 const rhue=145-140*Math.pow(Math.min(1,rdev),0.62);
 const rcol=`hsl(${rhue.toFixed(0)} 62% ${(52+8*Math.min(1,rdev)).toFixed(0)}%)`;""")

# ── K. le comité sanctionne l'excès de risque sans plafond ──
e.rep(""" let d=dev<band?3:-Math.min(12,(dev-band)*18)*SIZE().rcNeg;""",
""" /* plus aucun plafond : la sanction croît continûment avec l'écart au mandat. La seule
    limite restante est la borne de gauge(). */
 let d=dev<band?3:-(dev-band)*32*SIZE().rcNeg;""",2)

e.done("lot 19 — barre d'etat, formats, comite")
