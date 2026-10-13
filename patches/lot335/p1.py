p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# Octave (O2) : marge −20 %, et une fois par an il fait renoncer le prime broker à un appel de marge ; Anouk (A2) : séminaire, moral +25
rep("""*(boH(10)?0.85:1)}   /* lot 279 : Octave */""","""*(boH(10)?0.80:1)}   /* lot 279 : Octave ; lot 335 : −20 % */""")
rep("""pw:"marge exigée −15 % sur tout le book"}""","""pw:"marge exigée −20 % sur tout le book ; une fois par an, il fait renoncer le prime broker à un appel de marge"}""")
rep("""pw:"débauchage ÷2 ; incidents −20 %"}""","""pw:"débauchage ÷2 ; incidents −20 % ; une fois par an, un séminaire : moral +25"}""")
rep("""Ne compte pour l'année que si un extrême ou une cyberattaque tombe."}];""","""Ne compte pour l'année que si un extrême ou une cyberattaque tombe."},
 {id:'oc',bo:10,ic:'💱',nm:'Octave',inc:1,t:"Un coup de fil au prime broker",d:"Si un appel de marge tombe, il obtient un délai jusqu'à la clôture : rien n'est coupé, aucune perte de confiance. Se joue sur l'écran de l'appel (et tout seul à la clôture) ; ne compte pour l'année que s'il sert."},
 {id:'an',bo:12,ic:'🧘',nm:'Dr Anouk',t:"Le séminaire",d:"Deux jours au vert pour tout le desk : moral +25 d'un coup, dès ce trimestre (coûts, lecture, anecdotes, débauchage)."}];""")
rep("""  if(o.id==='fi')gauge(0,5,"Audit propre de Firmin");""","""  if(o.id==='fi')gauge(0,5,"Audit propre de Firmin");
  if(o.id==='an'){motAdd(25,"séminaire d'Anouk");toast('🧘 <b>Dr Anouk</b> emmène le desk au vert : moral +25.')}""")
# appel de marge en cours de trimestre : l'option Octave
rep("""  {id:'pb',b:"Laisser le prime broker liquider",s:`Il coupe ${Math.round(P.f*100)} % de chaque ligne au pire prix : ${mm(P.c2)} à votre charge.`,c:-5,k:P.k2,tc:P.c2}];""",
    """  {id:'pb',b:"Laisser le prime broker liquider",s:`Il coupe ${Math.round(P.f*100)} % de chaque ligne au pire prix : ${mm(P.c2)} à votre charge.`,c:-5,k:P.k2,tc:P.c2}];
 {const oc=PW.find(x=>x.id==='oc');if(oc&&pwAvail(oc))O.unshift({id:'oc',b:"💱 Octave appelle le prime broker",s:"Il obtient un délai jusqu'à la clôture : rien n'est coupé, et plus d'appel ce trimestre. Compté pour l'année.",c:0})}""")
rep("""  if(o.id==='inj'){const x=P.inj;""","""  if(o.id==='oc'){(S.pwLast=S.pwLast||{}).oc=S.q;S.ocGrace=S.q}
  else if(o.id==='inj'){const x=P.inj;""")
rep("""  if(marginPct(S.k)>MGC.thr){const r0=liveRet();S.k=S.k.map(()=>0);""","""  if(o.id!=='oc'&&marginPct(S.k)>MGC.thr){const r0=liveRet();S.k=S.k.map(()=>0);""")
rep(""" if(S.live&&marginPct(S.k)>MGC.thr+1e-9){screenMarginCall();""",""" if(S.live&&S.ocGrace!==S.q&&marginPct(S.k)>MGC.thr+1e-9){screenMarginCall();""")
# à la clôture : Octave joue tout seul s'il est disponible (ou a déjà obtenu le délai)
rep("""   if(mgTrough>MGC.thr){
    const f=Math.max(0.05,Math.min(MGC.cut,1-MGC.thr/mgTrough));""","""   const oc=PW.find(x=>x.id==='oc');
   if(mgTrough>MGC.thr&&(S.ocGrace===S.q||(oc&&pwAvail(oc)))){(S.pwLast=S.pwLast||{}).oc=S.q;S.ocSaved=S.q;S.qLog.push("appel de marge évité par Octave")}
   else if(mgTrough>MGC.thr){
    const f=Math.max(0.05,Math.min(MGC.cut,1-MGC.thr/mgTrough));""")
rep(""" if(S.marginCall)warn.push(""",""" if(S.ocSaved===S.q-1)warn.push(`💱 <b>Octave a appelé le prime broker</b> : l'appel de marge de la clôture n'a rien coupé.`);
 if(S.marginCall)warn.push(""")
open(p,'w',encoding='utf-8').write(s)
s=open(p,encoding='utf-8').read()
rep("""o.inc?(pwAvail(o)?'disponible · se joue sur l’incident'""","""o.inc?(pwAvail(o)?(o.id==='oc'?'disponible · joue sur l’appel de marge':'disponible · se joue sur l’incident')""")
open(p,'w',encoding='utf-8').write(s)
