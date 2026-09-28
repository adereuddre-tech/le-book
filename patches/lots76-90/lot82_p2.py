import re
P='/home/claude/le-book/index.html';s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:100]);s=s.replace(old,new)
def resub(pat,new):
    global s;m=list(re.finditer(pat,s,re.S));assert len(m)==1,(len(m),pat[:60]);s=s[:m[0].start()]+new+s[m[0].end():]
rep("</style>",".cisel{display:flex;gap:6px;margin-top:6px}.cisel .cip{flex:1;padding:9px 0;border-radius:6px;background:var(--panel2);border:1px solid var(--line2);color:var(--txt);font-family:var(--mono);font-size:13px}.cisel .cip.on{border-color:var(--gold);color:var(--gold)}\n.ess .attr .av{text-align:right}\n</style>")
# l'objectif passe dans l'essentiel
resub(r"\n if\(S\.qGoal\)warn\.push\([^\n]*","")
# bloc « l'essentiel » et co-investissement, calculés avant le gabarit
rep(" const story=S.qLog.filter(x=>x!=='mandat');",""" const story=S.qLog.filter(x=>x!=='mandat');
 /* lot 82 : l'essentiel d'abord ; le détail reste replié plus bas */
 const Gq=S.mgrQ,bon=S.qGoal&&S.qGoal.ok?(S.qGoal.bonus||0):0,netQ=Gq.fees-Gq.ops-(Gq.tc||0)+(Gq.coinv||0)-(Gq.claw||0)+bon;
 const cz=[...S.gLog.filter(g=>g.lp).map(g=>[g.why,g.lp]),...S.lpD.filter(x=>x[0]!=='Plafonnement')].sort((a,b)=>Math.abs(b[1])-Math.abs(a[1])).slice(0,3);
 const lpQ0=S.lpQ0!==undefined?S.lpQ0:S.lp,rkE=1+S.rivals.filter(r=>r.cum>S.idx).length;
 const gpart=[['commissions',Gq.fees],["bonus d'objectif",bon],['co-investissement '+Math.round((Gq.cp||COINV)*100)+' %',Gq.coinv||0],['restitution',-(Gq.claw||0)],['budget',-Gq.ops],['exécution',-(Gq.tc||0)]].filter(x=>Math.abs(x[1])>1e-9);
 const ess=`<div class="block ess"><div class="blockhead"><h2>L'essentiel</h2><span class="hint">trimestre ${S.q}/${QT()}</span></div>
  <div class="attr"><span class="an">Le fonds</span><span class="av"><b class="${cls(o.qTotal)}">${sgn(o.qTotal,1)}</b> · ${rkE}<sup>${rkE===1?'er':'e'}</sup>/4 · encours ${moneyB(S.nav)}</span></div>
  <div class="attr"><span class="an">Confiance des investisseurs</span><span class="av">${Math.round(lpQ0)} → <b>${Math.round(S.lp)}</b></span></div>
  ${cz.length?`<p class="note" style="margin:0 0 8px">${cz.map(x=>`${x[0]} <b class="${x[1]>=0?'pos-g':'neg-g'}">${sd1(x[1])}</b>`).join(' · ')}</p>`:''}
  ${S.comm&&S.comm.ret!==null?`<div class="attr"><span class="an">Engagement</span><span class="av">promis ≥ ${sgn(S.comm.ret,1)}, livré ${sgn(o.qTotal,1)} · <b class="${S.commRes&&S.commRes.ok?'pos-g':'neg-g'}">${S.commRes&&S.commRes.ok?'tenu':'manqué'}, confiance ${sd1(S.commRes&&S.commRes.ok?S.comm.win.lp:S.comm.lose.lp)}</b></span></div>`:''}
  ${S.qGoal?`<div class="attr"><span class="an">Objectif « ${S.qGoal.nm.toLowerCase()} »</span><span class="av"><b class="${S.qGoal.ok?'pos-g':'neg-g'}">${S.qGoal.ok?'tenu':'manqué'}</b>${bon?' · bonus '+mm(bon):''}</span></div>`:''}
  <div class="attr"><span class="an">Comité des risques</span><span class="av">${S.qCard?(S.qCard.c==='rouge'?'🟥 carton rouge':'🟨 carton jaune'):'aucun carton'}${S.cards&&S.cards.y&&!(S.qCard&&S.qCard.c==='rouge')?` · ${S.cards.y} jaune${S.cards.y>1?'s':''} en cours`:''}</span></div>
  <div class="attr" style="margin-top:10px"><span class="an" style="color:var(--txt)">Votre gain du trimestre</span><span class="av">${inU(netQ,UG)}</span></div>
  <p class="note" style="margin:0 0 6px">${gpart.map(x=>`${x[0]} <b class="${x[1]>=0?'pos-g':'neg-g'}">${x[1]>=0?'+':'−'}${mm(Math.abs(x[1]))}</b>`).join(' · ')}${Gq.claw?`. Restitution : le fonds finit sous son plus haut, vous rendez ${Math.round(Gq.clawSh*100)} % des commissions de performance des quatre derniers trimestres.`:''}</p>
  <div class="attr"><span class="an" style="color:var(--txt)">Trésorerie · votre gain net cumulé</span><span class="av"><b class="gold-g">${mm(mgrCash())}</b></span></div>
 </div>`;
 const coSel=(S.over||S.q>=QT())?'':`<div class="block"><div class="blockhead"><h2>Co-investissement</h2><span class="hint">trimestre prochain</span></div>
  <p class="note" style="margin-top:0">Part de votre trésorerie placée dans le fonds : elle suit son résultat net, gains comme pertes, et reste comptée dans la trésorerie à sa valeur du moment. 10 % au moins.</p>
  <div class="cisel">${COINVS.map(p=>`<button class="cip${Math.abs(p-coinvPct())<1e-9?' on':''}" data-p="${p}">${Math.round(p*100)} %</button>`).join('')}</div>
  <p class="note" id="cinote">${mm(coinvPct()*Math.max(0,mgrCash()))} exposés au prochain trimestre.</p></div>`;""")
