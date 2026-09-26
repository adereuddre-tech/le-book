# -*- coding: utf-8 -*-
"""Lot 68 — recrue sur toute la classe, coûts et effet sur le book affichés dans chaque choix qui touche
les positions, nuage μ/σ trimestriel avec l'ancien point, lingot pour l'or, hauts faits durcis."""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()

# ── 1. trader débauché : toute sa classe d'actifs coûte moitié moins ──
e.rep(" if(S.star===i)m*=0.35;"," if(S.star>=0&&INSTR[S.star]&&INSTR[i].grp===INSTR[S.star].grp)m*=0.5;   /* lot 68 : toute la classe */")
e.rep("g:`coûts d'exécution ÷3 sur ${INSTR[S.star].sym} ce trimestre`}","g:`coûts d'exécution ÷2 sur toute la classe ${INSTR[S.star].grp.toLowerCase()} ce trimestre`}")
e.rep("g:`coûts ÷3 sur ${INSTR[i].sym} ce trimestre · ${rv.nm} affaibli`}","g:`coûts ÷2 sur toute la classe ${INSTR[i].grp.toLowerCase()} ce trimestre · ${rv.nm} affaibli`}")

# ── 2. aperçu : nouveau book, coûts, rentabilité et risque de chaque choix qui touche les positions ──
e.rep("function fxTxt(s,x){",r"""/* lot 68 : simule sur une copie du book les effets déterministes d'un choix (mêmes règles que pickCh pour
   « mid », que l'anecdote d'exécution pour « exec ») et rend le coût des ordres. Les effets aléatoires
   (randAdd) ou fondés sur des signaux cachés (trendAdd) sont signalés, pas chiffrés. */
function kPrev(e,mode){
 const save=S.k;S.k=[...save];let cost=0,hid=false;
 try{
  const setK=(i,nk)=>{if(i===undefined)return;nk=clampK(i,nk);if(nk!==S.k[i]){cost+=tcost(nk-S.k[i],i).cost*(S.tcMultQ||1);S.k[i]=nk}};
  const syms=v=>(Array.isArray(v)?v:[v]).filter(sy=>IDX[sy]!==undefined);
  const top=n=>riskContrib(weights(S.k)).map((v,i)=>({v:Math.abs(v),i})).sort((a,b)=>b.v-a.v).slice(0,n);
  if(mode==='exec'){
   if(e.invert&&IDX[e.invert]!==undefined){const i=IDX[e.invert];S.k[i]=-S.k[i]}
   if(e.cap2)for(let i=0;i<N;i++)if(Math.abs(S.k[i])===3){const d=S.k[i]>0?-1:1;cost-=tcost(d,i).cost*0.8;S.k[i]+=d}
   if(e.halfOn)syms(e.halfOn).forEach(sy=>{const i=IDX[sy],nk=Math.trunc(S.k[i]/2);if(nk!==S.k[i]){cost-=tcost(nk-S.k[i],i).cost*0.7;S.k[i]=nk}});
   if(e.cutTop1){const o=top(1)[0];if(o&&S.k[o.i]!==0){const d=-Math.sign(S.k[o.i]);cost-=tcost(d,o.i).cost*0.8;S.k[o.i]+=d}}
   if(e.scaleAll)for(let i=0;i<N;i++)S.k[i]=Math.round(S.k[i]*e.scaleAll);
   if(e.randAdd)hid=true;
   if(e.kAddAbsE&&IDX[e.kAddAbsE[0]]!==undefined){const i=IDX[e.kAddAbsE[0]],nk=clampK(i,S.k[i]+e.kAddAbsE[1]);if(nk!==S.k[i]){cost+=tcost(nk-S.k[i],i).cost;S.k[i]=nk}}
  }else{
   const I=a=>a&&IDX[a[0]];
   if(e.kAdd&&I(e.kAdd)!==undefined){const i=I(e.kAdd);setK(i,S.k[i]+e.kAdd[1]*(S.k[i]===0?1:Math.sign(S.k[i])))}
   if(e.kAddAbs&&I(e.kAddAbs)!==undefined){const i=I(e.kAddAbs);setK(i,S.k[i]+e.kAddAbs[1])}
   if(e.kAddAbs2&&I(e.kAddAbs2)!==undefined){const i=I(e.kAddAbs2);setK(i,S.k[i]+e.kAddAbs2[1])}
   if(e.kToward&&I(e.kToward)!==undefined){const i=I(e.kToward);if(S.k[i]!==0)setK(i,S.k[i]-Math.sign(S.k[i])*e.kToward[1])}
   if(e.trendAdd)hid=true;
   if(e.cutTopN)top(e.cutTopN).forEach(o=>{if(S.k[o.i]!==0)setK(o.i,S.k[o.i]-Math.sign(S.k[o.i]))});
   if(e.cap2)for(let i=0;i<N;i++)if(Math.abs(S.k[i])>2)setK(i,2*Math.sign(S.k[i]));
   if(e.zeroOn)syms(e.zeroOn).forEach(sy=>setK(IDX[sy],0));
   if(e.halfOn)syms(e.halfOn).forEach(sy=>{const i=IDX[sy];setK(i,Math.trunc(S.k[i]/2))});
   if(e.scaleAll)for(let i=0;i<N;i++)setK(i,Math.round(S.k[i]*e.scaleAll));
   if(e.randAdd)hid=true;
   if(e.addBest){let bi=-1,bv=-1e9;for(let i=0;i<N;i++){const v=S.k[i]*S.lastR[i];if(S.k[i]!==0&&v>bv){bv=v;bi=i}}if(bi>=0)setK(bi,S.k[bi]+Math.sign(S.k[bi]))}
   if(e.cutFactor){const k=e.cutFactor[0],frac=e.cutFactor[1];const e0=factorExpo(weights(S.k))[k],target=Math.abs(e0)*(1-frac);
    for(let step=0;step<8;step++){const w=weights(S.k),ex=factorExpo(w)[k];if(Math.abs(ex)<=target+1e-6||Math.sign(ex)!==Math.sign(e0))break;
     let bi=-1,bv=0;for(let i=0;i<N;i++){const c=w[i]*INSTR[i].sig*INSTR[i].b[k];if(Math.sign(c)===Math.sign(e0)&&Math.abs(c)>bv&&S.k[i]!==0){bv=Math.abs(c);bi=i}}
     if(bi<0)break;setK(bi,S.k[bi]-Math.sign(S.k[bi]))}}
   if(e.kContra&&IDX[e.kContra]!==undefined){const i=IDX[e.kContra];setK(i,S.k[i]+(S.lastR[i]>=0?-1:1))}
   if(e.cutTop2)top(2).forEach(o=>{if(S.k[o.i]!==0)setK(o.i,S.k[o.i]-Math.sign(S.k[o.i]))});
  }
  return {k:S.k,cost,hid};
 }catch(err){return null}finally{S.k=save}
}
/* même lecture que les lignes de marché : rentabilité du trimestre, risque en points de vol ex ante */
function bkD(k1,cost,hid){
 if(!k1)return '';const same=k1.every((v,i)=>v===S.k[i]);if(same&&!hid&&!cost)return '';
 const R=kk=>riskShown(weights(kk)).total,dr=(R(k1)-R(S.k))*100,dp=profitBook(k1)-profitBook(S.k);
 const ch=k1.map((v,i)=>v!==S.k[i]?`${INSTR[i].sym} ${S.k[i]>0?'+':''}${S.k[i]}→${v>0?'+':''}${v}`:null).filter(Boolean);
 return `<span class="bkd">${ch.length?`${ch.slice(0,4).join(', ')}${ch.length>4?'…':''} · rentabilité ${pc2(dp)} · risque <b class="${dr>0.05?'neg-g':dr<-0.05?'pos-g':'dim-g'}">${dr>=0?'+':'−'}${dec(Math.abs(dr),1)} pt</b>`:''}${cost>0?` · coûts <b>${mm(cost)}</b>`:cost<0?` · coûts <b class="pos-g">−${mm(-cost)}</b>`:''}${hid?`${ch.length?' · ':''}<i>positions supplémentaires tirées au moment de l'exécution</i>`:''}</span>`;
}
function bkPrev(e,mode){if(!e)return '';const p=kPrev(e,mode);return p?bkD(p.k,p.cost,p.hid):''}
function fxTxt(s,x){""")
e.rep(".rmap .rd{",".bkd{display:block;margin-top:4px;font-size:11.5px;color:var(--dim);font-family:var(--mono)}.bkd b{font-weight:600}\n.rmap .rd{")
e.rep("""<span>${fxTxt(c.s,c.e)}${ko?' <b class="neg-g">hors trésorerie</b>':''}</span></button>`}).join('')}</div>`;
 const pickCh=idx=>""","""<span>${fxTxt(c.s,c.e)}${bkPrev(c.e,'mid')}${ko?' <b class="neg-g">hors trésorerie</b>':''}</span></button>`}).join('')}</div>`;
 const pickCh=idx=>""")
