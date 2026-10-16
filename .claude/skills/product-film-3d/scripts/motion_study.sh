#!/usr/bin/env bash
# Study a reference commercial: contact sheets + full-res frames + greyscale composition refs.
# FOR INTERNAL STUDY AND IMAGE-COMPOSITION REFERENCES ONLY. Never upload third-party footage
# to a video model as @video: it is flagged as "Protected content". Rebuild the motion as a
# blockout instead (blockout_scene.js).
# usage: motion_study.sh ref.mp4 outdir "4.8 6.3 11.5 13.0 14.3"
set -e; REF=$1; OUT=$2; TIMES=$3; mkdir -p "$OUT"
ffmpeg -v error -y -i "$REF" -vf "fps=2,scale=320:-1,drawtext=text='%{pts\:hms}':x=5:y=5:fontsize=18:fontcolor=white:box=1:boxcolor=black" "$OUT/s_%03d.png"
ffmpeg -v error -y -pattern_type glob -i "$OUT/s_*.png" -vf tile=6x8 "$OUT/contact.png"; rm "$OUT"/s_*.png
for t in $TIMES; do
  ffmpeg -v error -y -ss "$t" -i "$REF" -frames:v 1 -vf "scale=2560:-1:flags=lanczos" "$OUT/frame_$t.png"
  ffmpeg -v error -y -i "$OUT/frame_$t.png" -vf format=gray "$OUT/frame_${t}_GRAY.png"
done
echo "contact sheet + frames in $OUT (fine sheets: add -ss/-t and fps=6..8 around a cut)"
