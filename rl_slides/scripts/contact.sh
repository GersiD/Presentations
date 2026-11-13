#!/bin/sh
# contact.sh <build-subdir> [per-sheet=12]: tile build/<dir>/png pages into build/<dir>/sheet-N.png for quick review
cd "$(dirname "$0")/../build/$1/png" || exit 1
per=${2:-12}; i=0; set -- $(/bin/ls page-*.png)
while [ $# -gt 0 ]; do
  i=$((i+1)); batch=""
  for _ in $(seq $per); do [ $# -gt 0 ] && { batch="$batch $1"; shift; }; done
  magick montage $batch -tile 3x -geometry 520x390+4+4 -background '#777' ../sheet-$i.png 2>/dev/null
  echo "build/$(basename $(dirname $PWD))/sheet-$i.png"
done
