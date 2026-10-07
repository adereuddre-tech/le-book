# Lot 242 : dépenses et recettes des anecdotes pour la société de gestion, variées et significatives. Les petits montants
# d'origine (0,1 à 4 pb) avaient tous été ramenés au plancher de 5 pb (lot 216) puis passés au gérant (lot 222) : 50 k$
# presque à chaque fois. Nouvelle échelle, qui garde l'ordre entre les choix : 8 + 9 × √(montant d'origine en pb), en pb
# de l'encours de départ (1 pb → 17 pb, 4 pb → 26 pb, 30 pb → 57 pb ; 110 à 570 k$ sur 100 M$). Textes réécrits.
import re,json,os
s=open("index.html",encoding="utf-8").read()
M=json.load(open(os.path.join(os.path.dirname(__file__),'map.json'),encoding='utf-8'))
CH=re.compile(r'\{"?b"?:\s?"(?P<b>(?:[^"\\]|\\.)*)",\s?"?s"?:\s?"(?P<s>(?:[^"\\]|\\.)*)",\s?"?e"?:\s?\{(?P<e>[^{}]*)\}\}')
out=[];last=0;n=0;miss=[];txt=0
for m in CH.finditer(s):
    b,st,e=m.group('b'),m.group('s'),m.group('e')
    mo=re.search(r'(?<![A-Za-z])"?opex"?:\s?(-?[0-9.]+)',e)
    if not mo:continue
    old=float(mo.group(1));key=b.replace('\\"','"').replace("\\'","'")+'|'+str(round(old*1e4))
    if key not in M:miss.append(key);continue
    nv=M[key];e2=e[:mo.start(1)]+('%g'%(nv/1e4))+e[mo.end(1):]
    ok=round(abs(old)*1e5);nk=abs(nv)*10   # k$ sur 100 M$
    s2,c=re.subn(r'([+−-])\s?'+str(ok)+r' k\$',lambda q:q.group(1)+str(nk)+' k$',st,count=1)
    if not c:s2,c=re.subn(r'([+−-])\s?'+str(round(abs(old)*1e4))+r' pb',lambda q:q.group(1)+str(abs(nv))+' pb',st,count=1)
    txt+=c;n+=1
    full=m.group(0);b0=m.start()
    full2=full[:m.start('s')-b0]+s2+full[m.end('s')-b0:m.start('e')-b0]+e2+full[m.end('e')-b0:]
    out.append(s[last:m.start()]+full2);last=m.end()
out.append(s[last:]);s=''.join(out)
print('choix modifiés',n,'· textes réécrits',txt,'· non trouvés',len(miss))
open('index.html','w',encoding='utf-8').write(s)
# 2) les autres tableaux (conseil, investisseurs…) : valeur d'origine retrouvée par le libellé du choix (avant le lot 216)
import math
s=open("index.html",encoding="utf-8").read()
_J=json.load(open(os.path.join(os.path.dirname(__file__),'orig215.json'),encoding='utf-8'));O=_J['O'];cntb=_J['C']
out=[];last=0;n2=0;t2=0
for m in CH.finditer(s):
    b,st,e=m.group('b'),m.group('s'),m.group('e')
    mo=re.search(r'(?<![A-Za-z])"?opex"?:\s?(-?[0-9.]+)',e)
    if not mo:continue
    old=float(mo.group(1))
    if abs(old)*1e4>=10.5:continue   # déjà traité
    base=abs(O[b]) if (b in O and cntb[b]==1) else abs(old)*1e4
    nv=int(math.copysign(round(8+9*math.sqrt(base)),old))
    e2=e[:mo.start(1)]+('%g'%(nv/1e4))+e[mo.end(1):]
    ok=round(abs(old)*1e5)
    s2,c=re.subn(r'([+−-])\s?'+str(ok)+r' k\$',lambda q:q.group(1)+str(abs(nv)*10)+' k$',st,count=1)
    t2+=c;n2+=1
    full=m.group(0);b0=m.start()
    full2=full[:m.start('s')-b0]+s2+full[m.end('s')-b0:m.start('e')-b0]+e2+full[m.end('e')-b0:]
    out.append(s[last:m.start()]+full2);last=m.end()
out.append(s[last:]);s=''.join(out)
print('autres choix modifiés',n2,'· textes réécrits',t2)
open('index.html','w',encoding='utf-8').write(s)
