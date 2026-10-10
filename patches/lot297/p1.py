p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
# 1. tuile Moral dans la barre d'état, à côté de la confiance
rep("""<span class="trrow"><span class="track"><i style="width:${conf()}%;background:${gc(conf())}"></i></span>${cardTile()}</span></button>""",
"""<span class="trrow"><span class="track"><i style="width:${conf()}%;background:${gc(conf())}"></i></span>${cardTile()}</span>${(()=>{const m=motV(),m0=S.motQ0;return `<span class="motrow" data-gauge="mot"><span><i>Moral</i><b>${m0!=null?gArrow(m0,m):Math.round(m)}</b></span><span class="track"><i style="width:${Math.round(m)}%;background:${gc(m)}"></i><em style="left:${MORAL.lo}%"></em><em style="left:${MORAL.hi}%"></em></span></span>`})()}</button>""")
rep(""".sgrid .tile.gauge{flex:1.3!important;justify-content:center;gap:5px}""",""".sgrid .tile.gauge{flex:1.45!important;justify-content:center;gap:4px}.sgrid .tile.gauge>span:first-child{flex-wrap:nowrap!important}.sgrid .tile.gauge>span:first-child b{font-size:12px;letter-spacing:-.2px}
.sgrid .tile.gauge>span.motrow{display:flex;flex-direction:column;flex-wrap:nowrap;gap:3px;justify-content:flex-start;align-items:stretch}
.tile .motrow{display:flex;flex-direction:column;gap:3px;margin-top:2px;padding-top:4px;border-top:1px solid var(--line)}.tile .motrow>span:first-child{display:flex;justify-content:space-between;align-items:baseline;font-size:10.5px;color:var(--dim)}.tile .motrow>span:first-child i{font-style:normal}.tile .motrow b{font-family:var(--mono);color:var(--txt);font-weight:500;font-size:12px!important;letter-spacing:-.2px}.tile .motrow .track{position:relative;height:5px;margin-right:17px}.tile .motrow .track em{position:absolute;top:0;bottom:0;width:1px;background:var(--dim);opacity:.6}""")
# 2. la fiche du moral
rep(""" } else if(id==='card'){""",""" } else if(id==='mot'){   /* lot 297 */
  const m=motV(),L=(S.motLog||[]).slice(-8).reverse();
  openModal('Moral du desk',`<p>Le moral de vos traders ne dépend que de l'argent et des égards. Chaque trimestre, il fait la moitié du chemin vers la cible de votre taux de bonus — 35 au minimum, 75 au cran le plus haut, sans bonus s'il n'y a pas de commission de performance — corrigée par vos locaux (garage −5, yacht +8). Une baisse de taux coûte 5 points par cran ; les petits gestes du quotidien (anecdotes) le déplacent d'un coup.</p>
   ${tbl([['Moral',`<b>${Math.round(m)}</b>`],['Cible de votre taux et de vos locaux',`${Math.round(motT(S.bonI==null?MOT.i0:S.bonI))}`],["Coûts d'exécution",'×'+dec(motC(),2)],['Bruit sur la lecture des dépêches','×'+dec(motR(),2)],['Chances des anecdotes du desk',(bonD()>=0?'+':'−')+Math.round(Math.abs(bonD())*100)+' pts'],['Risque de débauchage ce trimestre',Math.round(poachNow()*100)+' %']])}
   <p class="note">Sous ${MORAL.lo}, le desk peut partir en groupe : ${Math.round(motLo(m)*100)} % aujourd'hui, de plus en plus probable vers 0. Au-dessus de ${MORAL.hi}, il peut refuser toutes les offres des concurrents et redoubler d'efforts : ${Math.round(motHi(m)*100)} % aujourd'hui, de plus en plus probable vers 100.</p>
   ${L.length?tbl(L.map(x=>[`T${x.q+1} · ${x.why}`,`<span class="${cls(x.d)}">${x.d>=0?'+':'−'}${Math.abs(x.d).toFixed(1)}</span>`]),['Derniers mouvements','Δ']):''}`);
 } else if(id==='card'){""")
open(p,'w',encoding='utf-8').write(s)
