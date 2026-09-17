import json,sys,math,collections
# usage : calib.py res1.jsonl:plan1.json [res2.jsonl:plan2.json …]
# le runner ne garde pas la graine : on la retrouve par l'ordre du plan
R=[]
for arg in sys.argv[1:]:
    f,pl=arg.split(':')
    try:rr=[json.loads(l) for l in open(f) if l.strip()]
    except FileNotFoundError:continue
    for r,p in zip(rr,json.load(open(pl))):r['seed']=p['seed']
    R+=rr
base={(r['cfg']['prof'],r['seed']):r for r in R if r['tag']=='base'}
def ms(a):
    n=len(a);m=sum(a)/n;sd=math.sqrt(sum((x-m)**2 for x in a)/max(1,n-1));return m,sd,sd/math.sqrt(n)
G=collections.defaultdict(list)
for r in R:
    if r['tag']!='base':G[r['tag']].append(r)
print('BUDGETS — écarts appariés au budget standard (M$ par partie)')
print(f"{'config':12}{'n':>4}{'Δcoût':>8}{'Δfrais':>8}{'±se':>6}{'Δscore':>8}{'±se':>6}{'ratio':>7}{'Δsurvie':>8}")
for k in sorted(G):
    if not k.startswith('bud/'):continue
    pr=[(r,base[(r['cfg']['prof'],r['seed'])]) for r in G[k] if (r['cfg']['prof'],r['seed']) in base]
    dc=ms([a['costs']-b['costs'] for a,b in pr]);df=ms([a['fees']-b['fees'] for a,b in pr]);ds=ms([a['score']-b['score'] for a,b in pr])
    sv=sum((not a['over'])-(not b['over']) for a,b in pr)/len(pr)
    print(f"{k:12}{len(pr):4}{dc[0]:8.2f}{df[0]:8.2f}{df[2]:6.2f}{ds[0]:8.2f}{ds[2]:6.2f}{(df[0]/dc[0] if abs(dc[0])>1e-9 else 0):7.2f}{sv:8.2f}")
print()
print('CHOIX INITIAUX — score (M$) et rendement, à comparer au standard')
bl=[base[(r['cfg']['prof'],r['seed'])] for r in G['vol/prud']] if 'vol/prud' in G else []
def row(k,a):
    s=ms([r['score'] for r in a]);t=ms([r['ret']*100 for r in a]);q=ms([r['q'] for r in a])[0]
    sv=sum(1 for r in a if not r['over'])/len(a)
    print(f"{k:14}{len(a):4}{s[0]:8.1f}{s[1]:7.1f}{s[2]:6.1f}{t[0]:8.1f}{t[1]:7.1f}{sv:7.2f}{q:5.1f}  frais {ms([r['fees'] for r in a])[0]:.1f} budget {ms([r['costs'] for r in a])[0]:.1f}")
print(f"{'config':14}{'n':>4}{'score':>8}{'σ':>7}{'±se':>6}{'rend%':>8}{'σ':>7}{'surv':>7}{'q':>5}")
seeds={r['seed'] for k in G if not k.startswith('bud/') for r in G[k]}
row('standard*',[r for r in R if r['tag']=='base' and ['syst','fonda','flux'][r['seed']%1000%3]==r['cfg']['prof'] and r['seed'] in seeds])
for k in sorted(G):
    if not k.startswith('bud/'):row(k,G[k])
print()
print('STYLES (tout standard)')
for p in ['syst','fonda','flux']:row(p,[r for r in R if r['tag']=='base' and r['cfg']['prof']==p])
print('erreurs',sum(r.get('nerr',0) for r in R),'crash',sum(1 for r in R if 'crash' in r),'n',len(R))
