p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# le titre « Positions visibles du marché » passe à la ligne au lieu de chevaucher le pourcentage d'accident
rep("""<div class="kv" style="margin-top:6px"><span><b>👁 Positions visibles du marché</b></span><b style="color:var(--short)">accident ${Math.round(pv*100)} %</b></div>""",
    """<div class="kv" style="margin-top:6px"><span><b style="white-space:normal;text-align:left">👁 Positions visibles du marché</b></span><b style="color:var(--short);flex-shrink:0">accident ${Math.round(pv*100)} %</b></div>""")
rep(""".kv b{white-space:nowrap;text-align:right}""",""".kv b{white-space:nowrap;text-align:right}.kv>b{flex-shrink:0}""")
open(p,'w',encoding='utf-8').write(s)