e.rep("""<span>${fxTxt(c.s,c.e)}${stake(c)}${ko?' <b class="neg-g">hors trésorerie</b>':''}</span></button>`""","""<span>${fxTxt(c.s,c.e)}${stake(c)}${bkPrev(c.e,'exec')}${ko?' <b class="neg-g">hors trésorerie</b>':''}</span></button>`""")
# dépêches : suivre le mouvement
e.rep("""<span class="evs">${o.s}${ban?""","""<span class="evs">${o.s}${o.a==='follow'&&o.t?bkD(o.t,0,false):''}${ban?""")
# accident : couper la moitié du book
e.rep("""row(o.id==='cut'?'book':'confiance',o.id==='cut'?'<b>positions divisées par deux · confiance −3</b>':`<b class="neg-g">−2</b>`);""",
 """row(o.id==='cut'?'book':'confiance',o.id==='cut'?'<b>positions divisées par deux · confiance −3</b>':`<b class="neg-g">−2</b>`)+(o.id==='cut'?bkD(S.k.map(v=>Math.trunc(v/2)),0,false):'');""")
# suivre / contrer un concurrent : coût exact (×tcMultQ, comme appliqué), effet sur le book, confiance seule
e.rep("""<div class="kv"><span>Effet de l'article</span><b><span class="${cls(g0.lp)}">investisseurs ${sd1(g0.lp)}</span> · <span class="${cls(g0.rc)}">comité ${sd1(g0.rc)}</span></b></div>""",
 """<div class="kv"><span>Effet de l'article</span><b><span class="${cls(g0.lp)}">confiance ${sd1(g0.lp)}</span></b></div>""")
