#!/usr/bin/env bash
# Places voice lines on their cues, ducks the score under them, and muxes with the picture.
#   bash audio/mix.sh            (expects audio/01.wav ... audio/16.wav and out/lawdeck-1080p.mp4)
set -euo pipefail
cd "$(dirname "$0")/.."
CUES=(0.35 1.15 1.95 3.75 5.65 8.3 16.8 25.3 33.8 42.3 50.3 56.4 58.2 59.9 64.8 66.3)
inputs=(); filters=""; labels=""
for i in "${!CUES[@]}"; do
  f=$(printf "audio/%02d.wav" $((i+1)))
  [ -f "$f" ] || { echo "missing $f"; exit 1; }
  ms=$(python3 -c "print(int(${CUES[$i]}*1000))")
  inputs+=(-i "$f")
  filters+="[$((i+2)):a]aresample=48000,aformat=channel_layouts=stereo,silenceremove=start_periods=1:start_threshold=-45dB,adelay=${ms}|${ms}[v$i];"
  labels+="[v$i]"
done
ffmpeg -y -loglevel error -i out/lawdeck-1080p.mp4 -i audio/score.wav "${inputs[@]}" -filter_complex \
  "${filters}${labels}amix=inputs=${#CUES[@]}:normalize=0,apad,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,volume=1.6[vo];[vo]asplit[vo1][vo2];\
   [1:a]volume=0.8[sc];[sc][vo1]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=350[bed];\
   [bed][vo2]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1:LRA=9[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest out/lawdeck-final.mp4
echo "wrote out/lawdeck-final.mp4"
