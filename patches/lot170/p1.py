# Lot 170 : tableau des investisseurs — ligne « Total » (encours et mouvement net du trimestre).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("<td>${never?'':mv}</td></tr>`}).join('')}</tbody></table>",
    "<td>${never?'':mv}</td></tr>`}).join('')}\n <tr style=\"border-top:2px solid var(--line2);font-weight:700\"><td style=\"text-align:left\">Total</td><td>${mm(E)}</td><td>${(()=>{const n=R.reduce((a,r)=>a+(r.sub||0)-(r.pay||0),0);return Math.abs(n)>1e-9?`<span class=\"${cls(n)}\">${n>=0?'+':'−'}${mm(Math.abs(n))}</span>`:'—'})()}</td></tr></tbody></table>")
open('index.html','w',encoding='utf-8').write(s);print('lot170 ok')