rep("""  <div class="thold">${warn.map(t=>`<div class="flag" style="margin-top:12px"><span>${t}</span></div>`).join('')}""",
    """  <div class="thold">${ess}${warn.map(t=>`<div class="flag" style="margin-top:12px"><span>${t}</span></div>`).join('')}${coSel}""")
# concurrence repliée
resub(r'<div class="block"><div class="blockhead"><h2>La concurrence</h2><span class="hint">(.*?)</span></div>',
      '<div class="block"><details><summary style="font-size:15px;color:var(--txt);font-weight:600">La concurrence · RANKX</summary>')
s=s.replace('font-weight:600">La concurrence · RANKX</summary>','font-weight:600">La concurrence · ${1+S.rivals.filter(r=>r.cum>S.idx).length}<sup>${(1+S.rivals.filter(r=>r.cum>S.idx).length)===1?\'er\':\'e\'}</sup> sur quatre</summary>')
rep("\n   </tbody></table></div>\n","\n   </tbody></table></details></div>\n")
# « Vos gains » : absorbé par l'essentiel
resub(r'\n  <div class="block"><div class="blockhead"><h2>Vos gains</h2>.*?</details>\n  </div>','')
# commentaires + presse : un seul bloc replié
resub(r'<div class="block"><div class="blockhead"><h2>Ce qu\'ils en disent</h2><span class="hint">confiance \$\{Math\.round\(conf\(\)\)\}</span></div>',
      '<div class="block"><details><summary style="font-size:15px;color:var(--txt);font-weight:600">Ce qu\'on en dit · investisseurs, comité, presse</summary>')
def regrp(pat,new):
    global s;m=list(re.finditer(pat,s,re.S));assert len(m)==1,(len(m),pat[:60]);s=re.sub(pat,new,s,count=1,flags=re.S)
regrp(r"(Aucun carton ce trimestre\.'\}[^\n]*?</p></div>)\n  </div>\n  <div class=\"block\"><div class=\"wire\" style=\"border-color:var\(--line2\)\">",
      r'\1\n  <div class="wire" style="border-color:var(--line2);margin-top:10px">')
regrp(r"(\$\{S\.press\.slice\(1\)[^\n]*</details></div>)\n  </div>\n  <div class=\"block\"><details><summary style=\"font-size:15px;color:var\(--txt\);font-weight:600\">Ce qui s'est passé ce trimestre",
      r'\1\n  </details></div>\n  <div class="block"><details><summary style="font-size:15px;color:var(--txt);font-weight:600">Pourquoi la confiance a bougé')
resub(r'\n  \$\{S\.comm&&S\.comm\.ret!==null\?`<div class="block"><details>.*?</details></div>`:\'\'\}','')
rep(" theatre(app.querySelector('.pnlhead').parentElement);",""" theatre(app.querySelector('.pnlhead').parentElement);
 app.querySelectorAll('.cip').forEach(b=>b.onclick=()=>{S.coinvPct=+b.dataset.p;app.querySelectorAll('.cip').forEach(x=>x.classList.toggle('on',x===b));
  const n=document.getElementById('cinote');if(n)n.textContent=`${mm(coinvPct()*Math.max(0,mgrCash()))} exposés au prochain trimestre.`});""")
open(P,'w',encoding='utf-8').write(s);print('ok')
