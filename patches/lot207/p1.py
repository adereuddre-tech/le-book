# Lot 207 (lot A) : dépêches et événements extrêmes — réaction graduée sur 5 crans : renforcer au maximum (+2 unités
# dans le sens du choc, comme avant), renforcer à moitié (+1), ne pas réagir, contrer à moitié (−1), contrer au maximum
# (−2). Même calcul qu'avant, au cran près (coûts ×2, ×5 en extrême ; écart au book ; dérogation du quant ; comité).
# Interface : sélecteur à 5 crans, un panneau de détail, bouton « Valider » ; sans choix, « ne pas réagir ».
# Le carton rouge (risque, interdiction de renforcer) bloque les crans qui augmentent la volatilité ex ante.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
# ---- evPlans : un cran a ∈ {2,1,−1,−2}
a0=s.index(" /* suivre le mouvement */\n"); end="pieces.push({a:'follow',b:'Suivre le mouvement',s:fS,t,kE,trades,cost:costP,costRaw:cost,free,pay:payF,gz:gzF,fixRc});\n"
a1=s.index(end,a0)+len(end); blk=s[a0:a1]
def br(o,n):
    global blk; assert blk.count(o)==1,(blk.count(o),o[:80]); blk=blk.replace(o,n)
br(" /* suivre le mouvement */\n"," /* lot 207 : un cran a (unités dans le sens du choc, négatif = contrer) */\n const mk=a=>{\n")
br("const tg=clampK(i,S.k[i]+sh*2),d=tg-S.k[i];","const tg=clampK(i,S.k[i]+sh*a),d=tg-S.k[i];")
br("if(S.noAddQ)fixRc.push([-6,\"Renforcement malgré l'interdiction du comité\"]);","if(S.noAddQ&&v1>v0+1e-9)fixRc.push([-6,`${a>0?'Renforcement':'Prise de position'} malgré l'interdiction du comité`]);")
br("const fS=!trades.length?'Déjà au maximum auto","const fS=!trades.length?(a<0?'Aucun ordre possible sur les marchés touchés (limite de position ou cotation suspendue).':'Déjà au maximum auto")
br("aucun ordre possible.'\n  :`${syst?'Dérogation au modèle : ':''}+2 unités dans le sens du choc sur ${syms}.",
   "aucun ordre possible.')\n  :`${syst?'Dérogation au modèle : ':''}${a>0?'+':'−'}${Math.abs(a)} unité${Math.abs(a)>1?'s':''} ${a>0?'dans le sens du choc':'contre le choc'} sur ${syms}.")
br(end," const AID={2:'follow',1:'half','-1':'chalf','-2':'contra'},ALAB={2:'Renforcer au maximum',1:'Renforcer à moitié','-1':'Contrer à moitié','-2':'Contrer au maximum'};\n return {a:AID[a],n:a,b:ALAB[a],s:fS,t,kE,trades,cost:costP,costRaw:cost,free,pay:payF,gz:gzF,fixRc,v0,v1};\n };\n pieces.push(mk(2),mk(1));\n")
s=s[:a0]+blk+s[a1:]
rep("  t:[...S.k],kE:[...S.k],trades:[],cost:0,costRaw:0,free:false,pay:payN,gz:payN.map(p=>{const a=pnlD(p);return {lp:cf(a.lp,a.rc),rc:a.rc,pnl:a}}),fixRc:[]});",
    "  t:[...S.k],kE:[...S.k],trades:[],cost:0,costRaw:0,free:false,pay:payN,gz:payN.map(p=>{const a=pnlD(p);return {lp:cf(a.lp,a.rc),rc:a.rc,pnl:a}}),fixRc:[],n:0});\n pieces.push(mk(-1),mk(-2));   /* lot 207 */")
# ---- écran : sélecteur à 5 crans + panneau
o_old="""   ${plan.map((o,i)=>{const ban=o.a==='follow'&&o.trades.length&&(redOn('risk')||redOn('noadd')),ko=false;
     return `<button class="choice evopt" data-i="${i}"${ban||ko?' disabled':''}><b>${o.b}</b><span class="evs">${o.s}${o.a==='follow'&&o.t?bkD(o.t,0,false):''}${ban?' <b class="neg-g">interdit par le comité (carton rouge)</b>':ko?' <b class="neg-g">hors trésorerie</b>':''}</span>${ptab(o)}</button>`}).join('')}"""
