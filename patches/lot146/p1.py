# Lot 146 : résultat du trimestre — titres des tableaux et en-têtes de colonnes plus visibles.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("table.qt th{text-align:right;color:var(--dimmer);font-weight:500;padding:5px 0;border-bottom:1px solid var(--line);font-size:10.5px}","table.qt th{text-align:right;color:var(--txt);font-weight:700;padding:6px 0;border-bottom:1px solid var(--line2);font-size:11.5px;letter-spacing:.02em}")
rep(".blockhead h2{font-size:15px;font-weight:600}",".blockhead h2{font-size:17px;font-weight:700;color:var(--txt)}")
open('index.html','w',encoding='utf-8').write(s);print('lot146 ok')
