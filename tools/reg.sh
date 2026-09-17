#!/bin/bash
# Régression : 9 combinaisons taille × univers × (actif, sage), styles en rotation.
# Usage : tools/reg.sh [fichier] [sortie]   puis   python3 tools/summ.py <sortie>
# Lancer détaché si la session limite la durée des commandes :
#   setsid nohup tools/reg.sh index.html r_reg.txt >/dev/null 2>&1 < /dev/null &
f=${1:-index.html}; out=${2:-r_reg.txt}; : > $out; i=0; D=$(dirname "$0")
for sz in small mid mega; do for u in fin com ext; do for sg in "" "--sage"; do i=$((i+1)); p=$(echo syst fonda flux | cut -d' ' -f$(( (i%3)+1 )))
echo "$p ${sg:-actif} $(node $D/play.js $f $((i*13)) --size $sz --univ $u --prof $p --dur normal $sg)" >> $out; done; done; done; echo FIN >> $out
