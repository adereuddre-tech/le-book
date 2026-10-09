p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep(""" const bnSel=(S.over||S.q>=QT())?'':(()=>{const pf=Math.max(0,(S.mgrQ&&S.mgrQ.perf)||0),cur=S.bonI==null?MOT.i0:S.bonI,prev=S.bonPrev==null?MOT.i0:S.bonPrev,e=EXECM[S.bud.exec];
""",""" const bnSel=(S.over||S.q>=QT())?'':(()=>{const pf=Math.max(0,(S.mgrQ&&S.mgrQ.perf)||0),cur=S.bonI==null?MOT.i0:S.bonI,prev=S.bonPrev==null?MOT.i0:S.bonPrev,e=EXECM[S.bud.exec];
  if(!(pf>0))return noBonusPage(cur,o.qTotal);   /* lot 255 : sans commission de performance, pas de choix du bonus */
""")
rep("""function payBonus(){""","""/* lot 255 : page « pas de bonus » — aucune commission de performance ce trimestre, le desk joue le trimestre suivant au cran minimal */
function noBonusPage(cur,qT){const sv=S.bonEff,r={};[['now',0],['had',cur]].forEach(([k,i])=>{S.bonEff=i;r[k]=xWatch()});S.bonEff=sv;
 const F0=BONFX[0],Fc=BONFX[cur],eq=cur===0,row=(a,b,c)=>`<tr><td style="color:var(--txt)">${a}</td>${eq?'':`<td>${b}</td>`}<td class="neg-g">${c}</td></tr>`;
 const why=qT>0?`Le trimestre est positif, mais le fonds reste sous son plus haut historique : pas de commission de performance tant que les pertes passées ne sont pas effacées.`:`Le trimestre ${qT<0?'est négatif':'est nul'} : pas de commission de performance, donc rien à partager.`;
 return `<div class="block"><div class="blockhead"><h2>Pas de bonus ce trimestre</h2><span class="hint">aucune commission de performance</span></div>
  <p class="note" style="margin-top:0">${why} Le bonus d'équipe est une part de cette commission : il n'y a rien à verser, et le desk le sait. ${eq?'Votre taux est au minimum : rien ne change, mais rien ne motive non plus.':`Votre taux de ${dec(bonRate(cur)*100,1)} % reste acquis pour le prochain trimestre gagnant.`}</p>
  <p class="note">Le trimestre prochain, le desk travaille comme au cran minimal :</p>
  <table class="qt"><thead><tr><th>Effet</th>${eq?'':'<th>Avec votre taux</th>'}<th>Sans bonus</th></tr></thead><tbody>
   ${row("Coûts d'exécution",'×'+dec(Fc.c,2),'×'+dec(F0.c,2))}
   ${row('Bruit sur la lecture des dépêches','×'+dec(BONREAD[cur],2),'×'+dec(BONREAD[0],2))}
   ${row('Chances des anecdotes du desk',(BONWIN[cur]>=0?'+':'−')+Math.round(Math.abs(BONWIN[cur])*100)+' pts','−'+Math.round(Math.abs(BONWIN[0])*100)+' pts')}
   ${row('Extrêmes sentis · identifiés',Math.round(r.had.s*100)+' % · '+Math.round(r.had.i*100)+' %',Math.round(r.now.s*100)+' % · '+Math.round(r.now.i*100)+' %')}
   ${row('Risque de débauchage',Math.round(Fc.p*100)+' %',Math.round(F0.p*100)+' %')}
  </tbody></table>
  <p class="note">Ces effets durent un trimestre : le bonus revient dès qu'une commission de performance est versée.</p></div>`}
function payBonus(){""")
rep("""const PGS=[];if(gtSel)PGS.push(['Gate',gtSel]);PGS.push(['Trésorerie du gérant',tresSel+lmSel+coSel]);if(bnSel)PGS.push(["Bonus d'équipe",bnSel]);""",
    """const PGS=[];if(gtSel)PGS.push(['Gate',gtSel]);PGS.push(['Trésorerie du gérant',tresSel+lmSel+coSel]);if(bnSel)PGS.push([((S.mgrQ&&S.mgrQ.perf)||0)>0?"Bonus d'équipe":'Pas de bonus',bnSel]);""")
open(p,'w',encoding='utf-8').write(s)
