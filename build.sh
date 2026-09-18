#!/bin/sh
# Reconstruit index.html à partir du fichier publié + les lots de patchs, dans l'ordre.
set -e
cd "$(dirname "$0")"
cp base.html index.html
for f in patches/[0-9]*.py; do printf '%s : ' "$f"; python3 "$f"; done
wc -c index.html
