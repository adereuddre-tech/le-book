# -*- coding: utf-8 -*-
"""Lot 69 — nuage : le point jaune pâle est le book juste avant le dernier changement, toutes les autres
positions comprises (et non plus le book de départ, souvent à plat)."""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep(""" const sq=sp/2,kB=(S.phase==='book'?S.k0:S.kVal)||null,gh=kB&&kB.length===S.k.length&&kB.some((v,i)=>v!==S.k[i])?{x:riskShown(weights(kB)).total/2,y:profitBook(kB)}:null;""",
""" /* lot 69 : S._kLast = book au dernier affichage ; dès qu'il diffère du book courant, il devient le point
    précédent (S._kGhost). Quel que soit le chemin du changement (case du book, dépêche, desk, accident),
    le point jaune est donc le book juste avant, les autres positions comprises. Remis à zéro chaque trimestre. */
 const sq=sp/2;
 if(!S._kLast||S._kLast.length!==S.k.length){S._kLast=[...S.k];S._kGhost=null}
 else if(S._kLast.some((v,i)=>v!==S.k[i])){S._kGhost=S._kLast;S._kLast=[...S.k]}
 const kB=S._kGhost,gh=kB&&kB.length===S.k.length&&kB.some((v,i)=>v!==S.k[i])?{x:riskShown(weights(kB)).total/2,y:profitBook(kB)}:null;""")
e.rep(" S.tailEv=null;S.tailDone=false;S.tailQ=null;\n"," S.tailEv=null;S.tailDone=false;S.tailQ=null;S._kLast=null;S._kGhost=null;\n")
e.rep("Point jaune pâle : votre fonds avant vos derniers changements de position.","Point jaune pâle : votre fonds juste avant votre dernier changement de position, toutes les autres positions comprises.")
e.done("lot 69")
