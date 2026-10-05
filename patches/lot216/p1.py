# Lot 216 : anecdotes et autres choix — effets trop faibles renforcés. Règle unique : un effet monétaire de moins de
# 5 pb (cash, gainBp, cashIfPos) est doublé, 5 pb au moins ; un effet sur les coûts de transaction de moins de 10 %
# (tcMult, tcMultQ, execBoost) est doublé, 10 % au moins. Les chiffres des textes sont réécrits en conséquence.
import re,sys
s=open("index.html",encoding="utf-8").read()
CH=re.compile(r'\{"?b"?:\s?"(?:[^"\\]|\\.)*",\s?"?s"?:\s?"(?P<s>(?:[^"\\]|\\.)*)",\s?"?e"?:\s?\{(?P<e>[^{}]*)\}\}')
fmt=lambda x:('%.4f'%x).rstrip('0').rstrip('.')
out=[];last=0;nch=0;fails=[]
for m in CH.finditer(s):
    st,e=m.group('s'),m.group('e');e2,s2=e,st;ch=False
    for key in ['cash','cashIfPos']:
        mm=re.search(r'(?<![A-Za-z])"?'+key+r'"?:\s?(-?[0-9.]+)',e2)
        if not mm:continue
        v=float(mm.group(1))
        if v==0 or abs(v)>=0.0005:continue
        obf=abs(v)*1e4;ob=round(obf);nb=max(5,2*ob);nv=(1 if v>0 else -1)*nb/1e4
        e2=e2[:mm.start(1)]+fmt(nv)+e2[mm.end(1):];ch=True
        obs=(('%.1f'%obf).rstrip('0').rstrip('.')).replace('.',',')
        r=re.compile(r'([+−-])\s?'+re.escape(obs)+r' pb')
        if r.search(s2):s2=r.sub(lambda q:q.group(1)+str(nb)+' pb',s2,count=1)
        else:fails.append(('pb',obs,st))
        if ob>=1:s2=s2.replace('(%d k$ sur 100 M$)'%(ob*10),'(%d k$ sur 100 M$)'%(nb*10))
    mm=re.search(r'"?gainBp"?:\s?(-?[0-9.]+)',e2)
    if mm:
        g=float(mm.group(1))
        if 0<abs(g)<5:
            ob=int(round(abs(g)));nb=max(5,2*ob);e2=e2[:mm.start(1)]+str(int(nb*(1 if g>0 else -1)))+e2[mm.end(1):];ch=True
            r=re.compile(r'([+−-])\s?'+str(ob)+r' pb')
            if r.search(s2):s2=r.sub(lambda q:q.group(1)+str(nb)+' pb',s2,count=1)
            else:fails.append(('gain',ob,st))
            s2=re.sub(r'\(%d k\$ sur 100 M\$\)'%(ob*10),'(%d k$ sur 100 M$)'%(nb*10),s2)
    for key in ['tcMult','tcMultQ','execBoost']:
        mm=re.search(r'(?<![A-Za-z])"?'+key+r'"?:\s?(-?[0-9.]+)',e2)
        if not mm:continue
        x=float(mm.group(1));d=x-1
        if d==0 or abs(d)>=0.0999:continue
        op=int(round(abs(d)*100));npct=max(10,2*op);nx=1+(1 if d>0 else -1)*npct/100
        e2=e2[:mm.start(1)]+fmt(nx)+e2[mm.end(1):];ch=True
        r=re.compile(r'([+−-])\s?'+str(op)+r' %')
        if r.search(s2):s2=r.sub(lambda q:q.group(1)+str(npct)+' %',s2,count=1)
        else:fails.append(('tc',op,st))
    if ch:
        nch+=1;full=m.group(0);b0=m.start();full2=full[:m.start('s')-b0]+s2+full[m.end('s')-b0:m.start('e')-b0]+e2+full[m.end('e')-b0:]
        out.append(s[last:m.start()]+full2);last=m.end()
out.append(s[last:]);s=''.join(out)
print('choix modifiés',nch,'· textes non réécrits',len(fails))
for f in fails:print('  ',f)
if '--write' in sys.argv:open('index.html','w',encoding='utf-8').write(s);print('lot216 écrit')
if '--write' in sys.argv:
    s=open("index.html",encoding="utf-8").read()
    o="const EXGAIN=40;   /* pb de 100 M$ par unité de baisse de coût d'origine */"
    assert s.count(o)==1
    s=s.replace(o,"const EXGAIN=80;   /* pb de 100 M$ par unité de baisse de coût d'origine ; lot 216 : 40 → 80 (−10 % de coûts = +8 pb, et non +4) */")
    open('index.html','w',encoding='utf-8').write(s);print('EXGAIN ok')
