p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# exécution : libellés qui passent à la ligne, montants alignés
rep("""<div class="kv"><span><b style="color:#fff">Fourchette et impact au tarif · payés par le fonds</b></span><b style="color:#fff;font-size:17px">${cS(tot)}</b></div>
   <div class="kv"><span>Glissement du prix moyen · supporté par le fonds</span>${mn(execImpactAmt(tot,1,S.leakQ))}</div>
   <div class="kv"><span>Courtage · payé par votre société (${dec(COMB*1e4,1)} pb du notionnel)</span>${cS(COMB*bnTraded(S.k0,S.k))}</div>""",
    """<div class="kv"><span style="color:var(--txt)">Fourchette et impact au tarif · payés par le fonds</span><b>${cS(tot)}</b></div>
   <div class="kv"><span>Glissement du prix moyen · supporté par le fonds</span><b>${mn(execImpactAmt(tot,1,S.leakQ))}</b></div>
   <div class="kv"><span>Courtage · payé par votre société (${dec(COMB*1e4,1)} pb du notionnel)</span><b>${cS(COMB*bnTraded(S.k0,S.k))}</b></div>""")
rep("""compris dans la facture</span>${mn(tot/S.pwJK-tot)}</div>""","""compris dans la facture</span><b>${mn(tot/S.pwJK-tot)}</b></div>""")
# tableau des six styles : colonnes lisibles, première colonne fixe, défilement horizontal
rep("""<div style="overflow-x:auto"><table class="qt" style="margin-top:8px;font-size:12px"><thead><tr><th style="text-align:left"></th>${P.map(p=>`<th>${({syst:'Quant',fonda:'Fondamental',flux:'Flux'})[p.id]}</th>`).join('')}</tr></thead>""",
    """<div style="overflow-x:auto;-webkit-overflow-scrolling:touch"><table class="qt sty" style="margin-top:8px;font-size:12px"><thead><tr><th style="text-align:left"></th>${P.map(p=>`<th>${({syst:'Quant',fonda:'Fondamental',flux:'Flux',rv:'Valeur relative',tail:'Cygnes noirs',act:'Activiste'})[p.id]||p.id}</th>`).join('')}</tr></thead>""")
rep("""table.qt{table-layout:auto;width:100%}""","""table.qt{table-layout:auto;width:100%}
table.qt.sty{width:auto;min-width:860px}table.qt.sty td,table.qt.sty th{white-space:normal;min-width:110px;text-align:left;padding-right:8px}
table.qt.sty td:first-child,table.qt.sty th:first-child{position:sticky;left:0;background:var(--panel);min-width:120px;color:var(--txt);z-index:1}""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep("""["Capital de départ",p=>STYSEED[p.id]?'+'+dec(STYSEED[p.id]*1000,2)+' M$':'—']""","""["Capital de départ",p=>STYSEED[p.id]?'+'+dec(STYSEED[p.id]*1000*0.8,2)+' M$':'—']""")
open(p,'w',encoding='utf-8').write(s)
