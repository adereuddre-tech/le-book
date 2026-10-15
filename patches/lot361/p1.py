p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# traders à 5, 6, 7, 8, 9 pb par trimestre (cumul 5, 11, 18, 26, 35) ; la suite de l'équipe garde ses écarts
rep("""role:"trader actions, exécution à la voix",ic:"📞",bp:10,""","""role:"trader actions, le plus jeune du desk, exécution à la voix",ic:"📞",bp:5,""")
rep("""role:"cheffe du desk taux, la plus senior",ic:"🏦",bp:25,""","""role:"trader taux, lit la courbe à l'œil nu",ic:"🏦",bp:11,""")
rep("""role:"trader devises, expert exécution et algorithmes",ic:"🤖",bp:45,""","""role:"trader devises confirmé, expert exécution et algorithmes",ic:"🤖",bp:18,""")
rep("""role:"trader matières premières, un cigare par cargaison",ic:"🛢️",bp:70,""","""role:"trader matières premières senior, un cigare par cargaison",ic:"🛢️",bp:26,""")
rep("""role:"trader exotiques, vit à l'heure de Hong Kong",ic:"🐉",bp:100,""","""role:"trader exotiques, la plus chevronnée du desk, vit à l'heure de Hong Kong",ic:"🐉",bp:35,""")
for o,n in [("bp:140","bp:75"),("bp:190","bp:125"),("ic:\"🛰️\",bp:250","ic:\"🛰️\",bp:185"),("ic:\"🏛️\",bp:320","ic:\"🏛️\",bp:255"),("ic:\"🥷\",bp:400","ic:\"🥷\",bp:335"),("ic:\"🏅\",bp:490","ic:\"🏅\",bp:425"),("ic:\"📒\",bp:590","ic:\"📒\",bp:525")]:
    rep(o,n)
open(p,'w',encoding='utf-8').write(s)
