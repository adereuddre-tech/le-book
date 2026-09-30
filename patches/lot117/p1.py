# Lot 117 : retours d'Antoine (textes, débauchage, cartons annoncés, annonces).
import re
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
# Jean-Kevin stagiaire ; Gontran sans « Maître »
rep('role:"analyste macro junior, à tout faire"','role:"stagiaire en analyse macro, à tout faire"')
def jk(m):
    return m.group(0).replace('juniors','stagiaires').replace('junior','stagiaire')
n0=s.count('junior')
s=re.sub(r'\{who:"(?:Jean-Kevin|[^"]*analyste junior)[^\n]*(?:\n(?! \{who:)[^\n]*)*',jk,s)
print('junior :',n0,'→',s.count('junior'))
rep("Maître Gontran Report-à-Nouveau","Gontran Report-à-Nouveau")
rep("Maître Report-à-Nouveau","Gontran Report-à-Nouveau",11)
# Tatillon et Mireille : positions inversées, crans (coûts, effets) inchangés
a=' {who:"Mireille",hi:"Je ne dis pas non. Je dis : justifiez.",full:"Mireille Cauchemar",role:"directrice des risques",ic:"⚖️",bp:30},\n {who:"L\'inspecteur Tatillon",hi:"Faites comme si je n\'étais pas là. Je note tout.",full:"L\'inspecteur Firmin Tatillon",role:"conformité et audit interne",ic:"🔎",bp:45},'
b=' {who:"L\'inspecteur Tatillon",hi:"Faites comme si je n\'étais pas là. Je note tout.",full:"L\'inspecteur Firmin Tatillon",role:"conformité et audit interne",ic:"🔎",bp:30},\n {who:"Mireille",hi:"Je ne dis pas non. Je dis : justifiez.",full:"Mireille Cauchemar",role:"directrice des risques",ic:"⚖️",bp:45},'
rep(a,b)
rep("{re:'Mireille Cauchemar|Mireille',bo:1,on:()=>S.bud.bo>=3,","{re:'Mireille Cauchemar|Mireille',bo:1,on:()=>S.bud.bo>=4,")
rep("(/Tatillon/.test(w)&&S.bud.bo<4)","(/Tatillon/.test(w)&&S.bud.bo<3)")
# graphique : « cumul »
rep(" · DEPUIS LE LANCEMENT</span>"," · CUMUL</span>",3)
# annonces
rep("ret:0.03,win:{lp:4,rc:4},lose:{lp:-4,rc:-4}},","ret:0.03,win:{lp:5,rc:0},lose:{lp:-10,rc:0}},")
rep("ret:0.09,win:{lp:12,rc:12},lose:{lp:-12,rc:-12}},","ret:0.09,win:{lp:15,rc:0},lose:{lp:-12,rc:0}},")
rep("ret:0.15,win:{lp:22,rc:22},lose:{lp:-25,rc:-25}}","ret:0.15,win:{lp:30,rc:0},lose:{lp:-15,rc:0}}")
# holding royale
rep("B('souv',g>=1.6&&conf0>=78,()=>{const v=invs().find(x=>x.id==='fs'),m=invFlow(v,0.20*extNav());S.bandTight=0.8;",
    "B('souv',g>=1.6&&conf0>=78,()=>{const m=flowInB(0.20);S.bandTight=0.8;")
