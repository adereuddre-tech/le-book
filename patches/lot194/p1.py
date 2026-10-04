# Lot 194 : logos des fonds dans le tableau des concurrents (écran de résultat), celui du joueur compris : écusson de 18 px
# devant le nom (S.crest pour vous, r.crest ou RIVCREST pour les concurrents, comme rivCol).
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("const all=[{nm:S.fundName,v:o.qTotal,me:1,",
    "const crI=i=>`<span style=\"display:inline-block;vertical-align:-4px;margin-right:6px\">${crestSvg(i,16)}</span>`;   /* lot 194 */\n const all=[{nm:crI(S.crest!==undefined?S.crest:0)+S.fundName,v:o.qTotal,me:1,")
rep("...S.rivals.map(r=>({nm:r.nm+'<span class=\"bossn\">'+r.boss+'</span>',v:r.last,",
    "...S.rivals.map((r,j)=>({nm:crI(r.crest!==undefined?r.crest:RIVCREST[j%4])+r.nm+'<span class=\"bossn\">'+r.boss+'</span>',v:r.last,")
open('index.html','w',encoding='utf-8').write(s);print('lot194 ok')
