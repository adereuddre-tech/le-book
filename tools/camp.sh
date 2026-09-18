#!/bin/bash
# Campagne : n graines x 3 styles sur une copie figée. Usage : camp.sh <fichier> <sortie> <n>
f=$1; out=$2; n=$3; : > $out
for s in $(seq 1 $n); do for p in syst fonda flux; do
  echo -n "$p " >> $out; node tools/econ.js --file $f --seed $s --prof $p >> $out
done; done
echo FIN >> $out
