#!/bin/bash
# lance runner.js par tranches de 15 parties (jsdom fuit un peu de mémoire)
plan=$1; out=$2
while [ ! -f $out.fin ]; do timeout 900 node "$(dirname "$0")/runner.js" $plan $out 15 || echo "tranche interrompue $?" >> $out.log; done
