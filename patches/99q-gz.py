# -*- coding: utf-8 -*-
"""Lot 28 — la mise en page cassée par le nouveau libellé de confiance.

`gz()` renvoyait DEUX éléments de premier niveau — le chiffre de confiance et le détail entre
parenthèses. Injecté dans une ligne en flex, le second devenait un troisième enfant et
écrasait la largeur du libellé : « Effets » passait sous « confiance −1 », et ailleurs un
paragraphe se retrouvait rendu une lettre par ligne, largeur réduite à zéro.

Correction : `gz()` ne renvoie plus qu'un seul élément, court. Le détail par canal passe en
info-bulle, là où il n'occupe aucune place.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep(""" const who=[];
 if(Math.abs(lp||0)>=0.05)who.push(`investisseurs ${sd1(lp)}`);
 if(Math.abs(rc||0)>=0.05)who.push(`comité ${sd1(rc)}`);
 return `<span class="${cls(d)}">confiance ${sd1(d)}</span>`
  +(who.length?` <span class="dim-g">(${who.join(', ')})</span>`:'');""",
""" const who=[];
 if(Math.abs(lp||0)>=0.05)who.push(`investisseurs ${(lp>=0?'+':'−')+Math.abs(lp).toFixed(0)}`);
 if(Math.abs(rc||0)>=0.05)who.push(`comité ${(rc>=0?'+':'−')+Math.abs(rc).toFixed(0)}`);
 /* un seul élément, court : deux enfants dans une ligne en flex écrasaient le libellé */
 return `<span class="${cls(d)}"${who.length?` title="${who.join(', ')}"`:''}>confiance ${sd1(d)}</span>`;""")
e.done("lot 28 — gz rendu sur un seul element")
