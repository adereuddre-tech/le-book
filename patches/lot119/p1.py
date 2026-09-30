# Lot 119 : gain brut des positions dans « l'essentiel » ; concurrents : l'événement extrême affiché à côté de l'accident de
# levier ; tableau des investisseurs allégé (sans % ni critère, noms plus larges) avec une ligne pour la holding royale
# (le plus sévère des quatre), critères en clair et règles de montant repliées ; dépêches : la confiance ne baisse pas
# quand l'effet net sur le fonds est nul ou positif.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
# essentiel
rep("<div class=\"attr\"><span class=\"an\">Confiance des investisseurs</span><span class=\"av\">${Math.round(lpQ0)} → <b>${Math.round(S.lp)}</b></span></div>",
    "<div class=\"attr\"><span class=\"an\">Gain brut des positions</span><span class=\"av\">${inU(o.P.grossM,UQ)}</span></div>\n  <div class=\"attr\"><span class=\"an\">Confiance des investisseurs</span><span class=\"av\">${Math.round(lpQ0)} → <b>${Math.round(S.lp)}</b></span></div>")
# concurrents
rep("st:(RIVSTRAT[r.style]||{}).nm,th:r.tailHit}))]","st:(RIVSTRAT[r.style]||{}).nm,th:r.tailHit,xr:(S.xRiv||[])[S.rivals.indexOf(r)]||0}))]")
rep("${a.th?`<br><span class=\"neg-g\" style=\"font-size:11px\">accident de levier</span>`:''}",
    "${a.th?`<br><span class=\"neg-g\" style=\"font-size:11px\">accident de levier</span>`:''}${Math.abs(a.xr||0)>=0.0005?`<br><span class=\"${cls(a.xr)}\" style=\"font-size:11px\">événement extrême ${sgnp(a.xr,1)}</span>`:''}")
# holding royale
rep(" {id:'ff',nm:'Fonds de fonds Albatros',",
    " {id:'roy',nm:'Couronne du Liquidistan (holding)',ic:'👑',w0:0,out:0.55,inn:0.05,crit:'Le plus sévère',royal:1,\n  rule:\"la holding de la famille royale se règle sur le plus sévère des quatre autres : elle rachète dès que l'un d'eux rachète, et ne souscrit que si tous souscrivent — au taux de rachat le plus fort et au taux de souscription le plus faible.\"},\n {id:'ff',nm:'Fonds de fonds Albatros',")
rep("function invs(){if(!S.inv)S.inv=INVR.map(d=>({id:d.id,w:d.w0,ntc:0}));return S.inv}",
    "function invs(){if(!S.inv)S.inv=INVR.map(d=>({id:d.id,w:d.w0,ntc:0}));if(!S.inv.some(v=>v.id==='roy'))S.inv.splice(3,0,{id:'roy',w:0,ntc:0});return S.inv}")
rep("const R=I.map(v=>{const r={id:v.id,vd:invVerdict(v.id,S.invH),",
    "const vds=I.filter(v=>v.id!=='roy').map(v=>invVerdict(v.id,S.invH)),vdMin=Math.min(...vds);\n const R=I.map(v=>{const r={id:v.id,vd:v.id==='roy'?vdMin:invVerdict(v.id,S.invH),")
rep("  if(v.w<0.01){if(!r.pay&&S.lp>=INVP.backLp){","  if(v.w<0.01){if(v.id!=='roy'&&!r.pay&&S.lp>=INVP.backLp){")
rep("B('souv',g>=1.6&&conf0>=78,()=>{const m=flowInB(0.20);S.bandTight=0.8;",
    "B('souv',g>=1.6&&conf0>=78&&!(invs().find(v=>v.id==='roy').w>0),()=>{const m=invFlow(invs().find(v=>v.id==='roy'),0.20*extNav());S.bandTight=0.8;")
rep("t:'La holding d\\'une maison royale veut entrer',d:\"Un mandat de taille, avec ses conditions : le comité sortira ses cartons plus tôt.\"",
    "t:'La Couronne du Liquidistan entre au capital',d:\"La holding de la famille royale du Liquidistan, émirat pétrolier et fiscal, prend un gros ticket. Ses conditions : le comité sortira ses cartons plus tôt, et elle se réglera sur le plus sévère de vos investisseurs.\"")
