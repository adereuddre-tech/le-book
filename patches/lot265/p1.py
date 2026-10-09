p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("""   <div class="num thold ${cls(o.qTotal)}" style="font-size:18px;margin-top:4px">${bn(o.qTotal*o.q0,2)} sur ${moneyB(o.q0)} d'encours en début de trimestre</div>""",
"""   <div class="num thold ${cls(o.qTotal)}" style="font-size:18px;margin-top:4px">${bn(o.qTotal*o.q0,2)} sur ${moneyB(o.q0)} d'encours en début de trimestre</div>
   ${(()=>{const P=o.P||{},q=Math.max(1e-9,o.q0),it=[['Book',P.grossM],['Dépêches et extrêmes',P.evM],['Incidents',P.incM],['Collatéral',P.collM],['Frais',P.feeM]].filter(x=>Math.abs(x[1]||0)>=5e-5*q);   /* lot 265 : le trimestre en une ligne */
     return it.length?`<div class="qline thold">${it.map(x=>`<span>${x[0]} <b class="${cls(x[1])}">${sgn(x[1]/q,1)}</b></span>`).join('<i>·</i>')}<i>=</i><span><b class="${cls(o.qTotal)}">${sgn(o.qTotal,1)}</b></span></div>`:''})()}""")
rep(""".evdet{min-height:3.2em;""",""".qline{font-family:var(--mono);font-size:11.5px;color:var(--dim);margin-top:6px;display:flex;flex-wrap:wrap;gap:2px 6px;align-items:baseline}.qline i{font-style:normal;color:var(--dimmer)}
.evdet{min-height:3.2em;""")
open(p,'w',encoding='utf-8').write(s)
