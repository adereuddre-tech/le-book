# Lot 203 : promesses aux investisseurs moins extrêmes. Objectif annoncé : conviction forte ×2 l'objectif standard
# (9 % → 6 % avant goalK), prophétie de gourou ×3 (15 % → 9 %). Récompenses et sanctions de confiance inchangées.
# Textes des objectifs et trophées qui citaient « 9 % » et « 15 % » mis à jour.
s=open("index.html",encoding="utf-8").read()
def rep(o,n,k=1):
    global s; c=s.count(o); assert c==k,(c,o[:100]); s=s.replace(o,n)
rep("p:`Vous annoncez ${pctc(0.09*gk)}. Si vous y arrivez","p:`Vous annoncez ${pctc(0.06*gk)}, le double d'un trimestre solide. Si vous y arrivez")
rep("ret:0.09,win:{lp:15,rc:0},lose:{lp:-8,rc:0}},","ret:0.06,win:{lp:15,rc:0},lose:{lp:-8,rc:0}},   /* lot 203 : ×2 l'objectif standard */")
rep("p:`Vous annoncez ${pctc(0.15*gk)} en un trimestre, devant les caméras.","p:`Vous annoncez ${pctc(0.09*gk)} en un trimestre, le triple d'un trimestre solide, devant les caméras.")
rep("ret:0.15,win:{lp:30,rc:0},lose:{lp:-10,rc:0}}","ret:0.09,win:{lp:30,rc:0},lose:{lp:-10,rc:0}}   /* lot 203 : ×3 */")
rep('d:"Annoncer au moins 9 % aux investisseurs, et les livrer."','d:"Annoncer une conviction forte ou une prophétie aux investisseurs, et la tenir."')
rep('d:"Tenir une prophétie de gourou : 15 % annoncés devant les caméras, 15 % livrés."','d:"Tenir une prophétie de gourou : le triple d\'un trimestre solide, annoncé devant les caméras et livré."')
open('index.html','w',encoding='utf-8').write(s);print('lot203 ok')
