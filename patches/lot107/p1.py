# Lot 107 : écran du budget. Premier trimestre : tout au cran 0 par défaut. Le cran choisi ressort (cadre doré épais,
# fond surligné, texte en clair). Un cran hors trésorerie reste lisible et l'écrit en rouge ; même mention, bien visible,
# sur les actions trop chères des événements.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("bud:{fo:3,bo:2,exec:3,risk:3,res:3,ret:3},","bud:{fo:0,bo:0,exec:0,risk:0,res:0,ret:0},")
rep(".lvl.on{background:var(--panel);border-color:var(--gold)}",
    ".lvl.on{background:var(--panel);border-color:var(--gold)}\n.lvl.tm.on{background:rgba(214,178,94,.20);border:2px solid var(--gold);box-shadow:0 0 0 3px rgba(214,178,94,.28)}\n.lvl.tm.on b,.lvl.tm.on i,.lvl.tm.on .tbp,.lvl.tm.on span{color:#fff;opacity:1}\n.hx{color:#E5483C;font-weight:700}")
rep(".lvl[disabled],.coll[disabled]{opacity:.25;cursor:not-allowed}",".lvl[disabled],.coll[disabled]{opacity:.55;cursor:not-allowed}\n.choice[disabled]{opacity:.6}\n.choice[disabled] .neg-g{opacity:1;font-weight:700}")
rep("${o?mm(l.bp*1e-4*budNav()):'hors caisse'}","${o?mm(l.bp*1e-4*budNav()):'<span class=\"hx\">hors trésorerie</span>'}")
open('index.html','w',encoding='utf-8').write(s);print('lot107 p1 ok')
