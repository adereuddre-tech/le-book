p='index.html';s=open(p,encoding='utf-8').read()
def rep(o,n,k=1):
    global s;c=s.count(o);assert c==k,(o[:60],c);s=s.replace(o,n)
rep("""{id:'crowding',nm:'Tout le monde a le même book',ext:1,tgt:'crowd',H:1.5,sh:[0,0,0,-0.5],p:"Les grands fonds macro portaient les mêmes positions que vous. L'un d'eux réduit ; toutes vos lignes partent contre vous."},""",
    """{id:'crowding',nm:'Tout le monde a le même book',ext:1,tgt:'crowd',H:2.5,sh:[0,0,0,-0.5],p:"Les grands fonds macro réduisent tous en même temps. Ce qu'ils détenaient en masse se retourne : leurs achats chutent, leurs ventes remontent. Ceux qui étaient avec eux paient ; ceux qui étaient à contre-courant encaissent."},""")
rep("""  if(sc.tgt==='crowd'&&k[i])v-=Math.sign(k[i])*sc.H;""","""  if(sc.tgt==='crowd')v-=((S&&S.crowd&&S.crowd[i])||0)*sc.H;   /* lot 258 : la foule se déboucle — chaque marché recule du positionnement des autres fonds */""")
open(p,'w',encoding='utf-8').write(s)
