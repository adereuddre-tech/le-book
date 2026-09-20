# -*- coding: utf-8 -*-
"""Lot 34 — noms de fonds ×3, et l'écusson qui va avec le nom.

Demande : « multiplie par 3 le nombre de noms proposés ». Le nom est `NAME1 + NAME2`
(40 × 30 = 1 200 combinaisons). La partie qui porte l'identité est NAME1 (Kestrel, Beacon
Hill, Stonebridge…) ; NAME2 n'est qu'une raison sociale. NAME1 passe de 40 à 120 : trois fois
plus de noms, trois fois plus de combinaisons (3 600).

Les 80 nouveaux sont écrits par thème d'écusson (phare, sommet, rose des vents, clé de voûte,
chêne, ancre, pont, tour, faucon, sablier, étoile polaire, rouage : 6 à 7 chacun), et 28 des 40
anciens y sont rattachés. « Proposez-m'en un » choisit alors l'écusson assorti — tant que le
joueur n'en a pas choisi un lui-même : un clic sur un écusson le fige. Aucun nom de fonds
célèbre (Bridgewater, Citadel, Millennium… sont déjà détournés chez les concurrents).
"""
import sys; sys.path.insert(0,'patches')
from _lib import Ed
e=Ed()
OLD='const NAME1=["Blackpoint","Ironwood","Brightwater","Northgate","Silverline","Stonebridge","Kestrel","Redcliff","Harborview","Greystone","Larkspur","Wolfstone","Copperfield","Windward","Fairhaven","Tidewater","Cobalt","Highfield","Sablewood","Cromwell","Ashford","Meridian","Sterling","Whitmore","Longbow","Falconer","Marbury","Quarrystone","Eastbourne","Thornhill","Deepwater","Pinehurst","Ravenswood","Castlegate","Summit Rock","Old Harbour","Beacon Hill","Two Rivers","Saltmarsh","Kingsford"];'
G=[ # (écusson, anciens rattachés, nouveaux)
 (0,["Beacon Hill","Brightwater"],["Lanternhill","Lightkeeper","Beaconsfield","Watchlight","Shorelight","Glimmerhead","Lamplough"]),
 (1,["Summit Rock","Highfield","Thornhill"],["Highcrest","Cairngorm","Crestmoor","Skyridge","Upland","Scarfell","Ridgeline"]),
 (2,["Windward","Meridian","Eastbourne"],["Compass Rose","Westwind","Southerly","Trade Winds","Crosswind","Tramontane","Galeforce"]),
 (3,["Quarrystone","Greystone"],["Capstone","Archway","Ashlar","Keyarch","Lintel Row","Buttress","Voussoir"]),
 (4,["Ironwood","Sablewood","Ravenswood","Pinehurst","Ashford"],["Oakhurst","Elmstead","Yewcroft","Birchwood","Ashgrove","Rowan Hill","Heartwood"]),
 (5,["Harborview","Old Harbour","Tidewater","Deepwater","Fairhaven","Saltmarsh"],["Anchorage","Moorings","Safe Harbour","Keelhaven","Quayside","Slipway","Holdfast"]),
 (6,["Stonebridge","Two Rivers","Kingsford"],["Ferrybridge","Kingsbridge","Riverspan","Spanwell","Toll Bridge","Pontefract"]),
 (7,["Castlegate","Northgate"],["Towerhill","Belfry","Bastion","Rampart","Highkeep","Barbican","Portcullis"]),
 (8,["Kestrel","Falconer"],["Peregrine","Goshawk","Harrier","Gyrfalcon","Osprey","Sparrowhawk","Merlin Heath"]),
 (9,[],["Hourglass","Timekeeper","Sundial","Longcase","Eventide","Clepsydra"]),
 (10,["Sterling"],["Polaris","Lodestar","Pole Star","Northlight","Vega","Sirius Point"]),
 (11,["Copperfield","Cobalt"],["Flywheel","Ratchet Lane","Sprocket","Mainspring","Escapement","Gearhouse"]),
]
import re,json
old=json.loads(OLD[len('const NAME1='):-1])
tag={n:c for c,a,_ in G for n in a}
assert all(n in old for n in tag),[n for n in tag if n not in old]
new=[n for _,_,b in G for n in b]
allN=old+new
assert len(allN)==120 and len(set(allN))==120,(len(allN),len(set(allN)))
for n in new: tag[n]=[c for c,_,b in G if n in b][0]
e.rep(OLD,'const NAME1='+json.dumps(allN,ensure_ascii=False)+';\n/* écusson assorti à chaque nom, quand il y en a un (index dans CRESTS) */\nconst NAMECREST='+json.dumps(tag,ensure_ascii=False)+';')
e.rep("let fundName='';let fundCrest=Math.floor(Math.random()*12);\nfunction randName(){return pick2(NAME1)+' '+pick2(NAME2)}",
      "let fundName='';let fundCrest=Math.floor(Math.random()*12),crestPicked=false;\n"
      "/* le nom proposé emmène son écusson, sauf si le joueur en a déjà choisi un */\n"
      "function randName(){const a=pick2(NAME1);if(!crestPicked&&NAMECREST[a]!==undefined)fundCrest=NAMECREST[a];return a+' '+pick2(NAME2)}")
e.rep("document.getElementById('shuffle').onclick=()=>{fundName=randName();inp.value=fundName};\n app.querySelectorAll('[data-c]').forEach(b=>b.onclick=()=>{fundCrest=+b.dataset.c;",
      "document.getElementById('shuffle').onclick=()=>{fundName=randName();inp.value=fundName;\n   app.querySelectorAll('[data-c]').forEach(z=>z.classList.toggle('on',+z.dataset.c===fundCrest))};\n app.querySelectorAll('[data-c]').forEach(b=>b.onclick=()=>{fundCrest=+b.dataset.c;crestPicked=true;")
# nom long : la saisie débordait (« Trade Winds Discretionary M… », capture 380 px) ; on réduit le corps
e.rep(" inp.oninput=()=>{fundName=inp.value};",
      " const fitN=()=>{inp.style.fontSize='';const w=inp.clientWidth,sw=inp.scrollWidth;\n  if(w>0&&sw>w)inp.style.fontSize=(parseFloat(getComputedStyle(inp).fontSize)*w/sw*0.97).toFixed(1)+'px'};\n fitN();\n inp.oninput=()=>{fundName=inp.value;fitN()};")
e.rep("fundName=randName();inp.value=fundName;\n","fundName=randName();inp.value=fundName;fitN();\n")
e.done("lot 34 — noms de fonds x3 et ecusson assorti")
