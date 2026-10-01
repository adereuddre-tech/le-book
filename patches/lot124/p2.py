# Lot 124, p2 : texte de fin de trimestre quand un investisseur retire son avis.
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("  if(r.id==='cr')out.push(v<0?","  if(r.cancel){out.push(`${invD(r.id).nm} retire son avis de rachat${r.id==='cr'?' : un trimestre positif lui suffit':' : son critère est repassé au vert'}.`);return}\n  if(r.id==='cr')out.push(v<0?")
open('index.html','w',encoding='utf-8').write(s);print('lot124 p2 ok')
