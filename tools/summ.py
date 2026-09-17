import json,sys,collections
for f in sys.argv[1:]:
    G=collections.defaultdict(list)
    for l in open(f):
        if l.startswith('FIN'):continue
        p,st,j=l.split(' ',2);G[(p,st)].append(json.loads(j))
    for k,R in sorted(G.items()):
        nav=sorted(r['nav'] for r in R)
        print(f,k,'n',len(R),'err',sum(r['nerr'] for r in R),'bloq',sum(not r['done'] for r in R),'q',round(sum(r['q'] for r in R)/len(R),1),'survie',sum(not r['over'] for r in R),'écarts',sum(r.get('bad',0) for r in R),'ev',sum(r['stats']['events'] for r in R),'poursuite',sum(r.get('npo',0) for r in R),'NAVméd',round(nav[len(nav)//2],3), R[0]['errs'][:1])
