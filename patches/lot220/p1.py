# Lot 220 : budget — total du trimestre juste. Il affichait « 65 pb de 100 M$ · 1,0 M$ » : les points de base étaient le
# prix catalogue (avant les multiplicateurs de difficulté, de style et BUDK), le montant le coût réel (0,65 M$ ≠ 0,97 M$),
# et les bonus versés aux partants étaient comptés à part. Désormais : montant réel (bonus aux partants compris), son poids
# en points de base de l'encours ce trimestre, et en % par an ; les lignes et la liste des crans en montants réels.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("document.getElementById('btot').textContent=`${bp.toFixed(0)} pb de 100 M$ · ${mm(bp*1e-4*budNav())} · ${dec(bp*1e-4*budNav()*4/Math.max(1e-9,S.nav)*100,1)} % de l'encours par an${S.qSevM>0?` · bonus versés aux partants ${mm(S.qSevM)}`:''}`;",
    "{const c=bp*1e-4*budNav()+(S.qSevM||0),nv=Math.max(1e-9,S.nav);   /* lot 220 : coût réel, partants compris */\n  document.getElementById('btot').textContent=`${mm(c)} · ${(c/nv*1e4).toFixed(0)} pb de l'encours ce trimestre · ${dec(c*4/nv*100,1)} % par an${S.qSevM>0?` · dont bonus versés aux partants ${mm(S.qSevM)}`:''}`}")
rep("<span>${b.lv[cur].bp} pb · ${mm(b.lv[cur].bp*1e-4*budNav())}</span></div>",
    "<span>${mm(b.lv[cur].bp*1e-4*budNav())} · ${(b.lv[cur].bp*1e-4*budNav()/Math.max(1e-9,S.nav)*1e4).toFixed(0)} pb</span></div>")
rep("<li><b>${l.who}</b> · ${l.bp} pb · ${budEf(b.id,i)}</li>","<li><b>${l.who}</b> · ${mm(l.bp*1e-4*budNav())} · ${budEf(b.id,i)}</li>")
open('index.html','w',encoding='utf-8').write(s);print('lot220 ok')
