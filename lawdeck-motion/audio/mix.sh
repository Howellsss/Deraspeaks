#!/usr/bin/env bash
# Places voice lines at their cue times, ducks the score under them, and muxes with the picture.
#   bash audio/mix.sh                      (expects audio/01.wav ... audio/12.wav)
set -euo pipefail
cd "$(dirname "$0")/.."
CUES=(1.0 7.0 11.5 15.0 25.0 35.0 44.0 54.0 65.0 74.0 82.2 84.0)
inputs=(); filters=""; labels=""
for i in "${!CUES[@]}"; do
  f=$(printf "audio/%02d.wav" $((i+1)))
  [ -f "$f" ] || { echo "missing $f"; exit 1; }
  ms=$(python3 -c "print(int(${CUES[$i]}*1000))")
  inputs+=(-i "$f")
  filters+="[$((i+2)):a]aresample=48000,aformat=channel_layouts=stereo,adelay=${ms}|${ms}[v$i];"
  labels+="[v$i]"
done
ffmpeg -y -loglevel error -i out/lawdeck-1080p.mp4 -i audio/score.wav "${inputs[@]}" -filter_complex \
  "${filters}${labels}amix=inputs=${#CUES[@]}:normalize=0,apad[vo];[vo]asplit[vo1][vo2];\
   [1:a][vo1]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=600[bed];\
   [bed][vo2]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest out/lawdeck-final.mp4
echo "wrote out/lawdeck-final.mp4"
