# Lot 116 : tableau des impacts d'une unité (book) en colonnes vente | achat, comme les boutons ; lignes rentabilité / risque.
# Styles par leurs pouvoirs (coûts et patience ne les classaient pas) : intuition du flux juste 75 % du temps (85 %),
# book du modèle du quant à 90 % de la vol cible (80 %).
s=open('index.html',encoding='utf-8').read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:90]); s=s.replace(o,n)
rep("gl=`<div class=\"rgrid2\"><div><span class=\"k\">+1</span> rentabilité ${ex1} · risque ${pct1(rP)}</div><div><span class=\"k\">−1</span> rentabilité ${pM} · risque ${pct1(rM)}</div></div>`}",
    "gl=`<div class=\"rgrid3\"><span></span><span class=\"k\">−1 · vente</span><span class=\"k\">+1 · achat</span><span class=\"lb\">rentabilité</span><span>${pM}</span><span>${ex1}</span><span class=\"lb\">risque</span><span>${pct1(rM)}</span><span>${pct1(rP)}</span></div>`}")
rep(".rgrid2 .k{",".rgrid3{width:100%;font-family:var(--mono);font-size:11px;color:var(--dim);margin-top:4px;display:grid;grid-template-columns:auto 1fr 1fr;gap:1px 10px;align-items:baseline}\n.rgrid3 .k{color:var(--dimmer);font-size:10px}\n.rgrid3 .lb{color:var(--dimmer)}\n.rgrid2 .k{")
rep("S.hunch={k,up:(rng()<0.85)===(S.f[k]>0)};","S.hunch={k,up:(rng()<0.75)===(S.f[k]>0)};")
rep("modelScale:0.80","modelScale:0.90")
rep("ne vise que 16 % de vol : régulier, mais il laisse du rendement","ne vise que 18 % de vol : régulier, mais il laisse du rendement")
open('index.html','w',encoding='utf-8').write(s);print('lot116 p1 ok')