# tableau
i=s.index("function invTable(){");j=s.index("\nfunction ",i+10)
s=s[:i]+'''function invTable(){const I=invs(),E=extNav(),R=S.invQ||[];
 return `<table class="qt inv" style="margin-top:12px"><thead><tr><th style="text-align:left;width:58%">Investisseur</th><th>Part</th><th>Mouvement</th></tr></thead><tbody>
 ${I.map(v=>{const D=invD(v.id),r=R.find(x=>x.id===v.id)||{},h=v.w*E,never=v.id==='roy'&&!(h>1e-9)&&!r.pay;
  const mv=[r.pay>0?`<span class="neg-g">−${mm(r.pay)}</span>`:'',r.sub>0?`<span class="pos-g">+${mm(r.sub)}</span>`:'',r.cancel?'avis retiré':'',v.ntc>0?`<span class="neg-g">avis ${mm(v.ntc*h)}</span>`:''].filter(Boolean).join(' · ')||'—';
  return `<tr${never?' style="opacity:.45"':''}><td style="text-align:left">${D.ic} ${D.nm}</td><td>${never?'pas entrée':h>1e-9?mm(h):'partie'}</td><td>${never?'':mv}</td></tr>`}).join('')}</tbody></table>
 <p class="note" style="margin-top:6px">${INVR.map(D=>`${D.ic} <b>${D.nm.split(' (')[0]}</b> ${D.rule.replace(/^la holding de la famille royale /,'')}`).join('<br>')}</p>
 <details style="margin-top:4px"><summary class="note">Montants, préavis et confiance</summary><p class="note">Le critère décide si un investisseur rachète ou souscrit ; la confiance décide combien. Un rachat vaut une part de sa ligne : ${INVR.filter(D=>!D.royal).map(D=>`${D.nm.split(' ')[0].toLowerCase()==='caisse'?'caisse de retraite':D.nm.split(' ').slice(0,2).join(' ').toLowerCase()} ${Math.round(D.out*100)} %`).join(', ')}, holding royale ${Math.round(INVR.find(D=>D.royal).out*100)} % — à confiance 50 ; deux fois plus à confiance nulle, rien à confiance 100. Une souscription vaut ${Math.round(Math.min(...INVR.map(D=>D.inn))*100)} à ${Math.round(Math.max(...INVR.map(D=>D.inn))*100)} % de la ligne à confiance 50, proportionnellement à la confiance. Un rachat est annoncé par un avis, payé à la clôture suivante ; l'avis tombe si le critère repasse au vert. Au-delà de 15 % de l'encours en avis, vous pouvez activer la gate.</p></details>`}
'''+s[j:]
# textes de fin de trimestre : la holding
rep("  if(r.id==='ff')out.push(","  if(r.id==='roy'&&(invs().find(v=>v.id==='roy').w>0||r.pay))out.push(v<0?\"La Couronne du Liquidistan suit le plus inquiet de vos investisseurs : elle réduit sa ligne.\":v>0?\"Tous vos investisseurs souscrivent : la Couronne du Liquidistan aussi, avec parcimonie.\":\"La Couronne du Liquidistan attend que tout le monde soit content.\");\n  if(r.id==='ff')out.push(")
# dépêches : plancher de confiance si l'effet net sur le fonds est nul ou positif
rep(" return pieces;\n","",0) if False else None
i=s.index("function evPlans(");j=s.index(" return pieces;\n",i)
s=s[:j]+" /* lot 119 : si l'effet net de la dépêche sur le fonds est nul ou positif, la confiance ne baisse pas sur l'ensemble de la dépêche */\n pieces.forEach(pc=>pc.gz.forEach((z,k)=>{const net=(S.evImm||0)+pc.pay[k],i0=(S.evImmG&&S.evImmG.lp)||0;z.fl=(net>=0&&z.lp+i0<0)?-(z.lp+i0):0;z.lp+=z.fl}));\n"+s[j:]
rep("  o.fixRc.forEach(x=>add(gauge(0,x[0],`${x[1]} — ${ev.t}`)));\n }\n",
    "  o.fixRc.forEach(x=>add(gauge(0,x[0],`${x[1]} — ${ev.t}`)));\n }\n if(o.gz[si].fl>0)gr.lp+=gauge(o.gz[si].fl,0,`${ev.t} — effet net positif ou nul : la confiance ne baisse pas`).lp;   /* lot 119 */\n")
open('index.html','w',encoding='utf-8').write(s);print('lot119 p1 ok')