rep("t:'Le fonds souverain frappe à la porte',","t:'La holding d\\'une maison royale veut entrer',")
# confiance : le chiffre de la ligne = celui du texte (cf)
rep("function cf(lp,rc){","function gcf(...a){return a.reduce((x,g)=>x+cf(g.lp,g.rc),0)}\nfunction cf(lp,rc){")
rep("['Confiance',`<span class=\"${cls(g0.lp+g.lp)}\">${sd1(g0.lp+g.lp)}</span>`]","['Confiance',`<span class=\"${cls(gcf(g0,g))}\">${sd1(gcf(g0,g))}</span>`]")
rep("['Confiance',`<span class=\"${cls(g0.lp+g.lp+g2.lp)}\">${sd1(g0.lp+g.lp+g2.lp)}</span>`]","['Confiance',`<span class=\"${cls(gcf(g0,g,g2))}\">${sd1(gcf(g0,g,g2))}</span>`]")
rep("['Confiance',`<span class=\"${cls(g.lp+g2.lp)}\">${sd1(g.lp+g2.lp)}</span>`]","['Confiance',`<span class=\"${cls(gcf(g,g2))}\">${sd1(gcf(g,g2))}</span>`]")
rep("['Confiance',`<span class=\"${cls(g.lp)}\">${sd1(g.lp)}</span>`]],\n  \"Poursuivre le trimestre\"","['Confiance',`<span class=\"${cls(gcf(g))}\">${sd1(gcf(g))}</span>`]],\n  \"Poursuivre le trimestre\"")
rep("['Confiance',`<span class=\"${cls(g.lp+g2.lp)}\">${sd1(g.lp+g2.lp)}</span>`]]});","['Confiance',`<span class=\"${cls(gcf(g,g2))}\">${sd1(gcf(g,g2))}</span>`]]});",0) if False else None
# mi-parcours : même chiffre que le graphique (celui du ruban)
rep(" const qtd0=navNow()/Math.max(1e-9,S.navQ0)-1,oth0=",
    " try{tapeTick()}catch(err){}\n const tp=S.tape&&S.tape.pts||[],tq0=Math.min(tp.length-1,S.tape&&S.tape.q0||0);\n const qtd0=tp.length>2&&tp[tq0]>0?tp[tp.length-1]/tp[tq0]-1:navNow()/Math.max(1e-9,S.navQ0)-1,oth0=")
# desk : liquidité d'abord, coût moyen d'une unité ; prime broker ensuite
rep("[`Les rumeurs arriveront après le budget : la recherche décide de leur nombre et de leur qualité.`,`Prime broker : marges à <b>×${dec(S.mgMult||1,2)}</b> du barème ce trimestre${(S.mgMult||1)>1.05?', liquidité oblige':''}.`,",
    "[`Liquidité des marchés : <b>${lqNm}</b>. Une position d'une unité sur un marché coûte en moyenne <b>${mm(cEx/Math.max(1,N))}</b> à ouvrir, soit ${dec(cBp/Math.max(1,N),1)} pb de l'encours — ${L>1.2?'nettement plus cher que d\\'habitude':L>1.05?'un peu plus cher que d\\'habitude':L<0.95?'moins cher que d\\'habitude':'le tarif habituel'}.`,`Prime broker : marges à <b>×${dec(S.mgMult||1,2)}</b> du barème ce trimestre${(S.mgMult||1)>1.05?', liquidité oblige':''}.`,")
m=re.search(r",`Liquidité des marchés : <b>\$\{lqNm\}</b>\. Ouvrir une unité sur chacun[^`]*`",s);assert m;s=s[:m.start()]+s[m.end():]
rep(",\"Prochaine étape : le budget, puis le book pour les trois prochains mois.\"],","],")
# budget : licenciement à un demi-trimestre ; phrase d'Antoine
rep("function sevRaw(){const P=S.budPrev;if(!P)return 0;return BUDGET.reduce((a,b)=>a+Math.max(0,b.lv[P[b.id]].bp-b.lv[S.bud[b.id]].bp),0)}",
    "function sevRaw(){const P=S.budPrev;if(!P)return 0;return 0.5*BUDGET.reduce((a,b)=>a+Math.max(0,b.lv[P[b.id]].bp-b.lv[S.bud[b.id]].bp),0)}   /* lot 117 : un demi-trimestre de salaire */")
rep("<b class=\"neg-g\">Descendre sous le cran du trimestre dernier, c'est licencier : chaque partant touche son bonus de départ, un trimestre de salaire.</b>",
    "<b class=\"neg-g\">Ne pas sélectionner, c'est licencier : chaque partant touche son bonus de départ, un demi-trimestre de salaire.</b>")