e.rep("""<span>Coût ${mm(t.cost*1.5)}, à votre charge, dans un marché qui a déjà bougé.""","""<span>Coût ${mm(tcost(nk-S.k[i],i).cost*1.5*S.tcMultQ)}, à votre charge, dans un marché qui a déjà bougé.""")
e.rep("""sinon, d'un gérant qui court après les autres.</span></button>""","""sinon, d'un gérant qui court après les autres.${bkD(S.k.map((v,m)=>m===i?nk:v),0,false)}</span></button>""")
e.rep("""<span>Vous pariez que ${rv.boss} a tort de rester. Même coût, même bruit, gloire ou ridicule.</span>""",
 """<span>Vous pariez que ${rv.boss} a tort de rester. Coût ${mm(tcost(-nk-S.k[i],i).cost*1.5*S.tcMultQ)}, même bruit, gloire ou ridicule.${bkD(S.k.map((v,m)=>m===i?-nk:v),0,false)}</span>""")
e.rep("""[['Jauges',`<span class="${cls(g0.lp+g.lp)}">${sd1(g0.lp+g.lp)}</span> · <span class="${cls(g0.rc+g.rc)}">${sd1(g0.rc+g.rc)}</span>`]]""","""[['Confiance',`<span class="${cls(g0.lp+g.lp)}">${sd1(g0.lp+g.lp)}</span>`]]""")