o_new="""   ${(()=>{const NO=plan.findIndex(o=>o.n===0);
     /* lot 207 : un cran, un panneau ; le bouton « Valider » joue le cran affiché */
     return `<div class="evsel">${plan.map((o,i)=>{const ban=o.trades.length&&(redOn('risk')||redOn('noadd'))&&o.v1>o.v0+1e-9;o.ban=ban;
       return `<button class="evstep${o.n>0?' up':o.n<0?' dn':' zr'}${i===NO?' on':''}" data-i="${i}"${ban||(!o.trades.length&&o.n!==0)?' disabled':''}><b>${o.n>0?'+':o.n<0?'−':''}${Math.abs(o.n)}</b><small>${o.n>0?'renforcer':o.n<0?'contrer':'rien'}</small></button>`}).join('')}</div>
     <div class="evpan" id="evpan"></div>
     <button class="cta" id="evok" style="margin-top:10px">Valider</button>`})()}"""
rep(o_old,o_new)
rep(""" const go=i=>{clearTimer();resolveEvent(ev,touched,plan[i],imm,navB)};
 app.querySelectorAll('.choice').forEach(b=>b.onclick=()=>go(+b.dataset.i));
 armTimer(()=>go(plan.length-1));""",
""" const go=i=>{clearTimer();resolveEvent(ev,touched,plan[i],imm,navB)};
 const NO=plan.findIndex(o=>o.n===0);let sel=NO;
 const pan=i=>{const o=plan[i];document.getElementById('evpan').innerHTML=`<div class="choice evopt" data-i="${i}" style="cursor:default"><b>${o.b}</b><span class="evs">${o.s}${o.n!==0&&o.trades.length&&o.t?bkD(o.t,0,false):''}${o.ban?' <b class="neg-g">interdit par le comité (carton rouge)</b>':''}</span>${ptab(o)}</div>`;
  app.querySelectorAll('.evstep').forEach(b=>b.classList.toggle('on',+b.dataset.i===i));sel=i};
 pan(NO);
 app.querySelectorAll('.evstep').forEach(b=>b.onclick=()=>{if(!b.disabled)pan(+b.dataset.i)});
 document.getElementById('evok').onclick=()=>go(sel);
 armTimer(()=>go(NO));""")
# ---- résultat : le verbe suit le cran
rep(""":`${syst?'Vous passez outre le modèle et suivez le mouvement':'Vous suivez le mouvement'} : ${tr}.""",
    """:`${syst?'Vous passez outre le modèle et ':'Vous '}${{2:'renforcez au maximum dans le sens du mouvement',1:'renforcez à moitié dans le sens du mouvement','-1':'contrez à moitié le mouvement','-2':'contrez au maximum le mouvement'}[o.n]||'suivez le mouvement'} : ${tr}.""")
# ---- CSS
rep(".seg{display:grid;grid-template-columns:repeat(11,1fr);gap:2px}",
""".seg{display:grid;grid-template-columns:repeat(11,1fr);gap:2px}
.evsel{display:grid;grid-template-columns:repeat(5,1fr);gap:4px;margin-top:6px}
.evstep{padding:8px 0 6px;border-radius:6px;background:var(--panel2);border:1px solid var(--line);color:var(--dim);text-align:center;font-family:var(--mono)}
.evstep b{display:block;font-size:15px}.evstep small{display:block;font-size:9px;letter-spacing:.03em}
.evstep.up.on{background:rgba(63,207,142,.16);border-color:var(--long);color:var(--long)}
.evstep.dn.on{background:rgba(242,84,91,.16);border-color:var(--short);color:var(--short)}
.evstep.zr.on{background:var(--flat);border-color:var(--txt);color:var(--txt)}
.evstep:disabled{opacity:.35}""")
open('index.html','w',encoding='utf-8').write(s);print('lot207 ok')
