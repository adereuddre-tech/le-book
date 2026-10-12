p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# 1. la pastille « portage » du book : signal du cycle + portage structurel, en un seul nombre (même échelle σ que le signal)
rep("""function tcvChip(nm,z){return `<i class="${z>0?'up':z<0?'dn':''}">${nm} ${chip(z)}</i>`}""",
    """function tcvChip(nm,z){return `<i class="${z>0?'up':z<0?'dn':''}">${nm} ${chip(z)}</i>`}
/* lot 316 : portage affiché = signal du cycle + portage structurel ramené en σ du signal */
function kapZ(i){const x=INSTR[i];return kap(i,(S.factEst||[])[3]||0)/Math.max(1e-9,x.sigQ*SIGW.c)}""")
rep("""return ['t','c','v'].map(z=>`<span class="${z===m?'mine':'oth'}">${tcvChip(SIGNM[z],S.tcvEst[z][i])}</span>`).join('')""",
    """return ['t','c','v'].map(z=>`<span class="${z===m?'mine':'oth'}">${tcvChip(SIGNM[z],S.tcvEst[z][i]+(z==='c'?kapZ(i):0))}</span>`).join('')""")
# 2. le détail d'un marché : portage = cycle + structurel, les deux lignes
rep("""['Portage',L(e.c[i]),pc(XP.c)],""","""['Portage · cycle',L(e.c[i]),pc(XP.c)],""")
rep("""...(Math.abs(XP.drift)>1e-6?[['Portage structurel','',pc(XP.drift)]]:[]),""","""...(Math.abs(XP.drift)>1e-6?[['Portage · structurel',KAPPA[x.sym]&&KAPPA[x.sym][1]?'selon l\\'appétit':'connu',pc(XP.drift)]]:[]),""")
rep("""<p><em>Portage</em> — ${TCVTXT.c.d[x.grp]}</p>""","""<p><em>Portage</em> — ${TCVTXT.c.d[x.grp]||''} Il a deux parts : le <em>structurel</em>, connu exactement (dividendes et prime de risque, prime de terme, écart de taux, coût de stockage, contango), et le <em>cycle</em>, que le desk lit avec du bruit. La pastille du book les additionne.</p>""")
rep("""'Matières premières':"Rendement de roulement des contrats à terme : positif quand la courbe est en déport, négatif en report."},eff:0.10},""",
    """'Matières premières':"Rendement de roulement des contrats à terme : positif quand la courbe est en déport, négatif en report.",Exotiques:"Ce que coûte ou rapporte de tenir la position : contango des contrats de volatilité (cher quand le marché est calme, payant dans la peur), coût de financement d'une crypto, roulement d'un contrat de fret ou de carbone."},eff:0.10},""")
# 3. glossaire
rep("""'portage':"Ce que rapporte une position si les prix ne bougent pas : l'écart de taux entre deux devises, la pente d'une courbe, le coût de stockage d'une matière première.",""",
    """'portage':"Ce que rapporte une position si les prix ne bougent pas : dividendes et prime de risque des actions, prime de terme des obligations, écart de taux entre deux devises, coût de stockage d'une matière, contango du VIX. Une part est structurelle et connue ; l'autre suit le cycle.",""")
open(p,'w',encoding='utf-8').write(s)
