import sys,json,statistics as st
from collections import defaultdict
D=defaultdict(list)
for l in open(sys.argv[1]):
    l=l.strip()
    if not l or l=='FIN': continue
    p,j=l.split(' ',1)
    try: d=json.loads(j)
    except: continue
    D[p].append(d)
print('%-7s %4s %8s %7s %7s %7s %7s  %s'%('style','n','score','ecart','mediane','survie','q moy','causes de fin'))
for p,rows in D.items():
    s=[r['score'] for r in rows]
    surv=sum(1 for r in rows if not r['over'])
    q=sum(r['q'] for r in rows)/len(rows)
    c=defaultdict(int)
    for r in rows:
        if r['over']: c[r['over']]+=1
    print('%-7s %4d %8.1f %7.1f %7.1f %6.0f%% %7.2f  %s'%(p,len(rows),sum(s)/len(s),st.pstdev(s),st.median(s),100*surv/len(rows),q,dict(c)))
allr=[r for v in D.values() for r in v]
print('\nensemble : %d parties, survie %.0f%%, erreurs %d'%(len(allr),100*sum(1 for r in allr if not r['over'])/len(allr),sum(r['nerr'] for r in allr)))
