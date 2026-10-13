p="index.html";s=open(p,encoding="utf-8").read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# activiste : le coup du siècle s'ouvre à la participation — trois manœuvres d'affilée à mises croissantes, quel que soit le résultat
rep("""if(a.cds)S.bkStreak=0;else if(ok){S.bkStreak=(S.bkStreak||0)>0&&a.st>(S.bkLast||0)?S.bkStreak+1:1;S.bkLast=a.st}else{S.bkStreak=0;S.bkLast=0}""",
    """if(a.cds){S.bkStreak=0;S.bkLast=0}else{S.bkStreak=(S.bkStreak||0)>0&&a.st>(S.bkLast||0)?S.bkStreak+1:1;S.bkLast=a.st}   /* lot 341 : réussie ou non */""")
rep("""`série : ${st} réussite${st>1?'s':''} à mises croissantes — ${3-st} de plus pour le coup du siècle`""","""`série : ${st} manœuvre${st>1?'s':''} d’affilée à mises croissantes, réussie${st>1?'s':''} ou non — ${3-st} de plus pour le coup du siècle`""")
rep("""${!R.cds&&R.ok&&(S.bkStreak||0)>=3?'<p class="note" style="margin:6px 0 0">👑 Trois réussites d’affilée à mises croissantes : le coup du siècle vous sera proposé au prochain trimestre.</p>':''}""",
    """${!R.cds&&(S.bkStreak||0)>=3?'<p class="note" style="margin:6px 0 0">👑 Trois manœuvres d’affilée à mises croissantes : le coup du siècle vous sera proposé au prochain trimestre.</p>':''}""")
rep("""   de l'encours, probabilité et multiple affichés ; verdict à la clôture. Trois réussites d'affilée à mises croissantes""","""   de l'encours, probabilité et multiple affichés ; verdict à la clôture. Trois manœuvres d'affilée à mises croissantes (lot 341 : réussies ou non)""")
open(p,'w',encoding='utf-8').write(s)