# ── 3. nuage μ / σ trimestriels, ancien point en jaune pâle ──
e.rep(" const pr=profitBook(S.k)*4,R=(S.rivals||[]).map((rv,j)=>{const p=rivPt(rv);p.y*=4;return Object.assign(p,{c:rivCol(j),nm:rv.nm})});",
 """ /* lot 68 : trimestriel — μ du trimestre, σ trimestriel = σ annuel / 2. gh = le fonds avant ses derniers changements
    (book de départ sur la page du book, book validé pendant le trimestre), en jaune pâle. */
 const pr=profitBook(S.k),R=(S.rivals||[]).map((rv,j)=>{const p=rivPt(rv);p.x/=2;return Object.assign(p,{c:rivCol(j),nm:rv.nm})});
 const sq=sp/2,kB=(S.phase==='book'?S.k0:S.kVal)||null,gh=kB&&kB.length===S.k.length&&kB.some((v,i)=>v!==S.k[i])?{x:riskShown(weights(kB)).total/2,y:profitBook(kB)}:null;""")
e.rep(" const xm=Math.max(0.10,sp,...R.map(r=>r.x))*1.10;\n const ys=[pr,...R.map(r=>r.y)],"," const xm=Math.max(0.05,sq,...R.map(r=>r.x),...(gh?[gh.x]:[]))*1.10;\n const ys=[pr,...R.map(r=>r.y),...(gh?[gh.y]:[])],")
e.rep(" const sv=`${dec(sp*100,1)} %`"," const sv=`${dec(sq*100,1)} %`")
e.rep("for(let v=Math.ceil(a/0.1-1e-9)*0.1;v<=b+1e-9;v+=0.1)o.push(+v.toFixed(2))","for(let v=Math.ceil(a/0.05-1e-9)*0.05;v<=b+1e-9;v+=0.05)o.push(+v.toFixed(2))")
e.rep("lv(0.1,xm)","lv(0.05,xm)",2)
e.rep("X(TAIL.x0)","X(TAIL.x0/2)",5)
e.rep("TAIL.x0<xm","TAIL.x0/2<xm",2)
e.rep("  const px=X(sp),py=Y(pr);","  const px=X(sq),py=Y(pr);\n  if(gh)g+=`<circle cx=\"${f(X(gh.x))}\" cy=\"${f(Y(gh.y))}\" r=\"5.5\" fill=\"#F3D250\" opacity=\".30\"/>`;")
e.rep(" const px=X(sp),py=Y(pr);\n s+="," const px=X(sq),py=Y(pr);\n if(gh)s+=`<i class=\"rd me\" style=\"left:${f(X(gh.x))}%;top:${f(Y(gh.y))}%;background:#F3D250;opacity:.30;border:none\"></i>`;\n s+=")
e.rep("σ : risque annualisé du book, bruit d'estimation compris. μ : rendement attendu annualisé (quatre fois celui du trimestre) — collatéral, impact, drain de volatilité et coût moyen des accidents de levier compris. Traits tous les 10 %. Les concurrents sont placés à leur couple estimé.",
 "Valeurs <b>trimestrielles</b>. σ : risque du book sur un trimestre (la moitié du σ annuel des lignes de marché), bruit d'estimation compris. μ : rendement attendu du trimestre — collatéral, impact, drain de volatilité et coût moyen des accidents de levier compris. Traits tous les 5 %. Point jaune pâle : votre fonds avant vos derniers changements de position. Les concurrents sont placés à leur couple estimé.")
e.rep("`Sous σ ${dec(TAIL.x0*100,0)} %, pas d'accident de levier possible.`","`Sous σ ${dec(TAIL.x0*50,1)} % par trimestre, pas d'accident de levier possible.`")

