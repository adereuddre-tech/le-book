# -*- coding: utf-8 -*-
"""Lot 30 — ramener le gérant de flux au niveau du fondamental, par son propre pouvoir.

Mesuré : flux 39,1 M$ contre 23,2 au fondamental. L'écart ne vient ni de sa taille de book
ni de ses coûts — il vient de son intuition, juste **93 fois sur 100** sur le facteur dominant
du trimestre. C'est une quasi-omniscience, et c'est de l'alpha sans risque : le seul paramètre
du jeu qui se convertisse directement en argent sans contrepartie.

On le ramène à 0,78. L'intuition reste un vrai pouvoir — quatre fois sur cinq elle dit vrai,
là où le fondamental n'a que des sources probabilistes — mais elle cesse d'être une certitude,
et une intuition fausse une fois sur cinq coûte cher quand on taille gros.

Rien d'autre ne bouge : ni `modelScale`, ni `capture`, ni `lpMult`, ni les coûts, ni les
rachats. Un seul nombre, celui qui porte l'anomalie.
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
e.rep("""S.hunch={k,up:(rng()<0.93)===(S.f[k]>0)};  /* une intuition, pas une certitude */""",
      """S.hunch={k,up:(rng()<0.78)===(S.f[k]>0)};  /* une intuition, pas une certitude */""")
e.done("lot 30 — intuition du flux ramenee a 78 %")
