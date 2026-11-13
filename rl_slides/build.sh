#!/bin/sh
# Usage:
#   ./build.sh                 build the full deck -> main.pdf, pages in build/main/png/
#   ./build.sh 03-value [...]  build only those section files -> build/<first>/<first>.pdf, pages in build/<first>/png/
# Separate outdirs per section so parallel builds do not collide.
cd "$(dirname "$0")"
if [ $# -eq 0 ]; then
  name=main; out=build/main; src=main.tex
else
  name=$1; out=build/$1; mkdir -p "$out"
  { printf '%s\n' '\input{preamble}' '\begin{document}'
    for s in "$@"; do printf '\\input{sections/%s}\n' "$s"; done
    printf '%s\n' '\end{document}'; } > "$out/$name.tex"
  src=$out/$name.tex
fi
mkdir -p "$out"
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir="$out" -jobname="$name" "$src" >"$out/latexmk.out" 2>&1 \
  || { grep -n '^!' -A6 "$out/$name.log" | head -40; echo BUILD FAILED; exit 1; }
[ "$name" = main ] && cp "$out/main.pdf" main.pdf
rm -rf "$out/png" && mkdir -p "$out/png"
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r110 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 \
  -sOutputFile="$out/png/page-%02d.png" "$out/$name.pdf"
grep -E 'Overfull \\[hv]box \(([1-9][0-9]+|[3-9])\.' "$out/$name.log" | head -20
echo "OK: $out/$name.pdf, $(ls "$out/png" | wc -l | tr -d ' ') pages in $out/png/"