# ── 4. l'or : un lingot ──
e.rep("GC:'🥇'","""GC:'<svg viewBox="0 0 20 14" width="1.25em" height="0.9em" style="vertical-align:-1px" aria-label="lingot"><path d="M4 3h12l3 9H1z" fill="#E0B53A"/><path d="M4 3h12l-1.4 2.2H5.4z" fill="#F6DB7A"/><path d="M1 12h18l-1 1.5H2z" fill="#A87D17"/></svg>'""")

# ── 5. hauts faits plus durs ──
H=[('nm:"Trois d\'affilée",d:"Enchaîner trois trimestres positifs dans une même partie.",tq:c=>c.streak>=3','nm:"Quatre d\'affilée",d:"Enchaîner quatre trimestres positifs dans une même partie.",tq:c=>c.streak>=4'),
 ('d:"Tenir trois objectifs trimestriels dans une même partie.",tf:f=>f.goals>=3','d:"Tenir quatre objectifs trimestriels dans une même partie.",tf:f=>f.goals>=4'),
 ('d:"Terminer un mandat complet avec un repli maximal sous 8 %.",tf:f=>!f.over&&f.maxdd<0.08','d:"Terminer un mandat d\'au moins huit trimestres avec un repli maximal sous 6 %.",tf:f=>!f.over&&f.maxdd<0.06&&f.q>=8'),
 ('d:"Atteindre 90 de confiance.",tq:c=>c.lp>=90','d:"Atteindre 95 de confiance.",tq:c=>c.lp>=95'),
 ('d:"Gagner, en commissions nettes, la moitié de l\'encours de départ.",tf:f=>f.gains>0.5*f.aum0','d:"Gagner, en commissions nettes, les trois quarts de l\'encours de départ.",tf:f=>f.gains>0.75*f.aum0'),
 ('d:"Tenir six objectifs trimestriels dans une même partie.",tf:f=>f.goals>=6','d:"Tenir sept objectifs trimestriels dans une même partie.",tf:f=>f.goals>=7'),
 ('d:"Gagner, en commissions nettes, une fois et demie l\'encours de départ.",tf:f=>f.gains>1.5*f.aum0','d:"Gagner, en commissions nettes, deux fois l\'encours de départ.",tf:f=>f.gains>2*f.aum0'),
 ('d:"Terminer avec un Sharpe probabiliste au-dessus de 95 %.",tf:f=>f.psr>0.95','d:"Terminer un mandat d\'au moins huit trimestres avec un Sharpe probabiliste au-dessus de 97,5 %.",tf:f=>f.psr>0.975&&f.q>=8'),
 ('nm:"Tripler la mise",d:"Terminer un mandat avec une performance nette au moins de +200 %.",tf:f=>f.idx>=3}','nm:"Quintupler la mise",d:"Terminer un mandat avec une performance nette au moins de +400 %.",tf:f=>f.idx>=5}'),
 ('nm:"Doubler la mise",d:"Terminer un mandat avec une performance nette au moins de +100 %.",tf:f=>f.idx>=2','nm:"Tripler la mise",d:"Terminer un mandat avec une performance nette au moins de +200 %.",tf:f=>f.idx>=3'),
 ('d:"Gagner, en commissions nettes, quatre fois l\'encours de départ.",tf:f=>f.gains>4*f.aum0','d:"Gagner, en commissions nettes, cinq fois l\'encours de départ.",tf:f=>f.gains>5*f.aum0'),
 ('nm:"Le Graal",d:"Terminer un mandat complet avec un repli maximal sous 5 % et un Sharpe probabiliste au-dessus de 95 %.",tf:f=>!f.over&&f.maxdd<0.05&&f.psr>0.95',
  'nm:"Le Graal",d:"Terminer un mandat d\'au moins huit trimestres premier des quatre fonds, sans un trimestre négatif ni un carton, avec au moins +150 % de performance nette et un repli maximal sous 8 %.",tf:f=>!f.over&&f.q>=8&&f.rank===1&&f.qNeg===0&&f.nocard&&f.idx>=2.5&&f.maxdd<0.08')]
for a,b in H: e.rep(a,b)
e.done("lot 68")
