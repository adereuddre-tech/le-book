# Lot 190 : budget — chaque personne affiche son coût supplémentaire en dollars (au lieu des pb de base, trompeurs une fois
# les multiplicateurs appliqués) et le coût de l'équipe jusqu'à elle ; indemnités de départ affichées comme appliquées (un
# demi-trimestre de salaire) ; montants à trois chiffres significatifs.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const mm=x=>{","const m3=x=>{const a=Math.abs(x)*1e9,sg=x<0?'−':'';const f=(v,u)=>sg+Number(v.toPrecision(3)).toString().replace('.',',')+' '+u;return a>=1e9?f(a/1e9,'Md$'):a>=1e6?f(a/1e6,'M$'):f(a/1e3,'k$')};   /* lot 190 */\nconst mm=x=>{")
rep("<span class=\"tbp\">${l.bp} pb<br>${o?mm(l.bp*1e-4*budNav()):",
    "<span class=\"tbp\">${i>0?'+'+m3((l.bp-b.lv[i-1].bp)*1e-4*budNav()):'—'}<br>${o?'équipe '+m3(l.bp*1e-4*budNav()):")
rep("<br><span class=\"neg-g\">départs −${mm((b.lv[S.budPrev[b.id]].bp-l.bp)*1e-4*budNav())}</span>","<br><span class=\"neg-g\">départs −${m3(0.5*(b.lv[S.budPrev[b.id]].bp-l.bp)*1e-4*budNav())}</span>")
open('index.html','w',encoding='utf-8').write(s);print('lot190 ok')
