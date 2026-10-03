# Lot 178 : trésorerie négative autorisée pour les transactions (ordres du book, choix des événements, tuyaux, incidents) ;
# interdite pour les salaires (budget, bonus d'équipe, départs). Si la trésorerie est négative à la clôture du trimestre,
# la partie est perdue (règle inchangée).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("   if(c>0&&c>Math.max(0,mgrCash()+c)){refreshSend();toast(\"Votre société de gestion ne peut pas payer ces ordres.\");return}\n","")
rep(" const c=liveTC(),rest=mgrCash(),avail=Math.max(0,rest+c),ko=c>0&&c>avail,rb=redBlock();"," const c=liveTC(),rest=mgrCash(),avail=Math.max(0,rest+c),ko=false,rb=redBlock();")
rep("  if(nt)nt.textContent=avail>0?`Les positions grisées coûteraient plus que votre trésorerie (${mm(avail)}).`\n    :\"Votre trésorerie est vide : vous ne pouvez plus passer d'ordre payant ce trimestre.\";}",
    "  if(nt)nt.textContent=rest<0?`Après ces ordres, votre trésorerie est négative (${mm(rest)}) : c'est permis pendant le trimestre, mais elle doit être revenue au-dessus de zéro à la clôture, sinon c'est le dépôt de bilan.`:'';}")
import re
m=re.search(r"function segAfford\(i,v\)\{\s*const purse=Math\.max\(0,mgrCash\(\)\+liveTC\(\)\);\s*return costIf\(i,v\)<=purse\+1e-12;\s*\}",s);assert m
s=s[:m.start()]+"function segAfford(i,v){return true}   /* lot 178 : les ordres peuvent creuser la trésorerie */"+s[m.end():]
rep("ko=mg<0&&(-mg/1000)>mgrCash();","ko=false;",3)
rep("ko=o.a==='follow'&&o.cost>0&&o.cost>Math.max(0,mgrCash());","ko=false;")
rep("const ko=o.m>0&&mgrCash()<o.m*nav;","const ko=false;")
rep("const ko=o.m>0&&o.m*navB>mgrCash();","const ko=false;")
rep("Vous êtes à découvert de <em>${mm(-mgrCash())}</em> : dépenses bloquées jusqu'à la prochaine commission.`",
    "Vous êtes à découvert de <em>${mm(-mgrCash())}</em>. Les ordres et les événements restent possibles, mais pas le budget de l'équipe ; à la clôture, une trésorerie négative, c'est le dépôt de bilan.`")
open('index.html','w',encoding='utf-8').write(s);print('lot178 ok')
