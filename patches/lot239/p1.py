# Lot 239 : négocier une limite de risque au début du trimestre, en bas de la page du book (sous le bloc risque, là où
# s'affichent les limites et le risque de carton), et non plus à la fin du trimestre précédent. Mêmes règles : sans carton
# à la dernière clôture, pas deux trimestres de suite, confiance −3 payée au choix (remboursée si l'on revient sur « Ne
# pas négocier » avant de valider le book). L'effet est immédiat dans les limites affichées et l'alerte de carton.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
# bloc dans renderRisk (phase book)
rep("  ${flags}`;\n renderTC();\n}","  ${flags}${limNegBlock()}`;\n renderTC();\n}")
rep("function renderRisk(){","""/* lot 239 : négociation d'une limite, en début de trimestre */
function limNegOk(){return S.phase==='book'&&!S.qCard&&!(S.limNeg&&S.limNeg.q===S.q-1)}
function limNegBlock(){if(!limNegOk())return '';const cur=S.limNeg&&S.limNeg.q===S.q?S.limNeg.id:'';
 const O=[['','Ne pas négocier'],['vol',`Risque ${dec(limVol(1)*50,1)} → ${dec(limVol(1)*LIM.neg.vol*50,1)} %`],['stop',`Stop −${dec(limStop(1)*100,1)} → −${dec((limStop(1)/((S.bandTight)||1)+LIM.neg.stop)*((S.bandTight)||1)*100,1)} %`],['conc',`Concentration ${Math.round(limConc(1)*100)} → ${Math.round(Math.min(1,limConc(1)+LIM.neg.conc)*100)} %`]];
 return `<div style="margin-top:12px"><div class="kv"><span><b>Négocier une limite</b> · facultatif, ce trimestre</span><b></b></div>
  <p class="note" style="margin-top:0">Sans carton à la dernière clôture, vous pouvez demander au comité de relever une limite pour ce trimestre. Les investisseurs l'apprennent : confiance ${LIM.negLp}. Pas deux trimestres de suite.</p>
  <div class="cisel">${O.map(([id,t])=>`<button class="lmp${cur===id?' on':''}" data-l="${id}">${t}</button>`).join('')}</div></div>`}
if(typeof document!=='undefined')document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('.lmp');if(!b||!limNegOk())return;
 const id=b.dataset.l,was=S.limNeg&&S.limNeg.q===S.q&&S.limNeg.paid;
 if(id){if(!was)S.lp=Math.max(0,S.lp+LIM.negLp);S.limNeg={id,q:S.q,paid:1}}
 else{if(was)S.lp=Math.min(100,S.lp-LIM.negLp);S.limNeg=null}
 renderRisk();try{refreshStatus()}catch(err){}try{cardWarnUpdate()}catch(err){}});
function renderRisk(){""")
# fin de trimestre : plus de bloc de négociation
i0=s.index('function screenDebrief(o){')
a=s.index(" const lmSel=(S.over||S.q>=QT()",i0);b=s.index("})();\n",a)+len("})();\n")
s=s[:a]+" const lmSel='';   /* lot 239 : la négociation se fait au début du trimestre, page du book */\n"+s[b:]
rep(" app.querySelectorAll('.lmp').forEach(b=>b.onclick=()=>{const id=b.dataset.l;S.limNeg=id?{id,q:S.q}:null;app.querySelectorAll('.lmp').forEach(x=>x.classList.toggle('on',x===b))});\n","")
open('index.html','w',encoding='utf-8').write(s);print('lot239 ok')
