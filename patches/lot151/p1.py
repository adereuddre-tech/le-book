# Lot 151 : mi-parcours et résultat du trimestre — la performance du trimestre défile avec le tracé, comme le cumul.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const dv=` data-vals=\"${vals.map(v=>v.toFixed(2)).join(';')}\" data-dur=\"${anim?DRAW:0}\"`;",
    "const dv=` data-vals=\"${vals.map(v=>v.toFixed(2)).join(';')}\" data-dur=\"${anim?DRAW:0}\" data-q0=\"${(p[Math.min(n-1,opt.qs||0)]||100).toFixed(3)}\"`;")
rep("  const put=v=>{c.textContent=fmt(v)+suf;c.className='cnt '+(v>=100?'pos-g':'neg-g')};",
    "  const cq=tp.querySelector('.cntq'),q0=+sv.dataset.q0||100;\n  const put=v=>{c.textContent=fmt(v)+suf;c.className='cnt '+(v>=100?'pos-g':'neg-g');if(cq){const r=v/q0-1;cq.textContent=(r>=0?'+':'−')+dec(Math.abs(r)*100,1)+'\\u00a0%';cq.className='cntq '+(r>=0?'pos-g':'neg-g')}};")
rep("<span>T${S.q+1} À DATE <b class=\"${p[p.length-1]>=p[Math.min(p.length-1,S.tape.q0||0)]?'pos-g':'neg-g'}\">${sgnp(p[p.length-1]/p[Math.min(p.length-1,S.tape.q0||0)]-1,1)}</b> · CUMUL</span>",
    "<span>T${S.q+1} À DATE <b class=\"cntq\">—</b> · CUMUL</span>")
rep("<span>T${S.q} <b class=\"${cls(o.qTotal)}\">${sgn(o.qTotal,1)}</b> · CUMUL</span><b class=\"cnt\">—</b></div>",
    "<span>T${S.q} <b class=\"cntq\">—</b> · CUMUL</span><b class=\"cnt\">—</b></div>")
open('index.html','w',encoding='utf-8').write(s);print('lot151 ok')
