p="index.html";s=open(p,encoding="utf-8").read()
import re
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:70],c);s=s.replace(o,n)
# reste du front office : 10, 12, 14, 16, 18, 21, 25 pb (cumul 45 … 151) ; back office : 3,3,4,4,5,5,6,6,7,8,9,10 (cumul 3 … 70)
for nm,old,new in [("Sœur Marie-Alpha",75,45),("Le professeur Onésime",125,57),("Priya",185,71),("Sir Mervyn",255,87),("Kenji",335,105),("Pr Ada",425,126),("Victoria",525,151),
    ("Gontran Report-à-Nouveau",5,3),("Josiane Suspens",12,6),("Firmin Tatillon",22,10),("Mireille",35,14),("Solange Pare-Feu",50,19),("Margaux",70,24),("Maître Fourche",95,30),("Lord Basil",125,36),("Cassandra",160,43),("Octave",200,51),("Hugo",245,60),("Dr Anouk",295,70)]:
    pat=re.compile(r'(\{who:"'+re.escape(nm)+r'"[^}]*?bp:)'+str(old)+r'\b')
    s,n=pat.subn(lambda m:m.group(1)+str(new),s);assert n==1,(nm,n)
open(p,'w',encoding='utf-8').write(s)
