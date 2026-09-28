P='/home/claude/le-book/index.html';s=open(P,encoding='utf-8').read()
def rep(old,new,k=1):
    global s;n=s.count(old);assert n==k,(n,old[:100]);s=s.replace(old,new)
# ---- budgets : chiffrer et expliquer ----
rep("""  return `coûts ×${dec(EXECM[i],2)} · débauchage ×${dec(RETM[i],2)} · indicateurs ${q>0.78?'très bruités':q>0.62?'bruités':q>0.45?'corrects':q>0.32?'précis':'très précis'}`""",
    """  return `coûts ×${dec(EXECM[i],2)} · débauchage ×${dec(RETM[i],2)} · bruit des indicateurs ±${dec(q,2)} σ (${q>0.78?'très bruités':q>0.62?'bruités':q>0.45?'corrects':q>0.32?'précis':'très précis'})`""")
rep("""fiabilité ${Math.abs(RESREL[i])<0.005?'de référence':(RESREL[i]>0?'+':'−')+Math.round(Math.abs(RESREL[i])*100)+' pts'}""",
    """fiabilité des sources ${Math.abs(RESREL[i])<0.005?'de référence':(RESREL[i]>0?'+':'−')+Math.round(Math.abs(RESREL[i])*100)+' pts'}""")
rep("function bandNow(){","""/* lot 82 : ce que veulent dire les chiffres de chaque budget, au cran choisi */
function budExpl(id){const i=S.bud[id];
 if(id==='exec')return `<p class="note"><b>Coûts</b> : chaque ordre coûte ${dec(EXECM[i],2)} fois le tarif de référence. <b>Débauchage</b> : risque de perdre un gérant ×${dec(RETM[i],2)}. <b>Indicateurs</b> : les tuiles tendance, portage et valeur affichent le vrai signal plus un bruit d'écart-type ${dec(TCVQ[i],2)} σ (standard ${dec(TCVQ[3],2)}, sans limite ${dec(TCVQ[6],2)}) ; à 0,30 σ, le signe affiché est juste dans environ ${Math.round(100*(0.5+0.5*Math.min(1,0.8/Math.max(0.3,TCVQ[i]))*0.8))} % des cas pour un signal moyen.</p>`;
 if(id==='risk')return `<p class="note"><b>Incidents</b> : fréquence ×${dec(RISKM[i],2)}, gravité ×${dec(RISKS[i]/RISKS[3],2)} par rapport au standard. <b>Accidents de levier</b> et appels de marge ×${dec(TAILM[i],2)}. ${Math.abs(RISKRC[i])>=0.05?`<b>Comité</b> : ${RISKRC[i]>0?'+':'−'}${dec(Math.abs(RISKRC[i]),1)} à chaque clôture.`:''}</p>`;
 const f=r=>Math.round(Math.min(0.99,(RELP[r]+RESREL[i]))*100);
 return `<p class="note"><b>Sources</b> : ${RESN[i]} par trimestre sur votre bureau. <b>Fiabilité</b> : la probabilité qu'une source dise vrai — à ce cran, faible ≈ ${f('faible')} %, moyenne ≈ ${f('moyenne')} %, forte ≈ ${f('forte')} %. <b>Pré-annonces</b> : ${Math.round(RESR[i]*100)} % des événements du trimestre vous sont signalés à l'avance. <b>Lecture des dépêches</b> : sur chaque dépêche, la probabilité de poursuite qu'on vous affiche est la vraie, décalée d'un écart typique de ±${Math.round(RESPH[i]*100)} pts${S.prof==='flux'?' (×0,6 pour le flux)':''} ; plus elle est serrée, plus vos choix sur les dépêches sont justes.</p>`}
function bandNow(){""")
rep("""<details style="margin-top:8px"><summary>À quoi sert ce budget · les sept crans</summary><p class="note">${b.d}</p><ul class="efl">""",
    """<details style="margin-top:8px"><summary>À quoi sert ce budget · les sept crans</summary><p class="note">${b.d}</p>${budExpl(b.id)}<ul class="efl">""")
# ---- desk : un seul bloc replié, à plat ----
L=s.split('\n')
a=[i for i,l in enumerate(L) if '<summary>Lire les sources · lecture consolidée · matrice</summary>' in l];assert len(a)==1;a=a[0]
b=a+11;assert L[b].strip()=='</details>' and L[b-1].strip()=='</details>',(L[b-1],L[b])
num=L[a+3];assert num.lstrip().startswith('${PROF().numeric?')
why=L[a+4];i0=why.index('<p class="note">');i1=why.index('</p></details></div>`')
whytxt=why[i0:i1+4]
hid=L[a+6];assert 'hidden>' in hid;hidtxt=hid.replace('<p class="note" hidden>','<p class="note">').strip()
new=['   <details style="margin-top:8px"><summary>Sous le capot · sources, avis du desk, matrice</summary>',
 '    <div class="kicker" style="margin:10px 0 4px">LIRE LES SOURCES</div>',
 '    '+hidtxt,
 '    <p class="note">Leur nombre et leur fiabilité dépendent du budget de recherche macro et de votre style. Les quatre tuiles de la barre du haut en donnent la lecture consolidée ; le rendement attendu de chaque marché en tient compte.</p>',
 '    <div class="kicker" style="margin:12px 0 4px">CE QUE PENSE LE DESK</div>',
 num.rstrip()+'</div>`:\'\'}',
 '    '+whytxt,
 '    <div class="wire" id="rsum"></div>',
 '    <div class="kicker" style="margin:12px 0 4px">MATRICE D\'EXPOSITION FACTORIELLE${S.rupture?\' <b style="color:var(--warn)">· rupture</b>\':\'\'}</div>',
 '    <div id="bmat" style="overflow-x:auto"></div>',
 L[a+9].rstrip(),
 '   </details>']
L[a:b+1]=new
s='\n'.join(L)
open(P,'w',encoding='utf-8').write(s);print('ok')