# débauchage : parti pour de bon, contre-offre par trader
rep("function here(p){return !!(S&&S.bud)&&S.bud.fo>=p&&!(S.gone&&S.gone.p===p&&S.gone.n===0)}",
    "function gonesL(){if(!S.gones){S.gones=[];if(S.gone){S.gones.push({p:S.gone.p,n:S.gone.n,boss:S.gone.boss});S.gone=null}}return S.gones}\n"
    "const CNTK=1.5;   /* lot 117 : un trader parti ne revient que contre 1,5 trimestre de son salaire */\n"
    "function cntCost(p){return Math.round(CNTK*(FOP[p].bp-FOP[p-1].bp))}\n"
    "function here(p){return !!(S&&S.bud)&&S.bud.fo>=p&&!gonesL().some(g=>g.p===p&&g.n===0)}")
rep("if(S.gone){if(S.gone.n>0)S.gone.n=0;else S.gone=null}","gonesL().forEach(g=>g.n=0);")
rep("S.gone={p,n:1,boss};S.poachMsg+=` ${boss} a débauché ${FOP[p].full} : son siège reste vide au trimestre prochain${FOP[p].cls?` (${FOP[p].cls.toLowerCase()} par un courtier, ×${dec(NOTRD,1)})`:''}, sauf contre-offre.`}",
    "gonesL().push({p,n:1,boss});S.poachMsg+=` ${boss} a débauché ${FOP[p].full} : il ne reviendra pas sans contre-offre${FOP[p].cls?` (${FOP[p].cls.toLowerCase()} par un courtier, ×${dec(NOTRD,1)}, en attendant)`:''}.`}")
rep(" const G=S.gone&&S.gone.n===0&&S.bud.fo>=S.gone.p?S.gone:null,cb=G?FOP[G.p].bp-FOP[G.p-1].bp:0,cok=G&&(budgetBp()+cb)*1e-4*budNav()<=purse;",
    " const GL=gonesL().filter(g=>g.n===0&&S.bud.fo>=g.p),cok=g=>(budgetBp()+cntCost(g.p))*1e-4*budNav()<=purse;")
rep("${b.id==='fo'&&G?`<div class=\"flag\" style=\"margin:8px 0 0\"><span><b>${FOP[G.p].who} est parti chez ${G.boss}.</b> Son siège reste vide ce trimestre${FOP[G.p].cls?` : la classe ${FOP[G.p].cls.toLowerCase()} passe par un courtier`:''}. Contre-offre : un trimestre de son salaire, ${cb} pb (${mm(cb*1e-4*budNav())}), et il revient tout de suite.</span></div><button class=\"lvl cntb\" id=\"cnt\"${cok?'':' disabled'}>Faire la contre-offre · ${mm(cb*1e-4*budNav())}</button>`:''}",
    "${b.id==='fo'?GL.map(G=>`<div class=\"flag\" style=\"margin:8px 0 0\"><span><b>${FOP[G.p].who} est parti chez ${G.boss}.</b> Il ne reviendra pas de lui-même${FOP[G.p].cls?` : la classe ${FOP[G.p].cls.toLowerCase()} passe par un courtier`:''}. Contre-offre : son salaire plus une prime de retour, ${cntCost(G.p)} pb au total (${mm(cntCost(G.p)*1e-4*budNav())}), et il revient tout de suite.</span></div><button class=\"lvl cntb\" data-cnt=\"${G.p}\"${cok(G)?'':' disabled'}>Faire revenir ${FOP[G.p].who} · ${mm(cntCost(G.p)*1e-4*budNav())}${cok(G)?'':' · <span class=\"hx\">hors trésorerie</span>'}</button>`).join(''):''}")
rep("const cn=document.getElementById('cnt');if(cn)cn.onclick=()=>{S.cntBp=cb;S.cntQ=S.q;const w=FOP[G.p].who;S.gone=null;setOps();drawBuds();refreshStatus();toast(`Contre-offre acceptée : <b>${w}</b> reste chez vous (${mm(cb*1e-4*budNav())}).`)};",
    "app.querySelectorAll('.cntb[data-cnt]').forEach(cn=>cn.onclick=()=>{const p=+cn.dataset.cnt,cb=cntCost(p);S.cntBp=(S.cntQ===S.q?(S.cntBp||0):0)+cb;S.cntQ=S.q;S.gones=gonesL().filter(g=>g.p!==p);setOps();drawBuds();refreshStatus();toast(`Contre-offre acceptée : <b>${FOP[p].who}</b> revient (${mm(cb*1e-4*budNav())}).`)});")
