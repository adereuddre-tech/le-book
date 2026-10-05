# Lot 222 : petites dépenses à la charge de la société de gestion. Les effets de trésorerie de fonctionnement (consultants,
# avocats, formations, heures sup, technicien, petites récupérations…), jusqu'à 30 pb, ne touchent plus le fonds (−5 pb
# d'un fonds de 100 M$ ne se voyaient pas) mais la caisse du gérant, au même montant en dollars (pb de l'encours de départ :
# 5 pb = 50 k$). Restent au fonds : les effets de financement et de marché (base de financement, prime, marge libérée ou
# rappelée) et les grosses licences ou frais de développement (au-delà de 30 pb). Nouveau champ e.opex ; pastille
# « société de gestion ±… » sur le choix.
import re,sys
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
# 1) bornes des tableaux d'anecdotes
def span(name):
    i=s.index('const '+name+'=') if ('const '+name+'=') in s else s.index(name+'=[')
    return i
CH=re.compile(r'\{"?b"?:\s?"(?:[^"\\]|\\.)*",\s?"?s"?:\s?"(?P<s>(?:[^"\\]|\\.)*)",\s?"?e"?:\s?\{(?P<e>[^{}]*)\}\}')
KEEP=re.compile(r'base|financ|marge|prime|libér|rappel|licence|développement|collatéral|repo|liquidité|\+40 pb|enfin, |neveu',re.I)
out=[];last=0;conv=[];kept=[]
for m in CH.finditer(s):
    st,e=m.group('s'),m.group('e')
    mm_=re.search(r'(?<![A-Za-z])"?cash"?:\s?(-?[0-9.]+)',e)
    if not mm_:continue
    v=float(mm_.group(1))
    if v==0:continue
    if abs(v)>0.00301 or KEEP.search(st):kept.append((round(v*1e4),st[:70]));continue
    bp=round(abs(v)*1e4);k=bp*10;sg='+' if v>0 else '−'
    key=e[mm_.start():mm_.end()].split(':')[0]
    e2=e[:mm_.start()]+key.replace('cash','opex')+':'+mm_.group(1)+e[mm_.end():]
    s2,n=re.subn(r'[+−-]\s?'+str(bp)+r' pb',sg+str(k)+' k$',st,count=1)
    if n:s2=s2.rstrip()+('' if s2.rstrip().endswith('.') else '.')+(' Payé par votre société de gestion.' if v<0 else ' Pour votre société de gestion.')
    conv.append((bp*(1 if v>0 else -1),s2[:90]))
    full=m.group(0);b0=m.start()
    full2=full[:m.start('s')-b0]+s2+full[m.end('s')-b0:m.start('e')-b0]+e2+full[m.end('e')-b0:]
    out.append(s[last:m.start()]+full2);last=m.end()
out.append(s[last:]);s=''.join(out)
print('passés au gérant :',len(conv),'· restés au fonds :',len(kept))
if '--list' in sys.argv:
    for c in conv:print('  G',c)
    for c in kept:print('  F',c)
s=s.replace('Elle reste. Le coût pèse immédiatement sur la performance.','Elle reste. Le coût est payé par votre société de gestion.',1)
s=s.replace('Il reste. La remise pèse sur le fonds.','Il reste. La remise est payée par votre société de gestion.',1)
# 2) application
rep("  if(e.cash){S.nav*=(1+e.cash);S.qEvM+=e.cash*navB0;msg.push(`Encours du fonds ${sgn(e.cash,1)}.`)}",
    "  if(e.cash){S.nav*=(1+e.cash);S.qEvM+=e.cash*navB0;msg.push(`Encours du fonds ${sgn(e.cash,1)}.`)}\n  if(e.opex){const a=e.opex*S.aum0;S.mgrCosts-=a;refreshGain();msg.push(`${a>=0?'+':'−'}${mm(Math.abs(a))} pour votre société de gestion.`)}   /* lot 222 */")
rep("  if(e.cash){pnl+=e.cash;msg.push(`Encours du fonds ${sgn(e.cash,1)} (${(e.cash*1e4).toFixed(0)} pb).`)}",
    "  if(e.cash){pnl+=e.cash;msg.push(`Encours du fonds ${sgn(e.cash,1)} (${(e.cash*1e4).toFixed(0)} pb).`)}\n  if(e.opex){const a=e.opex*S.aum0;S.mgrCosts-=a;refreshGain();msg.push(`${a>=0?'+':'−'}${mm(Math.abs(a))} pour votre société de gestion.`)}   /* lot 222 */")
rep("  if(e.cash)S.nav*=(1+e.cash);\n  if(e.tgt)S.tgt=e.tgt;","  if(e.cash)S.nav*=(1+e.cash);\n  if(e.opex){S.mgrCosts-=e.opex*S.aum0}   /* lot 222 */\n  if(e.tgt)S.tgt=e.tgt;")
# 3) pastille
rep("function winChip(e){","function opxChip(e){if(!e||!e.opex)return '';const a=e.opex*S.aum0;   /* lot 222 */\n return `<span class=\"stks\"><span class=\"stk\">société de gestion <em class=\"${a>=0?'pos-g':'neg-g'}\">${a>=0?'+':'−'}${mm(Math.abs(a))}</em></span></span>`}\nfunction winChip(e){")
rep("${stake(c)}${winChip(c.e)}${bkPrev(c.e,'exec')}","${stake(c)}${opxChip(c.e)}${winChip(c.e)}${bkPrev(c.e,'exec')}")
rep("<span>${fxTxt(c.s,c.e)}${winChip(c.e)}${bkPrev(c.e,'mid')}","<span>${fxTxt(c.s,c.e)}${opxChip(c.e)}${winChip(c.e)}${bkPrev(c.e,'mid')}")
rep("<span>${fxTxt(c.s,c.e)}${boardFx(c.e)}","<span>${fxTxt(c.s,c.e)}${boardFx(c.e)}${opxChip(c.e)}")
if '--write' in sys.argv:open('index.html','w',encoding='utf-8').write(s);print('lot222 écrit')
