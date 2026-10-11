p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# pré-annonces et rumeurs : les marchés touchés, avec leur sens
rep("""out.push({src:'Pré-annonce',t:ev.rum||`Le desk entend parler de : « ${ev.t} »`,v:eventFactorVec(ev),rel:'moyenne',ev:true,truth:true})}});""",
    """out.push({src:'Pré-annonce',t:ev.rum||`Le desk entend parler de : « ${ev.t} »`,v:eventFactorVec(ev),rel:'moyenne',ev:true,truth:true,hit:ev.hit})}});""")
rep("""out.push({src:'Pré-annonce',t:f.rum||`Le desk entend parler de : « ${f.t} »`,v:eventFactorVec(f),rel:'faible',ev:true,truth:false})}""",
    """out.push({src:'Pré-annonce',t:f.rum||`Le desk entend parler de : « ${f.t} »`,v:eventFactorVec(f),rel:'faible',ev:true,truth:false,hit:f.hit})}""")
rep(""" const one=r=>`<div class="news ${r.ev?'rum':''}"><span class="src">${r.src.toUpperCase()}</span><span>${r.t}<div class="chips">""",
""" /* lot 310 : les marchés que la source dit toucher — ceux de la dépêche annoncée, sinon les trois plus exposés à ses facteurs */
 const tk=r=>{let L;if(r.hit)L=Object.keys(r.hit).filter(sy=>IDX[sy]!==undefined&&mktOpen(IDX[sy])).map(sy=>({sy,z:r.hit[sy]}));
   else L=INSTR.map((x,i)=>({sy:x.sym,i,z:x.b.reduce((a,b,k)=>a+b*(r.v[k]||0),0)})).filter(o=>mktOpen(o.i));
   L=L.filter(o=>Math.abs(o.z)>1e-6).sort((a,b)=>Math.abs(b.z)-Math.abs(a.z)).slice(0,3);
   return L.length?`<div class="chips tks">${L.map(o=>`<i class="${o.z>0?'up':'dn'}">${o.sy} ${o.z>0?'▲':'▼'}</i>`).join('')}</div>`:''};
 const one=r=>`<div class="news ${r.ev?'rum':''}"><span class="src">${r.src.toUpperCase()}</span><span>${r.t}${tk(r)}<div class="chips">""")
rep(""".chips i.sure{""",""".chips.tks{margin-top:4px}.chips.tks i{font-family:var(--mono);font-weight:500}
.chips i.sure{""")
open(p,'w',encoding='utf-8').write(s)
