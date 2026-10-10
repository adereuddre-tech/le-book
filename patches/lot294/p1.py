p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# 1. trésorerie : la marge passe sur la ligne du titre, la jauge reste en dessous du montant (trois lignes → deux et demie)
rep("""<button class="tile gold" data-gauge="gain"><span style="display:flex;justify-content:space-between;gap:6px"><span>Trésorerie</span></span><b id="gaintile" class="${cashView()>=0?'':'neg-g'}">${treso(cashView())}</b>${(()=>{const m=S.k&&S.k.some(v=>v)?marginPct(S.k):0;return `<span class="mgbar${m>=MGC.warn?' hot':''}" title="Marge utilisée"><i style="width:${Math.min(100,m/0.6*100).toFixed(0)}%;background:${mgCol(m)}"></i><em style="left:${(MGZ.watch/0.6*100).toFixed(0)}%"></em><em style="left:${(MGC.thr/0.6*100).toFixed(0)}%" class="thr"></em></span><span class="mgl" style="color:${mgCol(m)}">marge ${Math.round(m*100)} %</span>`})()}</button>""",
"""${(()=>{const m=S.k&&S.k.some(v=>v)?marginPct(S.k):0;return `<button class="tile gold" data-gauge="gain"><span class="tgh"><span>Trésorerie</span><span class="mgl" style="color:${mgCol(m)}">marge ${Math.round(m*100)} %</span></span><b id="gaintile" class="${cashView()>=0?'':'neg-g'}">${treso(cashView())}</b><span class="mgbar${m>=MGC.warn?' hot':''}" title="Marge utilisée"><i style="width:${Math.min(100,m/0.6*100).toFixed(0)}%;background:${mgCol(m)}"></i><em style="left:${(MGZ.watch/0.6*100).toFixed(0)}%"></em><em style="left:${(MGC.thr/0.6*100).toFixed(0)}%" class="thr"></em></span></button>`})()}""")
# 2. confiance : le carton du comité rejoint la tuile, sur la ligne du titre ; la valeur tient sur la même ligne
rep("""<span><i>Confiance</i><b>${S.phase!=='book'&&S.lastG?""","""<span><i>Confiance${cardTile()}</i><b>${S.phase!=='book'&&S.lastG?""")
rep("""   ${cardTile()}
  </div>""","""  </div>""")
rep("""return `<button class="tile cardt" data-gauge="card" aria-label="Carton du comité"><svg viewBox="0 0 18 24" width="17" height="23">""",
    """return `<span class="cardt" data-gauge="card" role="button" aria-label="Carton du comité"><svg viewBox="0 0 18 24" width="11" height="15">""")
rep("""/></svg></button>`}""","""/></svg></span>`}""")
rep(""".sgrid .tile.cardt{flex:0 0 24px;padding:1px}.sgrid .tile.cardt svg{width:14px;height:19px}""",
    """.tile .cardt{display:inline-flex;align-items:center;margin-left:6px;padding:2px 4px;vertical-align:-3px}.tile .cardt svg{display:block}
.tile.gold .tgh{display:flex;justify-content:space-between;align-items:baseline;gap:4px;white-space:nowrap}.tile.gold .mgl{font-family:var(--mono);font-size:9.5px;opacity:1}""")
rep(""".tile.cardt{flex:0 0 38px;align-items:center;justify-content:center;padding:4px}
.tile.cardt svg{display:block}""","")
open(p,'w',encoding='utf-8').write(s)
# 3. ajustements après capture : pourcentage de marge au bout de la jauge ; carton au bout de la jauge de confiance ; titre et valeur sur une ligne
s=open(p,encoding='utf-8').read()
rep("""<span class="tgh"><span>Trésorerie</span><span class="mgl" style="color:${mgCol(m)}">marge ${Math.round(m*100)} %</span></span>""","""<span class="tgh"><span>Trésorerie</span></span>""")
rep("""<em style="left:${(MGC.thr/0.6*100).toFixed(0)}%" class="thr"></em></span></button>`})()}""",
    """<em style="left:${(MGC.thr/0.6*100).toFixed(0)}%" class="thr"></em></span><span class="mgl" style="color:${mgCol(m)}" title="Marge utilisée">${Math.round(m*100)} %</span></span></button>`})()}""")
rep("""<b id="gaintile" class="${cashView()>=0?'':'neg-g'}">${treso(cashView())}</b><span class="mgbar""","""<b id="gaintile" class="${cashView()>=0?'':'neg-g'}">${treso(cashView())}</b><span class="mgrow"><span class="mgbar""")
rep("""<span><i>Confiance${cardTile()}</i><b>""","""<span><i>Confiance</i><b>""")
rep("""<span class="track"><i style="width:${conf()}%;background:${gc(conf())}"></i></span></button>""",
    """<span class="trrow"><span class="track"><i style="width:${conf()}%;background:${gc(conf())}"></i></span>${cardTile()}</span></button>""")
rep(""".tile .cardt{display:inline-flex;align-items:center;margin-left:6px;padding:2px 4px;vertical-align:-3px}""",
    """.tile .cardt{display:inline-flex;align-items:center;padding:0 0 0 2px}.tile .trrow,.tile .mgrow{display:flex;align-items:center;gap:5px}.tile .trrow .track{flex:1;margin-top:0}.tile .mgrow .mgbar{flex:1;margin-top:0}""")
rep(""".tile.gold .mgl{font-family:var(--mono);font-size:9.5px;opacity:1}""",""".tile.gold .mgl{font-family:var(--mono);font-size:10px;opacity:1;flex:0 0 auto}""")
open(p,'w',encoding='utf-8').write(s)
# 4. largeurs : la confiance tient sur une ligne, la trésorerie garde son montant entier ; contenu centré verticalement
s=open(p,encoding='utf-8').read()
rep(""".sgrid .tile.gauge{flex:1.45!important}.sgrid .tile.gold{flex:1.35!important}""",""".sgrid .tile.gauge{flex:1.3!important;justify-content:center;gap:5px}.sgrid .tile.gold{flex:1!important;justify-content:center}""")
open(p,'w',encoding='utf-8').write(s)
