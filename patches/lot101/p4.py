# Lot 101d : relèvement des marges plus doux (×(1+0,04·choc), plafond 1,5) : jusqu'à 7 appels par partie au bot.
s=open('index.html',encoding='utf-8').read()
a="S.mgMult=Math.min(1.8,m0*(1+0.06*mh))";assert s.count(a)==1
s=s.replace(a,"S.mgMult=Math.min(1.5,m0*(1+0.04*mh))")
open('index.html','w',encoding='utf-8').write(s)
