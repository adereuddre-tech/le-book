p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)

rep("""nm:'Couronne du Farghestan (holding)'""","""nm:'Couronne du Farghestan'""")
rep("""rule:"la holding de la famille royale souscrit d'office""","""rule:"la famille royale souscrit d'office""")
rep(""".replace(/^la holding de la famille (royale|régnante) /,'')""",""".replace(/^la famille (royale|régnante) /,'')""")
rep("""holding royale ${Math.round(INVR""","""Couronne ${Math.round(INVR""")
rep("""d:"La holding de la famille régnante du Farghestan,""","""d:"La famille régnante du Farghestan,""")
open(p,'w',encoding='utf-8').write(s)