rep("<i>${gone?`parti chez ${G.boss}`:l.role}</i>","<i>${gone?`parti chez ${GL.find(g=>g.p===i).boss}`:l.role}</i>")
rep("const gone=b.id==='fo'&&G&&G.p===i,","const gone=b.id==='fo'&&GL.some(g=>g.p===i),")
assert not re.search(r'S\.gone\b',s.replace('if(S.gone){S.gones.push({p:S.gone.p,n:S.gone.n,boss:S.gone.boss});S.gone=null}',''))
# anecdotes de fidélisation : coût aligné sur les salaires (15 pb au moins)
rep("/* ══════════ lot 103 : limites du comité ══════════ */",r'''/* lot 117 : une anecdote qui réduit le débauchage coûte au moins 15 pb (10 pb + 50 pb par unité de débauchage évitée) */
[TRADER_EXEC,TRADER_MID,STAKE,INCIDENTS,BOARDEV].forEach(A=>A.forEach(ev=>(ev.ch||[]).forEach(c=>{const e=c.e||{};
 if(e.poach<0&&e.cash<0){const bp=Math.max(15,Math.round(10+50*Math.abs(e.poach)));e.cash=-bp/1e4;if(c.s)c.s=c.s.replace(/−\d+ pb/,'−'+bp+' pb')}})));
/* ══════════ lot 103 : limites du comité ══════════ */''')
# cartons annoncés dès que la condition est franchie
rep("function statusBar(done){\n","function cardWarn(){if(!S||S.over||!['book','exec','comm','events'].includes(S.phase)||!S.k)return null;\n"
 " const w=weights(S.k),sp=pvol(w),lv=limVol(),cc=clsConc(w),lc=limConc(),out=[];let lvl=0;\n"
 " if(sp>=lv*LIM.red){lvl=2;out.push(`risque ex ante ${dec(sp*50,1)} %, au moins ${dec(LIM.red,1)} fois la limite`)}\n"
 " else if(sp>lv+1e-9){lvl=1;out.push(`risque ex ante ${dec(sp*50,1)} % au-dessus de la limite de ${dec(lv*50,1)} %`)}\n"
 " if(Math.round(cc.v*100)>Math.round(lc*100)){lvl=Math.max(lvl,1);out.push(`${Math.round(cc.v*100)} % du risque en ${cc.g.toLowerCase()}, limite ${Math.round(lc*100)} %`)}\n"
 " if(S.live&&typeof liveRet==='function'){const r=liveRet(),ls=limStop();if(S.stopY===S.q){lvl=Math.max(lvl,1);out.push('stop franchi sans couper')}\n"
 "  if(S.stopCut!==S.q&&r<=-2*ls){lvl=2;out.push(`trimestre à ${sgnp(r,1)}, deux fois le stop`)}}\n"
 " if(!lvl)return null;if(lvl===1&&S.cards&&S.cards.y>=1){lvl=2;out.push('deuxième jaune')}return {lvl,txt:out.join(' · ')}}\n"
 "function cardWarnUpdate(){if(typeof document==='undefined')return;let el=document.getElementById('cardw');let c=null;try{c=cardWarn()}catch(e){}\n"
 " if(!c){if(el)el.remove();return}if(!el){el=document.createElement('div');el.id='cardw';document.body.appendChild(el)}\n"
 " el.className='cardw '+(c.lvl>1?'r':'y');el.innerHTML=`${c.lvl>1?'🟥 <b>Carton rouge</b>':'🟨 <b>Carton jaune</b>'} à la clôture si rien ne change : ${c.txt}.`}\n"
 "function statusBar(done){\n setTimeout(cardWarnUpdate,0);\n")
rep(".cisel{display:flex;gap:6px;margin-top:6px}",".cisel{display:flex;gap:6px;margin-top:6px}\n.cardw{position:fixed;left:10px;right:10px;bottom:12px;z-index:60;padding:10px 12px;border-radius:8px;font-size:13px;line-height:1.35;color:#fff;background:#3b300c;border:2px solid #E3B341;box-shadow:0 4px 18px rgba(0,0,0,.45)}\n.cardw.r{background:#3d1010;border-color:#E5483C}")
open('index.html','w',encoding='utf-8').write(s);print('lot117 p1 ok')
