import json,sys,math,collections
def load(f,pl):
    R=[json.loads(l) for l in open(f) if l.strip()]
    for r,p in zip(R,json.load(open(pl))):r['seed']=p['seed']
    return R
R=load(sys.argv[1],sys.argv[2]);tags=sys.argv[3].split(',')
base={(r['cfg']['prof'],r['seed']):r for r in R if r['tag']=='base'}
def ms(a):
    n=len(a);m=sum(a)/n;return m,math.sqrt(sum((x-m)**2 for x in a)/(n-1)),math.sqrt(sum((x-m)**2 for x in a)/(n-1))/math.sqrt(n)
for t in tags:
    pr=[(r,base[(r['cfg']['prof'],r['seed'])]) for r in R if r['tag']==t and (r['cfg']['prof'],r['seed']) in base]
    a=ms([x['score'] for x,_ in pr]);b=ms([y['score'] for _,y in pr]);d=ms([x['score']-y['score'] for x,y in pr])
    print(f"{t:10} n={len(pr)} option {a[0]:.1f} σ{a[1]:.1f} | standard apparié {b[0]:.1f} σ{b[1]:.1f} | Δ {d[0]:+.1f} ±{d[2]:.1f} | surv {sum(not x['over'] for x,_ in pr)/len(pr):.2f} vs {sum(not y['over'] for _,y in pr)/len(pr):.2f}")
