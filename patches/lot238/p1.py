# Lot 238 : fin de trimestre en pages successives. Page 1 : performance du fonds (bandeau, ruban, l'essentiel, détails).
# Puis, s'il y a lieu : gate ; trésorerie du gérant (gain du trimestre, décomposition, tableau de trésorerie) ; bonus
# d'équipe. Chaque page a son bouton « Suite » (#nx) ; la dernière garde « Trimestre suivant » ou « Voir le rapport final ».
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
i0=s.index('function screenDebrief(o){');i1=s.index('\nfunction ',i0+20);F=s[i0:i1]
def fr(o,n,k=1):
    global F; c=F.count(o); assert c==k,(c,o[:100]); F=F.replace(o,n)
# 1) trésorerie : sortir les lignes du gérant de « l'essentiel »
a=F.index('  <div class="attr" style="margin-top:10px"><span class="an" style="color:var(--txt)">Votre gain du trimestre</span>')
b=F.index('</div>\n  <table class="qt" style="margin-top:12px"><thead><tr><th>Fonds</th>',a)
b=F.rfind('</div>',a,b)+len('</div>')  # fin de la ligne « Trésorerie · votre gain net cumulé »
tres1=F[a:b];F=F[:a]+F[b:]
c=F.index("  ${(()=>{const T0=S.tresQ0!==undefined?S.tresQ0:0,T1=mgrCash()")
d=F.index("</tbody></table>`})()}",c)+len("</tbody></table>`})()}")
tres2=F[c:d];F=F[:c]+F[d:]
fr(" const bnSel=(S.over||S.q>=QT())",
   " const tresSel=`<div class=\"block ess\"><div class=\"blockhead\"><h2>Trésorerie du gérant</h2><span class=\"hint\">trimestre ${S.q}/${QT()}</span></div>\n"+tres1.replace('`','\\`').replace('${','${') if False else
   " const tresSel=`<div class=\"block ess\"><div class=\"blockhead\"><h2>Trésorerie du gérant</h2><span class=\"hint\">trimestre ${S.q}/${QT()}</span></div>\n"+tres1+"\n"+tres2+"\n </div>`;   /* lot 238 */\n const bnSel=(S.over||S.q>=QT())")
# 2) page 1 : sans les blocs de choix ; bouton « Suite »
fr("${warn.map(t=>`<div class=\"flag\" style=\"margin-top:12px\"><span>${t}</span></div>`).join('')}${bnSel}${gtSel}${lmSel}${coSel}",
   "${warn.map(t=>`<div class=\"flag\" style=\"margin-top:12px\"><span>${t}</span></div>`).join('')}")
fr("""  <button class="cta" id="nx">${S.over?'Voir le rapport final':(S.q>=QT()?`Clôturer les ${DUR().ans} an${DUR().ans>1?'s':''}`:'Trimestre suivant')}</button></div>`;""",
   """  <button class="cta" id="nx">Suite · ${PGS[0][0]}</button></div>`;""")
# 3) liste des pages (avant le rendu de la page 1)
fr(" app.innerHTML=statusBar(true)+`<div class=\"fade\">\n  <div class=\"pnlhead\">",
   """ /* lot 238 : pages suivantes */
 const PGS=[];if(gtSel)PGS.push(['Gate',gtSel]);PGS.push(['Trésorerie du gérant',tresSel+lmSel+coSel]);if(bnSel)PGS.push(["Bonus d'équipe",bnSel]);
 const lastLab=S.over?'Voir le rapport final':(S.q>=QT()?`Clôturer les ${DUR().ans} an${DUR().ans>1?'s':''}`:'Trimestre suivant');
 app.innerHTML=statusBar(true)+`<div class="fade">
  <div class="pnlhead">""")
# 4) câblage : une fonction pour toutes les pages ; la fin d'origine devient finish()
p=F.index(" app.querySelectorAll('.bnp').forEach(b=>b.onclick=")
q=F.index(" goldFlush(3500);",p)
wire=F[p:q]
F=F[:p]+" const wire=()=>{\n"+wire+" };\n wire();\n"+F[q:]
fr(" if(!S.over&&S.q<QT()){const nx=document.getElementById('nx'),qb=document.createElement('button');",
   " const quitBtn=()=>{if(!S.over&&S.q<QT()){const nx=document.getElementById('nx'),qb=document.createElement('button');")
fr("""   document.getElementById('quitok').onclick=()=>{document.getElementById('modal').style.display='none';S.over='quit';save('screenDebrief');screenFinal();window.scrollTo(0,0)}}}
 document.getElementById('nx').onclick=()=>{""",
"""   document.getElementById('quitok').onclick=()=>{document.getElementById('modal').style.display='none';S.over='quit';save('screenDebrief');screenFinal();window.scrollTo(0,0)}}}};
 const showPg=k=>{
  app.innerHTML=statusBar(true)+`<div class="fade"><div class="pnlhead"><div class="q">FIN DU TRIMESTRE ${S.q} · ${k+2}/${PGS.length+1}</div>
   <div class="regime">${PGS[k][0]}</div></div><div class="thold">${PGS[k][1]}</div>
   <button class="cta" id="nx">${k<PGS.length-1?'Suite · '+PGS[k+1][0]:lastLab}</button></div>`;
  wire();window.scrollTo(0,0);
  if(k<PGS.length-1)document.getElementById('nx').onclick=()=>showPg(k+1);
  else{quitBtn();document.getElementById('nx').onclick=finish}};
 document.getElementById('nx').onclick=()=>showPg(0);
 const finish=()=>{""")
s=s[:i0]+F+s[i1:]
open('index.html','w',encoding='utf-8').write(s);print('lot238 ok')
